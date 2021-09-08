def task1():
    strings = ['разработка', 'сокет', 'декоратор']
    for string in strings:
        encoded = string.encode('utf-8')
        print(type(encoded), encoded)

def task2():
    bytes_list = [b'class', b'function', b'method']
    for byte_object in bytes_list:
        print(type(byte_object), len(byte_object))

def task3():
    words = ['attribute', 'класс', 'функция', 'type']

    for word in words:
        try:
            byte_object = word.encode('ascii')
        except:
            print (f"{word}")

def task4():
    str_list = ['разработка', 'администрирование', 'protocol', 'standard']
    for s in str_list:
        byte_s = s.encode('utf-8')
        str_s = byte_s.decode('utf-8')
        print(s, byte_s, str_s)

def task5():
    from subprocess import Popen, PIPE
    site_list = ['yandex.ru', 'youtube.com']
    for site in site_list:
        args = ['ping', '-n', '3', site]
        proc = Popen(args, stdout=PIPE)
        proc.wait(timeout=30)
        for line in proc.stdout:
            print(line.decode('cp866'))

def task6():
    filename = 'test_file.txt'

    def open_with(encoding='utf-8'):
        print(f"Encoding = {encoding}")
        try:
            with open(filename, 'r', encoding=encoding) as f:
                for line in f:
                    print(line.strip())
        except Exception as err:
            print(f"ERROR: {err}")

        # print('---')

    open_with('utf-8')
    open_with('cp1251')
    open_with('utf-16')

def main():
    functions = [task1, task2, task3, task4, task5, task6]
    for func in functions:
        print(f"{func.__name__} Output:")
        func()
        print('---')

if __name__ == '__main__':
    main()