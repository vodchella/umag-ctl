from prompt_toolkit.completion import FuzzyCompleter, NestedCompleter

umag_ctl_completer = FuzzyCompleter(NestedCompleter.from_nested_dict({
    'ping': {
        'main': None,
        'reserve': None,
    },
    'exit': None,
    'help': None,
    'down': None,
    'up': None,
    'reserve': None,
    'status': None,
}))
