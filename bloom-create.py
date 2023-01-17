# #!/usr/bin/python3
# encoding=utf-8
# -*- coding: utf-8 -*-
"""
@author: NonameHUNT
@GitHub: https://github.com/Noname400
@telegram: https://t.me/NonameHunt
"""

version = '3.17 10.01.23'

from sys import argv
from os import system, path, name, mkdir
from time import time
from datetime import datetime
from lib.secp256k1_lib import dump_bloom_file, Fill_in_bloom, b58_decode, bech32_address_decode
from cashaddress import convert

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

def create_bf(file_in,file_out):
    bech_ = 0
    base_ = 0
    cancel = 0
    hash_ = 0
    eth_0x_ = 0
    conv_ = 0
    line_10 = 100000
    count = 0
    err= 0
    lis = []
    print(f"[I] Start create list ...")
    st = time()
    with open(file_in, "r") as f:
        for line in f:
            res = line.strip()
            if len(res) < 26 or len(res) > 43:
                err += 1
            elif res[:2] == 's-' or res[:2] == 'm-' or res[:2] == 'd-':
                err += 1
            elif len(res) == 40:
                lis.append(res.lower())
                hash_ += 1                
            elif res[:2] == '0x':
                lis.append(res.lower()[2:])
                eth_0x_ += 1
            elif (res[:4] == 'ltc1' and len(res) == 43):
                try:
                    h160 = bech32_address_decode(res, 21)
                except:
                    cancel += 1
                    continue
                else:
                    lis.append(h160)
                    bech_ += 1
            elif (res[:3] == 'bc1' and len(res) == 42):
                try:
                    h160 = bech32_address_decode(res, 0)
                except:
                    cancel += 1
                    continue
                else:
                    lis.append(h160)
                    bech_ += 1
            elif (res[:1] == 'q' and len(res) == 42) or res[:1] == 'p' and len(res) == 42:
                addr_bch = convert.to_legacy_address(f'bitcoincash:{res}')
                h160 = b58_decode(addr_bch)
                res = norm_hash(h160)
                if res == 0: 
                    cancel += 1
                    continue
                lis.append(res)
                base_ += 1
                conv_ +=1
            elif res[:2] == 't1' or res[:2] == 't3':
                h160 = b58_decode(res)
                res = norm_hash(h160)
                if res == 0: 
                    cancel += 1
                    continue
                lis.append(res)
                hash_ += 1
            else:
                h160 = b58_decode(res)
                res = norm_hash(h160)
                if res == 0: 
                    cancel += 1
                    continue
                lis.append(res)
                base_ += 1
            count += 1
            if count == line_10:
                print(f"> error: {err} | cancel: {cancel} | Convert: {conv_} | ETH 0x: {eth_0x_}| ETH/H160: {hash_} | bech32: {bech_} | base58:{base_} | total: {count}",end='\r')
                line_10 +=100000
    print('\n')
    print(f"[I] Finish create list ... ({time()-st:.2f} sec) | Total line: {len(lis)}")
    
    print(f"[I] Start sorted list and add to bloom...")
    st = time()
    #lis.sort()
    _bits, _hashes, _bf = Fill_in_bloom(lis, 0.000000000000001)
    dump_bloom_file(file_out, _bits, _hashes, _bf)
    print(f"[I] Finish sorted list and add to bloom: ({time()-st:.2f}) sec")
    print(f"[I] Bloom filter saved... ({time()-st:.2f} sec)")
    print(f"[END] error: {err} | Convert: {conv_} | ETH 0x: {eth_0x_}| ETH/H160: {hash_} | bech32: {bech_} | base58:{base_} | total: {count}",end='\r')
    print('\n')

if __name__ == "__main__":
    cls()
    file_in = argv[1]
    file_out = argv[2]
    if len (argv) < 3:
        print ("[E] Error. Too few options.")
        exit(1)

    if len (argv) > 3:
        print ("[E] Error. Too many parameters.")
        exit(1)
    print(f"[I] Start line count ...")
    print(f"[I] Finish line count ...")
    print('-'*70,end='\n')
    print(f'[I] Version: {version}')
    print(f'[I] File address : {file_in}')
    print(f'[I] Bloom Filter : {file_out}')
    print(f'[I] START: {date_str()}')
    print('-'*70,end='\n')
    create_bf(file_in,file_out)
    