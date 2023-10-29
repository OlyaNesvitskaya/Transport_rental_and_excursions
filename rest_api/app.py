import json
import os
import sys
from flask import Flask, jsonify
from flask_migrate import Migrate
import rest_api.config as config
from rest_api.rest.endpoints import api_app
from rest_api.models.database import db

migrate = Migrate()

sys.path.append(os.path.join(os.path.dirname(__file__), 'rest_api'))


def create_app(config_class=config.DevelopmentConfig):
    base_dir = os.path.dirname(__file__)
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    migrate.init_app(app, db, directory=os.path.join(base_dir, 'migrations'))

    with app.app_context():
        db.create_all()
        db.session.commit()

    app.register_blueprint(api_app)

    @app.errorhandler(404)
    @app.errorhandler(500)
    def invalid_api_usage(e):
        return jsonify({"message": 'Not found'}), 400

    return app




