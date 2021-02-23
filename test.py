import itertools
import string

f = open("product-test.txt","a")

for i in itertools.product(string.ascii_lowercase, repeat = 5):
    f.write("".join(i) + "\n")

f = open("permutations-test.txt","a")

for i in itertools.permutations(string.ascii_lowercase, 5):
    f.write("".join(i) + "\n")

f = open("combination-with-replacement-test.txt","a")

for i in itertools.combinations_with_replacement(string.ascii_lowercase, 5):
    f.write("".join(i) + "\n")

f = open("combination-test.txt","a")

for i in itertools.combinations(string.ascii_lowercase, 5):
    f.write("".join(i) + "\n")

f = open("combination-test.txt","r")

result = 0

lines = f.read()
line = lines.split("\n")

for i in line:
    if i:
        result += 1

f.close()

print(result)
