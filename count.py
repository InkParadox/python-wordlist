import os
import glob
import argparse

new_parser = argparse.ArgumentParser()

new_parser.add_argument("-s", "--start")

args = new_parser.parse_args()

fileName = "data/" + args.start + "-characters/" + str(args.start) + "-character-iteration-part-*.txt"
fileNames = glob.glob(fileName)

if len(fileNames) == 0:
    print("no files for " + str(args.start) + " characters in directory: " + str(os.getcwd()) + "data/" + str(args.start) + "-characters/")
    exit()

total = 0

for j in range(0,len(fileNames)):

    file = open("data/" + args.start + "-characters/" + str(args.start) + "-character-iteration-part-" + str(j+1) + ".txt", "r") 

    Content = file.read() 
    CoList = Content.split("\n") 
    
    result = 0

    for i in CoList: 
        if i: 
            result += 1

    total += result
            
    print("lines in file " + str(j+1) + " : " + str(result))

print("total lines : " + str(total))