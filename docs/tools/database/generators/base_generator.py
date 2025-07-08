"""
ベースジェネレーター

全てのジェネレーターの基底クラス
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path
import os

from ..core import Logger, ValidationResult, GenerationError


class BaseGenerator(ABC):
    """ジェネレーターの基底クラス"""
    
    def __init__(self, generator_type: str):
        """
        初期化
        
        Args:
            generator_type: ジェネレーターのタイプ
        """
        self.generator_type = generator_type
        self.logger = Logger.get_logger(f"generator.{generator_type}")
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """
        サポートする出力形式のリストを返す
        
        Returns:
            サポートする形式のリスト
        """
        pass
    
    @abstractmethod
    def generate(self, data: Dict[str, Any], output_path: str, **kwargs) -> bool:
        """
        データから出力ファイルを生成
        
        Args:
            data: 生成元データ
            output_path: 出力ファイルパス
            **kwargs: 追加オプション
            
        Returns:
            生成成功フラグ
            
        Raises:
            GenerationError: 生成エラー
        """
        pass
    
    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> ValidationResult:
        """
        生成用データの妥当性を検証
        
        Args:
            data: 検証対象データ
            
        Returns:
            検証結果
        """
        pass
    
    def _validate_output_path(self, output_path: str) -> None:
        """
        出力パスの妥当性を検証
        
        Args:
            output_path: 出力ファイルパス
            
        Raises:
            GenerationError: パス検証エラー
        """
        if not output_path:
            raise GenerationError("出力パスが指定されていません")
        
        # ディレクトリの存在確認・作成
        output_dir = Path(output_path).parent
        if not output_dir.exists():
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
                self.logger.debug(f"出力ディレクトリを作成: {output_dir}")
            except Exception as e:
                raise GenerationError(f"出力ディレクトリの作成に失敗: {str(e)}")
        
        # 書き込み権限の確認
        if output_dir.exists() and not os.access(output_dir, os.W_OK):
            raise GenerationError(f"出力ディレクトリに書き込み権限がありません: {output_dir}")
    
    def _validate_file_writable(self, file_path: str) -> None:
        """
        ファイルが書き込み可能かを検証
        
        Args:
            file_path: ファイルパス
            
        Raises:
            GenerationError: 書き込み権限エラー
        """
        path = Path(file_path)
        
        # ファイルが存在する場合は書き込み権限をチェック
        if path.exists() and not os.access(path, os.W_OK):
            raise GenerationError(f"ファイルに書き込み権限がありません: {file_path}")
    
    def _backup_existing_file(self, file_path: str) -> Optional[str]:
        """
        既存ファイルのバックアップを作成
        
        Args:
            file_path: ファイルパス
            
        Returns:
            バックアップファイルパス（バックアップが作成された場合）
        """
        path = Path(file_path)
        if not path.exists():
            return None
        
        # バックアップファイル名を生成
        backup_path = path.with_suffix(f"{path.suffix}.backup")
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}.backup.{counter}")
            counter += 1
        
        try:
            import shutil
            shutil.copy2(path, backup_path)
            self.logger.info(f"既存ファイルをバックアップ: {backup_path}")
            return str(backup_path)
        except Exception as e:
            self.logger.warning(f"バックアップの作成に失敗: {str(e)}")
            return None
    
    def _write_file(self, file_path: str, content: str, encoding: str = 'utf-8') -> None:
        """
        ファイルに内容を書き込み
        
        Args:
            file_path: ファイルパス
            content: 書き込み内容
            encoding: 文字エンコーディング
            
        Raises:
            GenerationError: 書き込みエラー
        """
        try:
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            self.logger.debug(f"ファイルを生成: {file_path}")
        except Exception as e:
            raise GenerationError(f"ファイルの書き込みに失敗: {str(e)}")
    
    def _format_template(self, template: str, data: Dict[str, Any]) -> str:
        """
        テンプレートをデータで置換
        
        Args:
            template: テンプレート文字列
            data: 置換データ
            
        Returns:
            置換後の文字列
        """
        try:
            return template.format(**data)
        except KeyError as e:
            raise GenerationError(f"テンプレートの置換に失敗: キー '{e.args[0]}' が見つかりません")
        except Exception as e:
            raise GenerationError(f"テンプレートの置換に失敗: {str(e)}")
    
    def _get_template_path(self, template_name: str) -> str:
        """
        テンプレートファイルのパスを取得
        
        Args:
            template_name: テンプレート名
            
        Returns:
            テンプレートファイルパス
            
        Raises:
            GenerationError: テンプレートファイルが見つからない
        """
        # テンプレートディレクトリを検索
        current_dir = Path(__file__).parent
        template_dirs = [
            current_dir / "templates",
            current_dir.parent / "templates",
            current_dir.parent / "shared" / "templates"
        ]
        
        for template_dir in template_dirs:
            template_path = template_dir / template_name
            if template_path.exists():
                return str(template_path)
        
        raise GenerationError(f"テンプレートファイルが見つかりません: {template_name}")
    
    def _load_template(self, template_name: str) -> str:
        """
        テンプレートファイルを読み込み
        
        Args:
            template_name: テンプレート名
            
        Returns:
            テンプレート内容
            
        Raises:
            GenerationError: テンプレート読み込みエラー
        """
        template_path = self._get_template_path(template_name)
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise GenerationError(f"テンプレートの読み込みに失敗: {str(e)}")
    
    def get_output_filename(self, data: Dict[str, Any], format_type: str) -> str:
        """
        出力ファイル名を生成
        
        Args:
            data: データ
            format_type: 出力形式
            
        Returns:
            ファイル名
        """
        # デフォルトの命名規則
        table_name = data.get('table_name', 'unknown')
        return f"{table_name}.{format_type}"
    
    def supports_format(self, format_type: str) -> bool:
        """
        指定された形式をサポートしているかチェック
        
        Args:
            format_type: 出力形式
            
        Returns:
            サポート状況
        """
        return format_type.lower() in [f.lower() for f in self.get_supported_formats()]
    
    def get_generation_info(self) -> Dict[str, Any]:
        """
        ジェネレーターの情報を取得
        
        Returns:
            ジェネレーター情報
        """
        return {
            'type': self.generator_type,
            'supported_formats': self.get_supported_formats(),
            'class_name': self.__class__.__name__
        }
