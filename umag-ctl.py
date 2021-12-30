#!/usr/bin/env python3

import asyncio
from pkg.completers import umag_ctl_completer
from pkg.lexers import umag_ctl_lexer
from pkg.processors import process_text
from pkg.styles import umag_ctl_style
from pkg.utils import check_python_version
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import PromptSession


async def background_worker():
    try:
        while True:
            await asyncio.sleep(3)
    except asyncio.CancelledError:
        pass


def get_prompt() -> HTML:
    return HTML(f'<prompt-server-name>MAIN</prompt-server-name>> ')


def get_bottom_toolbar() -> HTML:
    return HTML(
        'Services: <bottom-toolbar-service> <i>jboss</i> is <b>ON</b> </bottom-toolbar-service> ' +
        '<bottom-toolbar-service> <i>jboss2</i> is <b>OFF</b> </bottom-toolbar-service>'
    )


def get_placeholder() -> HTML:
    return HTML('<prompt-placeholder>enter command here</prompt-placeholder>')


async def interactive_shell():
    session = PromptSession(
        get_prompt,
        bottom_toolbar=get_bottom_toolbar,
        completer=umag_ctl_completer,
        auto_suggest=AutoSuggestFromHistory(),
        placeholder=get_placeholder,
        lexer=umag_ctl_lexer,
        style=umag_ctl_style,
        refresh_interval=1
    )

    while True:
        try:
            text = await session.prompt_async()
            if process_text(text) != 0:
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
    process_text('ping main')
    check_python_version()
    asyncio.run(main())
