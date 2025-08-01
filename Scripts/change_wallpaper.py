#!/bin/python3

import argparse
from os import getenv, makedirs, symlink, remove
from os.path import expandvars, isfile
from subprocess import run
from sys import stderr

# Argument parser setup
parser = argparse.ArgumentParser(
    description="Apply a pywal-compatible theme from a JSON colorscheme."
)
parser.add_argument(
    "wallpaper",
    help="wallpaper filename (with extension) used to identify theme name."
)
parser.add_argument(
    "-l", "--light",
    action="store_true",
    help="Use light variant of the colorscheme (default: dark variant)"
)
parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Print the resolved path and command without applying theme"
)

args = parser.parse_args()
if args.wallpaper.count(".") != 1:
    parser.error("Can't work with this format, I don't want to deal with .")

home_directory = expandvars("${HOME}")
wallpaper_path = f"{home_directory}/Pictures/Wallpapers/{args.wallpaper}"


config_directory = getenv("XDG_CONFIG_HOME")
if config_directory is None:
    config_directory = expandvars("${HOME}/.config")

colorscheme_directory = f"{config_directory}/colorschemes"

wallpaper_name = args.wallpaper[:args.wallpaper.find(".")]
if args.light:
    colorscheme_path = f"{colorscheme_directory}/{wallpaper_name}.light.json"
else:
    colorscheme_path = f"{colorscheme_directory}/{wallpaper_name}.dark.json"

print("Wallpaper path:", wallpaper_path)
print("Colorscheme path:", colorscheme_path)

if not isfile(wallpaper_path):
    print("Wallpaper file is not present", file=stderr)
    exit(1)

if not isfile(colorscheme_path):
    print("Colorscheme file is not present", file=stderr)
    exit(1)

if args.dry_run:
    exit(0)

run(["hyprctl", "hyprpaper", "reload", f",{wallpaper_path}"], check=True)
run(["wal", "-f", colorscheme_path], check=True)

hyprpaper_directory = f"{home_directory}/.local/state/hyprpaper"
makedirs(hyprpaper_directory, exist_ok=True)

hyprpaper_active_symlink = f"{hyprpaper_directory}/active_wallpaper"
remove(hyprpaper_active_symlink)
symlink(wallpaper_path, hyprpaper_active_symlink)
