import json
import os
import subprocess


class Processor:

    script_name: str

    def process(self, working_directory, input_file, output_file, error_file, parameters):
        process = subprocess.run(
            [
                os.path.join('/app', 'scripts', self.script_name),
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

    def _generate_command_args(self, parameters):
        return []
