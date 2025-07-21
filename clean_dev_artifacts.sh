#!/bin/bash

# Use this script to clean up dev artifacts in any directory tree.
# This can run from root, or can be scoped to a specific directory
# Specify a directory as the first argument: ./clean_dev_artifacts.sh ~/Documents
# Current directory: ./clean_dev_artifacts.sh

# As always, make executable by running: chmod +x clean_dev_artifacts.sh

# Set the root path to start scanning (defaults to current directory)
ROOT="${1:-$PWD}"

echo "Scanning and cleaning dev dependencies under: $ROOT"
sleep 1

# Patterns to clean — add/remove as needed
TARGETS=(
  "node_modules"
  "build"
  "dist"
  ".dart_tool"
  ".next"
  ".turbo"
  ".cache"
  "Pods"
  "ios/Pods"
  "android/.gradle"
  ".flutter-plugins"
  ".flutter-plugins-dependencies"
  "__pycache__"
)

for target in "${TARGETS[@]}"; do
  echo "Removing: $target"
  find "$ROOT" -type d -name "$target" -prune -exec rm -rf {} +
done

echo "Cleanup complete."