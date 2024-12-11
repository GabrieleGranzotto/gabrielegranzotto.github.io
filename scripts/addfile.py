import json
import sys
import shutil

# take the path from command line or call the input command
try:
    path_name = sys.argv[1]
except:
    print("Argument not found, please insert here the file path that you want upload: ")
    path_name = input()

# copy the file in the actual path
actual_path = "../misc/"
try:
    shutil.copy2(path_name, actual_path)
except:
    print("File not found in this directory!")
    exit()

# take only the file name and format it in the right way
file_name = path_name.split(sep="/")[-1]
string = f"                    <li><a href=\"{file_name}\">{file_name}</a></li>\n"

# open and read the JSON file
with open("../json/misc.json", "r") as files:
    data = json.load(files)

# check if is in the list, if not modify the list
if file_name in data["name"]:
    in_list = True
else:
    in_list = False
    data["name"].append(file_name)


if not in_list:
    # upload the modified list
    with open("../json/misc.json", "w") as files:
        json.dump(data, files)

    # find the right row and add the file in that
    with open("../misc/files.html", "r+") as files:
        lines = files.readlines()
        word = "<!-- ADD HERE -->"
        for row in lines:
            if row.find(word) != -1:
                idx = lines.index(row)
                
    lines.insert(idx+1, string)

    with open("../misc/files.html", "w") as files:
        files.writelines(lines)
    print("File successfully added!")
else:
    print("File successfully updated!")

#close the modified file
files.close()
