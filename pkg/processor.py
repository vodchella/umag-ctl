import pkg.commands as cmds

from inspect import iscoroutinefunction, getmembers, isfunction
from pkg.documentation import command_usages
from pkg.utils.console import write_stderr
from typing import Callable, Union, List

commands = {}


async def parse_and_execute(text: str) -> int:
    async def call_fn(func: Callable, args: List[str]) -> int:
        if iscoroutinefunction(func):
            return await func(args)
        else:
            return func(args)

    async def find_and_call(func: Union[Callable, dict], level: int) -> int:
        if func:
            if callable(func):
                args = words[level:]
                return await call_fn(func, args)
            elif isinstance(func, dict):
                if len(words) > level:
                    param = words[level]
                    func = func[param] if param in fn else None
                    return await find_and_call(func, level + 1)
        write_stderr('Unknown command\n')
        return 0

    words = text.lower().split()
    if words:
        command = words[0]
        fn = commands[command] if command in commands else None
        return await find_and_call(fn, 1)
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
