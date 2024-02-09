from __future__ import print_function
import time, requests, re, aioping, asyncio, wget, os, io


def remove_useless_files():
    try:
        print('Удаление безполезных файлов')
        os.remove('bridges.txt')
        os.remove('ips.txt')
        os.remove('tor-node-list.txt')
        print('Готово')
    except (FileNotFoundError, FileExistsError):
        print('Безполезные файлы не найдены, продолжаем работу')

def parse_and_extract_ip():
    responce = requests.get('https://drew-phillips.com/tor-node-list.txt')
    wget.download('https://drew-phillips.com/tor-node-list.txt')
    with open('bridges.txt', 'w', encoding='utf-8') as file:
        file.write(responce.text)

    with open('bridges.txt', 'r', encoding='utf-8') as file:
        file = file.read()

    pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    matches = pattern.findall(file)
    for _ in matches:
        with open(r'ips.txt', 'a') as file:
            file.write(_ + '\n')

    with open(r'ips.txt', 'a') as file:
        file.write(_ + '\n')

    print('Данные получены. Начинается проверка на работоспособность мостов')

async def check_valid_ip(ip):
    try:
        delay = await aioping.ping(ip.strip(), timeout=1)
        print(f'{ip.strip()} работает.')
        with open('valid.txt', 'a', encoding='utf-8') as file:
            file.write(ip.strip() + '\n')
    except TimeoutError:
        print(ip.strip() + ' превышено время ожидания запроса')

def extract_valid_from_tor_node_list():
    with open(r'valid.txt', 'r') as ip_file:
        ips = ip_file.readlines()


    with io.open('tor-node-list.txt', encoding='utf-8') as file:
        for line in file:
            for ip in ips:
                if ip.strip() in line:
                    bridge = line.split()
                    with open('output.txt', 'a', encoding='utf-8') as file:
                        file.write(bridge[1] + ':' + bridge[2] + '\n' + bridge[4] + '\n')

'''
вызов функций
'''

remove_useless_files()
parse_and_extract_ip()
time.sleep(10)

with open(r'ips.txt', 'r') as file:
    lines = file.readlines()

with open(r'valid.txt', 'w') as file:
    pass

for ip in lines:
    with open('valid.txt', 'r', encoding='utf-8') as file:
        valid_lines = file.readlines()
    if len(valid_lines) == 20: #здесь нужно написать количество мостов для парсинга, убери условие чтобы парсить все мосты
        break
    else:
        asyncio.run(check_valid_ip(ip))

extract_valid_from_tor_node_list()
remove_useless_files()