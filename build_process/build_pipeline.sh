#!/bin/bash
# Build script for CI/CD pipeline
# This script is designed to run after integration tests succeed

set -e  # Exit on any error

echo "IdleonWeb Standalone Build Pipeline"
echo "==================================="

# Get the current platform
PLATFORM=$(python3 -c "import platform; print(platform.system().lower())")
echo "Detected platform: $PLATFORM"

# Install build dependencies
echo "Installing build dependencies..."
pip install -r build_process/build-requirements.txt

# Get version from VERSION file if it exists
VERSION=""
if [ -f "VERSION" ]; then
    VERSION=$(cat VERSION)
    echo "Version: $VERSION"
fi

# Run the build
echo "Starting build process..."
if [ -n "$VERSION" ]; then
    python3 build_process/build_standalone.py --platform current --version "$VERSION"
else
    python3 build_process/build_standalone.py --platform current
fi

# Check if build was successful
if [ -d "build/dist" ]; then
    echo "Build successful!"
    echo "Generated files:"
    find build/dist -type f -exec ls -lh {} \;
    
    # Create release artifacts directory
    mkdir -p release-artifacts
    
    # Copy executables to release artifacts
    if [ "$PLATFORM" = "windows" ]; then
        cp build/dist/windows/IdleonWeb.exe release-artifacts/IdleonWeb-windows.exe
    elif [ "$PLATFORM" = "linux" ]; then
        cp build/dist/linux/IdleonWeb release-artifacts/IdleonWeb-linux
        chmod +x release-artifacts/IdleonWeb-linux
    elif [ "$PLATFORM" = "darwin" ]; then
        cp build/dist/macos/IdleonWeb release-artifacts/IdleonWeb-macos
        chmod +x release-artifacts/IdleonWeb-macos
    fi
    
    echo "Release artifacts created in release-artifacts/"
    ls -la release-artifacts/
else
    echo "Build failed - no output directory found"
    exit 1
fi

# Determine last real commit and full release notes since previous version tag
echo "Selecting last real commit and generating release notes..."

# Resolve repository base URL for linking commits
ORIGIN_URL=$(git config --get remote.origin.url)
BASE_URL=""
if [[ "$ORIGIN_URL" =~ ^git@github.com:(.*)\.git$ ]]; then
  BASE_URL="https://github.com/${BASH_REMATCH[1]}"
elif [[ "$ORIGIN_URL" =~ ^https?://github.com/(.*)\.git$ ]]; then
  BASE_URL="https://github.com/${BASH_REMATCH[1]}"
elif [[ "$ORIGIN_URL" =~ ^https?://github.com/.*$ ]]; then
  BASE_URL=${ORIGIN_URL%%.git}
fi

# Find the most recent version bump commit (the last release)
LAST_VERSION_BUMP=$(git log --no-merges --grep='bump version' -i --pretty=format:'%H' origin/main | head -n 1)

# Set range from last version bump to current HEAD (commits for the upcoming release)
RANGE_SPEC=""
if [ -n "$LAST_VERSION_BUMP" ]; then
  RANGE_SPEC="$LAST_VERSION_BUMP..origin/main"
else
  # Fallback if no version bumps found
  RANGE_SPEC="origin/main~50..origin/main"
fi

LAST_REAL_COMMIT=$(git log --no-merges -n 50 --grep='bump version' -i --invert-grep --pretty=format:'%H' origin/main | head -n 1)
LAST_REAL_SUBJECT=""
LAST_REAL_BODY=""
if [ -n "$LAST_REAL_COMMIT" ]; then
  LAST_REAL_SUBJECT=$(git log -n 1 --format='%s' "$LAST_REAL_COMMIT")
  LAST_REAL_BODY=$(git log -n 1 --format='%b' "$LAST_REAL_COMMIT")
fi

# Get current version tag for release notes
CURRENT_TAG=$(git describe --tags --abbrev=0 origin/main 2>/dev/null || cat VERSION 2>/dev/null || echo "unreleased")

# Build consolidated release notes including all real commits since last version bump
mkdir -p release-artifacts
{
  if [ -n "$CURRENT_TAG" ]; then
    echo "Release $CURRENT_TAG"
    echo
  fi
  if [ -n "$LAST_REAL_SUBJECT" ]; then
    echo "$LAST_REAL_SUBJECT"
    if [ -n "$LAST_REAL_BODY" ]; then
      echo
      echo "$LAST_REAL_BODY"
    fi
    echo
  fi
  echo "Changes since last version bump:"
  echo
  # List commits since last version bump, excluding merges and bumps
  git --no-pager log $RANGE_SPEC \
    --no-merges \
    --grep='bump version' -i --invert-grep \
    --pretty=format:'- %h %s' | while read -r line; do
      SHA=$(echo "$line" | awk '{print $2}')
      SUBJECT=$(echo "$line" | cut -d' ' -f3-)
      if [ -n "$BASE_URL" ] && [ -n "$SHA" ]; then
        echo "- [$SHA]($BASE_URL/commit/$SHA) $SUBJECT"
      else
        echo "$line"
      fi
    done
} > release-artifacts/RELEASE_NOTES.md

# Expose values to GitHub Actions, if available
if [ -n "$GITHUB_OUTPUT" ]; then
  if [ -n "$LAST_REAL_COMMIT" ]; then
    echo "last_real_commit_sha=$LAST_REAL_COMMIT" >> "$GITHUB_OUTPUT"
    printf "last_real_commit_subject<<EOF\n%s\nEOF\n" "$LAST_REAL_SUBJECT" >> "$GITHUB_OUTPUT"
    printf "last_real_commit_body<<EOF\n%s\nEOF\n" "$LAST_REAL_BODY" >> "$GITHUB_OUTPUT"
  fi
  printf "release_notes<<EOF\n%s\nEOF\n" "$(cat release-artifacts/RELEASE_NOTES.md)" >> "$GITHUB_OUTPUT"
fi

echo "Build pipeline completed successfully!"
