import json
import sys
import shutil
import os
import subprocess as sp

class ManageFile:
    def __init__(self):
        with open("../json/token.json", "r") as files:
            data = json.load(files)
        self.username = data["username"]
        repo = data["repo"]
        self.repo_url = f"https://github.com/{self.username}/{repo}"
        self.actual_path = "../misc/"

    def add(self, path_name=-1, flag_commit=False):
        # take the path from command line or call the input command
        if path_name == -1:
            print("Argument not found, please insert here the file path that you want upload: ")
            path_name = input()

        # copy the file in the actual path
        try:
            shutil.copy2(path_name, self.actual_path)
        except:
            print("File not found in this directory!")
            exit

        # take only the file name and format it in the right way
        file_name = path_name.split(sep="/")[-1] # linux and mac version
        file_name = file_name.split(sep="\\")[-1] # windows verision
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
        if flag_commit:
            file_path = f"{self.actual_path}{file_name}"
            self.commit(file_path)

    def remove(self, file_name=-1, flag_commit=False):
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
                exit
            print("deleted!")
        else:
            print("The file name is not present in the directory.")
        
        if flag_commit:
            file_path = f"{self.actual_path}{file_name}"
            self.commit(file_path)
        

    def commit(self, file_path):
        # commit the modified files with manage_files.py in the repository
        html_path = "../misc/files.html"
        json_path = "../json/misc.json"
        commit_message = "commit the modified files with manage_files.py in the repository"
        file_list = [file_path, html_path, json_path]
        self._git_commit(file_list, commit_message)

    def _git_commit(self, file_list, commit_message):
        try:
            for file_path in file_list:
                sp.run(["git", "add", file_path], check=True)
            sp.run(["git", "commit", "-m", commit_message], check=True)
            sp.run(["git", "push", "origin", "main"], check=True)
            print("Commit and Push succesfully done!")
        except sp.CalledProcessError as e:
            print(f"Error during the execution of Git command: {e}")

try: 
    command = sys.argv[1]
    path_file = sys.argv[2]
    have_commit = sys.argv[3]
    if have_commit == "commit":
        flag_commit = True
    if have_commit == "local":
        flag_commit = False

except:
    try:
        if sys.argv[1] == "-help":
            print("Usage: python3 ./manage_files.py [add/remove] [path_file] [commit/local]")
            exit
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
        print("Do you want to commit on Github? [y/n]")
        have_commit = "y"
        if have_commit == "y":
            flag_commit = True
        else:
            flag_commit = False

manage = ManageFile()
if command == "add":
    manage.add(path_file, flag_commit)
if command == "remove":
    manage.remove(path_file, flag_commit)


