from flask import Blueprint, request, Response, jsonify, stream_with_context
from app.services import ai_service

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/models", methods=["GET"])
def list_models():
    models = ai_service.get_models()
    return jsonify({"object": "list", "data": models})


@ai_bp.route("/chat/completions", methods=["POST"])
def chat_completions():
    data = request.get_json(force=True)
    model_id = data.get("model", "public-pollinations")
    messages = data.get("messages", [])
    stream = data.get("stream", False)
    api_key = data.get("api_key")
    secret_key = data.get("secret_key")
    base_url = data.get("base_url")

    if not messages:
        return jsonify({"error": "messages 不能为空"}), 400

    if stream:
        def generate():
            for chunk in ai_service.chat_stream(model_id, messages, api_key, base_url, secret_key):
                yield chunk
        return Response(stream_with_context(generate()), mimetype="text/plain")
    else:
        content = ai_service.chat(model_id, messages, api_key, base_url, secret_key)
        return jsonify({
            "id": "chatcmpl-local",
            "object": "chat.completion",
            "model": model_id,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop"
            }]
        })
