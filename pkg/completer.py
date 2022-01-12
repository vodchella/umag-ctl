from prompt_toolkit.completion import FuzzyCompleter, NestedCompleter

completer = FuzzyCompleter(NestedCompleter.from_nested_dict({
    'ping': {
        'main': None,
        'reserve': None,
    },
    'exit': None,
    'quit': None,
    'help': None,
    'down': None,
    'up': None,
    'reserve': None,
    'status': None,
}))