from flask import Flask, render_template, request
import csv
import os
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTACT_FILE = os.path.join(BASE_DIR, "contact_submissions.csv")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST"])
def contact():
    full_name = request.form.get("full-name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    organisation = request.form.get("organisation", "").strip()
    message = request.form.get("message", "").strip()

    file_exists = os.path.exists(CONTACT_FILE)
    with open(CONTACT_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "full_name", "email", "phone", "organisation", "message"])
        writer.writerow([
            datetime.utcnow().isoformat(),
            full_name,
            email,
            phone,
            organisation,
            message
        ])

    return render_template("thank_you.html", full_name=full_name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
