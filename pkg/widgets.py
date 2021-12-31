from prompt_toolkit import HTML

from pkg.utils.console import shell_execute


def umag_ctl_prompt() -> HTML:
    return HTML(f'<prompt-server-name>MAIN</prompt-server-name>> ')


def umag_ctl_bottom_toolbar() -> HTML:
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


def umag_ctl_placeholder() -> HTML:
    return HTML('<prompt-placeholder>enter command here</prompt-placeholder>')