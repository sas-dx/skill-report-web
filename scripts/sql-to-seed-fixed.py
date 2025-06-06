#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL サンプルデータから Prisma seed.ts ファイルを生成するスクリプト（修正版）
要求仕様ID: PLT.1-DB.1 - データベース初期データ投入自動化
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class SQLToSeedConverter:
    def __init__(self, sql_data_dir: str, output_file: str):
        self.sql_data_dir = Path(sql_data_dir)
        self.output_file = Path(output_file)
        self.table_data = {}
        
        # テーブル名のマッピング（SQL名 -> Prisma名）
        self.table_mapping = {
            'MST_Tenant': 'tenant',
            'MST_Department': 'department', 
            'MST_Position': 'position',
            'MST_JobType': 'jobType',
            'MST_Role': 'role',
            'MST_Permission': 'permission',
            'MST_SkillCategory': 'skillCategory',
            'MST_SkillItem': 'skillItem',
            'MST_Employee': 'employee',
            'MST_UserAuth': 'userAuth',
            'MST_UserRole': 'userRole',
            'TRN_SkillRecord': 'skillRecord',
        }
        
        # 依存関係の定義（参照される側 -> 参照する側の順序）
        self.dependency_order = [
            'MST_Tenant',
            'MST_Department', 
            'MST_Position',
            'MST_JobType',
            'MST_Role',
            'MST_Permission',
            'MST_SkillCategory',
            'MST_SkillItem',
            'MST_Employee',
            'MST_UserAuth',
            'MST_UserRole',
            'TRN_SkillRecord',
        ]

    def parse_sql_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """SQLファイルを解析してデータを抽出"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # テーブル名を抽出
            table_match = re.search(r'INSERT INTO (\w+)', content, re.IGNORECASE)
            if not table_match:
                return None
                
            table_name = table_match.group(1)
            
            # カラム名を抽出（複数行対応）
            columns_match = re.search(r'INSERT INTO \w+\s*\(\s*([^)]+)\s*\)\s*VALUES', content, re.IGNORECASE | re.DOTALL)
            if not columns_match:
                return None
                
            columns_text = columns_match.group(1)
            # カラム名をクリーンアップ
            columns = []
            for line in columns_text.split('\n'):
                line = line.strip()
                if line and not line.startswith('--'):
                    # カンマで分割してクリーンアップ
                    parts = line.split(',')
                    for part in parts:
                        part = part.strip()
                        if part:
                            columns.append(part)
            
            # VALUES句を抽出（セミコロンまで）
            values_match = re.search(r'VALUES\s*(.+?);', content, re.IGNORECASE | re.DOTALL)
            if not values_match:
                return None
                
            values_text = values_match.group(1)
            
            # 各行のデータを抽出
            rows = self.parse_values_section(values_text)
            
            # カラム数とデータ数の整合性チェック
            valid_rows = []
            for row in rows:
                if len(row) == len(columns):
                    row_data = dict(zip(columns, row))
                    valid_rows.append(row_data)
                else:
                    print(f"Warning: Column count mismatch in {table_name}: expected {len(columns)}, got {len(row)}")
            
            return {
                'table_name': table_name,
                'columns': columns,
                'rows': valid_rows
            }
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def parse_values_section(self, values_text: str) -> List[List[str]]:
        """VALUES句を解析して行データを抽出"""
        rows = []
        current_row = []
        current_value = ""
        in_quotes = False
        quote_char = None
        paren_depth = 0
        bracket_depth = 0
        
        i = 0
        while i < len(values_text):
            char = values_text[i]
            
            if not in_quotes:
                if char in ["'", '"']:
                    in_quotes = True
                    quote_char = char
                    current_value += char
                elif char == '(':
                    if paren_depth == 0:
                        # 新しい行の開始
                        current_row = []
                        current_value = ""
                    else:
                        current_value += char
                    paren_depth += 1
                elif char == ')':
                    paren_depth -= 1
                    if paren_depth == 0:
                        # 行の終了
                        if current_value.strip():
                            current_row.append(current_value.strip())
                        if current_row:
                            rows.append(current_row)
                        current_row = []
                        current_value = ""
                    else:
                        current_value += char
                elif char == '[':
                    bracket_depth += 1
                    current_value += char
                elif char == ']':
                    bracket_depth -= 1
                    current_value += char
                elif char == ',' and paren_depth > 0:
                    # 値の区切り
                    current_row.append(current_value.strip())
                    current_value = ""
                else:
                    current_value += char
            else:
                current_value += char
                if char == quote_char:
                    # エスケープされていない引用符の終了をチェック
                    if i == 0 or values_text[i-1] != '\\':
                        in_quotes = False
                        quote_char = None
            
            i += 1
        
        return rows

    def convert_value(self, value: str, column_name: str) -> str:
        """SQLの値をTypeScript/Prismaの値に変換"""
        value = value.strip()
        
        # NULL値
        if value.upper() == 'NULL':
            return 'null'
        
        # 文字列値（引用符で囲まれている）
        if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
            # 引用符を除去してエスケープ
            inner_value = value[1:-1]
            # JavaScriptの文字列としてエスケープ
            inner_value = inner_value.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\r', '\\r')
            return f"'{inner_value}'"
        
        # 数値（整数・小数）
        if re.match(r'^-?\d+(\.\d+)?$', value):
            return value
        
        # ブール値
        if value.upper() in ['TRUE', 'FALSE']:
            return value.lower()
        
        # 日付・時刻（ISO形式に変換）
        date_patterns = [
            r"'\d{4}-\d{2}-\d{2}'",
            r"'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'",
            r"'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'"
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, value):
                date_str = value[1:-1]  # 引用符を除去
                return f"new Date('{date_str}')"
        
        # JSON配列・オブジェクト
        if value.startswith("'[") and value.endswith("]'"):
            try:
                json_str = value[1:-1]  # 外側の引用符を除去
                json.loads(json_str)  # 有効性チェック
                return json_str
            except:
                pass
        
        if value.startswith("'{") and value.endswith("}'"):
            try:
                json_str = value[1:-1]  # 外側の引用符を除去
                json.loads(json_str)  # 有効性チェック
                return json_str
            except:
                pass
        
        # その他は文字列として扱う
        if not value.startswith("'"):
            value = f"'{value}'"
        
        return value

    def get_primary_key(self, table_name: str, columns: List[str]) -> str:
        """テーブルの主キーを推定"""
        # テーブル別の主キー定義
        primary_keys = {
            'MST_Tenant': 'tenant_id',
            'MST_Department': 'department_code',
            'MST_Position': 'position_code',
            'MST_JobType': 'job_type_code',
            'MST_Role': 'role_code',
            'MST_Permission': 'permission_code',
            'MST_SkillCategory': 'category_code',
            'MST_SkillItem': 'skill_code',
            'MST_Employee': 'employee_code',
            'MST_UserAuth': 'user_id',
            'MST_UserRole': 'user_id_role_id',  # 複合キー
            'TRN_SkillRecord': 'employee_id_skill_item_id',  # 複合キー
        }
        
        return primary_keys.get(table_name, columns[0] if columns else 'id')

    def get_code_name_mapping(self, table_name: str) -> Dict[str, str]:
        """テーブル別のcode/nameフィールドマッピングを取得"""
        mappings = {
            'MST_Tenant': {
                'code_field': 'tenant_code',
                'name_field': 'tenant_name'
            },
            'MST_Department': {
                'code_field': 'department_code', 
                'name_field': 'department_name'
            },
            'MST_Position': {
                'code_field': 'position_code',
                'name_field': 'position_name'
            },
            'MST_JobType': {
                'code_field': 'job_type_code',
                'name_field': 'job_type_name'
            },
            'MST_Role': {
                'code_field': 'role_code',
                'name_field': 'role_name'
            },
            'MST_Permission': {
                'code_field': 'permission_code',
                'name_field': 'permission_name'
            },
            'MST_SkillCategory': {
                'code_field': 'category_code',
                'name_field': 'category_name'
            },
            'MST_SkillItem': {
                'code_field': 'skill_code',
                'name_field': 'skill_name'
            },
            'MST_Employee': {
                'code_field': 'employee_code',
                'name_field': 'full_name'
            },
            'MST_UserAuth': {
                'code_field': 'user_id',  # user_idをcodeとして使用
                'name_field': 'login_id'  # login_idをnameとして使用
            },
            'MST_UserRole': {
                'code_field': None,  # 複合キーのため個別設定
                'name_field': None
            },
            'TRN_SkillRecord': {
                'code_field': None,  # 複合キーのため個別設定
                'name_field': None
            }
        }
        return mappings.get(table_name, {'code_field': None, 'name_field': None})

    def generate_upsert_code(self, table_name: str, data: Dict[str, Any]) -> str:
        """テーブルのupsertコードを生成"""
        prisma_table = self.table_mapping.get(table_name, table_name.lower())
        rows = data['rows']
        columns = data['columns']
        
        if not rows:
            return ""
        
        primary_key = self.get_primary_key(table_name, columns)
        code_name_mapping = self.get_code_name_mapping(table_name)
        
        code_lines = []
        code_lines.append(f"    // {table_name}データ")
        code_lines.append(f"    console.log('📊 {table_name}データを投入中...')")
        code_lines.append(f"    const {prisma_table}Data = await Promise.all([")
        
        for i, row in enumerate(rows):
            # whereクエリ用の条件
            if primary_key == 'user_id_role_id':
                # 複合キーの場合
                user_id = self.convert_value(row.get('user_id', ''), 'user_id')
                role_id = self.convert_value(row.get('role_id', ''), 'role_id')
                where_clause = f"{{ user_id_role_id: {{ user_id: {user_id}, role_id: {role_id} }} }}"
            elif primary_key == 'employee_id_skill_item_id':
                # 複合キーの場合
                employee_id = self.convert_value(row.get('employee_id', ''), 'employee_id')
                skill_item_id = self.convert_value(row.get('skill_item_id', ''), 'skill_item_id')
                where_clause = f"{{ employee_id_skill_item_id: {{ employee_id: {employee_id}, skill_item_id: {skill_item_id} }} }}"
            else:
                # 単一キーの場合
                where_value = self.convert_value(row.get(primary_key, ''), primary_key)
                where_clause = f"{{ {primary_key}: {where_value} }}"
            
            code_lines.append(f"      prisma.{prisma_table}.upsert({{")
            code_lines.append(f"        where: {where_clause},")
            code_lines.append(f"        update: {{}},")
            code_lines.append(f"        create: {{")
            
            # 各フィールドを追加
            for col, val in row.items():
                if val and val.upper() != 'NULL':
                    converted_val = self.convert_value(val, col)
                    code_lines.append(f"          {col}: {converted_val},")
            
            # code/nameフィールドの自動設定
            self.add_code_name_fields(code_lines, row, table_name, code_name_mapping)
            
            code_lines.append(f"        }},")
            code_lines.append(f"      }}),")
        
        code_lines.append(f"    ])")
        code_lines.append("")
        
        return "\n".join(code_lines)

    def add_code_name_fields(self, code_lines: List[str], row: Dict[str, str], table_name: str, mapping: Dict[str, str]):
        """code/nameフィールドを自動追加"""
        code_field = mapping.get('code_field')
        name_field = mapping.get('name_field')
        
        # codeフィールドの設定
        if code_field and code_field in row:
            code_value = row[code_field]
            if code_value and code_value.upper() != 'NULL':
                # 既存のフィールドと重複しないようにチェック
                if 'code' not in row:
                    converted_val = self.convert_value(code_value, 'code')
                    code_lines.append(f"          code: {converted_val},")
        
        # nameフィールドの設定
        if name_field and name_field in row:
            name_value = row[name_field]
            if name_value and name_value.upper() != 'NULL':
                # 既存のフィールドと重複しないようにチェック
                if 'name' not in row:
                    converted_val = self.convert_value(name_value, 'name')
                    code_lines.append(f"          name: {converted_val},")
        
        # 特別なケース：複合キーテーブル
        if table_name == 'MST_UserRole':
            # user_id + role_idからnameを生成
            user_id = row.get('user_id', '')
            role_id = row.get('role_id', '')
            if user_id and role_id and 'name' not in row:
                name_value = f"{user_id}-{role_id}"
                code_lines.append(f"          name: '{name_value}',")
            
            # user_idをcodeとして使用
            if user_id and 'code' not in row:
                converted_val = self.convert_value(user_id, 'code')
                code_lines.append(f"          code: {converted_val},")
        
        elif table_name == 'TRN_SkillRecord':
            # employee_id + skill_item_idからnameを生成
            employee_id = row.get('employee_id', '')
            skill_item_id = row.get('skill_item_id', '')
            if employee_id and skill_item_id and 'name' not in row:
                name_value = f"{employee_id}-{skill_item_id}"
                code_lines.append(f"          name: '{name_value}',")
            
            # employee_idをcodeとして使用
            if employee_id and 'code' not in row:
                converted_val = self.convert_value(employee_id, 'code')
                code_lines.append(f"          code: {converted_val},")

    def generate_seed_file(self):
        """seed.tsファイルを生成"""
        # SQLファイルを読み込み
        for sql_file in self.sql_data_dir.glob("*.sql"):
            if sql_file.name.endswith('_sample_data.sql'):
                data = self.parse_sql_file(sql_file)
                if data:
                    table_name = data['table_name']
                    self.table_data[table_name] = data
                    print(f"Parsed: {table_name} ({len(data['rows'])} rows)")

        # seed.tsファイルを生成
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_header())
            
            # 依存関係順にテーブルを処理
            for table_name in self.dependency_order:
                if table_name in self.table_data:
                    upsert_code = self.generate_upsert_code(table_name, self.table_data[table_name])
                    if upsert_code:
                        f.write(upsert_code)
                        f.write("\n")
            
            f.write(self.generate_footer())
        
        print(f"Generated seed file: {self.output_file}")

    def generate_header(self) -> str:
        """seed.tsファイルのヘッダーを生成"""
        return '''// 要求仕様ID: PLT.1-DB.1 - データベース初期データ投入
// 設計書: docs/design/database/data/ 配下のサンプルデータSQLファイル群
// 自動生成日時: ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function main() {
  console.log('🌱 データベースの初期データ投入を開始します...')

  try {
'''

    def generate_footer(self) -> str:
        """seed.tsファイルのフッターを生成"""
        return '''
    console.log('✅ データベースの初期データ投入が完了しました！')
    console.log('📋 投入されたデータの詳細はログを確認してください')
    console.log('')
    console.log('🔐 ログイン情報:')
    console.log('   管理者:')
    console.log('     ユーザーID: admin@skill-report.local')
    console.log('     パスワード: password')
    console.log('   テストユーザー1:')
    console.log('     ユーザーID: yamada.taro@company.com')
    console.log('     パスワード: password')
    console.log('   テストユーザー2:')
    console.log('     ユーザーID: sato.hanako@company.com')
    console.log('     パスワード: password')

  } catch (error) {
    console.error('❌ 初期データ投入中にエラーが発生しました:', error)
    throw error
  }
}

main()
  .then(async () => {
    await prisma.$disconnect()
  })
  .catch(async (e) => {
    console.error('❌ 初期データ投入中にエラーが発生しました:', e)
    await prisma.$disconnect()
    throw e
  })
'''

def main():
    """メイン処理"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SQLサンプルデータからPrisma seed.tsファイルを生成（修正版）')
    parser.add_argument('--sql-dir', default='docs/design/database/data', 
                       help='SQLファイルのディレクトリ (default: docs/design/database/data)')
    parser.add_argument('--output', default='src/database/prisma/seed.ts',
                       help='出力ファイル (default: src/database/prisma/seed.ts)')
    parser.add_argument('--backup', action='store_true',
                       help='既存のseed.tsファイルをバックアップ')
    
    args = parser.parse_args()
    
    # バックアップ作成
    if args.backup and os.path.exists(args.output):
        backup_file = f"{args.output}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.rename(args.output, backup_file)
        print(f"Backup created: {backup_file}")
    
    # 変換実行
    converter = SQLToSeedConverter(args.sql_dir, args.output)
    converter.generate_seed_file()
    
    print("✅ seed.tsファイルの生成が完了しました！")
    print(f"📁 出力ファイル: {args.output}")
    print("🚀 実行方法: npm run db:seed")

if __name__ == '__main__':
    main()
