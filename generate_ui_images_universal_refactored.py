#!/usr/bin/env python3
"""
汎用UI画像生成ツール（設定ファイル対応版）
統合設定マネージャーを使用した設定駆動型UI画像生成
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import hashlib

# 設定マネージャーのインポート
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
from config_manager import ConfigManager

try:
    from PIL import Image, ImageDraw, ImageFont
    import yaml
except ImportError as e:
    print(f"必要なライブラリがインストールされていません: {e}")
    print("以下のコマンドでインストールしてください:")
    print("pip install Pillow PyYAML")
    sys.exit(1)

class UniversalUIGenerator:
    """汎用UI画像生成クラス（設定ファイル対応）"""
    
    def __init__(self, project_name: str = "skill-report-web", tool_name: str = "ui-generator"):
        """
        初期化
        
        Args:
            project_name: プロジェクト名
            tool_name: ツール名
        """
        self.config_manager = ConfigManager(project_name=project_name, tool_name=tool_name)
        self.config = self.config_manager.merge_configs()
        
        # 設定検証
        validation = self.config_manager.validate_config()
        if validation["errors"]:
            print("設定エラー:")
            for error in validation["errors"]:
                print(f"  - {error}")
            sys.exit(1)
            
        if validation["warnings"]:
            print("設定警告:")
            for warning in validation["warnings"]:
                print(f"  - {warning}")
        
        # 基本設定の取得
        self.image_config = self.config_manager.get("image_generation", {})
        self.color_palette = self.config_manager.get_color_palette()
        self.font_config = self.config_manager.get("fonts", {})
        self.layout_config = self.config_manager.get("layout", {})
        self.component_config = self.config_manager.get("components", {})
        self.icon_config = self.config_manager.get("icons", {})
        self.output_config = self.config_manager.get_output_config()
        
        # フォント初期化
        self.fonts = self._initialize_fonts()
        
        print(f"UI生成ツール初期化完了")
        print(f"プロジェクト: {self.config_manager.get('project_info.name', 'Unknown')}")
        print(f"システム: {self.config_manager.get('system.name', 'Unknown')}")
        
    def _initialize_fonts(self) -> Dict[str, ImageFont.FreeTypeFont]:
        """フォント初期化"""
        fonts = {}
        font_sizes = self.font_config.get("sizes", {})
        
        # 日本語フォント候補から利用可能なものを探す
        japanese_font_path = None
        for font_path in self.font_config.get("japanese_candidates", []):
            if os.path.exists(font_path):
                japanese_font_path = font_path
                break
                
        # フォントサイズ別にフォントオブジェクトを作成
        for size_name, size in font_sizes.items():
            try:
                if japanese_font_path:
                    fonts[size_name] = ImageFont.truetype(japanese_font_path, size)
                else:
                    fonts[size_name] = ImageFont.load_default()
                    print(f"警告: 日本語フォントが見つからないため、デフォルトフォントを使用します")
            except Exception as e:
                print(f"フォント読み込みエラー ({size_name}): {e}")
                fonts[size_name] = ImageFont.load_default()
                
        return fonts
        
    def _get_color(self, color_key: str, default: str = "#000000") -> str:
        """カラーパレットから色を取得"""
        return self.color_palette.get(color_key, default)
        
    def _get_icon(self, icon_key: str, default: str = "📄") -> str:
        """アイコンマッピングからアイコンを取得"""
        return self.icon_config.get("mapping", {}).get(icon_key, default)
        
    def _draw_header(self, draw: ImageDraw.Draw, width: int) -> int:
        """ヘッダー描画"""
        header_config = self.component_config.get("header", {})
        header_height = header_config.get("height", 60)
        header_bg = header_config.get("background", self._get_color("background"))
        
        # ヘッダー背景
        draw.rectangle([0, 0, width, header_height], fill=header_bg)
        
        # ヘッダー下線
        if header_config.get("border_bottom", True):
            draw.line([0, header_height-1, width, header_height-1], 
                     fill=self._get_color("border"), width=1)
        
        # ロゴ・システム名
        branding = self.config_manager.get("branding", {})
        system_name = branding.get("system_name", "システム")
        
        # ロゴテキスト（左側）
        if header_config.get("logo_position") == "left":
            logo_text = branding.get("logo_text", "LOGO")
            draw.text((20, 20), logo_text, fill=self._get_color("primary"), 
                     font=self.fonts.get("header", self.fonts["text"]))
            
            # システム名
            draw.text((80, 25), system_name, fill=self._get_color("text"), 
                     font=self.fonts.get("text"))
        
        # ユーザーメニュー（右側）
        if header_config.get("user_menu_position") == "right":
            user_icon = self._get_icon("user")
            settings_icon = self._get_icon("settings")
            logout_icon = self._get_icon("logout")
            
            draw.text((width-120, 20), f"{user_icon} ユーザー", 
                     fill=self._get_color("text"), font=self.fonts.get("small"))
            draw.text((width-80, 20), settings_icon, 
                     fill=self._get_color("text_light"), font=self.fonts.get("small"))
            draw.text((width-50, 20), logout_icon, 
                     fill=self._get_color("text_light"), font=self.fonts.get("small"))
        
        return header_height
        
    def _draw_sidebar(self, draw: ImageDraw.Draw, height: int, header_height: int = 0) -> int:
        """サイドバー描画"""
        sidebar_config = self.component_config.get("sidebar", {})
        sidebar_width = sidebar_config.get("width", 250)
        sidebar_bg = sidebar_config.get("background", self._get_color("background_light"))
        
        # サイドバー背景
        draw.rectangle([0, header_height, sidebar_width, height], fill=sidebar_bg)
        
        # サイドバー右線
        if sidebar_config.get("border_right", True):
            draw.line([sidebar_width-1, header_height, sidebar_width-1, height], 
                     fill=self._get_color("border"), width=1)
        
        # ナビゲーション項目
        nav_items = self.config_manager.get_navigation_items()
        y_offset = header_height + 20
        
        for item in nav_items:
            icon = self._get_icon(item.get("icon", ""), "📄")
            name = item.get("name", "")
            
            # メニュー項目背景（ホバー効果風）
            if item.get("key") == "プロフィール":  # アクティブ項目の例
                draw.rectangle([10, y_offset-5, sidebar_width-10, y_offset+25], 
                             fill=self._get_color("primary", "#e3f2fd"))
            
            # アイコンとテキスト
            draw.text((20, y_offset), f"{icon} {name}", 
                     fill=self._get_color("text"), font=self.fonts.get("text"))
            
            y_offset += 35
            
        return sidebar_width
        
    def _draw_breadcrumb(self, draw: ImageDraw.Draw, x: int, y: int, width: int, 
                        breadcrumb_items: List[str]) -> int:
        """パンくずリスト描画"""
        if not breadcrumb_items:
            return 0
            
        breadcrumb_height = 30
        breadcrumb_text = " > ".join(breadcrumb_items)
        
        draw.text((x + 20, y + 8), breadcrumb_text, 
                 fill=self._get_color("text_light"), font=self.fonts.get("small"))
        
        # 下線
        draw.line([x, y + breadcrumb_height, x + width, y + breadcrumb_height], 
                 fill=self._get_color("border"), width=1)
        
        return breadcrumb_height
        
    def _draw_form_field(self, draw: ImageDraw.Draw, x: int, y: int, width: int, 
                        field_config: Dict[str, Any]) -> int:
        """フォーム項目描画"""
        field_height = 60
        label = field_config.get("label", "")
        field_type = field_config.get("type", "text")
        required = field_config.get("required", False)
        readonly = field_config.get("readonly", False)
        
        # ラベル
        label_text = f"{label}{'*' if required else ''}"
        draw.text((x, y), label_text, fill=self._get_color("text"), 
                 font=self.fonts.get("text"))
        
        # 入力フィールド
        input_config = self.component_config.get("input", {})
        field_y = y + 20
        field_bg = self._get_color("background") if not readonly else self._get_color("background_light")
        border_color = self._get_color("border")
        
        # フィールド背景
        draw.rectangle([x, field_y, x + width, field_y + 30], 
                     fill=field_bg, outline=border_color)
        
        # プレースホルダーテキスト
        if field_type == "select":
            placeholder = "選択してください"
            draw.text((x + width - 30, field_y + 8), "▼", 
                     fill=self._get_color("text_light"), font=self.fonts.get("small"))
        elif field_type == "email":
            placeholder = "example@company.com"
        else:
            placeholder = "入力してください"
            
        if not readonly:
            draw.text((x + 10, field_y + 8), placeholder, 
                     fill=self._get_color("text_light"), font=self.fonts.get("small"))
        else:
            draw.text((x + 10, field_y + 8), "（読み取り専用）", 
                     fill=self._get_color("text_light"), font=self.fonts.get("small"))
        
        return field_height
        
    def _draw_button(self, draw: ImageDraw.Draw, x: int, y: int, text: str, 
                    button_type: str = "primary") -> Tuple[int, int]:
        """ボタン描画"""
        button_config = self.component_config.get("button", {})
        padding = button_config.get("padding", "8px 16px")
        
        # パディングをパース（簡易版）
        if "px" in padding:
            padding_parts = padding.replace("px", "").split()
            if len(padding_parts) == 2:
                v_padding, h_padding = int(padding_parts[0]), int(padding_parts[1])
            else:
                v_padding = h_padding = int(padding_parts[0])
        else:
            v_padding = h_padding = 8
            
        # テキストサイズ計算
        text_bbox = draw.textbbox((0, 0), text, font=self.fonts.get("text"))
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        button_width = text_width + h_padding * 2
        button_height = text_height + v_padding * 2
        
        # ボタン色
        if button_type == "primary":
            bg_color = self._get_color("primary")
            text_color = self._get_color("background")
        elif button_type == "secondary":
            bg_color = self._get_color("secondary")
            text_color = self._get_color("text")
        else:
            bg_color = self._get_color("background")
            text_color = self._get_color("text")
        
        # ボタン描画
        draw.rectangle([x, y, x + button_width, y + button_height], 
                     fill=bg_color, outline=self._get_color("border"))
        
        # テキスト描画
        text_x = x + h_padding
        text_y = y + v_padding
        draw.text((text_x, text_y), text, fill=text_color, font=self.fonts.get("text"))
        
        return button_width, button_height
        
    def generate_screen_image(self, screen_type: str, spec_file_path: Optional[str] = None) -> str:
        """画面画像生成"""
        print(f"\n=== {screen_type}画面の生成開始 ===")
        
        # 画面設定取得
        screen_config = self.config_manager.get_screen_config(screen_type)
        if not screen_config:
            print(f"警告: {screen_type}の画面設定が見つかりません")
            screen_config = {}
        
        # 画像サイズ
        image_size = self.image_config.get("default_size", {"width": 1792, "height": 1024})
        width, height = image_size["width"], image_size["height"]
        
        # 画像作成
        image = Image.new('RGB', (width, height), self._get_color("background"))
        draw = ImageDraw.Draw(image)
        
        # レイアウト設定
        layout_type = screen_config.get("layout_type", "dashboard")
        
        current_y = 0
        sidebar_width = 0
        
        # ヘッダー描画
        if screen_config.get("show_header", layout_type != "login"):
            header_height = self._draw_header(draw, width)
            current_y += header_height
        
        # サイドバー描画
        if screen_config.get("show_sidebar", layout_type == "dashboard"):
            sidebar_width = self._draw_sidebar(draw, height, current_y)
        
        # メインコンテンツエリア
        content_x = sidebar_width + 20
        content_width = width - sidebar_width - 40
        content_y = current_y + 20
        
        # 画面タイプ別コンテンツ
        if layout_type == "login":
            self._draw_login_content(draw, width, height, screen_config)
        elif layout_type == "form":
            self._draw_form_content(draw, content_x, content_y, content_width, screen_config)
        elif layout_type == "detail":
            self._draw_detail_content(draw, content_x, content_y, content_width, screen_config)
        else:  # dashboard
            self._draw_dashboard_content(draw, content_x, content_y, content_width, screen_config)
        
        # 画像保存
        output_path = self._save_image(image, screen_type)
        print(f"画像生成完了: {output_path}")
        
        return output_path
        
    def _draw_login_content(self, draw: ImageDraw.Draw, width: int, height: int, 
                           screen_config: Dict[str, Any]):
        """ログイン画面コンテンツ"""
        # 中央配置計算
        form_width = 400
        form_height = 300
        form_x = (width - form_width) // 2
        form_y = (height - form_height) // 2
        
        # ログインフォーム背景
        card_config = self.component_config.get("card", {})
        draw.rectangle([form_x, form_y, form_x + form_width, form_y + form_height], 
                     fill=self._get_color("background"), outline=self._get_color("border"))
        
        # タイトル
        title = screen_config.get("title", "ログイン")
        draw.text((form_x + 20, form_y + 20), title, 
                 fill=self._get_color("text"), font=self.fonts.get("title"))
        
        # フォーム項目
        field_y = form_y + 60
        
        # ユーザーID
        draw.text((form_x + 20, field_y), "ユーザーID", 
                 fill=self._get_color("text"), font=self.fonts.get("text"))
        draw.rectangle([form_x + 20, field_y + 20, form_x + form_width - 20, field_y + 50], 
                     fill=self._get_color("background"), outline=self._get_color("border"))
        
        # パスワード
        field_y += 70
        draw.text((form_x + 20, field_y), "パスワード", 
                 fill=self._get_color("text"), font=self.fonts.get("text"))
        draw.rectangle([form_x + 20, field_y + 20, form_x + form_width - 20, field_y + 50], 
                     fill=self._get_color("background"), outline=self._get_color("border"))
        
        # ログインボタン
        button_y = field_y + 80
        self._draw_button(draw, form_x + 20, button_y, "ログイン", "primary")
        
    def _draw_form_content(self, draw: ImageDraw.Draw, x: int, y: int, width: int, 
                          screen_config: Dict[str, Any]):
        """フォーム画面コンテンツ"""
        # パンくずリスト
        breadcrumb_items = ["ホーム", screen_config.get("title", "フォーム")]
        if screen_config.get("breadcrumb", True):
            breadcrumb_height = self._draw_breadcrumb(draw, x, y, width, breadcrumb_items)
            y += breadcrumb_height + 20
        
        # タイトル
        title = screen_config.get("title", "フォーム")
        draw.text((x, y), title, fill=self._get_color("text"), font=self.fonts.get("title"))
        y += 40
        
        # フォーム項目（プロジェクト設定から取得）
        form_type = screen_config.get("screen_id", "").lower().replace("scr_", "").replace("_", "")
        if "pro" in form_type:  # プロフィール画面
            form_fields = self.config_manager.get_form_fields("profile")
            
            for section_name, fields in form_fields.items():
                # セクションタイトル
                section_title = section_name.replace("_", " ").title()
                draw.text((x, y), section_title, 
                         fill=self._get_color("text"), font=self.fonts.get("header"))
                y += 30
                
                # フィールド描画
                for field in fields:
                    field_height = self._draw_form_field(draw, x, y, width // 2, field)
                    y += field_height + 10
                
                y += 20
        
        # アクションボタン
        if screen_config.get("show_buttons", True):
            button_y = y + 20
            save_width, _ = self._draw_button(draw, x, button_y, "保存", "primary")
            self._draw_button(draw, x + save_width + 10, button_y, "キャンセル", "secondary")
        
    def _draw_detail_content(self, draw: ImageDraw.Draw, x: int, y: int, width: int, 
                            screen_config: Dict[str, Any]):
        """詳細画面コンテンツ"""
        # パンくずリスト
        breadcrumb_items = ["ホーム", screen_config.get("title", "詳細")]
        if screen_config.get("breadcrumb", True):
            breadcrumb_height = self._draw_breadcrumb(draw, x, y, width, breadcrumb_items)
            y += breadcrumb_height + 20
        
        # タイトル
        title = screen_config.get("title", "詳細")
        draw.text((x, y), title, fill=self._get_color("text"), font=self.fonts.get("title"))
        y += 40
        
        # 画面タイプ別コンテンツ
        if "skill" in screen_config.get("screen_id", "").lower():
            # スキル画面
            if screen_config.get("show_radar_chart", True):
                # レーダーチャートプレースホルダー
                chart_size = 200
                chart_x = x + (width - chart_size) // 2
                draw.ellipse([chart_x, y, chart_x + chart_size, y + chart_size], 
                           outline=self._get_color("primary"), width=2)
                draw.text((chart_x + chart_size//2 - 30, y + chart_size//2), "スキルマップ", 
                         fill=self._get_color("text"), font=self.fonts.get("text"))
                y += chart_size + 30
            
            # スキルカテゴリ
            skill_categories = self.config_manager.get("skills.categories", [])
            for category in skill_categories:
                icon = category.get("icon", "📄")
                name = category.get("name", "")
                draw.text((x, y), f"{icon} {name}", 
                         fill=self._get_color("text"), font=self.fonts.get("text"))
                y += 30
                
        elif "career" in screen_config.get("screen_id", "").lower():
            # キャリア画面
            if screen_config.get("show_timeline", True):
                # タイムラインプレースホルダー
                draw.text((x, y), "📈 キャリア目標進捗", 
                         fill=self._get_color("text"), font=self.fonts.get("header"))
                y += 40
                
                # 進捗バー例
                for i, goal in enumerate(["短期目標", "中期目標", "長期目標"]):
                    draw.text((x, y), f"• {goal}", 
                             fill=self._get_color("text"), font=self.fonts.get("text"))
                    
                    # 進捗バー
                    progress = (3 - i) * 30  # 例: 90%, 60%, 30%
                    bar_width = 200
                    bar_height = 10
                    bar_x = x + 150
                    
                    # 背景
                    draw.rectangle([bar_x, y + 5, bar_x + bar_width, y + 5 + bar_height], 
                                 fill=self._get_color("background_light"), outline=self._get_color("border"))
                    
                    # 進捗
                    progress_width = int(bar_width * progress / 100)
                    draw.rectangle([bar_x, y + 5, bar_x + progress_width, y + 5 + bar_height], 
                                 fill=self._get_color("success"))
                    
                    # パーセンテージ
                    draw.text((bar_x + bar_width + 10, y), f"{progress}%", 
                             fill=self._get_color("text_light"), font=self.fonts.get("small"))
                    
                    y += 35
        
    def _draw_dashboard_content(self, draw: ImageDraw.Draw, x: int, y: int, width: int, 
                               screen_config: Dict[str, Any]):
        """ダッシュボード画面コンテンツ"""
        # ウェルカムメッセージ
        if screen_config.get("show_welcome_message", True):
            welcome_text = "ようこそ、年間スキル報告書システムへ"
            draw.text((x, y), welcome_text, 
                     fill=self._get_color("text"), font=self.fonts.get("title"))
            y += 50
        
        # クイックアクション
        if screen_config.get("show_quick_actions", True):
            draw.text((x, y), "クイックアクション", 
                     fill=self._get_color("text"), font=self.fonts.get("header"))
            y += 30
            
            # アクションカード
            card_width = (width - 40) // 3
            card_height = 100
            
            actions = [
                {"icon": "user", "title": "プロフィール更新", "desc": "個人情報を更新"},
                {"icon": "skills", "title": "スキル登録", "desc": "新しいスキルを追加"},
                {"icon": "reports", "title": "レポート生成", "desc": "最新のレポートを作成"}
            ]
            
            for i, action in enumerate(actions):
                card_x = x + i * (card_width + 20)
                
                # カード背景
                draw.rectangle([card_x, y, card_x + card_width, y + card_height], 
                             fill=self._get_color("background"), outline=self._get_color("border"))
                
                # アイコン
                icon = self._get_icon(action["icon"])
                draw.text((card_x + 20, y + 20), icon, 
                         fill=self._get_color("primary"), font=self.fonts.get("title"))
                
                # タイトル
                draw.text((card_x + 60, y + 20), action["title"], 
                         fill=self._get_color("text"), font=self.fonts.get("text"))
                
                # 説明
                draw.text((card_x + 20, y + 50), action["desc"], 
                         fill=self._get_color("text_light"), font=self.fonts.get("small"))
        
    def _save_image(self, image: Image.Image, screen_type: str) -> str:
        """画像保存"""
        # タイムスタンプ生成
        timestamp = datetime.now().strftime(self.config_manager.get("naming_conventions.timestamp_format", "%Y%m%d_%H%M%S"))
        
        # ファイル名生成
        filename_pattern = self.output_config.get("filename_pattern", "{screen_type}_ui_mockup_{timestamp}.png")
        filename = filename_pattern.format(screen_type=screen_type, timestamp=timestamp)
        
        # 出力ディレクトリ
        output_dir = self.output_config.get("base_directory", "output")
        os.makedirs(output_dir, exist_ok=True)
        
        # 画像保存
        output_path = os.path.join(output_dir, filename)
        image.save(output_path, format=self.image_config.get("output_format", "PNG"))
        
        # メタデータ保存
        if self.output_config.get("metadata_enabled", True):
            self._save_metadata(output_path, screen_type, timestamp)
        
        return output_path
        
    def _save_metadata(self, image_path: str, screen_type: str, timestamp: str):
        """メタデータ保存"""
        metadata = {
            "generation_info": {
                "tool_name": self.config_manager.get("tool_info.name"),
                "tool_version": self.config_manager.get("tool_info.version"),
                "generated_at": timestamp,
                "screen_type": screen_type
            },
            "project_info": {
                "name": self.config_manager.get("project_info.name"),
                "version": self.config_manager.get("project_info.version")
            },
            "config_hash": hashlib.md5(str(self.config).encode()).hexdigest()[:8],
            "image_config": self.image_config,
            "screen_config": self.config_manager.get_screen_config(screen_type)
        }
        
        metadata_path = image_path.replace(".png", "_metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

def main():
    """メイン実行"""
    import argparse
    
    parser = argparse.ArgumentParser(description="汎用UI画像生成ツール")
    parser.add_argument("--screen-type", required=True, 
                       choices=["login", "home", "profile", "skill", "career"],
                       help="生成する画面タイプ")
    parser.add_argument("--project", default="skill-report-web", 
                       help="プロジェクト名")
    parser.add_argument("--tool", default="ui-generator", 
                       help="ツール名")
    parser.add_argument("--spec-file", 
                       help="画面仕様書ファイルパス")
    
    args = parser.parse_args()
    
    try:
        # UI生成ツール初期化
        generator = UniversalUIGenerator(
            project_name=args.project,
            tool_name=args.tool
        )
        
        # 画面画像生成
        output_path = generator.generate_screen_image(
            screen_type=args.screen_type,
            spec_file_path=args.spec_file
        )
        
        print(f"\n✅ 画像生成完了!")
        print(f"出力ファイル: {output_path}")
        
        # メタデータファイルの確認
        metadata_path = output_path.replace(".png", "_metadata.json")
        if os.path.exists(metadata_path):
            print(f"メタデータ: {metadata_path}")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
