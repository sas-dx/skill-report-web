"""
統合設計ツール - 統一生成エンジン

全ての設計ツールで共通利用される生成機能を提供します。
テンプレートベース生成、コード生成、ドキュメント生成を統一実装します。

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md
"""

import os
import re
import json
import yaml
from typing import Dict, List, Any, Optional, Union, Callable
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime
import jinja2

from .config import IntegratedConfig, ToolType


class GenerationType(Enum):
    """生成タイプ"""
    CODE = "code"
    DOCUMENTATION = "documentation"
    CONFIGURATION = "configuration"
    TEST = "test"
    SCHEMA = "schema"


class OutputFormat(Enum):
    """出力フォーマット"""
    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"
    PYTHON = "python"
    MARKDOWN = "markdown"
    HTML = "html"
    YAML = "yaml"
    JSON = "json"
    SQL = "sql"


@dataclass
class GenerationContext:
    """生成コンテキスト"""
    requirement_id: str
    design_doc_path: Optional[str] = None
    template_name: Optional[str] = None
    output_path: Optional[str] = None
    variables: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerationResult:
    """生成結果"""
    success: bool
    output_path: Optional[str] = None
    content: Optional[str] = None
    error_message: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseGenerator(ABC):
    """生成器基底クラス"""
    
    def __init__(self, config: IntegratedConfig):
        self.config = config
        self.template_env = self._setup_template_environment()
    
    def _setup_template_environment(self) -> jinja2.Environment:
        """テンプレート環境をセットアップ"""
        template_dirs = [
            os.path.join(os.path.dirname(__file__), "..", "templates"),
            os.path.join(self.config.project_root, "docs", "tools", "templates")
        ]
        
        loader = jinja2.FileSystemLoader(template_dirs)
        env = jinja2.Environment(
            loader=loader,
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # カスタムフィルターを追加
        env.filters['camel_case'] = self._to_camel_case
        env.filters['pascal_case'] = self._to_pascal_case
        env.filters['snake_case'] = self._to_snake_case
        env.filters['kebab_case'] = self._to_kebab_case
        env.filters['current_timestamp'] = lambda x: datetime.now().isoformat()
        
        return env
    
    @abstractmethod
    def generate(self, context: GenerationContext) -> GenerationResult:
        """生成実行（抽象メソッド）"""
        pass
    
    def _to_camel_case(self, text: str) -> str:
        """キャメルケースに変換"""
        components = re.split(r'[_\-\s]+', text)
        return components[0].lower() + ''.join(word.capitalize() for word in components[1:])
    
    def _to_pascal_case(self, text: str) -> str:
        """パスカルケースに変換"""
        components = re.split(r'[_\-\s]+', text)
        return ''.join(word.capitalize() for word in components)
    
    def _to_snake_case(self, text: str) -> str:
        """スネークケースに変換"""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    def _to_kebab_case(self, text: str) -> str:
        """ケバブケースに変換"""
        return self._to_snake_case(text).replace('_', '-')
    
    def _render_template(self, template_name: str, variables: Dict[str, Any]) -> str:
        """テンプレートをレンダリング"""
        try:
            template = self.template_env.get_template(template_name)
            return template.render(**variables)
        except jinja2.TemplateNotFound:
            raise FileNotFoundError(f"テンプレートが見つかりません: {template_name}")
        except jinja2.TemplateError as e:
            raise ValueError(f"テンプレートレンダリングエラー: {e}")
    
    def _ensure_output_directory(self, output_path: str):
        """出力ディレクトリを確保"""
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
    
    def _write_output_file(self, output_path: str, content: str):
        """出力ファイルを書き込み"""
        self._ensure_output_directory(output_path)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)


