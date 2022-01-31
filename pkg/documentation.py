from typing import List, Union

# Filled in processor.py
command_usages = {}


def print_command_usage(command_name: Union[str, List[str]]) -> bool:
    if isinstance(command_name, str):
        cmd_name = command_name
    elif isinstance(command_name, List):
        cmd_name = command_name[0]
    else:
        return False
    if usage := command_usages[cmd_name] if cmd_name in command_usages else None:
        print(f'Usage: {usage}')
    return usage is not None
