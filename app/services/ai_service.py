import os
import json
import logging
from typing import List, Dict, Optional, Iterator
import requests

logger = logging.getLogger(__name__)

BAIDU2API_BASE = "http://127.0.0.1:8000"
DDG2API_BASE = "http://127.0.0.1:3000"

# 反代服务不可用时的兜底模型清单（确保前端始终能展示）
BAIDU_FALLBACK_MODELS = [
    {"id": "ernie-4.0", "name": "ernie-4.0"},
    {"id": "ernie-3.5", "name": "ernie-3.5"},
    {"id": "ernie-speed", "name": "ernie-speed"},
    {"id": "ernie-lite", "name": "ernie-lite"},
    {"id": "ernie-tiny", "name": "ernie-tiny"},
]
DDG_FALLBACK_MODELS = [
    {"id": "duckduckgo", "name": "DuckDuckGo AI"},
]


def _fetch_models(base_url: str, fallback: List[Dict]) -> List[Dict]:
    try:
        resp = requests.get(f"{base_url}/v1/models", timeout=2.5)
        resp.raise_for_status()
        data = resp.json()
        models = data.get("data", [])
        if models:
            return models
        logger.warning(f"{base_url} 返回空模型列表，使用兜底")
        return fallback
    except Exception as e:
        logger.warning(f"反代不可达 {base_url}（{type(e).__name__}），使用兜底模型")
        return fallback


def get_baidu_models() -> List[Dict]:
    models = _fetch_models(BAIDU2API_BASE, BAIDU_FALLBACK_MODELS)
    return [{**m, "provider": "baidu", "provider_name": "百度"} for m in models]


def get_ddg_models() -> List[Dict]:
    models = _fetch_models(DDG2API_BASE, DDG_FALLBACK_MODELS)
    return [{**m, "provider": "ddg", "provider_name": "DuckDuckGo"} for m in models]


def get_test_models() -> List[Dict]:
    return [
        {"id": "test-echo", "name": "Echo 测试", "provider": "test", "provider_name": "测试"},
    ]


def get_custom_models() -> List[Dict]:
    custom = os.environ.get("CUSTOM_MODELS", "")
    if not custom:
        return []
    result = []
    for item in custom.split(";"):
        item = item.strip()
        if not item:
            continue
        parts = item.split(",")
        if len(parts) >= 2:
            result.append({
                "id": parts[0],
                "name": parts[1],
                "provider": "custom",
                "provider_name": "自定义",
            })
    return result


def get_models() -> List[Dict]:
    return get_baidu_models() + get_ddg_models() + get_custom_models()


def chat_baidu(model_id: str, messages: List[Dict]) -> str:
    """调用本地 baidu-2api 反代"""
    try:
        resp = requests.post(
            f"{BAIDU2API_BASE}/v1/chat/completions",
            json={"model": model_id, "messages": messages, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"baidu-2api 调用失败: {e}")
        return f"【百度 AI 错误】{str(e)}"


def chat_ddg(model_id: str, messages: List[Dict]) -> str:
    """调用本地 DDG2API 反代"""
    try:
        resp = requests.post(
            f"{DDG2API_BASE}/v1/chat/completions",
            json={"model": model_id, "messages": messages, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"DDG2API 调用失败: {e}")
        return f"【DuckDuckGo AI 错误】{str(e)}"


def chat_test(messages: List[Dict]) -> str:
    if not messages:
        return "【Echo】没有收到消息。"
    content = messages[-1].get("content", "")
    return f"【Echo 测试】后端连接正常。你发送了：{content}"


def chat_custom(model_id: str, messages: List[Dict], base_url: str, api_key: str) -> str:
    try:
        url = base_url.rstrip("/") + "/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        data = {
            "model": model_id,
            "messages": messages,
            "stream": False,
        }
        resp = requests.post(url, headers=headers, json=data, timeout=120)
        resp.raise_for_status()
        result = resp.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"自定义 API 调用失败: {e}")
        return f"【自定义 API 错误】{str(e)}"


def chat(model_id: str, messages: List[Dict], api_key: Optional[str] = None, base_url: Optional[str] = None, secret_key: Optional[str] = None) -> str:
    if model_id in [m["id"] for m in get_baidu_models()]:
        return chat_baidu(model_id, messages)
    elif model_id in [m["id"] for m in get_ddg_models()]:
        return chat_ddg(model_id, messages)
    else:
        if not api_key or not base_url:
            return "【错误】自定义模型需要配置 API Key 和 Base URL。"
        return chat_custom(model_id, messages, base_url, api_key)


def chat_stream(model_id: str, messages: List[Dict], api_key: Optional[str] = None, base_url: Optional[str] = None, secret_key: Optional[str] = None) -> Iterator[str]:
    baidu_ids = [m["id"] for m in get_baidu_models()]
    ddg_ids = [m["id"] for m in get_ddg_models()]

    if model_id in baidu_ids:
        target_url = f"{BAIDU2API_BASE}/v1/chat/completions"
        payload = {"model": model_id, "messages": messages, "stream": True}
        headers = {"Content-Type": "application/json"}
    elif model_id in ddg_ids:
        target_url = f"{DDG2API_BASE}/v1/chat/completions"
        payload = {"model": model_id, "messages": messages, "stream": True}
        headers = {"Content-Type": "application/json"}
    else:
        if not api_key or not base_url:
            yield f"data: {json.dumps({'error': '自定义模型需要配置 API Key 和 Base URL'})}\n\n"
            yield "data: [DONE]\n\n"
            return
        target_url = base_url.rstrip("/") + "/chat/completions"
        payload = {"model": model_id, "messages": messages, "stream": True}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    try:
        with requests.post(target_url, headers=headers, json=payload, stream=True, timeout=120) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line:
                    yield line.decode("utf-8") + "\n\n"
    except Exception as e:
        logger.error(f"流式调用失败: {e}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
        yield "data: [DONE]\n\n"
