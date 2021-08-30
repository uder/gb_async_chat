#!/usr/bin/env python3

filename = 'test_file.txt'


def open_with(encoding='utf-8'):
    print(f"Encoding = {encoding}")
    try:
        with open(filename, 'r', encoding=encoding) as f:
            for line in f:
                print(line)
    except Exception as err:
        print(f"ERROR: {err}")

    print('---')

open_with('utf-8')
open_with('cp1251')
open_with('utf-16')