class CodeGenerator(BaseGenerator):
    """コード生成器"""
    
    def generate(self, context: GenerationContext) -> GenerationResult:
        """コード生成"""
        try:
            # テンプレート名を決定
            template_name = context.template_name or self._determine_template_name(context)
            
            # 変数を準備
            variables = self._prepare_variables(context)
            
            # テンプレートをレンダリング
            content = self._render_template(template_name, variables)
            
            # 出力パスを決定
            output_path = context.output_path or self._determine_output_path(context)
            
            # ファイルに書き込み
            if output_path:
                self._write_output_file(output_path, content)
            
            return GenerationResult(
                success=True,
                output_path=output_path,
                content=content,
                metadata={
                    "template_name": template_name,
                    "generation_type": GenerationType.CODE.value,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            return GenerationResult(
                success=False,
                error_message=str(e)
            )
    
    def _determine_template_name(self, context: GenerationContext) -> str:
        """テンプレート名を決定"""
        # 要求仕様IDからテンプレートを推定
        req_id = context.requirement_id
        category = req_id.split('.')[0] if '.' in req_id else 'default'
        
        template_map = {
            'API': 'api/route.ts.j2',
            'PRO': 'components/profile.tsx.j2',
            'SKL': 'components/skill.tsx.j2',
            'CAR': 'components/career.tsx.j2',
            'WPM': 'components/work.tsx.j2',
            'TRN': 'components/training.tsx.j2',
            'RPT': 'components/report.tsx.j2'
        }
        
        return template_map.get(category, 'default/component.tsx.j2')
    
    def _determine_output_path(self, context: GenerationContext) -> str:
        """出力パスを決定"""
        req_id = context.requirement_id
        category = req_id.split('.')[0] if '.' in req_id else 'default'
        
        # カテゴリに基づいて出力ディレクトリを決定
        if category == 'API':
            base_dir = os.path.join(self.config.project_root, "src", "app", "api")
        else:
            base_dir = os.path.join(self.config.project_root, "src", "components", "generated")
        
        # ファイル名を生成
        filename = self._generate_filename(context)
        
        return os.path.join(base_dir, filename)
    
    def _generate_filename(self, context: GenerationContext) -> str:
        """ファイル名を生成"""
        req_id = context.requirement_id
        category = req_id.split('.')[0] if '.' in req_id else 'default'
        
        # 要求仕様IDからファイル名を生成
        safe_req_id = re.sub(r'[^\w\-]', '_', req_id)
        
        if category == 'API':
            return f"{safe_req_id.lower()}/route.ts"
        else:
            return f"{self._to_pascal_case(safe_req_id)}Component.tsx"
    
    def _prepare_variables(self, context: GenerationContext) -> Dict[str, Any]:
        """テンプレート変数を準備"""
        variables = {
            'requirement_id': context.requirement_id,
            'timestamp': datetime.now().isoformat(),
            'author': 'AI駆動開発システム',
            'design_doc_path': context.design_doc_path,
            **context.variables
        }
        
        # 要求仕様IDから追加情報を抽出
        req_id = context.requirement_id
        if '.' in req_id:
            parts = req_id.split('.')
            variables['category'] = parts[0]
            if len(parts) > 1 and '-' in parts[1]:
                series_parts = parts[1].split('-')
                variables['series'] = series_parts[0]
                variables['function'] = series_parts[1] if len(series_parts) > 1 else ''
        
        return variables


class DocumentationGenerator(BaseGenerator):
    """ドキュメント生成器"""
    
    def generate(self, context: GenerationContext) -> GenerationResult:
        """ドキュメント生成"""
        try:
            # テンプレート名を決定
            template_name = context.template_name or self._determine_template_name(context)
            
            # 変数を準備
            variables = self._prepare_variables(context)
            
            # テンプレートをレンダリング
            content = self._render_template(template_name, variables)
            
            # 出力パスを決定
            output_path = context.output_path or self._determine_output_path(context)
            
            # ファイルに書き込み
            if output_path:
                self._write_output_file(output_path, content)
            
            return GenerationResult(
                success=True,
                output_path=output_path,
                content=content,
                metadata={
                    "template_name": template_name,
                    "generation_type": GenerationType.DOCUMENTATION.value,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            return GenerationResult(
                success=False,
                error_message=str(e)
            )
    
    def _determine_template_name(self, context: GenerationContext) -> str:
        """テンプレート名を決定"""
        # ドキュメントタイプに基づいてテンプレートを選択
        doc_type = context.variables.get('doc_type', 'api')
        
        template_map = {
            'api': 'docs/api_spec.md.j2',
            'screen': 'docs/screen_spec.md.j2',
            'database': 'docs/table_spec.md.j2',
            'test': 'docs/test_spec.md.j2',
            'readme': 'docs/readme.md.j2'
        }
        
        return template_map.get(doc_type, 'docs/default.md.j2')
    
    def _determine_output_path(self, context: GenerationContext) -> str:
        """出力パスを決定"""
        doc_type = context.variables.get('doc_type', 'api')
        req_id = context.requirement_id
        
        # ドキュメントタイプに基づいて出力ディレクトリを決定
        type_dir_map = {
            'api': 'api/specs',
            'screen': 'screens/specs',
            'database': 'database/table-details',
            'test': 'testing/specs'
        }
        
        base_dir = os.path.join(
            self.config.project_root, 
            "docs", 
            "design", 
            type_dir_map.get(doc_type, 'misc')
        )
        
        # ファイル名を生成
        filename = self._generate_filename(context)
        
        return os.path.join(base_dir, filename)
    
    def _generate_filename(self, context: GenerationContext) -> str:
        """ファイル名を生成"""
        doc_type = context.variables.get('doc_type', 'api')
        req_id = context.requirement_id
        title = context.variables.get('title', req_id)
        
        # 安全なファイル名を生成
        safe_title = re.sub(r'[^\w\-\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', '_', title)
        
        if doc_type == 'api':
            return f"API定義書_{req_id}_{safe_title}.md"
        elif doc_type == 'screen':
            return f"画面定義書_{req_id}_{safe_title}.md"
        elif doc_type == 'database':
            return f"テーブル定義書_{req_id}_{safe_title}.md"
        else:
            return f"{safe_title}_{req_id}.md"
    
    def _prepare_variables(self, context: GenerationContext) -> Dict[str, Any]:
        """テンプレート変数を準備"""
        variables = {
            'requirement_id': context.requirement_id,
            'timestamp': datetime.now().isoformat(),
            'author': 'AI駆動開発システム',
            'design_doc_path': context.design_doc_path,
            'executive_summary': self._generate_executive_summary(context),
            **context.variables
        }
        
        return variables
    
    def _generate_executive_summary(self, context: GenerationContext) -> str:
        """エグゼクティブサマリーを生成"""
        doc_type = context.variables.get('doc_type', 'api')
        title = context.variables.get('title', context.requirement_id)
        
        summary_templates = {
            'api': f"この文書は{title}のAPI仕様を定義します。エンドポイント設計、リクエスト・レスポンス形式、エラーハンドリングを提供し、フロントエンドとバックエンド間の安全で効率的な通信を実現します。",
            'screen': f"この文書は{title}の画面仕様を定義します。UI/UXデザイン、コンポーネント構成、ユーザーインタラクションを提供し、直感的で使いやすいユーザーインターフェースを実現します。",
            'database': f"この文書は{title}のデータベース仕様を定義します。テーブル構造、制約、インデックス設計を提供し、データの整合性とパフォーマンスを両立したデータベースシステムを実現します。",
            'test': f"この文書は{title}のテスト仕様を定義します。テストケース、検証項目、品質基準を提供し、システムの信頼性と品質を保証するテスト戦略を実現します。"
        }
        
        return summary_templates.get(doc_type, f"この文書は{title}の仕様を定義します。")


class ConfigurationGenerator(BaseGenerator):
    """設定生成器"""
    
    def generate(self, context: GenerationContext) -> GenerationResult:
        """設定生成"""
        try:
            config_type = context.variables.get('config_type', 'yaml')
            
            if config_type == 'yaml':
                content = self._generate_yaml_config(context)
            elif config_type == 'json':
                content = self._generate_json_config(context)
            else:
                raise ValueError(f"サポートされていない設定タイプ: {config_type}")
            
            # 出力パスを決定
            output_path = context.output_path or self._determine_output_path(context)
            
            # ファイルに書き込み
            if output_path:
                self._write_output_file(output_path, content)
            
            return GenerationResult(
                success=True,
                output_path=output_path,
                content=content,
                metadata={
                    "config_type": config_type,
                    "generation_type": GenerationType.CONFIGURATION.value,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            return GenerationResult(
                success=False,
                error_message=str(e)
            )
    
    def _generate_yaml_config(self, context: GenerationContext) -> str:
        """YAML設定を生成"""
        config_data = {
            'requirement_id': context.requirement_id,
            'generated_at': datetime.now().isoformat(),
            'config': context.variables.get('config_data', {})
        }
        
        return yaml.dump(config_data, default_flow_style=False, allow_unicode=True)
    
    def _generate_json_config(self, context: GenerationContext) -> str:
        """JSON設定を生成"""
        config_data = {
            'requirement_id': context.requirement_id,
            'generated_at': datetime.now().isoformat(),
            'config': context.variables.get('config_data', {})
        }
        
        return json.dumps(config_data, ensure_ascii=False, indent=2)
    
    def _determine_output_path(self, context: GenerationContext) -> str:
        """出力パスを決定"""
        config_type = context.variables.get('config_type', 'yaml')
        req_id = context.requirement_id
        
        base_dir = os.path.join(self.config.project_root, "config", "generated")
        filename = f"{req_id.lower()}.{config_type}"
        
        return os.path.join(base_dir, filename)


class TestGenerator(BaseGenerator):
    """テスト生成器"""
    
    def generate(self, context: GenerationContext) -> GenerationResult:
        """テスト生成"""
        try:
            # テンプレート名を決定
            template_name = context.template_name or self._determine_template_name(context)
            
            # 変数を準備
            variables = self._prepare_variables(context)
            
            # テンプレートをレンダリング
            content = self._render_template(template_name, variables)
            
            # 出力パスを決定
            output_path = context.output_path or self._determine_output_path(context)
            
            # ファイルに書き込み
            if output_path:
                self._write_output_file(output_path, content)
            
            return GenerationResult(
                success=True,
                output_path=output_path,
                content=content,
                metadata={
                    "template_name": template_name,
                    "generation_type": GenerationType.TEST.value,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            return GenerationResult(
                success=False,
                error_message=str(e)
            )
    
    def _determine_template_name(self, context: GenerationContext) -> str:
        """テンプレート名を決定"""
        test_type = context.variables.get('test_type', 'unit')
        
        template_map = {
            'unit': 'tests/unit.test.ts.j2',
            'integration': 'tests/integration.test.ts.j2',
            'e2e': 'tests/e2e.test.ts.j2',
            'api': 'tests/api.test.ts.j2'
        }
        
        return template_map.get(test_type, 'tests/unit.test.ts.j2')
    
    def _determine_output_path(self, context: GenerationContext) -> str:
        """出力パスを決定"""
        test_type = context.variables.get('test_type', 'unit')
        req_id = context.requirement_id
        
        # テストタイプに基づいて出力ディレクトリを決定
        if test_type == 'e2e':
            base_dir = os.path.join(self.config.project_root, "tests", "e2e")
        else:
            base_dir = os.path.join(self.config.project_root, "src", "__tests__")
        
        # ファイル名を生成
        safe_req_id = re.sub(r'[^\w\-]', '_', req_id)
        filename = f"{safe_req_id.lower()}.{test_type}.test.ts"
        
        return os.path.join(base_dir, filename)
    
    def _prepare_variables(self, context: GenerationContext) -> Dict[str, Any]:
        """テンプレート変数を準備"""
        variables = {
            'requirement_id': context.requirement_id,
            'timestamp': datetime.now().isoformat(),
            'author': 'AI駆動開発システム',
            'test_type': context.variables.get('test_type', 'unit'),
            **context.variables
        }
        
        return variables


class GenerationEngine:
    """統一生成エンジン"""
    
    def __init__(self, config: IntegratedConfig):
        self.config = config
        self.generators = {
            GenerationType.CODE: CodeGenerator(config),
            GenerationType.DOCUMENTATION: DocumentationGenerator(config),
            GenerationType.CONFIGURATION: ConfigurationGenerator(config),
            GenerationType.TEST: TestGenerator(config)
        }
    
    def generate(self, generation_type: GenerationType, context: GenerationContext) -> GenerationResult:
        """生成実行"""
        if generation_type not in self.generators:
            return GenerationResult(
                success=False,
                error_message=f"サポートされていない生成タイプ: {generation_type}"
            )
        
        generator = self.generators[generation_type]
        return generator.generate(context)
    
    def generate_multiple(self, requests: List[tuple]) -> List[GenerationResult]:
        """複数生成実行"""
        results = []
        
        for generation_type, context in requests:
            result = self.generate(generation_type, context)
            results.append(result)
        
        return results
    
    def register_custom_generator(self, generation_type: GenerationType, generator: BaseGenerator):
        """カスタム生成器を登録"""
        self.generators[generation_type] = generator
    
    def get_available_templates(self, generation_type: GenerationType) -> List[str]:
        """利用可能なテンプレート一覧を取得"""
        template_dirs = [
            os.path.join(os.path.dirname(__file__), "..", "templates"),
            os.path.join(self.config.project_root, "docs", "tools", "templates")
        ]
        
        templates = []
        for template_dir in template_dirs:
            if os.path.exists(template_dir):
                for root, dirs, files in os.walk(template_dir):
                    for file in files:
                        if file.endswith('.j2'):
                            rel_path = os.path.relpath(os.path.join(root, file), template_dir)
                            templates.append(rel_path)
        
        return sorted(templates)
    
    def validate_template(self, template_name: str) -> bool:
        """テンプレートの妥当性を検証"""
        try:
            template_dirs = [
                os.path.join(os.path.dirname(__file__), "..", "templates"),
                os.path.join(self.config.project_root, "docs", "tools", "templates")
            ]
            
            loader = jinja2.FileSystemLoader(template_dirs)
            env = jinja2.Environment(loader=loader)
            
            template = env.get_template(template_name)
            # 空の変数でレンダリングテスト
            template.render()
            return True
            
        except Exception:
            return False
