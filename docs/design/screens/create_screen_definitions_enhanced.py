#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画面定義書検証・更新スクリプト v1.0 (拡張版)

改版履歴:
┌─────────┬────────────┬──────────┬─────────────────────────────────────────────────────┐
│ バージョン │    更新日    │  更新者  │                  主な変更内容                       │
├─────────┼────────────┼──────────┼─────────────────────────────────────────────────────┤
│  v1.0   │ 2025-06-03 │ システム │ 初版作成・検証・差分表示・更新・コミット機能搭載    │
└─────────┴────────────┴──────────┴─────────────────────────────────────────────────────┘

機能:
- 画面定義書の検証（YAML-Markdown整合性チェック）
- 差分表示（カラー対応）
- バックアップ機能
- ファイル更新機能
- Git統合（自動コミット）
- 詳細診断レポート
- ドライラン対応

推奨ワークフロー:
1. 検証実行: --validate-only
2. 差分確認: --show-diff
3. バックアップ作成: --backup
4. 更新実行: --force-update
5. コミット: --commit
"""

import os
import re
import sys
import yaml
import json
import argparse
import difflib
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

# カラー出力用
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
class ValidationResult:
    """検証結果を格納するデータクラス"""
    screen_id: str
    screen_name: str
    yaml_exists: bool
    markdown_exists: bool
    yaml_valid: bool
    markdown_valid: bool
    consistency_check: bool
    issues: List[str]
    warnings: List[str]
    suggestions: List[str]

@dataclass
class ComparisonResult:
    """比較結果を格納するデータクラス"""
    has_differences: bool
    added_lines: List[str]
    removed_lines: List[str]
    modified_lines: List[Tuple[str, str]]
    diff_html: str

class EnhancedLogger:
    """強化されたログ出力クラス"""
    
    def __init__(self, enable_color: bool = True, verbose: bool = False):
        self.enable_color = enable_color
        self.verbose = verbose
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
    
    def debug(self, message: str):
        """デバッグログ（詳細モード時のみ表示）"""
        if self.verbose:
            colored_msg = self._colorize(f"🔍 {message}", Colors.WHITE)
            print(colored_msg)
            self.logs.append((LogLevel.INFO, f"DEBUG: {message}"))

class ScreenDefinitionValidator:
    """画面定義書検証クラス"""
    
    def __init__(self, logger: EnhancedLogger):
        self.logger = logger
    
    def validate_yaml_structure(self, yaml_data: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """YAML構造検証"""
        issues = []
        warnings = []
        
        # 必須セクションチェック
        required_sections = [
            'screen_info', 'screen_overview', 'screen_layout', 
            'screen_items', 'operation_flow', 'events'
        ]
        
        for section in required_sections:
            if section not in yaml_data:
                issues.append(f"必須セクション '{section}' が存在しません")
        
        # screen_info詳細チェック
        if 'screen_info' in yaml_data:
            screen_info = yaml_data['screen_info']
            required_fields = ['screen_id', 'screen_name', 'category', 'function', 'users', 'priority']
            for field in required_fields:
                if field not in screen_info:
                    issues.append(f"screen_info.{field} が存在しません")
        
        # 警告レベルのチェック
        optional_sections = ['validations', 'error_handling', 'security', 'performance', 'accessibility']
        for section in optional_sections:
            if section not in yaml_data:
                warnings.append(f"推奨セクション '{section}' が存在しません")
        
        return len(issues) == 0, issues, warnings
    
    def validate_markdown_structure(self, md_content: str) -> Tuple[bool, List[str], List[str]]:
        """Markdown構造検証"""
        issues = []
        warnings = []
        
        # 必須セクションチェック
        required_sections = [
            '# 画面定義書:', '## 基本情報', '## 画面概要', 
            '## 画面レイアウト', '## 画面項目定義', '## 操作フロー'
        ]
        
        for section in required_sections:
            if section not in md_content:
                issues.append(f"必須セクション '{section}' が存在しません")
        
        # 改版履歴チェック
        if '## 改版履歴' not in md_content:
            warnings.append("改版履歴セクションが存在しません")
        
        return len(issues) == 0, issues, warnings
    
    def check_consistency(self, yaml_data: Dict[str, Any], md_content: str) -> Tuple[bool, List[str]]:
        """YAML-Markdown整合性チェック"""
        issues = []
        
        # 基本情報の整合性チェック
        if 'screen_info' in yaml_data:
            screen_info = yaml_data['screen_info']
            
            # 画面IDチェック
            if 'screen_id' in screen_info:
                screen_id = screen_info['screen_id']
                if f"画面定義書: {screen_id}" not in md_content:
                    issues.append(f"画面ID '{screen_id}' がMarkdownタイトルと一致しません")
            
            # 優先度チェック
            if 'priority' in screen_info:
                priority = screen_info['priority']
                if f"| 優先度 | {priority} |" not in md_content:
                    issues.append(f"基本情報テーブルの優先度 '{priority}' が一致しません")
        
        return len(issues) == 0, issues

class ScreenDefinitionComparator:
    """画面定義書比較クラス"""
    
    def __init__(self, logger: EnhancedLogger):
        self.logger = logger
    
    def compare_files(self, current_content: str, generated_content: str) -> ComparisonResult:
        """ファイル比較"""
        current_lines = current_content.splitlines(keepends=True)
        generated_lines = generated_content.splitlines(keepends=True)
        
        # 差分計算
        diff = list(difflib.unified_diff(
            current_lines, 
            generated_lines, 
            fromfile='現在のファイル', 
            tofile='生成予定ファイル',
            lineterm=''
        ))
        
        has_differences = len(diff) > 0
        added_lines = []
        removed_lines = []
        modified_lines = []
        
        # 差分解析
        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                added_lines.append(line[1:].strip())
            elif line.startswith('-') and not line.startswith('---'):
                removed_lines.append(line[1:].strip())
        
        # HTML形式の差分生成
        diff_html = '\n'.join(diff)
        
        return ComparisonResult(
            has_differences=has_differences,
            added_lines=added_lines,
            removed_lines=removed_lines,
            modified_lines=modified_lines,
            diff_html=diff_html
        )
    
    def show_diff(self, comparison: ComparisonResult, screen_id: str):
        """差分表示"""
        if not comparison.has_differences:
            self.logger.success(f"📄 {screen_id}: ファイルに差分はありません")
            return
        
        self.logger.section(f"差分レポート: {screen_id}")
        
        if comparison.added_lines:
            self.logger.info("🟢 追加された行:")
            for line in comparison.added_lines[:10]:  # 最初の10行のみ表示
                print(f"  + {line}")
            if len(comparison.added_lines) > 10:
                print(f"  ... 他 {len(comparison.added_lines) - 10} 行")
        
        if comparison.removed_lines:
            self.logger.info("🔴 削除された行:")
            for line in comparison.removed_lines[:10]:  # 最初の10行のみ表示
                print(f"  - {line}")
            if len(comparison.removed_lines) > 10:
                print(f"  ... 他 {len(comparison.removed_lines) - 10} 行")
        
        self.logger.info(f"📊 変更サマリー: +{len(comparison.added_lines)} -{len(comparison.removed_lines)}")

class ScreenDefinitionManager:
    """画面定義書管理クラス"""
    
    def __init__(self, base_dir: str = None, logger: EnhancedLogger = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.specs_dir = self.base_dir / "specs"
        self.details_dir = self.base_dir / "screen-details"
        self.screen_list_file = self.base_dir / "画面一覧.md"
        self.logger = logger or EnhancedLogger()
        
        # 各種クラスのインスタンス化
        self.validator = ScreenDefinitionValidator(self.logger)
        self.comparator = ScreenDefinitionComparator(self.logger)
        
        # ディレクトリ作成
        self._ensure_directories()
    
    def _ensure_directories(self):
        """必要なディレクトリを作成"""
        try:
            self.specs_dir.mkdir(exist_ok=True)
            self.details_dir.mkdir(exist_ok=True)
        except Exception as e:
            self.logger.error(f"ディレクトリ作成に失敗しました: {e}")
            raise
    
    def load_screen_info(self, screen_id: str) -> Optional[Dict[str, Any]]:
        """画面一覧から画面情報を読み込み"""
        if not self.screen_list_file.exists():
            self.logger.error(f"画面一覧ファイルが見つかりません: {self.screen_list_file}")
            return None
        
        with open(self.screen_list_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 画面情報を抽出
        lines = content.split('\n')
        in_table = False
        
        for line in lines:
            if '| 画面ID |' in line and '画面名称' in line:
                in_table = True
                continue
            
            if in_table and line.startswith('|---'):
                continue
            
            if in_table and (line.strip() == '' or not line.startswith('|')):
                in_table = False
                continue
            
            if in_table and f"[{screen_id}]" in line:
                parts = [part.strip() for part in line.split('|')]
                if len(parts) >= 7:
                    return {
                        'screen_id': screen_id,
                        'screen_name': parts[2],
                        'category': parts[3],
                        'function': parts[4],
                        'users': parts[5],
                        'priority': parts[6],
                        'notes': parts[7] if len(parts) > 7 else ""
                    }
        
        return None
    
    def load_yaml_details(self, screen_id: str) -> Tuple[Optional[Dict[str, Any]], bool]:
        """YAML詳細定義を読み込み"""
        details_file = self.details_dir / f"{screen_id}_details.yaml"
        
        if not details_file.exists():
            return None, False
        
        try:
            with open(details_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f), True
        except Exception as e:
            self.logger.error(f"{details_file} の読み込みに失敗: {e}")
            return None, False
    
    def load_current_markdown(self, screen_id: str, screen_name: str) -> Tuple[Optional[str], bool]:
        """現在のMarkdownファイルを読み込み"""
        md_file = self.specs_dir / f"画面定義書_{screen_id}_{screen_name}.md"
        
        if not md_file.exists():
            return None, False
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                return f.read(), True
        except Exception as e:
            self.logger.error(f"{md_file} の読み込みに失敗: {e}")
            return None, False
    
    def generate_markdown_from_yaml(self, screen_id: str, screen_info: Dict[str, Any], yaml_data: Dict[str, Any]) -> str:
        """YAMLからMarkdownを生成"""
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
        if 'screen_overview' in yaml_data:
            overview = yaml_data['screen_overview']
            md_content += f"## 画面概要\n\n"
            md_content += f"### 目的\n{overview.get('purpose', '')}\n\n"
            if overview.get('main_functions'):
                md_content += f"### 主な機能\n"
                for func in overview['main_functions']:
                    md_content += f"- {func}\n"
                md_content += "\n"
        
        # 画面レイアウト
        if 'screen_layout' in yaml_data:
            layout = yaml_data['screen_layout']
            md_content += f"## 画面レイアウト\n\n"
            md_content += f"{layout.get('description', '')}\n\n"
            if layout.get('sections'):
                md_content += f"| セクション名 | 説明 |\n"
                md_content += f"|-------------|------|\n"
                for section in layout['sections']:
                    md_content += f"| {section['section_name']} | {section['description']} |\n"
                md_content += "\n"
        
        # 画面項目定義
        if 'screen_items' in yaml_data:
            md_content += f"## 画面項目定義\n\n"
            md_content += f"| 項目ID | 項目名 | APIパラメータ対応 | データ型 | I/O区分 | 必須 | 備考 |\n"
            md_content += f"|--------|--------|-------------------|----------|---------|------|------|\n"
            for item in yaml_data['screen_items']:
                required = "○" if item.get('required', False) else "×"
                md_content += f"| {item['item_id']} | {item['item_name']} | {item.get('api_parameter', '')} | {item['data_type']} | {item['io_type']} | {required} | {item.get('remarks', '')} |\n"
            md_content += "\n"
        
        # 操作フロー
        if 'operation_flow' in yaml_data:
            md_content += f"## 操作フロー\n\n"
            md_content += f"| ステップ | 操作 | 説明 |\n"
            md_content += f"|----------|------|------|\n"
            for flow in yaml_data['operation_flow']:
                md_content += f"| {flow['step']} | {flow['operation']} | {flow['description']} |\n"
            md_content += "\n"
        
        # イベント・アクション定義
        if 'events' in yaml_data:
            md_content += f"## イベント・アクション定義\n\n"
            md_content += f"| イベントID | トリガー/アクション | イベント内容・アクション詳細 | 紐付くAPI ID・名称 | メッセージ表示 |\n"
            md_content += f"|------------|---------------------|------------------------------|-------------------|----------------|\n"
            for event in yaml_data['events']:
                md_content += f"| {event['event_id']} | {event['trigger_action']} | {event['event_detail']} | {event.get('related_api', '')} | {event.get('message_display', '')} |\n"
            md_content += "\n"
        
        # 改版履歴
        if 'revision_history' in yaml_data:
            md_content += f"## 改版履歴\n\n"
            md_content += f"| バージョン | 更新日 | 更新者 | 変更内容 |\n"
            md_content += f"|------------|--------|--------|----------|\n"
            for revision in yaml_data['revision_history']:
                md_content += f"| {revision['version']} | {revision['date']} | {revision['author']} | {revision['changes']} |\n"
            md_content += "\n"
        
        return md_content
    
    def backup_files(self, screen_id: str, screen_name: str) -> bool:
        """ファイルバックアップ"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        try:
            # Markdownファイルのバックアップ
            md_file = self.specs_dir / f"画面定義書_{screen_id}_{screen_name}.md"
            if md_file.exists():
                backup_md = md_file.with_suffix(f".md.backup.{timestamp}")
                backup_md.write_text(md_file.read_text(encoding='utf-8'), encoding='utf-8')
                self.logger.success(f"📁 Markdownバックアップ作成: {backup_md.name}")
            
            return True
        except Exception as e:
            self.logger.error(f"バックアップ作成に失敗: {e}")
            return False
    
    def update_markdown_file(self, screen_id: str, screen_name: str, new_content: str, dry_run: bool = False) -> bool:
        """Markdownファイル更新"""
        md_file = self.specs_dir / f"画面定義書_{screen_id}_{screen_name}.md"
        
        if dry_run:
            self.logger.info(f"[DRY] 更新予定: {md_file.name}")
            return True
        
        try:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            self.logger.success(f"✅ ファイル更新完了: {md_file.name}")
            return True
        except Exception as e:
            self.logger.error(f"ファイル更新に失敗: {e}")
            return False
    
    def commit_changes(self, screen_id: str, message: str = None, dry_run: bool = False) -> bool:
        """Git コミット"""
        if not message:
            message = f"🔧 feat: {screen_id}画面定義書の検証・更新\n\n- 画面定義書の整合性チェック完了\n- YAML-Markdown同期更新\n- 生成日時を最新に更新"
        
        if dry_run:
            self.logger.info(f"[DRY] コミット予定メッセージ:\n{message}")
            return True
        
        try:
            # Git add
            subprocess.run(['git', 'add', '.'], cwd=self.base_dir, check=True, capture_output=True)
            
            # Git commit
            subprocess.run(['git', 'commit', '-m', message], cwd=self.base_dir, check=True, capture_output=True)
            
            self.logger.success(f"✅ Gitコミット完了")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Gitコミットに失敗: {e}")
            return False
        except Exception as e:
            self.logger.error(f"予期しないエラー: {e}")
            return False
    
    def validate_screen(self, screen_id: str) -> ValidationResult:
        """画面定義書検証メイン処理"""
        self.logger.section(f"検証開始: {screen_id}")
        
        # 画面情報読み込み
        screen_info = self.load_screen_info(screen_id)
        if not screen_info:
            return ValidationResult(
                screen_id=screen_id,
                screen_name="不明",
                yaml_exists=False,
                markdown_exists=False,
                yaml_valid=False,
                markdown_valid=False,
                consistency_check=False,
                issues=[f"画面一覧.mdに{screen_id}が見つかりません"],
                warnings=[],
                suggestions=["画面一覧.mdに画面情報を追加してください"]
            )
        
        screen_name = screen_info['screen_name']
        
        # YAML読み込み・検証
        yaml_data, yaml_exists = self.load_yaml_details(screen_id)
        yaml_valid = False
        yaml_issues = []
        yaml_warnings = []
        
        if yaml_exists and yaml_data:
            yaml_valid, yaml_issues, yaml_warnings = self.validator.validate_yaml_structure(yaml_data)
        
        # Markdown読み込み・検証
        md_content, md_exists = self.load_current_markdown(screen_id, screen_name)
        md_valid = False
        md_issues = []
        md_warnings = []
        
        if md_exists and md_content:
            md_valid, md_issues, md_warnings = self.validator.validate_markdown_structure(md_content)
        
        # 整合性チェック
        consistency_check = False
        consistency_issues = []
        
        if yaml_exists and md_exists and yaml_data and md_content:
            consistency_check, consistency_issues = self.validator.check_consistency(yaml_data, md_content)
        
        # 結果統合
        all_issues = yaml_issues + md_issues + consistency_issues
        all_warnings = yaml_warnings + md_warnings
        suggestions = []
        
        if not yaml_exists:
            suggestions.append(f"{screen_id}_details.yamlファイルを作成してください")
        if not md_exists:
            suggestions.append(f"画面定義書_{screen_id}_{screen_name}.mdファイルを生成してください")
        
        return ValidationResult(
            screen_id=screen_id,
            screen_name=screen_name,
            yaml_exists=yaml_exists,
            markdown_exists=md_exists,
            yaml_valid=yaml_valid,
            markdown_valid=md_valid,
            consistency_check=consistency_check,
            issues=all_issues,
            warnings=all_warnings,
            suggestions=suggestions
        )
    
    def process_screen(self, screen_id: str, validate_only: bool = False, show_diff: bool = False, 
                      backup: bool = False, force_update: bool = False, commit: bool = False, 
                      dry_run: bool = False) -> bool:
        """画面処理メイン関数"""
        self.logger.header(f"画面定義書処理: {screen_id}")
        
        # 検証実行
        validation = self.validate_screen(screen_id)
        
        # 検証結果表示
        self._print_validation_result(validation)
        
        if validate_only:
            return validation.yaml_valid and validation.markdown_valid and validation.consistency_check
        
        # ファイル生成・比較
        if validation.yaml_exists:
            screen_info = self.load_screen_info(screen_id)
            yaml_data, _ = self.load_yaml_details(screen_id)
            
            if screen_info and yaml_data:
                # 新しいMarkdownを生成
                new_md_content = self.generate_markdown_from_yaml(screen_id, screen_info, yaml_data)
                
                # 既存ファイルと比較
                if validation.markdown_exists:
                    current_md, _ = self.load_current_markdown(screen_id, validation.screen_name)
                    if current_md:
                        comparison = self.comparator.compare_files(current_md, new_md_content)
                        
                        if show_diff:
                            self.comparator.show_diff(comparison, screen_id)
                        
                        if not comparison.has_differences:
                            self.logger.success("📄 ファイルに変更はありません")
                            return True
                        
                        if not force_update and not dry_run:
                            self.logger.warning("⚠️  ファイルに差分があります。--force-update で更新してください")
                            return False
                
                # バックアップ作成
                if backup and not dry_run:
                    self.backup_files(screen_id, validation.screen_name)
                
                # ファイル更新
                if force_update or not validation.markdown_exists:
                    success = self.update_markdown_file(screen_id, validation.screen_name, new_md_content, dry_run)
                    if not success:
                        return False
                
                # コミット
                if commit:
                    return self.commit_changes(screen_id, dry_run=dry_run)
                
                return True
        
        return False
    
    def _print_validation_result(self, result: ValidationResult):
        """検証結果表示"""
        self.logger.section(f"検証結果: {result.screen_id}")
        
        # ファイル存在チェック
        yaml_status = "✅" if result.yaml_exists else "❌"
        md_status = "✅" if result.markdown_exists else "❌"
        self.logger.info(f"YAMLファイル: {yaml_status} 存在")
        self.logger.info(f"Markdownファイル: {md_status} 存在")
        
        # 構造検証結果
        if result.yaml_exists:
            yaml_valid_status = "✅" if result.yaml_valid else "❌"
            self.logger.info(f"YAML構造: {yaml_valid_status} {'有効' if result.yaml_valid else '無効'}")
        
        if result.markdown_exists:
            md_valid_status = "✅" if result.markdown_valid else "❌"
            self.logger.info(f"Markdown構造: {md_valid_status} {'有効' if result.markdown_valid else '無効'}")
        
        # 整合性チェック結果
        if result.yaml_exists and result.markdown_exists:
            consistency_status = "✅" if result.consistency_check else "❌"
            self.logger.info(f"整合性チェック: {consistency_status} {'一致' if result.consistency_check else '不一致'}")
        
        # 問題点表示
        if result.issues:
            self.logger.section("問題点")
            for issue in result.issues:
                self.logger.error(f"  - {issue}")
        
        # 警告表示
        if result.warnings:
            self.logger.section("警告")
            for warning in result.warnings:
                self.logger.warning(f"  - {warning}")
        
        # 提案表示
        if result.suggestions:
            self.logger.section("提案")
            for suggestion in result.suggestions:
                self.logger.info(f"  💡 {suggestion}")

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="画面定義書検証・更新スクリプト v1.0 (拡張版)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""使用例:
  # 検証のみ
  python3 create_screen_definitions_enhanced.py --screen SCR_AUT_Login --validate-only

  # 差分表示
  python3 create_screen_definitions_enhanced.py --screen SCR_AUT_Login --show-diff

  # バックアップ付き更新
  python3 create_screen_definitions_enhanced.py --screen SCR_AUT_Login --backup --force-update

  # 自動コミット
  python3 create_screen_definitions_enhanced.py --screen SCR_AUT_Login --force-update --commit

  # ドライラン
  python3 create_screen_definitions_enhanced.py --screen SCR_AUT_Login --force-update --dry-run
        """
    )

    parser.add_argument(
        '--screen', '-s',
        required=True,
        help='処理対象画面ID'
    )

    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='検証のみ実行（ファイル更新なし）'
    )

    parser.add_argument(
        '--show-diff',
        action='store_true',
        help='差分表示'
    )

    parser.add_argument(
        '--backup',
        action='store_true',
        help='更新前にバックアップ作成'
    )

    parser.add_argument(
        '--force-update',
        action='store_true',
        help='強制的にファイル更新'
    )

    parser.add_argument(
        '--commit',
        action='store_true',
        help='更新後に自動コミット'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='ドライラン（実際にはファイル操作しない）'
    )

    parser.add_argument(
        '--no-color',
        action='store_true',
        help='カラー出力を無効化'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='詳細ログを表示'
    )

    parser.add_argument(
        '--base-dir', '-b',
        help='ベースディレクトリ（デフォルト: スクリプトのディレクトリ）'
    )

    args = parser.parse_args()

    try:
        # ログ設定
        logger = EnhancedLogger(not args.no_color, args.verbose)
        
        # マネージャー初期化
        manager = ScreenDefinitionManager(args.base_dir, logger)
        
        # 処理実行
        success = manager.process_screen(
            args.screen,
            validate_only=args.validate_only,
            show_diff=args.show_diff,
            backup=args.backup,
            force_update=args.force_update,
            commit=args.commit,
            dry_run=args.dry_run
        )
        
        if success:
            logger.success("🎉 処理が正常に完了しました")
            sys.exit(0)
        else:
            logger.error("❌ 処理中にエラーが発生しました")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n❌ 処理が中断されました")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 予期しないエラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
