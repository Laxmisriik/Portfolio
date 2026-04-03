from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
CORS(app)

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

@app.route('/send', methods=['POST'])
def send_email():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    try:
        msg = MIMEText(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")
        msg['Subject'] = "Portfolio Contact"
        msg['From'] = EMAIL
        msg['To'] = EMAIL

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()

        return jsonify({"status": "success"})
    except Exception as e:
        print(e)
        return jsonify({"status": "error"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001)