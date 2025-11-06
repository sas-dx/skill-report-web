// 統一設計ツール - ダッシュボード JavaScript

class UnifiedToolsDashboard {
    constructor() {
        this.socket = null;
        this.currentTab = 'dashboard';
        this.taskStatus = {
            running: 0,
            completed: 0,
            errors: 0
        };
        this.activities = [];
        this.init();
    }

    init() {
        this.initSocketIO();
        this.initEventListeners();
        this.initTabs();
        this.loadInitialData();
        this.startStatusPolling();
    }

    // Socket.IO初期化
    initSocketIO() {
        try {
            this.socket = io();
            
            this.socket.on('connect', () => {
                console.log('Socket.IO connected');
                this.updateStatus('ready', 'Connected');
            });

            this.socket.on('disconnect', () => {
                console.log('Socket.IO disconnected');
                this.updateStatus('error', 'Disconnected');
            });

            this.socket.on('task_started', (data) => {
                this.handleTaskStarted(data);
            });

            this.socket.on('task_progress', (data) => {
                this.handleTaskProgress(data);
            });

            this.socket.on('task_completed', (data) => {
                this.handleTaskCompleted(data);
            });

            this.socket.on('task_error', (data) => {
                this.handleTaskError(data);
            });

            this.socket.on('log_message', (data) => {
                this.handleLogMessage(data);
            });

        } catch (error) {
            console.warn('Socket.IO not available, using polling mode');
            this.socket = null;
        }
    }

