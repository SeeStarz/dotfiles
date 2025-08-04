#!/bin/python3

import os
from os import listdir
from os.path import isfile, join, basename, isdir, normpath, expanduser
from sys import stderr

def color4(message: str) -> str:
    return "\033[34m" + message + "\033[0m"

def color2(message: str) -> str:
    return "\033[32m" + message + "\033[0m"

def color1(message: str) -> str:
    return "\033[31m" + message + "\033[0m"

def check_is_last_dir(path: str) -> bool:
    if isfile(join(path, "last_dir")):
        return True
    return False

def tree(root: str, prefix: str="", err: str="") -> str:
    last_dir = True if check_is_last_dir(root) else False

    try:
        entries = [e for e in sorted(os.listdir(root)) if e != "last_dir"]
    except PermissionError:
        return err + f'\n"{root}": permission error'

    for idx, name in enumerate(entries):
        path = os.path.join(root, name)
        last = idx == len(entries) - 1
        new_prefix = prefix + ("└── " if last else "├── ")
        child_prefix = prefix + ("    " if last else "│   ")

        if isdir(path):
            if not last_dir:
                print(f"{new_prefix}{color4(name)}")
            else:
                print(f"{new_prefix}{color2(name)}")

            if not last_dir:
                err += tree(path, prefix=child_prefix, err=err)
        else:
            print(f"{new_prefix}{name}")
    return err

def main():
    try:
        import sys
        root = sys.argv[1] if len(sys.argv) > 1 else expanduser("~/Repos")
        normalized = normpath(root)

        if not isdir(normalized):
            print(normalized)
            return

        print(color4(normalized))
        err = tree(normalized)
        print(color1(err), file=stderr)
    except (BrokenPipeError, KeyboardInterrupt):
        return

if __name__ == "__main__":
    main()
