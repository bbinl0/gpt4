import os
from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": os.getenv("CORS_ORIGIN", "*")}})

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def handler():
    if request.method == 'OPTIONS':
        return '', 204

    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
    elif request.method == 'GET':
        data = request.args.to_dict()
    else:
        return jsonify({"error": "Method not allowed"}), 405

    messages = data.get('messages')
    input_text = data.get('input')
    system_prompt = data.get('system')
    model = data.get('model', 'gpt-4o-mini')
    temperature = float(data.get('temperature', 0.7))
    max_tokens = int(data.get('max_tokens')) if data.get('max_tokens') else None

    final_messages = []
    if messages and isinstance(messages, list):
        final_messages = messages
    else:
        if system_prompt:
            final_messages.append({"role": "system", "content": system_prompt})
        if input_text:
            final_messages.append({"role": "user", "content": str(input_text)})

    if not final_messages:
        return jsonify({"error": "Provide 'messages' array or 'input' string"}), 400

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model=model,
            messages=final_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        choice = completion.choices[0].message if completion.choices else None
        message_dict = {"role": choice.role, "content": choice.content} if choice else None
        return jsonify({
            "id": completion.id,
            "created": completion.created,
            "model": completion.model,
            "usage": completion.usage,
            "message": message_dict
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
