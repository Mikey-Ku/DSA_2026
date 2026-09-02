#!/usr/bin/env bash
#
# Verify that the Kotlin port and the original Python agree.
#
# Both implementations print the next-word map they build for every line of
# reference/corpus.txt in an identical normalised format. This script runs each
# of them and diffs the results, so a behavioural difference shows up as a diff
# rather than as a test nobody thought to write.
#
# Requires python3 on PATH. Run it from anywhere:
#
#     ./reference/crosscheck.sh
#
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT

echo "Running the original Python..."
(cd "$project_dir/reference/python" && python3 crosscheck.py ../corpus.txt) \
    > "$work_dir/python.txt"

echo "Running the Kotlin port..."
"$project_dir/gradlew" --project-dir "$project_dir" --quiet crossCheck \
    > "$work_dir/kotlin.txt"

if diff -u "$work_dir/python.txt" "$work_dir/kotlin.txt"; then
    echo
    echo "Match: $(wc -l < "$work_dir/python.txt" | tr -d ' ') transitions agree."
else
    echo
    echo "MISMATCH: the port and the original disagree." >&2
    exit 1
fi
