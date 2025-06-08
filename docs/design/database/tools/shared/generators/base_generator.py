"""
ベースジェネレータークラス
全てのジェネレーターの基底クラス

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from datetime import datetime

from ..core.models import TableDefinition
from ..core.exceptions import GenerationError


class BaseGenerator(ABC):
    """ベースジェネレータークラス"""
    
    def __init__(self, config=None):
        """
        初期化
        
        Args:
            config: 設定オブジェクト
        """
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_logging()
    
    def _setup_logging(self):
        """ログ設定のセットアップ"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    @abstractmethod
    def generate(self, table_def: TableDefinition, output_path: Optional[str] = None) -> str:
        """
        テーブル定義からファイルを生成
        
        Args:
            table_def: テーブル定義オブジェクト
            output_path: 出力ファイルパス（Noneの場合は文字列として返す）
            
        Returns:
            str: 生成された内容
            
        Raises:
            GenerationError: 生成エラー
        """
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """
        対応するファイル拡張子を取得
        
        Returns:
            str: ファイル拡張子（例: '.sql', '.md', '.yaml'）
        """
        pass
    
    def generate_to_file(self, table_def: TableDefinition, output_path: str) -> None:
        """
        テーブル定義からファイルを生成して保存
        
        Args:
            table_def: テーブル定義オブジェクト
            output_path: 出力ファイルパス
            
        Raises:
            GenerationError: 生成エラー
        """
        try:
            content = self.generate(table_def)
            
            # ディレクトリの作成
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # ファイルの書き込み
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"ファイルを生成しました: {output_path}")
            
        except Exception as e:
            raise GenerationError(f"ファイル生成エラー: {e}")
    
    def generate_multiple(self, table_defs: List[TableDefinition], output_dir: str) -> List[str]:
        """
        複数のテーブル定義からファイルを生成
        
        Args:
            table_defs: テーブル定義オブジェクトのリスト
            output_dir: 出力ディレクトリ
            
        Returns:
            List[str]: 生成されたファイルパスのリスト
            
        Raises:
            GenerationError: 生成エラー
        """
        generated_files = []
        output_path = Path(output_dir)
        
        for table_def in table_defs:
            try:
                filename = self._generate_filename(table_def)
                file_path = output_path / filename
                
                self.generate_to_file(table_def, str(file_path))
                generated_files.append(str(file_path))
                
            except Exception as e:
                self.logger.error(f"テーブル {table_def.name} の生成に失敗: {e}")
                raise GenerationError(f"複数ファイル生成エラー: {e}")
        
        return generated_files
    
    def _generate_filename(self, table_def: TableDefinition) -> str:
        """
        テーブル定義からファイル名を生成
        
        Args:
            table_def: テーブル定義オブジェクト
            
        Returns:
            str: ファイル名
        """
        extension = self.get_file_extension()
        return f"{table_def.name}{extension}"
    
    def _get_template_variables(self, table_def: TableDefinition) -> Dict[str, Any]:
        """
        テンプレート変数の取得
        
        Args:
            table_def: テーブル定義オブジェクト
            
        Returns:
            Dict[str, Any]: テンプレート変数
        """
        return {
            'table': table_def,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'config': self.config
        }
    
    def _log_generation_start(self, table_def: TableDefinition):
        """生成開始ログ"""
        self.logger.info(f"生成開始: {table_def.name} ({self.__class__.__name__})")
    
    def _log_generation_complete(self, table_def: TableDefinition):
        """生成完了ログ"""
        self.logger.info(f"生成完了: {table_def.name}")
    
    def _handle_generation_error(self, error: Exception, table_def: TableDefinition, context: str) -> GenerationError:
        """生成エラーのハンドリング"""
        error_msg = f"{context}: {table_def.name} - {str(error)}"
        self.logger.error(error_msg)
        return GenerationError(error_msg)


class GeneratorFactory:
    """ジェネレーターファクトリー"""
    
    _generators = {}
    
    @classmethod
    def register_generator(cls, extension: str, generator_class: type):
        """
        ジェネレーターを登録
        
        Args:
            extension: ファイル拡張子
            generator_class: ジェネレータークラス
        """
        cls._generators[extension] = generator_class
    
    @classmethod
    def create_generator(cls, extension: str, config=None) -> BaseGenerator:
        """
        ジェネレーターを作成
        
        Args:
            extension: ファイル拡張子
            config: 設定オブジェクト
            
        Returns:
            BaseGenerator: ジェネレーターインスタンス
            
        Raises:
            GenerationError: 未対応の拡張子
        """
        if extension not in cls._generators:
            raise GenerationError(f"未対応のファイル拡張子: {extension}")
        
        generator_class = cls._generators[extension]
        return generator_class(config)
    
    @classmethod
    def get_supported_extensions(cls) -> List[str]:
        """
        対応している拡張子のリストを取得
        
        Returns:
            List[str]: 拡張子のリスト
        """
        return list(cls._generators.keys())
    
    @classmethod
    def create_all_generators(cls, config=None) -> Dict[str, BaseGenerator]:
        """
        全てのジェネレーターを作成
        
        Args:
            config: 設定オブジェクト
            
        Returns:
            Dict[str, BaseGenerator]: 拡張子をキーとするジェネレーター辞書
        """
        generators = {}
        for extension in cls._generators:
            generators[extension] = cls.create_generator(extension, config)
        return generators


# 便利関数
def generate_file(table_def: TableDefinition, output_path: str, config=None) -> None:
    """
    テーブル定義からファイルを生成する便利関数
    
    Args:
        table_def: テーブル定義オブジェクト
        output_path: 出力ファイルパス
        config: 設定オブジェクト
        
    Raises:
        GenerationError: 生成エラー
    """
    extension = Path(output_path).suffix
    generator = GeneratorFactory.create_generator(extension, config)
    generator.generate_to_file(table_def, output_path)


def generate_multiple_files(table_defs: List[TableDefinition], output_dir: str, 
                          extensions: List[str], config=None) -> Dict[str, List[str]]:
    """
    複数のテーブル定義から複数形式のファイルを生成する便利関数
    
    Args:
        table_defs: テーブル定義オブジェクトのリスト
        output_dir: 出力ディレクトリ
        extensions: 生成する拡張子のリスト
        config: 設定オブジェクト
        
    Returns:
        Dict[str, List[str]]: 拡張子をキーとする生成ファイルパスのリスト
        
    Raises:
        GenerationError: 生成エラー
    """
    results = {}
    
    for extension in extensions:
        generator = GeneratorFactory.create_generator(extension, config)
        
        # 拡張子別のサブディレクトリを作成
        sub_dir = Path(output_dir) / extension.lstrip('.')
        generated_files = generator.generate_multiple(table_defs, str(sub_dir))
        results[extension] = generated_files
    
    return results
