import os
import glob
import argparse

new_parser = argparse.ArgumentParser()

new_parser.add_argument("-s", "--start")
new_parser.add_argument("-p", "--path")

args = new_parser.parse_args()

fileName = args.path + args.start + "-character-iteration-part-*.txt"
fileNames = glob.glob(fileName)

result = 0

for j in range(0,len(fileNames)):

    file = open(args.path + args.start + "-character-iteration-part-" + str(j+1) + ".txt", "r") 

    Content = file.read() 
    CoList = Content.split("\n") 
    
    for i in CoList: 
        if i: 
            result += 1
            
    print("lines in file " + str(j+1) + " : " + str(result))