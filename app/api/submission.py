"""
WA错题本 - 提交与错题 API
"""

import asyncio
from flask import Blueprint, jsonify, request
from sqlalchemy import select

from app.models.database import async_session
from app.models.submission import Submission, Platform, Status
from app.models.mistake import Mistake
from app.schemas.submission import (
    SubmissionCreateRequestSchema,
    SubmissionResponseSchema,
    MistakeDetailResponseSchema,
)
from app.services.scraper import scraper
from app.services.analyzer import analyzer
from app.utils.oj_detector import detect_platform, parse_submission_url

bp = Blueprint("submission", __name__, url_prefix="/api/v1")


def run_async(func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(func())


@bp.route("/submissions", methods=["POST"])
def create_mistake():
    data = request.get_json()
    schema = SubmissionCreateRequestSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400

    url = data["url"]
    platform_str = data["platform"]
    manual_code = data.get("code", "")
    manual_problem_name = data.get("problem_name", "")

    detected = detect_platform(url)
    if detected is None:
        return jsonify({"error": "无法识别的 OJ 平台链接"}), 400

    if detected != platform_str:
        return jsonify({
            "error": f"URL 属于 {detected} 平台，但你选择了 {platform_str}"
        }), 400

    async def _create():
        async with async_session() as session:
            existing = await session.execute(
                select(Submission).where(Submission.submission_url == url)
            )
            if existing.scalar_one_or_none():
                return {"error": "该提交已被记录过"}, 409

            scraped = None
            fallback_reason = None
            if manual_code:
                # 用户已提供代码，跳过网络抓取
                try:
                    parsed = parse_submission_url(url, platform_str)
                    problem_id = parsed.contest_id or parsed.submission_id
                except Exception:
                    problem_id = ""
                scraped = {
                    "problem_id": problem_id,
                    "problem_name": manual_problem_name or "手动输入题目",
                    "problem_url": "",
                    "difficulty": None,
                    "code": manual_code,
                    "language": None,
                    "status": "WA",
                    "failed_test_case": None,
                }
            else:
                try:
                    scraped = await scraper.scrape_submission(url, platform_str)
                except Exception as e:
                    # 网络抓取失败：如果用户没提供代码，则失败
                    fallback_reason = str(e)

            if scraped is None:
                msg = f"抓取失败: {fallback_reason}"
                if not manual_code:
                    msg += '。你可以展开"手动粘贴代码"输入代码后重试。'
                return {"error": msg}, 502

            # 用户提供了题目名称时优先使用
            if manual_problem_name:
                scraped["problem_name"] = manual_problem_name

            platform = Platform(platform_str)
            submission = Submission(
                platform=platform,
                submission_url=url,
                problem_id=scraped["problem_id"],
                problem_name=scraped["problem_name"],
                problem_url=scraped.get("problem_url"),
                difficulty=scraped.get("difficulty"),
                code=scraped["code"],
                language=scraped.get("language"),
                status=Status(scraped.get("status", "WA")),
                failed_test_case=scraped.get("failed_test_case"),
            )
            session.add(submission)
            await session.flush()

            analysis = analyzer.analyze(
                code=submission.code,
                status=submission.status.value,
                problem_name=submission.problem_name,
            )

            mistake = Mistake(
                submission_id=submission.id,
                error_category=analysis["error_category"],
                error_severity=analysis["error_severity"],
                error_summary=analysis["error_summary"],
                error_detail=analysis["error_detail"],
                suggestion=analysis["suggestion"],
                hints=analysis["hints"],
            )
            session.add(mistake)
            await session.commit()
            await session.refresh(mistake)
            await session.refresh(submission)

            result = MistakeDetailResponseSchema().dump({
                **mistake.__dict__,
                "submission": submission,
            })
            return result, 201

    return run_async(_create)


@bp.route("/mistakes", methods=["GET"])
def list_mistakes():
    platform = request.args.get("platform")
    category = request.args.get("category")
    resolved = request.args.get("resolved")
    limit = int(request.args.get("limit", 20))
    offset = int(request.args.get("offset", 0))

    async def _list():
        async with async_session() as session:
            query = select(Mistake).join(Submission).order_by(Mistake.created_at.desc())

            if platform:
                query = query.where(Submission.platform == platform)
            if category:
                query = query.where(Mistake.error_category == category)
            if resolved is not None:
                query = query.where(Mistake.resolved == (resolved.lower() == "true"))

            query = query.offset(offset).limit(limit)

            result = await session.execute(query)
            mistakes = result.scalars().all()

            responses = []
            for m in mistakes:
                sub = await session.get(Submission, m.submission_id)
                data = m.__dict__.copy()
                if sub:
                    data["submission"] = sub
                responses.append(MistakeDetailResponseSchema().dump(data))

            return responses, 200

    return run_async(_list)


@bp.route("/mistakes/<int:mistake_id>", methods=["GET"])
def get_mistake_detail(mistake_id):
    async def _get():
        async with async_session() as session:
            mistake = await session.get(Mistake, mistake_id)
            if not mistake:
                return {"error": "错题不存在"}, 404

            sub = await session.get(Submission, mistake.submission_id)
            data = mistake.__dict__.copy()
            if sub:
                data["submission"] = sub
            return MistakeDetailResponseSchema().dump(data), 200

    return run_async(_get)


@bp.route("/mistakes/<int:mistake_id>/hint", methods=["POST"])
def get_next_hint(mistake_id):
    async def _hint():
        async with async_session() as session:
            mistake = await session.get(Mistake, mistake_id)
            if not mistake:
                return {"error": "错题不存在"}, 404

            hint_text, next_idx = analyzer.get_next_hint(
                mistake.hints or [],
                mistake.current_hint_index,
            )

            mistake.current_hint_index = next_idx
            await session.commit()

            return {
                "hint": hint_text,
                "index": next_idx,
                "remaining": max(0, len(mistake.hints or []) - next_idx),
            }, 200

    return run_async(_hint)


@bp.route("/mistakes/<int:mistake_id>/resolve", methods=["PATCH"])
def resolve_mistake(mistake_id):
    async def _resolve():
        from datetime import datetime
        async with async_session() as session:
            mistake = await session.get(Mistake, mistake_id)
            if not mistake:
                return {"error": "错题不存在"}, 404

            mistake.resolved = True
            mistake.resolved_at = datetime.utcnow()
            await session.commit()

            return {"message": "已标记为解决", "mistake_id": mistake_id}, 200

    return run_async(_resolve)


@bp.route("/mistakes/<int:mistake_id>", methods=["DELETE"])
def delete_mistake(mistake_id):
    async def _delete():
        async with async_session() as session:
            mistake = await session.get(Mistake, mistake_id)
            if not mistake:
                return {"error": "错题不存在"}, 404

            sub = await session.get(Submission, mistake.submission_id)
            if sub:
                await session.delete(sub)
            await session.delete(mistake)
            await session.commit()

            return "", 204

    return run_async(_delete)
