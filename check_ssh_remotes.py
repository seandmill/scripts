#! /usr/bin/env python3


"""
Check if the SSH remotes are using the correct identity file.

Usage:
    python check_ssh_remotes.py -- or python3 check_ssh_remotes.py 

This script will check all git repositories in the home directory and print the
remote URLs and the expected identity file.

Run from anywhere! It will find all git repos in the home directory and check remotes.

"""
import os
import re
from pathlib import Path

def parse_ssh_config(config_path):
    """Parse ~/.ssh/config and return host -> identity mapping"""
    alias_map = {}
    current_host = None

    if not config_path.exists():
        return alias_map

    with open(config_path) as f:
        for line in f:
            line = line.strip()
            if line.lower().startswith("host "):
                current_host = line.split()[1]
            elif "identityfile" in line.lower() and current_host:
                identity = line.split(None, 1)[1].strip()
                alias_map[current_host] = identity
    return alias_map

def find_git_repos(base_path, max_depth=3):
    """Recursively find all folders with a .git directory"""
    git_repos = []
    for root, dirs, files in os.walk(base_path):
        if '.git' in dirs:
            git_repos.append(Path(root))
        # prevent going too deep
        if Path(root).relative_to(base_path).parts.__len__() >= max_depth:
            dirs[:] = []
    return git_repos

def check_remotes(repo_path):
    """Return remote URLs for a git repo"""
    try:
        output = os.popen(f'git -C "{repo_path}" remote -v').read()
        remotes = re.findall(r"(\w+)\s+(git@[^ ]+)", output)
        return remotes
    except Exception:
        return []

def main():
    base_dir = Path.home()
    ssh_config_path = Path.home() / ".ssh" / "config"
    ssh_aliases = parse_ssh_config(ssh_config_path)

    repos = find_git_repos(base_dir)
    if not repos:
        print("No Git repositories found.")
        return

    print("SSH Identity Mapping Check\n")
    for repo in repos:
        remotes = check_remotes(repo)
        for name, url in remotes:
            match = re.match(r"git@([^:]+):", url)
            if match:
                ssh_host = match.group(1)
                expected_identity = ssh_aliases.get(ssh_host, "UNKNOWN")
                print(f"Repo: {repo}")
                print(f"  Remote ({name}): {url}")
                print(f"  SSH Host: {ssh_host}")
                print(f"  Identity File: {expected_identity}")
                print()
                
if __name__ == "__main__":
    main()

