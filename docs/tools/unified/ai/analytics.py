#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統一設計ツールシステム - リアルタイム分析機能

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md

設計書の品質分析、整合性チェック、改善提案をリアルタイムで実行し、
継続的な品質向上を支援します。
"""

import os
import json
import time
import asyncio
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import logging
import threading
from collections import defaultdict

from ..config.schema import UnifiedConfig
from ..core.validation import UnifiedValidationEngine
from .integrations import AIIntegrationManager


class AnalysisType(Enum):
    """分析タイプ"""
    QUALITY_SCORE = "quality_score"
    CONSISTENCY_CHECK = "consistency_check"
    COMPLETENESS_CHECK = "completeness_check"
    IMPROVEMENT_SUGGESTIONS = "improvement_suggestions"
    TREND_ANALYSIS = "trend_analysis"
    PERFORMANCE_METRICS = "performance_metrics"


class AnalysisPriority(Enum):
    """分析優先度"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class AnalysisMetric:
    """分析メトリクス"""
    name: str
    value: float
    max_value: float = 100.0
    unit: str = ""
    description: str = ""
    trend: str = "stable"  # improving, declining, stable
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class AnalysisResult:
    """分析結果"""
    analysis_type: AnalysisType
    target_file: str
    score: float
    metrics: List[AnalysisMetric] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    priority: AnalysisPriority = AnalysisPriority.MEDIUM
    timestamp: datetime = field(default_factory=datetime.now)
    processing_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalysisContext:
    """分析コンテキスト"""
    target_files: List[str] = field(default_factory=list)
    analysis_types: List[AnalysisType] = field(default_factory=list)
    include_ai_analysis: bool = True
    real_time_mode: bool = False
    threshold_scores: Dict[str, float] = field(default_factory=dict)
    custom_rules: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class QualityAnalyzer:
    """品質分析器"""
    
    def __init__(self, config: UnifiedConfig):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.QualityAnalyzer")
        
        # 品質評価基準
        self.quality_criteria = {
            "executive_summary": {"weight": 0.2, "min_length": 50},
            "structure": {"weight": 0.15, "required_sections": ["概要", "詳細"]},
            "completeness": {"weight": 0.2, "required_fields": []},
            "consistency": {"weight": 0.15, "naming_rules": True},
            "technical_depth": {"weight": 0.15, "min_technical_terms": 5},
            "readability": {"weight": 0.15, "max_complexity": 10}
        }
    
    def analyze_document_quality(self, file_path: str, content: str) -> AnalysisResult:
        """文書品質分析"""
        start_time = time.time()
        
        try:
            # 各品質基準を評価
            scores = {}
            issues = []
            suggestions = []
            
            # エグゼクティブサマリー評価
            exec_score, exec_issues, exec_suggestions = self._analyze_executive_summary(content)
            scores["executive_summary"] = exec_score
            issues.extend(exec_issues)
            suggestions.extend(exec_suggestions)
            
            # 構造評価
            struct_score, struct_issues, struct_suggestions = self._analyze_structure(content)
            scores["structure"] = struct_score
            issues.extend(struct_issues)
            suggestions.extend(struct_suggestions)
            
            # 完全性評価
            complete_score, complete_issues, complete_suggestions = self._analyze_completeness(content)
            scores["completeness"] = complete_score
            issues.extend(complete_issues)
            suggestions.extend(complete_suggestions)
            
            # 一貫性評価
            consist_score, consist_issues, consist_suggestions = self._analyze_consistency(content)
            scores["consistency"] = consist_score
            issues.extend(consist_issues)
            suggestions.extend(consist_suggestions)
            
            # 技術的深度評価
            tech_score, tech_issues, tech_suggestions = self._analyze_technical_depth(content)
            scores["technical_depth"] = tech_score
            issues.extend(tech_issues)
            suggestions.extend(tech_suggestions)
            
            # 可読性評価
            read_score, read_issues, read_suggestions = self._analyze_readability(content)
            scores["readability"] = read_score
            issues.extend(read_issues)
            suggestions.extend(read_suggestions)
            
            # 総合スコア計算
            total_score = sum(
                scores[criterion] * self.quality_criteria[criterion]["weight"]
                for criterion in scores
            )
            
            # メトリクス作成
            metrics = [
                AnalysisMetric(
                    name=criterion,
                    value=score,
                    description=f"{criterion}の品質スコア"
                )
                for criterion, score in scores.items()
            ]
            
            # 優先度決定
            if total_score < 60:
                priority = AnalysisPriority.CRITICAL
            elif total_score < 75:
                priority = AnalysisPriority.HIGH
            elif total_score < 85:
                priority = AnalysisPriority.MEDIUM
            else:
                priority = AnalysisPriority.LOW
            
            return AnalysisResult(
                analysis_type=AnalysisType.QUALITY_SCORE,
                target_file=file_path,
                score=total_score,
                metrics=metrics,
                issues=issues,
                suggestions=suggestions,
                priority=priority,
                processing_time=time.time() - start_time,
                metadata={
                    "detailed_scores": scores,
                    "content_length": len(content),
                    "word_count": len(content.split())
                }
            )
            
        except Exception as e:
            self.logger.error(f"品質分析エラー: {e}")
            return AnalysisResult(
                analysis_type=AnalysisType.QUALITY_SCORE,
                target_file=file_path,
                score=0.0,
                issues=[f"分析エラー: {e}"],
                processing_time=time.time() - start_time
            )
    
    def _analyze_executive_summary(self, content: str) -> Tuple[float, List[str], List[str]]:
        """エグゼクティブサマリー分析"""
        issues = []
        suggestions = []
        
        # エグゼクティブサマリーの存在チェック
        if "## エグゼクティブサマリー" not in content and "エグゼクティブサマリー" not in content:
            issues.append("エグゼクティブサマリーが見つかりません")
            suggestions.append("文書の冒頭にエグゼクティブサマリーを追加してください")
            return 0.0, issues, suggestions
        
        # エグゼクティブサマリーの内容を抽出
        lines = content.split('\n')
        summary_content = ""
        in_summary = False
        
        for line in lines:
            if "エグゼクティブサマリー" in line:
                in_summary = True
                continue
            elif in_summary and line.startswith('#'):
                break
            elif in_summary:
                summary_content += line + " "
        
        # 長さチェック
        summary_length = len(summary_content.strip())
        min_length = self.quality_criteria["executive_summary"]["min_length"]
        
        if summary_length < min_length:
            issues.append(f"エグゼクティブサマリーが短すぎます（{summary_length}文字 < {min_length}文字）")
            suggestions.append("エグゼクティブサマリーをより詳細に記述してください")
            score = summary_length / min_length * 100
        else:
            score = 100.0
        
        # 内容の質チェック
        if "この文書は" not in summary_content:
            issues.append("エグゼクティブサマリーに文書の目的が明記されていません")
            suggestions.append("「この文書は...」で始まる目的説明を追加してください")
            score *= 0.8
        
        return min(score, 100.0), issues, suggestions
    
    def _analyze_structure(self, content: str) -> Tuple[float, List[str], List[str]]:
        """構造分析"""
        issues = []
        suggestions = []
        score = 100.0
        
        # 見出し構造の分析
        lines = content.split('\n')
        headings = [line for line in lines if line.startswith('#')]
        
        if len(headings) < 3:
            issues.append("見出しが少なすぎます")
            suggestions.append("適切な見出し構造を作成してください")
            score *= 0.7
        
        # 必須セクションのチェック
        required_sections = ["概要", "詳細", "仕様"]
        missing_sections = []
        
        for section in required_sections:
            if not any(section in heading for heading in headings):
                missing_sections.append(section)
        
        if missing_sections:
            issues.append(f"必須セクションが不足: {', '.join(missing_sections)}")
            suggestions.append("不足している必須セクションを追加してください")
            score *= (1 - len(missing_sections) / len(required_sections) * 0.5)
        
        return score, issues, suggestions
    
    def _analyze_completeness(self, content: str) -> Tuple[float, List[str], List[str]]:
        """完全性分析"""
        issues = []
        suggestions = []
        score = 100.0
        
        # 要求仕様IDの存在チェック
        if "要求仕様ID" not in content:
            issues.append("要求仕様IDが記載されていません")
            suggestions.append("対応する要求仕様IDを明記してください")
            score *= 0.8
        
        # 設計書参照の存在チェック
        if "設計書:" not in content and "docs/" not in content:
            issues.append("関連設計書への参照がありません")
            suggestions.append("関連する設計書への参照を追加してください")
            score *= 0.9
        
        # 実装日・実装者の記載チェック
        if "実装日" not in content and "作成日" not in content:
            issues.append("作成日が記載されていません")
            suggestions.append("文書の作成日を明記してください")
            score *= 0.95
        
        return score, issues, suggestions
    
    def _analyze_consistency(self, content: str) -> Tuple[float, List[str], List[str]]:
        """一貫性分析"""
        issues = []
        suggestions = []
        score = 100.0
        
        # 命名規則の一貫性チェック
        # テーブル名、API名、画面IDなどの命名パターンを確認
        
        # 用語の一貫性チェック
        inconsistent_terms = self._check_term_consistency(content)
        if inconsistent_terms:
            issues.extend([f"用語の不一致: {term}" for term in inconsistent_terms])
            suggestions.append("用語の統一を行ってください")
            score *= 0.9
        
        return score, issues, suggestions
    
    def _analyze_technical_depth(self, content: str) -> Tuple[float, List[str], List[str]]:
        """技術的深度分析"""
        issues = []
        suggestions = []
        
        # 技術用語の数をカウント
        technical_terms = [
            "API", "データベース", "テーブル", "インデックス", "クエリ",
            "レスポンス", "リクエスト", "認証", "認可", "暗号化",
            "パフォーマンス", "スケーラビリティ", "可用性"
        ]
        
        term_count = sum(content.lower().count(term.lower()) for term in technical_terms)
        min_terms = self.quality_criteria["technical_depth"]["min_technical_terms"]
        
        if term_count < min_terms:
            issues.append("技術的詳細が不足しています")
            suggestions.append("技術的な詳細説明を追加してください")
            score = (term_count / min_terms) * 100
        else:
            score = 100.0
        
        return min(score, 100.0), issues, suggestions
    
    def _analyze_readability(self, content: str) -> Tuple[float, List[str], List[str]]:
        """可読性分析"""
        issues = []
        suggestions = []
        score = 100.0
        
        # 文の長さチェック
        sentences = content.replace('。', '.').split('.')
        long_sentences = [s for s in sentences if len(s) > 100]
        
        if long_sentences:
            issues.append(f"長すぎる文が{len(long_sentences)}個あります")
            suggestions.append("文を短く分割して可読性を向上させてください")
            score *= 0.9
        
        # 箇条書きの使用チェック
        if content.count('-') < 3 and content.count('*') < 3:
            suggestions.append("箇条書きを使用して情報を整理してください")
            score *= 0.95
        
        return score, issues, suggestions
    
    def _check_term_consistency(self, content: str) -> List[str]:
        """用語の一貫性チェック"""
        inconsistent_terms = []
        
        # よくある不一致パターン
        term_patterns = [
            (["ユーザー", "ユーザ"], "ユーザー表記の不統一"),
            (["データベース", "DB"], "データベース表記の不統一"),
            (["API", "api"], "API表記の不統一")
        ]
        
        for patterns, description in term_patterns:
            found_patterns = [p for p in patterns if p in content]
            if len(found_patterns) > 1:
                inconsistent_terms.append(description)
        
        return inconsistent_terms


