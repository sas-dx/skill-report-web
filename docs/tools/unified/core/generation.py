"""
統一設計ツールシステム - 統一生成エンジン

全ての設計ツールで共通利用される設計書自動生成機能を提供します。
テンプレートベース生成、動的コンテンツ生成、品質保証を統一実装します。

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md
"""

import os
import yaml
import json
from typing import Dict, List, Any, Optional, Union, Callable
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import time
from datetime import datetime
import re

from ..config.manager import UnifiedConfigManager
from ..config.schema import UnifiedConfig


class GenerationType(Enum):
    """生成タイプ"""
    MARKDOWN = "markdown"
    YAML = "yaml"
    SQL = "sql"
    TYPESCRIPT = "typescript"
    PYTHON = "python"
    HTML = "html"
    JSON = "json"


class GenerationTemplate(Enum):
    """生成テンプレート"""
    DATABASE_SPEC = "database_spec"
    API_SPEC = "api_spec"
    SCREEN_SPEC = "screen_spec"
    TEST_SPEC = "test_spec"
    CONFIG_SPEC = "config_spec"
    INTEGRATION_SPEC = "integration_spec"


@dataclass
class GenerationContext:
    """生成コンテキスト"""
    template_type: GenerationTemplate
    output_type: GenerationType
    data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)
    filters: List[str] = field(default_factory=list)


@dataclass
class GenerationResult:
    """生成結果"""
    success: bool
    content: str
    file_path: Optional[str] = None
    template_used: Optional[str] = None
    generation_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class BaseGenerator(ABC):
    """生成器基底クラス"""
    
    def __init__(self, config: UnifiedConfig):
        self.config = config
        self.template_cache = {}
    
    @abstractmethod
    def generate(self, context: GenerationContext) -> GenerationResult:
        """生成実行（抽象メソッド）"""
        pass
    
    def _load_template(self, template_path: str) -> str:
        """テンプレートを読み込み"""
        if template_path in self.template_cache:
            return self.template_cache[template_path]
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.template_cache[template_path] = content
                return content
        except Exception as e:
            raise Exception(f"テンプレート読み込みエラー: {e}")
    
    def _apply_variables(self, content: str, variables: Dict[str, Any]) -> str:
        """変数を適用"""
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            content = content.replace(placeholder, str(value))
        return content
    
    def _apply_filters(self, content: str, filters: List[str]) -> str:
        """フィルターを適用"""
        for filter_name in filters:
            if filter_name == "upper":
                content = content.upper()
            elif filter_name == "lower":
                content = content.lower()
            elif filter_name == "title":
                content = content.title()
            elif filter_name == "strip":
                content = content.strip()
        return content


