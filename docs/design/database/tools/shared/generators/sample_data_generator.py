"""
サンプルデータジェネレーター
テーブル定義からサンプルデータ（SQL INSERT文）を生成する機能

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

from typing import List, Optional, Any, Dict
from datetime import datetime, date, timedelta
import random
import uuid

from .base_generator import BaseGenerator
from ..core.models import TableDefinition, ColumnDefinition


class SampleDataGenerator(BaseGenerator):
    """サンプルデータジェネレーター"""
    
    def __init__(self, config=None):
        super().__init__(config)
        self.sample_count = self.config.get('sample_count', 5)
        self.include_header = self.config.get('include_header', True)
        self.use_realistic_data = self.config.get('use_realistic_data', True)
        self.tenant_id = self.config.get('tenant_id', 'tenant001')
        
        # サンプルデータのパターン
        self._init_sample_patterns()
    
    def _init_sample_patterns(self):
        """サンプルデータパターンの初期化"""
        self.sample_names = [
            '山田太郎', '佐藤花子', '田中一郎', '鈴木美咲', '高橋健太',
            '渡辺由美', '伊藤誠', '中村麻衣', '小林大輔', '加藤愛子'
        ]
        
        self.sample_emails = [
            'yamada@example.com', 'sato@example.com', 'tanaka@example.com',
            'suzuki@example.com', 'takahashi@example.com', 'watanabe@example.com',
            'ito@example.com', 'nakamura@example.com', 'kobayashi@example.com', 'kato@example.com'
        ]
        
        self.sample_departments = [
            '開発部', '営業部', '総務部', '人事部', '経理部', 'マーケティング部'
        ]
        
        self.sample_skills = [
            'Java', 'Python', 'JavaScript', 'TypeScript', 'React', 'Vue.js',
            'Node.js', 'Spring Boot', 'Django', 'PostgreSQL', 'MySQL', 'AWS'
        ]
        
        self.sample_companies = [
            'ABC株式会社', 'XYZ商事', 'テクノロジー企業', 'システム開発会社'
        ]
    
    def generate(self, table_def: TableDefinition, output_path: Optional[str] = None) -> str:
        """
        テーブル定義からサンプルデータを生成
        
        Args:
            table_def: テーブル定義オブジェクト
            output_path: 出力ファイルパス（未使用）
            
        Returns:
            str: 生成されたサンプルデータSQL
        """
        self._log_generation_start(table_def)
        
        try:
            sql_parts = []
            
            # ヘッダーコメント
            if self.include_header:
                sql_parts.append(self._generate_header_comment(table_def))
            
            # INSERT文の生成
            insert_sql = self._generate_insert_statements(table_def)
            sql_parts.append(insert_sql)
            
            sql_content = '\n\n'.join(filter(None, sql_parts))
            
            self._log_generation_complete(table_def)
            return sql_content
            
        except Exception as e:
            raise self._handle_generation_error(e, table_def, "サンプルデータ生成エラー")
    
    def get_file_extension(self) -> str:
        """ファイル拡張子を取得"""
        return '_sample_data.sql'
    
    def _generate_header_comment(self, table_def: TableDefinition) -> str:
        """ヘッダーコメントの生成"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        lines = [
            "-- " + "=" * 70,
            f"-- サンプルデータ: {table_def.name}",
            f"-- 論理名: {table_def.logical_name}",
            f"-- 生成件数: {self.sample_count}件",
            f"-- 生成日時: {timestamp}",
            "-- " + "=" * 70,
            "",
            "-- 注意: このファイルはサンプルデータです。",
            "-- 本番環境では使用しないでください。"
        ]
        
        return '\n'.join(lines)
    
    def _generate_insert_statements(self, table_def: TableDefinition) -> str:
        """INSERT文の生成"""
        lines = [
            f"-- {table_def.name} サンプルデータ挿入",
            f"INSERT INTO {table_def.name} ("
        ]
        
        # カラム名リスト（AUTO_INCREMENTカラムを除く）
        insert_columns = [col for col in table_def.columns if not col.auto_increment]
        column_names = [col.name for col in insert_columns]
        
        lines.append("    " + ",\n    ".join(column_names))
        lines.append(") VALUES")
        
        # サンプルデータ行の生成
        value_rows = []
        for i in range(self.sample_count):
            row_values = self._generate_sample_row(table_def, insert_columns, i)
            value_rows.append(f"    ({', '.join(row_values)})")
        
        lines.append(",\n".join(value_rows) + ";")
        
        return '\n'.join(lines)
    
    def _generate_sample_row(self, table_def: TableDefinition, columns: List[ColumnDefinition], row_index: int) -> List[str]:
        """サンプルデータ行の生成"""
        values = []
        
        for column in columns:
            value = self._generate_column_value(table_def, column, row_index)
            values.append(value)
        
        return values
    
    def _generate_column_value(self, table_def: TableDefinition, column: ColumnDefinition, row_index: int) -> str:
        """カラム値の生成"""
        # デフォルト値がある場合
        if column.default is not None:
            if isinstance(column.default, str):
                if column.default.upper() in ['CURRENT_TIMESTAMP', 'NOW()']:
                    return "CURRENT_TIMESTAMP"
                else:
                    return f"'{column.default}'"
            else:
                return str(column.default)
        
        # NULL許可の場合、一部をNULLにする
        if column.nullable and random.random() < 0.1:  # 10%の確率でNULL
            return "NULL"
        
        # データ型に基づく値生成
        return self._generate_value_by_type(table_def, column, row_index)
    
    def _generate_value_by_type(self, table_def: TableDefinition, column: ColumnDefinition, row_index: int) -> str:
        """データ型に基づく値生成"""
        column_name = column.name.lower()
        data_type = column.type.upper()
        
        # 特定のカラム名パターンに基づく生成
        if 'tenant_id' in column_name:
            return f"'{self.tenant_id}'"
        elif 'id' in column_name and column.primary_key:
            return f"'{uuid.uuid4()}'"
        elif 'emp_no' in column_name or 'employee_no' in column_name:
            return f"'EMP{str(row_index + 1).zfill(3)}'"
        elif 'name' in column_name and 'file' not in column_name:
            return f"'{self.sample_names[row_index % len(self.sample_names)]}'"
        elif 'email' in column_name:
            return f"'{self.sample_emails[row_index % len(self.sample_emails)]}'"
        elif 'department' in column_name or 'dept' in column_name:
            return f"'{self.sample_departments[row_index % len(self.sample_departments)]}'"
        elif 'skill' in column_name and 'name' in column_name:
            return f"'{self.sample_skills[row_index % len(self.sample_skills)]}'"
        elif 'company' in column_name:
            return f"'{self.sample_companies[row_index % len(self.sample_companies)]}'"
        elif 'level' in column_name:
            return str(random.randint(1, 4))
        elif 'status' in column_name:
            statuses = ['active', 'inactive', 'pending']
            return f"'{statuses[row_index % len(statuses)]}'"
        elif 'created_at' in column_name or 'updated_at' in column_name:
            return "CURRENT_TIMESTAMP"
        elif 'is_deleted' in column_name or 'deleted' in column_name:
            return 'false'
        elif 'version' in column_name:
            return '1'
        
        # データ型に基づく生成
        if 'VARCHAR' in data_type or 'TEXT' in data_type or 'CHAR' in data_type:
            return self._generate_string_value(column, row_index)
        elif 'INT' in data_type or 'SERIAL' in data_type:
            return self._generate_integer_value(column, row_index)
        elif 'DECIMAL' in data_type or 'NUMERIC' in data_type or 'FLOAT' in data_type:
            return self._generate_decimal_value(column, row_index)
        elif 'BOOLEAN' in data_type or 'BOOL' in data_type:
            return 'true' if row_index % 2 == 0 else 'false'
        elif 'DATE' in data_type:
            return self._generate_date_value(column, row_index)
        elif 'TIMESTAMP' in data_type or 'DATETIME' in data_type:
            return "CURRENT_TIMESTAMP"
        elif 'UUID' in data_type:
            return f"'{uuid.uuid4()}'"
        else:
            # 不明な型の場合はデフォルト文字列
            return f"'sample_value_{row_index + 1}'"
    
    def _generate_string_value(self, column: ColumnDefinition, row_index: int) -> str:
        """文字列値の生成"""
        # 長さ制限の取得
        max_length = self._extract_length_from_type(column.type)
        
        base_value = f"sample_text_{row_index + 1}"
        
        # 長さ制限がある場合は調整
        if max_length and len(base_value) > max_length:
            base_value = base_value[:max_length-3] + "..."
        
        return f"'{base_value}'"
    
    def _generate_integer_value(self, column: ColumnDefinition, row_index: int) -> str:
        """整数値の生成"""
        if 'level' in column.name.lower():
            return str(random.randint(1, 4))
        elif 'version' in column.name.lower():
            return '1'
        elif 'count' in column.name.lower():
            return str(random.randint(0, 100))
        else:
            return str(row_index + 1)
    
    def _generate_decimal_value(self, column: ColumnDefinition, row_index: int) -> str:
        """小数値の生成"""
        if 'rate' in column.name.lower() or 'ratio' in column.name.lower():
            return str(round(random.uniform(0.0, 1.0), 2))
        elif 'price' in column.name.lower() or 'amount' in column.name.lower():
            return str(round(random.uniform(100.0, 10000.0), 2))
        else:
            return str(round(random.uniform(1.0, 100.0), 2))
    
    def _generate_date_value(self, column: ColumnDefinition, row_index: int) -> str:
        """日付値の生成"""
        base_date = date.today()
        
        if 'birth' in column.name.lower():
            # 生年月日は20-60歳の範囲
            years_ago = random.randint(20, 60)
            birth_date = base_date - timedelta(days=years_ago * 365)
            return f"'{birth_date}'"
        elif 'start' in column.name.lower() or 'join' in column.name.lower():
            # 開始日・入社日は過去1-10年
            days_ago = random.randint(365, 3650)
            start_date = base_date - timedelta(days=days_ago)
            return f"'{start_date}'"
        else:
            # その他は過去1年以内
            days_ago = random.randint(0, 365)
            sample_date = base_date - timedelta(days=days_ago)
            return f"'{sample_date}'"
    
    def _extract_length_from_type(self, data_type: str) -> Optional[int]:
        """データ型から長さ制限を抽出"""
        import re
        match = re.search(r'\((\d+)\)', data_type)
        return int(match.group(1)) if match else None
    
    def _generate_filename(self, table_def: TableDefinition) -> str:
        """ファイル名の生成（オーバーライド）"""
        return f"{table_def.name}_sample_data.sql"


