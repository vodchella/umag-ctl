from pkg.style import style
from pkg.utils.console import write_stdout, shell_execute, write_stderr
from pkg.utils.decorators import with_confirm, command
from pkg.utils.umag import jboss_direct_ping, nginx_get_jboss_proxy, nginx_get_state, nginx_set_jboss_proxy
from pkg.widgets import confirm_dialog
from prompt_toolkit import print_formatted_text, HTML

command_usage = {
    'ping': 'ping {main|reserve} [number_of_times]',
    'service': 'service {jboss|jboss2} {start|stop}',
}


@command
async def cmd_exit():
    return 1


@command
async def cmd_help():
    print("""Usage:
    'down'        - switch into \"UPDATING\" state
    'up'          - switch proxy to -> JBOSS1 (Main)
    'reserve'     - switch proxy to -> JBOSS2 (Reserve)
    'status'      - prints status ('s' or 'st' aliased)
    'ping'        - performing N ping requests, directly into jboss, bypassing nginx
    'service'     - start or stop jboss services
    'help, usage' - show this help
    'exit, quit'  - exit program
    """)
    print_formatted_text(
        HTML('In case of any errors use <prompt-server-name>umag-ctl-old</prompt-server-name> command\n'),
        style=style
    )
    return 0


def ping(server: str, times: int):
    print(f'Ping {server.upper()} {times} times:')
    port = 8080 if server == 'main' else 8081
    for i in range(times):
        write_stdout('+' if jboss_direct_ping(port) else 'F')
    print()


@command
async def cmd_ping_main(times: int = 100):
    ping('main', times)
    return 0


@command
async def cmd_ping_reserve(times: int = 100):
    ping('reserve', times)
    return 0


@command
async def cmd_service(service: str, action: str):
    svc = service.strip().lower()
    act = action.strip().lower()
    if svc not in ['jboss', 'jboss2'] or act not in ['start', 'stop']:
        print(f'Usage: {command_usage["service"]}')
    elif await confirm_dialog() and (result := shell_execute(f'service {svc} {act}')):
        write_stderr(f'{result}\n')
    return 0


@command
@with_confirm
async def cmd_down():
    nginx_set_jboss_proxy('UPDATING')
    return 0


@command
@with_confirm
async def cmd_up():
    nginx_set_jboss_proxy('ON')
    return 0


@command
@with_confirm
async def cmd_reserve():
    nginx_set_jboss_proxy('RESERVE')
    return 0


@command
async def cmd_status():
    proxy = nginx_get_jboss_proxy()
    nginx_state = nginx_get_state()
    if proxy and nginx_state:
        jboss = 'JBOSS1 (Main)' if proxy == 'ON' else 'JBOSS2 (Reserve)'
        jboss_proxy = f'[{proxy} -> {jboss}]'
        print('Current status:')
        print(f'    * nginx\'s jboss-proxy: {jboss_proxy}')
        print(f'    * http-check: [{nginx_state}]')
    return 0