class MarkdownGenerator(BaseGenerator):
    """Markdown生成器"""
    
    def generate(self, context: GenerationContext) -> GenerationResult:
        """Markdown生成"""
        start_time = time.time()
        result = GenerationResult(success=False, content="")
        
        try:
            # テンプレートパスを決定
            template_path = self._get_template_path(context.template_type)
            
            # テンプレートを読み込み
            template_content = self._load_template(template_path)
            
            # コンテンツを生成
            content = self._generate_markdown_content(template_content, context)
            
            # 変数とフィルターを適用
            content = self._apply_variables(content, context.variables)
            content = self._apply_filters(content, context.filters)
            
            # 品質チェック
            warnings = self._validate_markdown_quality(content)
            
            result.success = True
            result.content = content
            result.template_used = template_path
            result.warnings = warnings
            result.metadata = {
                "generator": "MarkdownGenerator",
                "template_type": context.template_type.value,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            result.errors.append(f"Markdown生成エラー: {e}")
        
        result.generation_time = time.time() - start_time
        return result
    
    def _get_template_path(self, template_type: GenerationTemplate) -> str:
        """テンプレートパスを取得"""
        template_dir = os.path.join(self.config.project_root, "docs/tools/unified/templates")
        
        template_map = {
            GenerationTemplate.DATABASE_SPEC: "database_spec.md.template",
            GenerationTemplate.API_SPEC: "api_spec.md.template",
            GenerationTemplate.SCREEN_SPEC: "screen_spec.md.template",
            GenerationTemplate.TEST_SPEC: "test_spec.md.template",
            GenerationTemplate.CONFIG_SPEC: "config_spec.md.template",
            GenerationTemplate.INTEGRATION_SPEC: "integration_spec.md.template"
        }
        
        template_file = template_map.get(template_type, "default.md.template")
        return os.path.join(template_dir, template_file)
    
    def _generate_markdown_content(self, template: str, context: GenerationContext) -> str:
        """Markdownコンテンツを生成"""
        content = template
        
        # データベース仕様書の場合
        if context.template_type == GenerationTemplate.DATABASE_SPEC:
            content = self._generate_database_markdown(content, context.data)
        
        # API仕様書の場合
        elif context.template_type == GenerationTemplate.API_SPEC:
            content = self._generate_api_markdown(content, context.data)
        
        # 画面仕様書の場合
        elif context.template_type == GenerationTemplate.SCREEN_SPEC:
            content = self._generate_screen_markdown(content, context.data)
        
        return content
    
    def _generate_database_markdown(self, template: str, data: Dict[str, Any]) -> str:
        """データベース仕様書Markdown生成"""
        # テーブル情報を展開
        if "table_name" in data:
            template = template.replace("{{table_name}}", data["table_name"])
        
        if "logical_name" in data:
            template = template.replace("{{logical_name}}", data["logical_name"])
        
        # カラム情報を展開
        if "columns" in data:
            columns_md = self._generate_columns_markdown(data["columns"])
            template = template.replace("{{columns_table}}", columns_md)
        
        # インデックス情報を展開
        if "indexes" in data:
            indexes_md = self._generate_indexes_markdown(data["indexes"])
            template = template.replace("{{indexes_table}}", indexes_md)
        
        return template
    
    def _generate_columns_markdown(self, columns: List[Dict[str, Any]]) -> str:
        """カラム情報のMarkdownテーブル生成"""
        lines = []
        lines.append("| カラム名 | データ型 | NULL許可 | 主キー | 一意制約 | デフォルト値 | 説明 |")
        lines.append("|----------|----------|----------|--------|----------|--------------|------|")
        
        for column in columns:
            name = column.get("name", "")
            data_type = column.get("type", "")
            nullable = "○" if column.get("nullable", False) else "×"
            primary_key = "○" if column.get("primary_key", False) else ""
            unique = "○" if column.get("unique", False) else ""
            default = column.get("default", "")
            comment = column.get("comment", "")
            
            lines.append(f"| {name} | {data_type} | {nullable} | {primary_key} | {unique} | {default} | {comment} |")
        
        return "\n".join(lines)
    
    def _generate_indexes_markdown(self, indexes: List[Dict[str, Any]]) -> str:
        """インデックス情報のMarkdownテーブル生成"""
        lines = []
        lines.append("| インデックス名 | カラム | 一意制約 | 説明 |")
        lines.append("|----------------|--------|----------|------|")
        
        for index in indexes:
            name = index.get("name", "")
            columns = ", ".join(index.get("columns", []))
            unique = "○" if index.get("unique", False) else ""
            comment = index.get("comment", "")
            
            lines.append(f"| {name} | {columns} | {unique} | {comment} |")
        
        return "\n".join(lines)
    
    def _generate_api_markdown(self, template: str, data: Dict[str, Any]) -> str:
        """API仕様書Markdown生成"""
        # API基本情報を展開
        if "api_id" in data:
            template = template.replace("{{api_id}}", data["api_id"])
        
        if "endpoint" in data:
            template = template.replace("{{endpoint}}", data["endpoint"])
        
        if "method" in data:
            template = template.replace("{{method}}", data["method"])
        
        # パラメータ情報を展開
        if "parameters" in data:
            params_md = self._generate_parameters_markdown(data["parameters"])
            template = template.replace("{{parameters_table}}", params_md)
        
        # レスポンス情報を展開
        if "responses" in data:
            responses_md = self._generate_responses_markdown(data["responses"])
            template = template.replace("{{responses_table}}", responses_md)
        
        return template
    
    def _generate_parameters_markdown(self, parameters: List[Dict[str, Any]]) -> str:
        """パラメータ情報のMarkdownテーブル生成"""
        lines = []
        lines.append("| パラメータ名 | 型 | 必須 | 説明 | 例 |")
        lines.append("|--------------|----|----|------|-----|")
        
        for param in parameters:
            name = param.get("name", "")
            param_type = param.get("type", "")
            required = "○" if param.get("required", False) else ""
            description = param.get("description", "")
            example = param.get("example", "")
            
            lines.append(f"| {name} | {param_type} | {required} | {description} | {example} |")
        
        return "\n".join(lines)
    
    def _generate_responses_markdown(self, responses: List[Dict[str, Any]]) -> str:
        """レスポンス情報のMarkdownテーブル生成"""
        lines = []
        lines.append("| ステータスコード | 説明 | レスポンス例 |")
        lines.append("|------------------|------|--------------|")
        
        for response in responses:
            status_code = response.get("status_code", "")
            description = response.get("description", "")
            example = response.get("example", "")
            
            lines.append(f"| {status_code} | {description} | {example} |")
        
        return "\n".join(lines)
    
    def _generate_screen_markdown(self, template: str, data: Dict[str, Any]) -> str:
        """画面仕様書Markdown生成"""
        # 画面基本情報を展開
        if "screen_id" in data:
            template = template.replace("{{screen_id}}", data["screen_id"])
        
        if "screen_name" in data:
            template = template.replace("{{screen_name}}", data["screen_name"])
        
        # コンポーネント情報を展開
        if "components" in data:
            components_md = self._generate_components_markdown(data["components"])
            template = template.replace("{{components_table}}", components_md)
        
        return template
    
    def _generate_components_markdown(self, components: List[Dict[str, Any]]) -> str:
        """コンポーネント情報のMarkdownテーブル生成"""
        lines = []
        lines.append("| コンポーネント名 | 種類 | 必須 | 説明 |")
        lines.append("|------------------|------|------|------|")
        
        for component in components:
            name = component.get("name", "")
            component_type = component.get("type", "")
            required = "○" if component.get("required", False) else ""
            description = component.get("description", "")
            
            lines.append(f"| {name} | {component_type} | {required} | {description} |")
        
        return "\n".join(lines)
    
    def _validate_markdown_quality(self, content: str) -> List[str]:
        """Markdown品質チェック"""
        warnings = []
        
        # エグゼクティブサマリーの存在チェック
        if "エグゼクティブサマリー" not in content:
            warnings.append("エグゼクティブサマリーが見つかりません")
        
        # 見出しレベルのチェック
        lines = content.split('\n')
        h1_count = len([line for line in lines if line.startswith('# ')])
        if h1_count == 0:
            warnings.append("H1見出しが見つかりません")
        elif h1_count > 1:
            warnings.append("H1見出しが複数あります")
        
        return warnings


class YamlGenerator(BaseGenerator):
    """YAML生成器"""
    
    def generate(self, context: GenerationContext) -> GenerationResult:
        """YAML生成"""
        start_time = time.time()
        result = GenerationResult(success=False, content="")
        
        try:
            # YAMLコンテンツを生成
            yaml_data = self._generate_yaml_data(context)
            
            # YAML文字列に変換
            content = yaml.dump(yaml_data, allow_unicode=True, default_flow_style=False, sort_keys=False)
            
            # 品質チェック
            warnings = self._validate_yaml_quality(content)
            
            result.success = True
            result.content = content
            result.warnings = warnings
            result.metadata = {
                "generator": "YamlGenerator",
                "template_type": context.template_type.value,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            result.errors.append(f"YAML生成エラー: {e}")
        
        result.generation_time = time.time() - start_time
        return result
    
    def _generate_yaml_data(self, context: GenerationContext) -> Dict[str, Any]:
        """YAMLデータを生成"""
        if context.template_type == GenerationTemplate.DATABASE_SPEC:
            return self._generate_database_yaml(context.data)
        elif context.template_type == GenerationTemplate.CONFIG_SPEC:
            return self._generate_config_yaml(context.data)
        else:
            return context.data
    
    def _generate_database_yaml(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """データベース仕様YAML生成"""
        yaml_data = {
            "table_name": data.get("table_name", ""),
            "logical_name": data.get("logical_name", ""),
            "category": data.get("category", ""),
            "priority": data.get("priority", ""),
            "requirement_id": data.get("requirement_id", ""),
            "comment": data.get("comment", ""),
            "revision_history": data.get("revision_history", []),
            "overview": data.get("overview", ""),
            "columns": data.get("columns", []),
            "indexes": data.get("indexes", []),
            "foreign_keys": data.get("foreign_keys", []),
            "notes": data.get("notes", []),
            "rules": data.get("rules", []),
            "sample_data": data.get("sample_data", [])
        }
        return yaml_data
    
    def _generate_config_yaml(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """設定仕様YAML生成"""
        return {
            "config_name": data.get("config_name", ""),
            "version": data.get("version", "1.0.0"),
            "settings": data.get("settings", {}),
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator": "UnifiedGenerationEngine"
            }
        }
    
    def _validate_yaml_quality(self, content: str) -> List[str]:
        """YAML品質チェック"""
        warnings = []
        
        try:
            yaml.safe_load(content)
        except yaml.YAMLError as e:
            warnings.append(f"YAML構文エラー: {e}")
        
        return warnings


class SqlGenerator(BaseGenerator):
    """SQL生成器"""
    
    def generate(self, context: GenerationContext) -> GenerationResult:
        """SQL生成"""
        start_time = time.time()
        result = GenerationResult(success=False, content="")
        
        try:
            # SQLコンテンツを生成
            content = self._generate_sql_content(context)
            
            # 品質チェック
            warnings = self._validate_sql_quality(content)
            
            result.success = True
            result.content = content
            result.warnings = warnings
            result.metadata = {
                "generator": "SqlGenerator",
                "template_type": context.template_type.value,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            result.errors.append(f"SQL生成エラー: {e}")
        
        result.generation_time = time.time() - start_time
        return result
    
    def _generate_sql_content(self, context: GenerationContext) -> str:
        """SQLコンテンツを生成"""
        if context.template_type == GenerationTemplate.DATABASE_SPEC:
            return self._generate_create_table_sql(context.data)
        else:
            return ""
    
    def _generate_create_table_sql(self, data: Dict[str, Any]) -> str:
        """CREATE TABLE SQL生成"""
        lines = []
        
        # テーブル作成文の開始
        table_name = data.get("table_name", "")
        lines.append(f"CREATE TABLE {table_name} (")
        
        # カラム定義
        columns = data.get("columns", [])
        column_lines = []
        
        for column in columns:
            name = column.get("name", "")
            data_type = column.get("type", "")
            nullable = "" if column.get("nullable", True) else " NOT NULL"
            default = f" DEFAULT {column.get('default')}" if column.get("default") else ""
            
            column_line = f"    {name} {data_type}{nullable}{default}"
            column_lines.append(column_line)
        
        # 主キー制約
        primary_keys = [col["name"] for col in columns if col.get("primary_key", False)]
        if primary_keys:
            column_lines.append(f"    PRIMARY KEY ({', '.join(primary_keys)})")
        
        # 一意制約
        unique_columns = [col["name"] for col in columns if col.get("unique", False)]
        for unique_col in unique_columns:
            column_lines.append(f"    UNIQUE ({unique_col})")
        
        lines.extend([line + "," if i < len(column_lines) - 1 else line for i, line in enumerate(column_lines)])
        lines.append(");")
        
        # インデックス作成
        indexes = data.get("indexes", [])
        for index in indexes:
            index_name = index.get("name", "")
            index_columns = ", ".join(index.get("columns", []))
            unique_clause = "UNIQUE " if index.get("unique", False) else ""
            
            lines.append("")
            lines.append(f"CREATE {unique_clause}INDEX {index_name} ON {table_name} ({index_columns});")
        
        return "\n".join(lines)
    
    def _validate_sql_quality(self, content: str) -> List[str]:
        """SQL品質チェック"""
        warnings = []
        
        # 基本的な構文チェック
        if "CREATE TABLE" not in content.upper():
            warnings.append("CREATE TABLE文が見つかりません")
        
        # セミコロンの存在チェック
        if not content.strip().endswith(';'):
            warnings.append("SQL文がセミコロンで終了していません")
        
        return warnings


class UnifiedGenerationEngine:
    """統一生成エンジン"""
    
    def __init__(self, project_name: str = "default"):
        self.config_manager = UnifiedConfigManager(project_name)
        self.config = self.config_manager.load_config()
        
        # 生成器を初期化
        self.generators = {
            GenerationType.MARKDOWN: MarkdownGenerator(self.config),
            GenerationType.YAML: YamlGenerator(self.config),
            GenerationType.SQL: SqlGenerator(self.config)
        }
    
    def generate(self, context: GenerationContext) -> GenerationResult:
        """統一生成実行"""
        if context.output_type not in self.generators:
            return GenerationResult(
                success=False,
                content="",
                errors=[f"サポートされていない出力タイプ: {context.output_type}"]
            )
        
        generator = self.generators[context.output_type]
        return generator.generate(context)
    
    def generate_from_yaml(self, yaml_file_path: str, template_type: GenerationTemplate, output_type: GenerationType) -> GenerationResult:
        """YAMLファイルから生成"""
        try:
            with open(yaml_file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            context = GenerationContext(
                template_type=template_type,
                output_type=output_type,
                data=data,
                metadata={"source_file": yaml_file_path}
            )
            
            return self.generate(context)
            
        except Exception as e:
            return GenerationResult(
                success=False,
                content="",
                errors=[f"YAMLファイル読み込みエラー: {e}"]
            )
    
    def batch_generate(self, contexts: List[GenerationContext]) -> List[GenerationResult]:
        """バッチ生成"""
        results = []
        
        for context in contexts:
            result = self.generate(context)
            results.append(result)
        
        return results
    
    def save_result(self, result: GenerationResult, output_path: str) -> bool:
        """生成結果を保存"""
        try:
            # ディレクトリを作成
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # ファイルに保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.content)
            
            result.file_path = output_path
            return True
            
        except Exception as e:
            result.errors.append(f"ファイル保存エラー: {e}")
            return False
    
    def create_template_context(self, template_type: GenerationTemplate, data: Dict[str, Any], **kwargs) -> GenerationContext:
        """テンプレートコンテキストを作成"""
        output_type = kwargs.get('output_type', GenerationType.MARKDOWN)
        variables = kwargs.get('variables', {})
        filters = kwargs.get('filters', [])
        
        # デフォルト変数を追加
        default_variables = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'project_name': self.config.project_name,
            'version': '1.0.0'
        }
        
        variables.update(default_variables)
        
        return GenerationContext(
            template_type=template_type,
            output_type=output_type,
            data=data,
            variables=variables,
            filters=filters,
            metadata=kwargs.get('metadata', {})
        )
