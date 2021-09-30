import subprocess
from ipaddress import ip_address
from socket import gethostbyname


def host_ping(host_list: list):
    result_dict = {}
    for host in host_list:
        try:
            ipv4 = ip_address(host)
        except:
            try:
                ip = gethostbyname(host)
                ipv4 = ip_address(ip)
            except:
                result_dict.update({host: False})
                continue

        args = ['ping', '-n', '3', str(ipv4)]
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        proc.wait(timeout=30)
        host_accessible = False
        success_line = "Пакетов: отправлено = 3, получено = 3, потеряно = 0"
        for line in proc.stdout:
            if success_line in line.decode('cp866'):
                host_accessible = True
        result_dict.update({host: host_accessible})

    for host, host_accessible in result_dict.items():
        if host_accessible:
            print(f'Узел доступен: {host}')
        else:
            print(f'Узел недоступен: {host}')

    return result_dict

host_ping(['google.ru', '8.8.8.8', 'notexistent.not', '55.55.55.55'])