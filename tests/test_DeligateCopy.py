import pytest
import tempfile
import os
from MigrationTools.DeligateCopy import TempCopy


@pytest.fixture(scope="module")
def test_file(request):
    """Creates a temp file to make sure to test on"""
    tmpfile = tempfile.NamedTemporaryFile(mode='r')

    def cleanup():

        print("Deleting")

    request.addfinalizer(cleanup)
    return tmpfile


def test_TempCopy_src_exists(test_file):
    with TempCopy(test_file.name) as tmp:
        assert os.path.exists(tmp.source_file)


def test_TempCopy_tmp_exists(test_file):
    with TempCopy(test_file.name) as tmp:
        assert os.path.exists(tmp.filename)


def test_TempCopy_cleanup(test_file):
    with TempCopy(test_file.name) as tmp:
        pass
    assert not os.path.exists(tmp.filename)


def test_TempCopy_cleanup_in_exception(test_file):
    with pytest.raises(RuntimeError) as excpt:
        with TempCopy(test_file.name) as tmp:
            raise RuntimeError
    assert not os.path.exists(tmp.filename)


def test_TempCopy_source_file(test_file):
    with TempCopy(test_file.name) as tmp:
        assert tmp.source_file == test_file.name


def test_TempCopy_same_filename(test_file):
    with TempCopy(test_file.name) as tmp:
        assert os.path.basename(tmp.filename) == os.path.basename(test_file.name)