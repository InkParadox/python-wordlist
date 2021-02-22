from itertools import product
from string import ascii_lowercase
import argparse
import multiprocessing as mp
import threading
import datetime
    

def writer(wordsList, filename):

    startTime = datetime.datetime.now()

    # l = mp.Lock()
    # l.acquire()

    f = open(filename, "a")

    for i in wordsList:
        f.write(i + "\n")
    
    f.close()

    # l.release()

    endTime = datetime.datetime.now()
    print(endTime - startTime)


def txtWriter(start, batch, path):

    count = 0
    wordsList = []
    processes = []

    for i in product(ascii_lowercase, repeat = start):

        wordsList.append("".join(i))
        count += 1

        if count % batch == 0 and count > 1: 

            filename = path + str(start) + "-character-iteration-part-" + str(count//batch) + ".txt"

            p = mp.Process(target = writer, args=(wordsList, filename))
            p.start()
            processes.append(p)

            wordsList.clear()


    filename = path + str(start) + "-character-iteration-part-" + str((count//batch)+1) + ".txt"
    p = mp.Process(target = writer, args=[wordsList, filename])
    processes.append(p)
    p.start()
    wordsList.clear()

    for i in processes:
        i.join()

if __name__ == "__main__":

    # create parser
    new_parser = argparse.ArgumentParser(description = "Create word list of combination a-z with number of character input.")

    # add arguments
    new_parser.add_argument("-s", "--start", help = "character start count", type = int)
    new_parser.add_argument("-p", "--path", help = "path in which the files will be stored", type = str)
    new_parser.add_argument("-b", "--batch", help = "enter the batches in which the data is to be split", type = int)

    arguments = new_parser.parse_args()

    startTime = datetime.datetime.now()

    txtWriter(arguments.start, arguments.batch, arguments.path)

    endTime = datetime.datetime.now()

    print(endTime - startTime)