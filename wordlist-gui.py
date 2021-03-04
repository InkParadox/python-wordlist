from itertools import product
from string import ascii_lowercase
import multiprocessing as mp
from tkinter import Tk, Frame, Entry, Button, Label, StringVar, IntVar
import datetime
import psutil
import argparse
import time
import os
    
class Menu:

    def __init__(self):
        self.root = Tk()
        self.root.title("Word List Generator")
        self.root.geometry("330x200")
        
        self.path = StringVar()
        self.batch = IntVar()
        self.start = IntVar() 
        self.end = IntVar()
        self.textFile = IntVar()

        self.frame1 = Frame(self.root, height = 150, width = 200, pady = 20)
        self.frame1.grid(row = 0, column = 0)
        self.frame2 = Frame(self.root, height = 150, width = 100)
        self.frame2.grid(row = 1, column = 0)
        
        self.startLabel = Label(self.frame1, text = "Alphabet count : ")
        self.startLabel.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.startEntry = Entry(self.frame1, width = 15, textvariable = self.start)
        self.startEntry.grid(row = 0, column = 1, pady = 5)

        self.endLabel = Label(self.frame1, text = " to ")
        self.endLabel.grid(row = 0, column = 2, pady = 5)
        self.endEntry = Entry(self.frame1, width = 15, textvariable = self.end)
        self.endEntry.grid(row = 0, column = 3, pady = 5)

        self.pathLabel = Label(self.frame1, text = "Folder path : ")
        self.pathLabel.grid(row = 1, column = 0, padx = 5, pady = 5)
        self.pathEntry = Entry(self.frame1, width = 35, textvariable = self.path)
        self.pathEntry.grid(row = 1, column = 1, columnspan = 3, pady = 5)

        self.batchLabel = Label(self.frame1, text = "Batch count : ")
        self.batchLabel.grid(row = 2, column = 0, padx = 5, pady = 5)
        self.batchEntry = Entry(self.frame1, width = 35, textvariable = self.batch)
        self.batchEntry.grid(row = 2, column = 1, columnspan = 3, pady = 5)

        self.textFileLabel = Label(self.frame1, text = "Text file number : ")
        self.textFileLabel.grid(row = 3, column = 0, padx = 5, pady = 5)
        self.textFileEntry = Entry(self.frame1, width = 35, textvariable = self.textFile)
        self.textFileEntry.grid(row = 3, column = 1, columnspan = 3, pady = 5)

        self.generateButton = Button(self.frame2, text = "Generate words !", bg = "light gray", padx = 100, command = self.generateButtonClick)
        self.generateButton.grid(row = 0, column = 0)

        self.root.mainloop()

    def generateButtonClick(self):

        start = self.start.get()

        path = r""+self.path.get()

        batch = self.batch.get()

        mid = self.textFile.get()
        
        if self.end.get():
            end = self.end.get()
        else:
            end = self.start.get()
        
        print(start, end, batch, path)

        self.frame1.destroy()
        self.frame2.destroy()
        self.root.destroy()

        for i in range(start, end+1):

            if os.path.exists(path):
                pass
            else:
                os.mkdir(path)

            if os.path.exists(path + str(i) + "-characters/"):
                pass
            else:
                os.mkdir(path + str(i) + "-characters/")

        self.iterProcesses = []

        for i in range(0, end+1 - start):
            self.p = mp.Process(target = txtWriter, args = [start, batch, path, mid])
            self.p.start()
            self.iterProcesses.append(self.p)
            start += 1

        for i in self.iterProcesses:
            i.join()

def writer(wordsList, filename, number):

    f = open(filename, "a")

    for i in wordsList:
        f.write(i + "\n")
    
    f.close()

    print("file " + number + "closed")


def txtWriter(start, batch, path, mid):

    count = 0
    wordsList = []
    processes = []

    for i in product(ascii_lowercase, repeat = start):

        wordsList.append("".join(i))
        count += 1

        if count % batch == 0 and count > 1: 
            
            if count//batch > mid:
                filename = path + str(start) + "-characters/" + str(start) + "-character-iteration-part-" + str(count//batch) + ".txt"
                p = mp.Process(target = writer, args=[wordsList, filename, str(count//batch)])
                p.start()
                processes.append(p)
                wordsList.clear()

            else:
                wordsList.clear()
            
    if count//batch > mid:
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

    a = Menu()
