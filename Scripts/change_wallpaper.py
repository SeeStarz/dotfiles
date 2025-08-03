#!/bin/python3

import argparse
import json
import re
from base64 import b64encode
from PIL import Image
from io import BytesIO
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

    print(f'Using user colorscheme at: "{colorscheme_path}"')

    cmd = ["wal", "-f", colorscheme_path] 
    if not args.dry_run:
        print(f"Running: {cmd}")
        run(cmd, check=True)
    else:
        print(f"Will run if not on dry run: {cmd}")


def apply_hyprpaper(args: argparse.Namespace):
    makedirs(Dirs.hyprpaper_state, exist_ok=True)
    state_path = f"{Dirs.hyprpaper_state}/active_wallpaper"
    wallpaper_path = f"{Dirs.wallpaper}/{args.wallpaper}"

    if not isfile(wallpaper_path):
        print(f'Wallpaper at: "{wallpaper_path}" not found', file=stderr)
    print(f'Using wallpaper at: "{wallpaper_path}"')

    if isfile(state_path) and not args.dry_run:
        print(f'Removing active wallpaper symlink at: "{state_path}"')
        remove(state_path)
    elif isfile(state_path) and args.dry_run:
        print(f'Will remove active wallpaper symlink at: "{state_path}" if not on dry run')

    if not args.dry_run:
        print(f'Symlinking "{state_path}" to "{wallpaper_path}"')
        symlink(wallpaper_path, state_path)
    else:
        print(f'Will symlink "{state_path}" to "{wallpaper_path}" if not on dry run')

    cmd = ["hyprctl", "hyprpaper", "reload", f",{state_path}"]
    if not args.dry_run:
        print(f"Running: {cmd}")
        run(cmd, check=True)
    else:
        print(f"Will run if not on dry run: {cmd}")

def apply_betterdiscord(args: argparse.Namespace):
    generated_theme_json_path = f"{Dirs.generated_colorscheme}/colors.json"
    template_path = f"{Dirs.betterdiscord_theme}/Scripted.theme.template"
    theme_path = f"{Dirs.betterdiscord_theme}/Scripted.theme.css"

    if not isfile(generated_theme_json_path):
        print(f'Generated theme at: "{generated_theme_json_path}" not found', file=stderr)
        return
    print(f'Using generated theme at: "{generated_theme_json_path}"')

    with open(generated_theme_json_path, "r") as file:
        background_color_str = json.loads(file.read())["special"]["background"].removeprefix("#")

    assert re.fullmatch("[0-9a-fA-F]{6}", background_color_str), f"Something is wrong with the generated json file, got: {background_color_str}"
    r, g, b = (int(background_color_str[i:i+2], 16) for i in range(0, 6, 2))
    print(f"Using colors r:{r} g:{g} b:{b}")

    img = Image.new("RGB", (1, 1), (r, g, b))
    buf = BytesIO()
    img.save(buf, format="png", optimize=True)
    base64_img = b64encode(buf.getvalue()).decode("ASCII", errors="strict")

    colors = f'''
:root {{
  --background: url("data:image/png;base64,{base64_img}");
  --accentcolor: {r}, {g}, {b};
}}
'''

    if not isfile(template_path):
        print(f'BetterDiscord template at: "{template_path}" not found', file=stderr)
        return
    print(f'Using BetterDiscord template at: "{template_path}"')

    with open(template_path, "r") as file:
        contents = file.read()

    if args.dry_run:
        print(f'Will write to: "{theme_path}" if not in dry run')
        return
    print(f'Writing to: "{theme_path}"')
    with open(theme_path, "w") as file:
        file.write(contents + colors)


def main():
    args: argparse.Namespace = parse_arguments()

    Dirs.setup()
    apply_wal(args)
    apply_hyprpaper(args)
    apply_betterdiscord(args)

if __name__ == "__main__":
    main()
