import os


def check_working_dir(working_dir, target_dir):
	"""Check if target_dir is within working_dir."""
	wdir = os.path.abspath(working_dir)
	tdir = os.path.normpath(target_dir)
	return os.path.commonpath([wdir, tdir]) == wdir


def resolve_safe_path(working_directory, file_path):
	"""
	Resolve a file path safely within the working directory.

	Returns:
		tuple: (target_dir, full_file_path, error_message)
		       If error_message is not None, the path is invalid.
	"""
	directory = os.path.dirname(file_path)
	working_dir_abs = os.path.abspath(working_directory)
	target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

	if not check_working_dir(working_directory, target_dir):
		return None, None, f'Error: Path "{file_path}" is outside the permitted working directory'

	fname = os.path.basename(file_path)
	full_path = os.path.join(target_dir, fname)

	return target_dir, full_path, None
