import re
import csv
from pprint import pprint

files = ['info_1.txt', 'info_2.txt', 'info_3.txt']

def add_quotes(string):
    return f'"{string}"'

def write_main_data(headers_list, csv_list):
    with open ('main_data.txt', 'w', encoding='utf-8') as f:
        headers_list_tmp = []
        for header in headers_list:
            string = add_quotes(header)
            headers_list_tmp.append(string)
        headers = ", ".join(headers_list_tmp) + "\n"
        f.write(headers)

        for row_dict in csv_list:
            row_list = []
            for header in headers_list:
                value = add_quotes(row_dict.get(header))
                row_list.append(value)
            row = ", ".join(row_list) + "\n"
            f.write(row)

def write_to_csv(headers_list, csv_list):
    with open('main_data.csv', 'w', encoding='utf-8') as f:
        csv_writer = csv.DictWriter(f, fieldnames=headers_list, quoting = csv.QUOTE_ALL )
        csv_writer.writeheader()
        for row in csv_list:
            csv_writer.writerow(row)



def process_file(headers_list, file):
    row_dict = {}
    with open(file, 'r', encoding='cp1251') as f:
        lines = f.readlines()
        for line in lines:
            for header in headers_list:
                if re.search(header, line):
                    value = line.split(":")[1].strip()
                    row_dict.update({header: value})

    return row_dict


def get_data():
    headers_list = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    csv_list = []
    for file in files:
        row_dict = process_file(headers_list, file)
        csv_list.append(row_dict)

    write_main_data(headers_list, csv_list)
    write_to_csv(headers_list, csv_list)


if __name__ == '__main__':
    get_data()
