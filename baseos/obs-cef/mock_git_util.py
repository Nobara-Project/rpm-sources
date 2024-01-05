# Mock git_util module to make CEF work with non-git checkouts
import os, subprocess

def ver_info(path):
    info = {}
    for line in open(os.path.join(path, '.git-version')):
        key, val = line.strip().split("=")
        info[key] = val
    return info

def is_checkout(path):
    return os.path.exists(os.path.join(path, '.git-version'))

def is_ancestor(path='.', commit1='HEAD', commit2='master'):
    return True

def get_hash(path='.', branch='HEAD'):
    return ver_info(path)["COMMIT_HASH"]

def get_branch_name(path='.', branch='HEAD'):
    return ver_info(path)["BRANCH_NAME"]

def get_commit_number(path='.', branch='HEAD'):
    return int(ver_info(path)["COMMIT_NUMBER"])

def get_changed_files(path, hash):
    return []

def get_branch_hashes(path='.', branch='HEAD', ref='origin/master'):
    return []

def git_apply_patch_file(patch_path, patch_dir):
    try:
        subprocess.run(["patch", "-p0", "--ignore-whitespace",
                        "-N", "-i", patch_path], cwd=patch_dir, check=True)
    except subprocess.CalledProcessError:
        return "fail"
    return "apply"

def get_url(path):
    return ver_info(path)["URL"]

