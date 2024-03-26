import os
import sys
from flask import Flask, jsonify
from flask_migrate import Migrate

from rest_api.log import logger
import rest_api.config as config
from rest_api.rest.endpoints import api_app
from rest_api.models.database import db

migrate = Migrate()

sys.path.append(os.path.join(os.path.dirname(__file__), 'rest_api'))
API_ROOT = os.path.dirname(os.path.abspath(__file__))


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


if __name__ == "__main__":
    api_app = create_app()
    logger.info("Start RestAPI : listen %s:%s" % ('127.0.0.1', 5000))
    api_app.run(host='127.0.0.1', port=5000)


