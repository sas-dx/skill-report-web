#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL サンプルデータから Prisma seed.ts ファイルを生成するスクリプト
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
        self.table_order = []
        
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
            'MST_SkillGrade': 'skillGrade',
            'MST_SkillHierarchy': 'skillHierarchy',
            'MST_Certification': 'certification',
            'MST_CertificationRequirement': 'certificationRequirement',
            'MST_CareerPlan': 'careerPlan',
            'MST_TrainingProgram': 'trainingProgram',
            'MST_SystemConfig': 'systemConfig',
            'MST_TenantSettings': 'tenantSettings',
            'MST_NotificationSettings': 'notificationSettings',
            'MST_NotificationTemplate': 'notificationTemplate',
            'MST_ReportTemplate': 'reportTemplate',
            'TRN_EmployeeSkillGrade': 'employeeSkillGrade',
            'TRN_GoalProgress': 'goalProgress',
            'TRN_Notification': 'notification',
            'TRN_PDU': 'pdu',
            'TRN_ProjectRecord': 'projectRecord',
            'TRN_SkillEvidence': 'skillEvidence',
            'TRN_TrainingHistory': 'trainingHistory',
            'HIS_AuditLog': 'auditLog',
            'HIS_NotificationLog': 'notificationLog',
            'HIS_TenantBilling': 'tenantBilling',
            'SYS_BackupHistory': 'backupHistory',
            'SYS_IntegrationConfig': 'integrationConfig',
            'SYS_MasterData': 'masterData',
            'SYS_SkillIndex': 'skillIndex',
            'SYS_SkillMatrix': 'skillMatrix',
            'SYS_SystemLog': 'systemLog',
            'SYS_TenantUsage': 'tenantUsage',
            'SYS_TokenStore': 'tokenStore',
            'WRK_BatchJobLog': 'batchJobLog',
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
            'MST_SkillGrade',
            'MST_SkillHierarchy',
            'MST_Certification',
            'MST_Employee',
            'MST_UserAuth',
            'MST_UserRole',
            'MST_CertificationRequirement',
            'MST_CareerPlan',
            'MST_TrainingProgram',
            'MST_SystemConfig',
            'MST_TenantSettings',
            'MST_NotificationSettings',
            'MST_NotificationTemplate',
            'MST_ReportTemplate',
            'TRN_SkillRecord',
            'TRN_EmployeeSkillGrade',
            'TRN_GoalProgress',
            'TRN_Notification',
            'TRN_PDU',
            'TRN_ProjectRecord',
            'TRN_SkillEvidence',
            'TRN_TrainingHistory',
            'HIS_AuditLog',
            'HIS_NotificationLog',
            'HIS_TenantBilling',
            'SYS_BackupHistory',
            'SYS_IntegrationConfig',
            'SYS_MasterData',
            'SYS_SkillIndex',
            'SYS_SkillMatrix',
            'SYS_SystemLog',
            'SYS_TenantUsage',
            'SYS_TokenStore',
            'WRK_BatchJobLog',
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
            
            # カラム名を抽出
            columns_match = re.search(r'INSERT INTO \w+\s*\(\s*([^)]+)\s*\)', content, re.IGNORECASE | re.DOTALL)
            if not columns_match:
                return None
                
            columns_text = columns_match.group(1)
            columns = [col.strip().strip(',') for col in columns_text.split('\n') if col.strip()]
            columns = [col for col in columns if col and not col.startswith('--')]
            
            # VALUES句を抽出
            values_match = re.search(r'VALUES\s*(.+?)(?:;|\n--)', content, re.IGNORECASE | re.DOTALL)
            if not values_match:
                return None
                
            values_text = values_match.group(1)
            
            # 各行のデータを抽出
            rows = []
            # VALUES内の各行を解析（括弧で囲まれた部分）
            row_pattern = r'\(\s*([^)]+)\s*\)'
            row_matches = re.findall(row_pattern, values_text, re.DOTALL)
            
            for row_match in row_matches:
                row_values = self.parse_row_values(row_match)
                if len(row_values) == len(columns):
                    row_data = dict(zip(columns, row_values))
                    rows.append(row_data)
            
            return {
                'table_name': table_name,
                'columns': columns,
                'rows': rows
            }
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def parse_row_values(self, row_text: str) -> List[str]:
        """行の値を解析"""
        values = []
        current_value = ""
        in_quotes = False
        quote_char = None
        paren_depth = 0
        
        i = 0
        while i < len(row_text):
            char = row_text[i]
            
            if not in_quotes:
                if char in ["'", '"']:
                    in_quotes = True
                    quote_char = char
                    current_value += char
                elif char == '(':
                    paren_depth += 1
                    current_value += char
                elif char == ')':
                    paren_depth -= 1
                    current_value += char
                elif char == ',' and paren_depth == 0:
                    values.append(current_value.strip())
                    current_value = ""
                else:
                    current_value += char
            else:
                current_value += char
                if char == quote_char:
                    # エスケープされていない引用符の終了をチェック
                    if i == 0 or row_text[i-1] != '\\':
                        in_quotes = False
                        quote_char = None
            
            i += 1
        
        if current_value.strip():
            values.append(current_value.strip())
        
        return values

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
            inner_value = inner_value.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"')
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
        
        # JSON文字列
        if value.startswith("'{") and value.endswith("}'"):
            try:
                json_str = value[1:-1]  # 外側の引用符を除去
                # JSONとして解析してみる
                json.loads(json_str)
                return json_str
            except:
                pass
        
        # その他は文字列として扱う
        if not value.startswith("'"):
            value = f"'{value}'"
        
        return value

    def generate_upsert_code(self, table_name: str, data: Dict[str, Any]) -> str:
        """テーブルのupsertコードを生成"""
        prisma_table = self.table_mapping.get(table_name, table_name.lower())
        rows = data['rows']
        
        if not rows:
            return ""
        
        # 主キーを推定（通常は最初のカラムまたは_idで終わるカラム）
        columns = data['columns']
        primary_key = None
        
        # 一般的な主キーパターンを検索
        for col in columns:
            if col.lower() in ['id', 'code', f'{table_name.lower()}_id', f'{table_name.lower()}_code']:
                primary_key = col
                break
        
        if not primary_key and columns:
            primary_key = columns[0]  # デフォルトは最初のカラム
        
        code_lines = []
        code_lines.append(f"    // {table_name} ({data.get('description', 'データ')})")
        code_lines.append(f"    console.log('📊 {table_name}データを投入中...')")
        code_lines.append(f"    const {prisma_table}Data = await Promise.all([")
        
        for i, row in enumerate(rows):
            # whereクエリ用の条件
            where_value = self.convert_value(row.get(primary_key, ''), primary_key)
            
            code_lines.append(f"      prisma.{prisma_table}.upsert({{")
            code_lines.append(f"        where: {{ {primary_key}: {where_value} }},")
            code_lines.append(f"        update: {{}},")
            code_lines.append(f"        create: {{")
            
            # 各フィールドを追加
            for col, val in row.items():
                if val and val.upper() != 'NULL':
                    converted_val = self.convert_value(val, col)
                    code_lines.append(f"          {col}: {converted_val},")
            
            code_lines.append(f"        }},")
            code_lines.append(f"      }}),")
        
        code_lines.append(f"    ])")
        code_lines.append("")
        
        return "\n".join(code_lines)

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
    
    parser = argparse.ArgumentParser(description='SQLサンプルデータからPrisma seed.tsファイルを生成')
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
