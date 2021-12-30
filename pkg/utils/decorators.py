from functools import wraps


def no_args(func):
    @wraps(func)
    def wrapped(*positional, **named):
        if len(positional):
            list_of_args = positional[0]
            if isinstance(list_of_args, list):
                if len(list_of_args):
                    print('This command must take no arguments')
                    return 0
                else:
                    return func()
        return func(*positional, **named)
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
                        print('Invalid number')
                        return 0
                    return func(first_arg)
                else:
                    print('Invalid number of arguments')
                    return 0
        return func(*positional, **named)
    return wrapped

