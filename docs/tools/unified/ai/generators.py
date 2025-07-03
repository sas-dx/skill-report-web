#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統一設計ツールシステム - AI生成エンジン

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md

AI駆動による設計書自動生成機能を提供します。
既存の統一生成エンジンを拡張し、より高度で知的な生成を実現します。
"""

import os
import json
import yaml
import time
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from abc import ABC, abstractmethod

from ..config.manager import UnifiedConfigManager
from ..config.schema import UnifiedConfig
from ..core.generation import (
    UnifiedGenerationEngine, 
    GenerationContext, 
    GenerationResult,
    GenerationType,
    GenerationTemplate
)


class AIGenerationMode(Enum):
    """AI生成モード"""
    CREATIVE = "creative"          # 創造的生成
    ANALYTICAL = "analytical"     # 分析的生成
    STRUCTURED = "structured"     # 構造化生成
    OPTIMIZED = "optimized"       # 最適化生成


class AIPromptTemplate(Enum):
    """AIプロンプトテンプレート"""
    DATABASE_DESIGN = "database_design"
    API_SPECIFICATION = "api_specification"
    SCREEN_DESIGN = "screen_design"
    TEST_SCENARIO = "test_scenario"
    QUALITY_IMPROVEMENT = "quality_improvement"
    CONSISTENCY_CHECK = "consistency_check"


@dataclass
class AIGenerationContext(GenerationContext):
    """AI生成コンテキスト"""
    ai_mode: AIGenerationMode = AIGenerationMode.STRUCTURED
    prompt_template: AIPromptTemplate = AIPromptTemplate.DATABASE_DESIGN
    ai_model: str = "gpt-4"
    temperature: float = 0.3
    max_tokens: int = 4000
    context_files: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)


@dataclass
class AIGenerationResult(GenerationResult):
    """AI生成結果"""
    ai_confidence: float = 0.0
    ai_reasoning: str = ""
    improvement_suggestions: List[str] = field(default_factory=list)
    alternative_approaches: List[str] = field(default_factory=list)
    quality_score: float = 0.0
    tokens_used: int = 0
    processing_time: float = 0.0


class BaseAIGenerator(ABC):
    """AI生成器基底クラス"""
    
    def __init__(self, config: UnifiedConfig):
        self.config = config
        self.ai_integration = None  # AIIntegrationManagerで初期化
        self.prompt_cache = {}
    
    @abstractmethod
    def generate_ai_content(self, context: AIGenerationContext) -> AIGenerationResult:
        """AI生成実行（抽象メソッド）"""
        pass
    
    def _load_prompt_template(self, template_type: AIPromptTemplate) -> str:
        """プロンプトテンプレートを読み込み"""
        if template_type in self.prompt_cache:
            return self.prompt_cache[template_type]
        
        template_dir = os.path.join(self.config.project_root, "docs/tools/unified/ai/prompts")
        template_file = f"{template_type.value}.txt"
        template_path = os.path.join(template_dir, template_file)
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.prompt_cache[template_type] = content
                return content
        except FileNotFoundError:
            # デフォルトプロンプトを返す
            return self._get_default_prompt(template_type)
    
    def _get_default_prompt(self, template_type: AIPromptTemplate) -> str:
        """デフォルトプロンプトを取得"""
        default_prompts = {
            AIPromptTemplate.DATABASE_DESIGN: """
あなたは経験豊富なデータベース設計者です。
以下の要求仕様に基づいて、高品質なデータベーステーブル設計を作成してください。

要求仕様: {requirements}
制約条件: {constraints}

以下の形式で回答してください：
1. テーブル設計の概要
2. カラム定義（名前、型、制約、説明）
3. インデックス設計
4. 外部キー関係
5. 設計の根拠と考慮事項
""",
            AIPromptTemplate.API_SPECIFICATION: """
あなたは経験豊富なAPI設計者です。
以下の要求仕様に基づいて、RESTful APIの詳細仕様を作成してください。

要求仕様: {requirements}
制約条件: {constraints}

以下の形式で回答してください：
1. API概要
2. エンドポイント定義
3. リクエスト/レスポンス形式
4. エラーハンドリング
5. セキュリティ考慮事項
""",
            AIPromptTemplate.SCREEN_DESIGN: """
あなたは経験豊富なUI/UX設計者です。
以下の要求仕様に基づいて、ユーザーフレンドリーな画面設計を作成してください。

