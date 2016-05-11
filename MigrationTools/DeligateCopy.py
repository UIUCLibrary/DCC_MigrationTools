import os
import shutil
import tempfile

class TempCopy:
    def __init__(self, filename):
        """

        :param filename: Name of file that you wish to make a temporary local copy
        """

        if not os.path.exists(filename):
            raise FileNotFoundError

        self._srr_file = os.path.abspath(filename)
        self._tmp_file_name = os.path.basename(filename)
        self._tmp_dir = None

    def __enter__(self):
        self._tmp_dir = tempfile.TemporaryDirectory()

        shutil.copy2(self._srr_file, os.path.join(self._tmp_dir.name, self._tmp_file_name))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tmp_dir.cleanup()
        pass

    @property
    def source_file(self):
        return self._srr_file

    @property
    def filename(self):
        return os.path.join(self._tmp_dir.name, self._tmp_file_name)