import os
import subprocess

import pytest

RT1 = r"""
<div id="runthis1"></div>
<script type="text/javascript">
  var app = Elm.Main.init({
    node: document.getElementById("runthis1"),
    flags: {"placeholder": "<div class=\"highlight-python notranslate\"><div class=\"highlight\"><pre><span></span><span class=\"kn\">import</span> <span class=\"nn\">sys</span>\n<span class=\"k\">print</span><span class=\"p\">(</span><span class=\"n\">sys</span><span class=\"o\">.</span><span class=\"n\">executable</span><span class=\"p\">)</span>\n</pre></div>\n</div>\n", "presetup": "", "serverUrl": "http://localhost:5000", "setup": "import sys\nprint(sys.executable)\n"}
  });
</script>
</div>
"""

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
    substrings = ["runthis", RT1]
    for sub in substrings:
        assert sub in s

    # cleanup
    subprocess.run(["make", "clean"], check=True, cwd=docs)
