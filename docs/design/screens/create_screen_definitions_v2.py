#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画面定義書生成スクリプト v2.0 (改善版)

改版履歴:
┌─────────┬────────────┬──────────┬─────────────────────────────────────────────────────┐
│ バージョン │    更新日    │  更新者  │                  主な変更内容                       │
├─────────┼────────────┼──────────┼─────────────────────────────────────────────────────┤
│  v2.0   │ 2025-06-02 │ システム │ 元の画面定義書構成に合わせて大幅改善・完全版        │
│  v1.0   │ 2025-06-02 │ システム │ 初版作成・テーブル定義書スクリプトベース・完全版    │
└─────────┴────────────┴──────────┴─────────────────────────────────────────────────────┘

機能:
- 画面一覧.mdと画面詳細YAMLファイルから画面定義書（Markdown）を自動生成
- 元の画面定義書の詳細構成に対応
- カラー出力対応（成功=緑、警告=黄、エラー=赤）
- 詳細診断レポート機能
- 不足YAMLファイルの自動テンプレート生成
- 実行前検証機能（ドライラン）
- エラー・警告の集約サマリー表示
- 整合性チェック機能
- 既存ファイル保護機能
"""

import os
import re
import sys
import yaml
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

# カラー出力用（coloramaがない場合の代替）
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"

@dataclass
class ProcessingResult:
    """処理結果を格納するデータクラス"""
    screen_id: str
    screen_name: str
    success: bool
    has_yaml: bool
    error_message: Optional[str] = None
    warning_message: Optional[str] = None

class EnhancedLogger:
    """強化されたログ出力クラス"""
    
    def __init__(self, enable_color: bool = True):
        self.enable_color = enable_color
        self.logs = []
    
    def _colorize(self, text: str, color: str) -> str:
        """テキストに色を付ける"""
        if not self.enable_color:
            return text
        return f"{color}{text}{Colors.END}"
    
    def info(self, message: str):
        """情報ログ"""
        colored_msg = self._colorize(f"ℹ️  {message}", Colors.BLUE)
        print(colored_msg)
        self.logs.append((LogLevel.INFO, message))
    
    def warning(self, message: str):
        """警告ログ"""
        colored_msg = self._colorize(f"⚠️  {message}", Colors.YELLOW)
        print(colored_msg)
        self.logs.append((LogLevel.WARNING, message))
    
    def error(self, message: str):
        """エラーログ"""
        colored_msg = self._colorize(f"❌ {message}", Colors.RED)
        print(colored_msg)
        self.logs.append((LogLevel.ERROR, message))
    
    def success(self, message: str):
        """成功ログ"""
        colored_msg = self._colorize(f"✅ {message}", Colors.GREEN)
        print(colored_msg)
        self.logs.append((LogLevel.SUCCESS, message))
    
    def header(self, message: str):
        """ヘッダーログ"""
        colored_msg = self._colorize(f"\n🚀 {message}", Colors.CYAN + Colors.BOLD)
        print(colored_msg)
        print(self._colorize("=" * 80, Colors.CYAN))
    
    def section(self, message: str):
        """セクションログ"""
        colored_msg = self._colorize(f"\n📋 {message}", Colors.MAGENTA + Colors.BOLD)
        print(colored_msg)
        print(self._colorize("-" * 60, Colors.MAGENTA))

class ScreenDefinitionGenerator:
    """画面定義書生成クラス（改善版）"""
    
    def __init__(self, base_dir: str = None, enable_color: bool = True):
        """初期化"""
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.specs_dir = self.base_dir / "specs"
        self.details_dir = self.base_dir / "screen-details"
        self.screen_list_file = self.base_dir / "画面一覧.md"
        
        # ログ設定
        self.logger = EnhancedLogger(enable_color)
        
        # 処理結果追跡
        self.results: List[ProcessingResult] = []
        self.missing_yamls: List[str] = []
        
        # ディレクトリ作成
        self._ensure_directories()
        
        # 画面情報
        self.screens_info = {}
    
    def _ensure_directories(self):
        """必要なディレクトリを作成"""
        try:
            self.specs_dir.mkdir(exist_ok=True)
            self.details_dir.mkdir(exist_ok=True)
        except Exception as e:
            self.logger.error(f"ディレクトリ作成に失敗しました: {e}")
            raise
    
    def load_screen_list(self) -> Dict[str, Dict[str, Any]]:
        """画面一覧.mdから画面情報を読み込み"""
        if not self.screen_list_file.exists():
            raise FileNotFoundError(f"画面一覧ファイルが見つかりません: {self.screen_list_file}")
        
        with open(self.screen_list_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 画面情報を抽出
        screens = {}
        
        # 画面行のパターンを検索
        lines = content.split('\n')
        in_table = False
        
        for line in lines:
            # テーブルヘッダーを検出
            if '| 画面ID |' in line and '画面名称' in line:
                in_table = True
                continue
            
            # テーブル区切り行をスキップ
            if in_table and line.startswith('|---'):
                continue
            
            # テーブル終了を検出
            if in_table and (line.strip() == '' or not line.startswith('|')):
                in_table = False
                continue
            
            # 画面行を解析
            if in_table and line.startswith('| [SCR_'):
                parts = [part.strip() for part in line.split('|')]
                if len(parts) >= 7:
                    # [SCR_AUT_Login](specs/画面定義書_SCR_AUT_Login_ログイン画面.md) 形式から画面IDを抽出
                    screen_id_part = parts[1]
                    screen_id_match = re.search(r'\[([^\]]+)\]', screen_id_part)
                    if screen_id_match:
                        screen_id = screen_id_match.group(1)
                        screen_name = parts[2]
                        category = parts[3]
                        function = parts[4]
                        users = parts[5]
                        priority = parts[6]
                        notes = parts[7] if len(parts) > 7 else ""
                        
                        screens[screen_id] = {
                            'screen_id': screen_id,
                            'screen_name': screen_name,
                            'category': category,
                            'function': function,
                            'users': users,
                            'priority': priority,
                            'notes': notes
                        }
        
        return screens
    
    def load_screen_details(self, screen_id: str) -> Tuple[Optional[Dict[str, Any]], bool]:
        """画面詳細定義YAMLを読み込み（存在フラグも返す）"""
        details_file = self.details_dir / f"{screen_id}_details.yaml"
        
        if not details_file.exists():
            return None, False
        
        try:
            with open(details_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f), True
        except Exception as e:
            self.logger.error(f"{details_file} の読み込みに失敗: {e}")
            return None, False
    
    def generate_yaml_template(self, screen_id: str, screen_info: Dict[str, Any]) -> str:
        """画面詳細YAMLテンプレートを生成（改善版）"""
        template = {
            'screen_info': {
                'screen_id': screen_id,
                'screen_name': screen_info['screen_name'],
                'category': screen_info['category'],
                'function': screen_info['function'],
                'users': screen_info['users'],
                'priority': screen_info['priority']
            },
            'screen_overview': {
                'purpose': f"{screen_info['screen_name']}の目的を記載してください",
                'main_functions': [
                    "主要機能1の説明",
                    "主要機能2の説明",
                    "主要機能3の説明"
                ]
            },
            'screen_layout': {
                'layout_type': 'single_column',
                'description': 'レイアウトの説明を記載',
                'sections': [
                    {
                        'section_name': 'ヘッダー部',
                        'description': 'タイトルとナビゲーション'
                    },
                    {
                        'section_name': 'メイン部',
                        'description': '主要コンテンツエリア'
                    },
                    {
                        'section_name': 'フッター部',
                        'description': 'フッター情報'
                    }
                ]
            },
            'screen_items': [
                {
                    'item_id': 'username',
                    'item_name': 'ユーザー名',
                    'api_parameter': 'username',
                    'data_type': 'string',
                    'io_type': 'input',
                    'required': True,
                    'remarks': 'ログイン用ユーザー名'
                },
                {
                    'item_id': 'password',
                    'item_name': 'パスワード',
                    'api_parameter': 'password',
                    'data_type': 'string',
                    'io_type': 'input',
                    'required': True,
                    'remarks': 'ログイン用パスワード（マスク表示）'
                },
                {
                    'item_id': 'login_button',
                    'item_name': 'ログインボタン',
                    'api_parameter': '',
                    'data_type': 'button',
                    'io_type': 'action',
                    'required': False,
                    'remarks': 'ログイン実行ボタン'
                }
            ],
            'operation_flow': [
                {
                    'step': 1,
                    'operation': '画面表示',
                    'description': 'ログイン画面が表示される'
                },
                {
                    'step': 2,
                    'operation': 'ユーザー名入力',
                    'description': 'ユーザー名を入力フィールドに入力'
                },
                {
                    'step': 3,
                    'operation': 'パスワード入力',
                    'description': 'パスワードを入力フィールドに入力'
                },
                {
                    'step': 4,
                    'operation': 'ログインボタン押下',
                    'description': 'ログインボタンを押下して認証実行'
                },
                {
                    'step': 5,
                    'operation': '画面遷移',
                    'description': '認証成功時はホーム画面へ遷移'
                }
            ],
            'events': [
                {
                    'event_id': 'EVT_001',
                    'trigger_action': 'on_load',
                    'event_detail': '画面読み込み時の初期化処理',
                    'related_api': '',
                    'message_display': ''
                },
                {
                    'event_id': 'EVT_002',
                    'trigger_action': 'on_login_click',
                    'event_detail': 'ログインボタン押下時の認証処理',
                    'related_api': 'API_AUTH_001 - ユーザー認証API',
                    'message_display': '認証中...'
                }
            ],
            'validations': {
                'input_validation': [
                    {
                        'field': 'username',
                        'rules': ['required', 'min_length:3', 'max_length:50'],
                        'error_message': 'ユーザー名は3文字以上50文字以内で入力してください。'
                    },
                    {
                        'field': 'password',
                        'rules': ['required', 'min_length:8'],
                        'error_message': 'パスワードは8文字以上で入力してください。'
                    }
                ]
            },
            'error_handling': {
                'error_messages': [
                    {
                        'error_code': 'ERR_001',
                        'error_type': 'validation_error',
                        'message': '入力内容に誤りがあります。',
                        'action': 'show_field_error'
                    },
                    {
                        'error_code': 'ERR_002',
                        'error_type': 'authentication_error',
                        'message': 'ユーザー名またはパスワードが正しくありません。',
                        'action': 'show_error_message'
                    },
                    {
                        'error_code': 'ERR_003',
                        'error_type': 'system_error',
                        'message': 'システムエラーが発生しました。しばらく時間をおいて再度お試しください。',
                        'action': 'show_error_page'
                    }
                ]
            },
            'security': {
                'authentication': {
                    'method': 'form_based',
                    'session_management': True,
                    'password_encryption': True
                },
                'authorization': {
                    'roles': ['user', 'admin'],
                    'access_control': 'role_based'
                },
                'data_protection': {
                    'csrf_protection': True,
                    'input_sanitization': True,
                    'sql_injection_prevention': True,
                    'xss_prevention': True
                }
            },
            'performance': {
                'load_time_target': '2s',
                'optimization': ['image_compression', 'css_minification', 'js_minification'],
                'caching': 'browser_cache'
            },
            'accessibility': {
                'keyboard_navigation': True,
                'screen_reader_support': True,
                'color_contrast': 'AA',
                'font_size_adjustable': True,
                'aria_labels': True
            },
            'responsive_design': {
                'mobile_support': True,
                'tablet_support': True,
                'desktop_support': True,
                'breakpoints': ['320px', '768px', '1024px'],
                'layout_adaptation': 'fluid'
            },
            'related_apis': [
                {
                    'api_id': 'API_AUTH_001',
                    'api_name': 'ユーザー認証API',
                    'method': 'POST',
                    'endpoint': '/api/auth/login',
                    'description': 'ユーザー認証を行うAPI'
                }
            ],
            'related_screens': [
                {
                    'screen_id': 'SCR_CMN_Home',
                    'screen_name': 'ホーム画面',
                    'relation_type': 'transition_to',
                    'condition': '認証成功時'
                },
                {
                    'screen_id': 'SCR_AUT_PasswordReset',
                    'screen_name': 'パスワードリセット画面',
                    'relation_type': 'link_to',
                    'condition': 'パスワードを忘れた場合'
                }
            ],
            'business_rules': [
                f"{screen_info['screen_name']}に関する業務ルールを記載",
                "例：ログイン試行回数は5回まで",
                "例：パスワードは定期的な変更が必要"
            ],
            'notes': [
                "実装時の注意事項を記載",
                "例：セッション管理の実装が必要",
                "例：ブルートフォース攻撃対策が必要"
            ],
            'remarks': [
                "その他の重要な情報を記載",
                "例：多要素認証の将来対応予定"
            ],
            'revision_history': [
                {
                    'version': '1.0',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'author': 'システム',
                    'changes': '初版作成'
                }
            ]
        }
        
        return yaml.dump(template, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    def generate_screen_definition(self, screen_id: str, screen_info: Dict[str, Any]) -> Tuple[str, bool]:
        """画面定義書（Markdown）を生成（改善版）"""
        details, has_yaml = self.load_screen_details(screen_id)
        
        # ヘッダー部分
        md_content = f"# 画面定義書: {screen_id}\n\n"
        md_content += f"## 基本情報\n\n"
        md_content += f"| 項目 | 値 |\n"
        md_content += f"|------|-----|\n"
        md_content += f"| 画面ID | {screen_id} |\n"
        md_content += f"| 画面名称 | {screen_info['screen_name']} |\n"
        md_content += f"| 機能カテゴリ | {screen_info['category']} |\n"
        md_content += f"| 主な対応機能 | {screen_info['function']} |\n"
        md_content += f"| 主な利用者 | {screen_info['users']} |\n"
        md_content += f"| 優先度 | {screen_info['priority']} |\n"
        md_content += f"| 生成日時 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |\n\n"
        
        # 画面概要
        if details and 'screen_overview' in details:
            overview = details['screen_overview']
            md_content += f"## 画面概要\n\n"
            md_content += f"### 目的\n{overview.get('purpose', '')}\n\n"
            if overview.get('main_functions'):
                md_content += f"### 主な機能\n"
                for func in overview['main_functions']:
                    md_content += f"- {func}\n"
                md_content += "\n"
        
        # 画面レイアウト
        if details and 'screen_layout' in details:
            layout = details['screen_layout']
            md_content += f"## 画面レイアウト\n\n"
            md_content += f"{layout.get('description', '')}\n\n"
            if layout.get('sections'):
                md_content += f"| セクション名 | 説明 |\n"
                md_content += f"|-------------|------|\n"
                for section in layout['sections']:
                    md_content += f"| {section['section_name']} | {section['description']} |\n"
                md_content += "\n"
        
        # 画面項目定義
        if details and 'screen_items' in details:
            md_content += f"## 画面項目定義\n\n"
            md_content += f"| 項目ID | 項目名 | APIパラメータ対応 | データ型 | I/O区分 | 必須 | 備考 |\n"
            md_content += f"|--------|--------|-------------------|----------|---------|------|------|\n"
            for item in details['screen_items']:
                required = "○" if item.get('required', False) else "×"
                md_content += f"| {item['item_id']} | {item['item_name']} | {item.get('api_parameter', '')} | {item['data_type']} | {item['io_type']} | {required} | {item.get('remarks', '')} |\n"
            md_content += "\n"
        
        # 操作フロー
        if details and 'operation_flow' in details:
            md_content += f"## 操作フロー\n\n"
            md_content += f"| ステップ | 操作 | 説明 |\n"
            md_content += f"|----------|------|------|\n"
            for flow in details['operation_flow']:
                md_content += f"| {flow['step']} | {flow['operation']} | {flow['description']} |\n"
            md_content += "\n"
        
        # イベント・アクション定義
        if details and 'events' in details:
            md_content += f"## イベント・アクション定義\n\n"
            md_content += f"| イベントID | トリガー/アクション | イベント内容・アクション詳細 | 紐付くAPI ID・名称 | メッセージ表示 |\n"
            md_content += f"|------------|---------------------|------------------------------|-------------------|----------------|\n"
            for event in details['events']:
                md_content += f"| {event['event_id']} | {event['trigger_action']} | {event['event_detail']} | {event.get('related_api', '')} | {event.get('message_display', '')} |\n"
            md_content += "\n"
        
        # バリデーション
        if details and 'validations' in details:
            md_content += f"## バリデーション\n\n"
            if details['validations'].get('input_validation'):
                md_content += f"### 入力値検証\n\n"
                md_content += f"| 対象フィールド | ルール | エラーメッセージ |\n"
                md_content += f"|----------------|--------|------------------|\n"
                for validation in details['validations']['input_validation']:
                    rules = ', '.join(validation.get('rules', [])) if validation.get('rules') else ''
                    md_content += f"| {validation['field']} | {rules} | {validation.get('error_message', '')} |\n"
                md_content += "\n"
        
        # エラーハンドリング
        if details and 'error_handling' in details:
            md_content += f"## エラーハンドリング\n\n"
            if details['error_handling'].get('error_messages'):
                md_content += f"### エラーメッセージ一覧\n\n"
                md_content += f"| エラーコード | エラー種別 | メッセージ | 対応アクション |\n"
                md_content += f"|-------------|------------|------------|----------------|\n"
                for error in details['error_handling']['error_messages']:
                    md_content += f"| {error.get('error_code', '')} | {error['error_type']} | {error.get('message', '')} | {error.get('action', '')} |\n"
                md_content += "\n"
        
        # セキュリティ要件
        if details and 'security' in details:
            security = details['security']
            md_content += f"## セキュリティ要件\n\n"
            
            if security.get('authentication'):
                auth = security['authentication']
                md_content += f"### 認証・認可\n\n"
                md_content += f"| 項目 | 設定 |\n"
                md_content += f"|------|------|\n"
                md_content += f"| 認証方式 | {auth.get('method', '')} |\n"
                md_content += f"| セッション管理 | {'有効' if auth.get('session_management', False) else '無効'} |\n"
                md_content += f"| パスワード暗号化 | {'有効' if auth.get('password_encryption', False) else '無効'} |\n"
                md_content += "\n"
            
            if security.get('data_protection'):
                protection = security['data_protection']
                md_content += f"### データ保護\n\n"
                md_content += f"| 項目 | 設定 |\n"
                md_content += f"|------|------|\n"
                md_content += f"| CSRF保護 | {'有効' if protection.get('csrf_protection', False) else '無効'} |\n"
                md_content += f"| 入力サニタイゼーション | {'有効' if protection.get('input_sanitization', False) else '無効'} |\n"
                md_content += f"| SQLインジェクション対策 | {'有効' if protection.get('sql_injection_prevention', False) else '無効'} |\n"
                md_content += f"| XSS対策 | {'有効' if protection.get('xss_prevention', False) else '無効'} |\n"
                md_content += "\n"
        
        # パフォーマンス要件
        if details and 'performance' in details:
            performance = details['performance']
            md_content += f"## パフォーマンス要件\n\n"
            md_content += f"| 項目 | 値 |\n"
            md_content += f"|------|----|\n"
            md_content += f"| 読み込み時間目標 | {performance.get('load_time_target', 'N/A')} |\n"
            if performance.get('optimization'):
                optimizations = ', '.join(performance['optimization']) if isinstance(performance['optimization'], list) else str(performance['optimization'])
                md_content += f"| 最適化手法 | {optimizations} |\n"
            md_content += f"| キャッシュ | {performance.get('caching', 'N/A')} |\n"
            md_content += "\n"
        
        # アクセシビリティ
        if details and 'accessibility' in details:
            accessibility = details['accessibility']
            md_content += f"## アクセシビリティ\n\n"
            md_content += f"| 項目 | 対応 |\n"
            md_content += f"|------|------|\n"
            md_content += f"| キーボードナビゲーション | {'対応' if accessibility.get('keyboard_navigation', False) else '非対応'} |\n"
            md_content += f"| スクリーンリーダー | {'対応' if accessibility.get('screen_reader_support', False) else '非対応'} |\n"
            md_content += f"| カラーコントラスト | {accessibility.get('color_contrast', 'N/A')} |\n"
            md_content += f"| フォントサイズ調整 | {'対応' if accessibility.get('font_size_adjustable', False) else '非対応'} |\n"
            md_content += f"| ARIAラベル | {'対応' if accessibility.get('aria_labels', False) else '非対応'} |\n"
            md_content += "\n"
        
        # レスポンシブデザイン
        if details and 'responsive_design' in details:
            responsive = details['responsive_design']
            md_content += f"## レスポンシブデザイン\n\n"
            md_content += f"| 項目 | 対応 |\n"
            md_content += f"|------|------|\n"
            md_content += f"| モバイル | {'対応' if responsive.get('mobile_support', False) else '非対応'} |\n"
            md_content += f"| タブレット | {'対応' if responsive.get('tablet_support', False) else '非対応'} |\n"
            md_content += f"| デスクトップ | {'対応' if responsive.get('desktop_support', False) else '非対応'} |\n"
            if responsive.get('breakpoints'):
                breakpoints = ', '.join(responsive['breakpoints']) if isinstance(responsive['breakpoints'], list) else str(responsive['breakpoints'])
                md_content += f"| ブレークポイント | {breakpoints} |\n"
            md_content += f"| レイアウト適応 | {responsive.get('layout_adaptation', 'N/A')} |\n"
            md_content += "\n"
        
        # 関連API
        if details and 'related_apis' in details:
            md_content += f"## 関連API\n\n"
            md_content += f"| API ID | API名称 | メソッド | エンドポイント | 説明 |\n"
            md_content += f"|--------|---------|----------|---------------|------|\n"
            for api in details['related_apis']:
                md_content += f"| {api['api_id']} | {api['api_name']} | {api['method']} | {api['endpoint']} | {api.get('description', '')} |\n"
            md_content += "\n"
        
        # 関連画面
        if details and 'related_screens' in details:
            md_content += f"## 関連画面\n\n"
            md_content += f"| 画面ID | 画面名称 | 関係種別 | 条件 |\n"
            md_content += f"|--------|----------|----------|------|\n"
            for screen in details['related_screens']:
                md_content += f"| {screen['screen_id']} | {screen['screen_name']} | {screen['relation_type']} | {screen.get('condition', '')} |\n"
            md_content += "\n"
        
        # 特記事項
        if details and 'notes' in details:
            md_content += f"## 特記事項\n\n"
            for note in details['notes']:
                md_content += f"- {note}\n"
            md_content += "\n"
        
        # 備考
        if details and 'remarks' in details:
            md_content += f"## 備考\n\n"
            for remark in details['remarks']:
                md_content += f"- {remark}\n"
            md_content += "\n"
        
        # 改版履歴
        if details and 'revision_history' in details:
            md_content += f"## 改版履歴\n\n"
            md_content += f"| バージョン | 更新日 | 更新者 | 変更内容 |\n"
            md_content += f"|------------|--------|--------|----------|\n"
            for revision in details['revision_history']:
                md_content += f"| {revision['version']} | {revision['date']} | {revision['author']} | {revision['changes']} |\n"
            md_content += "\n"
        
        if not has_yaml:
            md_content += f"## 注意\n\n"
            md_content += f"この画面定義書は詳細YAMLファイルが存在しないため、基本定義のみで生成されています。\n"
            md_content += f"詳細な仕様を追加するには、`{screen_id}_details.yaml` ファイルを作成してください。\n"
        
        return md_content, has_yaml
    
    def generate_templates(self, screen_ids: List[str] = None):
        """YAMLテンプレート生成"""
        self.screens_info = self.load_screen_list()
        
        if screen_ids:
            target_screens = {sid: info for sid, info in self.screens_info.items() if sid in screen_ids}
            missing_screens = set(screen_ids) - set(self.screens_info.keys())
            if missing_screens:
                self.logger.warning(f"以下の画面が見つかりません: {', '.join(missing_screens)}")
        else:
            target_screens = self.screens_info
        
        self.logger.header("YAMLテンプレート生成")
        self.logger.info(f"{len(target_screens)}個の画面のテンプレートを生成します。")
        
        for screen_id, screen_info in target_screens.items():
            details_file = self.details_dir / f"{screen_id}_details.yaml"
            
            if details_file.exists():
                self.logger.warning(f"既存ファイルをスキップ: {details_file}")
                continue
            
            try:
                template_content = self.generate_yaml_template(screen_id, screen_info)
                
                with open(details_file, 'w', encoding='utf-8') as f:
                    f.write(template_content)
                
                self.logger.success(f"テンプレート生成: {details_file}")
                
            except Exception as e:
                self.logger.error(f"テンプレート生成失敗 {screen_id}: {e}")
    
    def generate_files(self, screen_ids: List[str] = None, output_dir: str = None, dry_run: bool = False):
        """ファイル生成メイン処理"""
        # 画面一覧読み込み
        self.screens_info = self.load_screen_list()
        
        # 出力先ディレクトリ設定
        if output_dir:
            output_path = Path(output_dir)
            specs_output = output_path / "specs"
            specs_output.mkdir(parents=True, exist_ok=True)
        else:
            specs_output = self.specs_dir
        
        # 処理対象画面決定
        if screen_ids:
            target_screens = {sid: info for sid, info in self.screens_info.items() if sid in screen_ids}
            missing_screens = set(screen_ids) - set(self.screens_info.keys())
            if missing_screens:
                self.logger.warning(f"以下の画面が見つかりません: {', '.join(missing_screens)}")
        else:
            target_screens = self.screens_info
        
        self.logger.header(f"画面定義書生成スクリプト v2.0 (改善版)")
        self.logger.info(f"{len(target_screens)}個の画面を処理します。")
        
        if dry_run:
            self.logger.warning("ドライランモード: ファイルは実際には作成されません")
        
        for screen_id, screen_info in target_screens.items():
            self.logger.info(f"処理中: {screen_id} ({screen_info['screen_name']})")
            
            try:
                # 画面定義書生成
                md_content, has_yaml = self.generate_screen_definition(screen_id, screen_info)
                md_file = specs_output / f"画面定義書_{screen_id}_{screen_info['screen_name']}.md"
                
                if not dry_run:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(md_content)
                    self.logger.success(f"  ✓ {md_file}")
                else:
                    self.logger.info(f"  [DRY] {md_file}")
                
                # 処理結果を記録
                result = ProcessingResult(
                    screen_id=screen_id,
                    screen_name=screen_info['screen_name'],
                    success=True,
                    has_yaml=has_yaml
                )
                if not has_yaml:
                    result.warning_message = "YAMLファイルが存在しません"
                    self.missing_yamls.append(screen_id)
                self.results.append(result)
                
            except Exception as e:
                error_msg = f"エラー: {e}"
                self.logger.error(f"  ❌ {error_msg}")
                
                # エラー結果を記録
                result = ProcessingResult(
                    screen_id=screen_id,
                    screen_name=screen_info['screen_name'],
                    success=False,
                    has_yaml=False,
                    error_message=str(e)
                )
                self.results.append(result)
        
        # 処理結果サマリー
        self._print_summary()
        
        self.logger.success(f"処理が完了しました！")
        self.logger.info(f"📁 画面定義書出力先: {specs_output}")
        
        # YAMLテンプレート生成提案
        if self.missing_yamls:
            self.logger.section("YAMLテンプレート生成提案")
            self.logger.info("以下のコマンドでYAMLテンプレートを生成できます:")
            self.logger.info(f"python3 {Path(__file__).name} --generate-templates")
    
    def _print_summary(self):
        """処理結果サマリーを表示"""
        self.logger.section("処理結果サマリー")
        
        total = len(self.results)
        success = len([r for r in self.results if r.success])
        errors = len([r for r in self.results if not r.success])
        warnings = len([r for r in self.results if r.success and not r.has_yaml])
        
        self.logger.info(f"総画面数: {total}")
        self.logger.success(f"成功: {success}")
        if errors > 0:
            self.logger.error(f"エラー: {errors}")
        if warnings > 0:
            self.logger.warning(f"警告: {warnings} (YAMLファイル不足)")
        
        # エラー詳細
        if errors > 0:
            self.logger.section("エラー詳細")
            for result in self.results:
                if not result.success:
                    self.logger.error(f"{result.screen_id}: {result.error_message}")
        
        # 警告詳細
        if warnings > 0:
            self.logger.section("警告詳細 (YAMLファイル不足)")
            for result in self.results:
                if result.success and not result.has_yaml:
                    self.logger.warning(f"{result.screen_id}: 基本定義のみで生成")

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="画面定義書生成スクリプト v2.0 (改善版)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 全画面生成
  python3 create_screen_definitions_v2.py
  
  # 個別画面生成
  python3 create_screen_definitions_v2.py --screen SCR_AUT_Login
  python3 create_screen_definitions_v2.py --screen SCR_AUT_Login,SCR_CMN_Home
  
  # YAMLテンプレート生成
  python3 create_screen_definitions_v2.py --generate-templates
  python3 create_screen_definitions_v2.py --generate-templates --screen SCR_AUT_Login
  
  # 出力先指定
  python3 create_screen_definitions_v2.py --screen SCR_AUT_Login --output-dir custom/
  
  # ドライラン
  python3 create_screen_definitions_v2.py --dry-run
        """
    )
    
    parser.add_argument(
        '--screen', '-s',
        help='生成対象画面ID（カンマ区切りで複数指定可能）'
    )
    
    parser.add_argument(
        '--generate-templates', '-g',
        action='store_true',
        help='YAMLテンプレートを生成'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        help='出力先ディレクトリ'
    )
    
    parser.add_argument(
        '--base-dir', '-b',
        help='ベースディレクトリ（デフォルト: スクリプトのディレクトリ）'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='ドライラン（ファイルを実際には作成しない）'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='カラー出力を無効化'
    )
    
    args = parser.parse_args()
    
    try:
        generator = ScreenDefinitionGenerator(args.base_dir, not args.no_color)
        
        # 対象画面決定
        target_screens = None
        
        if args.screen:
            target_screens = [s.strip() for s in args.screen.split(',')]
        
        # YAMLテンプレート生成モード
        if args.generate_templates:
            generator.generate_templates(target_screens)
        else:
            # 画面定義書生成モード
            generator.generate_files(target_screens, args.output_dir, args.dry_run)
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
