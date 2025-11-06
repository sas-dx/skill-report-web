# 統合設定システム

## エグゼクティブサマリー

この統合設定システムは、プロジェクト固有設定・ツール設定・グローバル設定を階層的に管理し、設定駆動型の開発ツールを実現します。YAML形式の設定ファイル、優先度ベースの設定マージ、動的設定取得機能を提供し、複数プロジェクト・複数ツールでの再利用可能な設定管理を支援します。他プロジェクトでも容易に適用可能な汎用的な設計となっており、設定の一元管理と保守性の向上を実現します。

## 概要

このシステムは以下の3層構造で設定を管理します：

```
設定優先度（高 → 低）
├── プロジェクト設定 (config/projects/{project_name}.yaml)
├── ツール設定 (config/tools/{tool_name}.yaml)
└── グローバル設定 (config/global/default.yaml)
```

## ディレクトリ構造

```
config/
├── README.md                    # このファイル
├── config_manager.py           # 統合設定マネージャー
├── global/                     # グローバル設定
│   └── default.yaml           # デフォルト設定
├── tools/                      # ツール別設定
│   ├── ui-generator.yaml      # UI生成ツール設定
│   ├── database-tools.yaml    # データベースツール設定
│   └── report-generator.yaml  # レポート生成ツール設定
└── projects/                   # プロジェクト別設定
    ├── skill-report-web.yaml  # スキル報告書プロジェクト
    ├── project-template.yaml  # プロジェクトテンプレート
    └── example-project.yaml   # サンプルプロジェクト
```

## 設定ファイル形式

### グローバル設定 (global/default.yaml)

```yaml
# システム基本情報
system:
  name: "汎用開発ツールセット"
  version: "1.0.0"
  description: "設定駆動型開発ツール"

# エンコーディング設定
encoding:
  default: "utf-8"
  input: "utf-8"
  output: "utf-8"

# ディレクトリ設定
directories:
  docs: "docs"
  output: "output"
  temp: "temp"

# デフォルトカラーパレット
color_palette:
  primary: "#1976d2"
  secondary: "#424242"
  accent: "#ff5722"
  background: "#ffffff"
  background_light: "#f5f5f5"
  text: "#212121"
  text_light: "#757575"
  border: "#e0e0e0"
  success: "#4caf50"
  warning: "#ff9800"
  error: "#f44336"

# フォント設定
fonts:
  japanese_candidates:
    - "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
    - "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
    - "C:/Windows/Fonts/msgothic.ttc"
  sizes:
    small: 12
    text: 14
    header: 16
    title: 20
    large: 24

# アイコンマッピング
icons:
  mapping:
    user: "👤"
    settings: "⚙️"
    logout: "🚪"
    home: "🏠"
    profile: "👤"
    skills: "🎯"
    career: "📈"
    work: "💼"
    training: "📚"
    reports: "📊"
    search: "🔍"
    edit: "✏️"
    delete: "🗑️"
    save: "💾"
    cancel: "❌"
```

### ツール設定 (tools/ui-generator.yaml)

```yaml
# ツール基本情報
tool_info:
  name: "UI画像生成ツール"
  version: "2.0.0"
  description: "設定駆動型UI画像生成"

# 画像生成設定
image_generation:
  default_size:
    width: 1792
    height: 1024
  output_format: "PNG"
  quality: 95

# レイアウト設定
layout:
  header_height: 60
  sidebar_width: 250
  content_padding: 20

# コンポーネント設定
components:
  header:
    height: 60
    background: "#ffffff"
    border_bottom: true
    logo_position: "left"
    user_menu_position: "right"
  
  sidebar:
    width: 250
    background: "#f5f5f5"
    border_right: true
  
  button:
    padding: "8px 16px"
    border_radius: "4px"
  
  input:
    height: 30
    padding: "8px 12px"
    border_radius: "4px"
  
  card:
    padding: "16px"
    border_radius: "8px"
    shadow: true

# 画面タイプ設定
screen_types:
  login:
    layout_type: "login"
    show_header: false
    show_sidebar: false
    title: "ログイン"
  
  dashboard:
    layout_type: "dashboard"
    show_header: true
    show_sidebar: true
    show_welcome_message: true
    show_quick_actions: true
    title: "ダッシュボード"
  
  form:
    layout_type: "form"
    show_header: true
    show_sidebar: true
    breadcrumb: true
    show_buttons: true
  
  detail:
    layout_type: "detail"
    show_header: true
    show_sidebar: true
    breadcrumb: true

# 出力設定
output:
  base_directory: "output"
  filename_pattern: "{screen_type}_ui_mockup_{timestamp}.png"
  metadata_enabled: true

# 命名規則
naming_conventions:
  timestamp_format: "%Y%m%d_%H%M%S"
  file_prefix: "ui_mockup"
```

