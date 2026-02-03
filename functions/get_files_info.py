import os
from google.genai import types
from functions.path_utils import check_working_dir


def get_files_info(working_directory, directory="."):
	working_dir_abs = os.path.abspath(working_directory)
	target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

	if not check_working_dir(working_directory, target_dir):
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

	if not os.path.isdir(target_dir):
		return f'Error: "{directory}" is not a directory'

	result_strings = []
	for p in os.listdir(target_dir):
		fullpath = os.path.join(target_dir, p)
		s = f"{p}: file_size={os.path.getsize(fullpath)}, is_dir={os.path.isdir(fullpath)}"
		result_strings.append(s)

	return "\n".join([f" - {r}" for r in result_strings])


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
