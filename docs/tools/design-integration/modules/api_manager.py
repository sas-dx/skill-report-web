"""
設計統合ツール - API設計管理モジュール
要求仕様ID: PLT.1-WEB.1

API設計書の管理・検証・生成機能を提供します。
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import yaml

from ..core.config import DesignIntegrationConfig
from ..core.exceptions import DesignIntegrationError
from ..core.logger import get_logger


class APIDesignManager:
    """API設計管理クラス"""
    
    def __init__(self, config: DesignIntegrationConfig):
        """
        初期化
        
        Args:
            config: 設計統合ツール設定
        """
        self.config = config
        self.logger = get_logger(__name__)
        
        # API設計書のディレクトリ
        self.api_specs_dir = config.project_root / "docs" / "design" / "api" / "specs"
        
        # API設計書のパターン
        self.api_spec_pattern = re.compile(r"API定義書_API-(\d+)_(.+)\.md")
    
    def validate_all(self, verbose: bool = False) -> bool:
        """
        全API設計を検証
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            検証成功フラグ
        """
        self.logger.info("全API設計の検証を開始")
        
        if not self.api_specs_dir.exists():
            self.logger.error(f"API設計書ディレクトリが存在しません: {self.api_specs_dir}")
            return False
        
        api_files = list(self.api_specs_dir.glob("API定義書_*.md"))
        if not api_files:
            self.logger.warning("API設計書が見つかりません")
            return True
        
        success_count = 0
        total_count = len(api_files)
        
        for api_file in api_files:
            api_id = self._extract_api_id(api_file.name)
            if api_id:
                if self.validate_api(api_id, verbose):
                    success_count += 1
                else:
                    if verbose:
                        print(f"❌ API {api_id} の検証に失敗しました")
            else:
                self.logger.warning(f"API IDを抽出できません: {api_file.name}")
        
        success_rate = success_count / total_count if total_count > 0 else 0
        
        if verbose:
            print(f"\n📊 API設計検証結果: {success_count}/{total_count} 成功 ({success_rate:.1%})")
        
        if success_count == total_count:
            self.logger.info("全API設計の検証が完了しました")
            return True
        else:
            self.logger.error(f"API設計の検証でエラーが発生しました: {total_count - success_count} 件")
            return False
    
    def validate_api(self, api_id: str, verbose: bool = False) -> bool:
        """
        特定APIの設計を検証
        
        Args:
            api_id: API ID (例: API-021)
            verbose: 詳細出力フラグ
            
        Returns:
            検証成功フラグ
        """
        self.logger.info(f"API {api_id} の設計検証を開始")
        
        api_info = self.get_api_info(api_id)
        if not api_info:
            self.logger.error(f"API {api_id} の情報を取得できません")
            return False
        
        validation_errors = []
        
        # 必須フィールドの検証
        required_fields = ['title', 'endpoint', 'method', 'description']
        for field in required_fields:
            if field not in api_info or not api_info[field]:
                validation_errors.append(f"必須フィールド '{field}' が不足しています")
        
        # エンドポイント形式の検証
        if 'endpoint' in api_info:
            endpoint = api_info['endpoint']
            if not endpoint.startswith('/api/'):
                validation_errors.append(f"エンドポイントは '/api/' で始まる必要があります: {endpoint}")
        
        # HTTPメソッドの検証
        if 'method' in api_info:
            method = api_info['method'].upper()
            valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
            if method not in valid_methods:
                validation_errors.append(f"無効なHTTPメソッド: {method}")
        
        # レスポンス形式の検証
        if 'responses' in api_info:
            responses = api_info['responses']
            if not isinstance(responses, dict):
                validation_errors.append("レスポンス定義は辞書形式である必要があります")
            else:
                # 成功レスポンス（200番台）の存在確認
                success_responses = [code for code in responses.keys() if str(code).startswith('2')]
                if not success_responses:
                    validation_errors.append("成功レスポンス（200番台）が定義されていません")
        
        if validation_errors:
            if verbose:
                print(f"❌ API {api_id} の検証エラー:")
                for error in validation_errors:
                    print(f"  - {error}")
            self.logger.error(f"API {api_id} の検証でエラーが発生しました: {len(validation_errors)} 件")
            return False
        else:
            if verbose:
                print(f"✅ API {api_id} の検証が完了しました")
            self.logger.info(f"API {api_id} の設計検証が完了しました")
            return True
    
    def generate_all(self, verbose: bool = False) -> bool:
        """
        全API設計書を生成
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            生成成功フラグ
        """
        self.logger.info("全API設計書の生成を開始")
        
        # 現在は既存のAPI設計書の整合性チェックのみ実装
        # 将来的にはテンプレートからの自動生成機能を追加予定
        
        api_list = self.get_api_list()
        if not api_list:
            self.logger.warning("API設計書が見つかりません")
            return True
        
        success_count = 0
        total_count = len(api_list)
        
        for api_id in api_list:
            if self._ensure_api_consistency(api_id, verbose):
                success_count += 1
            else:
                if verbose:
                    print(f"❌ API {api_id} の整合性確保に失敗しました")
        
        success_rate = success_count / total_count if total_count > 0 else 0
        
        if verbose:
            print(f"\n📊 API設計書生成結果: {success_count}/{total_count} 成功 ({success_rate:.1%})")
        
        if success_count == total_count:
            self.logger.info("全API設計書の生成が完了しました")
            return True
        else:
            self.logger.error(f"API設計書の生成でエラーが発生しました: {total_count - success_count} 件")
            return False
    
    def generate_api(self, api_id: str, verbose: bool = False) -> bool:
        """
        特定APIの設計書を生成
        
        Args:
            api_id: API ID
            verbose: 詳細出力フラグ
            
        Returns:
            生成成功フラグ
        """
        self.logger.info(f"API {api_id} の設計書生成を開始")
        
        if self._ensure_api_consistency(api_id, verbose):
            if verbose:
                print(f"✅ API {api_id} の設計書生成が完了しました")
            self.logger.info(f"API {api_id} の設計書生成が完了しました")
            return True
        else:
            if verbose:
                print(f"❌ API {api_id} の設計書生成に失敗しました")
            self.logger.error(f"API {api_id} の設計書生成でエラーが発生しました")
            return False
    
    def _ensure_api_consistency(self, api_id: str, verbose: bool = False) -> bool:
        """
        API設計書の整合性を確保
        
        Args:
            api_id: API ID
            verbose: 詳細出力フラグ
            
        Returns:
            整合性確保成功フラグ
        """
        try:
            api_info = self.get_api_info(api_id)
            if not api_info:
                return False
            
            # 現在は検証のみ実装
            # 将来的には不整合の自動修正機能を追加予定
            return self.validate_api(api_id, verbose)
            
        except Exception as e:
            self.logger.error(f"API {api_id} の整合性確保エラー: {e}")
            return False
    
    def get_api_list(self) -> List[str]:
        """
        API一覧を取得
        
        Returns:
            API IDのリスト
        """
        try:
            if not self.api_specs_dir.exists():
                return []
            
            api_ids = []
            for api_file in self.api_specs_dir.glob("API定義書_*.md"):
                api_id = self._extract_api_id(api_file.name)
                if api_id:
                    api_ids.append(api_id)
            
            return sorted(api_ids)
            
        except Exception as e:
            self.logger.error(f"API一覧取得エラー: {e}")
            return []
    
    def get_api_info(self, api_id: str) -> Optional[Dict[str, Any]]:
        """
        API情報を取得
        
        Args:
            api_id: API ID
            
        Returns:
            API情報辞書
        """
        try:
            api_files = list(self.api_specs_dir.glob(f"API定義書_{api_id}_*.md"))
            if not api_files:
                return None
            
            api_file = api_files[0]
            
            # Markdownファイルからメタデータを抽出
            api_info = self._parse_api_markdown(api_file)
            
            return api_info
            
        except Exception as e:
            self.logger.error(f"API情報取得エラー ({api_id}): {e}")
            return None
    
    def _extract_api_id(self, filename: str) -> Optional[str]:
        """
        ファイル名からAPI IDを抽出
        
        Args:
            filename: ファイル名
            
        Returns:
            API ID
        """
        match = self.api_spec_pattern.match(filename)
        if match:
            return f"API-{match.group(1)}"
        return None
    
    def _parse_api_markdown(self, api_file: Path) -> Dict[str, Any]:
        """
        API設計書Markdownファイルを解析
        
        Args:
            api_file: API設計書ファイル
            
        Returns:
            API情報辞書
        """
        try:
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            api_info = {
                'file_path': str(api_file),
                'title': '',
                'endpoint': '',
                'method': '',
                'description': '',
                'parameters': {},
                'responses': {},
                'requirement_id': ''
            }
            
            lines = content.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                
                # タイトル抽出
                if line.startswith('# ') and not api_info['title']:
                    api_info['title'] = line[2:].strip()
                
                # エンドポイント抽出
                elif 'エンドポイント' in line and ':' in line:
                    endpoint = line.split(':', 1)[1].strip()
                    if endpoint.startswith('`') and endpoint.endswith('`'):
                        endpoint = endpoint[1:-1]
                    api_info['endpoint'] = endpoint
                
                # HTTPメソッド抽出
                elif 'HTTPメソッド' in line and ':' in line:
                    method = line.split(':', 1)[1].strip()
                    if method.startswith('`') and method.endswith('`'):
                        method = method[1:-1]
                    api_info['method'] = method
                
                # 要求仕様ID抽出
                elif '要求仕様ID' in line and ':' in line:
                    req_id = line.split(':', 1)[1].strip()
                    api_info['requirement_id'] = req_id
                
                # 概要抽出
                elif line.startswith('## 概要'):
                    current_section = 'description'
                elif current_section == 'description' and line and not line.startswith('#'):
                    if api_info['description']:
                        api_info['description'] += ' ' + line
                    else:
                        api_info['description'] = line
                
                # セクション変更
                elif line.startswith('##'):
                    current_section = None
            
            return api_info
            
        except Exception as e:
            self.logger.error(f"API Markdown解析エラー ({api_file}): {e}")
            return {}
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        API設計の統計情報を取得
        
        Returns:
            統計情報辞書
        """
        try:
            api_list = self.get_api_list()
            
            stats = {
                'total_apis': len(api_list),
                'methods': {},
                'endpoints_by_category': {},
                'apis_with_issues': 0,
                'requirement_coverage': {}
            }
            
            for api_id in api_list:
                api_info = self.get_api_info(api_id)
                if api_info:
                    # HTTPメソッド別集計
                    method = api_info.get('method', 'UNKNOWN').upper()
                    if method not in stats['methods']:
                        stats['methods'][method] = 0
                    stats['methods'][method] += 1
                    
                    # エンドポイントカテゴリ別集計
                    endpoint = api_info.get('endpoint', '')
                    if endpoint.startswith('/api/'):
                        category = endpoint.split('/')[2] if len(endpoint.split('/')) > 2 else 'other'
                        if category not in stats['endpoints_by_category']:
                            stats['endpoints_by_category'][category] = 0
                        stats['endpoints_by_category'][category] += 1
                    
                    # 要求仕様ID別集計
                    req_id = api_info.get('requirement_id', '')
                    if req_id:
                        if req_id not in stats['requirement_coverage']:
                            stats['requirement_coverage'][req_id] = 0
                        stats['requirement_coverage'][req_id] += 1
                    
                    # 検証エラーチェック
                    if not self.validate_api(api_id, verbose=False):
                        stats['apis_with_issues'] += 1
            
            return stats
            
        except Exception as e:
            self.logger.error(f"統計情報取得エラー: {e}")
            return {}
