#!/bin/sh
name=$(basename "$1")
ln -fs "$(pwd)/$1" "/usr/local/bin/$name"
