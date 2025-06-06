const fs = require('fs');
const path = require('path');

const ddlDir = process.argv[2];
const outputFile = process.argv[3];

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

  if (pkMatch) {
    primaryCols = pkMatch[1].split(/\s*,\s*/).map(c => c.replace(/`/g, ''));
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

  if (primaryCols.length === 0) {
    const idCol = columnDefs.find(c => c.name === 'id');
    if (idCol) primaryCols = ['id'];
    else if (columnDefs.length) primaryCols = [columnDefs[0].name];
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


  for (const line of lines) {
    const clean = line.replace(/,\s*$/, '').replace(/COMMENT\s+'.*'/i,'').trim();
    if (/^(PRIMARY KEY|UNIQUE|KEY|CONSTRAINT)/i.test(clean)) continue;
    const m = clean.match(/^`?([A-Za-z0-9_]+)`?\s+([A-Za-z]+(?:\([0-9,]+\))?)/);
    if (!m) continue;
    const name = m[1];
    const type = mapType(m[2]);
    const optional = !/NOT NULL/i.test(clean);
    const isId = primaryCols.includes(name) || name === 'id';
    let field = `  ${name} ${type}`;
    if (optional && !isId) field += '?';
    if (isId) field += ' @id';

    columns.push(field);
  }
  const modelName = toModelName(tableName);
  schema.push(`model ${modelName} {`);
  schema.push(...columns);

  schema.push(`  @@map("${tableName}")`);
  schema.push('}');
  schema.push('');
}

fs.writeFileSync(outputFile, schema.join('\n'));
