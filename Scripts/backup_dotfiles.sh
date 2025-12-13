#!/bin/bash
set -e
cd $HOME
# Effectively an alias
function dotfiles() {
  # Means the git store is on .dotfiles, but our working directory is $HOME
  git --git-dir=$HOME/.dotfiles --work-tree=$HOME "$@"
}
# Check if there is any change, whether it is untracked file or changes
if [ -n "$(dotfiles status --porcelain)" ]; then
  # Propagate changes to dev branch
  dotfiles checkout dev
  dotfiles add :/
  dotfiles commit -m "autosave configs"
  dotfiles push
fi
