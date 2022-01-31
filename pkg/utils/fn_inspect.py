# Code from https://github.com/tiangolo/typer

import inspect
from typing import Any, Callable, Dict, get_type_hints


Required = ...


class ParamMeta:
    empty = inspect.Parameter.empty

    def __init__(
        self,
        *,
        name: str,
        default: Any = inspect.Parameter.empty,
        annotation: Any = inspect.Parameter.empty,
    ) -> None:
        self.name = name
        self.default = default
        self.annotation = annotation


def get_params_from_function(func: Callable[..., Any]) -> Dict[str, ParamMeta]:
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    params = {}
    for param in signature.parameters.values():
        annotation = param.annotation
        if param.name in type_hints:
            annotation = type_hints[param.name]
        params[param.name] = ParamMeta(
            name=param.name, default=param.default, annotation=annotation
        )
    return params


def has_default_value(param: ParamMeta) -> bool:
    return not (param.default == Required or param.default == param.empty)