要求仕様: {requirements}
制約条件: {constraints}

以下の形式で回答してください：
1. 画面設計の概要
2. コンポーネント構成
3. レイアウト設計
4. インタラクション設計
5. アクセシビリティ考慮事項
"""
        }
        return default_prompts.get(template_type, "設計書を作成してください。")
    
    def _build_prompt(self, context: AIGenerationContext) -> str:
        """プロンプトを構築"""
        template = self._load_prompt_template(context.prompt_template)
        
        # コンテキスト情報を挿入
        prompt = template.format(
            requirements="\n".join(context.requirements),
            constraints="\n".join(context.constraints),
            data=json.dumps(context.data, ensure_ascii=False, indent=2)
        )
        
        # 追加コンテキストファイルの内容を追加
        if context.context_files:
            prompt += "\n\n参考資料:\n"
            for file_path in context.context_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        prompt += f"\n--- {file_path} ---\n{content}\n"
                except Exception as e:
                    prompt += f"\n--- {file_path} (読み込みエラー: {e}) ---\n"
        
        return prompt
    
    def _validate_ai_result(self, result: str, context: AIGenerationContext) -> List[str]:
        """AI生成結果の品質チェック"""
        warnings = []
        
        # 基本的な品質チェック
        if len(result) < 100:
            warnings.append("生成された内容が短すぎます")
        
        if "エグゼクティブサマリー" not in result and context.output_type == GenerationType.MARKDOWN:
            warnings.append("エグゼクティブサマリーが含まれていません")
        
        # 要求仕様IDの存在チェック
        if not any(req_id in result for req_id in context.requirements):
            warnings.append("要求仕様IDが含まれていません")
        
        return warnings


class AIDesignDocGenerator(BaseAIGenerator):
    """AI設計書生成器"""
    
    def generate_ai_content(self, context: AIGenerationContext) -> AIGenerationResult:
        """AI設計書生成"""
        start_time = time.time()
        result = AIGenerationResult(success=False, content="")
        
        try:
            # プロンプトを構築
            prompt = self._build_prompt(context)
            
            # AI APIを呼び出し（実装は integrations.py で行う）
            if self.ai_integration:
                ai_response = self.ai_integration.generate_content(
                    prompt=prompt,
                    model=context.ai_model,
                    temperature=context.temperature,
                    max_tokens=context.max_tokens
                )
                
                content = ai_response.get("content", "")
                tokens_used = ai_response.get("tokens_used", 0)
                confidence = ai_response.get("confidence", 0.0)
                reasoning = ai_response.get("reasoning", "")
                
            else:
                # AI統合が無効な場合のフォールバック
                content = self._generate_fallback_content(context)
                tokens_used = 0
                confidence = 0.5
                reasoning = "AI統合が無効のため、テンプレートベース生成を使用"
            
            # 品質チェック
            warnings = self._validate_ai_result(content, context)
            
            # 改善提案を生成
            suggestions = self._generate_improvement_suggestions(content, context)
            
            result.success = True
            result.content = content
            result.ai_confidence = confidence
            result.ai_reasoning = reasoning
            result.improvement_suggestions = suggestions
            result.tokens_used = tokens_used
            result.warnings = warnings
            result.metadata = {
                "generator": "AIDesignDocGenerator",
                "ai_model": context.ai_model,
                "prompt_template": context.prompt_template.value,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            result.errors.append(f"AI設計書生成エラー: {e}")
        
        result.processing_time = time.time() - start_time
        return result
    
    def _generate_fallback_content(self, context: AIGenerationContext) -> str:
        """AI統合が無効な場合のフォールバック生成"""
        if context.template_type == GenerationTemplate.DATABASE_SPEC:
            return self._generate_database_fallback(context)
        elif context.template_type == GenerationTemplate.API_SPEC:
            return self._generate_api_fallback(context)
        elif context.template_type == GenerationTemplate.SCREEN_SPEC:
            return self._generate_screen_fallback(context)
        else:
            return "# 設計書\n\n## エグゼクティブサマリー\n\nAI統合が無効のため、基本テンプレートを使用しています。"
    
    def _generate_database_fallback(self, context: AIGenerationContext) -> str:
        """データベース設計のフォールバック生成"""
        table_name = context.data.get("table_name", "SAMPLE_TABLE")
        return f"""# データベーステーブル設計書: {table_name}

