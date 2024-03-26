import os
from flask import Flask, render_template
from flask_talisman import Talisman

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

    talisman = Talisman(app)

    csp = {
        'default-src': [
            '\'self\''
        ],
        'script-src': [
            '\'self\'',
            'https://ajax.googleapis.com',
        ],
        'style-src': [
            '\'self\'',
            'https://cdn.jsdelivr.net',
            'https://maxcdn.bootstrapcdn.com'
        ],
        'font-src': ['\'self\'', 'https://maxcdn.bootstrapcdn.com']
    }

    hsts = {
        'max-age': 31536000,
        'includeSubDomains': True
    }

    talisman.force_https = True
    talisman.force_file_save = True
    talisman.x_xss_protection = True
    talisman.session_cookie_secure = True
    talisman.session_cookie_samesite = 'Lax'

    talisman.content_security_policy = csp
    talisman.strict_transport_security = hsts

    return app


if __name__ == '__main__':
    web_app = create_app()
    web_app.run(host='127.0.0.1', port=5009, ssl_context="adhoc")
