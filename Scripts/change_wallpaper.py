#!/bin/python3

import argparse
from os import getenv, makedirs, symlink, remove
from os.path import expanduser, isfile
from subprocess import run
from sys import stderr

class Dirs:
    wallpaper: str = ""
    hyprpaper_state: str = ""
    user_colorscheme: str = ""
    generated_colorscheme: str = ""
    betterdiscord_theme: str = ""

    @staticmethod
    def setup():
        cache_dir = getenv("XDG_CACHE_HOME", expanduser("~/.cache"))
        config_dir = getenv("XDG_CONFIG_HOME", expanduser("~/.config"))
        state_dir = getenv("XDG_STATE_HOME", expanduser("~/.local/state"))

        Dirs.wallpaper = expanduser("~/Pictures/Wallpapers")
        Dirs.hyprpaper_state = f"{state_dir}/hyprpaper"
        Dirs.user_colorscheme = f"{config_dir}/colorschemes"
        Dirs.generated_colorscheme = f"{cache_dir}/wal"
        Dirs.betterdiscord_theme = f"{config_dir}/BetterDiscord/themes"

    @staticmethod
    def check():
        assert Dirs.wallpaper != ""
        assert Dirs.hyprpaper_state != ""
        assert Dirs.user_colorscheme != ""
        assert Dirs.generated_colorscheme != ""
        assert Dirs.betterdiscord_theme != ""

def parse_arguments() -> argparse.Namespace:
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

    return args

def remove_extension(path: str) -> str:
    return path[:path.find(".")]

def apply_wal(args: argparse.Namespace):
    if args.light:
        colorscheme_path = f"{Dirs.user_colorscheme}/{remove_extension(args.wallpaper)}.light.json"
    else:
        colorscheme_path = f"{Dirs.user_colorscheme}/{remove_extension(args.wallpaper)}.dark.json"

    if not isfile(colorscheme_path):
        print(f'User colorscheme at: "{colorscheme_path}" not found', file=stderr)
        return

    run(["wal", "-f", colorscheme_path], check=True)


def apply_hyprpaper(args: argparse.Namespace):
    makedirs(Dirs.hyprpaper_state, exist_ok=True)
    state_file = f"{Dirs.hyprpaper_state}/active_wallpaper"

    if isfile(state_file):
        remove(state_file)

    symlink(f"{Dirs.wallpaper}/{args.wallpaper}", state_file)
    run(["hyprctl", "hyprpaper", "reload", f",{state_file}"], check=True)


def main():
    args: argparse.Namespace = parse_arguments()

    Dirs.setup()
    apply_wal(args)
    apply_hyprpaper(args)

if __name__ == "__main__":
    main()
