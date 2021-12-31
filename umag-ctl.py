#!/usr/bin/env python3

import asyncio

from pkg.commands import cmd_help
from pkg.completer import umag_ctl_completer
from pkg.lexer import umag_ctl_lexer
from pkg.processor import parse_and_execute
from pkg.style import umag_ctl_style
from pkg.utils import check_python_version
from pkg.widgets import umag_ctl_prompt, umag_ctl_bottom_toolbar, umag_ctl_placeholder
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.shortcuts import PromptSession


async def interactive_shell():
    cmd_help()

    session = PromptSession(
        umag_ctl_prompt,
        bottom_toolbar=umag_ctl_bottom_toolbar,
        completer=umag_ctl_completer,
        auto_suggest=AutoSuggestFromHistory(),
        placeholder=umag_ctl_placeholder,
        lexer=umag_ctl_lexer,
        style=umag_ctl_style,
    )

    while True:
        try:
            text = await session.prompt_async()
            if parse_and_execute(text) != 0:
                return
        except (EOFError, KeyboardInterrupt):
            return


async def main():
    # with patch_stdout():
    await interactive_shell()
    print('Bye!')


if __name__ == '__main__':
    check_python_version()
    asyncio.run(main())
