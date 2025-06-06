const fs = require('fs');
const path = require('path');

const ddlDir = process.argv[2];
const outputFile = process.argv[3];

if (!ddlDir || !outputFile) {
  console.error('Usage: node sql-to-prisma.js <ddl_dir> <output_file>');
  process.exit(1);
}

function toModelName(name) {
  return name.replace(/^([A-Z]+_)/, '').replace(/(?:^|_)([A-Za-z])/g, (_, c) => c.toUpperCase());
}

function mapType(t) {
  const base = t.toLowerCase().split('(')[0];
  if (['varchar', 'text', 'char', 'enum'].includes(base)) return 'String';
  if (['int', 'integer', 'smallint', 'mediumint'].includes(base)) return 'Int';
  if (['bigint'].includes(base)) return 'BigInt';
  if (['decimal', 'numeric', 'double', 'float'].includes(base)) return 'Decimal';
  if (['date', 'datetime', 'timestamp', 'time'].includes(base)) return 'DateTime';
  if (['boolean', 'tinyint'].includes(base)) return 'Boolean';
  return 'String';
}

function parseColumn(line) {
  // カラム定義の解析: column_name TYPE [NOT NULL] [DEFAULT value] [COMMENT 'comment']
  const match = line.match(/^\s*(\w+)\s+([^,\s]+(?:\([^)]*\))?)\s*(.*)/);
  if (!match) return null;
  
  const [, columnName, dataType, rest] = match;
  const isOptional = !rest.includes('NOT NULL');
  const prismaType = mapType(dataType);
  
  return {
    name: columnName,
    type: prismaType,
    optional: isOptional
  };
}

const schema = [];
schema.push('generator client {');
schema.push('  provider = "prisma-client-js"');
schema.push('}');
schema.push('');
schema.push('datasource db {');
schema.push('  provider = "postgresql"');
schema.push('  url      = env("DATABASE_URL")');
schema.push('}');
schema.push('');

// DDLディレクトリ内のSQLファイルを取得
const files = fs.readdirSync(ddlDir).filter(file => file.endsWith('.sql'));

for (const file of files) {
  try {
    const content = fs.readFileSync(path.join(ddlDir, file), 'utf8');
    const tableMatch = content.match(/CREATE TABLE\s+(\w+)\s*\(([^;]*)\)/s);
    
    if (!tableMatch) {
      console.warn(`No CREATE TABLE found in ${file}`);
      continue;
    }
    
    const tableName = tableMatch[1];
    const block = tableMatch[2];
    
    // カラム定義の行を抽出
    const lines = block.split(/\n/).map(l => l.trim()).filter(l => l && !l.startsWith('--'));
    const columns = [];
    let primaryCols = [];
    
    // PRIMARY KEY制約の検索
    const pkMatch = content.match(/PRIMARY KEY\s*\(([^)]+)\)/i);
    if (pkMatch) {
      primaryCols = pkMatch[1].split(',').map(col => col.trim());
    }
    
    // カラム定義の解析
    for (const line of lines) {
      // PRIMARY KEY、FOREIGN KEY、CONSTRAINT等の制約は除外
      if (line.toUpperCase().includes('PRIMARY KEY') || 
          line.toUpperCase().includes('FOREIGN KEY') ||
          line.toUpperCase().includes('CONSTRAINT') ||
          line.toUpperCase().includes('INDEX') ||
          line.toUpperCase().includes('KEY ')) {
        continue;
      }
      
      const column = parseColumn(line);
      if (column) {
        const isPrimary = primaryCols.includes(column.name);
        let columnDef = `  ${column.name} ${column.type}`;
        
        if (isPrimary) {
          columnDef += ' @id';
          if (column.type === 'Int' && column.name.toLowerCase().includes('id')) {
            columnDef += ' @default(autoincrement())';
          }
        } else if (column.optional) {
          columnDef += '?';
        }
        
        // デフォルト値の処理
        if (column.name === 'created_at' || column.name === 'updated_at') {
          columnDef += ' @default(now())';
        }
        
        // カラム名のマッピング（snake_case -> camelCase）
        if (column.name.includes('_')) {
          columnDef += ` @map("${column.name}")`;
        }
        
        columns.push(columnDef);
      }
    }
    
    // モデル定義の生成
    const modelName = toModelName(tableName);
    schema.push(`model ${modelName} {`);
    schema.push(...columns);
    
    // テーブル名のマッピング
    schema.push(`  @@map("${tableName}")`);
    schema.push('}');
    schema.push('');
    
    console.log(`Processed table: ${tableName} -> ${modelName}`);
    
  } catch (error) {
    console.error(`Error processing file ${file}:`, error.message);
  }
}

// スキーマファイルの出力
fs.writeFileSync(outputFile, schema.join('\n'));
console.log(`Prisma schema generated: ${outputFile}`);
