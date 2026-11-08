import os
import sys

import click
import pytest
from flask.cli import with_appcontext

THIS_FILE = os.path.abspath(os.path.dirname(__file__))
TESTS_DIR = os.path.join(THIS_FILE, 'tests/')


@click.command('test')
@with_appcontext
def test():
    """Command for running tests under CI.

    For development purposes please use pytest directly:

    $ PYTHONPATH=. pytest -sv  # or similar
    """
    sys.exit(pytest.main([TESTS_DIR, '-v']))


if __name__ == '__main__':
    test()
