#!/usr/bin/env bash
# Report what the next commit would add. Fails if any staged file is over the per-file
# limit or if the staged total is over the payload limit.
# Usage: tools/check_payload.sh [max_file_mb=5] [max_total_mb=50]
set -euo pipefail
max_file=$(( ${1:-5} * 1024 * 1024 ))
max_total=$(( ${2:-50} * 1024 * 1024 ))
total=0; bad=0
while IFS= read -r -d '' f; do
  [ -f "$f" ] || continue
  s=$(stat -c %s "$f"); total=$(( total + s ))
  if [ "$s" -gt "$max_file" ]; then echo "TOO BIG  $(( s / 1024 / 1024 )) MB  $f"; bad=1; fi
done < <(git diff --cached --name-only -z --diff-filter=AM)
echo "staged payload: $(( total / 1024 )) KB"
[ "$total" -gt "$max_total" ] && { echo "total over limit"; bad=1; }
exit $bad
