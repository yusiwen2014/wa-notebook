"""
WA错题本 - 聊天接口
支持与 AI 对话、代码分析、学习小结生成
"""

import asyncio
from collections import Counter

from flask import Blueprint, request, jsonify

from app.services.ai_client import AIAnalyzerClient, ai_client
from app.models.database import async_session
from app.models.mistake import Mistake


def run_async(func):
    """为每个请求创建独立事件循环执行异步任务"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(func())


def _fetch_mistakes():
    """获取所有错题数据"""
    async def _do():
        async with async_session() as session:
            from sqlalchemy import select
            result = await session.execute(select(Mistake))
            return result.scalars().all()
    return run_async(_do)


chat_bp = Blueprint('chat', __name__, url_prefix='/api/v1/chat')


@chat_bp.route('', methods=['POST'])
def chat():
    """AI 对话接口 - 支持多轮对话"""
    data = request.get_json(silent=True) or {}
    messages = data.get('messages', [])
    ai_config = data.get('ai_config') or {}

    if not messages:
        return jsonify({'error': 'messages 不能为空'}), 400

    client = _build_client(ai_config)

    def _do_chat():
        return client.chat(messages)

    try:
        result = run_async(_do_chat)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/analyze-code', methods=['POST'])
def analyze_code():
    """快速代码分析（聊天式）- 粘贴代码直接分析"""
    data = request.get_json(silent=True) or {}
    code = data.get('code', '')
    ai_config = data.get('ai_config') or {}

    if not code:
        return jsonify({'error': 'code 不能为空'}), 400

    client = _build_client(ai_config)

    def _do_analyze():
        return client.analyze(code, 'WA', '', None)

    try:
        result = run_async(_do_analyze)
        response_text = (
            f"**错误分类**: {result['error_category']}\n\n"
            f"**严重程度**: {result['error_severity']}\n\n"
            f"**错误概述**: {result['error_summary']}\n\n"
            f"**详细分析**: {result['error_detail']}\n\n"
            f"**修改建议**: {result['suggestion']}"
        )
        return jsonify({ 'reply': response_text, 'analysis': result })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/summary', methods=['POST'])
def generate_summary():
    """基于错题历史生成学习小结"""
    ai_config = request.get_json(silent=True) or {}

    # 获取所有错题
    try:
        mistakes = _fetch_mistakes()
    except Exception as e:
        return jsonify({'error': f'获取错题数据失败: {e}'}), 500

    if not mistakes:
        return jsonify({
            'reply': '📋 **学习小结**\n\n目前还没有错题记录哦！先提交几道 WA 的题目，我就能帮你生成详细的学习小结了。',
        })

    # 统计数据
    categories = Counter(m.error_category for m in mistakes)
    severities = Counter(m.error_severity for m in mistakes)
    resolved_count = sum(1 for m in mistakes if m.resolved)
    total = len(mistakes)

    # 构建数据摘要
    cat_lines = []
    for cat, count in categories.most_common():
        cat_lines.append(f"- {cat}: {count} 次")
    detail_lines = [m.error_summary for m in mistakes if m.error_summary]

    data_summary = (
        f"总错题数: {total}\n"
        f"已解决: {resolved_count} / 未解决: {total - resolved_count}\n"
        f"深层问题: {severities.get('high', 0)} / 低级错误: {severities.get('low', 0)}\n"
        f"\n错误分类分布:\n" + '\n'.join(cat_lines) +
        f"\n\n各题错误概述:\n" + '\n'.join(f"{i+1}. {d}" for i, d in enumerate(detail_lines[:20]))
    )

    client = _build_client(ai_config)

    try:
        # mock 模式下 generate_summary 是同步的，直接调用
        if not ai_config.get('api_key') or ai_config.get('provider') == 'mock':
            result = client.generate_summary(data_summary)
        else:
            def _do_summary():
                return client.generate_summary(data_summary)
            result = run_async(_do_summary)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def _build_client(ai_config):
    """根据配置构建 AI 客户端"""
    if ai_config.get('provider') and ai_config.get('provider') != 'mock' and ai_config.get('api_key'):
        return AIAnalyzerClient(
            provider=ai_config.get('provider', 'openai'),
            api_key=ai_config.get('api_key'),
            base_url=ai_config.get('base_url'),
            model=ai_config.get('model'),
            prompt=ai_config.get('prompt'),
        )
    return ai_client
