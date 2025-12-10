import os
import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError


db = SQLAlchemy()


def create_app(config_object="config.DevelopmentConfig"):
    app = Flask(__name__)

    # Database para
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")

    db_url = os.getenv(
        "DB_URL",
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}",
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        from . import routes  # noqa: F401

        retries = 5
        while retries > 0:
            try:
                db.create_all()
                print("Database created successfully")
                break
            except SQLAlchemyError as e:
                print(f"Failed to create database: {str(e)}")
                time.sleep(6)
                retries -= 1
    return app
