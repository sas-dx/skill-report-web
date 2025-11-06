"""
統一設計ツールシステム - 統一バリデーションエンジン

全ての設計ツールで共通利用される横断的バリデーション機能を提供します。
要求仕様ID検証、設計書整合性チェック、品質基準検証を統一実装します。

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md
"""

import re
import os
import yaml
import json
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import time

from ..config.manager import UnifiedConfigManager
from ..config.schema import UnifiedConfig


class ValidationLevel(Enum):
    """バリデーションレベル"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationCategory(Enum):
    """バリデーションカテゴリ"""
    REQUIREMENT_ID = "requirement_id"
    DESIGN_SYNC = "design_sync"
    FORMAT = "format"
    CONTENT = "content"
    QUALITY = "quality"
    SECURITY = "security"
    TRACEABILITY = "traceability"


@dataclass
class ValidationResult:
    """バリデーション結果"""
    valid: bool
    level: ValidationLevel
    category: ValidationCategory
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None
    requirement_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


@dataclass
class ValidationReport:
    """バリデーションレポート"""
    total_files: int = 0
    total_checks: int = 0
    errors: List[ValidationResult] = field(default_factory=list)
    warnings: List[ValidationResult] = field(default_factory=list)
    infos: List[ValidationResult] = field(default_factory=list)
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_valid(self) -> bool:
        """エラーがない場合はTrue"""
        return len(self.errors) == 0
    
    @property
    def error_count(self) -> int:
        """エラー数"""
        return len(self.errors)
    
    @property
    def warning_count(self) -> int:
        """警告数"""
        return len(self.warnings)
    
    @property
    def info_count(self) -> int:
        """情報数"""
        return len(self.infos)


class BaseValidator(ABC):
    """バリデーター基底クラス"""
    
    def __init__(self, config: UnifiedConfig):
        self.config = config
    
    @abstractmethod
    def validate(self, target: Any) -> List[ValidationResult]:
        """バリデーション実行（抽象メソッド）"""
        pass
    
    def _create_result(
        self,
        valid: bool,
        level: ValidationLevel,
        category: ValidationCategory,
        message: str,
        **kwargs
    ) -> ValidationResult:
        """バリデーション結果を作成"""
        return ValidationResult(
            valid=valid,
            level=level,
            category=category,
            message=message,
            **kwargs
        )


class RequirementIdValidator(BaseValidator):
    """要求仕様IDバリデーター"""
    
    # 要求仕様IDパターン
    REQUIREMENT_ID_PATTERN = re.compile(r'^[A-Z]{3}\.\d+-[A-Z]+\.\d+$')
    
    # 有効なカテゴリ
    VALID_CATEGORIES = {
        'TNT', 'PLT', 'ACC', 'PRO', 'SKL', 'CAR', 'WPM', 'TRN', 'RPT', 'NTF'
    }
    
    def validate(self, content: str, file_path: Optional[str] = None) -> List[ValidationResult]:
        """要求仕様IDの検証"""
        results = []
        
        # 要求仕様IDの存在チェック
        requirement_ids = self._extract_requirement_ids(content)
        
        # 必須チェック
        if not requirement_ids and self.config.validation.requirement_id_mandatory:
            results.append(self._create_result(
                valid=False,
                level=ValidationLevel.ERROR,
                category=ValidationCategory.REQUIREMENT_ID,
                message="要求仕様IDが見つかりません",
                file_path=file_path,
                suggestion="コメントまたはドキュメントに要求仕様IDを追加してください"
            ))
        
        # 各要求仕様IDの形式チェック
        for req_id, line_num in requirement_ids:
            if not self.REQUIREMENT_ID_PATTERN.match(req_id):
                results.append(self._create_result(
                    valid=False,
                    level=ValidationLevel.ERROR,
                    category=ValidationCategory.REQUIREMENT_ID,
                    message=f"要求仕様ID形式が無効です: {req_id}",
                    file_path=file_path,
                    line_number=line_num,
                    requirement_id=req_id,
                    suggestion="形式: カテゴリ.シリーズ-機能.詳細 (例: PRO.1-BASE.1)"
                ))
                continue
            
            # カテゴリの妥当性チェック
            category = req_id.split('.')[0]
            if category not in self.VALID_CATEGORIES:
                results.append(self._create_result(
                    valid=False,
                    level=ValidationLevel.WARNING,
                    category=ValidationCategory.REQUIREMENT_ID,
                    message=f"未知のカテゴリです: {category}",
                    file_path=file_path,
                    line_number=line_num,
                    requirement_id=req_id,
                    suggestion=f"有効なカテゴリ: {', '.join(sorted(self.VALID_CATEGORIES))}"
                ))
        
        return results
    
    def _extract_requirement_ids(self, content: str) -> List[Tuple[str, int]]:
        """コンテンツから要求仕様IDを抽出"""
        requirement_ids = []
        lines = content.split('\n')
        
        # パターン1: 要求仕様ID: XXX.X-XXX.X
        pattern1 = re.compile(r'要求仕様ID[:\s]*([A-Z]{3}\.\d+-[A-Z]+\.\d+)')
        
        # パターン2: @requirement XXX.X-XXX.X
        pattern2 = re.compile(r'@requirement\s+([A-Z]{3}\.\d+-[A-Z]+\.\d+)')
        
        # パターン3: [XXX.X-XXX.X]
        pattern3 = re.compile(r'\[([A-Z]{3}\.\d+-[A-Z]+\.\d+)\]')
        
        for line_num, line in enumerate(lines, 1):
            for pattern in [pattern1, pattern2, pattern3]:
                matches = pattern.findall(line)
                for match in matches:
                    requirement_ids.append((match, line_num))
        
        return requirement_ids


class DesignSyncValidator(BaseValidator):
    """設計書同期バリデーター"""
    
    def validate(self, file_path: str) -> List[ValidationResult]:
        """設計書との同期チェック"""
        results = []
        
        if not os.path.exists(file_path):
            results.append(self._create_result(
                valid=False,
                level=ValidationLevel.ERROR,
                category=ValidationCategory.DESIGN_SYNC,
                message=f"ファイルが存在しません: {file_path}",
                file_path=file_path
            ))
            return results
        
        # ファイル内容を読み込み
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            results.append(self._create_result(
                valid=False,
                level=ValidationLevel.ERROR,
                category=ValidationCategory.DESIGN_SYNC,
                message=f"ファイル読み込みエラー: {e}",
                file_path=file_path
            ))
            return results
        
        # 設計書参照の存在チェック
        design_refs = self._extract_design_references(content)
        
        if not design_refs and self.config.validation.design_doc_sync:
            results.append(self._create_result(
                valid=False,
                level=ValidationLevel.WARNING,
                category=ValidationCategory.DESIGN_SYNC,
                message="設計書への参照が見つかりません",
                file_path=file_path,
                suggestion="対応する設計書へのパスを追加してください"
            ))
        
        # 設計書ファイルの存在チェック
        for ref_path, line_num in design_refs:
            full_path = self._resolve_design_doc_path(ref_path, file_path)
            if not os.path.exists(full_path):
                results.append(self._create_result(
                    valid=False,
                    level=ValidationLevel.ERROR,
                    category=ValidationCategory.DESIGN_SYNC,
                    message=f"参照先設計書が存在しません: {ref_path}",
                    file_path=file_path,
                    line_number=line_num,
                    suggestion="設計書パスを確認するか、設計書を作成してください"
                ))
        
        return results
    
    def _extract_design_references(self, content: str) -> List[Tuple[str, int]]:
        """設計書参照を抽出"""
        references = []
        lines = content.split('\n')
        
        # パターン1: 設計書: docs/design/...
        pattern1 = re.compile(r'設計書[:\s]*(docs/design/[^\s\)]+)')
        
        # パターン2: 対応設計書: docs/design/...
        pattern2 = re.compile(r'対応設計書[:\s]*(docs/design/[^\s\)]+)')
        
        # パターン3: @design docs/design/...
        pattern3 = re.compile(r'@design\s+(docs/design/[^\s\)]+)')
        
        for line_num, line in enumerate(lines, 1):
            for pattern in [pattern1, pattern2, pattern3]:
                matches = pattern.findall(line)
                for match in matches:
                    references.append((match, line_num))
        
        return references
    
    def _resolve_design_doc_path(self, ref_path: str, source_file: str) -> str:
        """設計書パスを解決"""
        if os.path.isabs(ref_path):
            return ref_path
        
        # プロジェクトルートからの相対パス
        project_root = self.config.project_root
        return os.path.join(project_root, ref_path)


class FormatValidator(BaseValidator):
    """フォーマットバリデーター"""
    
    def validate(self, content: str, file_type: str, file_path: Optional[str] = None) -> List[ValidationResult]:
        """フォーマット検証"""
        results = []
        
        if file_type.lower() == 'yaml':
            results.extend(self._validate_yaml_format(content, file_path))
        elif file_type.lower() == 'markdown':
            results.extend(self._validate_markdown_format(content, file_path))
        elif file_type.lower() in ['typescript', 'javascript']:
            results.extend(self._validate_code_format(content, file_path))
        
        return results
    
    def _validate_yaml_format(self, content: str, file_path: Optional[str] = None) -> List[ValidationResult]:
        """YAML形式の検証"""
        results = []
        
        try:
            yaml.safe_load(content)
        except yaml.YAMLError as e:
            results.append(self._create_result(
                valid=False,
                level=ValidationLevel.ERROR,
                category=ValidationCategory.FORMAT,
                message=f"YAML構文エラー: {e}",
                file_path=file_path,
                suggestion="YAML構文を確認してください"
            ))
        
        return results
    
    def _validate_markdown_format(self, content: str, file_path: Optional[str] = None) -> List[ValidationResult]:
        """Markdown形式の検証"""
        results = []
        lines = content.split('\n')
        
        # エグゼクティブサマリーの存在チェック
        has_executive_summary = any('エグゼクティブサマリー' in line for line in lines)
        if not has_executive_summary and self.config.validation.executive_summary_mandatory:
            results.append(self._create_result(
                valid=False,
                level=ValidationLevel.ERROR,
                category=ValidationCategory.FORMAT,
                message="エグゼクティブサマリーが見つかりません",
                file_path=file_path,
                suggestion="## エグゼクティブサマリー セクションを追加してください"
            ))
        
        return results
    
    def _validate_code_format(self, content: str, file_path: Optional[str] = None) -> List[ValidationResult]:
        """コード形式の検証"""
        results = []
        lines = content.split('\n')
        
        # TypeScript型安全性チェック
        if 'any' in content and file_path and file_path.endswith('.ts'):
            any_lines = [i+1 for i, line in enumerate(lines) if 'any' in line and not line.strip().startswith('//')]
            for line_num in any_lines:
                results.append(self._create_result(
                    valid=False,
                    level=ValidationLevel.WARNING,
                    category=ValidationCategory.FORMAT,
                    message="any型の使用が検出されました",
                    file_path=file_path,
                    line_number=line_num,
                    suggestion="具体的な型を指定してください"
                ))
        
        return results


class TraceabilityValidator(BaseValidator):
    """トレーサビリティバリデーター"""
    
    def validate(self, file_path: str, requirement_mapping: Dict[str, List[str]]) -> List[ValidationResult]:
        """要求仕様IDトレーサビリティの検証"""
        results = []
        
        # ファイル内容を読み込み
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            results.append(self._create_result(
                valid=False,
                level=ValidationLevel.ERROR,
                category=ValidationCategory.TRACEABILITY,
                message=f"ファイル読み込みエラー: {e}",
                file_path=file_path
            ))
            return results
        
        # 要求仕様IDを抽出
        req_validator = RequirementIdValidator(self.config)
        requirement_ids = req_validator._extract_requirement_ids(content)
        
        # トレーサビリティチェック
        for req_id, line_num in requirement_ids:
            if req_id not in requirement_mapping:
                results.append(self._create_result(
                    valid=False,
                    level=ValidationLevel.WARNING,
                    category=ValidationCategory.TRACEABILITY,
                    message=f"要求仕様IDのマッピングが見つかりません: {req_id}",
                    file_path=file_path,
                    line_number=line_num,
                    requirement_id=req_id,
                    suggestion="要求仕様書で該当IDを確認してください"
                ))
        
        return results


class UnifiedValidationEngine:
    """統一バリデーションエンジン"""
    
    def __init__(self, project_name: str = "default"):
        self.config_manager = UnifiedConfigManager(project_name)
        self.config = self.config_manager.load_config()
        
        # バリデーターを初期化
        self.validators = {
            ValidationCategory.REQUIREMENT_ID: RequirementIdValidator(self.config),
            ValidationCategory.DESIGN_SYNC: DesignSyncValidator(self.config),
            ValidationCategory.FORMAT: FormatValidator(self.config),
            ValidationCategory.TRACEABILITY: TraceabilityValidator(self.config)
        }
    
    def validate_file(self, file_path: str, categories: Optional[List[ValidationCategory]] = None) -> ValidationReport:
        """ファイルの検証"""
        start_time = time.time()
        
        report = ValidationReport(total_files=1)
        report.metadata = {
            "file_path": file_path,
            "validation_engine": "UnifiedValidationEngine",
            "version": "2.0.0",
            "timestamp": time.time()
        }
        
        if not os.path.exists(file_path):
            result = ValidationResult(
                valid=False,
                level=ValidationLevel.ERROR,
                category=ValidationCategory.FORMAT,
                message=f"ファイルが存在しません: {file_path}",
                file_path=file_path
            )
            report.errors.append(result)
            return report
        
        # ファイル内容を読み込み
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            result = ValidationResult(
                valid=False,
                level=ValidationLevel.ERROR,
                category=ValidationCategory.FORMAT,
                message=f"ファイル読み込みエラー: {e}",
                file_path=file_path
            )
            report.errors.append(result)
            return report
        
        # ファイル拡張子から種類を判定
        file_ext = Path(file_path).suffix.lower()
        file_type = self._get_file_type(file_ext)
        
        # 検証カテゴリを決定
        if categories is None:
            categories = list(self.validators.keys())
        
        # 各バリデーターを実行
        for category in categories:
            if category not in self.validators:
                continue
            
            validator = self.validators[category]
            
            try:
                if category == ValidationCategory.REQUIREMENT_ID:
                    results = validator.validate(content, file_path)
                elif category == ValidationCategory.DESIGN_SYNC:
                    results = validator.validate(file_path)
                elif category == ValidationCategory.FORMAT:
                    results = validator.validate(content, file_type, file_path)
                elif category == ValidationCategory.TRACEABILITY:
                    # トレーサビリティは別途マッピング情報が必要
                    results = []
                else:
                    results = []
                
                # 結果を分類
                for result in results:
                    report.total_checks += 1
                    if result.level == ValidationLevel.ERROR:
                        report.errors.append(result)
                    elif result.level == ValidationLevel.WARNING:
                        report.warnings.append(result)
                    else:
                        report.infos.append(result)
                        
            except Exception as e:
                error_result = ValidationResult(
                    valid=False,
                    level=ValidationLevel.ERROR,
                    category=category,
                    message=f"バリデーション実行エラー: {e}",
                    file_path=file_path
                )
                report.errors.append(error_result)
        
        report.execution_time = time.time() - start_time
        return report
    
    def validate_directory(self, directory_path: str, pattern: str = "*", categories: Optional[List[ValidationCategory]] = None) -> ValidationReport:
        """ディレクトリの検証"""
        from glob import glob
        
        start_time = time.time()
        combined_report = ValidationReport()
        combined_report.metadata = {
            "directory_path": directory_path,
            "pattern": pattern,
            "validation_engine": "UnifiedValidationEngine",
            "version": "2.0.0",
            "timestamp": time.time()
        }
        
        # ファイルパターンに一致するファイルを検索
        search_pattern = os.path.join(directory_path, "**", pattern)
        files = glob(search_pattern, recursive=True)
        
        combined_report.total_files = len(files)
        
        for file_path in files:
            if os.path.isfile(file_path):
                file_report = self.validate_file(file_path, categories)
                
                # レポートを統合
                combined_report.total_checks += file_report.total_checks
                combined_report.errors.extend(file_report.errors)
                combined_report.warnings.extend(file_report.warnings)
                combined_report.infos.extend(file_report.infos)
        
        combined_report.execution_time = time.time() - start_time
        return combined_report
    
    def validate_cross_reference(self, base_directory: str) -> ValidationReport:
        """横断参照検証"""
        start_time = time.time()
        
        report = ValidationReport()
        report.metadata = {
            "validation_type": "cross_reference",
            "base_directory": base_directory,
            "validation_engine": "UnifiedValidationEngine",
            "version": "2.0.0",
            "timestamp": time.time()
        }
        
        # 設計書ディレクトリを検索
        design_dirs = [
            os.path.join(base_directory, "docs/design/database"),
            os.path.join(base_directory, "docs/design/api"),
            os.path.join(base_directory, "docs/design/screens"),
            os.path.join(base_directory, "src")
        ]
        
        all_requirement_ids = set()
        file_requirement_mapping = {}
        
        # 全ファイルから要求仕様IDを収集
        for design_dir in design_dirs:
            if os.path.exists(design_dir):
                for root, dirs, files in os.walk(design_dir):
                    for file in files:
                        if file.endswith(('.md', '.yaml', '.ts', '.tsx', '.js', '.jsx')):
                            file_path = os.path.join(root, file)
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                
                                req_validator = RequirementIdValidator(self.config)
                                requirement_ids = req_validator._extract_requirement_ids(content)
                                
                                file_requirement_mapping[file_path] = [req_id for req_id, _ in requirement_ids]
                                all_requirement_ids.update(req_id for req_id, _ in requirement_ids)
                                
                            except Exception:
                                continue
        
        # 横断参照チェック
        for file_path, req_ids in file_requirement_mapping.items():
            for req_id in req_ids:
                # 他のファイルでの参照をチェック
                referenced_files = [fp for fp, rids in file_requirement_mapping.items() 
                                  if fp != file_path and req_id in rids]
                
                if len(referenced_files) == 0:
                    report.warnings.append(ValidationResult(
                        valid=False,
                        level=ValidationLevel.WARNING,
                        category=ValidationCategory.TRACEABILITY,
                        message=f"要求仕様ID {req_id} が他のファイルで参照されていません",
                        file_path=file_path,
                        requirement_id=req_id,
                        suggestion="関連する設計書や実装ファイルで参照を追加してください"
                    ))
        
        report.execution_time = time.time() - start_time
        return report
    
    def _get_file_type(self, file_ext: str) -> str:
        """ファイル拡張子から種類を判定"""
        type_map = {
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.py': 'python',
            '.sql': 'sql'
        }
        return type_map.get(file_ext, 'text')
    
    def generate_report(self, report: ValidationReport, format: str = 'text') -> str:
        """レポート生成"""
        if format == 'json':
            return self._generate_json_report(report)
        elif format == 'html':
            return self._generate_html_report(report)
        else:
            return self._generate_text_report(report)
    
    def _generate_text_report(self, report: ValidationReport) -> str:
        """テキスト形式レポート生成"""
        lines = []
        lines.append("=" * 60)
        lines.append("統一設計ツールシステム バリデーションレポート")
        lines.append("=" * 60)
        lines.append(f"検証ファイル数: {report.total_files}")
        lines.append(f"検証項目数: {report.total_checks}")
        lines.append(f"実行時間: {report.execution_time:.2f}秒")
        lines.append(f"結果: {'✅ 成功' if report.is_valid else '❌ 失敗'}")
        lines.append("")
        
        # サマリー
        lines.append("📊 サマリー")
        lines.append("-" * 20)
        lines.append(f"エラー: {report.error_count}")
        lines.append(f"警告: {report.warning_count}")
        lines.append(f"情報: {report.info_count}")
        lines.append("")
        
        # エラー詳細
        if report.errors:
            lines.append("❌ エラー詳細")
            lines.append("-" * 20)
            for error in report.errors:
                lines.append(f"📁 {error.file_path or 'N/A'}")
                if error.line_number:
                    lines.append(f"📍 行 {error.line_number}")
                lines.append(f"🔍 {error.category.value}: {error.message}")
                if error.suggestion:
                    lines.append(f"💡 提案: {error.suggestion}")
                lines.append("")
        
        # 警告詳細
        if report.warnings:
            lines.append("⚠️ 警告詳細")
            lines.append("-" * 20)
            for warning in report.warnings:
                lines.append(f"📁 {warning.file_path or 'N/A'}")
                if warning.line_number:
                    lines.append(f"📍 行 {warning.line_number}")
                lines.append(f"🔍 {warning.category.value}: {warning.message}")
                if warning.suggestion:
                    lines.append(f"💡 提案: {warning.suggestion}")
                lines.append("")
        
        return "\n".join(lines)
    
    def _generate_json_report(self, report: ValidationReport) -> str:
        """JSON形式レポート生成"""
        def result_to_dict(result: ValidationResult) -> Dict[str, Any]:
            return {
                "valid": result.valid,
                "level": result.level.value,
                "category": result.category.value,
                "message": result.message,
                "file_path": result.file_path,
                "line_number": result.line_number,
                "suggestion": result.suggestion,
                "requirement_id": result.requirement_id,
                "context": result.context
            }
        
        report_dict = {
            "metadata": report.metadata,
            "summary": {
                "total_files": report.total_files,
                "total_checks": report.total_checks,
                "execution_time": report.execution_time,
                "is_valid": report.is_valid,
                "error_count": report.error_count,
                "warning_count": report.warning_count,
                "info_count": report.info_count
            },
            "results": {
                "errors": [result_to_dict(error) for error in report.errors],
                "warnings": [result_to_dict(warning) for warning in report.warnings],
                "infos": [result_to_dict(info) for info in report.infos]
            }
        }
        
        return json.dumps(report_dict, ensure_ascii=False, indent=2)
    
    def _generate_html_report(self, report: ValidationReport) -> str:
        """HTML形式レポート生成"""
        html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>統一設計ツールシステム バリデーションレポート</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f5f5f5; padding: 20px; border-radius: 5px; }}
        .summary {{ margin: 20px 0; }}
        .result-section {{ margin: 20px 0; }}
        .error {{ color: #d32f2f; }}
        .warning {{ color: #f57c00; }}
        .info {{ color: #1976d2; }}
        .result-item {{ margin: 10px 0; padding: 10px; border-left: 4px solid #ccc; }}
        .result-item.error {{ border-left-color: #d32f2f; }}
        .result-item.warning {{ border-left-color: #f57c00; }}
        .result-item.info {{ border-left-color: #1976d2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>統一設計ツールシステム バリデーションレポート</h1>
        <p>検証ファイル数: {report.total_files} | 検証項目数: {report.total_checks} | 実行時間: {report.execution_time:.2f}秒</p>
        <p>結果: {'✅ 成功' if report.is_valid else '❌ 失敗'}</p>
    </div>
    
    <div class="summary">
        <h2>📊 サマリー</h2>
        <p>エラー: <span class="error">{report.error_count}</span></p>
        <p>警告: <span class="warning">{report.warning_count}</span></p>
        <p>情報: <span class="info">{report.info_count}</span></p>
    </div>
"""
        
        if report.errors:
            html += '<div class="result-section"><h2 class="error">❌ エラー詳細</h2>'
            for error in report.errors:
                html += f'''
                <div class="result-item error">
                    <strong>📁 {error.file_path or 'N/A'}</strong>
                    {f'<br>📍 行 {error.line_number}' if error.line_number else ''}
                    <br>🔍 {error.category.value}: {error.message}
                    {f'<br>💡 提案: {error.suggestion}' if error.suggestion else ''}
                </div>
                '''
            html += '</div>'
        
        if report.warnings:
            html += '<div class="result-section"><h2 class="warning">⚠️ 警告詳細</h2>'
            for warning in report.warnings:
                html += f'''
                <div class="result-item warning">
                    <strong>📁 {warning.file_path or 'N/A'}</strong>
                    {f'<br>📍 行 {warning.line_number}' if warning.line_number else ''}
                    <br>🔍 {warning.category.value}: {warning.message}
                    {f'<br>💡 提案: {warning.suggestion}' if warning.suggestion else ''}
                </div>
                '''
            html += '</div>'
        
        html += '</body></html>'
        return html
