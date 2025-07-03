#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統一設計ツールシステム - Web UIダッシュボード

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md

リアルタイム分析結果を可視化するWebダッシュボードを提供し、
設計書の品質状況を直感的に把握できるインターフェースを実現します。
"""

import os
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, send_from_directory
import threading
import logging

from .analytics import RealTimeAnalyticsEngine, AnalysisType, AnalysisPriority
from ..config.manager import UnifiedConfigManager


@dataclass
class DashboardConfig:
    """ダッシュボード設定"""
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    auto_refresh_interval: int = 30  # 秒
    max_history_points: int = 100
    theme: str = "light"  # light, dark
    enable_real_time: bool = True


class AnalyticsDashboard:
    """分析ダッシュボード"""
    
    def __init__(self, project_name: str = "default", config: Optional[DashboardConfig] = None):
        self.project_name = project_name
        self.config = config or DashboardConfig()
        self.logger = logging.getLogger(__name__)
        
        # Flask アプリケーションを初期化
        self.app = Flask(__name__, 
                        template_folder=self._get_template_dir(),
                        static_folder=self._get_static_dir())
        
        # 分析エンジンを初期化
        config_manager = UnifiedConfigManager(project_name)
        unified_config = config_manager.load_config()
        self.analytics_engine = RealTimeAnalyticsEngine(unified_config)
        
        # ルートを設定
        self._setup_routes()
        
        # サーバースレッド
        self.server_thread = None
        self.running = False
    
    def _get_template_dir(self) -> str:
        """テンプレートディレクトリを取得"""
        current_dir = os.path.dirname(__file__)
        return os.path.join(current_dir, "templates")
    
    def _get_static_dir(self) -> str:
        """静的ファイルディレクトリを取得"""
        current_dir = os.path.dirname(__file__)
        return os.path.join(current_dir, "static")
    
    def _setup_routes(self):
        """ルートを設定"""
        
        @self.app.route('/')
        def dashboard():
            """メインダッシュボード"""
            return render_template('dashboard.html', 
                                 config=asdict(self.config),
                                 project_name=self.project_name)
        
        @self.app.route('/api/dashboard/data')
        def get_dashboard_data():
            """ダッシュボードデータAPI"""
            try:
                data = self.analytics_engine.get_analytics_dashboard_data()
                return jsonify({
                    'success': True,
                    'data': data,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                self.logger.error(f"ダッシュボードデータ取得エラー: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/analyze/file', methods=['POST'])
        def analyze_file():
            """ファイル分析API"""
            try:
                data = request.get_json()
                file_path = data.get('file_path')
                
                if not file_path:
                    return jsonify({
                        'success': False,
                        'error': 'file_path is required'
                    }), 400
                
                # 分析実行
                result = self.analytics_engine.analyze_document(file_path)
                
                return jsonify({
                    'success': True,
                    'data': {
                        'analysis_type': result.analysis_type.value,
                        'target_file': result.target_file,
                        'score': result.score,
                        'priority': result.priority.value,
                        'issues': result.issues,
                        'suggestions': result.suggestions,
                        'processing_time': result.processing_time,
                        'timestamp': result.timestamp.isoformat()
                    }
                })
                
            except Exception as e:
                self.logger.error(f"ファイル分析エラー: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/analyze/multiple', methods=['POST'])
        def analyze_multiple_files():
            """複数ファイル分析API"""
            try:
                data = request.get_json()
                file_paths = data.get('file_paths', [])
                
                if not file_paths:
                    return jsonify({
                        'success': False,
                        'error': 'file_paths is required'
                    }), 400
                
                # 分析実行
                results = self.analytics_engine.analyze_multiple_documents(file_paths)
                
                response_data = []
                for result in results:
                    response_data.append({
                        'analysis_type': result.analysis_type.value,
                        'target_file': result.target_file,
                        'score': result.score,
                        'priority': result.priority.value,
                        'issues': result.issues,
                        'suggestions': result.suggestions,
                        'processing_time': result.processing_time,
                        'timestamp': result.timestamp.isoformat()
                    })
                
                return jsonify({
                    'success': True,
                    'data': response_data
                })
                
            except Exception as e:
                self.logger.error(f"複数ファイル分析エラー: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/monitoring/start', methods=['POST'])
        def start_monitoring():
            """リアルタイム監視開始API"""
            try:
                data = request.get_json()
                watch_directories = data.get('watch_directories', [])
                
                if not watch_directories:
                    return jsonify({
                        'success': False,
                        'error': 'watch_directories is required'
                    }), 400
                
                self.analytics_engine.start_real_time_monitoring(watch_directories)
                
                return jsonify({
                    'success': True,
                    'message': 'リアルタイム監視を開始しました'
                })
                
            except Exception as e:
                self.logger.error(f"監視開始エラー: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/monitoring/stop', methods=['POST'])
        def stop_monitoring():
            """リアルタイム監視停止API"""
            try:
                self.analytics_engine.stop_real_time_monitoring()
                
                return jsonify({
                    'success': True,
                    'message': 'リアルタイム監視を停止しました'
                })
                
            except Exception as e:
                self.logger.error(f"監視停止エラー: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/metrics/history')
        def get_metrics_history():
            """メトリクス履歴API"""
            try:
                metric_name = request.args.get('metric')
                limit = int(request.args.get('limit', 50))
                
                if metric_name and metric_name in self.analytics_engine.metrics_history:
                    history = self.analytics_engine.metrics_history[metric_name][-limit:]
                else:
                    history = []
                
                return jsonify({
                    'success': True,
                    'data': {
                        'metric': metric_name,
                        'history': history
                    }
                })
                
            except Exception as e:
                self.logger.error(f"メトリクス履歴取得エラー: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/export/report')
        def export_report():
            """レポート出力API"""
            try:
                format_type = request.args.get('format', 'json')
                
                dashboard_data = self.analytics_engine.get_analytics_dashboard_data()
                
                if format_type == 'json':
                    return jsonify({
                        'success': True,
                        'data': dashboard_data,
                        'export_timestamp': datetime.now().isoformat()
                    })
                elif format_type == 'csv':
                    # CSV形式での出力（簡易実装）
                    csv_data = self._generate_csv_report(dashboard_data)
                    return csv_data, 200, {
                        'Content-Type': 'text/csv',
                        'Content-Disposition': 'attachment; filename=analytics_report.csv'
                    }
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Unsupported format'
                    }), 400
                
            except Exception as e:
                self.logger.error(f"レポート出力エラー: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
    
    def _generate_csv_report(self, dashboard_data: Dict[str, Any]) -> str:
        """CSV形式のレポートを生成"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # ヘッダー
        writer.writerow(['File', 'Score', 'Priority', 'Issues Count', 'Timestamp'])
        
        # データ
        for analysis in dashboard_data.get('recent_analyses', []):
            writer.writerow([
                analysis['file'],
                analysis['score'],
                analysis['priority'],
                analysis['issues_count'],
                analysis['timestamp']
            ])
        
        return output.getvalue()
    
    def start_server(self):
        """ダッシュボードサーバーを開始"""
        if self.running:
            self.logger.warning("ダッシュボードサーバーは既に実行中です")
            return
        
        self.running = True
        
        # テンプレートとスタティックファイルを作成
        self._create_dashboard_files()
        
        # サーバーを別スレッドで開始
        self.server_thread = threading.Thread(
            target=self._run_server,
            daemon=True
        )
        self.server_thread.start()
        
        self.logger.info(f"ダッシュボードサーバーを開始しました: http://{self.config.host}:{self.config.port}")
    
    def stop_server(self):
        """ダッシュボードサーバーを停止"""
        self.running = False
        if self.server_thread:
            self.server_thread.join(timeout=5)
        self.logger.info("ダッシュボードサーバーを停止しました")
    
    def _run_server(self):
        """サーバーを実行"""
        try:
            self.app.run(
                host=self.config.host,
                port=self.config.port,
                debug=self.config.debug,
                use_reloader=False,
                threaded=True
            )
        except Exception as e:
            self.logger.error(f"サーバー実行エラー: {e}")
    
    def _create_dashboard_files(self):
        """ダッシュボードファイルを作成"""
        # テンプレートディレクトリを作成
        template_dir = self._get_template_dir()
        static_dir = self._get_static_dir()
        
        os.makedirs(template_dir, exist_ok=True)
        os.makedirs(static_dir, exist_ok=True)
        
        # HTMLテンプレートを作成
        self._create_html_template(template_dir)
        
        # CSSファイルを作成
        self._create_css_file(static_dir)
        
        # JavaScriptファイルを作成
        self._create_js_file(static_dir)
    
    def _create_html_template(self, template_dir: str):
        """HTMLテンプレートを作成"""
        html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>統一設計ツール - 分析ダッシュボード</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='dashboard.css') }}">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="{{ config.theme }}">
    <div class="dashboard-container">
        <header class="dashboard-header">
            <h1>統一設計ツール分析ダッシュボード</h1>
            <div class="project-info">
                <span>プロジェクト: {{ project_name }}</span>
                <span id="last-updated">最終更新: --</span>
            </div>
        </header>

        <main class="dashboard-main">
            <!-- サマリーカード -->
            <section class="summary-cards">
                <div class="card">
                    <h3>総文書数</h3>
                    <div class="metric-value" id="total-documents">--</div>
                </div>
                <div class="card">
                    <h3>平均品質スコア</h3>
                    <div class="metric-value" id="avg-quality-score">--</div>
                </div>
                <div class="card">
                    <h3>重要な問題</h3>
                    <div class="metric-value critical" id="critical-issues">--</div>
                </div>
                <div class="card">
                    <h3>監視状態</h3>
                    <div class="metric-value" id="monitoring-status">停止中</div>
                </div>
            </section>

            <!-- チャートセクション -->
            <section class="charts-section">
                <div class="chart-container">
                    <h3>品質トレンド</h3>
                    <canvas id="quality-trend-chart"></canvas>
                </div>
                <div class="chart-container">
                    <h3>問題カテゴリ</h3>
                    <canvas id="issue-category-chart"></canvas>
                </div>
            </section>

            <!-- 最近の分析結果 -->
            <section class="recent-analyses">
                <h3>最近の分析結果</h3>
                <div class="table-container">
                    <table id="recent-analyses-table">
                        <thead>
                            <tr>
                                <th>ファイル</th>
                                <th>スコア</th>
                                <th>優先度</th>
                                <th>問題数</th>
                                <th>分析時刻</th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- データは JavaScript で動的に追加 -->
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- 頻出問題 -->
            <section class="top-issues">
                <h3>頻出問題</h3>
                <div id="top-issues-list">
                    <!-- データは JavaScript で動的に追加 -->
                </div>
            </section>
        </main>

        <!-- コントロールパネル -->
        <aside class="control-panel">
            <h3>コントロール</h3>
            
            <div class="control-group">
                <h4>リアルタイム監視</h4>
                <button id="start-monitoring" class="btn btn-primary">監視開始</button>
                <button id="stop-monitoring" class="btn btn-secondary">監視停止</button>
            </div>

            <div class="control-group">
                <h4>ファイル分析</h4>
                <input type="file" id="file-input" accept=".md" multiple>
                <button id="analyze-files" class="btn btn-primary">分析実行</button>
            </div>

            <div class="control-group">
                <h4>レポート出力</h4>
                <button id="export-json" class="btn btn-secondary">JSON出力</button>
                <button id="export-csv" class="btn btn-secondary">CSV出力</button>
            </div>

            <div class="control-group">
                <h4>設定</h4>
                <label>
                    <input type="checkbox" id="auto-refresh" {% if config.enable_real_time %}checked{% endif %}>
                    自動更新 ({{ config.auto_refresh_interval }}秒)
                </label>
                <label>
                    <select id="theme-selector">
                        <option value="light" {% if config.theme == 'light' %}selected{% endif %}>ライト</option>
                        <option value="dark" {% if config.theme == 'dark' %}selected{% endif %}>ダーク</option>
                    </select>
                    テーマ
                </label>
            </div>
        </aside>
    </div>

    <script src="{{ url_for('static', filename='dashboard.js') }}"></script>
