"""
統合設計ツール - 統一バリデーションエンジン

全ての設計ツールで共通利用されるバリデーション機能を提供します。
要求仕様ID検証、設計書整合性チェック、品質基準検証を統一実装します。

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md
"""

import re
import os
import yaml
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

from .config import IntegratedConfig, ToolType


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


@dataclass
class ValidationReport:
    """バリデーションレポート"""
    total_files: int = 0
    total_checks: int = 0
    errors: List[ValidationResult] = field(default_factory=list)
    warnings: List[ValidationResult] = field(default_factory=list)
    infos: List[ValidationResult] = field(default_factory=list)
    execution_time: float = 0.0
    
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
    
    def __init__(self, config: IntegratedConfig):
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
        
        if not requirement_ids and self.config.quality.requirement_id_mandatory:
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
        
        if not design_refs and self.config.quality.design_doc_sync:
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
        if not has_executive_summary:
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


class QualityValidator(BaseValidator):
    """品質バリデーター"""
    
    def validate(self, content: str, file_path: Optional[str] = None) -> List[ValidationResult]:
        """品質検証"""
        results = []
        
        # コメント密度チェック
        results.extend(self._check_comment_density(content, file_path))
        
        # 関数サイズチェック
        results.extend(self._check_function_size(content, file_path))
        
        # 複雑度チェック
        results.extend(self._check_complexity(content, file_path))
        
        return results
    
    def _check_comment_density(self, content: str, file_path: Optional[str] = None) -> List[ValidationResult]:
        """コメント密度チェック"""
        results = []
        lines = content.split('\n')
        
        total_lines = len([line for line in lines if line.strip()])
        comment_lines = len([line for line in lines if line.strip().startswith(('///', '//', '#'))])
        
        if total_lines > 0:
            comment_ratio = comment_lines / total_lines
            if comment_ratio < 0.1:  # 10%未満
                results.append(self._create_result(
                    valid=False,
                    level=ValidationLevel.WARNING,
                    category=ValidationCategory.QUALITY,
                    message=f"コメント密度が低いです: {comment_ratio:.1%}",
                    file_path=file_path,
                    suggestion="適切なコメントを追加してください"
                ))
        
        return results
    
    def _check_function_size(self, content: str, file_path: Optional[str] = None) -> List[ValidationResult]:
        """関数サイズチェック"""
        results = []
        lines = content.split('\n')
        
        # 簡易的な関数検出
        function_pattern = re.compile(r'(function\s+\w+|const\s+\w+\s*=.*=>|\w+\s*\([^)]*\)\s*{)')
        
        in_function = False
        function_start = 0
        brace_count = 0
        
        for i, line in enumerate(lines):
            if function_pattern.search(line):
                in_function = True
                function_start = i + 1
                brace_count = line.count('{') - line.count('}')
            elif in_function:
                brace_count += line.count('{') - line.count('}')
                if brace_count <= 0:
                    function_length = i - function_start + 1
                    if function_length > 50:  # 50行超過
                        results.append(self._create_result(
                            valid=False,
                            level=ValidationLevel.WARNING,
                            category=ValidationCategory.QUALITY,
                            message=f"関数が長すぎます: {function_length}行",
                            file_path=file_path,
                            line_number=function_start,
                            suggestion="関数を小さく分割することを検討してください"
                        ))
                    in_function = False
        
        return results
    
    def _check_complexity(self, content: str, file_path: Optional[str] = None) -> List[ValidationResult]:
        """複雑度チェック"""
        results = []
        
        # 簡易的な循環的複雑度計算
        complexity_keywords = ['if', 'else', 'for', 'while', 'switch', 'case', 'catch', '&&', '||']
        complexity_count = sum(content.count(keyword) for keyword in complexity_keywords)
        
        if complexity_count > 20:
            results.append(self._create_result(
                valid=False,
                level=ValidationLevel.WARNING,
                category=ValidationCategory.QUALITY,
                message=f"複雑度が高いです: {complexity_count}",
                file_path=file_path,
                suggestion="コードの簡素化を検討してください"
            ))
        
        return results


class ValidationEngine:
    """統一バリデーションエンジン"""
    
    def __init__(self, config: IntegratedConfig):
        self.config = config
        self.validators = {
            ValidationCategory.REQUIREMENT_ID: RequirementIdValidator(config),
            ValidationCategory.DESIGN_SYNC: DesignSyncValidator(config),
            ValidationCategory.FORMAT: FormatValidator(config),
            ValidationCategory.QUALITY: QualityValidator(config)
        }
    
    def validate_file(self, file_path: str, categories: Optional[List[ValidationCategory]] = None) -> ValidationReport:
        """ファイルの検証"""
        import time
        start_time = time.time()
        
        report = ValidationReport(total_files=1)
        
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
                elif category == ValidationCategory.QUALITY:
                    results = validator.validate(content, file_path)
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
        import time
        from glob import glob
        
        start_time = time.time()
        combined_report = ValidationReport()
        
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
        lines.append("統合設計ツール バリデーションレポート")
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
        import json
        
        def result_to_dict(result: ValidationResult) -> Dict[str, Any]:
            return {
                "valid": result.valid,
                "level": result.level.value,
                "category": result.category.value,
                "message": result.message,
                "file_path": result.file_path,
                "line_number": result.line_number,
                "suggestion": result.suggestion,
                "requirement_id": result.requirement_id
            }
        
        report_dict = {
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
    <title>統合設計ツール バリデーションレポート</title>
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
        <h1>統合設計ツール バリデーションレポート</h1>
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
