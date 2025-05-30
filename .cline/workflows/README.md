# 設計書ベース修正ワークフロー

## 概要

このワークフローは、要件定義起点の包括的な設計書ベース修正システムです。設計書間の相互参照を自動同期し、一貫性を保持します。

## ワークフロー構成

```
.cline/workflows/
├── design-driven.json          # メインワークフロー定義
├── templates/                  # 設計書テンプレート
│   ├── screen_spec_template.md
│   ├── interface_spec_template.md
│   ├── table_spec_template.md
│   ├── api_spec_template.md
│   └── batch_definition_template.md
├── logs/                       # 実行ログ（自動生成）
└── README.md                   # このファイル
```

## 主要機能

### 1. 相互参照同期
- **画面一覧** ⇔ **画面設計書**
- **インターフェース一覧** ⇔ **インターフェース定義書**
- **テーブル一覧** ⇔ **テーブル定義書** ⇔ **エンティティ関連図**
- **API一覧** ⇔ **API定義書**
- **バッチ一覧** ⇔ **バッチ仕様書**

### 2. 自動テンプレート生成
新規設計書の追加時に、適切なテンプレートから設計書を自動生成

### 3. 整合性検証
設計書間の矛盾や循環依存を検知・報告

### 4. プロジェクト基本情報同期
設計変更をプロジェクト基本情報に自動反映

## トリガー一覧

