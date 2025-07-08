"""
サンプルデータジェネレーター

TableDefinitionからサンプルデータを生成する
"""

from typing import Dict, List, Any, Optional
import logging
import random
from datetime import datetime, timedelta
from faker import Faker

from ..core.models import TableDefinition, ColumnDefinition

logger = logging.getLogger(__name__)


class SampleDataGenerator:
    """サンプルデータジェネレーター"""
    
    def __init__(self):
        """初期化"""
        self.fake = Faker('ja_JP')  # 日本語ロケール
        
        # データ型別のサンプルデータ生成ルール
        self.data_generators = {
            'VARCHAR': self._generate_varchar,
            'TEXT': self._generate_text,
            'INTEGER': self._generate_integer,
            'BIGINT': self._generate_bigint,
            'SMALLINT': self._generate_smallint,
            'BOOLEAN': self._generate_boolean,
            'TIMESTAMP': self._generate_timestamp,
            'DATE': self._generate_date,
            'TIME': self._generate_time,
            'DECIMAL': self._generate_decimal,
            'NUMERIC': self._generate_decimal,
            'FLOAT': self._generate_float,
            'REAL': self._generate_float,
            'DOUBLE': self._generate_float,
            'SERIAL': self._generate_serial,
            'BIGSERIAL': self._generate_bigserial
        }
        
        # カラム名に基づく特別なデータ生成ルール
        self.column_name_generators = {
            'name': lambda: self.fake.name(),
            'email': lambda: self.fake.email(),
            'phone': lambda: self.fake.phone_number(),
            'address': lambda: self.fake.address(),
            'company': lambda: self.fake.company(),
            'department': lambda: random.choice(['開発部', '営業部', '総務部', '人事部', '経理部']),
            'position': lambda: random.choice(['部長', '課長', '主任', '一般', 'アルバイト']),
            'skill_name': lambda: random.choice(['Java', 'Python', 'JavaScript', 'React', 'Vue.js', 'Angular', 'Node.js', 'Spring Boot']),
            'skill_level': lambda: random.randint(1, 4),
            'tenant_id': lambda: f"tenant_{random.randint(1, 5):03d}",
            'emp_no': lambda: f"EMP{random.randint(1, 9999):04d}",
            'user_id': lambda: f"user_{random.randint(1, 1000):03d}",
            'password': lambda: self.fake.password(),
            'status': lambda: random.choice(['active', 'inactive', 'pending']),
            'created_at': lambda: self.fake.date_time_between(start_date='-1y', end_date='now'),
            'updated_at': lambda: self.fake.date_time_between(start_date='-30d', end_date='now'),
            'is_deleted': lambda: random.choice([True, False]),
            'version': lambda: random.randint(1, 10)
        }
        
        # シーケンス管理
        self.sequences = {}
    
    def generate(self, table_definition: TableDefinition, 
                record_count: int = 10) -> str:
        """
        テーブル定義からサンプルデータのINSERT文を生成
        
        Args:
            table_definition: テーブル定義
            record_count: 生成するレコード数
            
        Returns:
            str: INSERT文
        """
        try:
            lines = []
            
            # ヘッダーコメント
            lines.append(f"-- {table_definition.table_name} サンプルデータ")
            lines.append(f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append(f"-- レコード数: {record_count}")
            lines.append("")
            
            # カラム名リスト
            column_names = [col.name for col in table_definition.columns]
            columns_str = ", ".join(column_names)
            
            # INSERT文の開始
            lines.append(f"INSERT INTO {table_definition.table_name} ({columns_str}) VALUES")
            
            # データ生成
            values_list = []
            for i in range(record_count):
                values = []
                for column in table_definition.columns:
                    value = self._generate_column_value(column, i)
                    values.append(value)
                
                values_str = ", ".join(str(v) for v in values)
                values_list.append(f"  ({values_str})")
            
            # VALUES句を結合
            lines.append(",\n".join(values_list) + ";")
            lines.append("")
            
            return "\n".join(lines)
            
        except Exception as e:
            logger.error(f"サンプルデータ生成エラー: {e}")
            raise
    
    def _generate_column_value(self, column: ColumnDefinition, record_index: int) -> Any:
        """
        カラムの値を生成
        
        Args:
            column: カラム定義
            record_index: レコードインデックス
            
        Returns:
            Any: 生成された値
        """
        try:
            # NULL値の処理
            if column.nullable and random.random() < 0.1:  # 10%の確率でNULL
                return 'NULL'
            
            # デフォルト値がある場合
            if column.default and random.random() < 0.2:  # 20%の確率でデフォルト値
                return f"'{column.default}'"
            
            # カラム名に基づく特別な生成ルール
            column_name_lower = column.name.lower()
            for pattern, generator in self.column_name_generators.items():
                if pattern in column_name_lower:
                    value = generator()
                    return self._format_value(value, column.type)
            
            # データ型に基づく生成
            base_type = self._extract_base_type(column.type)
            if base_type in self.data_generators:
                value = self.data_generators[base_type](column, record_index)
                return self._format_value(value, column.type)
            
            # デフォルト値
            return "'sample_value'"
            
        except Exception as e:
            logger.error(f"カラム値生成エラー: {column.name}, {e}")
            return "'error_value'"
    
    def _extract_base_type(self, data_type: str) -> str:
        """データ型からベース型を抽出"""
        if '(' in data_type:
            return data_type.split('(')[0].upper()
        return data_type.upper()
    
    def _format_value(self, value: Any, data_type: str) -> str:
        """値をSQL形式にフォーマット"""
        if value is None or value == 'NULL':
            return 'NULL'
        
        base_type = self._extract_base_type(data_type)
        
        # 文字列型
        if base_type in ['VARCHAR', 'TEXT', 'CHAR']:
            escaped_value = str(value).replace("'", "''")
            return f"'{escaped_value}'"
        
        # 日時型
        elif base_type in ['TIMESTAMP', 'DATE', 'TIME']:
            return f"'{value}'"
        
        # 数値型・ブール型
        else:
            return str(value)
    
    # データ型別生成メソッド
    
    def _generate_varchar(self, column: ColumnDefinition, record_index: int) -> str:
        """VARCHAR型の値を生成"""
        # 長さ制限を取得
        max_length = self._extract_length(column.type, 50)
        text = self.fake.text(max_nb_chars=max_length)
        return text[:max_length]
    
    def _generate_text(self, column: ColumnDefinition, record_index: int) -> str:
        """TEXT型の値を生成"""
        return self.fake.text(max_nb_chars=200)
    
    def _generate_integer(self, column: ColumnDefinition, record_index: int) -> int:
        """INTEGER型の値を生成"""
        if column.primary_key:
            return record_index + 1
        return random.randint(1, 1000000)
    
    def _generate_bigint(self, column: ColumnDefinition, record_index: int) -> int:
        """BIGINT型の値を生成"""
        if column.primary_key:
            return record_index + 1
        return random.randint(1, 9223372036854775807)
    
    def _generate_smallint(self, column: ColumnDefinition, record_index: int) -> int:
        """SMALLINT型の値を生成"""
        return random.randint(1, 32767)
    
    def _generate_boolean(self, column: ColumnDefinition, record_index: int) -> bool:
        """BOOLEAN型の値を生成"""
        return random.choice([True, False])
    
    def _generate_timestamp(self, column: ColumnDefinition, record_index: int) -> datetime:
        """TIMESTAMP型の値を生成"""
        return self.fake.date_time_between(start_date='-1y', end_date='now')
    
    def _generate_date(self, column: ColumnDefinition, record_index: int) -> str:
        """DATE型の値を生成"""
        return self.fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
    
    def _generate_time(self, column: ColumnDefinition, record_index: int) -> str:
        """TIME型の値を生成"""
        return self.fake.time()
    
    def _generate_decimal(self, column: ColumnDefinition, record_index: int) -> float:
        """DECIMAL/NUMERIC型の値を生成"""
        precision, scale = self._extract_precision_scale(column.type, 10, 2)
        max_value = 10 ** (precision - scale) - 1
        return round(random.uniform(0, max_value), scale)
    
    def _generate_float(self, column: ColumnDefinition, record_index: int) -> float:
        """FLOAT/REAL/DOUBLE型の値を生成"""
        return round(random.uniform(0, 1000000), 2)
    
    def _generate_serial(self, column: ColumnDefinition, record_index: int) -> int:
        """SERIAL型の値を生成"""
        sequence_name = f"{column.name}_seq"
        if sequence_name not in self.sequences:
            self.sequences[sequence_name] = 0
        self.sequences[sequence_name] += 1
        return self.sequences[sequence_name]
    
    def _generate_bigserial(self, column: ColumnDefinition, record_index: int) -> int:
        """BIGSERIAL型の値を生成"""
        sequence_name = f"{column.name}_seq"
        if sequence_name not in self.sequences:
            self.sequences[sequence_name] = 0
        self.sequences[sequence_name] += 1
        return self.sequences[sequence_name]
    
    # ヘルパーメソッド
    
    def _extract_length(self, data_type: str, default: int = 50) -> int:
        """データ型から長さを抽出"""
        try:
            if '(' in data_type:
                length_str = data_type.split('(')[1].split(')')[0]
                return int(length_str)
            return default
        except:
            return default
    
    def _extract_precision_scale(self, data_type: str, default_precision: int = 10, 
                                default_scale: int = 2) -> tuple:
        """データ型から精度とスケールを抽出"""
        try:
            if '(' in data_type:
                params = data_type.split('(')[1].split(')')[0]
                if ',' in params:
                    precision, scale = params.split(',')
                    return int(precision.strip()), int(scale.strip())
                else:
                    return int(params.strip()), 0
            return default_precision, default_scale
        except:
            return default_precision, default_scale
