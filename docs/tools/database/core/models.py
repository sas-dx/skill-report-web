"""
統一データモデル

全ツールで共通のデータ構造を定義
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class RevisionHistory:
    """改版履歴"""
    version: str
    date: str
    author: str
    changes: str


@dataclass
class ColumnDefinition:
    """カラム定義"""
    name: str
    type: str
    nullable: bool = True
    primary_key: bool = False
    unique: bool = False
    default: Optional[str] = None
    comment: str = ""
    requirement_id: Optional[str] = None


@dataclass
class IndexDefinition:
    """インデックス定義"""
    name: str
    columns: List[str]
    unique: bool = False
    comment: str = ""


@dataclass
class ForeignKeyDefinition:
    """外部キー定義"""
    name: str
    columns: List[str]
    references: Dict[str, Any]
    on_update: str = "RESTRICT"
    on_delete: str = "RESTRICT"
    comment: str = ""


@dataclass
class TableDefinition:
    """テーブル定義"""
    table_name: str
    logical_name: str
    category: str
    priority: str
    requirement_id: str
    comment: str
    revision_history: List[RevisionHistory]
    overview: str
    columns: List[ColumnDefinition]
    indexes: List[IndexDefinition] = field(default_factory=list)
    foreign_keys: List[ForeignKeyDefinition] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    rules: List[str] = field(default_factory=list)
    sample_data: List[Dict[str, Any]] = field(default_factory=list)
    
    def get_primary_key_columns(self) -> List[str]:
        """主キーカラムを取得"""
        return [col.name for col in self.columns if col.primary_key]
    
    def get_required_columns(self) -> List[str]:
        """必須カラムを取得"""
        return [col.name for col in self.columns if not col.nullable]
    
    def get_unique_columns(self) -> List[str]:
        """一意制約カラムを取得"""
        return [col.name for col in self.columns if col.unique]
    
    def validate(self) -> List[str]:
        """テーブル定義の妥当性チェック"""
        errors = []
        
        # 必須フィールドチェック
        if not self.table_name:
            errors.append("テーブル名が設定されていません")
        if not self.logical_name:
            errors.append("論理名が設定されていません")
        if not self.overview or len(self.overview) < 50:
            errors.append("概要は50文字以上で記述してください")
        if len(self.notes) < 3:
            errors.append("特記事項は3項目以上記述してください")
        if len(self.rules) < 3:
            errors.append("業務ルールは3項目以上記述してください")
        if not self.revision_history:
            errors.append("改版履歴が設定されていません")
        
        # カラム定義チェック
        if not self.columns:
            errors.append("カラム定義が設定されていません")
        
        # 主キーチェック
        primary_keys = self.get_primary_key_columns()
        if not primary_keys:
            errors.append("主キーが設定されていません")
        
        # カラム名重複チェック
        column_names = [col.name for col in self.columns]
        if len(column_names) != len(set(column_names)):
            errors.append("重複するカラム名があります")
        
        return errors


@dataclass
class ValidationResult:
    """バリデーション結果"""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    file_path: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def add_error(self, message: str) -> None:
        """エラーを追加"""
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str) -> None:
        """警告を追加"""
        self.warnings.append(message)
    
    def has_issues(self) -> bool:
        """問題があるかチェック"""
        return bool(self.errors or self.warnings)
    
    def get_summary(self) -> str:
        """結果サマリーを取得"""
        if self.is_valid and not self.warnings:
            return "✅ 検証成功"
        elif self.is_valid and self.warnings:
            return f"⚠️ 検証成功（警告 {len(self.warnings)} 件）"
        else:
            return f"❌ 検証失敗（エラー {len(self.errors)} 件、警告 {len(self.warnings)} 件）"


@dataclass
class GenerationResult:
    """生成結果"""
    success: bool
    generated_files: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def add_generated_file(self, file_path: str) -> None:
        """生成ファイルを追加"""
        self.generated_files.append(file_path)
    
    def add_error(self, message: str) -> None:
        """エラーを追加"""
        self.errors.append(message)
        self.success = False
    
    def add_warning(self, message: str) -> None:
        """警告を追加"""
        self.warnings.append(message)
    
    def get_summary(self) -> str:
        """結果サマリーを取得"""
        if self.success:
            file_count = len(self.generated_files)
            warning_text = f"（警告 {len(self.warnings)} 件）" if self.warnings else ""
            return f"✅ 生成成功: {file_count} ファイル {warning_text}"
        else:
            return f"❌ 生成失敗（エラー {len(self.errors)} 件）"


@dataclass
class ConsistencyCheckResult:
    """整合性チェック結果"""
    table_name: str
    yaml_exists: bool = False
    ddl_exists: bool = False
    markdown_exists: bool = False
    yaml_valid: bool = False
    consistency_issues: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def is_consistent(self) -> bool:
        """整合性があるかチェック"""
        return (self.yaml_exists and self.ddl_exists and 
                self.markdown_exists and self.yaml_valid and 
                not self.consistency_issues)
    
    def get_status(self) -> str:
        """ステータスを取得"""
        if self.is_consistent():
            return "✅ 整合性OK"
        elif not self.yaml_exists:
            return "❌ YAML未存在"
        elif not self.yaml_valid:
            return "❌ YAML不正"
        elif self.consistency_issues:
            return f"⚠️ 整合性問題 ({len(self.consistency_issues)} 件)"
        else:
            return "⚠️ ファイル不足"


@dataclass
class ToolExecutionResult:
    """ツール実行結果"""
    tool_name: str
    success: bool
    execution_time: float
    validation_results: List[ValidationResult] = field(default_factory=list)
    generation_results: List[GenerationResult] = field(default_factory=list)
    consistency_results: List[ConsistencyCheckResult] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def get_summary(self) -> str:
        """実行結果サマリーを取得"""
        if self.success:
            return f"✅ {self.tool_name} 実行成功 ({self.execution_time:.2f}s)"
        else:
            return f"❌ {self.tool_name} 実行失敗 ({len(self.errors)} エラー)"
