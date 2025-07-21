#!/bin/bash

set -e

# Use this script to reclaim space on your Mac by removing local iMessage storage.
# Ensure you sign out of iMessage before running this script.

# Config: Set to 1 to create a backup
BACKUP_MESSAGES=0

# Paths
MSG_DIR="$HOME/Library/Messages"
CACHE_DIR="$HOME/Library/Caches/com.apple.iChat"
CONTAINER_DIR="$HOME/Library/Containers/com.apple.iChat"
GROUP_CONTAINER_DIR="$HOME/Library/Group Containers/group.com.apple.messages"

timestamp=$(date +%Y%m%d_%H%M%S)
backup_dir="$HOME/Archive/MessagesBackup_$timestamp"

# Function to print human-readable disk usage
get_disk_usage() {
  du -sh "$HOME/Library/Messages" 2>/dev/null | cut -f1
}

# Check if user is signed into iMessage
signed_in=$(defaults read ~/Library/Preferences/com.apple.iChat iMessageLoginHint 2>/dev/null || echo "none")

echo "iMessage Storage Cleanup Script"
echo "----------------------------------"
echo "Signed in as: $signed_in"
echo "Messages folder size: $(get_disk_usage)"
echo

read -p "Are you sure you want to remove all local iMessage storage from this Mac? (y/N) " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
  echo "Aborted."
  exit 1
fi

# Optional backup
if [[ "$BACKUP_MESSAGES" -eq 1 && -d "$MSG_DIR" ]]; then
  echo "Creating backup at $backup_dir"
  mkdir -p "$backup_dir"
  cp -a "$MSG_DIR"/* "$backup_dir" || echo "Warning: some files may not have copied."
fi

# Begin cleanup
echo "Deleting Messages folder..."
rm -rf "$MSG_DIR"

echo "Deleting Messages cache..."
rm -rf "$CACHE_DIR"

echo "Deleting Messages container..."
rm -rf "$CONTAINER_DIR"

echo "Deleting Messages group container..."
rm -rf "$GROUP_CONTAINER_DIR"

# Final state
echo
echo "Cleanup complete."
echo "Messages folder now: $(get_disk_usage)"
