from functools import wraps
from pkg.utils.console import write_stderr
from pkg.utils.fn_inspect import get_params_from_function, has_default_value


def with_confirm(func):
    func._with_confirm = True

    @wraps(func)
    def wrapped(*positional, **named):
        return func(*positional, **named)
    return wrapped


def command(func):
    @wraps(func)
    async def wrapped(*positional, **named):
        if len(positional):
            params = list(get_params_from_function(func).values())
            list_of_args = positional[0]
            required_params = [p for p in params if not has_default_value(p)]
            if len(required_params) > len(list_of_args):
                write_stderr('Invalid number of arguments\n')
                return 0
            prepared_args = []
            for i, arg in enumerate(list_of_args):
                param = params[i]
                if issubclass(param.annotation, int):
                    try:
                        prepared_arg = int(arg)
                    except ValueError:
                        write_stderr('Invalid number\n')
                        return 0
                else:
                    prepared_arg = arg
                prepared_args.append(prepared_arg)
            return await func(*prepared_args)
        return await func(*positional, **named)
    return wrapped
