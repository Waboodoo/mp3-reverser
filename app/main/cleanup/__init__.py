import datetime
import os
import shutil
from datetime import timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from app.main.utils.session_ids import get_datetime_from_session_id
from app.main.utils.session_ids import is_valid_session_id

CLEANUP_INTERVAL = 30  # minutes
KEEP_SESSIONS_FOR = timedelta(minutes=30)


def cleanup_old_sessions(sessions_dir):
    session_ids = [
        session_id
        for session_id in os.listdir(sessions_dir)
        if os.path.isdir(os.path.join(sessions_dir, session_id)) and is_valid_session_id(session_id)
    ]

    for session_id in session_ids:
        if not is_valid_session_id(session_id):
            continue
        date = get_datetime_from_session_id(session_id)
        if date + KEEP_SESSIONS_FOR < datetime.datetime.now():
            shutil.rmtree(os.path.join(sessions_dir, session_id))


def start_cleanup_scheduler(sessions_dir):
    def cleanup_task():
        cleanup_old_sessions(sessions_dir)

    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanup_task, 'interval', minutes=CLEANUP_INTERVAL)
    scheduler.start()
