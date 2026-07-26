#!/bin/bash
set -e

BACKUP_DIR="/backups/zim-emr"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting backup..."

docker exec zim-emr-db pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc \
  > "$BACKUP_DIR/zim_emr_$DATE.dump"

gzip "$BACKUP_DIR/zim_emr_$DATE.dump"

find "$BACKUP_DIR" -name "zim_emr_*.dump.gz" -mtime +$RETENTION_DAYS -delete

echo "[$(date)] Backup complete: zim_emr_$DATE.dump.gz"