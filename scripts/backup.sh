#!/bin/bash
set -e

BACKUP_DIR="/backups/emr"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting backup..."

docker exec emr-db pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc \
  > "$BACKUP_DIR/emr_$DATE.dump"

gzip "$BACKUP_DIR/emr_$DATE.dump"

find "$BACKUP_DIR" -name "emr_*.dump.gz" -mtime +$RETENTION_DAYS -delete

echo "[$(date)] Backup complete: emr_$DATE.dump.gz"
