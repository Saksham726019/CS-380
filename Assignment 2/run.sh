#!/bin/sh

if [ "$#" -eq 3 ]; then
    python3 sbp.py "$1" "$2" "$3"
elif [ "$#" -eq 2 ]; then
    python3 sbp.py "$1" "$2"
else
    python3 sbp.py "$1"
fi