from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexer import RegexLexer, words
from pygments.token import Keyword, Error, Operator, Number


class UmagCtlLexerBase(RegexLexer):
    simple_commands = ['exit', 'quit', 'help', 'down', 'up', 'reserve', 'status']
    tokens = {
        'root': [
            (words(simple_commands), Keyword),
            (words(['ping']), Keyword, 'ping'),
            (r'\S+', Error),
        ],
        'ping': [
            (words(['main', 'reserve']), Operator.Word, 'ping_times')
        ],
        'ping_times': [
            (r'[0-9]+', Number.Integer)
        ]
    }


umag_ctl_lexer = PygmentsLexer(UmagCtlLexerBase)
