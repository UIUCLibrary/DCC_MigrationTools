import py
import subprocess
def test_linkcheck(tmpdir):
    source = tmpdir.join("source")
    htmldir = tmpdir.join("html")
    subprocess.check_call(
        ["sphinx-build", "-W", "-blinkcheck",
          "-d", str(source), ".", str(htmldir)])
def test_build_docs(tmpdir):
    source = tmpdir.join("source")
    htmldir = tmpdir.join("html")
    subprocess.check_call([
        "sphinx-build", "-W", "-bhtml",
          "-d", str(source), ".", str(htmldir)])
