from pkg.utils.console import write_stdout
from pkg.utils.decorators import no_args, optional_int_arg
from pkg.utils.umag import jboss_direct_ping


@no_args
def cmd_exit():
    return 1


@no_args
def cmd_help():
    print("""Usage:
    'down'   - switch into \"UPDATING\" state
    'up'     - switch proxy to -> JBOSS1 (Main)
    'reserve'- switch proxy to -> JBOSS2 (Reserve)
    'status' - prints status
    'ping'   - performing N ping requests, directly into {main|reserve} jboss, bypassing nginx
    'help, exit, quit'
    """)
    return 0


def ping(server: str, times: int):
    print(f'Ping {server.upper()} {times} times:')
    port = 8080 if server == 'main' else 8081
    for i in range(times):
        write_stdout('+' if jboss_direct_ping(port) else 'F')
    print('\n')


@optional_int_arg
def cmd_ping_main(times: int = 100):
    ping('main', times)
    return 0


@optional_int_arg
def cmd_ping_reserve(times: int = 100):
    ping('reserve', times)
    return 0


@no_args
def cmd_down():
    print('Down')
    return 0


@no_args
def cmd_up():
    print('Up')
    return 0


@no_args
def cmd_reserve():
    print('Reserve')
    return 0


@no_args
def cmd_status():
    print('Status')
    return 0
