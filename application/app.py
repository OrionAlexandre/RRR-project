from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import datetime


db = SQLAlchemy()

annee = datetime.now().year


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./database.db"  # Création de la base de données.
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///./database_{annee}.db"  # Création de la base de données.

    db.init_app(app)

    # Enregistrement des chemins d'urls dans l'application
    from routes import enregistrer_routes

    enregistrer_routes(app, db)

    migrate = Migrate(app, db)

    return app
