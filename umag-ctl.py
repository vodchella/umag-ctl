#!/usr/bin/env python3

import asyncio
from pkg.utils import check_python_version
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import NestedCompleter, FuzzyCompleter, Completer
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style
from pygments.lexer import RegexLexer, words
from pygments.token import Keyword, Number, Operator, Error


async def background_worker():
    try:
        while True:
            await asyncio.sleep(3)
    except asyncio.CancelledError:
        print('Background task cancelled.')


def get_prompt() -> HTML:
    return HTML(f'<prompt-server-name>MAIN</prompt-server-name>> ')


def get_bottom_toolbar() -> HTML:
    return HTML(
        'Services: <bottom-toolbar-service> <i>jboss</i> is <b>ON</b> </bottom-toolbar-service> ' +
        '<bottom-toolbar-service> <i>jboss2</i> is <b>OFF</b> </bottom-toolbar-service>'
    )


def get_placeholder() -> HTML:
    return HTML('<prompt-placeholder>enter command here</prompt-placeholder>')


def get_completer() -> Completer:
    return FuzzyCompleter(NestedCompleter.from_nested_dict({
        'ping': {
            'main': None,
            'reserve': None,
        },
        'exit': None,
        'help': None,
        'down': None,
        'up': None,
        'reserve': None,
        'status': None,
    }))


class UmagCtlLexer(RegexLexer):
    simple_commands = ['exit', 'help', 'down', 'up', 'reserve', 'status']
    tokens = {
        'root': [
            (words(simple_commands), Keyword),
            (words(['ping']), Keyword, 'ping'),
            (r'\S+', Error),
        ],
        'ping': [
            (words(['main', 'reserve']), Operator.Word, 'ping_times')
        ],
        'ping_times': [
            (r'[0-9]+', Number.Integer)
        ]
    }


async def interactive_shell():
    style = Style.from_dict(
        {
            'bottom-toolbar': '#444444 bg:#ff0000',
            'bottom-toolbar.text': '#444444 bg:#aaaaaa',
            'bottom-toolbar-service': '#666666 bg:#aaaaaa',
            'prompt-server-name': '#ffffff bold',
            'prompt-placeholder': '#888888',
            'pygments.keyword': '#164fbb',
            'pygments.operator.word': '#1c92de',
            'pygments.error': '#ff0000',
        }
    )

    session = PromptSession(
        get_prompt,
        bottom_toolbar=get_bottom_toolbar,
        completer=get_completer(),
        auto_suggest=AutoSuggestFromHistory(),
        placeholder=get_placeholder,
        lexer=PygmentsLexer(UmagCtlLexer),
        style=style,
        refresh_interval=1
    )

    while True:
        try:
            result = await session.prompt_async()
            print(f'You said: {result}')
        except (EOFError, KeyboardInterrupt):
            return


async def main():
    with patch_stdout():
        bg_task = asyncio.create_task(background_worker())
        try:
            await interactive_shell()
        finally:
            bg_task.cancel()
        print('Quitting event loop. Bye.')


if __name__ == '__main__':
    check_python_version()
    asyncio.run(main())
