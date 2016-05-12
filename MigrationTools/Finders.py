import os


def find_file_locally(filename, path):
    for root, dirs, files in os.walk(path):
        for file_ in files:
            if file_ == filename:
                yield os.path.join(root, file_)