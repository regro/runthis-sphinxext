"""Sphinx extension which adds a directive for a
highlighted code-block that may be executed by clicking the
run button above the code block/

The directive, like the standard code-block directive, takes
a language argument and an optional linenos parameter.  The
hidden-code-block adds starthidden and label as optional
parameters.

Examples:

.. runthis:: python
    :starthidden: False

    a = 10
    b = a + 5

.. runthis:: python
    :label: --- SHOW/HIDE ---

    x = 10
    y = x + 5

"""
import json
from functools import partial, wraps

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.directives.code import CodeBlock

RT_COUNTER = 0

JS_RUNTHIS = """\
<div id="{divid}"></div>
<script type="text/javascript">
  var app = Elm.Main.init({{
    node: document.getElementById("{divid}"),
    flags: {flags}
  }});
</script>
"""

def nice_bool(arg):
    tvalues = ('true',  't', 'yes', 'y')
    fvalues = ('false', 'f', 'no',  'n')
    arg = directives.choice(arg, tvalues + fvalues)
    return arg in tvalues


class runthis_code_block(nodes.General, nodes.FixedTextElement):
    pass


class RunThisCodeBlock(CodeBlock):
    """RunThis code block is executed as needed"""

    option_spec = dict(starthidden=nice_bool,
                       label=str,
                       **CodeBlock.option_spec)

    def run(self):
        # Body of the method is more or less copied from CodeBlock
        code = '\n'.join(self.content)
        rtcb = runthis_code_block(code, code)
        rtcb['language'] = self.arguments[0]
        rtcb['linenos'] = 'linenos' in self.options
        rtcb['starthidden'] = self.options.get('starthidden', True)
        rtcb['label'] = self.options.get('label', '+ show/hide code')
        rtcb.line = self.lineno
        return [rtcb]


def visit_runthis_html(self, node, app=None):
    """Visit runthis code block"""
    global RT_COUNTER
    RT_COUNTER += 1

    # We want to use the original highlighter so that we don't
    # have to reimplement it.  However it raises a SkipNode
    # error at the end of the function call.  Thus we intercept
    # it and raise it again later.
    try:
        self.visit_literal_block(node)
    except nodes.SkipNode:
        pass

    # The last element of the body should be the literal code
    # block that was just made.
    code_block = self.body[-1]

    config = self.config
    flags = {
        "placeholder": code_block,
        "serverUrl": config.runthis_server,
        "presetup": "",
        "setup": node.rawsource + "\n",
    }
    ctx = {
        'divid': 'runthis{0}'.format(RT_COUNTER),
        'startdisplay': 'none' if node['starthidden'] else 'block',
        'label': node.get('label'),
        'flags': json.dumps(flags, sort_keys=True, indent=None),
    }
    code_block = JS_RUNTHIS.format(**ctx)

    # reassign and exit
    self.body[-1] = code_block
    raise nodes.SkipNode


def depart_runthis_html(self, node):
    """Depart hidden code block"""
    # Stub because of SkipNode in visit


def setup(app):
    app.add_js_file('runthis-client.min.js')
    app.add_directive('runthis', RunThisCodeBlock)
    app.add_node(
        runthis_code_block,
        html=(
            #wraps(visit_runthis_html)(partial(visit_runthis_html, app=app)),
            visit_runthis_html,
            depart_runthis_html
        )
    )
    # add global app config options
    app.add_config_value('runthis_server', str, 'html')

