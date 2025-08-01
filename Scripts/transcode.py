#!/bin/python3
from sys import argv
from subprocess import call

for file in argv[1:]:
    name = file[: file.rfind(".")].replace("'", "\\'")
    call(
        f"ffmpeg -i '{file}' -c:v dnxhd -profile:v dnxhr_hq "
        f"-pix_fmt yuv422p -c:a alac '{name}_transcoded.mov'",
        shell=True,
    )
