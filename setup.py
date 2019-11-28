#!/usr/bin/env python3
import os
import sys

from setuptools import setup


def main():
    """The main entry point."""
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
        readme = f.read()
    skw = dict(
        name='runthis-sphinxext',
        description='Provides a sphinx code-block for rendering RunThis blocks',
        long_description=readme,
        long_description_content_type='text/markdown',
        license='BSD',
        version='0.0.0',
        author='Anthony Scopatz',
        maintainer='Anthony Scopatz',
        author_email='scopatz@gmail.com',
        url='https://github.com/regro/runthis-sphinxext',
        platforms='Cross Platform',
        classifiers=['Programming Language :: Python :: 3'],
        py_modules=['runthis_sphinxext'],
        packages=['runthis'],
        package_dir={'runthis': 'runthis'},
        package_data={'runthis': ['*.js']},
        install_requires=[],
        python_requires=">=3.6",
        zip_safe=False,
        entry_points={
            'sphinx.builders': [
                'runthis = runthis.sphinxext',
            ],
        }
    )
    setup(**skw)


if __name__ == '__main__':
    main()
