# テーブル定義書_MST_NotificationTemplate_通知テンプレート

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_NotificationTemplate |
| 論理名 | 通知テンプレート |
| 用途 | 通知メッセージのテンプレート管理 |
| カテゴリ | マスタ系 |
| 作成日 | 2024-12-19 |
| 最終更新日 | 2024-12-19 |

## テーブル概要

通知機能で使用するメッセージテンプレートを管理するマスタテーブルです。
メール、Slack、Teams、LINE WORKS等の各種通知チャネルに対応したテンプレートを格納し、
動的な値の埋め込みに対応したプレースホルダー機能を提供します。

## テーブル構造

| # | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | PK | FK | インデックス | 説明 |
|---|----------|--------|----------|------|------|------------|----|----|--------------|------|
| 1 | template_id | テンプレートID | VARCHAR | 50 | NOT NULL | - | ○ | - | PK | テンプレートの一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 50 | NOT NULL | - | - | ○ | IDX | テナント識別子 |
| 3 | template_name | テンプレート名 | VARCHAR | 100 | NOT NULL | - | - | - | IDX | テンプレートの名称 |
| 4 | template_type | テンプレート種別 | VARCHAR | 20 | NOT NULL | - | - | - | IDX | EMAIL/SLACK/TEAMS/LINE_WORKS |
| 5 | category | カテゴリ | VARCHAR | 50 | NOT NULL | - | - | - | IDX | 通知カテゴリ（SYSTEM/USER/ADMIN等） |
| 6 | subject_template | 件名テンプレート | VARCHAR | 200 | NULL | - | - | - | - | メール件名等のテンプレート |
| 7 | body_template | 本文テンプレート | TEXT | - | NOT NULL | - | - | - | - | メッセージ本文のテンプレート |
| 8 | variables | 変数定義 | JSON | - | NULL | - | - | - | - | 利用可能な変数の定義情報 |
| 9 | is_active | 有効フラグ | BOOLEAN | - | NOT NULL | true | - | - | IDX | テンプレートの有効/無効 |
| 10 | priority | 優先度 | INTEGER | - | NOT NULL | 1 | - | - | - | テンプレートの優先度（1:高 2:中 3:低） |
| 11 | description | 説明 | TEXT | - | NULL | - | - | - | - | テンプレートの説明 |
| 12 | created_at | 作成日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード作成日時 |
| 13 | created_by | 作成者 | VARCHAR | 50 | NOT NULL | - | - | - | - | レコード作成者 |
| 14 | updated_at | 更新日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | - | レコード更新日時 |
| 15 | updated_by | 更新者 | VARCHAR | 50 | NOT NULL | - | - | - | - | レコード更新者 |

## リレーション

### 参照先テーブル
- MST_Tenant (tenant_id)

### 参照元テーブル
- TRN_Notification (template_id)
- HIS_NotificationLog (template_id)

## データ仕様

### template_type（テンプレート種別）
- EMAIL: メール通知用テンプレート
- SLACK: Slack通知用テンプレート
- TEAMS: Microsoft Teams通知用テンプレート
- LINE_WORKS: LINE WORKS通知用テンプレート

### category（カテゴリ）
- SYSTEM: システム通知（メンテナンス、障害等）
- USER: ユーザー通知（登録完了、パスワード変更等）
- ADMIN: 管理者通知（承認依頼、アラート等）
- SKILL: スキル関連通知（評価完了、証跡登録等）
- TRAINING: 研修関連通知（受講案内、完了通知等）

### priority（優先度）
- 1: 高（緊急通知）
- 2: 中（通常通知）
- 3: 低（情報通知）

### variables（変数定義）例
```json
{
  "user_name": "ユーザー名",
  "skill_name": "スキル名",
  "evaluation_date": "評価日",
  "system_url": "システムURL"
}
```

### テンプレート例
```
件名: 【スキル管理システム】スキル評価が完了しました
本文: 
{{user_name}}様

お疲れ様です。
{{skill_name}}のスキル評価が{{evaluation_date}}に完了しました。

詳細は以下のURLからご確認ください。
{{system_url}}/skill/detail/{{skill_id}}

スキル管理システム
```

## 運用仕様

### データ保持期間
- 無期限（マスタデータのため）

### バックアップ
- 日次バックアップ対象
- 月次アーカイブ対象

### メンテナンス
- 定期的なテンプレート内容の見直し
- 不要テンプレートの無効化

## パフォーマンス

### 想定レコード数
- 初期: 100件
- 1年後: 500件
- 3年後: 1,000件

### アクセスパターン
- 通知送信時の参照: 高頻度
- テンプレート管理画面での更新: 低頻度

### インデックス設計
- PRIMARY KEY: template_id
- INDEX: tenant_id, template_type, category, is_active

## セキュリティ

### アクセス制御
- 参照: 通知機能、管理者
- 更新: システム管理者のみ
- 削除: システム管理者のみ

### 機密情報
- テンプレート内容に個人情報を含めない
- プレースホルダーを使用した動的値埋め込み

## 移行仕様

### 初期データ
- システム標準テンプレートの投入
- 各通知チャネル用のデフォルトテンプレート

### データ移行
- 既存システムからのテンプレート移行
- 変数定義の標準化

## 特記事項

### 制約事項
- テンプレート内のプレースホルダーは{{変数名}}形式
- HTMLタグの使用はメール通知のみ許可
- 各通知チャネルの文字数制限に注意

### 拡張予定
- 多言語対応テンプレート
- 条件分岐テンプレート
- リッチテキスト対応

### 関連システム
- 通知配信システム
- テンプレート管理画面
- 外部連携システム（Slack、Teams等）