class ConsistencyAnalyzer:
    """整合性分析器"""
    
    def __init__(self, config: UnifiedConfig):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.ConsistencyAnalyzer")
    
    def analyze_cross_document_consistency(self, file_paths: List[str]) -> AnalysisResult:
        """複数文書間の整合性分析"""
        start_time = time.time()
        
        try:
            documents = {}
            for file_path in file_paths:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        documents[file_path] = f.read()
                except Exception as e:
                    self.logger.warning(f"ファイル読み込みエラー {file_path}: {e}")
            
            issues = []
            suggestions = []
            metrics = []
            
            # 要求仕様IDの整合性チェック
            req_id_consistency = self._check_requirement_id_consistency(documents)
            issues.extend(req_id_consistency["issues"])
            suggestions.extend(req_id_consistency["suggestions"])
            metrics.append(AnalysisMetric(
                name="requirement_id_consistency",
                value=req_id_consistency["score"],
                description="要求仕様IDの整合性"
            ))
            
            # 命名規則の整合性チェック
            naming_consistency = self._check_naming_consistency(documents)
            issues.extend(naming_consistency["issues"])
            suggestions.extend(naming_consistency["suggestions"])
            metrics.append(AnalysisMetric(
                name="naming_consistency",
                value=naming_consistency["score"],
                description="命名規則の整合性"
            ))
            
            # データ構造の整合性チェック
            data_consistency = self._check_data_structure_consistency(documents)
            issues.extend(data_consistency["issues"])
            suggestions.extend(data_consistency["suggestions"])
            metrics.append(AnalysisMetric(
                name="data_structure_consistency",
                value=data_consistency["score"],
                description="データ構造の整合性"
            ))
            
            # 総合スコア計算
            total_score = sum(metric.value for metric in metrics) / len(metrics) if metrics else 0
            
            # 優先度決定
            if total_score < 70:
                priority = AnalysisPriority.CRITICAL
            elif total_score < 85:
                priority = AnalysisPriority.HIGH
            else:
                priority = AnalysisPriority.MEDIUM
            
            return AnalysisResult(
                analysis_type=AnalysisType.CONSISTENCY_CHECK,
                target_file=", ".join(file_paths),
                score=total_score,
                metrics=metrics,
                issues=issues,
                suggestions=suggestions,
                priority=priority,
                processing_time=time.time() - start_time,
                metadata={
                    "documents_analyzed": len(documents),
                    "total_content_length": sum(len(content) for content in documents.values())
                }
            )
            
        except Exception as e:
            self.logger.error(f"整合性分析エラー: {e}")
            return AnalysisResult(
                analysis_type=AnalysisType.CONSISTENCY_CHECK,
                target_file=", ".join(file_paths),
                score=0.0,
                issues=[f"分析エラー: {e}"],
                processing_time=time.time() - start_time
            )
    
    def _check_requirement_id_consistency(self, documents: Dict[str, str]) -> Dict[str, Any]:
        """要求仕様IDの整合性チェック"""
        issues = []
        suggestions = []
        
        # 各文書から要求仕様IDを抽出
        req_ids = {}
        for file_path, content in documents.items():
            ids = self._extract_requirement_ids(content)
            req_ids[file_path] = ids
        
        # 重複チェック
        all_ids = []
        for ids in req_ids.values():
            all_ids.extend(ids)
        
        duplicates = [id for id in set(all_ids) if all_ids.count(id) > 1]
        if duplicates:
            issues.append(f"重複する要求仕様ID: {', '.join(duplicates)}")
            suggestions.append("要求仕様IDの重複を解消してください")
        
        # 命名規則チェック
        invalid_ids = [id for id in all_ids if not self._is_valid_requirement_id(id)]
        if invalid_ids:
            issues.append(f"命名規則に従わない要求仕様ID: {', '.join(invalid_ids)}")
            suggestions.append("要求仕様IDの命名規則を統一してください")
        
        # スコア計算
        total_ids = len(all_ids)
        valid_ids = total_ids - len(duplicates) - len(invalid_ids)
        score = (valid_ids / total_ids * 100) if total_ids > 0 else 100
        
        return {
            "score": score,
            "issues": issues,
            "suggestions": suggestions
        }
    
    def _check_naming_consistency(self, documents: Dict[str, str]) -> Dict[str, Any]:
        """命名規則の整合性チェック"""
        issues = []
        suggestions = []
        
        # テーブル名、API名、画面IDなどの命名パターンを確認
        naming_patterns = {
            "table_names": [],
            "api_names": [],
            "screen_ids": []
        }
        
        for file_path, content in documents.items():
            # テーブル名を抽出
            if "テーブル" in content or "TABLE" in content:
                table_names = self._extract_table_names(content)
                naming_patterns["table_names"].extend(table_names)
            
            # API名を抽出
            if "API" in content:
                api_names = self._extract_api_names(content)
                naming_patterns["api_names"].extend(api_names)
            
            # 画面IDを抽出
            if "画面" in content or "SCR" in content:
                screen_ids = self._extract_screen_ids(content)
                naming_patterns["screen_ids"].extend(screen_ids)
        
        # 命名規則の一貫性をチェック
        consistency_score = 100.0
        
        for pattern_type, names in naming_patterns.items():
            if names:
                inconsistent_count = self._count_naming_inconsistencies(names)
                if inconsistent_count > 0:
                    issues.append(f"{pattern_type}の命名規則に不一致があります")
                    suggestions.append(f"{pattern_type}の命名規則を統一してください")
                    consistency_score *= 0.8
        
        return {
            "score": consistency_score,
            "issues": issues,
            "suggestions": suggestions
        }
    
    def _check_data_structure_consistency(self, documents: Dict[str, str]) -> Dict[str, Any]:
        """データ構造の整合性チェック"""
        issues = []
        suggestions = []
        
        # データ構造の定義を抽出
        data_structures = {}
        for file_path, content in documents.items():
            structures = self._extract_data_structures(content)
            data_structures[file_path] = structures
        
        # 同じエンティティの定義が一致しているかチェック
        entity_definitions = defaultdict(list)
        for file_path, structures in data_structures.items():
            for entity_name, definition in structures.items():
                entity_definitions[entity_name].append((file_path, definition))
        
        consistency_score = 100.0
        
        for entity_name, definitions in entity_definitions.items():
            if len(definitions) > 1:
                # 複数の定義がある場合、一致しているかチェック
                first_def = definitions[0][1]
                for file_path, definition in definitions[1:]:
                    if definition != first_def:
                        issues.append(f"エンティティ'{entity_name}'の定義が不一致: {file_path}")
                        suggestions.append(f"エンティティ'{entity_name}'の定義を統一してください")
                        consistency_score *= 0.9
        
        return {
            "score": consistency_score,
            "issues": issues,
            "suggestions": suggestions
        }
    
    def _extract_requirement_ids(self, content: str) -> List[str]:
        """要求仕様IDを抽出"""
        import re
        pattern = r'[A-Z]{3}\.\d+-[A-Z]+\.\d+'
        return re.findall(pattern, content)
    
    def _is_valid_requirement_id(self, req_id: str) -> bool:
        """要求仕様IDの妥当性チェック"""
        import re
        pattern = r'^[A-Z]{3}\.\d+-[A-Z]+\.\d+$'
        return bool(re.match(pattern, req_id))
    
    def _extract_table_names(self, content: str) -> List[str]:
        """テーブル名を抽出"""
        import re
        patterns = [
            r'MST_[A-Z_]+',
            r'TRN_[A-Z_]+',
            r'HIS_[A-Z_]+',
            r'SYS_[A-Z_]+'
        ]
        
        table_names = []
        for pattern in patterns:
            table_names.extend(re.findall(pattern, content))
        
        return list(set(table_names))
    
    def _extract_api_names(self, content: str) -> List[str]:
        """API名を抽出"""
        import re
        pattern = r'API-\d{3}'
        return re.findall(pattern, content)
    
    def _extract_screen_ids(self, content: str) -> List[str]:
        """画面IDを抽出"""
        import re
        pattern = r'SCR-[A-Z]+'
        return re.findall(pattern, content)
    
    def _count_naming_inconsistencies(self, names: List[str]) -> int:
        """命名の不一致数をカウント"""
        # 簡単な実装：プレフィックスの一貫性をチェック
        if not names:
            return 0
        
        prefixes = [name.split('_')[0] if '_' in name else name.split('-')[0] for name in names]
        unique_prefixes = set(prefixes)
        
        # 期待されるプレフィックス数と実際の数の差
        expected_prefixes = 1  # 通常は1つのプレフィックスが期待される
        return max(0, len(unique_prefixes) - expected_prefixes)
    
    def _extract_data_structures(self, content: str) -> Dict[str, str]:
        """データ構造を抽出"""
        # 簡単な実装：テーブル定義やインターフェース定義を抽出
        structures = {}
        
        lines = content.split('\n')
        current_structure = None
        current_definition = []
        
        for line in lines:
            if 'interface' in line.lower() or 'table' in line.lower():
                if current_structure:
                    structures[current_structure] = '\n'.join(current_definition)
                current_structure = line.strip()
                current_definition = [line]
            elif current_structure and (line.startswith('  ') or line.startswith('\t')):
                current_definition.append(line)
            elif current_structure and line.strip() == '':
                continue
            elif current_structure:
                structures[current_structure] = '\n'.join(current_definition)
                current_structure = None
                current_definition = []
        
        if current_structure:
            structures[current_structure] = '\n'.join(current_definition)
        
        return structures


