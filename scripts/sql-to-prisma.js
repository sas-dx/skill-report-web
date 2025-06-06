const fs = require('fs');
const path = require('path');

const ddlDir = process.argv[2];
const outputFile = process.argv[3];
const provider = process.env.DB_PROVIDER || 'postgresql';
if (!ddlDir || !outputFile) {
  console.error('Usage: node sql-to-prisma.js <ddl_dir> <output_file>');
  process.exit(1);
}

function toModelName(name) {
  return name.replace(/^([A-Z]+_)/, '').replace(/(?:^|_)([A-Za-z])/g, (_,c)=>c.toUpperCase());
}

function mapType(t) {
  const base = t.toLowerCase().split('(')[0];
  if (['varchar','text','char','enum'].includes(base)) return 'String';
  if (['int','integer','smallint','mediumint'].includes(base)) return 'Int';
  if (['bigint'].includes(base)) return 'BigInt';
  if (['decimal','numeric','double','float'].includes(base)) return 'Decimal';
  if (['date','datetime','timestamp','time'].includes(base)) return 'DateTime';
  if (['boolean','tinyint'].includes(base)) return 'Boolean';
  return 'String';
}

const schema = [];
schema.push('generator client {');
schema.push('  provider = "prisma-client-js"');
schema.push('}');
schema.push('');
schema.push('datasource db {');
schema.push(`  provider = "${provider}"`);
schema.push('  url      = env("DATABASE_URL")');
schema.push('}');
schema.push('');

const processed = new Set();

for (const file of fs.readdirSync(ddlDir)) {
  if (!file.endsWith('.sql')) continue;
  if (file === 'all_tables.sql' || file.startsWith('------------')) continue;
  const content = fs.readFileSync(path.join(ddlDir, file), 'utf8');
  const tableMatch = content.match(/CREATE TABLE\s+(\w+)\s*\(([^;]*)\)/s);
  if (!tableMatch) continue;
  const tableName = tableMatch[1];
  if (processed.has(tableName)) continue;
  processed.add(tableName);
  const block = tableMatch[2];
  const lines = block.split(/\n/).map(l=>l.trim()).filter(l=>l && !l.startsWith('--'));
  const columns = [];
  let primaryCols = [];
  const pkMatch = content.match(/PRIMARY KEY\s*\(([^)]+)\)/i);
  if (pkMatch) {
    primaryCols = pkMatch[1].split(/\s*,\s*/).map(c => c.replace(/`/g, ''));
  }

  const uniqueIndices = [];
  const uniqRegexes = [
    /CREATE UNIQUE INDEX\s+\w+\s+ON\s+\w+\s*\(([^)]+)\)/gi,
    /ALTER TABLE\s+\w+\s+ADD CONSTRAINT\s+\w+\s+UNIQUE\s*\(([^)]+)\)/gi
  ];
  for (const re of uniqRegexes) {
    let m;
    while ((m = re.exec(content))) {
      const cols = m[1].split(/\s*,\s*/).map(c=>c.replace(/`/g,''));
      if (cols[0]) uniqueIndices.push(cols);
    }
  }

  const columnDefs = [];
  for (const line of lines) {
    const clean = line.replace(/,\s*$/, '').replace(/COMMENT\s+'.*'/i, '').trim();
    if (/^(PRIMARY KEY|UNIQUE|KEY|CONSTRAINT)/i.test(clean)) continue;
    const m = clean.match(/^`?([A-Za-z0-9_]+)`?\s+([A-Za-z]+(?:\([0-9,]+\))?)/);
    if (!m) continue;
    columnDefs.push({
      name: m[1],
      type: mapType(m[2]),
      optional: !/NOT NULL/i.test(clean)
    });
  }

  if (primaryCols.length === 0 && uniqueIndices.length) {
    primaryCols = uniqueIndices.shift();
  }

  if (primaryCols.length === 0) {
    const idCol = columnDefs.find(c => c.name === 'id');
    if (idCol) primaryCols = ['id'];
    else if (columnDefs.length) primaryCols = [columnDefs[0].name];
  }

  const uniqueSingles = [];
  const uniqueMulti = [];
  for (const u of uniqueIndices) {
    if (u.length === 1) uniqueSingles.push(u[0]);
    else uniqueMulti.push(u);
  }

  for (const col of columnDefs) {
    const isPkField = primaryCols.includes(col.name);
    const parts = [`  ${col.name}`, col.type];
    if (!isPkField && col.optional) parts[1] += '?';
    if (primaryCols.length === 1 && isPkField) {
      parts.push('@id');
    } else if (uniqueSingles.includes(col.name) && !isPkField) {
      parts.push('@unique');
    }
    columns.push(parts.join(' '));
  }
  const modelName = toModelName(tableName);
  schema.push(`model ${modelName} {`);
  schema.push(...columns);
  if (primaryCols.length > 1) {
    schema.push(`  @@id([${primaryCols.join(', ')}])`);
  }
  for (const u of uniqueMulti) {
    schema.push(`  @@unique([${u.join(', ')}])`);
  }
  schema.push(`  @@map("${tableName}")`);
  schema.push('}');
  schema.push('');
}

fs.writeFileSync(outputFile, schema.join('\n'));