## エグゼクティブサマリー

この文書は{table_name}テーブルの設計仕様を定義します。基本的なCRUD操作、データ整合性、パフォーマンス要件を満たす設計を提供し、システムの安定性と拡張性を確保します。

## テーブル概要

- **テーブル名**: {table_name}
- **論理名**: {context.data.get("logical_name", "サンプルテーブル")}
- **目的**: {context.requirements[0] if context.requirements else "データ管理"}

## カラム定義

| カラム名 | データ型 | NULL許可 | 主キー | 説明 |
|----------|----------|----------|--------|------|
| id | SERIAL | × | ○ | 主キー |
| created_at | TIMESTAMP | × | | 作成日時 |
| updated_at | TIMESTAMP | × | | 更新日時 |

## 設計考慮事項

- データ整合性の確保
- パフォーマンスの最適化
- 将来の拡張性を考慮
"""
    
    def _generate_api_fallback(self, context: AIGenerationContext) -> str:
        """API設計のフォールバック生成"""
        api_id = context.data.get("api_id", "API-001")
        return f"""# API仕様書: {api_id}

## エグゼクティブサマリー

この文書は{api_id}の詳細仕様を定義します。RESTful設計原則に従い、セキュリティ、パフォーマンス、保守性を考慮したAPI設計を提供します。

## API概要

- **API ID**: {api_id}
- **エンドポイント**: {context.data.get("endpoint", "/api/sample")}
- **メソッド**: {context.data.get("method", "GET")}

## リクエスト仕様

### パラメータ

| パラメータ名 | 型 | 必須 | 説明 |
|--------------|----|----|------|
| id | integer | ○ | リソースID |

## レスポンス仕様

### 成功レスポンス (200)

```json
{
  "success": true,
  "data": {}
}
```

## エラーハンドリング

- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error
"""
    
    def _generate_screen_fallback(self, context: AIGenerationContext) -> str:
        """画面設計のフォールバック生成"""
        screen_id = context.data.get("screen_id", "SCR-001")
        return f"""# 画面設計書: {screen_id}

## エグゼクティブサマリー

この文書は{screen_id}の画面設計仕様を定義します。ユーザビリティ、アクセシビリティ、レスポンシブデザインを考慮した設計を提供し、優れたユーザーエクスペリエンスを実現します。

## 画面概要

- **画面ID**: {screen_id}
- **画面名**: {context.data.get("screen_name", "サンプル画面")}
- **目的**: {context.requirements[0] if context.requirements else "ユーザー操作"}

## コンポーネント構成

### ヘッダー
- ナビゲーション
- ユーザー情報

### メインコンテンツ
- 主要機能エリア
- データ表示エリア

### フッター
- 補助情報
- リンク集

## レスポンシブ対応

- モバイル: 320px〜767px
- タブレット: 768px〜1023px
- デスクトップ: 1024px〜

## アクセシビリティ

