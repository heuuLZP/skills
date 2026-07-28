#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STANDALONE=(ai-reflect arch-review commit human-review)
HOTPOT=(hot-requirement-analysis hot-pre-analysis hot-module-split hot-use-cases hot-spec hot-plan hot-plan-review hot-check)

python3 -m json.tool "$REPO_ROOT/.agents/plugins/marketplace.json" >/dev/null
python3 -m json.tool "$REPO_ROOT/.claude-plugin/marketplace.json" >/dev/null
python3 -m json.tool "$REPO_ROOT/plugins/hotpot/.codex-plugin/plugin.json" >/dev/null
python3 -m json.tool "$REPO_ROOT/plugins/hotpot/.claude-plugin/plugin.json" >/dev/null

for skill in "${STANDALONE[@]}"; do
  test -f "$REPO_ROOT/skills/$skill/SKILL.md"
  test -f "$REPO_ROOT/skills/$skill/agents/openai.yaml"
  ruby -ryaml -e '
    text = File.read(ARGV[0])
    abort "missing frontmatter: #{ARGV[0]}" unless text.start_with?("---\n")
    frontmatter = text.split("---", 3)[1]
    data = YAML.safe_load(frontmatter)
    abort "invalid name: #{ARGV[0]}" unless data["name"] == ARGV[1]
    abort "missing description: #{ARGV[0]}" unless data["description"].is_a?(String) && !data["description"].empty?
  ' "$REPO_ROOT/skills/$skill/SKILL.md" "$skill"
  ruby -ryaml -e 'YAML.safe_load(File.read(ARGV[0]))' "$REPO_ROOT/skills/$skill/agents/openai.yaml"
done
for skill in "${HOTPOT[@]}"; do
  test -f "$REPO_ROOT/plugins/hotpot/skills/$skill/SKILL.md"
  ruby -ryaml -e '
    text = File.read(ARGV[0])
    abort "missing frontmatter: #{ARGV[0]}" unless text.start_with?("---\n")
    data = YAML.safe_load(text.split("---", 3)[1])
    abort "invalid name: #{ARGV[0]}" unless data["name"] == ARGV[1]
    abort "missing description: #{ARGV[0]}" unless data["description"].is_a?(String) && !data["description"].empty?
  ' "$REPO_ROOT/plugins/hotpot/skills/$skill/SKILL.md" "$skill"
done
for reference in artifact-templates.md output-style-guide.md review-checklist.md shared-conventions.md; do
  test -f "$REPO_ROOT/plugins/hotpot/references/$reference"
done

python3 -m unittest discover -s "$REPO_ROOT/skills/ai-reflect/tests" -p 'test_*.py'
python3 -m unittest discover -s "$REPO_ROOT/plugins/hotpot/tests" -p 'test_*.py'

if rg -n '/Users/night|mingyuanyun|myscrm' \
  "$REPO_ROOT/skills" "$REPO_ROOT/plugins"; then
  echo "Found local absolute paths or company-specific content." >&2
  exit 1
fi

echo "Local validation passed."
