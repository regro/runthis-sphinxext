#!/usr/bin/env python3
import os
import sys
import hashlib
import urllib.request

from setuptools import setup

CLIENT_VERSION = "0.0.3"


def download_client():
    url = f"https://github.com/regro/runthis-client/releases/download/{CLIENT_VERSION}/runthis-client-{CLIENT_VERSION}.min.js"
    client_fname = os.path.join("runthis", f"runthis-client-{CLIENT_VERSION}.min.js")
    if not os.path.isfile(client_fname):
        with urllib.request.urlopen(url) as f:
            b = f.read()
        with open(client_fname, "wb") as f:
            f.write(b)


def checksum_client():
    # download checksum
    client_fname = os.path.join("runthis", f"runthis-client-{CLIENT_VERSION}.min.js")
    url = f"https://github.com/regro/runthis-client/releases/download/{CLIENT_VERSION}/sha256.txt"
    sha256_fname = f"sha256-{CLIENT_VERSION}.txt"
    if not os.path.isfile(sha256_fname):
        with urllib.request.urlopen(url) as f:
            b = f.read()
        with open(sha256_fname, "wb") as f:
            f.write(b)
    # make checksum mapping
    with open(sha256_fname) as f:
        data = f.read()
    tups = [line.split() for line in data.splitlines()]
    sums = {fname: value for value, fname in tups}
    # get checksum
    with open(client_fname, "rb") as f:
        client = f.read()
    obs = hashlib.sha256(client).hexdigest()
    assert (
        sums[f"runthis-client-{CLIENT_VERSION}.min.js"] == obs
    ), f"runthis-client-{CLIENT_VERSION}.min.js checksums don't match"


def copy_client():
    src = os.path.join("runthis", f"runthis-client-{CLIENT_VERSION}.min.js")
    tar = os.path.join("runthis", f"runthis-client.min.js")
    with open(src, "rb") as f:
        b = f.read()
    with open(tar, "wb") as f:
        f.write(b)


def main():
    """The main entry point."""
    with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as f:
        readme = f.read()
    # make sure we have the client with the correct version avialable
    download_client()
    checksum_client()
    copy_client()
    # actually install
    skw = dict(
        name="runthis-sphinxext",
        description="Provides a sphinx code-block for rendering RunThis blocks",
        long_description=readme,
        long_description_content_type="text/markdown",
        license="BSD",
        version='0.0.3',
        author="Anthony Scopatz",
        maintainer="Anthony Scopatz",
        author_email="scopatz@gmail.com",
        url="https://github.com/regro/runthis-sphinxext",
        platforms="Cross Platform",
        classifiers=["Programming Language :: Python :: 3"],
        py_modules=["runthis_sphinxext"],
        packages=["runthis"],
        package_dir={"runthis": "runthis"},
        package_data={"runthis": ["runthis-client.min.js"]},
        install_requires=[],
        python_requires=">=3.6",
        zip_safe=False,
        entry_points={"sphinx.builders": ["runthis = runthis.sphinxext",],},
    )
    setup(**skw)


if __name__ == "__main__":
    main()
