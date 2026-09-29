#!/data/data/com.termux/files/usr/bin/bash
set -e

PROJECT="$(cd "$(dirname "$0")" && pwd)"
BACKUP_DIR="$PROJECT/backups"

mkdir -p "$BACKUP_DIR"

STAMP="$(date -u +"%Y%m%d_%H%M%S")"
ARCHIVE="$BACKUP_DIR/ultron_$STAMP.tar.gz"

tar \
  --exclude="./backups" \
  --exclude="./.git" \
  -czf "$ARCHIVE" \
  -C "$PROJECT" .

echo "Backup criado:"
echo "$ARCHIVE"
