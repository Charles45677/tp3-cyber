from flask import Flask, jsonify, request

from database import add_faq_message, initialize_database


app = Flask(__name__)
initialize_database()


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/faq")
def create_faq_message():
    if not request.is_json:
        return jsonify(error="Le contenu doit être au format JSON."), 415

    data = request.get_json()
    message = data.get("message") if isinstance(data, dict) else None
    if not isinstance(message, str) or not message.strip():
        return jsonify(error="Le message est obligatoire."), 400

    message = message.strip()
    if len(message) > 500:
        return jsonify(error="Le message ne peut pas dépasser 500 caractères."), 400

    add_faq_message(message)
    return jsonify(message="Message ajouté à la FAQ."), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)