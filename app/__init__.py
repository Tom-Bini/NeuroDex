from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)

    from .models import User, Deck, Card, ReviewProgress  # on les importe ici
    
    with app.app_context():
        db.create_all()  # crée les tables

    return app
