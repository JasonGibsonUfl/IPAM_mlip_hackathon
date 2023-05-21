#!/bin/bash

# Function to remove POTCAR files recursively
remove_potcar() {
  local dir="$1"

  # Loop through all files and directories in the current directory
  for entry in "$dir"/*; do
    if [[ -d "$entry" ]]; then
      # If the entry is a directory, call the function recursively
      remove_potcar "$entry"
    elif [[ -f "$entry" && $(basename "$entry") == "POTCAR" ]]; then
      # If the entry is a file and its name is "POTCAR", remove it
      echo "Removing: $entry"
      rm "$entry"
    fi
  done
}

# Call the function with the current directory
remove_potcar "."

echo "POTCAR files removed successfully."

