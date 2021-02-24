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
   

def writer(wordsList, words, walletAddress):

    mnemo = Mnemonic("english")

    # words = "winner equip edge stock junior kangaroo avocado wild escape never guide embody comfort slide account cycle hip unaware field view warfare toss soup small"

    for j in wordsList:

        seed = mnemo.to_seed(words,passphrase=j)
        # Create from seed
        bip44_mst = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)

        # Derive account 0 for Bitcoin: m/44'/0'/0'
        bip44_acc = bip44_mst.Purpose().Coin().Account(0)

        # Derive the external chain: m/44'/0'/0'/0
        bip44_change = bip44_acc.Change(Bip44Changes.CHAIN_EXT)

        # Derive the first 20 addresses of the external chain: m/44'/0'/0'/0/i
        for i in range(10):
            bip44_addr = bip44_change.AddressIndex(i)
            # Print extended keys and address
            # print(bip44_addr.PrivateKey().ToExtended())
            # print(bip44_addr.PublicKey().ToExtended())
            if bip44_addr.PublicKey().ToAddress() == walletAddress:
                print(j)
                exit()

        print(j + " done")


def txtWriter(start, batch, words, walletAddress):

    count = 0
    wordsList = []
    processes = []

    for i in product(ascii_lowercase, repeat = start):

        while psutil.virtual_memory()._asdict().get("percent") > 95:
            print("memory exceeding 96% ... freeing up the RAM ... ")
            time.sleep(3)

        wordsList.append("".join(i))
        count += 1

        if count % batch == 0 and count > 1: 

            p = mp.Process(target = writer, args=[wordsList, words, walletAddress])
            p.start()
            processes.append(p)
            wordsList.clear()
            

    p = mp.Process(target = writer, args=[wordsList, words, walletAddress])
    processes.append(p)
    p.start()
    wordsList.clear()

    for i in processes:
        i.join()

if __name__ == "__main__":

    new_parser = argparse.ArgumentParser(description = "Create word list of combination a-z with number of character input.")

    new_parser.add_argument("-s", "--start", help = "character start count", type = int)
    new_parser.add_argument("-e", "--end", help = "character end count", type = int)
    new_parser.add_argument("-b", "--batch", help = "enter the batches in which the data is to be split", type = int)
    new_parser.add_argument("-w", "--words", help = "enter wallet address", type = str)
    new_parser.add_argument("-a", "--address", help = "enter wallet address", type = str)

    arguments = new_parser.parse_args()

    startTime = datetime.datetime.now()

    start = arguments.start
    
    if arguments.end:
        end = arguments.end
    else:
        end = start

    iterProcesses = []

    for i in range(0, end+1 - start):
        p = mp.Process(target = txtWriter, args = [start, arguments.batch, arguments.words, arguments.address])
        p.start()
        iterProcesses.append(p)
        start += 1

    for i in iterProcesses:
        i.join()

    endTime = datetime.datetime.now()

    print(endTime - startTime)
