"""
統合パーサー基底クラス
データベースツール統合における統一解析基盤

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict, Union
from pathlib import Path

from ..core.models import TableDefinition, CheckResult
from ..core.exceptions import ParsingError, ValidationError
from ..core.logger import get_logger


class BaseParser(ABC):
    """統合パーサー基底クラス"""
    
    def __init__(self, config=None):
        """
        パーサー初期化
        
        Args:
            config: 統合設定オブジェクト
        """
        self.config = config
        self.logger = get_logger(self.__class__.__name__)
        self._validation_enabled = True
        self._strict_mode = False
    
    @abstractmethod
    def parse(self, source: Any) -> Union[TableDefinition, List[TableDefinition]]:
        """
        解析実行（抽象メソッド）
        
        Args:
            source: 解析対象（ファイルパス、文字列、辞書等）
            
        Returns:
            解析結果（TableDefinition または そのリスト）
            
        Raises:
            ParsingError: 解析エラー
        """
        pass
    
    def validate(self, result: Union[TableDefinition, List[TableDefinition]]) -> List[CheckResult]:
        """
        解析結果の検証
        
        Args:
            result: 解析結果
            
        Returns:
            検証結果リスト
        """
        if not self._validation_enabled:
            return []
        
        validation_results = []
        
        # 単一テーブルの場合はリストに変換
        tables = result if isinstance(result, list) else [result]
        
        for table in tables:
            validation_results.extend(self._validate_table(table))
        
        return validation_results
    
    def _validate_table(self, table: TableDefinition) -> List[CheckResult]:
        """
        個別テーブルの検証
        
        Args:
            table: テーブル定義
            
        Returns:
            検証結果リスト
        """
        results = []
        
        # 基本的な検証
        if not table.name:
            results.append(CheckResult(
                check_type="table_validation",
                status="error",
                message="テーブル名が設定されていません",
                details={"table": table.name}
            ))
        
        if not table.columns:
            results.append(CheckResult(
                check_type="table_validation", 
                status="error",
                message="カラムが定義されていません",
                details={"table": table.name}
            ))
        
        # カラム検証
        primary_key_count = 0
        for column in table.columns:
            column_results = self._validate_column(column, table.name)
            results.extend(column_results)
            
            if column.primary_key:
                primary_key_count += 1
        
        # プライマリキー検証
        if primary_key_count == 0:
            results.append(CheckResult(
                check_type="table_validation",
                status="warning", 
                message="プライマリキーが定義されていません",
                details={"table": table.name}
            ))
        elif primary_key_count > 1:
            results.append(CheckResult(
                check_type="table_validation",
                status="warning",
                message="複数のプライマリキーが定義されています",
                details={"table": table.name, "primary_key_count": primary_key_count}
            ))
        
        return results
    
    def _validate_column(self, column, table_name: str) -> List[CheckResult]:
        """
        個別カラムの検証
        
        Args:
            column: カラム定義
            table_name: テーブル名
            
        Returns:
            検証結果リスト
        """
        results = []
        
        # カラム名検証
        if not column.name:
            results.append(CheckResult(
                check_type="column_validation",
                status="error",
                message="カラム名が設定されていません",
                details={"table": table_name}
            ))
        
        # データ型検証
        if not column.type:
            results.append(CheckResult(
                check_type="column_validation",
                status="error", 
                message="データ型が設定されていません",
                details={"table": table_name, "column": column.name}
            ))
        
        # 命名規則検証（設定がある場合）
        if self.config and hasattr(self.config, 'naming_rules'):
            naming_results = self._validate_naming_rules(column, table_name)
            results.extend(naming_results)
        
        return results
    
    def _validate_naming_rules(self, column, table_name: str) -> List[CheckResult]:
        """
        命名規則検証
        
        Args:
            column: カラム定義
            table_name: テーブル名
            
        Returns:
            検証結果リスト
        """
        results = []
        
        # 実装例：スネークケース検証
        if column.name and not column.name.islower():
            results.append(CheckResult(
                check_type="naming_validation",
                status="warning",
                message="カラム名は小文字で記述することを推奨します",
                details={"table": table_name, "column": column.name}
            ))
        
        return results
    
    def set_validation_enabled(self, enabled: bool):
        """検証の有効/無効設定"""
        self._validation_enabled = enabled
    
    def set_strict_mode(self, strict: bool):
        """厳密モードの設定"""
        self._strict_mode = strict
    
    def _handle_parsing_error(self, error: Exception, source: Any, context: str = "") -> ParsingError:
        """
        解析エラーのハンドリング
        
        Args:
            error: 元の例外
            source: 解析対象
            context: エラーコンテキスト
            
        Returns:
            ParsingError
        """
        source_info = str(source)
        if isinstance(source, Path):
            source_info = str(source.absolute())
        
        message = f"解析エラーが発生しました: {str(error)}"
        if context:
            message = f"{context}: {message}"
        
        return ParsingError(
            message=message,
            parser_type=self.__class__.__name__,
            file_path=source_info if isinstance(source, (str, Path)) else None,
            details={"original_error": str(error), "source": source_info}
        )
    
    def _log_parsing_start(self, source: Any):
        """解析開始ログ"""
        self.logger.info(f"解析開始: {source}")
    
    def _log_parsing_complete(self, source: Any, result_count: int):
        """解析完了ログ"""
        self.logger.info(f"解析完了: {source} (結果: {result_count}件)")
    
    def _log_validation_results(self, results: List[CheckResult]):
        """検証結果ログ"""
        if not results:
            self.logger.debug("検証結果: 問題なし")
            return
        
        error_count = sum(1 for r in results if r.status == "error")
        warning_count = sum(1 for r in results if r.status == "warning")
        
        self.logger.info(f"検証結果: エラー {error_count}件, 警告 {warning_count}件")
        
        for result in results:
            if result.status == "error":
                self.logger.error(f"検証エラー: {result.message}")
            elif result.status == "warning":
                self.logger.warning(f"検証警告: {result.message}")


class ParserFactory:
    """パーサーファクトリー"""
    
    _parsers = {}
    
    @classmethod
    def register_parser(cls, file_extension: str, parser_class):
        """パーサーを登録"""
        cls._parsers[file_extension.lower()] = parser_class
    
    @classmethod
    def create_parser(cls, file_path: Union[str, Path], config=None) -> BaseParser:
        """
        ファイル拡張子に基づいてパーサーを作成
        
        Args:
            file_path: ファイルパス
            config: 設定オブジェクト
            
        Returns:
            適切なパーサーインスタンス
            
        Raises:
            ParsingError: 対応するパーサーが見つからない場合
        """
        path = Path(file_path)
        extension = path.suffix.lower()
        
        if extension not in cls._parsers:
            raise ParsingError(
                f"拡張子 '{extension}' に対応するパーサーが見つかりません",
                file_path=str(path),
                details={"supported_extensions": list(cls._parsers.keys())}
            )
        
        parser_class = cls._parsers[extension]
        return parser_class(config)
    
    @classmethod
    def get_supported_extensions(cls) -> List[str]:
        """サポートされている拡張子一覧を取得"""
        return list(cls._parsers.keys())


# 共通ユーティリティ関数
def parse_file(file_path: Union[str, Path], config=None, validate: bool = True) -> Union[TableDefinition, List[TableDefinition]]:
    """
    ファイルを解析する便利関数
    
    Args:
        file_path: ファイルパス
        config: 設定オブジェクト
        validate: 検証を実行するかどうか
        
    Returns:
        解析結果
        
    Raises:
        ParsingError: 解析エラー
    """
    parser = ParserFactory.create_parser(file_path, config)
    parser.set_validation_enabled(validate)
    
    result = parser.parse(file_path)
    
    if validate:
        validation_results = parser.validate(result)
        error_results = [r for r in validation_results if r.status == "error"]
        
        if error_results:
            error_messages = [r.message for r in error_results]
            raise ValidationError(
                f"検証エラーが発生しました: {'; '.join(error_messages)}",
                details={"validation_errors": error_results}
            )
    
    return result
