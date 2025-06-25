#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル詳細定義YAMLとサンプルデータの整合性チェックツール

要求仕様ID: PLT.1-WEB.1
対応設計書: docs/design/database/
実装内容: 全51テーブルのYAML定義とサンプルデータの整合性を包括的にチェック
"""

import os
import re
import yaml
import glob
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ColumnDefinition:
    """カラム定義クラス"""
    name: str
    type: str
    nullable: bool
    primary_key: bool = False
    unique: bool = False
    default: Optional[str] = None
    comment: str = ""

@dataclass
class ValidationIssue:
    """検証問題クラス"""
    table_name: str
    issue_type: str
    severity: str  # 'ERROR', 'WARNING', 'INFO'
    column_name: str = ""
    description: str = ""
    yaml_value: str = ""
    sample_value: str = ""
    suggestion: str = ""

class SampleDataConsistencyValidator:
    """サンプルデータ整合性検証クラス"""
    
    def __init__(self):
        self.yaml_dir = "docs/design/database/table-details"
        self.data_dir = "docs/design/database/data"
        self.issues: List[ValidationIssue] = []
        self.table_definitions: Dict[str, Dict] = {}
        self.sample_data: Dict[str, List[Dict]] = {}
        
    def load_yaml_definitions(self) -> None:
        """全YAMLファイルを読み込み"""
        print("📂 YAML定義ファイルを読み込み中...")
        
        yaml_files = glob.glob(f"{self.yaml_dir}/テーブル詳細定義YAML_*.yaml")
        
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'table_name' in data:
                        table_name = data['table_name']
                        self.table_definitions[table_name] = data
                        print(f"  ✅ {table_name}")
                    else:
                        print(f"  ❌ {yaml_file}: table_name が見つかりません")
            except Exception as e:
                print(f"  ❌ {yaml_file}: {str(e)}")
        
        print(f"📊 読み込み完了: {len(self.table_definitions)} テーブル")
    
    def load_sample_data(self) -> None:
        """全サンプルデータファイルを読み込み"""
        print("\n📂 サンプルデータファイルを読み込み中...")
        
        sql_files = glob.glob(f"{self.data_dir}/*_sample_data.sql")
        
        for sql_file in sql_files:
            try:
                table_name = os.path.basename(sql_file).replace('_sample_data.sql', '')
                
                with open(sql_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # INSERT文を解析
                insert_data = self.parse_insert_statements(content, table_name)
                if insert_data:
                    self.sample_data[table_name] = insert_data
                    print(f"  ✅ {table_name}: {len(insert_data)} レコード")
                else:
                    print(f"  ⚠️ {table_name}: INSERT文が見つかりません")
                    
            except Exception as e:
                print(f"  ❌ {sql_file}: {str(e)}")
        
        print(f"📊 読み込み完了: {len(self.sample_data)} テーブル")
    
    def parse_insert_statements(self, content: str, table_name: str) -> List[Dict]:
        """INSERT文を解析してデータを抽出"""
        insert_data = []
        
        # INSERT文のパターンを検索
        insert_pattern = rf"INSERT\s+INTO\s+{re.escape(table_name)}\s*\((.*?)\)\s*VALUES\s*\((.*?)\);"
        matches = re.findall(insert_pattern, content, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            columns_str, values_str = match
            
            # カラム名を抽出
            columns = [col.strip().strip('`"[]') for col in columns_str.split(',')]
            
            # 値を抽出（簡易的な解析）
            values = self.parse_values(values_str)
            
            if len(columns) == len(values):
                record = dict(zip(columns, values))
                insert_data.append(record)
        
        return insert_data
    
    def parse_values(self, values_str: str) -> List[str]:
        """VALUES句の値を解析"""
        values = []
        current_value = ""
        in_quotes = False
        quote_char = None
        
        i = 0
        while i < len(values_str):
            char = values_str[i]
            
            if not in_quotes:
                if char in ["'", '"']:
                    in_quotes = True
                    quote_char = char
                    current_value += char
                elif char == ',':
                    values.append(current_value.strip())
                    current_value = ""
                else:
                    current_value += char
            else:
                current_value += char
                if char == quote_char:
                    # エスケープされていない引用符の終了をチェック
                    if i == 0 or values_str[i-1] != '\\':
                        in_quotes = False
                        quote_char = None
            
            i += 1
        
        if current_value.strip():
            values.append(current_value.strip())
        
        return values
    
    def validate_table_existence(self) -> None:
        """テーブル存在整合性チェック"""
        print("\n🔍 テーブル存在整合性をチェック中...")
        
        yaml_tables = set(self.table_definitions.keys())
        sample_tables = set(self.sample_data.keys())
        
        # YAMLにあるがサンプルデータにないテーブル
        missing_sample = yaml_tables - sample_tables
        for table in missing_sample:
            self.issues.append(ValidationIssue(
                table_name=table,
                issue_type="MISSING_SAMPLE_DATA",
                severity="WARNING",
                description="サンプルデータファイルが存在しません",
                suggestion=f"{self.data_dir}/{table}_sample_data.sql を作成してください"
            ))
        
        # サンプルデータにあるがYAMLにないテーブル
        missing_yaml = sample_tables - yaml_tables
        for table in missing_yaml:
            self.issues.append(ValidationIssue(
                table_name=table,
                issue_type="MISSING_YAML_DEFINITION",
                severity="ERROR",
                description="YAML定義ファイルが存在しません",
                suggestion=f"{self.yaml_dir}/テーブル詳細定義YAML_{table}.yaml を作成してください"
            ))
        
        print(f"  📊 YAML定義: {len(yaml_tables)} テーブル")
        print(f"  📊 サンプルデータ: {len(sample_tables)} テーブル")
        print(f"  ⚠️ サンプルデータ不足: {len(missing_sample)} テーブル")
        print(f"  ❌ YAML定義不足: {len(missing_yaml)} テーブル")
    
    def validate_column_consistency(self) -> None:
        """カラム整合性チェック"""
        print("\n🔍 カラム整合性をチェック中...")
        
        common_tables = set(self.table_definitions.keys()) & set(self.sample_data.keys())
        
        for table_name in common_tables:
            yaml_def = self.table_definitions[table_name]
            sample_records = self.sample_data[table_name]
            
            if not sample_records:
                continue
            
            # YAML定義からカラム情報を取得
            yaml_columns = {}
            if 'columns' in yaml_def:
                for col in yaml_def['columns']:
                    yaml_columns[col['name']] = ColumnDefinition(
                        name=col['name'],
                        type=col.get('type', ''),
                        nullable=col.get('nullable', True),
                        primary_key=col.get('primary_key', False),
                        unique=col.get('unique', False),
                        default=col.get('default'),
                        comment=col.get('comment', '')
                    )
            
            # サンプルデータからカラム情報を取得
            sample_columns = set(sample_records[0].keys()) if sample_records else set()
            
            # カラム名の一致性チェック
            yaml_column_names = set(yaml_columns.keys())
            
            # YAMLにあるがサンプルデータにないカラム
            missing_in_sample = yaml_column_names - sample_columns
            for col_name in missing_in_sample:
                self.issues.append(ValidationIssue(
                    table_name=table_name,
                    issue_type="MISSING_COLUMN_IN_SAMPLE",
                    severity="ERROR",
                    column_name=col_name,
                    description="サンプルデータにカラムが存在しません",
                    yaml_value=col_name,
                    suggestion=f"サンプルデータに {col_name} カラムを追加してください"
                ))
            
            # サンプルデータにあるがYAMLにないカラム
            extra_in_sample = sample_columns - yaml_column_names
            for col_name in extra_in_sample:
                self.issues.append(ValidationIssue(
                    table_name=table_name,
                    issue_type="EXTRA_COLUMN_IN_SAMPLE",
                    severity="WARNING",
                    column_name=col_name,
                    description="YAML定義にないカラムがサンプルデータに存在します",
                    sample_value=col_name,
                    suggestion=f"YAML定義に {col_name} カラムを追加するか、サンプルデータから削除してください"
                ))
            
            # データ型・制約チェック
            self.validate_data_constraints(table_name, yaml_columns, sample_records)
        
        print(f"  📊 チェック完了: {len(common_tables)} テーブル")
    
    def validate_data_constraints(self, table_name: str, yaml_columns: Dict[str, ColumnDefinition], sample_records: List[Dict]) -> None:
        """データ型・制約チェック"""
        for record in sample_records:
            for col_name, value in record.items():
                if col_name not in yaml_columns:
                    continue
                
                col_def = yaml_columns[col_name]
                
                # NULL制約チェック
                if not col_def.nullable and (value is None or value in ['NULL', 'null', '']):
                    self.issues.append(ValidationIssue(
                        table_name=table_name,
                        issue_type="NULL_CONSTRAINT_VIOLATION",
                        severity="ERROR",
                        column_name=col_name,
                        description="NOT NULL制約に違反しています",
                        yaml_value=f"nullable: {col_def.nullable}",
                        sample_value=str(value),
                        suggestion=f"{col_name} に有効な値を設定してください"
                    ))
                
                # 文字列長チェック
                if value and value not in ['NULL', 'null']:
                    self.validate_string_length(table_name, col_name, col_def, str(value))
                
                # 数値範囲チェック
                if 'INTEGER' in col_def.type.upper() or 'DECIMAL' in col_def.type.upper():
                    self.validate_numeric_value(table_name, col_name, col_def, value)
    
    def validate_string_length(self, table_name: str, col_name: str, col_def: ColumnDefinition, value: str) -> None:
        """文字列長チェック"""
        # VARCHAR(n) の n を抽出
        varchar_match = re.search(r'VARCHAR\((\d+)\)', col_def.type.upper())
        if varchar_match:
            max_length = int(varchar_match.group(1))
            # クォートを除去して実際の文字列長をチェック
            actual_value = value.strip("'\"")
            if len(actual_value) > max_length:
                self.issues.append(ValidationIssue(
                    table_name=table_name,
                    issue_type="STRING_LENGTH_VIOLATION",
                    severity="ERROR",
                    column_name=col_name,
                    description=f"文字列長制限を超過しています（最大{max_length}文字）",
                    yaml_value=col_def.type,
                    sample_value=f"{actual_value} ({len(actual_value)}文字)",
                    suggestion=f"{col_name} の値を{max_length}文字以内に短縮してください"
                ))
    
    def validate_numeric_value(self, table_name: str, col_name: str, col_def: ColumnDefinition, value: str) -> None:
        """数値チェック"""
        if value in ['NULL', 'null', '']:
            return
        
        try:
            # クォートを除去
            clean_value = str(value).strip("'\"")
            
            if 'INTEGER' in col_def.type.upper():
                int(clean_value)
            elif 'DECIMAL' in col_def.type.upper() or 'NUMERIC' in col_def.type.upper():
                float(clean_value)
        except ValueError:
            self.issues.append(ValidationIssue(
                table_name=table_name,
                issue_type="INVALID_NUMERIC_VALUE",
                severity="ERROR",
                column_name=col_name,
                description="数値型に無効な値が設定されています",
                yaml_value=col_def.type,
                sample_value=str(value),
                suggestion=f"{col_name} に有効な数値を設定してください"
            ))
    
    def generate_report(self) -> str:
        """検証レポートを生成"""
        report = []
        report.append("=" * 80)
        report.append("📋 テーブル詳細定義YAML vs サンプルデータ 整合性チェック結果")
        report.append("=" * 80)
        report.append(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # サマリー
        total_issues = len(self.issues)
        error_count = len([i for i in self.issues if i.severity == 'ERROR'])
        warning_count = len([i for i in self.issues if i.severity == 'WARNING'])
        info_count = len([i for i in self.issues if i.severity == 'INFO'])
        
        report.append("📊 検証結果サマリー")
        report.append("-" * 40)
        report.append(f"対象テーブル数: {len(self.table_definitions)}")
        report.append(f"サンプルデータ数: {len(self.sample_data)}")
        report.append(f"総問題数: {total_issues}")
        report.append(f"  ❌ エラー: {error_count}")
        report.append(f"  ⚠️ 警告: {warning_count}")
        report.append(f"  ℹ️ 情報: {info_count}")
        report.append("")
        
        if total_issues == 0:
            report.append("🎉 問題は見つかりませんでした！")
            return "\n".join(report)
        
        # 問題種別サマリー
        issue_types = {}
        for issue in self.issues:
            issue_types[issue.issue_type] = issue_types.get(issue.issue_type, 0) + 1
        
        report.append("📈 問題種別サマリー")
        report.append("-" * 40)
        for issue_type, count in sorted(issue_types.items()):
            report.append(f"  {issue_type}: {count}件")
        report.append("")
        
        # テーブル別詳細レポート
        table_issues = {}
        for issue in self.issues:
            if issue.table_name not in table_issues:
                table_issues[issue.table_name] = []
            table_issues[issue.table_name].append(issue)
        
        report.append("📋 テーブル別詳細レポート")
        report.append("=" * 80)
        
        for table_name in sorted(table_issues.keys()):
            issues = table_issues[table_name]
            error_count = len([i for i in issues if i.severity == 'ERROR'])
            warning_count = len([i for i in issues if i.severity == 'WARNING'])
            
            status = "❌ 問題あり" if error_count > 0 else "⚠️ 警告あり"
            
            report.append(f"\n🏷️ テーブル: {table_name}")
            report.append(f"状態: {status}")
            report.append(f"問題数: {len(issues)}件 (エラー: {error_count}, 警告: {warning_count})")
            report.append("-" * 60)
            
            for i, issue in enumerate(issues, 1):
                severity_icon = {"ERROR": "❌", "WARNING": "⚠️", "INFO": "ℹ️"}[issue.severity]
                
                report.append(f"\n問題{i}: {severity_icon} {issue.issue_type}")
                if issue.column_name:
                    report.append(f"  カラム: {issue.column_name}")
                report.append(f"  説明: {issue.description}")
                if issue.yaml_value:
                    report.append(f"  YAML定義: {issue.yaml_value}")
                if issue.sample_value:
                    report.append(f"  サンプル値: {issue.sample_value}")
                if issue.suggestion:
                    report.append(f"  修正提案: {issue.suggestion}")
        
        return "\n".join(report)
    
    def run_validation(self) -> None:
        """整合性チェックを実行"""
        print("🚀 テーブル詳細定義YAML vs サンプルデータ 整合性チェック開始")
        print("=" * 80)
        
        # データ読み込み
        self.load_yaml_definitions()
        self.load_sample_data()
        
        # 検証実行
        self.validate_table_existence()
        self.validate_column_consistency()
        
        # レポート生成
        print("\n📋 検証レポートを生成中...")
        report = self.generate_report()
        
        # レポート保存
        report_file = f"sample_data_consistency_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ 検証完了！レポートを保存しました: {report_file}")
        print("\n" + "=" * 80)
        print("📋 検証結果サマリー")
        print("=" * 80)
        
        total_issues = len(self.issues)
        error_count = len([i for i in self.issues if i.severity == 'ERROR'])
        warning_count = len([i for i in self.issues if i.severity == 'WARNING'])
        
        print(f"総問題数: {total_issues}")
        print(f"  ❌ エラー: {error_count}")
        print(f"  ⚠️ 警告: {warning_count}")
        
        if total_issues == 0:
            print("\n🎉 すべてのテーブルで整合性が確認されました！")
        else:
            print(f"\n📄 詳細は {report_file} をご確認ください。")

def main():
    """メイン関数"""
    validator = SampleDataConsistencyValidator()
    validator.run_validation()

if __name__ == "__main__":
    main()
