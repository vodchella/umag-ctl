import os

from pkg.style import style
from pkg.utils.console import shell_execute, write_stderr
from prompt_toolkit import print_formatted_text, HTML
from time import sleep, time
from typing import Optional


def jboss_direct_ping(port: int) -> bool:
    cmd = 'curl -H "api-ver: 999.0" -H "client-ver: angular_cabinet_999.0.0" -s ' + \
          f'--max-time 1 http://localhost:{port}/rest/cabinet/glob/utils/ping'
    result = shell_execute(cmd)
    return result.find('{"principal":"anonymous"}') != -1


def nginx_get_status_code() -> Optional[str]:
    cmd = 'curl -I -H "api-ver: 999.0" -H "client-ver: angular_cabinet_999.0.0" -s --max-time 1 ' + \
          '--connect-to api.umag.kz:443:127.0.0.1:443 https://api.umag.kz/rest/cabinet/glob/utils/ping | ' + \
          'awk \'{if(NR==1)print $2; else if($1=="x-serv-res:")print $2}\''
    return result.replace('\n', ' ').strip() if (result := shell_execute(cmd)) else None


def nginx_get_state() -> Optional[str]:
    status = nginx_get_status_code()
    if status == '200':
        return 'ON'
    elif status == '200 res':
        return 'RESERVE'
    elif status == '499':
        return 'UPDATING'
    else:
        write_stderr(f'Strange http status-code from api.umag.kz: {status}, NGINX REST considered as NOT AVAILABLE\n')


def nginx_get_jboss_proxy() -> Optional[str]:
    try:
        link = os.readlink('/etc/nginx/sites-available/_jboss.proxy')
        if link[:13] == '_jboss.proxy.':
            return link[13:]
    except FileNotFoundError:
        pass
    write_stderr('File /etc/nginx/sites-available/_jboss.proxy must be symlink to _jboss.proxy.*\n')


def nginx_set_jboss_proxy(proxy: str):
    if proxy in ['ON', 'RESERVE', 'UPDATING']:
        if (current_proxy := nginx_get_jboss_proxy()) is not None:
            print(f'Nginx config: switching symlink to _jboss.proxy.{proxy}...')
            if proxy == current_proxy:
                print(f'Already switched to _jboss.proxy.{proxy}')
            else:
                shell_execute(f'/bin/ln -sf _jboss.proxy.{proxy} /etc/nginx/sites-available/_jboss.proxy')
                shell_execute('/usr/sbin/nginx -t 2>/dev/null && /usr/sbin/service nginx reload')

                ok = False
                restart_applied = False
                start_time = time()
                while int(time() - start_time) < 10:
                    print('Waiting 0.5s')
                    sleep(0.5)

                    ok = nginx_get_state() == proxy
                    tag = 'prompt-server-name' if ok else 'prompt-server-name-unavailable'
                    status = 'OK' if ok else 'FAILED'
                    print_formatted_text(
                        HTML(f'Checking https://api.umag.kz/: {proxy} [<{tag}>{status}</{tag}>]'),
                        style=style, flush=True
                    )

                    if ok:
                        break

                    if not restart_applied and int(time() - start_time) > 3:
                        restart_applied = True
                        write_stderr('\nRestarting nginx (reload didn\'t help after 3 sec)\n\n')
                        shell_execute('/usr/sbin/nginx -t 2>/dev/null && /usr/sbin/service nginx restart')

                if not ok:
                    write_stderr('\nFAILED TO SWITCH NGINX CONFIG, ')
                    write_stderr('GO AND FIX STATE MANUALLY, BACKEND COULD BE UNREACHABLE BY NOW!!!\n')
