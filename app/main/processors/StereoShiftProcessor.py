from app.main.processors.Processor import Processor


class StereoShiftProcessor(Processor):

    script_name = 'stereo-shift.sh'

    def _generate_command_args(self, parameters):
        return ['2']
