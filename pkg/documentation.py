from typing import List, Union

# Filled in processor.py
command_usages = {}

program_usage = """Usage:
    'down'        - switch into \"UPDATING\" state
    'up'          - switch proxy to -> JBOSS1 (Main)
    'reserve'     - switch proxy to -> JBOSS2 (Reserve)
    'status'      - prints status ('s' or 'st' aliased)
    'ping'        - performing N ping requests, directly into jboss, bypassing nginx
    'service'     - start or stop jboss services
    'help, usage' - show this help
    'exit, quit'  - exit program
    """


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
