from itertools import product
from string import ascii_lowercase
import multiprocessing as mp
import datetime
import psutil
import argparse
import time
import os
    
def chunks(LIST, NUMBER_OF_PARTS):
    # For item i in a range that is a length of l,
    for i in range(0, len(LIST), NUMBER_OF_PARTS):
        # Create an index range for l of n items:
        yield LIST[i:i+NUMBER_OF_PARTS]

def writer(wordsList, filename, number):

    f = open(filename, "a")

    for i in wordsList:
        f.write(i + "\n")
    
    f.close()

    print("file " + number + "closed")

def txtWriter(start, batch, path):

    count = 0
    wordsList = []
    processes = []

    for i in product(ascii_lowercase, repeat = start):

        wordsList.append("".join(i))
        count += 1

        if count % batch == 0 and count > 1: 

            if count//batch > 6662:
                filename = path + str(start) + "-characters/" + str(start) + "-character-iteration-part-" + str(count//batch) + ".txt"

                p = mp.Process(target = writer, args=[wordsList, filename, str(count//batch)])
                p.start()
                processes.append(p)
                wordsList.clear()
            else:
                wordsList.clear()
            
    if count//batch > 6662:
        filename = path + str(start) + "-characters/" + str(start) + "-character-iteration-part-" + str((count//batch)+1) + ".txt"
        p = mp.Process(target = writer, args=[wordsList, filename, str((count//batch)+1)])
        processes.append(p)
        p.start()
        wordsList.clear()
    else:
        wordsList.clear()

    for i in processes:
        i.join()

if __name__ == "__main__":

    new_parser = argparse.ArgumentParser(description = "Create word list of combination a-z with number of character input.")

    new_parser.add_argument("-s", "--start", help = "character start count", type = int)
    new_parser.add_argument("-e", "--end", help = "character end count", type = int)
    new_parser.add_argument("-p", "--path", help = "path in which the files will be stored", type = str)
    new_parser.add_argument("-b", "--batch", help = "enter the batches in which the data is to be split", type = int)

    arguments = new_parser.parse_args()

    startTime = datetime.datetime.now()

    start = arguments.start
    
    if arguments.end:
        end = arguments.end
    else:
        end = start

    for i in range(start, end+1):

        if os.path.exists(arguments.path):
            pass
        else:
            os.mkdir(arguments.path)

        if os.path.exists(arguments.path + str(i) + "-characters/"):
            pass
        else:
            os.mkdir(arguments.path + str(i) + "-characters/")

    iterProcesses = []

    for i in range(0, end+1 - start):
        p = mp.Process(target = txtWriter, args = [start, arguments.batch, arguments.path])
        p.start()
        iterProcesses.append(p)
        start += 1

    for i in iterProcesses:
        i.join()

    endTime = datetime.datetime.now()

    print(endTime - startTime)