    // イベントリスナー初期化
    initEventListeners() {
        // タブ切り替え
        document.querySelectorAll('[data-tab]').forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                const tabName = e.currentTarget.getAttribute('data-tab');
                this.switchTab(tabName);
            });
        });

        // 更新ボタン
        document.getElementById('refresh-btn')?.addEventListener('click', () => {
            this.refreshDashboard();
        });

        // 設定保存
        document.getElementById('save-config-btn')?.addEventListener('click', () => {
            this.saveConfig();
        });
    }

    // タブ初期化
    initTabs() {
        this.switchTab('dashboard');
    }

    // タブ切り替え
    switchTab(tabName) {
        // 現在のタブを非アクティブに
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.querySelectorAll('[data-tab]').forEach(tab => {
            tab.classList.remove('active');
        });

        // 新しいタブをアクティブに
        const newContent = document.getElementById(`${tabName}-tab`);
        const newTab = document.querySelector(`[data-tab="${tabName}"]`);
        
        if (newContent) newContent.classList.add('active');
        if (newTab) newTab.classList.add('active');

        this.currentTab = tabName;

        // タブ固有の初期化
        switch (tabName) {
            case 'analytics':
                this.loadAnalytics();
                break;
            case 'logs':
                this.loadLogs();
                break;
            case 'config':
                this.loadConfig();
                break;
        }
    }

    // 初期データ読み込み
    async loadInitialData() {
        try {
            await this.refreshDashboard();
        } catch (error) {
            console.error('Failed to load initial data:', error);
            this.showAlert('初期データの読み込みに失敗しました', 'danger');
        }
    }

    // ダッシュボード更新
    async refreshDashboard() {
        try {
            this.updateStatus('running', 'Refreshing...');
            
            // ステータス情報を取得
            const response = await fetch('/api/status');
            if (response.ok) {
                const data = await response.json();
                this.updateDashboardData(data);
            }

            // アクティビティを取得
            await this.loadRecentActivity();
            
            this.updateStatus('ready', 'Ready');
        } catch (error) {
            console.error('Dashboard refresh failed:', error);
            this.updateStatus('error', 'Error');
            this.showAlert('ダッシュボードの更新に失敗しました', 'danger');
        }
    }

    // ダッシュボードデータ更新
    updateDashboardData(data) {
        // ステータスカード更新
        document.getElementById('running-tasks').textContent = data.running_tasks || 0;
        document.getElementById('completed-tasks').textContent = data.completed_tasks || 0;
        document.getElementById('error-count').textContent = data.error_count || 0;

        // プログレスバー更新
        const progressBar = document.getElementById('progress-bar');
        if (progressBar && data.progress !== undefined) {
            progressBar.style.width = `${data.progress}%`;
            progressBar.setAttribute('aria-valuenow', data.progress);
        }

        // タスクステータス更新
        this.taskStatus = {
            running: data.running_tasks || 0,
            completed: data.completed_tasks || 0,
            errors: data.error_count || 0
        };
    }

    // ステータス更新
    updateStatus(status, message) {
        const indicator = document.getElementById('status-indicator');
        const systemStatus = document.getElementById('system-status');
        
        if (indicator) {
            // ステータスクラスをリセット
            document.body.className = document.body.className.replace(/status-\w+/g, '');
            document.body.classList.add(`status-${status}`);
            
            // アイコンとメッセージ更新
            const icon = indicator.querySelector('i');
            if (icon) {
                icon.className = 'fas fa-circle';
                switch (status) {
                    case 'ready':
                        icon.classList.add('text-success');
                        break;
                    case 'running':
                        icon.classList.add('text-warning');
                        break;
                    case 'error':
                        icon.classList.add('text-danger');
                        break;
                    case 'completed':
                        icon.classList.add('text-info');
                        break;
                }
            }
            
            indicator.innerHTML = `<i class="${icon?.className || 'fas fa-circle'}"></i> ${message}`;
        }
        
        if (systemStatus) {
            systemStatus.textContent = message;
        }
    }

    // 最近のアクティビティ読み込み
    async loadRecentActivity() {
        try {
            const response = await fetch('/api/activity');
            if (response.ok) {
                const data = await response.json();
                this.updateActivityList(data.activities || []);
            }
        } catch (error) {
            console.error('Failed to load activity:', error);
        }
    }

    // アクティビティリスト更新
    updateActivityList(activities) {
        const container = document.getElementById('recent-activity');
        if (!container) return;

        if (activities.length === 0) {
            container.innerHTML = '<p class="text-muted">アクティビティはありません</p>';
            return;
        }

        const html = activities.map(activity => `
            <div class="activity-item">
                <div class="activity-time">${this.formatTime(activity.timestamp)}</div>
                <div class="activity-message">${activity.message}</div>
                <span class="activity-status ${activity.status}">${activity.status}</span>
            </div>
        `).join('');

        container.innerHTML = html;
    }

    // ツール実行
    async executeTools(toolType) {
        try {
            this.updateStatus('running', `Executing ${toolType} tools...`);
            
            const response = await fetch('/api/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ tool_type: toolType })
            });

            if (response.ok) {
                const data = await response.json();
                this.showAlert(`${toolType}ツールの実行を開始しました`, 'success');
                
                // プログレス追跡開始
                if (data.task_id) {
                    this.trackTaskProgress(data.task_id);
                }
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.error('Tool execution failed:', error);
            this.updateStatus('error', 'Execution failed');
            this.showAlert('ツールの実行に失敗しました', 'danger');
        }
    }

    // タスク進捗追跡
    async trackTaskProgress(taskId) {
        const pollProgress = async () => {
            try {
                const response = await fetch(`/api/task/${taskId}/status`);
                if (response.ok) {
                    const data = await response.json();
                    
                    if (data.status === 'completed') {
                        this.updateStatus('completed', 'Task completed');
                        this.refreshDashboard();
                        return;
                    } else if (data.status === 'error') {
                        this.updateStatus('error', 'Task failed');
                        this.showAlert('タスクの実行中にエラーが発生しました', 'danger');
                        return;
                    } else if (data.status === 'running') {
                        // 進捗更新
                        const progressBar = document.getElementById('progress-bar');
                        if (progressBar && data.progress !== undefined) {
                            progressBar.style.width = `${data.progress}%`;
                        }
                        
                        // 継続してポーリング
                        setTimeout(pollProgress, 2000);
                    }
                }
            } catch (error) {
                console.error('Progress polling failed:', error);
            }
        };

        pollProgress();
    }

    // 分析結果読み込み
    async loadAnalytics() {
        try {
            const response = await fetch('/api/analytics');
            if (response.ok) {
                const data = await response.json();
                this.updateAnalyticsDisplay(data);
            }
        } catch (error) {
            console.error('Failed to load analytics:', error);
            this.showAlert('分析結果の読み込みに失敗しました', 'danger');
        }
    }

    // 分析結果表示更新
    updateAnalyticsDisplay(data) {
        const container = document.getElementById('analytics-content');
        if (!container) return;

        const html = `
            <div class="row">
                <div class="col-md-3">
                    <div class="analytics-metric">
                        <h4>総テーブル数</h4>
                        <div class="metric-value">${data.total_tables || 0}</div>
                        <div class="metric-label">テーブル</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="analytics-metric">
                        <h4>検証済み</h4>
                        <div class="metric-value">${data.validated_tables || 0}</div>
                        <div class="metric-label">テーブル</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="analytics-metric">
                        <h4>エラー</h4>
                        <div class="metric-value">${data.error_count || 0}</div>
                        <div class="metric-label">件</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="analytics-metric">
                        <h4>成功率</h4>
                        <div class="metric-value">${data.success_rate || 0}%</div>
                        <div class="metric-label">成功率</div>
                    </div>
                </div>
            </div>
            
            <div class="card mt-4">
                <div class="card-header">
                    <h5>詳細レポート</h5>
                </div>
                <div class="card-body">
                    <pre>${JSON.stringify(data.details || {}, null, 2)}</pre>
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    // ログ読み込み
    async loadLogs() {
        try {
            const response = await fetch('/api/logs');
            if (response.ok) {
                const data = await response.json();
                this.updateLogsDisplay(data.logs || []);
            }
        } catch (error) {
            console.error('Failed to load logs:', error);
            this.showAlert('ログの読み込みに失敗しました', 'danger');
        }
    }

    // ログ表示更新
    updateLogsDisplay(logs) {
        const container = document.getElementById('logs-content');
        if (!container) return;

        if (logs.length === 0) {
            container.innerHTML = '<p class="text-muted">ログはありません</p>';
            return;
        }

        const html = logs.map(log => `
            <div class="log-entry">
                <span class="log-timestamp">${this.formatTime(log.timestamp)}</span>
                <span class="log-level ${log.level}">${log.level}</span>
                <span class="log-message">${log.message}</span>
            </div>
        `).join('');

        container.innerHTML = html;
        
        // 最新ログまでスクロール
        container.scrollTop = container.scrollHeight;
    }

    // 設定読み込み
    async loadConfig() {
        try {
            const response = await fetch('/api/config');
            if (response.ok) {
                const data = await response.json();
                this.updateConfigForm(data);
            }
        } catch (error) {
            console.error('Failed to load config:', error);
        }
    }

    // 設定フォーム更新
    updateConfigForm(config) {
        document.getElementById('project-name').value = config.project_name || '';
        document.getElementById('database-path').value = config.database_path || '';
        document.getElementById('output-dir').value = config.output_dir || '';
    }

    // 設定保存
    async saveConfig() {
        try {
            const config = {
                project_name: document.getElementById('project-name').value,
                database_path: document.getElementById('database-path').value,
                output_dir: document.getElementById('output-dir').value
            };

            const response = await fetch('/api/config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(config)
            });

            if (response.ok) {
                this.showAlert('設定を保存しました', 'success');
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.error('Failed to save config:', error);
            this.showAlert('設定の保存に失敗しました', 'danger');
        }
    }

    // ステータスポーリング開始
    startStatusPolling() {
        if (this.socket) return; // Socket.IOが利用可能な場合はポーリング不要

        setInterval(async () => {
            if (this.currentTab === 'dashboard') {
                await this.refreshDashboard();
            }
        }, 10000); // 10秒間隔
    }

    // Socket.IOイベントハンドラー
    handleTaskStarted(data) {
        this.taskStatus.running++;
        this.updateDashboardData(this.taskStatus);
        this.addActivity(data.message, 'running', data.timestamp);
        this.updateStatus('running', 'Task running...');
    }

    handleTaskProgress(data) {
        const progressBar = document.getElementById('progress-bar');
        if (progressBar) {
            progressBar.style.width = `${data.progress}%`;
        }
    }

    handleTaskCompleted(data) {
        this.taskStatus.running = Math.max(0, this.taskStatus.running - 1);
        this.taskStatus.completed++;
        this.updateDashboardData(this.taskStatus);
        this.addActivity(data.message, 'success', data.timestamp);
        
        if (this.taskStatus.running === 0) {
            this.updateStatus('completed', 'All tasks completed');
        }
    }

    handleTaskError(data) {
        this.taskStatus.running = Math.max(0, this.taskStatus.running - 1);
        this.taskStatus.errors++;
        this.updateDashboardData(this.taskStatus);
        this.addActivity(data.message, 'error', data.timestamp);
        this.updateStatus('error', 'Task failed');
    }

    handleLogMessage(data) {
        if (this.currentTab === 'logs') {
            this.loadLogs(); // ログタブが開いている場合は更新
        }
    }

    // アクティビティ追加
    addActivity(message, status, timestamp) {
        this.activities.unshift({
            message,
            status,
            timestamp: timestamp || new Date().toISOString()
        });

        // 最大50件まで保持
        if (this.activities.length > 50) {
            this.activities = this.activities.slice(0, 50);
        }

        if (this.currentTab === 'dashboard') {
            this.updateActivityList(this.activities);
        }
    }

    // 時刻フォーマット
    formatTime(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleString('ja-JP');
    }

    // アラート表示
    showAlert(message, type = 'info') {
        // 既存のアラートを削除
        const existingAlert = document.querySelector('.alert');
        if (existingAlert) {
            existingAlert.remove();
        }

        // 新しいアラートを作成
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // メインコンテンツの先頭に挿入
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.insertBefore(alert, mainContent.firstChild);
        }

        // 5秒後に自動削除
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }
}

// グローバル関数（HTMLから呼び出し用）
let dashboard;

function executeTools(toolType) {
    if (dashboard) {
        dashboard.executeTools(toolType);
    }
}

function loadAnalytics() {
    if (dashboard) {
        dashboard.loadAnalytics();
    }
}

function loadLogs() {
    if (dashboard) {
        dashboard.loadLogs();
    }
}

function saveConfig() {
    if (dashboard) {
        dashboard.saveConfig();
    }
}

// DOM読み込み完了後に初期化
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new UnifiedToolsDashboard();
});
