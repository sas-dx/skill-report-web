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

schema.push('  url      = env("DATABASE_URL")');
schema.push('}');
schema.push('');


  const content = fs.readFileSync(path.join(ddlDir, file), 'utf8');
  const tableMatch = content.match(/CREATE TABLE\s+(\w+)\s*\(([^;]*)\)/s);
  if (!tableMatch) continue;
  const tableName = tableMatch[1];

  const block = tableMatch[2];
  const lines = block.split(/\n/).map(l=>l.trim()).filter(l=>l && !l.startsWith('--'));
  const columns = [];
  let primaryCols = [];
  const pkMatch = content.match(/PRIMARY KEY\s*\(([^)]+)\)/i);


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
