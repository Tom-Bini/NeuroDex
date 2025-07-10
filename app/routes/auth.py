# app/routes/auth.py
from flask import Blueprint, request, render_template, redirect, url_for, flash
from .. import db
from ..models import LoginCode
from datetime import datetime, timezone, timedelta
import random
import smtplib
from email.message import EmailMessage

auth_bp = Blueprint('auth', __name__)

def send_code_email(recipient_email, code):
    # 🧪 version simple SMTP (à adapter selon ton provider ou Gmail)
    EMAIL_ADDRESS = "ton_email@example.com"
    EMAIL_PASSWORD = "ton_mdp"

    msg = EmailMessage()
    msg["Subject"] = "Votre code de connexion NeuroDex"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient_email
    msg.set_content(f"Votre code : {code}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        code = f"{random.randint(100000, 999999)}"

        # Supprimer les anciens codes de plus de 10 min
        expiration = datetime.now(timezone.utc) - timedelta(minutes=10)
        LoginCode.query.filter(LoginCode.created_at < expiration).delete()

        login_code = LoginCode(email=email, code=code)
        db.session.add(login_code)
        db.session.commit()

        send_code_email(email, code)

        flash("Un code de connexion vous a été envoyé par email.")
        return redirect(url_for("auth.verify"))

    return render_template("login.html")
