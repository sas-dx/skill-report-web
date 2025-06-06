#!/bin/bash
# Convert SQL DDL files in docs/design/database/ddl to Prisma schema
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DDL_DIR="$ROOT_DIR/docs/design/database/ddl"
OUT_FILE="$ROOT_DIR/src/database/prisma/schema.prisma"

node "$SCRIPT_DIR/sql-to-prisma.js" "$DDL_DIR" "$OUT_FILE"

echo "Generated Prisma schema at $OUT_FILE"
