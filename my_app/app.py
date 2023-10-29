import os
from flask import Flask, render_template
import my_app.config as config
from my_app.views.views import web_app


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_TEMPLATES = os.path.join(APP_ROOT, 'templates', 'web')
APP_STATIC = os.path.join(APP_ROOT, 'static')


def create_app(name='web_app', config_class=config.Config):
    app = Flask(name, template_folder=APP_TEMPLATES, static_folder=APP_STATIC,
                static_url_path='/my_app/static/')
    app.config.from_object(config_class)
    app.register_blueprint(web_app)

    @app.errorhandler(404)
    @app.errorhandler(500)
    def not_found(e):
        return render_template("404.html", context={'title': 'error'})

    return app
