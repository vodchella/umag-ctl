from prompt_toolkit.styles import Style
from prompt_toolkit.styles.named_colors import NAMED_COLORS

style = Style.from_dict({
    'error-text': NAMED_COLORS['Red'],
    'bottom-toolbar': '#444444 bg:#ff0000',
    'bottom-toolbar.text': '#444444 bg:#aaaaaa',
    'bottom-toolbar-service': '#666666 bg:#aaaaaa',
    'prompt-server-name': NAMED_COLORS['White'] + ' bold',
    'prompt-server-name-updating': NAMED_COLORS['Orange'] + ' bold',
    'prompt-server-name-unavailable': NAMED_COLORS['IndianRed'] + ' bold',
    'prompt-placeholder': '#888888',
    'pygments.keyword': '#164fbb',
    'pygments.operator.word': '#1c92de',
    'pygments.error': NAMED_COLORS['Red'],
})
