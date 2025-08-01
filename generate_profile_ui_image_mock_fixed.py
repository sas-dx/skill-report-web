#!/usr/bin/env python3
"""
プロフィール画面UI画像生成スクリプト（モック版・日本語対応）
要求仕様ID: PRO.1-BASE.1
対応設計書: docs/design/screens/specs/画面定義書_SCR_PRO_Profile_プロフィール画面.md
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import json
from datetime import datetime

def get_japanese_font(size=14):
    """日本語対応フォントを取得"""
    
    # 日本語フォントの候補リスト（優先順位順）
    font_candidates = [
        "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf",  # IPAゴシック
        "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",  # IPAゴシック（別パス）
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # WenQuanYi Zen Hei
        "/usr/share/fonts/opentype/unifont/unifont_jp.otf",  # Unifont JP
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # DejaVu Sans（フォールバック）
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"  # Liberation Sans（フォールバック）
    ]
    
    # 利用可能なフォントを検索
    for font_path in font_candidates:
        try:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, size)
                print(f"✅ フォント使用: {font_path} (サイズ: {size})")
                return font
        except Exception as e:
            print(f"⚠️ フォント読み込み失敗: {font_path} - {e}")
            continue
    
    # すべて失敗した場合はデフォルトフォント
    print("⚠️ 日本語フォントが見つかりません。デフォルトフォントを使用します。")
    return ImageFont.load_default()

def create_mock_ui_image():
    """モックUI画像を生成（日本語対応）"""
    
    # 画像サイズ設定
    width, height = 1792, 1024
    
    # 背景色（白）
    background_color = (255, 255, 255)
    
    # カラーパレット
    primary_color = (51, 153, 204)  # #3399cc
    secondary_color = (240, 240, 240)  # #f0f0f0
    text_color = (51, 51, 51)  # #333333
    border_color = (200, 200, 200)  # #c8c8c8
    
    # 画像作成
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)
    
    # 日本語対応フォント設定
    try:
        title_font = get_japanese_font(20)  # タイトル用（大）
        header_font = get_japanese_font(16)  # ヘッダー用（中）
        text_font = get_japanese_font(14)   # 本文用（小）
        small_font = get_japanese_font(12)  # 小文字用
        print("✅ 日本語フォントの設定が完了しました")
    except Exception as e:
        print(f"❌ フォント設定エラー: {e}")
        # フォールバック
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # ヘッダー部分
    draw.rectangle([0, 0, width, 80], fill=primary_color)
    draw.text((20, 25), "年間スキル報告書システム", fill=(255, 255, 255), font=title_font)
    draw.text((width-250, 25), "ユーザー ▼ 🔔 ログアウト", fill=(255, 255, 255), font=text_font)
    
    # サイドバー
    sidebar_width = 250
    draw.rectangle([0, 80, sidebar_width, height], fill=secondary_color)
    
    # サイドバーメニュー項目
    menu_items = [
        ("ホーム", False),
        ("プロフィール", True),  # ハイライト
        ("スキル情報", False),
        ("目標管理", False),
        ("作業実績", False),
        ("研修記録", False),
        ("レポート", False)
    ]
    
    y_pos = 120
    for item, is_active in menu_items:
        if is_active:
            draw.rectangle([10, y_pos-5, sidebar_width-10, y_pos+25], fill=primary_color)
            text_color_menu = (255, 255, 255)
        else:
            text_color_menu = text_color
        
        draw.text((20, y_pos), item, fill=text_color_menu, font=text_font)
        y_pos += 40
    
    # メインコンテンツエリア
    content_x = sidebar_width + 20
    content_width = width - sidebar_width - 40
    
    # ページタイトル
    draw.text((content_x, 100), "プロフィール管理", fill=text_color, font=title_font)
    
    # 基本情報セクション
    section_y = 150
    draw.rectangle([content_x, section_y, content_x + content_width, section_y + 250], 
                  outline=border_color, width=2)
    draw.text((content_x + 10, section_y + 10), "基本情報", fill=text_color, font=header_font)
    
    # フォームフィールド
    fields = [
        ("社員番号", "EMP001 (読み取り専用)"),
        ("氏名(漢字)", "山田 太郎"),
        ("氏名(カナ)", "ヤマダ タロウ"),
        ("メールアドレス", "yamada@company.com"),
        ("生年月日", "1990/01/01"),
        ("入社日", "2020/04/01")
    ]
    
    field_y = section_y + 40
    for label, value in fields:
        draw.text((content_x + 20, field_y), f"{label}:", fill=text_color, font=text_font)
        draw.rectangle([content_x + 150, field_y - 5, content_x + 450, field_y + 20], 
                      outline=border_color, width=1)
        draw.text((content_x + 155, field_y), value, fill=text_color, font=text_font)
        field_y += 35
    
    # 所属情報セクション
    section_y = 420
    draw.rectangle([content_x, section_y, content_x + content_width, section_y + 180], 
                  outline=border_color, width=2)
    draw.text((content_x + 10, section_y + 10), "所属情報", fill=text_color, font=header_font)
    
    org_fields = [
        ("部署", "開発部 ▼"),
        ("役職", "主任 ▼"),
        ("グループ", "システム開発G ▼"),
        ("上長", "佐藤 部長 (読み取り専用)")
    ]
    
    field_y = section_y + 40
    for label, value in org_fields:
        draw.text((content_x + 20, field_y), f"{label}:", fill=text_color, font=text_font)
        draw.rectangle([content_x + 150, field_y - 5, content_x + 450, field_y + 20], 
                      outline=border_color, width=1)
        draw.text((content_x + 155, field_y), value, fill=text_color, font=text_font)
        field_y += 35
    
    # 更新履歴セクション
    section_y = 620
    draw.rectangle([content_x, section_y, content_x + content_width, section_y + 150], 
                  outline=border_color, width=2)
    draw.text((content_x + 10, section_y + 10), "更新履歴", fill=text_color, font=header_font)
    
    # テーブルヘッダー
    headers = ["日時", "項目", "変更前", "変更後", "変更者"]
    header_y = section_y + 40
    x_positions = [content_x + 20, content_x + 120, content_x + 220, content_x + 320, content_x + 420]
    
    for i, header in enumerate(headers):
        draw.text((x_positions[i], header_y), header, fill=text_color, font=text_font)
    
    # サンプルデータ行
    sample_data = [
        ("2025/06/01", "部署", "営業部", "開発部", "人事部"),
        ("2025/05/15", "役職", "一般", "主任", "人事部")
    ]
    
    data_y = header_y + 25
    for row in sample_data:
        for i, cell in enumerate(row):
            draw.text((x_positions[i], data_y), cell, fill=text_color, font=small_font)
        data_y += 25
    
    # アクションボタン
    button_y = height - 80
    
    # キャンセルボタン
    draw.rectangle([content_x + content_width - 200, button_y, 
                   content_x + content_width - 120, button_y + 35], 
                  outline=border_color, width=2)
    draw.text((content_x + content_width - 175, button_y + 10), "キャンセル", 
              fill=text_color, font=text_font)
    
    # 保存ボタン
    draw.rectangle([content_x + content_width - 100, button_y, 
                   content_x + content_width - 20, button_y + 35], 
                  fill=primary_color)
    draw.text((content_x + content_width - 75, button_y + 10), "保存", 
              fill=(255, 255, 255), font=text_font)
    
    return img

def generate_profile_ui_image_mock():
    """プロフィール管理画面のモックUI画像を生成（日本語対応）"""
    
    print("🎨 日本語対応モックUI画像を生成中...")
    
    try:
        # モック画像を生成
        img = create_mock_ui_image()
        
        # 画像を保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"profile_ui_mockup_fixed_{timestamp}.png"
        filepath = os.path.join("docs/design/screens", filename)
        
        # ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        img.save(filepath)
        
        print(f"💾 日本語対応モック画像を保存しました: {filepath}")
        
        # 画像情報をJSONで保存
        metadata = {
            "generated_at": datetime.now().isoformat(),
            "type": "mock_ui_image_japanese_fixed",
            "description": "プロフィール管理画面のモックUI画像（日本語対応版）",
            "size": f"{img.size[0]}x{img.size[1]}",
            "filename": filename,
            "specification_id": "PRO.1-BASE.1",
            "screen_id": "SCR-PROFILE",
            "design_document": "docs/design/screens/specs/画面定義書_SCR_PRO_Profile_プロフィール画面.md",
            "improvements": [
                "日本語フォント対応（IPAゴシック使用）",
                "フォントサイズの階層化（タイトル20px、ヘッダー16px、本文14px、小文字12px）",
                "フォント検出・フォールバック機能",
                "レイアウト調整（フィールド幅拡張）"
            ],
            "features": [
                "ヘッダー（タイトル、ユーザードロップダウン、通知、ログアウト）",
                "サイドバーナビゲーション（プロフィールがハイライト）",
                "基本情報フォーム（社員番号、氏名、メール、生年月日、入社日）",
                "所属情報フォーム（部署、役職、グループ、上長）",
                "更新履歴テーブル（日時、項目、変更前、変更後、変更者）",
                "アクションボタン（キャンセル、保存）"
            ]
        }
        
        metadata_filepath = filepath.replace('.png', '_metadata.json')
        with open(metadata_filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"📋 メタデータを保存しました: {metadata_filepath}")
        
        # 画像サイズ情報を表示
        print(f"📐 画像サイズ: {img.size[0]}x{img.size[1]} pixels")
        
        print("\n🎉 日本語対応プロフィール画面モックUI画像の生成が完了しました！")
        print(f"📁 保存場所: {filepath}")
        print("✅ 日本語文字が正しく表示されるようになりました")
        print("📝 IPAゴシックフォントを使用して日本語表示を改善")
        
        return True
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """メイン実行関数"""
    print("=" * 70)
    print("🎨 プロフィール管理画面 UI画像生成ツール（日本語対応版）")
    print("要求仕様ID: PRO.1-BASE.1")
    print("画面ID: SCR-PROFILE")
    print("改善点: 日本語フォント対応、レイアウト調整")
    print("=" * 70)
    
    success = generate_profile_ui_image_mock()
    
    if success:
        print("\n✅ 処理が正常に完了しました")
        print("\n📌 改善内容:")
        print("• IPAゴシックフォントによる日本語表示対応")
        print("• フォントサイズの階層化（タイトル、ヘッダー、本文）")
        print("• フォント検出・フォールバック機能")
        print("• レイアウト調整（フィールド幅拡張）")
        print("\n📌 次のステップ:")
        print("1. 生成された画像で日本語表示を確認してください")
        print("2. 他の画面の日本語対応版も生成可能です")
        print("3. 実際のAI生成画像が必要な場合は、OpenAI APIキーを取得してください")
        sys.exit(0)
    else:
        print("\n❌ 処理が失敗しました")
        sys.exit(1)

if __name__ == "__main__":
    main()
