#!/bin/bash

function display_help() {
  echo "Usage: ./setup.sh <venv_name> [options]"
  echo "Options:"
  echo "  --help     - Display this message"
  echo "  --d <dir>  - Specify the directory to setup venv in"
}

dir="/app/tiny-link"
name="venv"

if [[ $# -gt 0 ]]; then
  while [[ $# -gt 0 ]]; do
    case $1 in
      --help)
        display_help
        exit 0
        ;;
      --d)
        if [ -n "$2" ]; then
          dir="$2"
          shift
        else
          echo "Error: --d requires an argument."
          exit 1
        fi
        ;;
      *)
        name="$1"
        ;;
    esac
    shift
  done
fi

echo "Creating virtual environment called $name in $dir"

mkdir -p "$dir"
chmod -R 755 "$dir"


python3 -m venv "$dir/$name"

echo "Activating virtual environment"
source "$dir/$name/bin/activate"

if [ -f /app/tiny-link/requirements.txt ]; then
  echo "Installing dependencies from requirements.txt"
  pip install --no-cache-dir -r /app/tiny-link/requirements.txt
else
  echo "No requirements.txt found, skipping dependency installation"
fi

echo "Virtual environment '$name' is ready and activated."
