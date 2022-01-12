#!/usr/bin/env python3

import asyncio

from pkg.commands import cmd_help, cmd_status
from pkg.completer import completer
from pkg.lexer import lexer
from pkg.processor import parse_and_execute
from pkg.style import style
from pkg.utils import check_python_version
from pkg.widgets import prompt, bottom_toolbar, placeholder
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.shortcuts import PromptSession


async def interactive_shell():
    cmd_help()
    cmd_status()
    print()

    session = PromptSession(
        prompt,
        bottom_toolbar=bottom_toolbar,
        completer=completer,
        auto_suggest=AutoSuggestFromHistory(),
        placeholder=placeholder,
        lexer=lexer,
        style=style,
    )

    while True:
        try:
            text = await session.prompt_async()
            if parse_and_execute(text) != 0:
                return
            print()
        except (EOFError, KeyboardInterrupt):
            return


async def main():
    # with patch_stdout():
    await interactive_shell()
    print('Bye!\n')


if __name__ == '__main__':
    check_python_version()
    asyncio.run(main())
