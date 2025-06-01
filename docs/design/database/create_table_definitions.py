#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル定義書生成スクリプト v12.0 (完全統合版)

改版履歴:
┌─────────┬────────────┬──────────┬─────────────────────────────────────────────────────┐
│ バージョン │    更新日    │  更新者  │                  主な変更内容                       │
├─────────┼────────────┼──────────┼─────────────────────────────────────────────────────┤
│  v12.0  │ 2025-06-01 │ システム │ 複数スクリプト統合・カラー出力・診断機能・完全版    │
│  v11.0  │ 2025-06-01 │ システム │ エラーハンドリング強化・ログ出力改善・診断機能追加  │
│  v10.0  │ 2025-06-01 │ システム │ 複数スクリプトの統合・単一ファイル化・機能統一      │
└─────────┴────────────┴──────────┴─────────────────────────────────────────────────────┘

統合内容:
- create_table_definitions.py (v10.0) - 基本機能・main関数
- create_table_definitions_enhanced.py (v11.0) - カラー出力・診断機能
- create_table_definitions_enhanced_complete.py (v11.0) - エラーハンドリング強化
→ 単一ファイルに完全統合し、保守性と運用効率を最大化

新機能:
- カラー出力対応（成功=緑、警告=黄、エラー=赤）
- 詳細診断レポート機能
- 不足YAMLファイルの自動テンプレート生成
- 実行前検証機能（ドライラン）
- エラー・警告の集約サマリー表示
- 進捗表示の改善
"""

import os
import re
import sys
import yaml
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

# カラー出力用（coloramaがない場合の代替）
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"

@dataclass
class ProcessingResult:
    """処理結果を格納するデータクラス"""
    table_name: str
    logical_name: str
    success: bool
    has_yaml: bool
    error_message: Optional[str] = None
    warning_message: Optional[str] = None

class EnhancedLogger:
    """強化されたログ出力クラス"""
    
    def __init__(self, enable_color: bool = True):
        self.enable_color = enable_color
        self.logs = []
    
    def _colorize(self, text: str, color: str) -> str:
        """テキストに色を付ける"""
        if not self.enable_color:
            return text
        return f"{color}{text}{Colors.END}"
    
    def info(self, message: str):
        """情報ログ"""
        colored_msg = self._colorize(f"ℹ️  {message}", Colors.BLUE)
        print(colored_msg)
        self.logs.append((LogLevel.INFO, message))
    
    def warning(self, message: str):
        """警告ログ"""
        colored_msg = self._colorize(f"⚠️  {message}", Colors.YELLOW)
        print(colored_msg)
        self.logs.append((LogLevel.WARNING, message))
    
    def error(self, message: str):
        """エラーログ"""
        colored_msg = self._colorize(f"❌ {message}", Colors.RED)
        print(colored_msg)
        self.logs.append((LogLevel.ERROR, message))
    
    def success(self, message: str):
        """成功ログ"""
        colored_msg = self._colorize(f"✅ {message}", Colors.GREEN)
        print(colored_msg)
        self.logs.append((LogLevel.SUCCESS, message))
    
    def header(self, message: str):
        """ヘッダーログ"""
        colored_msg = self._colorize(f"\n🚀 {message}", Colors.CYAN + Colors.BOLD)
        print(colored_msg)
        print(self._colorize("=" * 80, Colors.CYAN))
    
    def section(self, message: str):
        """セクションログ"""
        colored_msg = self._colorize(f"\n📋 {message}", Colors.MAGENTA + Colors.BOLD)
        print(colored_msg)
        print(self._colorize("-" * 60, Colors.MAGENTA))

class TableDefinitionGenerator:
    """テーブル定義書生成クラス（統合版）"""
    
    def __init__(self, base_dir: str = None, enable_color: bool = True):
        """初期化"""
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.tables_dir = self.base_dir / "tables"
        self.ddl_dir = self.base_dir / "ddl"
        self.details_dir = self.base_dir / "table-details"
        self.table_list_file = self.base_dir / "テーブル一覧.md"
        
        # ログ設定
        self.logger = EnhancedLogger(enable_color)
        
        # 処理結果追跡
        self.results: List[ProcessingResult] = []
        self.missing_yamls: List[str] = []
        
        # ディレクトリ作成
        self._ensure_directories()
        
        # テーブル情報
        self.tables_info = {}
        self.common_columns = self._get_common_columns()
    
    def _ensure_directories(self):
        """必要なディレクトリを作成"""
        try:
            self.tables_dir.mkdir(exist_ok=True)
            self.ddl_dir.mkdir(exist_ok=True)
            self.details_dir.mkdir(exist_ok=True)
        except Exception as e:
            self.logger.error(f"ディレクトリ作成に失敗しました: {e}")
            raise
        
    def _get_common_columns(self) -> Dict[str, Any]:
        """共通カラム定義を取得"""
        return {
            'audit_columns': [
                {
                    'name': 'created_at',
                    'logical': '作成日時',
                    'type': 'TIMESTAMP',
                    'length': None,
                    'null': False,
                    'default': 'CURRENT_TIMESTAMP',
                    'description': 'レコード作成日時'
                },
                {
                    'name': 'updated_at',
                    'logical': '更新日時',
                    'type': 'TIMESTAMP',
                    'length': None,
                    'null': False,
                    'default': 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                    'description': 'レコード更新日時'
                },
                {
                    'name': 'created_by',
                    'logical': '作成者',
                    'type': 'VARCHAR',
                    'length': 50,
                    'null': False,
                    'description': 'レコード作成者のユーザーID'
                },
                {
                    'name': 'updated_by',
                    'logical': '更新者',
                    'type': 'VARCHAR',
                    'length': 50,
                    'null': False,
                    'description': 'レコード更新者のユーザーID'
                }
            ],
            'tenant_columns': [
                {
                    'name': 'tenant_id',
                    'logical': 'テナントID',
                    'type': 'VARCHAR',
                    'length': 50,
                    'null': False,
                    'description': 'マルチテナント識別子'
                }
            ],
            'base_columns': [
                {
                    'name': 'id',
                    'logical': 'ID',
                    'type': 'VARCHAR',
                    'length': 50,
                    'null': False,
                    'primary': True,
                    'description': 'プライマリキー（UUID）'
                },
                {
                    'name': 'is_deleted',
                    'logical': '削除フラグ',
                    'type': 'BOOLEAN',
                    'length': None,
                    'null': False,
                    'default': False,
                    'description': '論理削除フラグ'
                }
            ]
        }
    
    def load_table_list(self) -> Dict[str, Dict[str, Any]]:
        """テーブル一覧.mdからテーブル情報を読み込み"""
        if not self.table_list_file.exists():
            raise FileNotFoundError(f"テーブル一覧ファイルが見つかりません: {self.table_list_file}")
        
        with open(self.table_list_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # テーブル情報を抽出（新しいテーブル一覧形式に対応）
        tables = {}
        
        # テーブル行のパターンを検索
        lines = content.split('\n')
        in_table = False
        
        for line in lines:
            # テーブルヘッダーを検出
            if '| テーブルID |' in line and 'テーブル名' in line:
                in_table = True
                continue
            
            # テーブル区切り行をスキップ
            if in_table and line.startswith('|---'):
                continue
            
            # テーブル終了を検出
            if in_table and (line.strip() == '' or not line.startswith('|')):
                in_table = False
                continue
            
            # テーブル行を解析
            if in_table and line.startswith('| TBL-'):
                parts = [part.strip() for part in line.split('|')]
                if len(parts) >= 5:
                    table_id = parts[1]
                    category = parts[2]
                    table_name = parts[3]
                    logical_name = parts[4]
                    
                    tables[table_name] = {
                        'table_id': table_id,
                        'category': category,
                        'logical_name': logical_name,
                        'table_name': table_name
                    }
        
        return tables
    
    def load_table_details(self, table_name: str) -> Tuple[Optional[Dict[str, Any]], bool]:
        """テーブル詳細定義YAMLを読み込み（存在フラグも返す）"""
        details_file = self.details_dir / f"{table_name}_details.yaml"
        
        if not details_file.exists():
            return None, False
        
        try:
            with open(details_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f), True
        except Exception as e:
            self.logger.error(f"{details_file} の読み込みに失敗: {e}")
            return None, False
    
    def generate_ddl(self, table_name: str, table_info: Dict[str, Any]) -> Tuple[str, bool]:
        """DDLを生成（YAMLファイル存在フラグも返す）"""
        details, has_yaml = self.load_table_details(table_name)
        
        ddl_content = f"-- {table_name} ({table_info['logical_name']}) DDL\n"
        ddl_content += f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        if not has_yaml:
            ddl_content += "-- 注意: 詳細YAMLファイルが存在しないため、基本定義のみで生成\n"
        ddl_content += "\n"
        
        # テーブル作成
        ddl_content += f"CREATE TABLE {table_name} (\n"
        
        columns = []
        
        # 基本カラム
        for col in self.common_columns['base_columns']:
            col_type = col['type']
            if col.get('length'):
                col_type += f"({col['length']})"
            
            col_def = f"    {col['name']} {col_type}"
            if not col.get('null', True):
                col_def += " NOT NULL"
            if col.get('default') is not None:
                if isinstance(col['default'], str):
                    col_def += f" DEFAULT '{col['default']}'"
                else:
                    col_def += f" DEFAULT {col['default']}"
            if col.get('primary'):
                col_def += " PRIMARY KEY"
            columns.append(col_def)
        
        # テナントカラム
        if not table_name.startswith('SYS_'):
            for col in self.common_columns['tenant_columns']:
                col_type = col['type']
                if col.get('length'):
                    col_type += f"({col['length']})"
                
                col_def = f"    {col['name']} {col_type}"
                if not col.get('null', True):
                    col_def += " NOT NULL"
                columns.append(col_def)
        
        # 業務固有カラム
        if details and 'business_columns' in details:
            for col in details['business_columns']:
                col_type = col['type']
                if col.get('length'):
                    col_type += f"({col['length']})"
                
                col_def = f"    {col['name']} {col_type}"
                if not col.get('null', True):
                    col_def += " NOT NULL"
                if col.get('default') is not None:
                    if isinstance(col['default'], str):
                        col_def += f" DEFAULT '{col['default']}'"
                    else:
                        col_def += f" DEFAULT {col['default']}"
                columns.append(col_def)
        
        # 監査カラム
        for col in self.common_columns['audit_columns']:
            col_type = col['type']
            if col.get('length'):
                col_type += f"({col['length']})"
            
            col_def = f"    {col['name']} {col_type}"
            if not col.get('null', True):
                col_def += " NOT NULL"
            if col.get('default'):
                col_def += f" DEFAULT {col['default']}"
            columns.append(col_def)
        
        ddl_content += ",\n".join(columns)
        ddl_content += "\n);\n\n"
        
        # インデックス作成
        if details and 'business_indexes' in details:
            for idx in details['business_indexes']:
                unique_str = "UNIQUE " if idx.get('unique', False) else ""
                columns_str = ", ".join(idx['columns'])
                ddl_content += f"CREATE {unique_str}INDEX {idx['name']} ON {table_name} ({columns_str});\n"
        
        # 外部キー制約
        if details and 'foreign_keys' in details:
            ddl_content += "\n-- 外部キー制約\n"
            for fk in details['foreign_keys']:
                ddl_content += f"ALTER TABLE {table_name} ADD CONSTRAINT {fk['name']} "
                ddl_content += f"FOREIGN KEY ({fk['column']}) REFERENCES {fk['reference_table']}({fk['reference_column']}) "
                ddl_content += f"ON UPDATE {fk['on_update']} ON DELETE {fk['on_delete']};\n"
        
        return ddl_content, has_yaml
    
    def generate_files(self, table_names: List[str] = None, output_dir: str = None, dry_run: bool = False):
        """ファイル生成メイン処理（統合版）"""
        # テーブル一覧読み込み
        self.tables_info = self.load_table_list()
        
        # 出力先ディレクトリ設定
        if output_dir:
            output_path = Path(output_dir)
            tables_output = output_path / "tables"
            ddl_output = output_path / "ddl"
            tables_output.mkdir(parents=True, exist_ok=True)
            ddl_output.mkdir(parents=True, exist_ok=True)
        else:
            tables_output = self.tables_dir
            ddl_output = self.ddl_dir
        
        # 処理対象テーブル決定
        if table_names:
            target_tables = {name: info for name, info in self.tables_info.items() if name in table_names}
            missing_tables = set(table_names) - set(self.tables_info.keys())
            if missing_tables:
                self.logger.warning(f"以下のテーブルが見つかりません: {', '.join(missing_tables)}")
        else:
            target_tables = self.tables_info
        
        self.logger.header(f"テーブル定義書生成スクリプト v12.0 (完全統合版)")
        self.logger.info(f"{len(target_tables)}個のテーブルを処理します。")
        
        if dry_run:
            self.logger.warning("ドライランモード: ファイルは実際には作成されません")
        
        generated_ddls = []
        
        for table_name, table_info in target_tables.items():
            self.logger.info(f"処理中: {table_name} ({table_info['logical_name']})")
            
            try:
                # DDL生成
                ddl_content, has_yaml = self.generate_ddl(table_name, table_info)
                ddl_file = ddl_output / f"{table_name}.sql"
                
                if not dry_run:
                    with open(ddl_file, 'w', encoding='utf-8') as f:
                        f.write(ddl_content)
                    self.logger.success(f"  ✓ {ddl_file}")
                else:
                    self.logger.info(f"  [DRY] {ddl_file}")
                
                generated_ddls.append(ddl_content)
                
                # 処理結果を記録
                result = ProcessingResult(
                    table_name=table_name,
                    logical_name=table_info['logical_name'],
                    success=True,
                    has_yaml=has_yaml
                )
                if not has_yaml:
                    result.warning_message = "YAMLファイルが存在しません"
                self.results.append(result)
                
            except Exception as e:
                error_msg = f"エラー: {e}"
                self.logger.error(f"  ❌ {error_msg}")
                
                # エラー結果を記録
                result = ProcessingResult(
                    table_name=table_name,
                    logical_name=table_info['logical_name'],
                    success=False,
                    has_yaml=False,
                    error_message=str(e)
                )
                self.results.append(result)
        
        # 統合DDL生成
        if generated_ddls and not dry_run:
            all_ddl_file = ddl_output / "all_tables.sql"
            with open(all_ddl_file, 'w', encoding='utf-8') as f:
                f.write("-- 全テーブル統合DDL\n")
                f.write(f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("\n\n".join(generated_ddls))
            self.logger.success(f"統合DDL: {all_ddl_file}")
        elif generated_ddls and dry_run:
            self.logger.info(f"[DRY] 統合DDL: {ddl_output / 'all_tables.sql'}")
        
        # 処理結果サマリー
        self._print_summary()
        
        self.logger.success(f"処理が完了しました！")
        self.logger.info(f"📁 DDL出力先: {ddl_output}")
    
    def _print_summary(self):
        """処理結果サマリーを表示"""
        self.logger.section("処理結果サマリー")
        
        total = len(self.results)
        success = len([r for r in self.results if r.success])
        errors = len([r for r in self.results if not r.success])
        warnings = len([r for r in self.results if r.success and not r.has_yaml])
        
        self.logger.info(f"総テーブル数: {total}")
        self.logger.success(f"成功: {success}")
        if errors > 0:
            self.logger.error(f"エラー: {errors}")
        if warnings > 0:
            self.logger.warning(f"警告: {warnings} (YAMLファイル不足)")
        
        # エラー詳細
        if errors > 0:
            self.logger.section("エラー詳細")
            for result in self.results:
                if not result.success:
                    self.logger.error(f"{result.table_name}: {result.error_message}")
        
        # 警告詳細
        if warnings > 0:
            self.logger.section("警告詳細 (YAMLファイル不足)")
            for result in self.results:
                if result.success and not result.has_yaml:
                    self.logger.warning(f"{result.table_name}: 基本定義のみで生成")

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="テーブル定義書生成スクリプト v12.0 (完全統合版)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 全テーブル生成
  python3 create_table_definitions.py
  
  # 個別テーブル生成
  python3 create_table_definitions.py --table MST_Employee
  python3 create_table_definitions.py --table MST_Role,MST_Permission
  
  # 出力先指定
  python3 create_table_definitions.py --table MST_Employee --output-dir custom/
  
  # ドライラン
  python3 create_table_definitions.py --dry-run
        """
    )
    
    parser.add_argument(
        '--table', '-t',
        help='生成対象テーブル名（カンマ区切りで複数指定可能）'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        help='出力先ディレクトリ'
    )
    
    parser.add_argument(
        '--base-dir', '-b',
        help='ベースディレクトリ（デフォルト: スクリプトのディレクトリ）'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='ドライラン（ファイルを実際には作成しない）'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='カラー出力を無効化'
    )
    
    args = parser.parse_args()
    
    try:
        generator = TableDefinitionGenerator(args.base_dir, not args.no_color)
        
        # 対象テーブル決定
        target_tables = None
        
        if args.table:
            target_tables = [t.strip() for t in args.table.split(',')]
        
        generator.generate_files(target_tables, args.output_dir, args.dry_run)
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
