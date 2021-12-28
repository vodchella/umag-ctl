import os
import sys
from pathlib import Path
from pkg.utils.console import panic


def get_project_root() -> str:
    return str(Path(__file__).parent.parent.parent)


def bye(code=0):
    # noinspection PyProtectedMember
    os._exit(code)


def check_python_version():
    if sys.version_info < (3, 10):
        panic('We need minimum Python version 3.10 to run. Current version: %s.%s.%s' % sys.version_info[:3])
