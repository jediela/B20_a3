#!/bin/bash

for i in {1..10}; do
    filename="userstory${i}.txt"

    if [ -e "$filename" ]; then
        echo "Reading from file: $filename"
        cat "$filename"
        echo -e "\n-----------------------------"
    else
        echo "File '$filename' not found."
    fi
done
