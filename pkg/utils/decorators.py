from functools import wraps
from pkg.documentation import print_command_usage
from pkg.utils.console import write_stderr
from pkg.utils.fn_inspect import get_params_from_function, has_default_value
from typing import Union, List


def command(
        command_names: Union[str, List[str]],
        usage: str = None,
        with_confirm: bool = False,
        strict_args: dict = None,
):
    def decorator(func):
        func._command_names = command_names
        if usage:
            func._usage = usage
        if with_confirm:
            func._with_confirm = with_confirm
        if strict_args:
            func._strict_args = strict_args

        @wraps(func)
        async def wrapped(*positional, **named):
            def err(err_text: str):
                write_stderr(f'{err_text}\n')
                print_command_usage(getattr(wrapped, '_command_names'))

            if len(positional):
                params = list(get_params_from_function(func).values())
                list_of_args = positional[0]
                required_params = [p for p in params if not has_default_value(p)]
                if len(required_params) > len(list_of_args):
                    err('Invalid number of arguments')
                    return 0
                s_args = getattr(wrapped, '_strict_args') if hasattr(wrapped, '_strict_args') else {}
                prepared_args = []
                for i, arg in enumerate(list_of_args):
                    param = params[i]
                    if param.name in s_args:
                        allowed_values = s_args[param.name]
                        if arg not in allowed_values:
                            err(f'Argument #{i+1} must be one of: {", ".join(allowed_values)}')
                            return 0
                    if issubclass(param.annotation, int):
                        try:
                            prepared_arg = int(arg)
                        except ValueError:
                            err(f'Argument #{i+1} must be integer')
                            return 0
                    else:
                        prepared_arg = arg
                    prepared_args.append(prepared_arg)
                return await func(*prepared_args)
            return await func(*positional, **named)
        return wrapped
    return decorator
