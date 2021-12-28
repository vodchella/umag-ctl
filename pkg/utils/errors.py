import sys
import traceback
from typing import Optional


def get_raised_error(full: bool = False) -> Optional[str]:
    info = sys.exc_info()
    if info[0] is None and info[1] is None and info[2] is None:
        return
    exc, value, tb = info
    e = traceback.format_exception(exc, value, tb)
    if full:
        return ''.join(e)
    else:
        return (e[-1:][0]).strip('\n')
