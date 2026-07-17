#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SHARED_ROOT="${HOME}/.agents/skills"
BACKUP_ROOT="${HOME}/.agents/backups/skills-$(date +%Y%m%d-%H%M%S)"
SKILLS=(ai-reflect arch-review commit human-review)
BACKUP_CREATED=0

backup_path() {
  local path="$1"
  local label="$2"
  if [[ -e "$path" || -L "$path" ]]; then
    if [[ "$BACKUP_CREATED" -eq 0 ]]; then
      mkdir -p "$BACKUP_ROOT"
      BACKUP_CREATED=1
    fi
    mkdir -p "$(dirname "$BACKUP_ROOT/$label")"
    mv "$path" "$BACKUP_ROOT/$label"
  fi
}

ensure_link() {
  local source="$1"
  local target="$2"
  local label="$3"
  mkdir -p "$(dirname "$target")"
  if [[ -L "$target" && "$(readlink "$target")" == "$source" ]]; then
    return
  fi
  backup_path "$target" "$label"
  ln -s "$source" "$target"
}

mkdir -p "$SHARED_ROOT"
for skill in "${SKILLS[@]}"; do
  source_path="$REPO_ROOT/skills/$skill"
  [[ -f "$source_path/SKILL.md" ]] || { echo "Missing $source_path/SKILL.md" >&2; exit 1; }

  ensure_link "$source_path" "$SHARED_ROOT/$skill" "agents/$skill"
  ensure_link "$SHARED_ROOT/$skill" "$HOME/.codex/skills/$skill" "codex/$skill"
  ensure_link "$SHARED_ROOT/$skill" "$HOME/.claude/skills/$skill" "claude/$skill"
done

echo "Installed ${#SKILLS[@]} skills for Codex and Claude Code."
if [[ "$BACKUP_CREATED" -eq 1 ]]; then
  echo "Backups: $BACKUP_ROOT"
fi
