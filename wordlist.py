
from itertools import product
from string import ascii_lowercase
import argparse


def txtWriter(index, start, end, batch, path):

    count = 0
    words_list = []

    f = open(path + str(start) + "-character-iteration-part-" + str(index//batch) + ".txt", "a")

    for j in range(start, end):

        for i in product(ascii_lowercase, repeat = j):

            if count % batch == 0 and count > 2:

                for itr in range (0, len (words_list)):

                    if (count == index or count > index):

                        f.write(str(words_list[itr]) + "\n")

                f.close()
                words_list.clear()

                f = open(path + str(j) + "-character-iteration-part-" + str(count//batch) + ".txt", "a")

            words_list.append("".join(i))
            count += 1

    f.close()

if __name__ == "__main__":

    # create parser
    new_parser = argparse.ArgumentParser(description = "Create word list of combination a-z with number of character input.")

    # add arguments
    new_parser.add_argument("-i", "--index", help = "file index to start from", type = int)
    new_parser.add_argument("-s", "--start", help = "character start count", type = int)
    new_parser.add_argument("-e", "--end", help = "character end count", type = int)
    new_parser.add_argument("-p", "--path", help = "path in which the files will be stored", type = str)
    new_parser.add_argument("-b", "--batch", help = "enter the batches in which the data is to be split", type = int)

    args = new_parser.parse_args()

    txtWriter(args.index, args.start, args.end, args.batch, args.path)
