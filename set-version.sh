#!/usr/bin/env bash

set -euo pipefail

test $# -eq 1 || { echo "Usage: $0 <version>"; exit 1; }

git diff --exit-code > /dev/null || { echo "Usage: Git working directory must be clean"; exit 1; }

if test "$(git rev-parse --abbrev-ref HEAD)" != "master"; then
  echo "Error: Must be working on master branch"
  exit 8
fi

# e.g. 5.0.5
NEW_VERSION="$1"

[[ $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] ||  { echo "Error: version must be x.y.z"; exit 2; }

poetry version "$NEW_VERSION" > /dev/null || exit 3

if git diff --exit-code > /dev/null; then
  echo "Usage: Nothing to commit"
  exit 11
fi

VERSION_TAG="v$NEW_VERSION"

git add pyproject.toml
git commit -m "------------ Version $NEW_VERSION" || exit 4

git pull --tags
git tag "$VERSION_TAG" || exit 9

echo
echo "Updated to version $NEW_VERSION; commited but did not push; use ..."
echo "- git push origin master"
echo "- git push --tags"
echo "- (merge master into dev)"%