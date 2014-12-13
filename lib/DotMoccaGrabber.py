import os


def find_mocca_file(start_dir):
    """
    Tries to find a .mocca in start_dir.
    If no .mocca file could be found the parent directory is searched until the file system root is reached.
    :param start_dir: The directory to search
    :return: Returns the full path to the found .mocca file
    """

    if not os.path.isdir(start_dir):
        raise RuntimeError("Couldn't find .mocca file in file tree")

    mocca_files = [file for file in os.listdir(start_dir) if os.path.isfile(os.path.join(start_dir, file)) and file == '.mocca']

    if len(mocca_files) > 1:
        raise RuntimeError("Found multiple .mocca files in {0}".format(start_dir))

    if len(mocca_files) == 0:
        next_dir = os.path.abspath(os.path.join(start_dir, '..'))
        if os.path.samefile(start_dir, next_dir):
            raise RuntimeError("Couldn't find .mocca file in file tree")

        return find_mocca_file(next_dir)

    return os.path.join(start_dir, mocca_files[0])


def validate_mocca_file(file):
    """
    Raises exceptions if the provided file is either not a file or not writable.
    :param file: The file to validate
    """
    if not os.path.isfile(file):
        raise RuntimeError('{0} is not a file'.format(file))

    if not os.access(file, os.W_OK):
        raise RuntimeError('{0} is not writable'.format(file))