class RealTimeAnalyticsEngine:
    """リアルタイム分析エンジン"""
    
    def __init__(self, config: UnifiedConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 分析器を初期化
        self.quality_analyzer = QualityAnalyzer(config)
        self.consistency_analyzer = ConsistencyAnalyzer(config)
        self.validation_engine = UnifiedValidationEngine("default")
        
        # AI統合（オプション）
        try:
            self.ai_integration = AIIntegrationManager(config)
        except Exception as e:
            self.logger.warning(f"AI統合の初期化に失敗: {e}")
            self.ai_integration = None
        
        # リアルタイム監視
        self.monitoring_active = False
        self.monitoring_thread = None
        self.file_watchers = {}
        self.analysis_queue = asyncio.Queue()
        
        # 分析結果キャッシュ
        self.analysis_cache = {}
        self.cache_ttl = timedelta(minutes=30)
        
        # メトリクス追跡
        self.metrics_history = defaultdict(list)
        self.performance_stats = {
            "total_analyses": 0,
            "avg_processing_time": 0.0,
            "cache_hit_rate": 0.0
        }
    
    def start_real_time_monitoring(self, watch_directories: List[str]):
        """リアルタイム監視開始"""
        if self.monitoring_active:
            self.logger.warning("リアルタイム監視は既に開始されています")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(watch_directories,),
            daemon=True
        )
        self.monitoring_thread.start()
        self.logger.info(f"リアルタイム監視を開始しました: {watch_directories}")
    
    def stop_real_time_monitoring(self):
        """リアルタイム監視停止"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        self.logger.info("リアルタイム監視を停止しました")
    
    def _monitoring_loop(self, watch_directories: List[str]):
        """監視ループ"""
        try:
            import watchdog.observers
            import watchdog.events
            
            class FileChangeHandler(watchdog.events.FileSystemEventHandler):
                def __init__(self, analytics_engine):
                    self.analytics_engine = analytics_engine
                
                def on_modified(self, event):
                    if not event.is_directory and event.src_path.endswith('.md'):
                        # ファイル変更を分析キューに追加
                        self.analytics_engine._queue_analysis(event.src_path)
            
            observer = watchdog.observers.Observer()
            handler = FileChangeHandler(self)
            
            for directory in watch_directories:
                observer.schedule(handler, directory, recursive=True)
            
            observer.start()
            
            # 分析処理ループ
            while self.monitoring_active:
                try:
                    # 分析キューから処理
                    self._process_analysis_queue()
                    time.sleep(1)  # 1秒間隔で処理
                except Exception as e:
                    self.logger.error(f"分析処理エラー: {e}")
            
            observer.stop()
            observer.join()
            
        except ImportError:
            self.logger.warning("watchdogライブラリが利用できません。リアルタイム監視は無効です。")
        except Exception as e:
            self.logger.error(f"監視ループエラー: {e}")
    
    def _queue_analysis(self, file_path: str):
        """分析をキューに追加"""
        try:
            # 重複チェック
            if file_path not in self.analysis_queue._queue:
                asyncio.run_coroutine_threadsafe(
                    self.analysis_queue.put(file_path),
                    asyncio.new_event_loop()
                )
        except Exception as e:
            self.logger.error(f"分析キュー追加エラー: {e}")
    
    def _process_analysis_queue(self):
        """分析キューを処理"""
        try:
            while not self.analysis_queue.empty():
                file_path = self.analysis_queue.get_nowait()
                self._analyze_file_async(file_path)
        except asyncio.QueueEmpty:
            pass
        except Exception as e:
            self.logger.error(f"分析キュー処理エラー: {e}")
    
    def _analyze_file_async(self, file_path: str):
        """非同期ファイル分析"""
        try:
            # ファイル内容を読み込み
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 品質分析を実行
            result = self.quality_analyzer.analyze_document_quality(file_path, content)
            
            # 結果をキャッシュに保存
            self.analysis_cache[file_path] = {
                'result': result,
                'timestamp': datetime.now()
            }
            
            # メトリクス履歴を更新
            self._update_metrics_history(result)
            
            # 重要な問題がある場合はログ出力
            if result.priority in [AnalysisPriority.CRITICAL, AnalysisPriority.HIGH]:
                self.logger.warning(f"品質問題検出 [{result.priority.value}]: {file_path}")
                for issue in result.issues[:3]:  # 最初の3つの問題のみ表示
                    self.logger.warning(f"  - {issue}")
            
        except Exception as e:
            self.logger.error(f"ファイル分析エラー {file_path}: {e}")
    
    def analyze_document(self, file_path: str, context: Optional[AnalysisContext] = None) -> AnalysisResult:
        """文書分析（メインエントリーポイント）"""
        start_time = time.time()
        
        # キャッシュチェック
        cached_result = self._get_cached_result(file_path)
        if cached_result:
            self.performance_stats["cache_hit_rate"] += 1
            return cached_result
        
        try:
            # ファイル内容を読み込み
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 分析タイプを決定
            analysis_types = context.analysis_types if context else [AnalysisType.QUALITY_SCORE]
            
            results = []
            
            for analysis_type in analysis_types:
                if analysis_type == AnalysisType.QUALITY_SCORE:
                    result = self.quality_analyzer.analyze_document_quality(file_path, content)
                elif analysis_type == AnalysisType.COMPLETENESS_CHECK:
                    result = self._analyze_completeness(file_path, content)
                elif analysis_type == AnalysisType.IMPROVEMENT_SUGGESTIONS:
                    result = self._generate_improvement_suggestions(file_path, content, context)
                else:
                    # その他の分析タイプは基本分析を実行
                    result = self.quality_analyzer.analyze_document_quality(file_path, content)
                
                results.append(result)
            
            # 複数の分析結果を統合
            final_result = self._merge_analysis_results(results)
            
            # キャッシュに保存
            self.analysis_cache[file_path] = {
                'result': final_result,
                'timestamp': datetime.now()
            }
            
            # パフォーマンス統計を更新
            self._update_performance_stats(time.time() - start_time)
            
            return final_result
            
        except Exception as e:
            self.logger.error(f"文書分析エラー {file_path}: {e}")
            return AnalysisResult(
                analysis_type=AnalysisType.QUALITY_SCORE,
                target_file=file_path,
                score=0.0,
                issues=[f"分析エラー: {e}"],
                processing_time=time.time() - start_time
            )
    
    def analyze_multiple_documents(self, file_paths: List[str], context: Optional[AnalysisContext] = None) -> List[AnalysisResult]:
        """複数文書分析"""
        results = []
        
        # 個別文書分析
        for file_path in file_paths:
            result = self.analyze_document(file_path, context)
            results.append(result)
        
        # 整合性分析（複数文書間）
        if len(file_paths) > 1:
            consistency_result = self.consistency_analyzer.analyze_cross_document_consistency(file_paths)
            results.append(consistency_result)
        
        return results
    
    def get_analytics_dashboard_data(self) -> Dict[str, Any]:
        """分析ダッシュボード用データを取得"""
        dashboard_data = {
            "summary": {
                "total_documents": len(self.analysis_cache),
                "avg_quality_score": self._calculate_average_quality_score(),
                "critical_issues": self._count_critical_issues(),
                "last_updated": datetime.now().isoformat()
            },
            "metrics": {
                "quality_trends": self._get_quality_trends(),
                "issue_categories": self._get_issue_categories(),
                "performance_stats": self.performance_stats
            },
            "recent_analyses": self._get_recent_analyses(limit=10),
            "top_issues": self._get_top_issues(limit=5)
        }
        
        return dashboard_data
    
    def _get_cached_result(self, file_path: str) -> Optional[AnalysisResult]:
        """キャッシュから結果を取得"""
        if file_path in self.analysis_cache:
            cached_data = self.analysis_cache[file_path]
            if datetime.now() - cached_data['timestamp'] < self.cache_ttl:
                return cached_data['result']
            else:
                # 期限切れのキャッシュを削除
                del self.analysis_cache[file_path]
        return None
    
    def _merge_analysis_results(self, results: List[AnalysisResult]) -> AnalysisResult:
        """複数の分析結果を統合"""
        if not results:
            return AnalysisResult(
                analysis_type=AnalysisType.QUALITY_SCORE,
                target_file="",
                score=0.0
            )
        
        if len(results) == 1:
            return results[0]
        
        # 統合結果を作成
        merged_result = AnalysisResult(
            analysis_type=AnalysisType.QUALITY_SCORE,
            target_file=results[0].target_file,
            score=sum(r.score for r in results) / len(results),
            metrics=[],
            issues=[],
            suggestions=[],
            priority=AnalysisPriority.MEDIUM,
            processing_time=sum(r.processing_time for r in results)
        )
        
        # メトリクス、問題、提案を統合
        for result in results:
            merged_result.metrics.extend(result.metrics)
            merged_result.issues.extend(result.issues)
            merged_result.suggestions.extend(result.suggestions)
        
        # 重複を除去
        merged_result.issues = list(set(merged_result.issues))
        merged_result.suggestions = list(set(merged_result.suggestions))
        
        # 最高優先度を設定
        priorities = [r.priority for r in results]
        if AnalysisPriority.CRITICAL in priorities:
            merged_result.priority = AnalysisPriority.CRITICAL
        elif AnalysisPriority.HIGH in priorities:
            merged_result.priority = AnalysisPriority.HIGH
        elif AnalysisPriority.MEDIUM in priorities:
            merged_result.priority = AnalysisPriority.MEDIUM
        else:
            merged_result.priority = AnalysisPriority.LOW
        
        return merged_result
    
    def _analyze_completeness(self, file_path: str, content: str) -> AnalysisResult:
        """完全性分析"""
        start_time = time.time()
        
        issues = []
        suggestions = []
        score = 100.0
        
        # 必須セクションのチェック
        required_sections = [
            "エグゼクティブサマリー",
            "概要",
            "詳細仕様",
            "実装考慮事項"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            issues.append(f"必須セクションが不足: {', '.join(missing_sections)}")
            suggestions.append("不足している必須セクションを追加してください")
            score *= (1 - len(missing_sections) / len(required_sections) * 0.5)
        
        # 要求仕様IDの存在チェック
        if "要求仕様ID" not in content:
            issues.append("要求仕様IDが記載されていません")
            suggestions.append("対応する要求仕様IDを明記してください")
            score *= 0.8
        
        return AnalysisResult(
            analysis_type=AnalysisType.COMPLETENESS_CHECK,
            target_file=file_path,
            score=score,
            issues=issues,
            suggestions=suggestions,
            processing_time=time.time() - start_time
        )
    
    def _generate_improvement_suggestions(self, file_path: str, content: str, context: Optional[AnalysisContext]) -> AnalysisResult:
        """改善提案生成"""
        start_time = time.time()
        
        suggestions = []
        
        # AI統合が利用可能な場合はAI提案を生成
        if self.ai_integration and context and context.include_ai_analysis:
            try:
                ai_response = self.ai_integration.generate_content(
                    prompt=f"以下の設計書の改善提案を生成してください:\n\n{content[:2000]}",
                    model="gpt-4",
                    temperature=0.3,
                    max_tokens=1000
                )
                
                if ai_response["success"]:
                    suggestions.append(f"AI提案: {ai_response['content']}")
            except Exception as e:
                self.logger.warning(f"AI改善提案生成エラー: {e}")
        
        # 基本的な改善提案
        if len(content) < 500:
            suggestions.append("文書の内容をより詳細に記述することを推奨します")
        
        if content.count('\n#') < 3:
            suggestions.append("適切な見出し構造を作成することを推奨します")
        
        if "図" not in content and "表" not in content:
            suggestions.append("図表を追加して理解しやすさを向上させることを推奨します")
        
        return AnalysisResult(
            analysis_type=AnalysisType.IMPROVEMENT_SUGGESTIONS,
            target_file=file_path,
            score=80.0,  # 提案なので固定スコア
            suggestions=suggestions,
            processing_time=time.time() - start_time
        )
    
    def _update_metrics_history(self, result: AnalysisResult):
        """メトリクス履歴を更新"""
        timestamp = datetime.now()
        
        for metric in result.metrics:
            self.metrics_history[metric.name].append({
                'timestamp': timestamp,
                'value': metric.value,
                'file': result.target_file
            })
        
        # 履歴サイズを制限（最新100件）
        for metric_name in self.metrics_history:
            if len(self.metrics_history[metric_name]) > 100:
                self.metrics_history[metric_name] = self.metrics_history[metric_name][-100:]
    
    def _update_performance_stats(self, processing_time: float):
        """パフォーマンス統計を更新"""
        self.performance_stats["total_analyses"] += 1
        
        # 平均処理時間を更新
        total_time = (self.performance_stats["avg_processing_time"] * 
                     (self.performance_stats["total_analyses"] - 1) + processing_time)
        self.performance_stats["avg_processing_time"] = total_time / self.performance_stats["total_analyses"]
    
    def _calculate_average_quality_score(self) -> float:
        """平均品質スコアを計算"""
        if not self.analysis_cache:
            return 0.0
        
        total_score = sum(data['result'].score for data in self.analysis_cache.values())
        return total_score / len(self.analysis_cache)
    
    def _count_critical_issues(self) -> int:
        """重要な問題の数をカウント"""
        count = 0
        for data in self.analysis_cache.values():
            if data['result'].priority in [AnalysisPriority.CRITICAL, AnalysisPriority.HIGH]:
                count += 1
        return count
    
    def _get_quality_trends(self) -> List[Dict[str, Any]]:
        """品質トレンドを取得"""
        trends = []
        
        for metric_name, history in self.metrics_history.items():
            if history:
                recent_values = [h['value'] for h in history[-10:]]  # 最新10件
                trend_data = {
                    'metric': metric_name,
                    'current_value': recent_values[-1] if recent_values else 0,
                    'trend': 'improving' if len(recent_values) > 1 and recent_values[-1] > recent_values[0] else 'stable',
                    'history': recent_values
                }
                trends.append(trend_data)
        
        return trends
    
    def _get_issue_categories(self) -> Dict[str, int]:
        """問題カテゴリ別の集計を取得"""
        categories = defaultdict(int)
        
        for data in self.analysis_cache.values():
            for issue in data['result'].issues:
                # 問題の種類を分類
                if "エグゼクティブサマリー" in issue:
                    categories["エグゼクティブサマリー"] += 1
                elif "構造" in issue or "見出し" in issue:
                    categories["文書構造"] += 1
                elif "要求仕様ID" in issue:
                    categories["要求仕様"] += 1
                elif "技術" in issue:
                    categories["技術的詳細"] += 1
                else:
                    categories["その他"] += 1
        
        return dict(categories)
    
    def _get_recent_analyses(self, limit: int = 10) -> List[Dict[str, Any]]:
        """最近の分析結果を取得"""
        recent = []
        
        # タイムスタンプでソート
        sorted_cache = sorted(
            self.analysis_cache.items(),
            key=lambda x: x[1]['timestamp'],
            reverse=True
        )
        
        for file_path, data in sorted_cache[:limit]:
            result = data['result']
            recent.append({
                'file': file_path,
                'score': result.score,
                'priority': result.priority.value,
                'issues_count': len(result.issues),
                'timestamp': data['timestamp'].isoformat()
            })
        
        return recent
    
    def _get_top_issues(self, limit: int = 5) -> List[Dict[str, Any]]:
        """頻出問題を取得"""
        issue_counts = defaultdict(int)
        
        for data in self.analysis_cache.values():
            for issue in data['result'].issues:
                issue_counts[issue] += 1
        
        # 頻度でソート
        sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {'issue': issue, 'count': count}
            for issue, count in sorted_issues[:limit]
        ]
