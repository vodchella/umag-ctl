from functools import wraps
from pkg.utils.console import write_stderr


def with_confirm(func):
    func._with_confirm = True

    @wraps(func)
    def wrapped(*positional, **named):
        return func(*positional, **named)
    return wrapped


def no_args(func):
    @wraps(func)
    def wrapped(*positional, **named):
        if len(positional):
            list_of_args = positional[0]
            if isinstance(list_of_args, list):
                if len(list_of_args):
                    write_stderr('This command must take no arguments\n')
                    return 0
                else:
                    return func()
        return func(*positional, **named)
    return wrapped


def two_args_async(func):
    @wraps(func)
    async def wrapped(*positional, **named):
        if len(positional):
            list_of_args = positional[0]
            if isinstance(list_of_args, list):
                args_count = len(list_of_args)
                if args_count == 2:
                    first_arg = list_of_args[0]
                    second_arg = list_of_args[1]
                    return await func(first_arg, second_arg)
                else:
                    write_stderr('Invalid number of arguments\n')
                    return 0
        return await func(*positional, **named)
    return wrapped


def optional_int_arg(func):
    @wraps(func)
    def wrapped(*positional, **named):
        if len(positional):
            list_of_args = positional[0]
            if isinstance(list_of_args, list):
                args_count = len(list_of_args)
                if args_count == 0:
                    return func()
                elif args_count == 1:
                    try:
                        first_arg = int(list_of_args[0])
                    except ValueError:
                        write_stderr('Invalid number\n')
                        return 0
                    return func(first_arg)
                else:
                    write_stderr('Invalid number of arguments\n')
                    return 0
        return func(*positional, **named)
    return wrapped

