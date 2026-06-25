from collections import Counter
from datetime import datetime, timedelta
from app.models.mistake import Mistake
from sqlalchemy import func, select
from app.models.database import async_session


async def get_overview_stats() -> dict:
    async with async_session() as session:
        total_result = await session.execute(
            select(func.count()).select_from(Mistake)
        )
        total = total_result.scalar() or 0

        cat_result = await session.execute(
            select(Mistake.error_category, func.count())
            .group_by(Mistake.error_category)
        )
        by_category = dict(cat_result.all())

        from app.models.submission import Submission
        plat_result = await session.execute(
            select(Submission.platform, func.count())
            .join(Mistake, Mistake.submission_id == Submission.id)
            .group_by(Submission.platform)
        )
        by_platform = {}
        for row in plat_result.all():
            platform_value = row[0].value if hasattr(row[0], "value") else str(row[0])
            by_platform[platform_value] = row[1]

        sev_result = await session.execute(
            select(Mistake.error_severity, func.count())
            .group_by(Mistake.error_severity)
        )
        by_severity = dict(sev_result.all())

        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        trend_result = await session.execute(
            select(
                func.date(Mistake.created_at).label("date"),
                func.count().label("count"),
            )
            .where(Mistake.created_at >= seven_days_ago)
            .group_by(func.date(Mistake.created_at))
            .order_by(func.date(Mistake.created_at))
        )
        recent_trend = [
            {"date": str(row.date), "count": row.count}
            for row in trend_result.all()
        ]

        resolved_result = await session.execute(
            select(func.count()).select_from(Mistake).where(Mistake.resolved == True)
        )
        resolved_count = resolved_result.scalar() or 0
        unresolved_count = total - resolved_count

        return {
            "total_mistakes": total,
            "resolved_count": resolved_count,
            "unresolved_count": unresolved_count,
            "by_category": by_category,
            "by_platform": by_platform,
            "by_severity": by_severity,
            "recent_trend": recent_trend,
        }


# v0.0.3 新的分类体系
CATEGORY_NAMES = {
    "CE": "CE 编译错误",
    "RE_div0": "RE 除以零",
    "RE_oob": "RE 越界访问",
    "WA_logic": "WA 思路错误",
    "WA_code": "WA 代码错误",
    "TLE": "TLE 时间超限",
    "MLE": "MLE 内存超限",
}
