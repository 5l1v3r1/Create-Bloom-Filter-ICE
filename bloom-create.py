# !/usr/bin/python3
# encoding=utf8
# -*- coding: utf-8 -*-
"""
@author: Noname400
"""
version = '3.14 23.11.22'

from sys import argv
from os import system, path, name, mkdir
from time import time
from datetime import datetime
from lib.secp256k1_lib import dump_bloom_file, Fill_in_bloom, check_in_bloom
from cashaddress import convert
from bitcoinlib.keys import addr_to_pubkeyhash, addr_bech32_to_pubkeyhash, deserialize_address

def cls():
    system('cls' if name=='nt' else 'clear')

def date_str():
    now = datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")

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
            if len(res) < 26 or len(res) > 63:
                err += 1
            elif res[:2] == 's-' or res[:2] == 'm-' or res[:2] == 'd-':
                err += 1
            elif len(res) == 40:
                lis.append(res.lower())
                hash_ += 1                
            elif res[:2] == '0x':
                lis.append(res.lower()[2:])
                eth_0x_ += 1
            elif (res[:4] == 'ltc1' and len(res) == 43) or (res[:4] == 'ltc1' and len(res) == 63):
                try:
                    h160 = addr_bech32_to_pubkeyhash(res, prefix='ltc', as_hex=True)
                except:
                    cancel += 1
                    continue
                else:
                    lis.append(h160)
                    bech_ += 1
            elif (res[:3] == 'bc1' and len(res) == 42) or (res[:3] == 'bc1' and len(res) == 62):
                try:
                    h160 = addr_bech32_to_pubkeyhash(res, as_hex=True)
                except:
                    cancel += 1
                    continue
                else:
                    lis.append(h160)
                    bech_ += 1
            elif (res[:1] == 'q' and len(res) == 42) or res[:1] == 'p' and len(res) == 42:
                addr_bch = convert.to_legacy_address(f'bitcoincash:{res}')
                h160 = deserialize_address(addr_bch, encoding='base58')['public_key_hash']
                lis.append(h160)
                base_ += 1
                conv_ +=1
            elif res[:2] == 't1' or res[:2] == 't3':
                #h160 = addr_to_pubkeyhash(res, as_hex=True, encoding='base58')
                h160 = deserialize_address(res, encoding='base58')['public_key_hash']
                lis.append(h160[2:])
                hash_ += 1
            else:
                #print(res)
                try:
                    h160 = deserialize_address(res, encoding='base58')['public_key_hash']
                except:
                    #print(res)
                    cancel += 1
                    continue
                lis.append(h160)
                base_ += 1
            count += 1
            if count == line_10:
                print(f"> error: {err} | cancel: {cancel} | Convert: {conv_} | ETH 0x: {eth_0x_}| ETH/H160: {hash_} | bech32: {bech_} | base58:{base_} | total: {count}",end='\r')
                line_10 +=100000
    print('\n')
    print(f"[I] Finish create list ... ({time()-st:.2f} sec) | Total line: {len(lis)}")
    # line_count = len(lis)
    print(f"[I] Start sorted list and add to bloom...")
    st = time()
    lis.sort()
    #bloom_filter = BloomFilter(size=line_count, fp_probability=1e-12)
    _bits, _hashes, _bf = Fill_in_bloom(lis, 1e-12)
    dump_bloom_file(file_out, _bits, _hashes, _bf)

    # for h in lis:
    #     bloom_filter.add(h)
    print(f"[I] Finish sorted list and add to bloom: ({time()-st:.2f}) sec")

    st = time()
    # with open(file_out, "wb") as fp:
    #     bloom_filter.save(fp)
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
    