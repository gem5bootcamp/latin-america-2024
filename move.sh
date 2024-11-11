#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <old_prefix> <new_prefix>"
    exit 1
fi

old_prefix="$1"
new_prefix="$2"

# Rename files
for file in "${old_prefix}"-*; do
    if [[ -e "$file" ]]; then
        new_file="${file/$old_prefix/$new_prefix}"
        git mv "$file" "$new_file"
    fi
done

# Rename directories
for dir in "${old_prefix}"-*; do
    if [[ -d "$dir" ]]; then
        new_dir="${dir/$old_prefix/$new_prefix}"
        git mv "$dir" "$new_dir"
    fi
done

echo "Renaming from $old_prefix to $new_prefix complete!"
