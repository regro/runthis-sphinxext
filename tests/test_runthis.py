import os
import subprocess

import pytest


def test_sphinxext():
    # build docs first
    cwd = os.path.dirname(__file__)
    docs = os.path.join(cwd, 'docs')
    subprocess.run(["make", "clean", "all"], check=True, cwd=docs)

    # read the output
    index = os.path.join(docs, "_build", "html", "index.html")
    with open(index) as f:
        s = f.read()

    # check the output
    assert "runthis" in s


    # cleanup
    subprocess.run(["make", "clean"], check=True, cwd=docs)
