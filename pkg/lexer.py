from typing import List

from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexer import RegexLexer, words as words_orig
from pygments.token import Keyword, Error, Operator, Number, String


def words(arr: List[str]):
    return words_orig(arr, prefix=r'\b', suffix=r'\s*\b')


class UmagCtlLexerBase(RegexLexer):
    simple_commands = ['exit', 'quit', 'help', 'usage', 'down', 'up', 'reserve', 'status', 's', 'st']
    tokens = {
        'root': [
            (words(simple_commands), Keyword, '#pop'),
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
            (r'[0-9]+\s*\b', Number.Integer, '#pop')
        ],
        'service_action': [
            (words(['start', 'stop']), Operator.Word, '#pop')
        ],
    }


lexer = PygmentsLexer(UmagCtlLexerBase)
