"""
WA错题本 - 统计 API
"""

import asyncio
from flask import Blueprint, jsonify

from app.services.stats import get_overview_stats, CATEGORY_NAMES

bp = Blueprint("stats", __name__, url_prefix="/api/v1")


def run_async(func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(func())


@bp.route("/stats", methods=["GET"])
def get_stats():
    async def _stats():
        data = await get_overview_stats()
        return data, 200

    return run_async(_stats)


@bp.route("/stats/categories", methods=["GET"])
def get_category_list():
    return jsonify(CATEGORY_NAMES), 200
