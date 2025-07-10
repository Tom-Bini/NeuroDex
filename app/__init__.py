from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)

    from .models import User, Deck, Card, ReviewProgress, LoginCode

    with app.app_context():
        db.create_all()

    # 👇 Middleware défini juste après db.create_all()
    @app.before_request
    def set_fake_user():
        session["user_id"] = 1  # Utilisateur simulé temporairement

    return app