- WCAG 2.1 AA準拠
- キーボードナビゲーション対応
- スクリーンリーダー対応
"""
    
    def _generate_improvement_suggestions(self, content: str, context: AIGenerationContext) -> List[str]:
        """改善提案を生成"""
        suggestions = []
        
        # 基本的な改善提案
        if len(content) < 500:
            suggestions.append("内容をより詳細に記述することを推奨します")
        
        if "## エグゼクティブサマリー" not in content:
            suggestions.append("エグゼクティブサマリーセクションの追加を推奨します")
        
        if context.template_type == GenerationTemplate.DATABASE_SPEC:
            if "インデックス" not in content:
                suggestions.append("インデックス設計の追加を推奨します")
            if "外部キー" not in content:
                suggestions.append("外部キー制約の検討を推奨します")
        
        elif context.template_type == GenerationTemplate.API_SPEC:
            if "エラーハンドリング" not in content:
                suggestions.append("エラーハンドリング仕様の追加を推奨します")
            if "認証" not in content and "セキュリティ" not in content:
                suggestions.append("セキュリティ考慮事項の追加を推奨します")
        
        elif context.template_type == GenerationTemplate.SCREEN_SPEC:
            if "アクセシビリティ" not in content:
                suggestions.append("アクセシビリティ要件の追加を推奨します")
            if "レスポンシブ" not in content:
                suggestions.append("レスポンシブデザイン仕様の追加を推奨します")
        
        return suggestions


class AIQualityImprover(BaseAIGenerator):
    """AI品質改善器"""
    
    def generate_ai_content(self, context: AIGenerationContext) -> AIGenerationResult:
        """AI品質改善提案生成"""
        start_time = time.time()
        result = AIGenerationResult(success=False, content="")
        
        try:
            # 既存コンテンツを分析
            original_content = context.data.get("original_content", "")
            
            # 品質改善プロンプトを構築
            prompt = self._build_quality_improvement_prompt(original_content, context)
            
            # AI APIを呼び出し
            if self.ai_integration:
                ai_response = self.ai_integration.generate_content(
                    prompt=prompt,
                    model=context.ai_model,
                    temperature=0.2,  # 品質改善では低い温度を使用
                    max_tokens=context.max_tokens
                )
                
                content = ai_response.get("content", "")
                tokens_used = ai_response.get("tokens_used", 0)
                confidence = ai_response.get("confidence", 0.0)
                
            else:
                # フォールバック
                content = self._generate_quality_fallback(original_content)
                tokens_used = 0
                confidence = 0.5
            
            result.success = True
            result.content = content
            result.ai_confidence = confidence
            result.tokens_used = tokens_used
            result.metadata = {
                "generator": "AIQualityImprover",
                "original_length": len(original_content),
                "improved_length": len(content),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            result.errors.append(f"AI品質改善エラー: {e}")
        
        result.processing_time = time.time() - start_time
        return result
    
    def _build_quality_improvement_prompt(self, original_content: str, context: AIGenerationContext) -> str:
        """品質改善プロンプトを構築"""
        requirements_text = "\n".join(context.requirements)
        constraints_text = "\n".join(context.constraints)
        
        return f"""
あなたは経験豊富な技術文書レビューアです。
以下の設計書の品質を改善してください。

【改善対象の文書】
{original_content}

【改善要求】
{requirements_text}

【制約条件】
{constraints_text}

【改善観点】
1. エグゼクティブサマリーの充実
2. 技術的詳細の追加
3. 可読性の向上
4. 一貫性の確保
5. 必須セクションの補完

改善された文書を出力してください。
"""
    
    def _generate_quality_fallback(self, original_content: str) -> str:
        """品質改善のフォールバック"""
        improvements = []
        
        if "## エグゼクティブサマリー" not in original_content:
            improvements.append("- エグゼクティブサマリーセクションの追加")
        
        if len(original_content) < 500:
            improvements.append("- 内容の詳細化")
        
        if "要求仕様ID" not in original_content:
            improvements.append("- 要求仕様IDの明記")
        
        improvements_text = "\n".join(improvements)
        
        return f"""# 品質改善提案

## 改善点
{improvements_text}

## 改善された文書
{original_content}

## 追加推奨事項
- 図表の追加による可読性向上
- 具体例の追加
- 関連文書との整合性確認
"""


class AIConsistencyChecker(BaseAIGenerator):
    """AI整合性チェッカー"""
    
    def generate_ai_content(self, context: AIGenerationContext) -> AIGenerationResult:
        """AI整合性チェック実行"""
        start_time = time.time()
        result = AIGenerationResult(success=False, content="")
        
        try:
            # 複数文書の整合性をチェック
            documents = context.data.get("documents", [])
            
            # 整合性チェックプロンプトを構築
            prompt = self._build_consistency_check_prompt(documents, context)
            
            # AI APIを呼び出し
            if self.ai_integration:
                ai_response = self.ai_integration.generate_content(
                    prompt=prompt,
                    model=context.ai_model,
                    temperature=0.1,  # 整合性チェックでは非常に低い温度を使用
                    max_tokens=context.max_tokens
                )
                
                content = ai_response.get("content", "")
                tokens_used = ai_response.get("tokens_used", 0)
                confidence = ai_response.get("confidence", 0.0)
                
            else:
                # フォールバック
                content = self._generate_consistency_fallback(documents)
                tokens_used = 0
                confidence = 0.5
            
            result.success = True
            result.content = content
            result.ai_confidence = confidence
            result.tokens_used = tokens_used
            result.metadata = {
                "generator": "AIConsistencyChecker",
                "documents_checked": len(documents),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            result.errors.append(f"AI整合性チェックエラー: {e}")
        
        result.processing_time = time.time() - start_time
        return result
    
    def _build_consistency_check_prompt(self, documents: List[Dict[str, Any]], context: AIGenerationContext) -> str:
        """整合性チェックプロンプトを構築"""
        docs_text = ""
        for i, doc in enumerate(documents):
            docs_text += f"\n【文書{i+1}: {doc.get('name', 'Unknown')}】\n{doc.get('content', '')}\n"
        
        return f"""
