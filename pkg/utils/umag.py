import os

from pkg.utils.console import shell_execute, write_stderr
from typing import Optional


def jboss_direct_ping(port: int) -> bool:
    cmd = 'curl -H "api-ver: 999.0" -H "client-ver: angular_cabinet_999.0.0" -s ' +\
          f'--max-time 1 http://localhost:{port}/rest/cabinet/glob/utils/ping'
    result = shell_execute(cmd)
    return result.find('{"principal":"anonymous"}') != -1


def nginx_get_status_code() -> str:
    cmd = 'curl -I -H "api-ver: 999.0" -H "client-ver: angular_cabinet_999.0.0" -s --max-time 1 ' +\
          '--connect-to api.umag.kz:443:127.0.0.1:443 https://api.umag.kz/rest/cabinet/glob/utils/ping | ' +\
          'awk \'{if(NR==1)print $2; else if($1=="x-serv-res:")print $2}\''
    return shell_execute(cmd)


def nginx_get_state() -> Optional[str]:
    status = nginx_get_status_code()
    if status == '200':
        return 'ON'
    elif status == '200 res':
        return 'RESERVE'
    elif status == '499':
        return 'UPDATING'
    write_stderr(f'Strange http status-code from api.umag.kz: {status}, NGINX REST considered as NOT AVAILABLE\n')


def nginx_get_jboss_proxy() -> Optional[str]:
    try:
        link = os.readlink('/etc/nginx/sites-available/_jboss.proxy')
        if link[:13] == '_jboss.proxy.':
            return link[13:]
    except FileNotFoundError:
        pass
    write_stderr('File /etc/nginx/sites-available/_jboss.proxy must be symlink to _jboss.proxy.*\n')
