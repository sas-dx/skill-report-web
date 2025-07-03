#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統一設計ツールシステム - AI統合管理

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md

複数のAIプロバイダー（OpenAI、Claude、ローカルLLM）との統合を管理し、
統一されたインターフェースでAI機能を提供します。
"""

import os
import json
import time
import asyncio
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import logging

# AI統合用ライブラリ（実際の実装時にインストール）
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from ..config.schema import UnifiedConfig


class AIProvider(Enum):
    """AIプロバイダー"""
    OPENAI = "openai"
    CLAUDE = "claude"
    LOCAL_LLM = "local_llm"
    MOCK = "mock"  # テスト用


class AIModelType(Enum):
    """AIモデルタイプ"""
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    CLAUDE_3_OPUS = "claude-3-opus-20240229"
    CLAUDE_3_SONNET = "claude-3-sonnet-20240229"
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
    LOCAL_LLAMA = "llama-2-70b"
    LOCAL_CODELLAMA = "codellama-34b"


@dataclass
class AIRequest:
    """AIリクエスト"""
    prompt: str
    model: str = "gpt-4"
    temperature: float = 0.3
    max_tokens: int = 4000
    system_prompt: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIResponse:
    """AIレスポンス"""
    content: str
    tokens_used: int = 0
    confidence: float = 0.0
    reasoning: str = ""
    model_used: str = ""
    provider: str = ""
    processing_time: float = 0.0
    cost: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    success: bool = True
    error: Optional[str] = None


class BaseAIIntegration(ABC):
    """AI統合基底クラス"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.rate_limiter = None  # レート制限管理
        self.cost_tracker = {}    # コスト追跡
    
    @abstractmethod
    async def generate_content_async(self, request: AIRequest) -> AIResponse:
        """非同期コンテンツ生成（抽象メソッド）"""
        pass
    
    def generate_content(self, request: AIRequest) -> AIResponse:
        """同期コンテンツ生成"""
        return asyncio.run(self.generate_content_async(request))
    
    def _calculate_cost(self, tokens_used: int, model: str) -> float:
        """コスト計算"""
        # モデル別の料金表（実際の料金は変動するため、設定ファイルから読み込むべき）
        cost_per_1k_tokens = {
            "gpt-4": 0.03,
            "gpt-4-turbo": 0.01,
            "gpt-3.5-turbo": 0.002,
            "claude-3-opus": 0.015,
            "claude-3-sonnet": 0.003,
            "claude-3-haiku": 0.00025,
        }
        
        rate = cost_per_1k_tokens.get(model, 0.01)
        return (tokens_used / 1000) * rate
    
    def _track_usage(self, model: str, tokens: int, cost: float):
        """使用量追跡"""
        today = time.strftime("%Y-%m-%d")
        if today not in self.cost_tracker:
            self.cost_tracker[today] = {}
        
        if model not in self.cost_tracker[today]:
            self.cost_tracker[today][model] = {"tokens": 0, "cost": 0.0, "requests": 0}
        
        self.cost_tracker[today][model]["tokens"] += tokens
        self.cost_tracker[today][model]["cost"] += cost
        self.cost_tracker[today][model]["requests"] += 1


