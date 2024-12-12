import json
import sys
import shutil
import os
import subprocess as sp

class ManageFile:
    def __init__(self):
        with open("../json/token.json", "r") as files:
            data = json.load(files)
        self.token = data["token"]
        self.username = data["username"]
        self.repo_url = f"https://{self.username}:{self.token}@github.com/{self.username}/{data["repo"]}"

    def add(self, path_name=-1):
        # take the path from command line or call the input command
        if path_name == -1:
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

    def remove(self, file_name=-1):
        # take the name of the file that has to remove from command line or call the input command
        if file_name == -1:
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
                exit()
            print("deleted!")
        else:
            print("The file name is not present in the directory.")

    def _git_commit(file_path, commit_message, repo_url):
        try:
            sp.run(["git", "remote", "set-url", "origin", repo_url], check=True)
            sp.run(["git", "add", file_path], check=True)
            sp.run(["git", "commit", "-m", commit_message], check=True)
            sp.run(["git", "push"], check=True)
            print("Commit and Push succesfully done!")
        except sp.CalledProcessError as e:
            print(f"Error during the execution of Git command: {e}")


# file_path = "path/del/file"
# git_commit(file_path, "commit trammite https e token", repo_url)

try: 
    command = sys.argv[1]
    path_file = sys.arg[2]
except:
    print("Do you want to add or remove file? [add/remove]")
    command = input()
    if command=="add":
        print("\nWhich is the path of the file?")
        path_file = input()
    if command=="remove":
        print("\nWhich is the name of the file?")
        path_file = input()
    else:
        print("Command unknown!")
    try:
        flag_commit = sys.arg[3]
    except:
        flag_commit = False

manage = ManageFile()
if command == "add":
    manage.add(path_file, flag_commit)
if command == "remove":
    manage.remove(path_file, flag_commit)

