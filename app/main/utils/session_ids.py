from uuid import uuid4
import datetime

from app.main.utils.validators import is_valid_uuid4

DATETIME_FORMAT = '%Y-%m-%d-%H-%M-%S'


def is_valid_session_id(session_id):
    parts = session_id.split('_')
    if len(parts) != 2:
        return False
    try:
        datetime.datetime.strptime(parts[0], DATETIME_FORMAT)
    except ValueError:
        return False
    return is_valid_uuid4(parts[1])


def generate_session_id():
    uuid = str(uuid4())
    date = datetime.datetime.now().strftime(DATETIME_FORMAT)
    return '{date}_{uuid}'.format(date=date, uuid=uuid)


def get_datetime_from_session_id(session_id):
    parts = session_id.split('_')
    return datetime.datetime.strptime(parts[0], DATETIME_FORMAT)
