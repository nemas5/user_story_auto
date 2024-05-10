import json
import os

from flask import Flask, render_template, session

from api.blueprints import list_of_blueprints


def reg_blueprints(application: Flask) -> None:
    for bp, url_prefix in list_of_blueprints:
        application.register_blueprint(bp, url_prefix=url_prefix)


def get_app() -> Flask:
    application = Flask(__name__)
    reg_blueprints(application)
    return application


app = get_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
