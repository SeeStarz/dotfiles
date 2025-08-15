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

for metapkg in $(ls); do
  if ! [ -d "$metapkg" ]; then
    continue
  fi

  cd "$metapkg"

  if [ $skip_build -eq 0 ]; then
    makepkg -sif
  fi

  if [ $skip_asdeps -eq 0 ]; then
    for deps in $(pactree -l -d 1 "$metapkg"); do
      sudo pacman -D --asdeps "$deps"
    done
  fi

  cd ..
done