class OpenAIIntegration(BaseAIIntegration):
    """OpenAI統合"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.getenv("OPENAI_API_KEY")
        self.organization = config.get("organization")
        self.base_url = config.get("base_url")
        
        if OPENAI_AVAILABLE and self.api_key:
            self.client = openai.OpenAI(
                api_key=self.api_key,
                organization=self.organization,
                base_url=self.base_url
            )
            self.available = True
        else:
            self.client = None
            self.available = False
            self.logger.warning("OpenAI統合が利用できません（APIキーまたはライブラリが不足）")
    
    async def generate_content_async(self, request: AIRequest) -> AIResponse:
        """OpenAI非同期コンテンツ生成"""
        start_time = time.time()
        
        if not self.available:
            return AIResponse(
                content="",
                success=False,
                error="OpenAI統合が利用できません",
                provider="openai"
            )
        
        try:
            # システムプロンプトとユーザープロンプトを構築
            messages = []
            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.prompt})
            
            # OpenAI API呼び出し
            response = self.client.chat.completions.create(
                model=request.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # レスポンス解析
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            cost = self._calculate_cost(tokens_used, request.model)
            
            # 使用量追跡
            self._track_usage(request.model, tokens_used, cost)
            
            return AIResponse(
                content=content,
                tokens_used=tokens_used,
                confidence=0.8,  # OpenAIは信頼度を返さないため固定値
                model_used=request.model,
                provider="openai",
                processing_time=time.time() - start_time,
                cost=cost,
                metadata={
                    "finish_reason": response.choices[0].finish_reason,
                    "response_id": response.id,
                    "created": response.created
                }
            )
            
        except Exception as e:
            self.logger.error(f"OpenAI API呼び出しエラー: {e}")
            return AIResponse(
                content="",
                success=False,
                error=str(e),
                provider="openai",
                processing_time=time.time() - start_time
            )


class ClaudeIntegration(BaseAIIntegration):
    """Claude統合"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
        
        if ANTHROPIC_AVAILABLE and self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.available = True
        else:
            self.client = None
            self.available = False
            self.logger.warning("Claude統合が利用できません（APIキーまたはライブラリが不足）")
    
    async def generate_content_async(self, request: AIRequest) -> AIResponse:
        """Claude非同期コンテンツ生成"""
        start_time = time.time()
        
        if not self.available:
            return AIResponse(
                content="",
                success=False,
                error="Claude統合が利用できません",
                provider="claude"
            )
        
        try:
            # Claudeのメッセージ形式に変換
            messages = [{"role": "user", "content": request.prompt}]
            
            # Claude API呼び出し
            response = self.client.messages.create(
                model=request.model,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                system=request.system_prompt or "",
                messages=messages
            )
            
            # レスポンス解析
            content = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            cost = self._calculate_cost(tokens_used, request.model)
            
            # 使用量追跡
            self._track_usage(request.model, tokens_used, cost)
            
            return AIResponse(
                content=content,
                tokens_used=tokens_used,
                confidence=0.85,  # Claudeは一般的に高品質
                model_used=request.model,
                provider="claude",
                processing_time=time.time() - start_time,
                cost=cost,
                metadata={
                    "stop_reason": response.stop_reason,
                    "response_id": response.id,
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            )
            
        except Exception as e:
            self.logger.error(f"Claude API呼び出しエラー: {e}")
            return AIResponse(
                content="",
                success=False,
                error=str(e),
                provider="claude",
                processing_time=time.time() - start_time
            )


class LocalLLMIntegration(BaseAIIntegration):
    """ローカルLLM統合"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.endpoint = config.get("endpoint", "http://localhost:11434")
        self.model_name = config.get("model_name", "llama2")
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """ローカルLLMの利用可能性をチェック"""
        try:
            import requests
            response = requests.get(f"{self.endpoint}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            self.logger.warning("ローカルLLMが利用できません")
            return False
    
    async def generate_content_async(self, request: AIRequest) -> AIResponse:
        """ローカルLLM非同期コンテンツ生成"""
        start_time = time.time()
        
        if not self.available:
            return AIResponse(
                content="",
                success=False,
                error="ローカルLLMが利用できません",
                provider="local_llm"
            )
        
        try:
            import requests
            
            # ローカルLLM API呼び出し（Ollama形式）
            payload = {
                "model": self.model_name,
                "prompt": request.prompt,
                "system": request.system_prompt or "",
                "options": {
                    "temperature": request.temperature,
                    "num_predict": request.max_tokens
                },
                "stream": False
            }
            
            response = requests.post(
                f"{self.endpoint}/api/generate",
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            content = result.get("response", "")
            
            # トークン数を推定（正確な値は取得できない場合が多い）
            tokens_used = len(content.split()) * 1.3  # 概算
            
            return AIResponse(
                content=content,
                tokens_used=int(tokens_used),
                confidence=0.7,  # ローカルLLMは品質が変動
                model_used=self.model_name,
                provider="local_llm",
                processing_time=time.time() - start_time,
                cost=0.0,  # ローカルなのでコストなし
                metadata={
                    "eval_count": result.get("eval_count", 0),
                    "eval_duration": result.get("eval_duration", 0)
                }
            )
            
        except Exception as e:
            self.logger.error(f"ローカルLLM呼び出しエラー: {e}")
            return AIResponse(
                content="",
                success=False,
                error=str(e),
                provider="local_llm",
                processing_time=time.time() - start_time
            )


class MockAIIntegration(BaseAIIntegration):
    """モックAI統合（テスト用）"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.available = True
        self.mock_responses = config.get("mock_responses", {})
    
    async def generate_content_async(self, request: AIRequest) -> AIResponse:
        """モック非同期コンテンツ生成"""
        start_time = time.time()
        
        # 遅延をシミュレート
        await asyncio.sleep(0.5)
        
        # プロンプトに基づいてモックレスポンスを選択
        if "データベース" in request.prompt:
            content = self._generate_database_mock()
        elif "API" in request.prompt:
            content = self._generate_api_mock()
        elif "画面" in request.prompt:
            content = self._generate_screen_mock()
        else:
            content = self._generate_generic_mock()
        
        return AIResponse(
            content=content,
            tokens_used=len(content.split()),
            confidence=0.9,  # モックなので高い信頼度
            model_used=request.model,
            provider="mock",
            processing_time=time.time() - start_time,
            cost=0.0,
            metadata={"mock": True}
        )
    
    def _generate_database_mock(self) -> str:
        """データベース設計のモックレスポンス"""
        return """# データベーステーブル設計書

## エグゼクティブサマリー

この文書はAI生成によるデータベーステーブル設計を定義します。正規化原則、パフォーマンス要件、拡張性を考慮した設計を提供し、システムの安定性と保守性を確保します。

## テーブル概要

高品質なデータベース設計により、効率的なデータ管理と高速なクエリ実行を実現します。

## 設計考慮事項

- 第3正規形による正規化
- 適切なインデックス設計
- 外部キー制約による整合性保証
- 将来の拡張性を考慮した設計
"""
    
    def _generate_api_mock(self) -> str:
        """API設計のモックレスポンス"""
        return """# API仕様書

## エグゼクティブサマリー

この文書はAI生成によるRESTful API設計を定義します。セキュリティ、パフォーマンス、保守性を考慮した設計を提供し、優れた開発者体験を実現します。

## API概要

RESTful設計原則に従い、直感的で使いやすいAPIを提供します。

## 設計考慮事項

- RESTful設計原則の遵守
- 適切なHTTPステータスコード
- 包括的なエラーハンドリング
- セキュリティベストプラクティス
"""
    
    def _generate_screen_mock(self) -> str:
        """画面設計のモックレスポンス"""
        return """# 画面設計書

## エグゼクティブサマリー

この文書はAI生成による画面設計を定義します。ユーザビリティ、アクセシビリティ、レスポンシブデザインを考慮した設計を提供し、優れたユーザーエクスペリエンスを実現します。

## 画面概要

直感的で使いやすいインターフェースにより、ユーザーの生産性を向上させます。

## 設計考慮事項

- ユーザー中心設計
- アクセシビリティ要件（WCAG 2.1 AA）
- レスポンシブデザイン
- 一貫性のあるUI/UX
"""
    
    def _generate_generic_mock(self) -> str:
        """汎用モックレスポンス"""
        return """# AI生成設計書

## エグゼクティブサマリー

この文書はAI駆動による設計書生成のデモンストレーションです。高品質で一貫性のある設計書を自動生成し、開発効率の向上と品質の標準化を実現します。

## 概要

AI技術を活用することで、従来の手動作業を大幅に効率化し、より高品質な設計書を短時間で作成できます。

## 特徴

- 自動生成による効率化
- 一貫性のある品質
- 継続的な改善提案
- 複数文書の整合性チェック
"""


class AIIntegrationManager:
    """AI統合管理クラス"""
    
    def __init__(self, config: UnifiedConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.integrations: Dict[str, BaseAIIntegration] = {}
        self.default_provider = "mock"
        self.fallback_providers = ["mock"]
        
        self._initialize_integrations()
    
    def _initialize_integrations(self):
        """AI統合を初期化"""
        ai_config = getattr(self.config, 'ai', {})
        
        # OpenAI統合
        if ai_config.get('openai', {}).get('enabled', False):
            try:
                self.integrations['openai'] = OpenAIIntegration(ai_config['openai'])
                if self.integrations['openai'].available:
                    self.default_provider = 'openai'
                    self.logger.info("OpenAI統合を初期化しました")
            except Exception as e:
                self.logger.error(f"OpenAI統合初期化エラー: {e}")
        
        # Claude統合
        if ai_config.get('claude', {}).get('enabled', False):
            try:
                self.integrations['claude'] = ClaudeIntegration(ai_config['claude'])
                if self.integrations['claude'].available and self.default_provider == 'mock':
                    self.default_provider = 'claude'
                    self.logger.info("Claude統合を初期化しました")
            except Exception as e:
                self.logger.error(f"Claude統合初期化エラー: {e}")
        
        # ローカルLLM統合
        if ai_config.get('local_llm', {}).get('enabled', False):
            try:
                self.integrations['local_llm'] = LocalLLMIntegration(ai_config['local_llm'])
                if self.integrations['local_llm'].available:
                    self.logger.info("ローカルLLM統合を初期化しました")
            except Exception as e:
                self.logger.error(f"ローカルLLM統合初期化エラー: {e}")
        
        # モック統合（常に利用可能）
        self.integrations['mock'] = MockAIIntegration(ai_config.get('mock', {}))
        self.logger.info("モックAI統合を初期化しました")
    
    def generate_content(self, 
                        prompt: str,
                        model: str = "gpt-4",
                        temperature: float = 0.3,
                        max_tokens: int = 4000,
                        system_prompt: Optional[str] = None,
                        provider: Optional[str] = None,
                        **kwargs) -> Dict[str, Any]:
        """コンテンツ生成（統一インターフェース）"""
        
        # プロバイダーを決定
        target_provider = provider or self.default_provider
        
        # リクエストを作成
        request = AIRequest(
            prompt=prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
            context=kwargs.get('context', {}),
            metadata=kwargs.get('metadata', {})
        )
        
        # AI統合を実行
        response = self._execute_with_fallback(request, target_provider)
        
        # レスポンスを辞書形式で返す
        return {
            "content": response.content,
            "tokens_used": response.tokens_used,
            "confidence": response.confidence,
            "reasoning": response.reasoning,
            "model_used": response.model_used,
            "provider": response.provider,
            "processing_time": response.processing_time,
            "cost": response.cost,
            "success": response.success,
            "error": response.error,
            "metadata": response.metadata
        }
    
    def _execute_with_fallback(self, request: AIRequest, provider: str) -> AIResponse:
        """フォールバック付きでAI統合を実行"""
        
        # 指定されたプロバイダーを試行
        if provider in self.integrations:
            response = self.integrations[provider].generate_content(request)
            if response.success:
                return response
            else:
                self.logger.warning(f"{provider}での生成に失敗: {response.error}")
        
        # フォールバックプロバイダーを試行
        for fallback_provider in self.fallback_providers:
            if fallback_provider != provider and fallback_provider in self.integrations:
                self.logger.info(f"フォールバック: {fallback_provider}を使用")
                response = self.integrations[fallback_provider].generate_content(request)
                if response.success:
                    return response
        
        # 全て失敗した場合
        return AIResponse(
            content="",
            success=False,
            error="全てのAIプロバイダーで生成に失敗しました",
            provider="none"
        )
    
    def get_available_providers(self) -> List[str]:
        """利用可能なプロバイダー一覧を取得"""
        return [
            provider for provider, integration in self.integrations.items()
            if integration.available
        ]
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """使用統計を取得"""
        stats = {}
        for provider, integration in self.integrations.items():
            if hasattr(integration, 'cost_tracker'):
                stats[provider] = integration.cost_tracker
        return stats
    
    def set_default_provider(self, provider: str):
        """デフォルトプロバイダーを設定"""
        if provider in self.integrations and self.integrations[provider].available:
            self.default_provider = provider
            self.logger.info(f"デフォルトプロバイダーを{provider}に設定しました")
        else:
            self.logger.error(f"プロバイダー{provider}は利用できません")
