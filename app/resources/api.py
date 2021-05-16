import os

from flask import abort
from flask import request
from flask import send_from_directory

from app import app
from app.main.RequestParameters import RequestParameters
from app.main.Session import Session
from app.main.Session import Status
from app.main.exceptions.exceptions import InvalidSessionIdError

API_PATH_PREFIX = '/api'


def _get_session(session_id):
    try:
        return Session(session_id)
    except InvalidSessionIdError:
        abort(404)


def _get_status_url(session_id):
    return API_PATH_PREFIX + '/status/' + session_id


def _get_result_file_url(session_id):
    return API_PATH_PREFIX + '/results/' + session_id


@app.route(API_PATH_PREFIX + '/process', methods=['POST'])
def new_request():
    try:
        file = request.files['file']
        if not file:
            abort(400)
        # TODO Validate file

        session = Session()
        session.store_input_file(file)
        request_parameters = RequestParameters.parse(request.form)
        session.start_processing(request_parameters)

        return {
            'status_url': _get_status_url(session.session_id),
        }
    except ValueError:
        abort(400)


@app.route(API_PATH_PREFIX + '/health')
def health():
    return 'health'


@app.route(API_PATH_PREFIX + '/status/<path:session_id>')
def check_status(session_id):
    session = _get_session(session_id)
    status_result = {
        'status': 'in_progress',
    }
    status = session.get_status()
    if status == Status.SUCCESS:
        status_result['status'] = 'done'
    elif status == Status.FAILURE:
        status_result['status'] = 'error'

    is_done = session.get_status() == Status.SUCCESS

    if is_done:
        status_result['result_url'] = _get_result_file_url(session_id)
    return status_result


@app.route(API_PATH_PREFIX + '/results/<path:session_id>')
def results(session_id):
    session = _get_session(session_id)
    return send_from_directory(
        os.path.join('..', session.get_session_directory()),
        session.get_result_file_name(),
    )
