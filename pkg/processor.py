from pkg.commands import (
    cmd_ping_main,
    cmd_ping_reserve,
    cmd_exit,
    cmd_help,
    cmd_down,
    cmd_up,
    cmd_reserve,
    cmd_status,
    cmd_service,
    command_usage,
)
from pkg.utils.console import write_stderr

functions = {
    'ping': {
        'main': cmd_ping_main,
        'reserve': cmd_ping_reserve,
    },
    'service': cmd_service,
    'exit': cmd_exit,
    'quit': cmd_exit,
    'help': cmd_help,
    'usage': cmd_help,
    'down': cmd_down,
    'up': cmd_up,
    'reserve': cmd_reserve,
    's': cmd_status,
    'st': cmd_status,
    'status': cmd_status,
}


def parse_and_execute(text: str) -> int:
    def call(func, level):
        if func:
            if callable(func):
                args = words[level:]
                return func(args)
            elif isinstance(func, dict):
                if len(words) > level:
                    param = words[level]
                    func = func[param] if param in fn else None
                    return call(func, level + 1)
        if usage := command_usage[command] if command in command_usage else None:
            print(f'Usage: {usage}')
        else:
            write_stderr('Unknown command\n')
        return 0

    words = text.lower().split()
    if words:
        command = words[0]
        fn = functions[command] if command in functions else None
        return call(fn, 1)
    return 0
