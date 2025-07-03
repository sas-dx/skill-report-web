#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統一設計ツールシステム - 外部システム連携API

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md

外部システムとの連携機能を提供し、設計書の品質分析結果を
他のツールやサービスと統合できるAPIインターフェースを実現します。
"""

import os
import json
import time
import asyncio
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging
import requests
from urllib.parse import urljoin

from .analytics import RealTimeAnalyticsEngine, AnalysisResult, AnalysisType
from ..config.manager import UnifiedConfigManager


class IntegrationType(Enum):
    """統合タイプ"""
    WEBHOOK = "webhook"
    REST_API = "rest_api"
    SLACK = "slack"
    TEAMS = "teams"
    JIRA = "jira"
    GITHUB = "github"
    GITLAB = "gitlab"
    CONFLUENCE = "confluence"
    NOTION = "notion"


@dataclass
class ExternalSystemConfig:
    """外部システム設定"""
    name: str
    integration_type: IntegrationType
    endpoint_url: str
    api_key: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    headers: Dict[str, str] = None
    enabled: bool = True
    retry_count: int = 3
    timeout: int = 30
    rate_limit: int = 100  # requests per minute


@dataclass
class IntegrationEvent:
    """統合イベント"""
    event_type: str
    source_system: str
    target_system: str
    data: Dict[str, Any]
    timestamp: datetime
    correlation_id: str
    priority: str = "normal"  # low, normal, high, critical


class ExternalAPIManager:
    """外部API管理"""
    
    def __init__(self, project_name: str = "default"):
        self.project_name = project_name
        self.logger = logging.getLogger(__name__)
        
        # 設定管理
        config_manager = UnifiedConfigManager(project_name)
        self.unified_config = config_manager.load_config()
        
        # 分析エンジン
        self.analytics_engine = RealTimeAnalyticsEngine(self.unified_config)
        
        # 外部システム設定
        self.external_systems: Dict[str, ExternalSystemConfig] = {}
        self._load_external_systems()
        
        # イベントキュー
        self.event_queue = asyncio.Queue()
        self.processing_events = False
        
        # レート制限管理
        self.rate_limiters = {}
        
        # 統計情報
        self.integration_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "avg_response_time": 0.0,
            "last_request_time": None
        }
    
    def _load_external_systems(self):
        """外部システム設定を読み込み"""
        try:
            # 設定ファイルから外部システム情報を読み込み
            config_path = f"config/projects/{self.project_name}.yaml"
            if os.path.exists(config_path):
                import yaml
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
                
                external_systems = config_data.get('external_systems', {})
                for name, config in external_systems.items():
                    self.external_systems[name] = ExternalSystemConfig(
                        name=name,
                        integration_type=IntegrationType(config.get('type', 'webhook')),
                        endpoint_url=config.get('endpoint_url', ''),
                        api_key=config.get('api_key'),
                        username=config.get('username'),
                        password=config.get('password'),
                        headers=config.get('headers', {}),
                        enabled=config.get('enabled', True),
                        retry_count=config.get('retry_count', 3),
                        timeout=config.get('timeout', 30),
                        rate_limit=config.get('rate_limit', 100)
                    )
            
        except Exception as e:
            self.logger.warning(f"外部システム設定の読み込みに失敗: {e}")
    
    async def start_event_processing(self):
        """イベント処理を開始"""
        if self.processing_events:
            return
        
        self.processing_events = True
        self.logger.info("外部システム連携イベント処理を開始しました")
        
        while self.processing_events:
            try:
                # イベントキューから処理
                event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)
                await self._process_integration_event(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"イベント処理エラー: {e}")
    
    async def stop_event_processing(self):
        """イベント処理を停止"""
        self.processing_events = False
        self.logger.info("外部システム連携イベント処理を停止しました")
    
    async def send_analysis_result(self, result: AnalysisResult, target_systems: List[str] = None):
        """分析結果を外部システムに送信"""
        if target_systems is None:
            target_systems = [name for name, config in self.external_systems.items() if config.enabled]
        
        for system_name in target_systems:
            if system_name not in self.external_systems:
                self.logger.warning(f"未知の外部システム: {system_name}")
                continue
            
            event = IntegrationEvent(
                event_type="analysis_result",
                source_system="unified_design_tools",
                target_system=system_name,
                data={
                    "analysis_type": result.analysis_type.value,
                    "target_file": result.target_file,
                    "score": result.score,
                    "priority": result.priority.value,
                    "issues": result.issues,
                    "suggestions": result.suggestions,
                    "timestamp": result.timestamp.isoformat(),
                    "processing_time": result.processing_time
                },
                timestamp=datetime.now(),
                correlation_id=f"analysis_{int(time.time())}_{result.target_file.replace('/', '_')}",
                priority="high" if result.priority.value in ["critical", "high"] else "normal"
            )
            
            await self.event_queue.put(event)
    
    async def send_quality_alert(self, file_path: str, issues: List[str], priority: str = "high"):
        """品質アラートを外部システムに送信"""
        alert_data = {
            "alert_type": "quality_issue",
            "file_path": file_path,
            "issues": issues,
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
            "project": self.project_name
        }
        
        for system_name, config in self.external_systems.items():
            if not config.enabled:
                continue
            
            event = IntegrationEvent(
                event_type="quality_alert",
                source_system="unified_design_tools",
                target_system=system_name,
                data=alert_data,
                timestamp=datetime.now(),
                correlation_id=f"alert_{int(time.time())}_{file_path.replace('/', '_')}",
                priority=priority
            )
            
            await self.event_queue.put(event)
    
    async def _process_integration_event(self, event: IntegrationEvent):
        """統合イベントを処理"""
        system_config = self.external_systems.get(event.target_system)
        if not system_config or not system_config.enabled:
            return
        
        try:
            # レート制限チェック
            if not self._check_rate_limit(event.target_system):
                self.logger.warning(f"レート制限により送信をスキップ: {event.target_system}")
                return
            
            # 統合タイプに応じた処理
            if system_config.integration_type == IntegrationType.WEBHOOK:
                await self._send_webhook(system_config, event)
            elif system_config.integration_type == IntegrationType.SLACK:
                await self._send_slack_message(system_config, event)
            elif system_config.integration_type == IntegrationType.TEAMS:
                await self._send_teams_message(system_config, event)
            elif system_config.integration_type == IntegrationType.JIRA:
                await self._create_jira_issue(system_config, event)
            elif system_config.integration_type == IntegrationType.GITHUB:
                await self._create_github_issue(system_config, event)
            else:
                await self._send_generic_api_request(system_config, event)
            
            self.integration_stats["successful_requests"] += 1
            
        except Exception as e:
            self.logger.error(f"統合イベント処理エラー {event.target_system}: {e}")
            self.integration_stats["failed_requests"] += 1
        
        finally:
            self.integration_stats["total_requests"] += 1
            self.integration_stats["last_request_time"] = datetime.now()
    
    async def _send_webhook(self, config: ExternalSystemConfig, event: IntegrationEvent):
        """Webhook送信"""
        payload = {
            "event_type": event.event_type,
            "source": event.source_system,
            "timestamp": event.timestamp.isoformat(),
            "correlation_id": event.correlation_id,
            "priority": event.priority,
            "data": event.data
        }
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "UnifiedDesignTools/1.0"
        }
        
        if config.headers:
            headers.update(config.headers)
        
        if config.api_key:
            headers["Authorization"] = f"Bearer {config.api_key}"
        
        start_time = time.time()
        
        response = requests.post(
            config.endpoint_url,
            json=payload,
            headers=headers,
            timeout=config.timeout
        )
        
        response.raise_for_status()
        
        processing_time = time.time() - start_time
        self._update_response_time(processing_time)
        
        self.logger.info(f"Webhook送信成功: {config.name} ({processing_time:.2f}s)")
    
    async def _send_slack_message(self, config: ExternalSystemConfig, event: IntegrationEvent):
        """Slackメッセージ送信"""
        if event.event_type == "analysis_result":
            message = self._format_slack_analysis_message(event.data)
        elif event.event_type == "quality_alert":
            message = self._format_slack_alert_message(event.data)
        else:
            message = f"イベント: {event.event_type}\n```{json.dumps(event.data, indent=2, ensure_ascii=False)}```"
        
        payload = {
            "text": message,
            "username": "統一設計ツール",
            "icon_emoji": ":gear:"
        }
        
        response = requests.post(
            config.endpoint_url,
            json=payload,
            timeout=config.timeout
        )
        
        response.raise_for_status()
        self.logger.info(f"Slackメッセージ送信成功: {config.name}")
    
    async def _send_teams_message(self, config: ExternalSystemConfig, event: IntegrationEvent):
        """Teamsメッセージ送信"""
        if event.event_type == "analysis_result":
            card = self._format_teams_analysis_card(event.data)
        elif event.event_type == "quality_alert":
            card = self._format_teams_alert_card(event.data)
        else:
            card = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "summary": f"統一設計ツール: {event.event_type}",
                "themeColor": "0076D7",
                "sections": [{
                    "activityTitle": f"イベント: {event.event_type}",
                    "text": f"```{json.dumps(event.data, indent=2, ensure_ascii=False)}```"
                }]
            }
        
        response = requests.post(
            config.endpoint_url,
            json=card,
            timeout=config.timeout
        )
        
        response.raise_for_status()
        self.logger.info(f"Teamsメッセージ送信成功: {config.name}")
    
    async def _create_jira_issue(self, config: ExternalSystemConfig, event: IntegrationEvent):
        """JIRA課題作成"""
        if event.event_type != "quality_alert":
            return  # 品質アラートのみJIRA課題として作成
        
        data = event.data
        
        issue_data = {
            "fields": {
                "project": {"key": "DESIGN"},  # プロジェクトキーは設定で指定
                "summary": f"設計書品質問題: {data.get('file_path', 'Unknown')}",
                "description": self._format_jira_description(data),
                "issuetype": {"name": "Bug"},
                "priority": {"name": self._map_priority_to_jira(data.get('priority', 'normal'))}
            }
        }
        
        auth = None
        if config.username and config.password:
            auth = (config.username, config.password)
        
        headers = {"Content-Type": "application/json"}
        if config.api_key:
            headers["Authorization"] = f"Bearer {config.api_key}"
        
        response = requests.post(
            urljoin(config.endpoint_url, "/rest/api/2/issue"),
            json=issue_data,
            headers=headers,
            auth=auth,
            timeout=config.timeout
        )
        
        response.raise_for_status()
        self.logger.info(f"JIRA課題作成成功: {config.name}")
    
    async def _create_github_issue(self, config: ExternalSystemConfig, event: IntegrationEvent):
        """GitHub Issue作成"""
        if event.event_type != "quality_alert":
            return
        
        data = event.data
        
        issue_data = {
            "title": f"設計書品質問題: {data.get('file_path', 'Unknown')}",
            "body": self._format_github_issue_body(data),
            "labels": ["quality", "documentation", data.get('priority', 'normal')]
        }
        
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {config.api_key}"
        }
        
        response = requests.post(
            urljoin(config.endpoint_url, "/issues"),
            json=issue_data,
            headers=headers,
            timeout=config.timeout
        )
        
        response.raise_for_status()
        self.logger.info(f"GitHub Issue作成成功: {config.name}")
    
    async def _send_generic_api_request(self, config: ExternalSystemConfig, event: IntegrationEvent):
        """汎用API リクエスト送信"""
        payload = {
            "event": asdict(event),
            "timestamp": datetime.now().isoformat()
        }
        
        headers = {"Content-Type": "application/json"}
        if config.headers:
            headers.update(config.headers)
        
        if config.api_key:
            headers["Authorization"] = f"Bearer {config.api_key}"
        
        response = requests.post(
            config.endpoint_url,
            json=payload,
            headers=headers,
            timeout=config.timeout
        )
        
        response.raise_for_status()
        self.logger.info(f"汎用API送信成功: {config.name}")
    
    def _check_rate_limit(self, system_name: str) -> bool:
        """レート制限チェック"""
        current_time = time.time()
        
        if system_name not in self.rate_limiters:
            self.rate_limiters[system_name] = {
                "requests": [],
                "limit": self.external_systems[system_name].rate_limit
            }
        
        limiter = self.rate_limiters[system_name]
        
        # 1分以内のリクエストをカウント
        minute_ago = current_time - 60
        limiter["requests"] = [req_time for req_time in limiter["requests"] if req_time > minute_ago]
        
        if len(limiter["requests"]) >= limiter["limit"]:
            return False
        
        limiter["requests"].append(current_time)
        return True
    
    def _update_response_time(self, processing_time: float):
        """レスポンス時間統計を更新"""
        total_requests = self.integration_stats["total_requests"]
        current_avg = self.integration_stats["avg_response_time"]
        
        new_avg = (current_avg * total_requests + processing_time) / (total_requests + 1)
        self.integration_stats["avg_response_time"] = new_avg
    
    def _format_slack_analysis_message(self, data: Dict[str, Any]) -> str:
        """Slack用分析結果メッセージをフォーマット"""
        priority_emoji = {
            "critical": ":red_circle:",
            "high": ":orange_circle:",
            "medium": ":yellow_circle:",
            "low": ":green_circle:"
        }
        
        emoji = priority_emoji.get(data.get('priority', 'medium'), ":white_circle:")
        
        message = f"{emoji} *設計書分析結果*\n"
        message += f"ファイル: `{data.get('target_file', 'Unknown')}`\n"
        message += f"スコア: {data.get('score', 0):.1f}/100\n"
        message += f"優先度: {data.get('priority', 'medium')}\n"
        
        if data.get('issues'):
            message += f"\n*問題点:*\n"
            for issue in data['issues'][:3]:  # 最初の3つのみ表示
                message += f"• {issue}\n"
        
        if data.get('suggestions'):
            message += f"\n*改善提案:*\n"
            for suggestion in data['suggestions'][:2]:  # 最初の2つのみ表示
                message += f"• {suggestion}\n"
        
        return message
    
    def _format_slack_alert_message(self, data: Dict[str, Any]) -> str:
        """Slack用アラートメッセージをフォーマット"""
        priority_emoji = {
            "critical": ":rotating_light:",
            "high": ":warning:",
            "medium": ":information_source:",
            "low": ":white_check_mark:"
        }
        
        emoji = priority_emoji.get(data.get('priority', 'medium'), ":information_source:")
        
        message = f"{emoji} *品質アラート*\n"
        message += f"ファイル: `{data.get('file_path', 'Unknown')}`\n"
        message += f"優先度: {data.get('priority', 'medium')}\n"
        
        if data.get('issues'):
            message += f"\n*検出された問題:*\n"
            for issue in data['issues']:
                message += f"• {issue}\n"
        
        return message
    
    def _format_teams_analysis_card(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Teams用分析結果カードをフォーマット"""
        color_map = {
            "critical": "FF0000",
            "high": "FF8C00",
            "medium": "FFD700",
            "low": "32CD32"
        }
        
        color = color_map.get(data.get('priority', 'medium'), "0076D7")
        
        return {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "summary": "設計書分析結果",
            "themeColor": color,
            "sections": [{
                "activityTitle": "設計書分析結果",
                "activitySubtitle": f"ファイル: {data.get('target_file', 'Unknown')}",
                "facts": [
                    {"name": "スコア", "value": f"{data.get('score', 0):.1f}/100"},
                    {"name": "優先度", "value": data.get('priority', 'medium')},
                    {"name": "問題数", "value": str(len(data.get('issues', [])))}
                ],
                "text": "\n".join(data.get('issues', [])[:3])
            }]
        }
    
    def _format_teams_alert_card(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Teams用アラートカードをフォーマット"""
        return {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "summary": "品質アラート",
            "themeColor": "FF0000",
            "sections": [{
                "activityTitle": "品質アラート",
                "activitySubtitle": f"ファイル: {data.get('file_path', 'Unknown')}",
                "facts": [
                    {"name": "優先度", "value": data.get('priority', 'medium')},
                    {"name": "検出時刻", "value": data.get('timestamp', 'Unknown')}
                ],
                "text": "\n".join(data.get('issues', []))
            }]
        }
    
    def _format_jira_description(self, data: Dict[str, Any]) -> str:
        """JIRA用説明文をフォーマット"""
        description = f"設計書品質問題が検出されました。\n\n"
        description += f"*ファイル:* {data.get('file_path', 'Unknown')}\n"
        description += f"*優先度:* {data.get('priority', 'medium')}\n"
        description += f"*検出時刻:* {data.get('timestamp', 'Unknown')}\n\n"
        
        if data.get('issues'):
            description += "*検出された問題:*\n"
            for issue in data['issues']:
                description += f"* {issue}\n"
        
        return description
    
    def _format_github_issue_body(self, data: Dict[str, Any]) -> str:
        """GitHub Issue用本文をフォーマット"""
        body = f"## 設計書品質問題\n\n"
        body += f"**ファイル:** `{data.get('file_path', 'Unknown')}`\n"
        body += f"**優先度:** {data.get('priority', 'medium')}\n"
        body += f"**検出時刻:** {data.get('timestamp', 'Unknown')}\n\n"
        
        if data.get('issues'):
            body += "### 検出された問題\n\n"
            for issue in data['issues']:
                body += f"- {issue}\n"
        
        body += "\n---\n*このIssueは統一設計ツールにより自動生成されました*"
        
        return body
    
    def _map_priority_to_jira(self, priority: str) -> str:
        """優先度をJIRA形式にマッピング"""
        mapping = {
            "critical": "Highest",
            "high": "High",
            "medium": "Medium",
            "low": "Low"
        }
        return mapping.get(priority, "Medium")
    
    def get_integration_status(self) -> Dict[str, Any]:
        """統合状況を取得"""
        return {
            "external_systems": {
                name: {
                    "name": config.name,
                    "type": config.integration_type.value,
                    "enabled": config.enabled,
                    "endpoint": config.endpoint_url
                }
                for name, config in self.external_systems.items()
            },
            "statistics": self.integration_stats,
            "event_queue_size": self.event_queue.qsize(),
            "processing_active": self.processing_events
        }
    
    def add_external_system(self, config: ExternalSystemConfig):
        """外部システムを追加"""
        self.external_systems[config.name] = config
        self.logger.info(f"外部システムを追加しました: {config.name}")
    
    def remove_external_system(self, name: str):
        """外部システムを削除"""
        if name in self.external_systems:
            del self.external_systems[name]
            self.logger.info(f"外部システムを削除しました: {name}")
    
    def enable_system(self, name: str):
        """外部システムを有効化"""
        if name in self.external_systems:
            self.external_systems[name].enabled = True
            self.logger.info(f"外部システムを有効化しました: {name}")
    
    def disable_system(self, name: str):
        """外部システムを無効化"""
        if name in self.external_systems:
            self.external_systems[name].enabled = False
            self.logger.info(f"外部システムを無効化しました: {name}")


# 使用例とテスト関数
async def test_external_api_integration():
    """外部API統合のテスト"""
    # 外部APIマネージャーを初期化
    api_manager = ExternalAPIManager("skill-report-web")
    
    # Slack統合を追加
    slack_config = ExternalSystemConfig(
        name="slack_notifications",
        integration_type=IntegrationType.SLACK,
        endpoint_url="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
        enabled=True
    )
    api_manager.add_external_system(slack_config)
    
    # イベント処理を開始
    await api_manager.start_event_processing()
    
    # テスト用の品質アラートを送信
    await api_manager.send_quality_alert(
        file_path="docs/design/api/test.md",
        issues=["エグゼクティブサマリーが不足", "要求仕様IDが未記載"],
        priority="high"
    )
    
    # 少し待機
    await asyncio.sleep(2)
    
    # 統合状況を確認
    status = api_manager.get_integration_status()
    print(f"統合状況: {json.dumps(status, indent=2, ensure_ascii=False)}")
    
    # イベント処理を停止
    await api_manager.stop_event_processing()


if __name__ == "__main__":
    # テスト実行
    asyncio.run(test_external_api_integration())
