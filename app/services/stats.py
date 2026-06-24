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

        return {
            "total_mistakes": total,
            "by_category": by_category,
            "by_platform": by_platform,
            "by_severity": by_severity,
            "recent_trend": recent_trend,
        }


CATEGORY_NAMES = {
    "logic_error": "逻辑错误",
    "boundary": "边界条件",
    "overflow": "整数溢出",
    "uninitialized": "未初始化",
    "complexity": "复杂度超限",
    "precision": "精度问题",
    "io_format": "输入输出格式",
    "memory": "内存超限",
    "typo": "拼写笔误",
    "modular": "取模错误",
    "graph": "图论细节",
    "dp": "DP状态/转移",
}
