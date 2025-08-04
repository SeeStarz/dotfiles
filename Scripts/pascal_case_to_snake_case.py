#!/bin/python3

import re
import argparse
import os
from sys import stderr

def pascal_to_snake(name: str) -> str:
    # Insert underscore before uppercase letters that follow lowercase letters or digits
    s1 = re.sub(r'(?<=[a-z0-9])([A-Z])', r'_\1', name)
    # Insert underscore before uppercase letters that are followed by lowercase letters (to handle boundaries)
    s2 = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s1)
    return s2.lower()

def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rename files and directories from pascal case to snake case. Handles acronyms properly.")

    parser.add_argument("names", help="files, directories, or symlinks to rename", nargs="+")
    parser.add_argument("--dry-run", action="store_true", help="only show action that will be taken on non dry run")
    parser.add_argument("-f", "--force", action="store_true", help="force rename even if a file or symlink already exists")

    return parser.parse_args()

def main():
    args: argparse.Namespace = parse()

    for name in args.names:
        src_path = os.path.normpath(name)

        if not os.path.lexists(src_path):
            print(f'Source "{src_path}" does not exist', file=stderr)
            continue

        print(f'Working with source "{src_path}"')

        target_path = pascal_to_snake(src_path)
        if src_path == target_path:
            print("Source already in snake case, skipping.")
            continue

        print(f'Source "{src_path}" has target "{target_path}"')

        # If a directory
        if os.path.isdir(target_path) and not os.path.islink(target_path):
            print(f'Target "{target_path}" is a directory, cannot overwrite', file=stderr)
            continue

        # If a file or symlink but not forced
        if os.path.lexists(target_path) and not args.force:
            print(f'Target "{target_path}" exists, will not overwrite (use -f to force)', file=stderr)
            continue

        if args.dry_run:
            print(f'Source "{src_path}" will be renamed to "{target_path}" outside of dry run')
        else:
            print(f'Renaming "{src_path}" to "{target_path}"')
            os.rename(src_path, target_path)

if __name__ == "__main__":
    main()
