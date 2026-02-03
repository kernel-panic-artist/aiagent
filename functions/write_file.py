import os
from google.genai import types
from functions.path_utils import resolve_safe_path


def write_file(working_directory, file_path, content):
	try:
		target_dir, full_path, error = resolve_safe_path(working_directory, file_path)
		if error:
			return error

		if os.path.isdir(full_path):
			return f'Error: Cannot write to "{file_path}" as it is a directory'

		os.makedirs(target_dir, exist_ok=True)

		with open(full_path, "w") as fh:
			fh.write(content)

	except RuntimeError as e:
		return f"Error: {e}"

	return f'Successfully wrote to "{full_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file path. Return an error if there is a problem with the requested path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to write, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file.",
            ),
        },
    ),
)
