#!/usr/bin/env bash
set -euo pipefail

BUMP=""
NO_TAG=false
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

for arg in "$@"; do
  case "$arg" in
    major|minor|patch) BUMP="$arg" ;;
    --no-tag) NO_TAG=true ;;
    *) echo "Unknown argument: $arg" >&2; exit 1 ;;
  esac
done

if [[ -z "$BUMP" ]]; then
  echo "Usage: $0 major|minor|patch [--no-tag]" >&2
  exit 1
fi

# Read current version from schema
CURRENT=$(grep 'version:' "$REPO_ROOT/radical.schema.yaml" | head -1 | sed 's/.*version: "\([^"]*\)".*/\1/')
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

case "$BUMP" in
  major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
  minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
  patch) PATCH=$((PATCH + 1)) ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
DATE=$(date +'%Y.%m.%d')

echo "Bumping $CURRENT -> $NEW_VERSION"

# Update version in schema files (macOS sed -i '' for in-place edit)
sed -i '' "s/version: \"[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\"/version: \"$NEW_VERSION\"/" \
  "$REPO_ROOT/radical.schema.yaml" \
  "$REPO_ROOT/radical_pinyin.schema.yaml"

# Record version history in dict-head-note.yaml
echo "# v$NEW_VERSION -> $DATE" >> "$REPO_ROOT/src/dict/dict-head-note.yaml"

# Build
cd "$REPO_ROOT"
make -C src

# Commit
cd "$REPO_ROOT"
git add --all
git commit -m "chore: bump version to $NEW_VERSION"

# Tag
if [[ "$NO_TAG" == false ]]; then
  git tag "$NEW_VERSION"
  echo "Tagged: $NEW_VERSION"
fi

echo "Done: $NEW_VERSION"
