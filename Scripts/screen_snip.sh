#!/bin/bash
mkdir -p "${HOME}/Pictures/Screenshots"
# Double - made it read from stdin and output stdout idk why
slurp | grim -g - - | wl-copy
wl-paste > $(date "+${HOME}/Pictures/Screenshots/Screenshot_%Y-%m-%d_%H.%M.%S.png")
