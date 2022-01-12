from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexer import RegexLexer, words
from pygments.token import Keyword, Error, Operator, Number, String


class UmagCtlLexerBase(RegexLexer):
    simple_commands = ['exit', 'quit', 'help', 'usage', 'down', 'up', 'reserve', 'status']
    tokens = {
        'root': [
            (words(simple_commands), Keyword),
            (words(['ping']), Keyword, 'ping'),
            (words(['service']), Keyword, 'service'),
            (r'\S+', Error),
        ],
        'ping': [
            (words(['main', 'reserve']), Operator.Word, 'ping_times')
        ],
        'service': [
            (words(['jboss', 'jboss2']), String, 'service_action')
        ],
        'ping_times': [
            (r'[0-9]+', Number.Integer)
        ],
        'service_action': [
            (words(['start', 'stop']), Operator.Word)
        ],
    }


lexer = PygmentsLexer(UmagCtlLexerBase)
