from pkg.documentation import program_usage
from pkg.style import style
from pkg.utils.console import write_stdout, shell_execute, write_stderr
from pkg.utils.decorators import command
from pkg.utils.umag import jboss_direct_ping, nginx_get_jboss_proxy, nginx_get_state, nginx_set_jboss_proxy
from prompt_toolkit import print_formatted_text, HTML


@command(['exit', 'quit'])
async def cmd_exit():
    return 1


@command(['help', 'usage'])
async def cmd_help():
    print(program_usage)
    print_formatted_text(
        HTML('In case of any errors use <prompt-server-name>umag-ctl-old</prompt-server-name> command\n'),
        style=style
    )
    return 0


@command(
    'ping', 'ping {main|reserve} [number_of_times]',
    strict_args={'server': ['main', 'reserve']},
)
async def cmd_ping(server: str, times: int = 100):
    print(f'Ping {server.upper()} {times} times:')
    port = 8080 if server == 'main' else 8081
    for i in range(times):
        write_stdout('+' if jboss_direct_ping(port) else 'F')
    print()
    return 0


@command(
    'service', 'service {jboss|jboss2} {start|stop}',
    strict_args={'service': ['jboss', 'jboss2'], 'action': ['start', 'stop']},
    with_confirm=True,
)
async def cmd_service(service: str, action: str):
    if result := shell_execute(f'service {service} {action}'):
        write_stderr(f'{result}\n')
    return 0


@command('down', with_confirm=True)
async def cmd_down():
    nginx_set_jboss_proxy('UPDATING')
    return 0


@command('up', with_confirm=True)
async def cmd_up():
    nginx_set_jboss_proxy('ON')
    return 0


@command('reserve', with_confirm=True)
async def cmd_reserve():
    nginx_set_jboss_proxy('RESERVE')
    return 0


@command(['status', 'st', 's'])
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
