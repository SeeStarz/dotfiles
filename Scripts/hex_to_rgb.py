#!/bin/python3
import sys

if len(sys.argv) == 1:
    inp = input()
else:
    inp = sys.argv[1]

inp = inp.strip().replace("#", "")
assert len(inp) == 6 or len(inp) == 8
if len(inp) == 6:
    inp += "ff"
r, g, b, a = inp[:2], inp[2:4], inp[4:6], inp[6:8]
r, g, b, a = int(r, 16), int(g, 16), int(b, 16), int(a, 16)

print(f"({r}, {g}, {b}, {a})")
