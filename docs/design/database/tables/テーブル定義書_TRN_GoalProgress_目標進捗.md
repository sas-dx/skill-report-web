# テーブル定義書: TRN_GoalProgress (目標進捗)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | TRN_GoalProgress |
| 論理名 | 目標進捗 |
| カテゴリ | トランザクション系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/TRN_GoalProgress_details.yaml` で行ってください。



## 📝 テーブル概要

TRN_GoalProgress（目標進捗）は、社員個人の目標設定と進捗状況を管理するトランザクションテーブルです。

主な目的：
- 個人目標の設定・管理（業務目標、スキル向上目標等）
- 目標達成度の定期的な進捗管理
- 上司・部下間での目標共有・フィードバック
- 人事評価・査定の基礎データ
- 組織目標と個人目標の連携管理

このテーブルは、人事評価制度、目標管理制度（MBO）、人材育成など、
組織の成果管理と人材開発の基盤となる重要なデータを提供します。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  |  |  | 目標を設定した社員のID |
| goal_title | 目標タイトル | VARCHAR | 200 | ○ |  |  |  | 目標の簡潔なタイトル |
| goal_category | 目標カテゴリ | ENUM |  | ○ |  |  |  | 目標のカテゴリ（BUSINESS:業務、SKILL:スキル、CAREER:キャリア） |
| target_date | 目標期限 | DATE |  | ○ |  |  |  | 目標達成の期限日 |
| progress_rate | 進捗率 | DECIMAL | 5,2 | ○ |  |  |  | 目標の進捗率（0.00-100.00%） |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_employee | employee_id | × | 社員別検索用 |

## 📊 サンプルデータ

```json
[
  {
    "employee_id": "EMP000001",
    "goal_title": "Java技術習得",
    "goal_category": "SKILL",
    "target_date": "2025-12-31",
    "progress_rate": 50.0
  }
]
```

## 📋 業務ルール

- 進捗率は0-100%の範囲で設定
- 目標期限は設定日より未来の日付
