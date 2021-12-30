from prompt_toolkit import HTML


def umag_ctl_prompt() -> HTML:
    return HTML(f'<prompt-server-name>MAIN</prompt-server-name>> ')


def umag_ctl_bottom_toolbar() -> HTML:
    return HTML(
        'Services: <bottom-toolbar-service> <i>jboss</i> is <b>ON</b> </bottom-toolbar-service> ' +
        '<bottom-toolbar-service> <i>jboss2</i> is <b>OFF</b> </bottom-toolbar-service>'
    )


def umag_ctl_placeholder() -> HTML:
    return HTML('<prompt-placeholder>enter command here</prompt-placeholder>')