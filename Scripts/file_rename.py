#!/bin/python3
import argparse
import os

parser = argparse.ArgumentParser(
    prog="file rename",
    description="rename file according to format given in format file. uses python str.format",
)
parser.add_argument("format_file", help="describes how to rename the file")
parser.add_argument("file", help="file to rename according to format_file")
parser.add_argument(
    "args", help="passed arguments to the formatter", nargs=argparse.REMAINDER
)

namespace = parser.parse_args()
with open(namespace.format_file, "r") as f:
    format = f.read().strip()
new_name = format.format(*namespace.args)
os.rename(namespace.file, new_name)
