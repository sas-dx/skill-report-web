"""
統一ユーティリティシステム

全ツールで共通のユーティリティ機能を提供
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import hashlib
import shutil

from .config import get_config
from .logger import get_logger
from .exceptions import FileNotFoundError, ParseError, ValidationError


logger = get_logger(__name__)


class FileUtils:
    """ファイル操作ユーティリティ"""
    
    @staticmethod
    def ensure_directory(path: str) -> None:
        """ディレクトリの存在を確保"""
        os.makedirs(path, exist_ok=True)
        logger.debug(f"ディレクトリを確保: {path}")
    
    @staticmethod
    def backup_file(file_path: str, backup_dir: Optional[str] = None) -> str:
        """ファイルをバックアップ"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        
        if backup_dir is None:
            config = get_config()
            backup_dir = config.get_backup_dir()
        
        FileUtils.ensure_directory(backup_dir)
        
        # バックアップファイル名生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        backup_filename = f"{filename}.backup.{timestamp}"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # ファイルコピー
        shutil.copy2(file_path, backup_path)
        logger.info(f"ファイルをバックアップ: {file_path} -> {backup_path}")
        
        return backup_path
    
    @staticmethod
    def get_file_hash(file_path: str) -> str:
        """ファイルのハッシュ値を取得"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        
        return hash_md5.hexdigest()
    
    @staticmethod
    def find_files(directory: str, pattern: str = "*", recursive: bool = True) -> List[str]:
        """ファイルを検索"""
        path = Path(directory)
        if not path.exists():
            return []
        
        if recursive:
            files = list(path.rglob(pattern))
        else:
            files = list(path.glob(pattern))
        
        return [str(f) for f in files if f.is_file()]
    
    @staticmethod
    def get_relative_path(file_path: str, base_path: str) -> str:
        """相対パスを取得"""
        return os.path.relpath(file_path, base_path)


class YamlUtils:
    """YAML操作ユーティリティ"""
    
    @staticmethod
    def load_yaml(file_path: str) -> Dict[str, Any]:
        """YAMLファイルを読み込み"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            logger.debug(f"YAMLファイルを読み込み: {file_path}")
            return data or {}
            
        except yaml.YAMLError as e:
            raise ParseError(f"YAML解析エラー: {str(e)}", file_path)
        except Exception as e:
            raise ParseError(f"ファイル読み込みエラー: {str(e)}", file_path)
    
    @staticmethod
    def save_yaml(data: Dict[str, Any], file_path: str, backup: bool = True) -> None:
        """YAMLファイルに保存"""
        # バックアップ作成
        if backup and os.path.exists(file_path):
            FileUtils.backup_file(file_path)
        
        # ディレクトリ作成
        FileUtils.ensure_directory(os.path.dirname(file_path))
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False, indent=2)
            
            logger.info(f"YAMLファイルを保存: {file_path}")
            
        except Exception as e:
            raise ParseError(f"ファイル保存エラー: {str(e)}", file_path)
    
    @staticmethod
    def validate_yaml_structure(data: Dict[str, Any], required_keys: List[str]) -> List[str]:
        """YAML構造の妥当性チェック"""
        errors = []
        
        for key in required_keys:
            if key not in data:
                errors.append(f"必須キー '{key}' が存在しません")
            elif data[key] is None:
                errors.append(f"キー '{key}' の値がNullです")
        
        return errors