### プロジェクト設定 (projects/skill-report-web.yaml)

```yaml
# プロジェクト基本情報
project_info:
  name: "年間スキル報告書WEB化PJT"
  version: "1.0.0"
  description: "AI駆動開発による年間スキル報告書システム"

# ブランディング設定
branding:
  system_name: "年間スキル報告書システム"
  logo_text: "SKILL"
  primary_color: "#1976d2"
  secondary_color: "#424242"
  accent_color: "#ff5722"

# ディレクトリ設定（プロジェクト固有）
directories:
  design: "docs/design"
  screens: "docs/design/screens"
  api: "docs/design/api"
  database: "docs/design/database"

# ナビゲーション設定
navigation:
  sidebar_items:
    - key: "ダッシュボード"
      name: "ダッシュボード"
      icon: "home"
      path: "/dashboard"
    - key: "プロフィール"
      name: "プロフィール"
      icon: "profile"
      path: "/profile"
    - key: "スキル"
      name: "スキル管理"
      icon: "skills"
      path: "/skills"
    - key: "キャリア"
      name: "キャリアプラン"
      icon: "career"
      path: "/career"
    - key: "作業実績"
      name: "作業実績"
      icon: "work"
      path: "/work"
    - key: "研修"
      name: "研修管理"
      icon: "training"
      path: "/training"
    - key: "レポート"
      name: "レポート"
      icon: "reports"
      path: "/reports"

# 画面設定（プロジェクト固有）
screens:
  profile:
    screen_id: "SCR_PRO_Profile"
    title: "プロフィール管理"
    layout_type: "form"
    show_radar_chart: false
  
  skill:
    screen_id: "SCR_SKL_Skill"
    title: "スキル管理"
    layout_type: "detail"
    show_radar_chart: true
  
  career:
    screen_id: "SCR_CAR_Career"
    title: "キャリアプラン"
    layout_type: "detail"
    show_timeline: true
  
  home:
    screen_id: "SCR_HOME_Dashboard"
    title: "ダッシュボード"
    layout_type: "dashboard"

# フォーム項目設定
form_fields:
  profile:
    basic_info:
      - label: "社員番号"
        type: "text"
        required: true
        readonly: true
      - label: "氏名"
        type: "text"
        required: true
      - label: "メールアドレス"
        type: "email"
        required: true
      - label: "所属部署"
        type: "select"
        required: true
    
    contact_info:
      - label: "電話番号"
        type: "tel"
        required: false
      - label: "内線番号"
        type: "text"
        required: false

# スキル設定
skills:
  categories:
    - name: "プログラミング言語"
      icon: "💻"
      subcategories: ["JavaScript", "Python", "Java", "C#"]
    - name: "フレームワーク"
      icon: "🔧"
      subcategories: ["React", "Vue.js", "Angular", "Django"]
    - name: "データベース"
      icon: "🗄️"
      subcategories: ["PostgreSQL", "MySQL", "MongoDB", "Redis"]
    - name: "クラウド"
      icon: "☁️"
      subcategories: ["AWS", "Azure", "GCP", "Docker"]
```

## 使用方法

### 1. 基本的な使用方法

```python
from config_manager import ConfigManager

# 設定マネージャー初期化
config = ConfigManager(
    project_name="skill-report-web",
    tool_name="ui-generator"
)

# 設定値取得
system_name = config.get("system.name")
primary_color = config.get("branding.primary_color")
nav_items = config.get_navigation_items()
```

### 2. UI生成ツールでの使用

```bash
# プロフィール画面生成
python generate_ui_images_universal_refactored.py \
  --screen-type profile \
  --project skill-report-web \
  --tool ui-generator

# ログイン画面生成
python generate_ui_images_universal_refactored.py \
  --screen-type login \
  --project skill-report-web
```

### 3. 設定の階層マージ

設定は以下の優先度でマージされます：

