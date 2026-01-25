sudo -v
set -e

skip_build=0
skip_asdeps=0
for arg in $@; do
  if [ $arg = "--skip-build" ]; then
    skip_build=1
  fi
  if [ $arg = "--skip-asdeps" ]; then
    skip_asdeps=1
  fi
done

for metapkg in seestarz-*; do
  if ! [ -d "$metapkg" ]; then
    continue
  fi

  cd "$metapkg"

  if [ $skip_build -eq 0 ]; then
    makepkg -sf
    sudo pacman -U seestarz-*.pkg.tar.zst
  fi

  if [ $skip_asdeps -eq 0 ]; then
    sudo pacman -D --asdeps $(pactree -l -d 1 "$metapkg" | tail -n +2)
  fi

  cd ..
done
