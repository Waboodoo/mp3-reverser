from flask import Flask

from app.main.cleanup import start_cleanup_scheduler

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

from app.resources import api


start_cleanup_scheduler('sessions')
