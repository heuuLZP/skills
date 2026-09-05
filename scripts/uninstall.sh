#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS=(ai-reflect arch-coach arch-review commit human-review)

remove_matching_link() {
  local target="$1"
  local expected="$2"
  if [[ -L "$target" && "$(readlink "$target")" == "$expected" ]]; then
    rm "$target"
  fi
}

for skill in "${SKILLS[@]}"; do
  shared="$HOME/.agents/skills/$skill"
  remove_matching_link "$HOME/.codex/skills/$skill" "$shared"
  remove_matching_link "$HOME/.claude/skills/$skill" "$shared"
  remove_matching_link "$shared" "$REPO_ROOT/skills/$skill"
done

echo "Removed repository-managed skill links. User data and backups were preserved."
