import subprocess
from ipaddress import ip_address
from socket import gethostbyname
from itertools import zip_longest
from tabulate import tabulate


def host_ping(host_list: list, printout=True):
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
        try:
            proc.wait(timeout=5)
        except:
            result_dict.update({host: False})
            continue

        host_accessible = False
        success_line = "Пакетов: отправлено = 3, получено = 3, потеряно = 0"
        for line in proc.stdout:
            if success_line in line.decode('cp866'):
                host_accessible = True
        result_dict.update({host: host_accessible})

    if printout:
        for host, host_accessible in result_dict.items():
            if host_accessible:
                print(f'Узел доступен: {host}')
            else:
                print(f'Узел недоступен: {host}')

    return result_dict


# host_ping(['google.ru', '8.8.8.8', 'notexistent.not', '55.55.55.55'])

from ipaddress import ip_network


def host_range_ping(network: str, prtintout=True):
    try:
        ipv4_network = ip_network(network)
    except:
        raise Exception(f"Not valid ip network {network}")

    result_dict = host_ping(list(ipv4_network.hosts()), printout=prtintout)
    return result_dict


# host_range_ping('192.168.2.0/28')

def host_range_ping_tab(network: str):
    result_dict = host_range_ping(network, False)
    true_list = []
    false_list = []
    for host, accessible in result_dict.items():
        if accessible:
            true_list.append(host)
        else:
            false_list.append(host)

    tab_list = []
    for i in zip_longest(true_list, false_list):
        tab_list.append(i)

    headers = ['Reachable', 'Unreachable']
    print(tabulate(tab_list, headers, tablefmt="simple"))


host_range_ping_tab('192.168.2.0/28')
