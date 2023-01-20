# #!/usr/bin/python3
# encoding=utf-8
# -*- coding: utf-8 -*-
"""
@author: NonameHUNT
@GitHub: https://github.com/Noname400
@telegram: https://t.me/NonameHunt
"""

version = '4.1 20.01.23'

from sys import argv
from os import system, path, name, mkdir
from time import time
from signal import SIGINT, SIG_IGN, signal
from datetime import datetime
from lib.secp256k1_lib import dump_bloom_file, Fill_in_bloom, b58_decode, bech32_address_decode
from cashaddress import convert
from multiprocessing import Pool, freeze_support, cpu_count
from colorama import Back, Fore, Style, init
init(autoreset = True)

class color:
    yellow = Fore.YELLOW+Style.BRIGHT
    red = Fore.RED+Style.BRIGHT
    clear = Style.RESET_ALL
    green = Fore.GREEN+Style.BRIGHT
    magenta = Fore.LIGHTMAGENTA_EX+Style.BRIGHT
    blink = Fore.RED+Style.DIM
    cyan = Fore.CYAN+Style.BRIGHT
    back = '\033[1A'
    clear_screen = '\x1b[2J'
    
def convert_int(num:int):
    dict_suffix = {0:'key', 1:'Kkey', 2:'Mkey', 3:'Gkey', 4:'Tkey', 5:'Pkey', 6:'Ekeys'}
    num *= 1.0
    idx = 0
    for ii in range(len(dict_suffix)-1):
        if int(num/1000) > 0:
            idx += 1
            num /= 1000
    return ('%.2f'%num), dict_suffix[idx]

def init_worker():
    signal(SIGINT, SIG_IGN)

def cls():
    system('cls' if name=='nt' else 'clear')

def date_str():
    now = datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")

def norm_hash(hash):
    res = ''
    if len(hash) == 52:
        res = hash[4:44]
    elif len(hash) == 50:
        res = hash[2:42]
    else:
        print(f'Error HASH:{hash}')
        return 0
    return res

def create_bf(res):
    lis = []
    if len(res) < 26 or len(res) > 43:
        return None
    elif res[:2] == 's-' or res[:2] == 'm-' or res[:2] == 'd-':
        return None
    elif len(res) == 40:
        lis.append(res.lower())
    elif res[:2] == '0x':
        lis.append(res.lower()[2:])
    elif (res[:4] == 'ltc1' and len(res) == 43):
        try:
            h160 = bech32_address_decode(res, 21)
        except:
            return None
        else:
            lis.append(h160)
    elif (res[:3] == 'bc1' and len(res) == 42):
        try:
            h160 = bech32_address_decode(res, 0)
        except:
            return None
        else:
            lis.append(h160)
    elif (res[:1] == 'q' and len(res) == 42) or res[:1] == 'p' and len(res) == 42:
        addr_bch = convert.to_legacy_address(f'bitcoincash:{res}')
        h160 = b58_decode(addr_bch)
        res = norm_hash(h160)
        if res == 0: 
            return None
        lis.append(res)
    elif res[:2] == 't1' or res[:2] == 't3':
        h160 = b58_decode(res)
        res = norm_hash(h160)
        if res == 0: 
            return None
        lis.append(res)
    else:
        h160 = b58_decode(res)
        res = norm_hash(h160)
        if res == 0: 
            return None
        lis.append(res)
    return lis

if __name__ == "__main__":
    freeze_support()
    cls()
    th = int(argv[1], 10)
    if th < 1 or th > cpu_count():
        print(f'Error cores')
    div = int(argv[2], 10)
    file_in = argv[3]
    prefix = argv[4]
    
    line_count = 0
    step = 10000
    total_count = 0
    file_count = 0
    print_count = 0
    co = 0
    err = 0
    l = []
    tmp = 0
    BF_list = []
    print('-'*70,end='\n')
    print(f'[I] Version: {color.cyan}{version}')
    print(f'[I] Start proogramm: {color.cyan}{date_str()}')
    print(f'[I] Total kernel of CPU: {color.cyan}{cpu_count()}')
    print(f'[I] Used kernel: {color.cyan}{th}')
    print(f'[I] File address : {color.cyan}{file_in}')
    print(f'[I] Prefix :{color.cyan} {prefix}')
    print(f'[I] Divider line : {color.cyan}{div}')
    print('-'*70,end='\n')
    global_timer = time()
    st = time()
    pool = Pool(th, init_worker)
    with open(file_in, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            line_count += 1
            l.append(line)
            if line_count == step:
                line_count = 0
                results = pool.map(create_bf, l)
                for res in results:
                    if res == None:
                        err += 1
                        continue
                    if len(res[0]) < 40 or len(res[0]) > 40:
                        err += 1
                        print(f'\n[W] <> 40')
                        continue
                        
                    BF_list.append(res[0])
                    total_count += 1
                    co += 1
                    tmp += 1
                if co >= div:
                    st_ = time()
                    print(f'\n[I] {color.green}Сортируем... {len(BF_list)} элементов')
                    BF_list.sort()
                    print(f'[I] {color.green}Закончили сортировать. ({time()-st_:.2f}) sec')
                    st_ = time()
                    print(f'[I] {color.green}Создаем блюм - {prefix}{file_count}.bin')
                    _bits, _hashes, _bf = Fill_in_bloom(BF_list, _fp = 0.00000000000001)
                    dump_bloom_file(f'{prefix}{file_count}.bin', _bits, _hashes, _bf)
                    print(f'[I] {color.green}Закончили создание и запись. ({time()-st_:.2f}) sec')
                    BF_list = []
                    file_count += 1
                    co = 0
                else:
                    if print_count == 100:
                        speed_float, speed_hash = convert_int(tmp/(time()-st))
                        print(' '*110,end='\r')
                        print(f'{color.yellow}[Total time: {time()-global_timer:.2f}] [Total Hash: {total_count}] [error:{err}] [Speed:{speed_float} {speed_hash}]',end='\r')
                        print_count = 0
                    else: print_count += 1
                    
                    
                tmp = 0
                st = time()
                l = []
                results = []
                
        else:
            results = pool.map(create_bf, l)
            st_ = time()
            print(f'\n[I] {color.green}Сортируем... {len(BF_list)} элементов')
            BF_list.sort()
            print(f'[I] {color.green}Закончили сортировать. ({time()-st_:.2f}) sec')
            st_ = time()
            print(f'[I] {color.green}Создаем блюм - {prefix}{file_count}.bin')
            _bits, _hashes, _bf = Fill_in_bloom(BF_list, _fp = 0.00000000000001)
            dump_bloom_file(f'{prefix}{file_count}.bin', _bits, _hashes, _bf)
            print(f'[I] {color.green}Закончили создание и запись. ({time()-st_:.2f}) sec')
            
    print(f'Finish.')
            