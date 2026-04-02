#!/usr/bin/env bash
set -euo pipefail

# One-command helper to wire this repo to GitHub and push branch `work`.
# Usage:
#   bash scripts/setup_github_easy.sh omfardo/omfardo-ajan
# or set env:
#   GITHUB_REPO=omfardo/omfardo-ajan bash scripts/setup_github_easy.sh

REPO_SLUG="${1:-${GITHUB_REPO:-}}"

if [[ -z "$REPO_SLUG" ]]; then
  echo "Usage: bash scripts/setup_github_easy.sh <owner/repo>"
  echo "Example: bash scripts/setup_github_easy.sh omfardo/omfardo-ajan"
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: this script must run inside a git repository"
  exit 1
fi

URL="https://github.com/${REPO_SLUG}.git"

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$URL"
  echo "Updated origin => $URL"
else
  git remote add origin "$URL"
  echo "Added origin => $URL"
fi

CURRENT_BRANCH="$(git branch --show-current)"
if [[ "$CURRENT_BRANCH" != "work" ]]; then
  echo "Switching to branch 'work'..."
  git checkout work
fi

git push -u origin work

echo
echo "Done. Open these links on tablet:"
echo "- Actions: https://github.com/${REPO_SLUG}/actions"
echo "- Issues : https://github.com/${REPO_SLUG}/issues"