あなたは経験豊富なシステム設計レビューアです。
以下の複数の設計書の整合性をチェックしてください。

{docs_text}

【チェック観点】
1. 要求仕様IDの一貫性
2. データ構造の整合性
3. API仕様とデータベース設計の整合性
4. 画面設計とAPI仕様の整合性
5. 命名規則の統一性

【出力形式】
## 整合性チェック結果
### ✅ 整合性が取れている項目
### ⚠️ 注意が必要な項目
### ❌ 不整合が検出された項目

各項目について具体的な指摘と改善提案を含めてください。
"""
    
    def _generate_consistency_fallback(self, documents: List[Dict[str, Any]]) -> str:
        """整合性チェックのフォールバック"""
        return f"""# 整合性チェック結果

## チェック対象
- 文書数: {len(documents)}

## 基本チェック結果

### ✅ 整合性が取れている項目
- 文書形式の統一
- 基本構造の一貫性

### ⚠️ 注意が必要な項目
- 詳細な整合性チェックにはAI統合が必要です
- 手動での確認を推奨します

### 推奨事項
- 要求仕様IDの一貫性確認
- 命名規則の統一確認
- データ構造の整合性確認
"""


class AIGenerationEngine:
    """AI生成エンジン統合クラス"""
    
    def __init__(self, project_name: str = "default"):
        self.config_manager = UnifiedConfigManager(project_name)
        self.config = self.config_manager.load_config()
        
        # 基本生成エンジンを初期化
        self.base_engine = UnifiedGenerationEngine(project_name)
        
        # AI生成器を初期化
        self.design_doc_generator = AIDesignDocGenerator(self.config)
        self.quality_improver = AIQualityImprover(self.config)
        self.consistency_checker = AIConsistencyChecker(self.config)
        
        # AI統合を設定（後で integrations.py で実装）
        self.ai_integration = None
    
    def set_ai_integration(self, ai_integration):
        """AI統合を設定"""
        self.ai_integration = ai_integration
        self.design_doc_generator.ai_integration = ai_integration
        self.quality_improver.ai_integration = ai_integration
        self.consistency_checker.ai_integration = ai_integration
    
    def generate_design_document(self, context: AIGenerationContext) -> AIGenerationResult:
        """AI設計書生成"""
        return self.design_doc_generator.generate_ai_content(context)
    
    def improve_quality(self, context: AIGenerationContext) -> AIGenerationResult:
        """AI品質改善"""
        return self.quality_improver.generate_ai_content(context)
    
    def check_consistency(self, context: AIGenerationContext) -> AIGenerationResult:
        """AI整合性チェック"""
        return self.consistency_checker.generate_ai_content(context)
    
    def create_ai_context(self, 
                         template_type: GenerationTemplate,
                         data: Dict[str, Any],
                         requirements: List[str],
                         **kwargs) -> AIGenerationContext:
        """AI生成コンテキストを作成"""
        
        ai_mode = kwargs.get('ai_mode', AIGenerationMode.STRUCTURED)
        prompt_template = kwargs.get('prompt_template', AIPromptTemplate.DATABASE_DESIGN)
        ai_model = kwargs.get('ai_model', 'gpt-4')
        temperature = kwargs.get('temperature', 0.3)
        max_tokens = kwargs.get('max_tokens', 4000)
        
        return AIGenerationContext(
            template_type=template_type,
            output_type=kwargs.get('output_type', GenerationType.MARKDOWN),
            data=data,
            ai_mode=ai_mode,
            prompt_template=prompt_template,
            ai_model=ai_model,
            temperature=temperature,
            max_tokens=max_tokens,
            requirements=requirements,
            constraints=kwargs.get('constraints', []),
            context_files=kwargs.get('context_files', []),
            variables=kwargs.get('variables', {}),
            filters=kwargs.get('filters', []),
            metadata=kwargs.get('metadata', {})
        )
