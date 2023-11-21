import os

from flask import send_from_directory
from flask_script import Manager

from config import BASE_DIR
from grimm import create_app, logger

basedir = os.path.abspath(os.path.dirname(__file__))
app = create_app()
manager = Manager(app)


@app.errorhandler(404)
def page_not_found(e):
    logger.warning('Server 404.')


@app.errorhandler(500)
def internal_server_error(e):
    logger.error('Server 500.')


@app.errorhandler(503)
def server_unavailable(e):
    logger.error('Server 503.')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(BASE_DIR, 'static/favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    manager.run()
