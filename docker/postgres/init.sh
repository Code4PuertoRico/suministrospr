#!/bin/bash

FILE=/docker-entrypoint-initdb.d/backup.dump

if [[ -f "$FILE" ]]; then
  echo "==> Restoring..."
  pg_restore --verbose --clean --no-acl --no-owner -U postgres -d postgres $FILE || true
fi
