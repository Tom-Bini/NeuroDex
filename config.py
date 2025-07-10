import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'neurodex.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'change-this-later'