# ジェネレーターファクトリーへの登録
from .base_generator import GeneratorFactory
GeneratorFactory.register_generator('_sample_data.sql', SampleDataGenerator)


# 便利関数
def generate_sample_data(table_def: TableDefinition, config=None) -> str:
    """
    テーブル定義からサンプルデータを生成する便利関数
    
    Args:
        table_def: テーブル定義オブジェクト
        config: 設定オブジェクト
        
    Returns:
        str: 生成されたサンプルデータSQL
    """
    generator = SampleDataGenerator(config)
    return generator.generate(table_def)


def generate_sample_data_file(table_def: TableDefinition, output_path: str, config=None) -> None:
    """
    テーブル定義からサンプルデータファイルを生成する便利関数
    
    Args:
        table_def: テーブル定義オブジェクト
        output_path: 出力ファイルパス
        config: 設定オブジェクト
    """
    generator = SampleDataGenerator(config)
    generator.generate_to_file(table_def, output_path)


def generate_realistic_sample_data(table_def: TableDefinition, sample_count: int = 10, 
                                 tenant_id: str = 'tenant001') -> str:
    """
    リアルなサンプルデータを生成する便利関数
    
    Args:
        table_def: テーブル定義オブジェクト
        sample_count: サンプル件数
        tenant_id: テナントID
        
    Returns:
        str: 生成されたサンプルデータSQL
    """
    config = {
        'sample_count': sample_count,
        'use_realistic_data': True,
        'tenant_id': tenant_id,
        'include_header': True
    }
    
    generator = SampleDataGenerator(config)
    return generator.generate(table_def)
