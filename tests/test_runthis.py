import os
import subprocess

import pytest

RT1 = r"""
<div id="runthis1"></div>
<script type="text/javascript">
  var app = Elm.Main.init({
    node: document.getElementById("runthis1"),
    flags: {"placeholder": "<div class=
""".strip()
RT2 = '<script src="_static/runthis-client.min.js"></script>'


def test_sphinxext():
    # build docs first
    cwd = os.path.dirname(__file__)
    docs = os.path.join(cwd, 'docs')
    subprocess.run(["make", "clean", "html"], check=True, cwd=docs)

    # read the output
    index = os.path.join(docs, "_build", "html", "index.html")
    with open(index) as f:
        s = f.read()

    # check the output
    substrings = ["runthis", RT1, RT2]
    for sub in substrings:
        assert sub in s

    # check that the file was copied
    client_js = os.path.join(docs, "_build", "html", "_static", "runthis-client.min.js")
    assert os.path.isfile(client_js), "runthis-client.min.js missing"

    # cleanup
    subprocess.run(["make", "clean"], check=True, cwd=docs)
