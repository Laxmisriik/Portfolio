from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__, template_folder="templates")
CORS(app)

# Environment variables (from Render)
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")


# ✅ HOME PAGE ROUTE (IMPORTANT)
@app.route("/")
def home():
    return render_template("index.html")


# ✅ CONTACT FORM EMAIL ROUTE
@app.route("/send", methods=["POST"])
def send_email():
    try:
        data = request.json

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        # Email content
        msg = MIMEText(
            f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        )
        msg["Subject"] = "Portfolio Contact Form"
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        # Gmail SMTP server
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()

        return jsonify({"status": "success"})

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error"})


# ✅ REQUIRED FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)