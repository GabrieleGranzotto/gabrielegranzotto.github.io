with open("./files.html", "r+") as files:
    lines = files.readlines()
    title = "Misc Files"
    title_flag = False
    word = "</ul>"
    for row in lines:
        if row.find(title) != -1 and title_flag == False:
            title_flag = True
        if row.find(word) != -1 and title_flag == True:
            print('string exists in file')
            print('line Number:', lines.index(row))
            idx = lines.index(row)
            break

file_name = "PLACE HOLDER"
string = f"                    <li><a href=\"{file_name}\">{file_name}</a></li>\n"

with open("./files.html", "r") as files:
    lines = files.readlines()

lines.insert(idx, string)

with open("./files.html", "w") as files:
    files.writelines(lines)

files.close()