class JsonUtils:
    """JSON操作ユーティリティ"""
    
    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """JSONファイルを読み込み"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.debug(f"JSONファイルを読み込み: {file_path}")
            return data
            
        except json.JSONDecodeError as e:
            raise ParseError(f"JSON解析エラー: {str(e)}", file_path)
        except Exception as e:
            raise ParseError(f"ファイル読み込みエラー: {str(e)}", file_path)
    
    @staticmethod
    def save_json(data: Dict[str, Any], file_path: str, backup: bool = True) -> None:
        """JSONファイルに保存"""
        # バックアップ作成
        if backup and os.path.exists(file_path):
            FileUtils.backup_file(file_path)
        
        # ディレクトリ作成
        FileUtils.ensure_directory(os.path.dirname(file_path))
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"JSONファイルを保存: {file_path}")
            
        except Exception as e:
            raise ParseError(f"ファイル保存エラー: {str(e)}", file_path)


class TextUtils:
    """テキスト操作ユーティリティ"""
    
    @staticmethod
    def normalize_table_name(name: str) -> str:
        """テーブル名を正規化"""
        # 大文字に変換し、不正な文字を除去
        normalized = ''.join(c for c in name.upper() if c.isalnum() or c == '_')
        
        # 先頭が数字の場合は T_ を付加
        if normalized and normalized[0].isdigit():
            normalized = f"T_{normalized}"
        
        return normalized
    
    @staticmethod
    def camel_to_snake(name: str) -> str:
        """キャメルケースをスネークケースに変換"""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @staticmethod
    def snake_to_camel(name: str) -> str:
        """スネークケースをキャメルケースに変換"""
        components = name.split('_')
        return components[0] + ''.join(x.capitalize() for x in components[1:])
    
    @staticmethod
    def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
        """テキストを指定長で切り詰め"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def format_sql_identifier(name: str) -> str:
        """SQL識別子をフォーマット"""
        # 予約語チェック（基本的なもの）
        reserved_words = {
            'SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE',
            'CREATE', 'DROP', 'ALTER', 'TABLE', 'INDEX', 'VIEW',
            'USER', 'ORDER', 'GROUP', 'HAVING', 'UNION', 'JOIN'
        }
        
        if name.upper() in reserved_words:
            return f'"{name}"'
        
        return name


class ValidationUtils:
    """バリデーションユーティリティ"""
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
        """必須フィールドの検証"""
        errors = []
        
        for field in required_fields:
            if field not in data:
                errors.append(f"必須フィールド '{field}' が存在しません")
            elif data[field] is None:
                errors.append(f"必須フィールド '{field}' がNullです")
            elif isinstance(data[field], str) and not data[field].strip():
                errors.append(f"必須フィールド '{field}' が空文字です")
        
        return errors
    
    @staticmethod
    def validate_data_type(value: Any, expected_type: type, field_name: str) -> Optional[str]:
        """データ型の検証"""
        if not isinstance(value, expected_type):
            return f"フィールド '{field_name}' の型が不正です。期待値: {expected_type.__name__}, 実際: {type(value).__name__}"
        return None
    
    @staticmethod
    def validate_string_length(value: str, min_length: int, max_length: int, field_name: str) -> Optional[str]:
        """文字列長の検証"""
        if len(value) < min_length:
            return f"フィールド '{field_name}' は{min_length}文字以上である必要があります"
        if len(value) > max_length:
            return f"フィールド '{field_name}' は{max_length}文字以下である必要があります"
        return None
    
    @staticmethod
    def validate_list_length(value: List[Any], min_length: int, field_name: str) -> Optional[str]:
        """リスト長の検証"""
        if len(value) < min_length:
            return f"フィールド '{field_name}' は{min_length}項目以上である必要があります"
        return None


class DateTimeUtils:
    """日時操作ユーティリティ"""
    
    @staticmethod
    def get_current_timestamp() -> str:
        """現在のタイムスタンプを取得"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def get_current_date() -> str:
        """現在の日付を取得"""
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """日時をフォーマット"""
        return dt.strftime(format_str)
    
    @staticmethod
    def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> datetime:
        """日付文字列をパース"""
        try:
            return datetime.strptime(date_str, format_str)
        except ValueError as e:
            raise ValidationError(f"日付形式が不正です: {date_str}", details={"format": format_str})


# 便利な関数をモジュールレベルで提供
def load_yaml(file_path: str) -> Dict[str, Any]:
    """YAMLファイルを読み込み（便利関数）"""
    return YamlUtils.load_yaml(file_path)


def save_yaml(data: Dict[str, Any], file_path: str, backup: bool = True) -> None:
    """YAMLファイルに保存（便利関数）"""
    YamlUtils.save_yaml(data, file_path, backup)


def ensure_directory(path: str) -> None:
    """ディレクトリの存在を確保（便利関数）"""
    FileUtils.ensure_directory(path)


def get_current_timestamp() -> str:
    """現在のタイムスタンプを取得（便利関数）"""
    return DateTimeUtils.get_current_timestamp()
