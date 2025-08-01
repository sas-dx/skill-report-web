#!/usr/bin/env python3
"""
プロフィール画面UI画像生成スクリプト
要求仕様ID: PRO.1-BASE.1
対応設計書: docs/design/screens/specs/画面定義書_SCR_PRO_Profile_プロフィール画面.md
"""

import os
import sys
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
import json
from datetime import datetime

def generate_profile_ui_image():
    """プロフィール管理画面のUI画像を生成"""
    
    # OpenAI APIキーの確認
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ エラー: OPENAI_API_KEYが設定されていません")
        print("以下のコマンドでAPIキーを設定してください:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    client = OpenAI(api_key=api_key)
    
    # プロンプト作成（設計書のワイヤーフレームを基に詳細なUI説明）
    prompt = """
Create a professional web application interface mockup for a Japanese employee profile management screen. 

Layout specifications:
- Modern, clean corporate web application design
- Left sidebar navigation with menu items: ホーム, プロフィール (highlighted), スキル情報, 目標管理, 作業実績, 研修記録, レポート
- Top header with user dropdown, notifications icon, and logout button
- Main content area with "プロフィール管理" (Profile Management) title

Main content sections:
1. "基本情報" (Basic Information) section with form fields:
   - 社員番号 (Employee ID): read-only text field
   - 氏名(漢字) (Name in Kanji): editable text field
   - 氏名(カナ) (Name in Katakana): editable text field  
   - メールアドレス (Email): editable text field
   - 生年月日 (Birth Date): date picker field
   - 入社日 (Join Date): date picker field

2. "所属情報" (Organization Info) section with:
   - 部署 (Department): dropdown menu
   - 役職 (Position): dropdown menu
   - グループ (Group): dropdown menu
   - 上長 (Manager): read-only text field

3. "更新履歴" (Update History) section with:
   - Table with columns: 日時 (Date), 項目 (Item), 変更前 (Before), 変更後 (After), 変更者 (Changed By)
   - Sample data rows

4. Bottom action buttons: キャンセル (Cancel) and 保存 (Save)

Design style:
- Modern Japanese corporate web application
- Clean, professional layout with proper spacing
- Blue and white color scheme (#3399cc primary color)
- Form fields with proper labels and styling
- Responsive design appearance
- Professional typography
- Subtle shadows and borders for sections
"""

    try:
        print("🎨 UI画像を生成中...")
        print(f"📝 プロンプト: {prompt[:100]}...")
        
        # DALL-E 3で画像生成
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",  # 横長のレイアウトに適したサイズ
            quality="hd",
            n=1
        )
        
        # 生成された画像のURLを取得
        image_url = response.data[0].url
        print(f"✅ 画像生成完了: {image_url}")
        
        # 画像をダウンロード
        print("📥 画像をダウンロード中...")
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        # 画像を保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"profile_ui_mockup_{timestamp}.png"
        filepath = os.path.join("docs/design/screens", filename)
        
        # ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'wb') as f:
            f.write(image_response.content)
        
        print(f"💾 画像を保存しました: {filepath}")
        
        # 画像情報をJSONで保存
        metadata = {
            "generated_at": datetime.now().isoformat(),
            "prompt": prompt,
            "model": "dall-e-3",
            "size": "1792x1024",
            "quality": "hd",
            "original_url": image_url,
            "filename": filename,
            "specification_id": "PRO.1-BASE.1",
            "screen_id": "SCR-PROFILE",
            "design_document": "docs/design/screens/specs/画面定義書_SCR_PRO_Profile_プロフィール画面.md"
        }
        
        metadata_filepath = filepath.replace('.png', '_metadata.json')
        with open(metadata_filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"📋 メタデータを保存しました: {metadata_filepath}")
        
        # 画像サイズ情報を表示
        with Image.open(filepath) as img:
            print(f"📐 画像サイズ: {img.size[0]}x{img.size[1]} pixels")
        
        print("\n🎉 プロフィール画面UI画像の生成が完了しました！")
        print(f"📁 保存場所: {filepath}")
        print(f"🔗 元画像URL: {image_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {str(e)}")
        return False

def main():
    """メイン実行関数"""
    print("=" * 60)
    print("🎨 プロフィール管理画面 UI画像生成ツール")
    print("要求仕様ID: PRO.1-BASE.1")
    print("画面ID: SCR-PROFILE")
    print("=" * 60)
    
    success = generate_profile_ui_image()
    
    if success:
        print("\n✅ 処理が正常に完了しました")
        sys.exit(0)
    else:
        print("\n❌ 処理が失敗しました")
        sys.exit(1)

if __name__ == "__main__":
    main()
