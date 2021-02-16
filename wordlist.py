
from itertools import product
from string import ascii_lowercase

f = open("demofile.txt", "a")

for i in product(ascii_lowercase, repeat = 5):
    f.write("".join(i))
    f.write("\n")

f.close()