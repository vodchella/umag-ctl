from prompt_toolkit.completion import FuzzyCompleter, NestedCompleter

jboss_actions = {
    'start': None,
    'stop': None,
}

completer = FuzzyCompleter(NestedCompleter.from_nested_dict({
    'ping': {
        'main': None,
        'reserve': None,
    },
    'service': {
        'jboss': jboss_actions,
        'jboss2': jboss_actions,
    },
    'exit': None,
    'quit': None,
    'help': None,
    'down': None,
    'up': None,
    'reserve': None,
    'status': None,
}))
