#!/usr/bin/env python3

from subprocess import Popen, PIPE
site_list = ['yandex.ru', 'youtube.com']
for site in site_list:
    args = ['ping', '-c', '3', site]
    proc = Popen(args, stdout=PIPE)
    proc.wait(timeout=30)
    for line in proc.stdout:
        print(line.decode('utf-8'))