</body>
</html>"""
        
        with open(os.path.join(template_dir, 'dashboard.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _create_css_file(self, static_dir: str):
        """CSSファイルを作成"""
        css_content = """/* 統一設計ツール ダッシュボード CSS */

:root {
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --success-color: #28a745;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
    --light-color: #f8f9fa;
    --dark-color: #343a40;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
}

body.dark {
    color: #fff;
    background-color: #1a1a1a;
}

.dashboard-container {
    display: grid;
    grid-template-areas: 
        "header header"
        "main sidebar";
    grid-template-columns: 1fr 300px;
    grid-template-rows: auto 1fr;
    min-height: 100vh;
    gap: 20px;
    padding: 20px;
}

.dashboard-header {
    grid-area: header;
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

body.dark .dashboard-header {
    background: #2d2d2d;
}

.dashboard-header h1 {
    color: var(--primary-color);
    font-size: 1.8rem;
}

.project-info {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    font-size: 0.9rem;
    color: #666;
}

body.dark .project-info {
    color: #ccc;
}

.dashboard-main {
    grid-area: main;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.summary-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;
}

body.dark .card {
    background: #2d2d2d;
}

.card h3 {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

body.dark .card h3 {
    color: #ccc;
}

.metric-value {
    font-size: 2rem;
    font-weight: bold;
    color: var(--primary-color);
}

.metric-value.critical {
    color: var(--danger-color);
}

.charts-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.chart-container {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

body.dark .chart-container {
    background: #2d2d2d;
}

.chart-container h3 {
    margin-bottom: 15px;
    color: #333;
}

body.dark .chart-container h3 {
    color: #fff;
}

.recent-analyses, .top-issues {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

body.dark .recent-analyses,
body.dark .top-issues {
    background: #2d2d2d;
}

.table-container {
    overflow-x: auto;
    margin-top: 15px;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

body.dark th,
body.dark td {
    border-bottom-color: #555;
}

th {
    background-color: #f8f9fa;
    font-weight: 600;
}

body.dark th {
    background-color: #3d3d3d;
}

.control-panel {
    grid-area: sidebar;
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    height: fit-content;
}

body.dark .control-panel {
    background: #2d2d2d;
}

.control-group {
    margin-bottom: 25px;
}

.control-group h4 {
    margin-bottom: 10px;
    color: #333;
    font-size: 1rem;
}

body.dark .control-group h4 {
    color: #fff;
}

.btn {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
    margin: 2px;
    transition: background-color 0.2s;
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background-color: #0056b3;
}

.btn-secondary {
    background-color: var(--secondary-color);
    color: white;
}

.btn-secondary:hover {
    background-color: #545b62;
}

input[type="file"],
select {
    width: 100%;
    padding: 8px;
    margin: 5px 0;
    border: 1px solid #ddd;
    border-radius: 4px;
}

body.dark input[type="file"],
body.dark select {
    background-color: #3d3d3d;
    border-color: #555;
    color: #fff;
}

label {
    display: block;
    margin: 10px 0;
    font-size: 0.9rem;
}

.priority-high {
    color: var(--danger-color);
    font-weight: bold;
}

.priority-medium {
    color: var(--warning-color);
    font-weight: bold;
}

.priority-low {
    color: var(--success-color);
}

.priority-critical {
    color: var(--danger-color);
    font-weight: bold;
    background-color: rgba(220, 53, 69, 0.1);
    padding: 2px 6px;
    border-radius: 3px;
}

#top-issues-list {
    margin-top: 15px;
}

.issue-item {
    padding: 10px;
    margin: 5px 0;
    background-color: #f8f9fa;
    border-radius: 4px;
    border-left: 4px solid var(--warning-color);
}

body.dark .issue-item {
    background-color: #3d3d3d;
}

.issue-count {
    float: right;
    background-color: var(--primary-color);
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.8rem;
}

@media (max-width: 768px) {
    .dashboard-container {
        grid-template-areas: 
            "header"
            "main"
            "sidebar";
        grid-template-columns: 1fr;
    }
    
    .charts-section {
        grid-template-columns: 1fr;
    }
    
    .summary-cards {
        grid-template-columns: repeat(2, 1fr);
    }
}"""
        
        with open(os.path.join(static_dir, 'dashboard.css'), 'w', encoding='utf-8') as f:
            f.write(css_content)
    
    def _create_js_file(self, static_dir: str):
        """JavaScriptファイルを作成"""
        js_content = """// 統一設計ツール ダッシュボード JavaScript

class AnalyticsDashboard {
    constructor() {
        this.charts = {};
        this.autoRefreshInterval = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadDashboardData();
        this.setupAutoRefresh();
    }

    setupEventListeners() {
        // 監視制御
        document.getElementById('start-monitoring').addEventListener('click', () => {
            this.startMonitoring();
        });

        document.getElementById('stop-monitoring').addEventListener('click', () => {
            this.stopMonitoring();
        });

        // ファイル分析
        document.getElementById('analyze-files').addEventListener('click', () => {
            this.analyzeFiles();
        });

        // レポート出力
        document.getElementById('export-json').addEventListener('click', () => {
            this.exportReport('json');
        });

        document.getElementById('export-csv').addEventListener('click', () => {
            this.exportReport('csv');
        });

        // 設定
        document.getElementById('auto-refresh').addEventListener('change', (e) => {
            if (e.target.checked) {
                this.setupAutoRefresh();
            } else {
                this.stopAutoRefresh();
            }
        });

        document.getElementById('theme-selector').addEventListener('change', (e) => {
            this.changeTheme(e.target.value);
        });
    }

    async loadDashboardData() {
        try {
            const response = await fetch('/api/dashboard/data');
            const result = await response.json();

            if (result.success) {
                this.updateDashboard(result.data);
                this.updateLastUpdated(result.timestamp);
            } else {
                console.error('ダッシュボードデータ取得エラー:', result.error);
            }
        } catch (error) {
            console.error('API呼び出しエラー:', error);
        }
    }

    updateDashboard(data) {
        // サマリーカードを更新
        document.getElementById('total-documents').textContent = data.summary.total_documents;
        document.getElementById('avg-quality-score').textContent = 
            data.summary.avg_quality_score.toFixed(1);
        document.getElementById('critical-issues').textContent = data.summary.critical_issues;

        // チャートを更新
        this.updateQualityTrendChart(data.metrics.quality_trends);
        this.updateIssueCategoryChart(data.metrics.issue_categories);

        // 最近の分析結果を更新
        this.updateRecentAnalyses(data.recent_analyses);

        // 頻出問題を更新
        this.updateTopIssues(data.top_issues);
    }

    updateQualityTrendChart(trends) {
        const ctx = document.getElementById('quality-trend-chart').getContext('2d');
        
        if (this.charts.qualityTrend) {
            this.charts.qualityTrend.destroy();
        }

        const datasets = trends.map((trend, index) => ({
            label: trend.metric,
            data: trend.history,
            borderColor: this.getChartColor(index),
            backgroundColor: this.getChartColor(index, 0.1),
            fill: false,
            tension: 0.1
        }));

        this.charts.qualityTrend = new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array.from({length: Math.max(...trends.map(t => t.history.length))}, (_, i) => i + 1),
                datasets: datasets
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: '品質トレンド'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    updateIssueCategoryChart(categories) {
        const ctx = document.getElementById('issue-category-chart').getContext('2d');
        
        if (this.charts.issueCategory) {
            this.charts.issueCategory.destroy();
        }

        const labels = Object.keys(categories);
        const data = Object.values(categories);

        this.charts.issueCategory = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF',
                        '#FF9F40'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: '問題カテゴリ分布'
                    }
                }
            }
        });
    }

    updateRecentAnalyses(analyses) {
        const tbody = document.querySelector('#recent-analyses-table tbody');
        tbody.innerHTML = '';

        analyses.forEach(analysis => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td title="${analysis.file}">${this.truncateFileName(analysis.file)}</td>
                <td>${analysis.score.toFixed(1)}</td>
                <td><span class="priority-${analysis.priority}">${analysis.priority}</span></td>
                <td>${analysis.issues_count}</td>
                <td>${this.formatTimestamp(analysis.timestamp)}</td>
            `;
            tbody.appendChild(row);
        });
    }

    updateTopIssues(issues) {
        const container = document.getElementById('top-issues-list');
        container.innerHTML = '';

        issues.forEach(issue => {
            const div = document.createElement('div');
            div.className = 'issue-item';
            div.innerHTML = `
                ${issue.issue}
                <span class="issue-count">${issue.count}</span>
            `;
            container.appendChild(div);
        });
    }

    async startMonitoring() {
        try {
            const response = await fetch('/api/monitoring/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    watch_directories: ['docs/design', 'docs/requirements']
                })
            });

            const result = await response.json();
            if (result.success) {
                document.getElementById('monitoring-status').textContent = '監視中';
                this.showNotification('リアルタイム監視を開始しました', 'success');
            } else {
                this.showNotification('監視開始に失敗しました: ' + result.error, 'error');
            }
        } catch (error) {
            this.showNotification('監視開始エラー: ' + error.message, 'error');
        }
    }

    async stopMonitoring() {
        try {
            const response = await fetch('/api/monitoring/stop', {
                method: 'POST'
            });

            const result = await response.json();
            if (result.success) {
                document.getElementById('monitoring-status').textContent = '停止中';
                this.showNotification('リアルタイム監視を停止しました', 'info');
            } else {
                this.showNotification('監視停止に失敗しました: ' + result.error, 'error');
            }
        } catch (error) {
            this.showNotification('監視停止エラー: ' + error.message, 'error');
        }
    }

    async analyzeFiles() {
        const fileInput = document.getElementById('file-input');
        const files = Array.from(fileInput.files);

        if (files.length === 0) {
            this.showNotification('ファイルを選択してください', 'warning');
            return;
        }

        try {
            // ファイルパスを取得（実際の実装では適切なパス変換が必要）
            const filePaths = files.map(file => file.name);

            const response = await fetch('/api/analyze/multiple', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    file_paths: filePaths
                })
            });

            const result = await response.json();
            if (result.success) {
                this.showNotification(`${files.length}個のファイルの分析が完了しました`, 'success');
                this.loadDashboardData(); // データを再読み込み
            } else {
                this.showNotification('ファイル分析に失敗しました: ' + result.error, 'error');
            }
        } catch (error) {
            this.showNotification('ファイル分析エラー: ' + error.message, 'error');
        }
    }

    async exportReport(format) {
        try {
            const response = await fetch(`/api/export/report?format=${format}`);
            
            if (format === 'csv') {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'analytics_report.csv';
                a.click();
                window.URL.revokeObjectURL(url);
            } else {
                const result = await response.json();
                if (result.success) {
                    const blob = new Blob([JSON.stringify(result.data, null, 2)], {
                        type: 'application/json'
                    });
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'analytics_report.json';
                    a.click();
                    window.URL.revokeObjectURL(url);
                }
            }
            
            this.showNotification(`レポートを${format.toUpperCase()}形式で出力しました`, 'success');
        } catch (error) {
            this.showNotification('レポート出力エラー: ' + error.message, 'error');
        }
    }

    setupAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
        }

        const interval = 30000; // 30秒
        this.autoRefreshInterval = setInterval(() => {
            this.loadDashboardData();
        }, interval);
    }

    stopAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
            this.autoRefreshInterval = null;
        }
    }

    changeTheme(theme) {
        document.body.className = theme;
        localStorage.setItem('dashboard-theme', theme);
    }

    updateLastUpdated(timestamp) {
        const element = document.getElementById('last-updated');
        const date = new Date(timestamp);
        element.textContent = `最終更新: ${date.toLocaleString('ja-JP')}`;
    }

    truncateFileName(filePath) {
        const maxLength = 30;
        if (filePath.length <= maxLength) {
            return filePath;
        }
        return '...' + filePath.slice(-maxLength + 3);
    }

    formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleString('ja-JP', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    getChartColor(index, alpha = 1) {
        const colors = [
            `rgba(54, 162, 235, ${alpha})`,
            `rgba(255, 99, 132, ${alpha})`,
            `rgba(255, 205, 86, ${alpha})`,
            `rgba(75, 192, 192, ${alpha})`,
            `rgba(153, 102, 255, ${alpha})`,
            `rgba(255, 159, 64, ${alpha})`
        ];
        return colors[index % colors.length];
    }

    showNotification(message, type = 'info') {
        // 簡易通知システム
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 4px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s;
        `;

        // タイプ別の色設定
        const colors = {
            success: '#28a745',
            error: '#dc3545',
            warning: '#ffc107',
            info: '#007bff'
        };
        notification.style.backgroundColor = colors[type] || colors.info;

        document.body.appendChild(notification);

        // フェードイン
        setTimeout(() => {
            notification.style.opacity = '1';
        }, 100);

        // 自動削除
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

// ダッシュボードを初期化
document.addEventListener('DOMContentLoaded', () => {
    new AnalyticsDashboard();
});"""
