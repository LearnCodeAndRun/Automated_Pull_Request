from dotenv import load_dotenv
import os
import subprocess
import requests
import time

# 🔹 CONFIGURATION
load_dotenv()
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
LOCAL_PARENT_DIR = os.getenv("LOCAL_PARENT_DIR", r"C:\Users\User\Desktop\GITHUB_REPOS")
if not GITHUB_USERNAME or not GITHUB_TOKEN:
    print("Please set GITHUB_USERNAME and GITHUB_TOKEN in the .env file.")
    exit(1)

# -----------------------------

def get_github_repos():
    url = f"https://api.github.com/user/repos"
    repos = []
    page = 1

    while True:
        response = requests.get(
            url,
            auth=(GITHUB_USERNAME, GITHUB_TOKEN),
            params={"per_page": 100, "page": page}
        )
        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code} - {response.text}")
            break

        data = response.json()

        if not data:
            break

        for repo in data:
            repos.append({
                "name": repo["name"],
                "clone_url": repo["clone_url"]
            })

        page += 1

    return repos


def clone_repo(clone_url, repo_name):
    print(f"📥 Cloning new repo: {repo_name}")
    subprocess.run(["git", "clone", clone_url], cwd=LOCAL_PARENT_DIR)


def pull_repo(repo_path):
    print(f"🔄 Pulling updates in {repo_path}")
    subprocess.run(["git", "pull"], cwd=repo_path)


def sync_repositories():
    github_repos = get_github_repos()

    if not os.path.exists(LOCAL_PARENT_DIR):
        os.makedirs(LOCAL_PARENT_DIR)

    local_repos = os.listdir(LOCAL_PARENT_DIR)

    for repo in github_repos:
        repo_name = repo["name"]
        repo_path = os.path.join(LOCAL_PARENT_DIR, repo_name)

        if repo_name not in local_repos:
            clone_repo(repo["clone_url"], repo_name)
        else:
            if os.path.isdir(os.path.join(repo_path, ".git")):
                pull_repo(repo_path)


if __name__ == "__main__":
    while True:
      sync_repositories()
      time.sleep(300)
