import binascii
import argparse
from bip_utils import Bip44, Bip44Coins, Bip44Changes
from mnemonic import Mnemonic
from itertools import product
from string import ascii_lowercase
import multiprocessing as mp
import datetime
import psutil
import time
import os
from numba import jit, cuda


mnemo = Mnemonic("english")


def rippleAddressChecker(wordsList, words, walletAddress, addressNum):

    for phrase in wordsList:

        seed = mnemo.to_seed(words, passphrase = phrase)
        # Create from seed
        bip44_mst = Bip44.FromSeed(seed, Bip44Coins.RIPPLE)

        # Derive account 0 for Bitcoin: m/44'/0'/0'
        bip44_acc = bip44_mst.Purpose().Coin().Account(0)

        # Derive the external chain: m/44'/0'/0'/0
        bip44_change = bip44_acc.Change(Bip44Changes.CHAIN_EXT)

        # Derive the addresses of the external chain: m/44'/0'/0'/0/i
        for i in range(addressNum+1):
            bip44_addr = bip44_change.AddressIndex(i)

            # Check whether provided address is equal to the generated address
            if bip44_addr.PublicKey().ToAddress() == walletAddress:
                print(phrase)
                print(datetime.datetime.now())
                exit()
        
    wordsList.clear()

def bitcoinAddressChecker(wordsList, words, walletAddress, addressNum):

    for phrase in wordsList:

        seed = mnemo.to_seed(words, passphrase = phrase)
        # Create from seed
        bip44_mst = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)

        # Derive account 0 for Bitcoin: m/44'/0'/0'
        bip44_acc = bip44_mst.Purpose().Coin().Account(0)

        # Derive the external chain: m/44'/0'/0'/0
        bip44_change = bip44_acc.Change(Bip44Changes.CHAIN_EXT)

        # Derive the first 20 addresses of the external chain: m/44'/0'/0'/0/i
        for i in range(addressNum+1):
            bip44_addr = bip44_change.AddressIndex(i)

            # Check whether provided address is equal to the generated address
            if bip44_addr.PublicKey().ToAddress() == walletAddress:
                print(phrase)
                print(datetime.datetime.now())
                exit()
        
    wordsList.clear()


def batchHandler(start, batch, words, walletAddress, addressNum, coin):

    count = 0
    wordsList = []
    processes = []

    for i in product(ascii_lowercase, repeat = start):

        wordsList.append("".join(i))
        count += 1

        if count % batch == 0 and count > 1: 

            if coin == "btc":
                p = mp.Process(target = bitcoinAddressChecker, args=[wordsList, words, walletAddress, addressNum])
                p.start()
                processes.append(p)
                wordsList.clear()

            if coin == "xrp":
                p = mp.Process(target = rippleAddressChecker, args=[wordsList, words, walletAddress, addressNum])
                p.start()
                processes.append(p)
                wordsList.clear()

    if coin == "btc":
        p = mp.Process(target = bitcoinAddressChecker, args=[wordsList, words, walletAddress, addressNum])
        p.start()
        processes.append(p)
        wordsList.clear()

    if coin == "xrp":
        p = mp.Process(target = bitcoinAddressChecker, args=[wordsList, words, walletAddress, addressNum])
        p.start()
        processes.append(p)
        wordsList.clear()

    for i in processes:
        i.join()

if __name__ == "__main__":

    new_parser = argparse.ArgumentParser(description = "Create word list of combination a-z with number of character input.")

    new_parser.add_argument("-s","--start", help = "character start count", type = int)
    new_parser.add_argument("-e","--end", help = "character end count", type = int)
    new_parser.add_argument("-w","--words", help = "enter wallet address", type = str)
    new_parser.add_argument("-a","--address", help = "enter wallet address", type = str)
    new_parser.add_argument("-c","--coin", help = "coin to search", type = str)
    new_parser.add_argument("-n","--numberOfAddress", help = "number of addresses to search", type = int)

    arguments = new_parser.parse_args()

    print(datetime.datetime.now())

    start = arguments.start
    
    if arguments.end:
        end = arguments.end
    else:
        end = start

#==================================================================================================================================================

    iterProcesses = []

    for i in range(0, end+1 - start):
        p = mp.Process(target = batchHandler, args = [start, 30000, arguments.words, arguments.address, arguments.numberOfAddress, arguments.coin])
        p.start()
        iterProcesses.append(p)
        start += 1

    for i in iterProcesses:
        i.join()

# python passphrase_wordlist_check.py -s 4 -c "btc" -n 10 -w "physical fly just divert nothing mother parent napkin fantasy journey tenant invite snake timber inform zebra wheel field nothing nephew creek rather spike celery" -a "17o9ZYh6HyS5yYzY15Zeq9Xym3tFy4mG8Q"