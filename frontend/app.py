import requests
from flask import Flask, render_template, request


app = Flask(__name__)
BACKEND_URL = "http://backend:5000"


@app.route("/", methods=["GET", "POST"])
@app.route("/faq", methods=["GET", "POST"])
def faq():
    error = None
    success = None

    if request.method == "POST":
        message = request.form.get("message", "").strip()
        if not message:
            error = "Le message est obligatoire."
        elif len(message) > 500:
            error = "Le message ne peut pas dépasser 500 caractères."
        else:
            try:
                response = requests.post(
                    f"{BACKEND_URL}/faq",
                    json={"message": message},
                    timeout=5,
                )
                if response.status_code == 201:
                    success = "Message ajouté à la FAQ."
                else:
                    error = response.json().get(
                        "error", "Le backend n'a pas accepté le message."
                    )
            except requests.RequestException as exc:
                app.logger.error("Impossible de joindre le backend: %s", exc)
                error = "Le backend est indisponible. Réessaie plus tard."

    return render_template("faq.html", error=error, success=success)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=15556)