import subprocess as sp
import os

def git_commit(file_path, commit_message, repo_url):
    try:
        sp.run(["git", "remote", "set-url", "origin", repo_url], check=True)
        sp.run(["git", "add", file_path], check=True)
        sp.run(["git", "commit", "-m", commit_message], check=True)
        sp.run(["git", "push"], check=True)
        print("Commit and Push succesfully done!")
    except sp.CalledProcessError as e:
        print(f"Error during the execution of Git command: {e}")


file_path = "path/del/file"
token = "token"
username = "GabrieleGranzotto"
repo_url = f"https://{username}:{token}@github.com/{username}/gabrielegranzotto.github.io.git"
git_commit(file_path, "commit trammite https e token", repo_url)