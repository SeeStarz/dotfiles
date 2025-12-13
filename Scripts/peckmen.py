#!/bin/python3
import pty
import argparse
import json
import re
import traceback
from os import getenv, makedirs, symlink, remove, chdir, listdir, mkdir
from os.path import expanduser, isfile
from subprocess import run
from sys import stderr
import ansicolor

BUILD_DIR = expanduser('~/.cache/yay')
DATA_FILE_PATH = expanduser('~/.peckmen')

def printerr(msg: str, shutdown: bool = True):
    print(ansicolor.red(msg), file=stderr)
    if shutdown:
        exit(1)

def parse_arguments() -> argparse.Namespace:
    import argparse

    parser = argparse.ArgumentParser(
        description='peckmen: minimal AUR update/install wrapper.'
    )

    parser.add_argument(
        'action',
        choices=['update', 'install'],
        help='action to perform: update whitelist or install AUR packages.'
    )

    parser.add_argument(
        'packages',
        nargs='*',
        help=(
            "optional list of explicitly requested large packages for 'update' or "
            "one or more AUR packages to install for 'install'."
        ),
    )

    parser.add_argument(
        '-d',
        action='store_true',
        help='do default actions on interactive prompt whenever possible'
    )

    args: argparse.Namespace = parser.parse_args()

    # Basic sanity check
    if args.action == 'install' and not args.packages:
        parser.error('install requires at least one package name')

    # For update: empty list = normal mode; list = force-build these packages
    # No extra validation needed.
    return args

def install(args: argparse.Namespace):
    for package in args.packages:
        chdir(BUILD_DIR)
        dirs: list[str] = listdir()
        if package not in dirs:
            mkdir(package)
        chdir(package)

def update(args: argparse.Namespace):
    pass

def main():
    args: argparse.Namespace = parse_arguments()

    if args.action == 'install':
        install(args)
    elif args.action == 'update':
        update(args)
    else:
        printerr('Unknown action, also unreachable code, how did we get here?')

if __name__ == '__main__':
    main()
