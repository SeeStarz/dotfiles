#!/bin/bash

base=${XDG_DATA_HOME:-${HOME}/.local/share}/nvim/site/pack

{
for package in $(ls "${base}"); do
  for kind in start opt; do
  if [ -d "${base}/${package}/${kind}" ]; then
    for repo in $(ls "${base}/${package}/${kind}"); do
      cd "${base}/${package}/${kind}/${repo}"
      url="$(git remote get-url origin)"
      commit="$(git rev-parse HEAD)"
      path="${package}/${kind}/${repo}"
      jq -n --arg url "$url" --arg commit "$commit" --arg path "$path" \
        '{url:$url, commit:$commit, path:$path}' | cat
    done
  fi
  done
done
} | jq -s > package-lock.json