```python
# 1. グローバル設定を読み込み
global_config = {
    "color_palette": {"primary": "#1976d2"},
    "fonts": {"sizes": {"text": 14}}
}

# 2. ツール設定をマージ
tool_config = {
    "image_generation": {"default_size": {"width": 1792}}
}

# 3. プロジェクト設定をマージ（最高優先度）
project_config = {
    "branding": {"primary_color": "#2196f3"}  # グローバル設定を上書き
}

# 最終的な統合設定
merged_config = {
    "color_palette": {"primary": "#2196f3"},  # プロジェクト設定で上書き
    "fonts": {"sizes": {"text": 14}},
    "image_generation": {"default_size": {"width": 1792}},
    "branding": {"primary_color": "#2196f3"}
}
```

## 新しいプロジェクトの追加

### 1. プロジェクト設定ファイル作成

```bash
# 新しいプロジェクト設定を作成
cp config/projects/project-template.yaml config/projects/my-new-project.yaml
```

### 2. プロジェクト固有設定の編集

```yaml
# config/projects/my-new-project.yaml
project_info:
  name: "新しいプロジェクト"
  version: "1.0.0"

branding:
  system_name: "新システム"
  primary_color: "#4caf50"

# プロジェクト固有の設定を追加...
```

### 3. ツールでの使用

```python
# 新しいプロジェクトでツール使用
config = ConfigManager(
    project_name="my-new-project",
    tool_name="ui-generator"
)
```

## 新しいツールの追加

### 1. ツール設定ファイル作成

```yaml
# config/tools/my-new-tool.yaml
tool_info:
  name: "新しいツール"
  version: "1.0.0"

# ツール固有の設定
my_tool_settings:
  option1: "value1"
  option2: "value2"
```

### 2. ツールでの設定使用

```python
from config_manager import ConfigManager

class MyNewTool:
    def __init__(self, project_name: str):
        self.config = ConfigManager(
            project_name=project_name,
            tool_name="my-new-tool"
        )
        
        # ツール固有設定取得
        self.tool_settings = self.config.get("my_tool_settings", {})
```

## 設定検証

```python
# 設定検証実行
validation = config.validate_config()

if validation["errors"]:
    print("設定エラー:")
    for error in validation["errors"]:
        print(f"  - {error}")

if validation["warnings"]:
    print("設定警告:")
    for warning in validation["warnings"]:
        print(f"  - {warning}")
```

## 設定のエクスポート

```python
# 統合設定をファイルにエクスポート
config.export_merged_config("merged_config.yaml", format="yaml")
config.export_merged_config("merged_config.json", format="json")
```

## ベストプラクティス

### 1. 設定の分離
- **グローバル設定**: 全プロジェクト共通の基本設定
- **ツール設定**: ツール固有の動作設定
- **プロジェクト設定**: プロジェクト固有のブランディング・業務設定

### 2. 命名規則
- ファイル名: `{project_name}.yaml`, `{tool_name}.yaml`
- キー名: スネークケース (`primary_color`, `font_sizes`)
- 階層: ドット記法でアクセス (`branding.primary_color`)

### 3. 設定の継承
- 上位設定を継承し、必要な部分のみ上書き
- デフォルト値の適切な設定
- 設定の重複を避ける

### 4. バージョン管理
- 設定ファイルもGitで管理
- 破壊的変更時はバージョン番号を更新
- 設定変更時は影響範囲を確認

## トラブルシューティング

### よくある問題

#### 1. 設定ファイルが見つからない
```
警告: 設定ファイルが見つかりません: config/projects/my-project.yaml
```
**解決方法**: ファイルパスとファイル名を確認

#### 2. YAML構文エラー
```
設定ファイル読み込みエラー: invalid yaml syntax
```
**解決方法**: YAMLの構文を確認（インデント、コロン、ハイフンなど）

#### 3. 必須設定の不足
```
設定エラー: 必須設定が不足: system.name
```
**解決方法**: グローバル設定に必須項目を追加

### デバッグ方法

```python
# 設定の詳細確認
config = ConfigManager(project_name="my-project", tool_name="my-tool")

# 各レベルの設定を個別確認
print("グローバル設定:", config.get_global_config())
print("ツール設定:", config.get_tool_config())
print("プロジェクト設定:", config.get_project_config())
print("統合設定:", config.merge_configs())

# 特定キーの値確認
print("プライマリカラー:", config.get("branding.primary_color"))
```

## 関連ドキュメント

- [プロジェクト固有ルール](.clinerules/01-project-specific-rules.md)
- [統合開発ルール](.clinerules/00-core-rules.md)
- [UI生成ツール使用方法](../generate_ui_images_universal_refactored.py)

---

この統合設定システムにより、複数のプロジェクトとツールで一貫した設定管理を実現し、開発効率と保守性を向上させることができます。
