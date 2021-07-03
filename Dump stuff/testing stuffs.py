import os

dir = os.getcwd() #gets and prints the current working directory
print(dir)
parent = os.path.dirname(dir) #gets the parent dir
print(parent)
dir = os.listdir(parent+"/graphics/maps") #looks in the graphics/maps folder

files= [] #json array

for file in dir:
    #looks for extensions and adds json extensions to json array. if its a folder, tell us
    dot = file.rfind(".") 
    if dot != -1:
    	ext = file[dot:]
    	print(ext)
    	if ext == ".json":
        	files.append(file)
        	
    else: print(file)

print(files) #print the json array
