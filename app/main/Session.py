import os
from enum import Enum
from enum import auto
from multiprocessing import Process

from app.main.exceptions.exceptions import InvalidSessionIdError
from app.main.processors.StereoShiftProcessor import StereoShiftProcessor
from app.main.utils.session_ids import generate_session_id
from app.main.utils.session_ids import is_valid_session_id

INPUT_FILE = 'input.mp3'
OUTPUT_FILE = 'output.mp3'
ERROR_FILE = 'error.txt'


class Status(Enum):
    IN_PROGRESS = auto()
    SUCCESS = auto()
    FAILURE = auto()


class Session:

    session_id: str

    def __init__(self, session_id=None):
        self.session_id = session_id or generate_session_id()
        if not is_valid_session_id(self.session_id):
            raise InvalidSessionIdError()

    def get_session_directory(self):
        return os.path.join('sessions', self.session_id)

    def store_input_file(self, file):
        session_directory = self.get_session_directory()
        os.mkdir(session_directory)
        file.save(os.path.join(session_directory, INPUT_FILE))

    def start_processing(self, request_parameters):
        process = Process(
            target=lambda: self._process(request_parameters),
            daemon=True,
        )
        process.start()

    def _process(self, parameters):
        # TODO: Pick appropriate processor for given parameters, e.g. using a factory
        processor = StereoShiftProcessor()
        processor.process(
            working_directory=self.get_session_directory(),
            input_file=INPUT_FILE,
            output_file=OUTPUT_FILE,
            error_file=ERROR_FILE,
            parameters=parameters,
        )

    def get_status(self):
        session_directory = self.get_session_directory()
        is_done = os.path.isfile(os.path.join(session_directory, OUTPUT_FILE))
        if is_done:
            return Status.SUCCESS
        is_failure = os.path.isfile(os.path.join(session_directory, ERROR_FILE))
        if is_failure:
            return Status.FAILURE
        return Status.IN_PROGRESS

    def get_result_file_name(self):
        return OUTPUT_FILE
