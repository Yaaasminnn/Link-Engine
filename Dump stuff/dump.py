import os

os.chdir("/home/monemperor/")
with open("./ascii1", "r") as f:
    ascii = f.read()

ascii_fin = ""
for char in ascii:
    if char == "@":
        char = " "
    ascii_fin+=char

print(ascii_fin)