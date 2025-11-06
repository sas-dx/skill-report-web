#!/usr/bin/env python3
"""
汎用画面UI画像生成スクリプト（日本語対応）
複数の画面設計書に対応した画像生成ツール
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
                return font
        except Exception as e:
            continue
    
    # すべて失敗した場合はデフォルトフォント
    return ImageFont.load_default()

def create_base_layout(width=1792, height=1024, title="画面タイトル", active_menu="ホーム"):
    """基本レイアウトを作成"""
    
    # カラーパレット
    primary_color = (51, 153, 204)  # #3399cc
    secondary_color = (240, 240, 240)  # #f0f0f0
    text_color = (51, 51, 51)  # #333333
    border_color = (200, 200, 200)  # #c8c8c8
    background_color = (255, 255, 255)
    
    # 画像作成
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)
    
    # フォント設定
    title_font = get_japanese_font(20)
    header_font = get_japanese_font(16)
    text_font = get_japanese_font(14)
    small_font = get_japanese_font(12)
    
    # ヘッダー部分
    draw.rectangle([0, 0, width, 80], fill=primary_color)
    draw.text((20, 25), "年間スキル報告書システム", fill=(255, 255, 255), font=title_font)
    draw.text((width-250, 25), "ユーザー ▼ 🔔 ログアウト", fill=(255, 255, 255), font=text_font)
    
    # サイドバー
    sidebar_width = 250
    draw.rectangle([0, 80, sidebar_width, height], fill=secondary_color)
    
    # サイドバーメニュー項目
    menu_items = [
        ("ホーム", "ホーム"),
        ("プロフィール", "プロフィール"),
        ("スキル情報", "スキル"),
        ("目標管理", "キャリア"),
        ("作業実績", "作業実績"),
        ("研修記録", "研修"),
        ("レポート", "レポート")
    ]
    
    y_pos = 120
    for item, menu_key in menu_items:
        is_active = (menu_key in active_menu)
        if is_active:
            draw.rectangle([10, y_pos-5, sidebar_width-10, y_pos+25], fill=primary_color)
            text_color_menu = (255, 255, 255)
        else:
            text_color_menu = text_color
        
        draw.text((20, y_pos), item, fill=text_color_menu, font=text_font)
        y_pos += 40
    
    # ページタイトル
    content_x = sidebar_width + 20
    draw.text((content_x, 100), title, fill=text_color, font=title_font)
    
    return img, draw, {
        'content_x': content_x,
        'content_width': width - sidebar_width - 40,
        'sidebar_width': sidebar_width,
        'fonts': {
            'title': title_font,
            'header': header_font,
            'text': text_font,
            'small': small_font
        },
        'colors': {
            'primary': primary_color,
            'secondary': secondary_color,
            'text': text_color,
            'border': border_color,
            'background': background_color
        }
    }

def create_login_screen():
    """ログイン画面を生成"""
    img, draw, layout = create_base_layout(title="ログイン", active_menu="")
    
    # ログイン画面は特別レイアウト
    img = Image.new('RGB', (1792, 1024), layout['colors']['background'])
    draw = ImageDraw.Draw(img)
    
    # 中央にログインフォーム
    center_x, center_y = 896, 512
    form_width, form_height = 400, 300
    
    # ログインフォーム背景
    draw.rectangle([center_x - form_width//2, center_y - form_height//2,
                   center_x + form_width//2, center_y + form_height//2],
                  outline=layout['colors']['border'], width=2)
    
    # タイトル
    draw.text((center_x - 100, center_y - 120), "年間スキル報告書システム", 
              fill=layout['colors']['text'], font=layout['fonts']['title'])
    draw.text((center_x - 50, center_y - 90), "ログイン", 
              fill=layout['colors']['text'], font=layout['fonts']['header'])
    
    # フォームフィールド
    draw.text((center_x - 180, center_y - 50), "ユーザーID:", 
              fill=layout['colors']['text'], font=layout['fonts']['text'])
    draw.rectangle([center_x - 180, center_y - 25, center_x + 180, center_y - 5],
                  outline=layout['colors']['border'], width=1)
    
    draw.text((center_x - 180, center_y + 10), "パスワード:", 
              fill=layout['colors']['text'], font=layout['fonts']['text'])
    draw.rectangle([center_x - 180, center_y + 35, center_x + 180, center_y + 55],
                  outline=layout['colors']['border'], width=1)
    
    # ログインボタン
    draw.rectangle([center_x - 80, center_y + 80, center_x + 80, center_y + 110],
                  fill=layout['colors']['primary'])
    draw.text((center_x - 30, center_y + 90), "ログイン", 
              fill=(255, 255, 255), font=layout['fonts']['text'])
    
    return img

def create_home_screen():
    """ホーム画面を生成"""
    img, draw, layout = create_base_layout(title="ホーム", active_menu="ホーム")
    
    content_x = layout['content_x']
    content_width = layout['content_width']
    
    # ダッシュボードカード
    cards = [
        ("プロフィール", "基本情報を管理", 150),
        ("スキル情報", "スキルを登録・更新", 150),
        ("目標管理", "キャリアプランを設定", 300),
        ("作業実績", "案件実績を記録", 300),
        ("研修記録", "研修履歴を管理", 450),
        ("レポート", "各種レポートを出力", 450)
    ]
    
    card_width = 200
    card_height = 120
    
    for i, (title, desc, y_pos) in enumerate(cards):
        x_pos = content_x + (i % 3) * (card_width + 20)
        
        # カード背景
        draw.rectangle([x_pos, y_pos, x_pos + card_width, y_pos + card_height],
                      outline=layout['colors']['border'], width=2)
        
        # カードタイトル
        draw.text((x_pos + 10, y_pos + 10), title, 
                  fill=layout['colors']['text'], font=layout['fonts']['header'])
        
        # カード説明
        draw.text((x_pos + 10, y_pos + 40), desc, 
                  fill=layout['colors']['text'], font=layout['fonts']['small'])
    
    return img

def create_skill_screen():
    """スキル管理画面を生成"""
    img, draw, layout = create_base_layout(title="スキル管理", active_menu="スキル")
    
    content_x = layout['content_x']
    content_width = layout['content_width']
    
    # スキルカテゴリセクション
    section_y = 150
    draw.rectangle([content_x, section_y, content_x + content_width, section_y + 200],
                  outline=layout['colors']['border'], width=2)
    draw.text((content_x + 10, section_y + 10), "技術スキル", 
              fill=layout['colors']['text'], font=layout['fonts']['header'])
    
    # スキル項目
    skills = [
        ("Java", "レベル 3"),
        ("Python", "レベル 2"),
        ("JavaScript", "レベル 4"),
        ("SQL", "レベル 3")
    ]
    
    skill_y = section_y + 40
    for skill, level in skills:
        draw.text((content_x + 20, skill_y), f"{skill}:", 
                  fill=layout['colors']['text'], font=layout['fonts']['text'])
        draw.text((content_x + 200, skill_y), level, 
                  fill=layout['colors']['text'], font=layout['fonts']['text'])
        skill_y += 30
    
    # スキルレーダーチャート（簡易版）
    chart_x = content_x + 400
    chart_y = section_y + 50
    chart_size = 120
    
    draw.ellipse([chart_x, chart_y, chart_x + chart_size, chart_y + chart_size],
                outline=layout['colors']['border'], width=2)
    draw.text((chart_x + 30, chart_y + chart_size + 10), "スキルレーダー", 
              fill=layout['colors']['text'], font=layout['fonts']['small'])
    
    return img

def create_career_screen():
    """キャリアプラン画面を生成"""
    img, draw, layout = create_base_layout(title="キャリアプラン", active_menu="キャリア")
    
    content_x = layout['content_x']
    content_width = layout['content_width']
    
    # 目標設定セクション
    section_y = 150
    draw.rectangle([content_x, section_y, content_x + content_width, section_y + 180],
                  outline=layout['colors']['border'], width=2)
    draw.text((content_x + 10, section_y + 10), "今年度の目標", 
              fill=layout['colors']['text'], font=layout['fonts']['header'])
    
    # 目標項目
    goals = [
        "Javaスキルをレベル4に向上",
        "プロジェクトリーダー経験を積む",
        "AWS認定資格を取得"
    ]
    
    goal_y = section_y + 40
    for i, goal in enumerate(goals, 1):
        draw.text((content_x + 20, goal_y), f"{i}. {goal}", 
                  fill=layout['colors']['text'], font=layout['fonts']['text'])
        goal_y += 30
    
    # 進捗セクション
    section_y = 350
    draw.rectangle([content_x, section_y, content_x + content_width, section_y + 150],
                  outline=layout['colors']['border'], width=2)
    draw.text((content_x + 10, section_y + 10), "進捗状況", 
              fill=layout['colors']['text'], font=layout['fonts']['header'])
    
    # 進捗バー（簡易版）
    progress_items = [
        ("Javaスキル向上", 70),
        ("リーダー経験", 40),
        ("AWS資格取得", 20)
    ]
    
    progress_y = section_y + 40
    for item, progress in progress_items:
        draw.text((content_x + 20, progress_y), item, 
                  fill=layout['colors']['text'], font=layout['fonts']['text'])
        
        # 進捗バー
        bar_width = 200
        draw.rectangle([content_x + 250, progress_y, content_x + 250 + bar_width, progress_y + 15],
                      outline=layout['colors']['border'], width=1)
        draw.rectangle([content_x + 250, progress_y, content_x + 250 + (bar_width * progress // 100), progress_y + 15],
                      fill=layout['colors']['primary'])
        
        draw.text((content_x + 460, progress_y), f"{progress}%", 
                  fill=layout['colors']['text'], font=layout['fonts']['small'])
        progress_y += 35
    
    return img

def generate_screen_image(screen_type, spec_id, screen_id):
    """指定された画面タイプの画像を生成"""
    
    screen_generators = {
        'login': create_login_screen,
        'home': create_home_screen,
        'skill': create_skill_screen,
        'career': create_career_screen,
        'profile': lambda: create_base_layout(title="プロフィール", active_menu="プロフィール")[0]
    }
    
    if screen_type not in screen_generators:
        raise ValueError(f"未対応の画面タイプ: {screen_type}")
    
    img = screen_generators[screen_type]()
    
    # 画像を保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{screen_type}_ui_mockup_{timestamp}.png"
    filepath = os.path.join("docs/design/screens", filename)
    
    # ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    img.save(filepath)
    
    # メタデータを保存
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "type": f"mock_ui_image_{screen_type}",
        "description": f"{screen_type}画面のモックUI画像（日本語対応版）",
        "size": f"{img.size[0]}x{img.size[1]}",
        "filename": filename,
        "specification_id": spec_id,
        "screen_id": screen_id,
        "screen_type": screen_type
    }
    
    metadata_filepath = filepath.replace('.png', '_metadata.json')
    with open(metadata_filepath, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    return filepath, metadata_filepath

def main():
    """メイン実行関数"""
    print("=" * 70)
    print("🎨 汎用画面UI画像生成ツール（日本語対応版）")
    print("=" * 70)
    
    # 優先度の高い画面から生成
    screens_to_generate = [
        ('login', 'TNT.3-AUTH.1', 'SCR_AUT_Login'),
        ('home', 'PLT.1-WEB.1', 'SCR_CMN_Home'),
        ('skill', 'SKL.1-HIER.1', 'SCR_SKL_Skill'),
        ('career', 'CAR.1-PLAN.1', 'SCR_CAR_Plan')
    ]
    
    generated_files = []
    
    for screen_type, spec_id, screen_id in screens_to_generate:
        try:
            print(f"\n🎨 {screen_type}画面を生成中...")
            filepath, metadata_filepath = generate_screen_image(screen_type, spec_id, screen_id)
            generated_files.append((screen_type, filepath))
            print(f"✅ {screen_type}画面の生成完了: {filepath}")
        except Exception as e:
            print(f"❌ {screen_type}画面の生成失敗: {e}")
    
    print(f"\n🎉 画像生成完了！ {len(generated_files)}個の画面画像を生成しました")
    print("\n📁 生成されたファイル:")
    for screen_type, filepath in generated_files:
        print(f"  • {screen_type}: {filepath}")
    
    return len(generated_files) > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
