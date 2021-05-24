import json
import os
import subprocess


class Processor:

    script_name: str

    def process(self, working_directory, input_file, output_file, error_file, parameters):
        process = subprocess.run(
            [
                os.path.join('/app', 'scripts', 'process.sh'),
                input_file,
                output_file,
            ] + self._generate_command_args(parameters),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=working_directory,
        )

        if process.returncode != 0:
            with open(os.path.join(working_directory, error_file), 'w+') as f:
                f.write(json.dumps({
                    'return_code': process.returncode,
                    'error': process.stderr.decode('utf-8'),
                }))

    @staticmethod
    def _generate_command_args(parameters):
        args = []
        if parameters.reverse:
            args.append('--reverse')
        if parameters.speed != 100:
            args.append('--speed')
            args.append(str(parameters.speed / 100))
        if parameters.keep_pitch:
            args.append('--keep-pitch')
        if parameters.stereo_shift != 0:
            args.append('--stereo-shift')
            args.append(str(parameters.stereo_shift))
        return args
