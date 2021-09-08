import pytest
import re
from lesson1_funcs import *


def test_task1(capsys):
    strings = ['разработка', 'сокет', 'декоратор']
    task1()
    captured = capsys.readouterr()

    lines = captured.out.split("\n")
    for i, line in enumerate(lines):
        if i > len(strings) - 1:
            break
        assert line == f"<class 'bytes'> {strings[i].encode('utf-8')}"


def test_task2(capsys):
    lens = [5, 8, 6]
    task2()
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    for i, line in enumerate(lines):
        if i > len(lens) - 1:
            break
        assert line == f"<class 'bytes'> {lens[i]}"


def test_task3(capsys):
    outs = ['класс', 'функция']
    task3()
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    for i, line in enumerate(lines):
        if i > len(outs) - 1:
            break
        assert line == f"{outs[i]}"


def test_task4(capsys):
    str_list = ['разработка', 'администрирование', 'protocol', 'standard']
    task4()
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    for i, line in enumerate(lines):
        if i > len(str_list) - 1:
            break
        assert line == f"{str_list[i]} {str_list[i].encode('utf-8')} {str_list[i]}"


def test_task5(capsys):
    sites = ['yandex.ru', 'youtube.com']
    task5()
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    result = True
    for site in sites:
        exchange_begin = False
        exchange_end = False
        for i, line in enumerate(lines):
            if exchange_begin and exchange_end:
                break

            if re.match(f'Обмен пакетами с {site}', line):
                exchange_begin = True
                lines[i] = ''
            elif re.match(f'Обмен пакетами с', line):
                break
            elif re.match(r'\s+Пакетов: отправлено = \d+, получено = \d+, потеряно = \d+', line):
                exchange_end = True
                lines[i] = ''

        if not (exchange_begin and exchange_end):
            result = False
    assert result


def test_task6(capsys):
    outs = [
        'Encoding = utf-8',
        'сетевое программирование',
        'сокет',
        'декоратор',
        'Encoding = cp1251',
        'СЃРµС‚РµРІРѕРµ РїСЂРѕРіСЂР°РјРјРёСЂРѕРІР°РЅРёРµ',
        'СЃРѕРєРµС‚',
        'РґРµРєРѕСЂР°С‚РѕСЂ',
        'Encoding = utf-16',
        'ERROR: UTF-16 stream does not start with BOM',
        ''
    ]
    task6()

    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    for i, line in enumerate(lines):
        if i > len(outs) - 1:
            break
        assert line == f"{outs[i]}"
