import itertools
import string

f = open("product-test.txt","a")

for i in itertools.product(string.ascii_lowercase, repeat = 5):
    f.write("".join(i) + "\n")

# f = open("permutations-test.txt","a")

# for i in itertools.permutations(string.ascii_lowercase, 5):
#     f.write("".join(i) + "\n")

f.close()