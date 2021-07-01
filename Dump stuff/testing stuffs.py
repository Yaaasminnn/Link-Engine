import os

dir = os.getcwd()
print(dir)
parent = os.path.dirname(dir)
print(parent)
dir = os.listdir(dir)

files= []

for file in dir:
    dot = file.rfind(".")
    ext = file[dot:]
    print(ext)
    if ext == ".json":
        files.append(file)

print(files)