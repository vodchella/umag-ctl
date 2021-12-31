from pkg.utils.console import shell_execute


def jboss_direct_ping(port: int) -> bool:
    cmd = 'curl -H "api-ver: 999.0" -H "client-ver: angular_cabinet_999.0.0" -s ' +\
          f'--max-time 1 http://localhost:{port}/rest/cabinet/glob/utils/ping'
    result = shell_execute(cmd)
    return result.find('{"principal":"anonymous"}') != -1


def nginx_get_status_code():
    cmd = 'curl -I -H "api-ver: 999.0" -H "client-ver: angular_cabinet_999.0.0" -s --max-time 1 ' +\
          '--connect-to api.umag.kz:443:127.0.0.1:443 https://api.umag.kz/rest/cabinet/glob/utils/ping | ' +\
          'awk \'{if(NR==1)print $2; else if($1=="x-serv-res:")print $2}\''
    return shell_execute(cmd)