| トリガー | 対象ファイル | 優先度 | 説明 |
|----------|--------------|--------|------|
| requirements_change | docs/requirements/*.md | critical | 要件定義変更 |
| screen_list_update | docs/design/screens/画面一覧.md | high | 画面一覧更新 |
| screen_spec_update | docs/design/screens/specs/画面設計書_*.md | high | 画面設計書更新 |
| interface_list_update | docs/design/interface/インターフェース一覧.md | high | インターフェース一覧更新 |
| interface_spec_update | docs/design/interfaces/specs/インターフェース仕様書_*.md | high | インターフェース定義書更新 |
| table_list_update | docs/design/database/テーブル一覧.md | high | テーブル一覧更新 |
| table_spec_update | docs/design/database/tables/テーブル定義書_*.md | high | テーブル定義書更新 |
| entity_diagram_update | docs/design/database/エンティティ関連図.md | high | エンティティ関連図更新 |
| api_list_update | docs/design/api/API一覧.md | high | API一覧更新 |
| api_spec_update | docs/design/api/specs/API定義書_*.md | high | API定義書更新 |
| batch_list_update | docs/design/batch/バッチ一覧.md | high | バッチ一覧更新 |
| batch_spec_update | docs/design/batch/specs/バッチ仕様書_*.md | high | バッチ仕様書更新 |

## 実行フェーズ

### Phase 1: 変更検知・分析
1. 変更元ファイルの特定
2. 影響範囲の分析
3. 更新優先度の計算

### Phase 2: 相互参照同期
1. 画面設計の相互同期
2. インターフェース設計の相互同期
3. データベース設計の相互同期
4. API設計の相互同期
5. バッチ設計の相互同期

### Phase 3: 設計統合
1. 画面-インターフェース統合
2. API-データベース統合
3. バッチ-データベース統合

### Phase 4: プロジェクト基本情報同期
1. README.md更新
2. 要件定義基本情報更新
3. メモリバンク更新
4. 実装計画更新

### Phase 5: 実装同期
1. 実装更新の生成
2. コードテンプレート生成
3. テスト仕様更新
4. マイグレーション生成

### Phase 6: 整合性検証
1. 設計書整合性検証
2. 相互参照チェック
3. 要件トレーサビリティ検証
4. データモデル整合性チェック

## 使用方法

### 手動実行
```bash
# ワークフロー全体の実行
cline workflow run design-driven

# 特定フェーズの実行
cline workflow run design-driven --phase cross_reference_sync

# 特定トリガーの実行
cline workflow run design-driven --trigger screen_list_update
```

### 自動実行
ファイル変更時に自動的にトリガーされ、該当する同期処理が実行されます。

## 設定

### ワークフロー設定
`design-driven.json`で以下の設定が可能：

- **トリガー条件**: ファイルパターンと優先度
- **同期ルール**: 同期対象フィールドと更新戦略
- **テンプレート**: 新規作成時のテンプレート
- **バリデーション**: 命名規則と整合性チェック
- **通知設定**: ログレベルと通知先
- **パフォーマンス**: タイムアウトと並列実行数

### ログ設定
```json
{
  "notification_settings": {
    "channels": {
      "console": {
        "enabled": true,
        "log_level": "info"
      },
      "file": {
        "enabled": true,
        "log_file": ".cline/logs/workflow.log",
        "log_level": "debug"
      }
    }
  }
}
```

## テンプレート

### 利用可能なテンプレート
- `screen_spec_template.md`: 画面設計書テンプレート
- `interface_spec_template.md`: インターフェース仕様書テンプレート
- `table_spec_template.md`: テーブル定義書テンプレート
- `api_spec_template.md`: API定義書テンプレート
- `batch_definition_template.md`: バッチ定義書テンプレート

### テンプレート変数
各テンプレートで使用可能な変数：

```handlebars
{{id}}              # 設計書ID
{{name}}            # 設計書名
{{priority}}        # 優先度
{{description}}     # 説明
{{current_date}}    # 現在日時
{{related_*}}       # 関連要素配列
```

## エラーハンドリング

### リトライ設定
```json
{
  "error_handling": {
    "retry_policy": {
      "max_retries": 3,
      "retry_delay": 1000,
      "exponential_backoff": true
    }
  }
}
```

### フォールバック戦略
- **テンプレート生成失敗**: 最小限のテンプレートを使用
- **同期失敗**: ログ出力して継続
- **バリデーション失敗**: レポート出力してスキップ

### 復旧機能
- **バックアップ**: 同期前に自動バックアップ
- **ロールバック**: 重大エラー時の自動ロールバック
- **エラーレポート**: 詳細なエラーレポート生成

## 監視・アラート

### メトリクス
- 同期操作回数
- 同期実行時間
- エラー率
- ファイル変更頻度

### アラート条件
- **高エラー率**: 10%超過時に管理者通知
- **長時間実行**: 5分超過時に警告ログ

## トラブルシューティング

### よくある問題

#### 1. 同期が実行されない
**原因**: ファイルパターンが一致しない
**対処**: `design-driven.json`のトリガー設定を確認

#### 2. テンプレート生成に失敗
**原因**: テンプレートファイルが見つからない
**対処**: `templates/`ディレクトリの存在を確認

#### 3. 循環依存エラー
**原因**: 設計書間で循環参照が発生
**対処**: 依存関係を見直し、循環を解消

### ログ確認
```bash
# 実行ログの確認
tail -f .cline/logs/workflow.log

# エラーログの確認
grep ERROR .cline/logs/workflow.log
```

## 開発・カスタマイズ

### 新しいトリガーの追加
1. `design-driven.json`の`triggers`配列に追加
2. 対応する`automation_rules`を定義
3. 必要に応じてテンプレートを作成

### カスタムバリデーションの追加
1. `validation_rules`セクションに新しいルールを定義
2. 対応する検証ロジックを実装

### 通知チャネルの追加
1. `notification_settings.channels`に新しいチャネルを定義
2. 対応する通知ロジックを実装

## バージョン履歴

| バージョン | 日付 | 変更内容 |
|------------|------|----------|
| 2.0.0 | 2025-05-31 | 包括的設計書ベース修正ワークフロー実装 |
| 1.0.0 | 2025-05-20 | 初版リリース |

---

**このワークフローにより、設計書の一貫性を保ちながら効率的な開発プロセスを実現します。**
