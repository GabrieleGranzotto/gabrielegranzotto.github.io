import json
import sys
import os

# take the name of the file that has to remove from command line or call the input command
try:
    file_name = sys.argv[1]
except:
    print("Argument not found, please insert here the file name of the file you want remove: ")
    file_name = input()

# open and read the JSON file
with open("../json/misc.json", "r") as files:
    data = json.load(files)

flag_word = False
for item in data["name"]:
    if item == file_name:
        data["name"].remove(item)
        flag_word = True

# upload the modified list
with open("../json/misc.json", "w") as files:
    json.dump(data, files)

if flag_word:
    # find the right row and add the file in that
    with open("../misc/files.html", "r") as files:
        lines = files.readlines()
        for row in lines:
            if row.find(file_name) != -1:
                idx = lines.index(row)
    with open("../misc/files.html", "r") as files:
        lines = files.readlines()
        ptr = 1
        with open("../misc/files.html", "w") as files:
            for row in lines:
                if ptr != idx+1:
                    files.write(row)
                ptr += 1
    try:
        os.remove(f"../misc/{file_name}")
    except:
        print("file can not be removed from the specified directory.")
    print("deleted!")
else:
    print("The file name is not present in the directory.")