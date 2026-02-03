import os
from google.genai import types
from functions.path_utils import resolve_safe_path

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
	try:
		target_dir, full_path, error = resolve_safe_path(working_directory, file_path)
		if error:
			return error

		if not os.path.isfile(full_path):
			return f'Error: File not found or is not a regular file: "{file_path}"'

		with open(full_path, "r") as fh:
			content = fh.read(MAX_CHARS)
			if fh.read(1):
				content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
	except RuntimeError as e:
		return f"Error: {e}"

	return content


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the contents of a file, truncating it at MAX_CHARS (10000) if it is long. Return an error if there is a problem with the requested path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to get content from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
