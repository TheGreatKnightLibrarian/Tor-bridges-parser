from __future__ import print_function
import time, requests, re, aioping, asyncio, wget, os, io


def remove_useless_files():
    try:
        print('Removing useless files')
        os.remove('bridges.txt')
        os.remove('ips.txt')
        os.remove('tor-node-list.txt')
        os.remove('valid.txt')
        print('Completed')
    except (FileNotFoundError, FileExistsError):
        print('No useless files were found, continue working')

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

    print('Data received. Testing for bridge functionality begins')

async def check_valid_ip(ip):
    try:
        delay = await aioping.ping(ip.strip(), timeout=1)
        print(f'{ip.strip()} работает.')
        with open('valid.txt', 'a', encoding='utf-8') as file:
            file.write(ip.strip() + '\n')
        extract_valid_from_tor_node_list()
    except TimeoutError:
        print(ip.strip() + ' request timed out')

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
calling functions
'''

remove_useless_files()
parse_and_extract_ip()
time.sleep(15)

with open(r'ips.txt', 'r') as file:
    lines = file.readlines()

with open(r'valid.txt', 'w') as file:
    pass

for ip in lines:
    with open('valid.txt', 'r', encoding='utf-8') as file:
        valid_lines = file.readlines()
    if len(valid_lines) == 5: # here you need to write the number of bridges for parsing, remove the condition to parse all bridges
        break
    else:
        asyncio.run(check_valid_ip(ip))

remove_useless_files()