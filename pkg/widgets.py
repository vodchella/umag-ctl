from pkg.style import style
from pkg.utils.console import shell_execute
from pkg.utils.umag import nginx_get_status_code
from prompt_toolkit import HTML, PromptSession


def prompt() -> HTML:
    status = nginx_get_status_code()
    tag = 'prompt-server-name'
    if status == '200':
        server = 'MAIN'
    elif status == '200 res':
        server = 'RESERVE'
    elif status == '499':
        server = 'UPDATING'
        tag = 'prompt-server-name-updating'
    else:
        server = 'UNAVAILABLE'
        tag = 'prompt-server-name-unavailable'

    return HTML(f'<{tag}>{server}</{tag}>> ')


def bottom_toolbar() -> HTML:
    def status_from_result(result: str) -> str:
        prepared = result.strip().lower()
        if prepared.startswith('active: active'):
            return 'ON'
        if prepared.startswith('active: inactive'):
            return 'OFF'
        return 'MISSING'

    command_template = 'service %s status | grep Active'
    jboss1_cmd = command_template % 'jboss'
    jboss2_cmd = command_template % 'jboss2'
    jboss1 = status_from_result(shell_execute(jboss1_cmd))
    jboss2 = status_from_result(shell_execute(jboss2_cmd))
    return HTML(
        f'Services: <bottom-toolbar-service> <i>jboss</i> is <b>{jboss1}</b> </bottom-toolbar-service> ' +
        f'<bottom-toolbar-service> <i>jboss2</i> is <b>{jboss2}</b> </bottom-toolbar-service>'
    )


def placeholder() -> HTML:
    return HTML('<prompt-placeholder>enter command here</prompt-placeholder>')


async def confirm_dialog() -> bool:
    session = PromptSession('Are you sure [y/N]? ', bottom_toolbar=bottom_toolbar, style=style)
    result = str(await session.prompt_async()).strip().lower() in ['y', 'yes']
    if not result:
        print('Cancelled')
    return result
