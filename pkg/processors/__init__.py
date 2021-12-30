from pkg.utils.decorators import no_args, optional_int_arg


@no_args
def fn_exit():
    return 1


@no_args
def fn_help():
    print("""Usage:
    'down'   - switch into \"UPDATING\" state
    'up'     - switch proxy to -> JBOSS1 (Main)
    'reserve'- switch proxy to -> JBOSS2 (Reserve)
    'status' - prints status
    'ping'   - performing N ping requests, directly into {main|reserve} jboss, bypassing nginx
    'help, exit, quit'
    """)
    return 0


@optional_int_arg
def fn_ping_main(times: int = 100):
    print(f'Ping main {times}')
    return 0


@optional_int_arg
def fn_ping_reserve(times: int = 100):
    print(f'Ping reserve {times}')
    return 0


@no_args
def fn_down():
    print('Down')
    return 0


@no_args
def fn_up():
    print('Up')
    return 0


@no_args
def fn_reserve():
    print('Reserve')
    return 0


@no_args
def fn_status():
    print('Status')
    return 0


functions = {
    'ping': {
        'main': fn_ping_main,
        'reserve': fn_ping_reserve,
    },
    'exit': fn_exit,
    'quit': fn_exit,
    'help': fn_help,
    'down': fn_down,
    'up': fn_up,
    'reserve': fn_reserve,
    'status': fn_status,
}

command_usage = {
    'ping': 'ping {main|reserve} [number_of_times]'
}


def process_text(text: str) -> int:
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
            print('Unknown command')
        return 0

    words = text.lower().split()
    if words:
        command = words[0]
        fn = functions[command] if command in functions else None
        return call(fn, 1)
    return 0
