#!/usr/bin/env python3

import asyncio
from pkg.completer import umag_ctl_completer
from pkg.lexer import umag_ctl_lexer
from pkg.processor import parse_and_execute
from pkg.style import umag_ctl_style
from pkg.utils import check_python_version
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import PromptSession

from pkg.widgets import umag_ctl_prompt, umag_ctl_bottom_toolbar, umag_ctl_placeholder


async def background_worker():
    try:
        while True:
            await asyncio.sleep(3)
    except asyncio.CancelledError:
        pass


async def interactive_shell():
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
    with patch_stdout():
        bg_task = asyncio.create_task(background_worker())
        try:
            await interactive_shell()
        finally:
            bg_task.cancel()
        print('Bye!')


if __name__ == '__main__':
    check_python_version()
    asyncio.run(main())
