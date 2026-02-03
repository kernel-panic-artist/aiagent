import os
import subprocess
from google.genai import types
from functions.path_utils import resolve_safe_path


def run_python_file(working_directory, file_path, args=None):
	try:
		target_dir, full_path, error = resolve_safe_path(working_directory, file_path)
		if error:
			return error

		fname = os.path.basename(file_path)

		if not os.path.isfile(full_path):
			return f'Error: "{fname}" does not exist or is not a regular file'

		if not fname.endswith('.py'):
			return f'Error: "{fname}" is not a Python file'

		command = ["python", full_path]
		if args:
			command.extend(args)

		completed = subprocess.run(command, cwd=target_dir, capture_output=True, text=True, timeout=30)
		if completed.returncode != 0:
			return f"Process exited with code {completed.returncode}"
		if not completed.stderr and not completed.stdout:
			return "No output produced"

		return_string = f"""STDOUT:{completed.stdout}
		STDERR:{completed.stderr}
		"""

	except RuntimeError as e:
		return f"Error: {e}"

	return return_string


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the python code in a file. Return an error if there is a problem with the requested path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to run, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command line arguments to pass to the Python script",
            ),
        },
    ),
)
