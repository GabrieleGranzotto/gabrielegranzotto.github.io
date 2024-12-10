import json

file_name = "PLACE HOLDER"
string = f"                    <li><a href=\"{file_name}\">{file_name}</a></li>\n"

# Open and read the JSON file
with open("../json/misc.json", "r") as files:
    data = json.load(files)

data["name"].append(file_name)

with open("../json/misc.json", "w") as files:
    json.dump(data, files)

with open("../misc/files.html", "r+") as files:
    lines = files.readlines()
    word = "<!-- ADD HERE -->"
    for row in lines:
        if row.find(word) != -1:
            print('string exists in file')
            idx = lines.index(row)
            print('line Number:', idx)
            
lines.insert(idx+1, string)

with open("../misc/files.html", "w") as files:
    files.writelines(lines)

files.close()