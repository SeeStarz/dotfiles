#!/bin/python3
from sys import argv
from subprocess import call

assert len(argv) > 2

call(["mkdir", ".temp", "-p"])
filenames = []
for item in argv[2:]:
    filenames.append(f".temp/{item}.pdf")
    call(["magick", "convert", item, filenames[-1]])

call(["pdfunite"] + [filename for filename in filenames] + [argv[1]])
call(["rm"] + [filename for filename in filenames])
call(["rmdir", ".temp"])
