#!/bin/bash

# Setup script. Run me to install.

[[ -z "$PREFIX" ]] && PREFIX="/usr/local"

for ARG; do
    if [[ "$ARG" == --prefix=* ]]; then
        PREFIX="$ARG"
    fi
done

R="$(dirname $0)"

install -Cv -o root -g wheel -m 0755 "$R/clang-fake-gcc" "$PREFIX/bin"
