"""
設計統合ツール - 画面設計管理モジュール
要求仕様ID: PLT.1-WEB.1

画面設計書の管理・検証・生成機能を提供します。
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

import sys
from pathlib import Path

# パスを追加してモジュールをインポート
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

try:
    from core.config import DesignIntegrationConfig
    from core.exceptions import DesignIntegrationError
    from core.logger import get_logger
except ImportError as e:
    print(f"インポートエラー: {e}")
    # フォールバック用の基本クラス
    class DesignIntegrationConfig:
        def __init__(self, config_path=None):
            self.project_root = Path.cwd()
        def get_screen_specs_dir(self):
            return self.project_root / "docs" / "design" / "screens" / "specs"
    
    class DesignIntegrationError(Exception):
        pass
    
    def get_logger(name):
        import logging
        return logging.getLogger(name)


class ScreenDesignManager:
    """画面設計管理クラス"""
    
    def __init__(self, config: DesignIntegrationConfig):
        """
        初期化
        
        Args:
            config: 設計統合ツール設定
        """
        self.config = config
        self.logger = get_logger(__name__)
        
        # 画面設計書のディレクトリ
        self.screen_specs_dir = config.project_root / "docs" / "design" / "screens" / "specs"
        
        # 画面設計書のパターン
        self.screen_spec_pattern = re.compile(r"画面設計書_SCR-([A-Z]+)_(.+)\.md")
    
    def validate_all(self, verbose: bool = False) -> bool:
        """
        全画面設計を検証
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            検証成功フラグ
        """
        self.logger.info("全画面設計の検証を開始")
        
        if not self.screen_specs_dir.exists():
            self.logger.error(f"画面設計書ディレクトリが存在しません: {self.screen_specs_dir}")
            return False
        
        screen_files = list(self.screen_specs_dir.glob("画面設計書_*.md"))
        if not screen_files:
            self.logger.warning("画面設計書が見つかりません")
            return True
        
        success_count = 0
        total_count = len(screen_files)
        
        for screen_file in screen_files:
            screen_id = self._extract_screen_id(screen_file.name)
            if screen_id:
                if self.validate_screen(screen_id, verbose):
                    success_count += 1
                else:
                    if verbose:
                        print(f"❌ 画面 {screen_id} の検証に失敗しました")
            else:
                self.logger.warning(f"画面IDを抽出できません: {screen_file.name}")
        
        success_rate = success_count / total_count if total_count > 0 else 0
        
        if verbose:
            print(f"\n📊 画面設計検証結果: {success_count}/{total_count} 成功 ({success_rate:.1%})")
        
        if success_count == total_count:
            self.logger.info("全画面設計の検証が完了しました")
            return True
        else:
            self.logger.error(f"画面設計の検証でエラーが発生しました: {total_count - success_count} 件")
            return False
    
    def validate_screen(self, screen_id: str, verbose: bool = False) -> bool:
        """
        特定画面の設計を検証
        
        Args:
            screen_id: 画面ID (例: SCR-SKILL)
            verbose: 詳細出力フラグ
            
        Returns:
            検証成功フラグ
        """
        self.logger.info(f"画面 {screen_id} の設計検証を開始")
        
        screen_info = self.get_screen_info(screen_id)
        if not screen_info:
            self.logger.error(f"画面 {screen_id} の情報を取得できません")
            return False
        
        validation_errors = []
        
        # 必須フィールドの検証
        required_fields = ['title', 'url', 'description', 'components']
        for field in required_fields:
            if field not in screen_info or not screen_info[field]:
                validation_errors.append(f"必須フィールド '{field}' が不足しています")
        
        # URL形式の検証
        if 'url' in screen_info:
            url = screen_info['url']
            if not url.startswith('/'):
                validation_errors.append(f"URLは '/' で始まる必要があります: {url}")
        
        # コンポーネント定義の検証
        if 'components' in screen_info:
            components = screen_info['components']
            if not isinstance(components, list):
                validation_errors.append("コンポーネント定義はリスト形式である必要があります")
            elif len(components) == 0:
                validation_errors.append("少なくとも1つのコンポーネントが定義されている必要があります")
        
        # レスポンシブ対応の検証
        if 'responsive' in screen_info:
            responsive = screen_info['responsive']
            if not isinstance(responsive, dict):
                validation_errors.append("レスポンシブ定義は辞書形式である必要があります")
            else:
                required_breakpoints = ['mobile', 'tablet', 'desktop']
                for breakpoint in required_breakpoints:
                    if breakpoint not in responsive:
                        validation_errors.append(f"レスポンシブ定義に '{breakpoint}' が不足しています")
        
        if validation_errors:
            if verbose:
                print(f"❌ 画面 {screen_id} の検証エラー:")
                for error in validation_errors:
                    print(f"  - {error}")
            self.logger.error(f"画面 {screen_id} の検証でエラーが発生しました: {len(validation_errors)} 件")
            return False
        else:
            if verbose:
                print(f"✅ 画面 {screen_id} の検証が完了しました")
            self.logger.info(f"画面 {screen_id} の設計検証が完了しました")
            return True
    
    def generate_all(self, verbose: bool = False) -> bool:
        """
        全画面設計書を生成
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            生成成功フラグ
        """
        self.logger.info("全画面設計書の生成を開始")
        
        # 現在は既存の画面設計書の整合性チェックのみ実装
        # 将来的にはテンプレートからの自動生成機能を追加予定
        
        screen_list = self.get_screen_list()
        if not screen_list:
            self.logger.warning("画面設計書が見つかりません")
            return True
        
        success_count = 0
        total_count = len(screen_list)
        
        for screen_id in screen_list:
            if self._ensure_screen_consistency(screen_id, verbose):
                success_count += 1
            else:
                if verbose:
                    print(f"❌ 画面 {screen_id} の整合性確保に失敗しました")
        
        success_rate = success_count / total_count if total_count > 0 else 0
        
        if verbose:
            print(f"\n📊 画面設計書生成結果: {success_count}/{total_count} 成功 ({success_rate:.1%})")
        
        if success_count == total_count:
            self.logger.info("全画面設計書の生成が完了しました")
            return True
        else:
            self.logger.error(f"画面設計書の生成でエラーが発生しました: {total_count - success_count} 件")
            return False
    
    def generate_screen(self, screen_id: str, verbose: bool = False) -> bool:
        """
        特定画面の設計書を生成
        
        Args:
            screen_id: 画面ID
            verbose: 詳細出力フラグ
            
        Returns:
            生成成功フラグ
        """
        self.logger.info(f"画面 {screen_id} の設計書生成を開始")
        
        if self._ensure_screen_consistency(screen_id, verbose):
            if verbose:
                print(f"✅ 画面 {screen_id} の設計書生成が完了しました")
            self.logger.info(f"画面 {screen_id} の設計書生成が完了しました")
            return True
        else:
            if verbose:
                print(f"❌ 画面 {screen_id} の設計書生成に失敗しました")
            self.logger.error(f"画面 {screen_id} の設計書生成でエラーが発生しました")
            return False
    
    def _ensure_screen_consistency(self, screen_id: str, verbose: bool = False) -> bool:
        """
        画面設計書の整合性を確保
        
        Args:
            screen_id: 画面ID
            verbose: 詳細出力フラグ
            
        Returns:
            整合性確保成功フラグ
        """
        try:
            screen_info = self.get_screen_info(screen_id)
            if not screen_info:
                return False
            
            # 現在は検証のみ実装
            # 将来的には不整合の自動修正機能を追加予定
            return self.validate_screen(screen_id, verbose)
            
        except Exception as e:
            self.logger.error(f"画面 {screen_id} の整合性確保エラー: {e}")
            return False
    
    def get_screen_list(self) -> List[str]:
        """
        画面一覧を取得
        
        Returns:
            画面IDのリスト
        """
        try:
            if not self.screen_specs_dir.exists():
                return []
            
            screen_ids = []
            for screen_file in self.screen_specs_dir.glob("画面設計書_*.md"):
                screen_id = self._extract_screen_id(screen_file.name)
                if screen_id:
                    screen_ids.append(screen_id)
            
            return sorted(screen_ids)
            
        except Exception as e:
            self.logger.error(f"画面一覧取得エラー: {e}")
            return []
    
    def get_screen_info(self, screen_id: str) -> Optional[Dict[str, Any]]:
        """
        画面情報を取得
        
        Args:
            screen_id: 画面ID
            
        Returns:
            画面情報辞書
        """
        try:
            screen_files = list(self.screen_specs_dir.glob(f"画面設計書_{screen_id}_*.md"))
            if not screen_files:
                return None
            
            screen_file = screen_files[0]
            
            # Markdownファイルからメタデータを抽出
            screen_info = self._parse_screen_markdown(screen_file)
            
            return screen_info
            
        except Exception as e:
            self.logger.error(f"画面情報取得エラー ({screen_id}): {e}")
            return None
    
    def _extract_screen_id(self, filename: str) -> Optional[str]:
        """
        ファイル名から画面IDを抽出
        
        Args:
            filename: ファイル名
            
        Returns:
            画面ID
        """
        match = self.screen_spec_pattern.match(filename)
        if match:
            return f"SCR-{match.group(1)}"
        return None
    
    def _parse_screen_markdown(self, screen_file: Path) -> Dict[str, Any]:
        """
        画面設計書Markdownファイルを解析
        
        Args:
            screen_file: 画面設計書ファイル
            
        Returns:
            画面情報辞書
        """
        try:
            with open(screen_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            screen_info = {
                'file_path': str(screen_file),
                'title': '',
                'url': '',
                'description': '',
                'components': [],
                'responsive': {},
                'requirement_id': '',
                'wireframe': '',
                'interactions': []
            }
            
            lines = content.split('\n')
            current_section = None
            current_component = None
            
            for line in lines:
                line = line.strip()
                
                # タイトル抽出
                if line.startswith('# ') and not screen_info['title']:
                    screen_info['title'] = line[2:].strip()
                
                # URL抽出
                elif 'URL' in line and ':' in line:
                    url = line.split(':', 1)[1].strip()
                    if url.startswith('`') and url.endswith('`'):
                        url = url[1:-1]
                    screen_info['url'] = url
                
                # 要求仕様ID抽出
                elif '要求仕様ID' in line and ':' in line:
                    req_id = line.split(':', 1)[1].strip()
                    screen_info['requirement_id'] = req_id
                
                # 概要抽出
                elif line.startswith('## 概要'):
                    current_section = 'description'
                elif current_section == 'description' and line and not line.startswith('#'):
                    if screen_info['description']:
                        screen_info['description'] += ' ' + line
                    else:
                        screen_info['description'] = line
                
                # コンポーネント抽出
                elif line.startswith('## コンポーネント'):
                    current_section = 'components'
                elif current_section == 'components' and line.startswith('### '):
                    component_name = line[4:].strip()
                    current_component = {
                        'name': component_name,
                        'description': '',
                        'props': [],
                        'events': []
                    }
                    screen_info['components'].append(current_component)
                elif current_section == 'components' and current_component and line and not line.startswith('#'):
                    if not current_component['description']:
                        current_component['description'] = line
                
                # レスポンシブ対応抽出
                elif line.startswith('## レスポンシブ'):
                    current_section = 'responsive'
                elif current_section == 'responsive' and line.startswith('### '):
                    breakpoint = line[4:].strip().lower()
                    screen_info['responsive'][breakpoint] = True
                
                # セクション変更
                elif line.startswith('##'):
                    current_section = None
                    current_component = None
            
            return screen_info
            
        except Exception as e:
            self.logger.error(f"画面 Markdown解析エラー ({screen_file}): {e}")
            return {}
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        画面設計の統計情報を取得
        
        Returns:
            統計情報辞書
        """
        try:
            screen_list = self.get_screen_list()
            
            stats = {
                'total_screens': len(screen_list),
                'screens_by_category': {},
                'total_components': 0,
                'responsive_screens': 0,
                'screens_with_issues': 0,
                'requirement_coverage': {}
            }
            
            for screen_id in screen_list:
                screen_info = self.get_screen_info(screen_id)
                if screen_info:
                    # カテゴリ別集計（画面IDのプレフィックスから推定）
                    if screen_id.startswith('SCR-'):
                        category = screen_id.split('-')[1] if len(screen_id.split('-')) > 1 else 'other'
                        if category not in stats['screens_by_category']:
                            stats['screens_by_category'][category] = 0
                        stats['screens_by_category'][category] += 1
                    
                    # コンポーネント数集計
                    components = screen_info.get('components', [])
                    stats['total_components'] += len(components)
                    
                    # レスポンシブ対応集計
                    responsive = screen_info.get('responsive', {})
                    if responsive:
                        stats['responsive_screens'] += 1
                    
                    # 要求仕様ID別集計
                    req_id = screen_info.get('requirement_id', '')
                    if req_id:
                        if req_id not in stats['requirement_coverage']:
                            stats['requirement_coverage'][req_id] = 0
                        stats['requirement_coverage'][req_id] += 1
                    
                    # 検証エラーチェック
                    if not self.validate_screen(screen_id, verbose=False):
                        stats['screens_with_issues'] += 1
            
            return stats
            
        except Exception as e:
            self.logger.error(f"統計情報取得エラー: {e}")
            return {}
    
    def check_component_consistency(self, verbose: bool = False) -> bool:
        """
        コンポーネントの整合性をチェック
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            チェック成功フラグ
        """
        self.logger.info("コンポーネント整合性チェックを開始")
        
        try:
            screen_list = self.get_screen_list()
            all_components = set()
            component_usage = {}
            
            # 全画面からコンポーネントを収集
            for screen_id in screen_list:
                screen_info = self.get_screen_info(screen_id)
                if screen_info:
                    components = screen_info.get('components', [])
                    for component in components:
                        component_name = component.get('name', '')
                        if component_name:
                            all_components.add(component_name)
                            if component_name not in component_usage:
                                component_usage[component_name] = []
                            component_usage[component_name].append(screen_id)
            
            # 共通コンポーネントの特定
            common_components = {name: screens for name, screens in component_usage.items() if len(screens) > 1}
            
            if verbose:
                print(f"\n📊 コンポーネント整合性チェック結果:")
                print(f"  - 総コンポーネント数: {len(all_components)}")
                print(f"  - 共通コンポーネント数: {len(common_components)}")
                
                if common_components:
                    print(f"\n🔄 共通コンポーネント:")
                    for component_name, screens in common_components.items():
                        print(f"  - {component_name}: {', '.join(screens)}")
            
            self.logger.info("コンポーネント整合性チェックが完了しました")
            return True
            
        except Exception as e:
            self.logger.error(f"コンポーネント整合性チェックエラー: {e}")
            return False
