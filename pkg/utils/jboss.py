from pkg.utils.console import shell_execute


def jboss_direct_ping(port: int) -> bool:
    cmd = 'curl -H "api-ver: 999.0" -H "client-ver: angular_cabinet_999.0.0" -s ' +\
          f'--max-time 1 http://localhost:{port}/rest/cabinet/glob/utils/ping'
    result = shell_execute(cmd)
    return result.find('{"principal":"anonymous"}') != -1
