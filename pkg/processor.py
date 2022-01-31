import pkg.commands as cmds

from inspect import iscoroutinefunction, getmembers, isfunction
from pkg.documentation import command_usages
from pkg.utils.console import write_stderr
from typing import Callable, List

commands = {}


async def parse_and_execute(text: str) -> int:
    async def call(func: Callable) -> int:
        if func and callable(func):
            args = words[1:]
            if iscoroutinefunction(func):
                return await func(args)
            else:
                return func(args)
        write_stderr('Unknown command\n')
        return 0

    words = text.lower().split()
    if words:
        command = words[0]
        fn = commands[command] if command in commands else None
        return await call(fn)
    return 0


def _setup_command(cmd_name):
    commands[cmd_name] = fun
    if command_usage:
        command_usages[cmd_name] = command_usage


for _, fun in getmembers(cmds, isfunction):
    if hasattr(fun, '_command_names'):
        command_usage = getattr(fun, '_usage') if hasattr(fun, '_usage') else None
        names = getattr(fun, '_command_names')
        if isinstance(names, str):
            _setup_command(names)
        elif isinstance(names, List):
            for n in names:
                _setup_command(n)
