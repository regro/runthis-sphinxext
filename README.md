# runthis-sphinxext
This provides a sphinx extension that adds RunThis code blocks,
which display a highligthed code-block statically, but with a
"RunThis" button above them. When the button is clicked, the code
block is replaced by a terminal session that has executed that
code.

## Installation
RunThis Sphinx Extention may be installed with either conda or pip:

```sh
# use the conda-forge channel
$ conda install -c conda-forge runthis-sphinxext

# Or you can use Pip, if you must.
$ pip install runthis-sphinxext
```

## Configuration
To use the RunThis code blocks, you must configure sphinx to know about
RunThis. First, make sure the sphinx extension is registered. In the
`conf.py`, add `runthis.sphinxext` somewhere in the extensions block:

```python
extensions = [
    ...
    "runthis.sphinxext",
    ...
]
```

After this, you also need to tell sphinx where the RunThis Server is
located.  This can be set with the `runthis_server` variable anywhere
in the `conf.py`.  For example:

```python
# runthis options
runthis_server = "http://localhost:5000"
```

## Usage
To use the RunThis directive is very similar to the `code-block`
directive in rST. In any of your `*.rst` files, you may use
the `runthis` directive, followed by the language name on the
same line.  After any `code-block` options and one or more blank lines,
the code that you wish to display and run, is in an indented block.
For example:

```rst
.. runthis:: python

    import sys
    print(sys.executable)
```

This will be run on the remote server specified in the `conf.py` file.