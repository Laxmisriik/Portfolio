from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__, template_folder="templates")
CORS(app)

# ENV VARIABLES
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def send_email():
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({"status": "error", "message": "Missing fields"})

        msg = MIMEText(
            f"New message from your portfolio:\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n\n"
            f"Message:\n{message}"
        )

        msg["Subject"] = "Portfolio Contact Form"
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        # ✅ FIXED SMTP (with timeout)
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()

        return jsonify({"status": "success"})

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)