import os
import subprocess
import sys

from pkg.style import style
from pkg.utils.errors import get_raised_error
from prompt_toolkit import HTML, print_formatted_text, PromptSession
from typing import Optional


def write_stderr(line: str):
    print_formatted_text(
        HTML(f'<error-text>{line}</error-text>'),
        flush=True, file=sys.stderr, end='', style=style
    )


def write_stdout(line: str):
    sys.stdout.write(line)
    sys.stdout.flush()


def panic(msg: str = None, show_original_error: bool = False):
    if not msg:
        msg = get_raised_error()
    elif show_original_error:
        write_stderr(get_raised_error())
    write_stderr(f'{msg}\n')
    # noinspection PyProtectedMember
    os._exit(1)


def shell_execute(command: str) -> Optional[str]:
    return subprocess.getoutput(command)


async def confirm() -> bool:
    result = str(await PromptSession('Are you sure [y/N]? ').prompt_async()).strip().lower() in ['y', 'yes']
    if not result:
        print('Cancelled')
    return result
