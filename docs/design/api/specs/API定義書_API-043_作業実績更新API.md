# API定義書：API-043 作業実績更新API

## 1. 基本情報

- **API ID**: API-043
- **API名称**: 作業実績更新API
- **概要**: ユーザーの作業実績情報を更新する
- **エンドポイント**: `/api/work-records/{user_id}/{record_id}`
- **HTTPメソッド**: PUT
- **リクエスト形式**: JSON
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-WORK](画面設計書_SCR-WORK.md)
- **作成日**: 2025/05/28
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/28 初版作成

---

## 2. リクエスト仕様

### 2.1 リクエストヘッダ

| ヘッダ名 | 必須 | 説明 | 備考 |
|---------|------|------|------|
| Authorization | ○ | 認証トークン | Bearer {JWT} 形式 |
| Content-Type | ○ | リクエスト形式 | application/json |
| Accept | - | レスポンス形式 | application/json |

### 2.2 パスパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| user_id | string | ○ | ユーザーID | 自身のIDまたは部下のIDを指定可能 |
| record_id | string | ○ | 実績ID | |

### 2.3 リクエストボディ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| date | string | △ | 作業日 | ISO 8601形式（YYYY-MM-DD）<br>更新する場合のみ必須 |
| project_id | string | △ | プロジェクトID | 更新する場合のみ必須 |
| category | string | △ | 作業カテゴリ | 更新する場合のみ必須 |
| task | string | △ | 作業内容 | 最大100文字<br>更新する場合のみ必須 |
| hours | number | △ | 作業時間（時間） | 0.5単位、0.5〜24.0の範囲<br>更新する場合のみ必須 |
| status | string | △ | ステータス | "draft", "submitted", "approved", "rejected"<br>更新する場合のみ必須<br>承認者のみ"approved"/"rejected"に変更可能 |
| details | object | - | 詳細情報 | |
| review_comment | string | - | レビューコメント | status="approved"または"rejected"の場合のみ有効<br>最大1000文字 |

#### details オブジェクト

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| description | string | - | 詳細説明 | 最大1000文字 |
| achievements | string | - | 成果物・達成事項 | 最大1000文字 |
| issues | string | - | 課題・問題点 | 最大1000文字 |
| next_actions | string | - | 次のアクション | 最大1000文字 |
| related_skills | array | - | 関連スキル | |
| attachments | array | - | 添付ファイル | |

#### related_skills 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| skill_id | string | ○ | スキルID | |
| level_used | number | ○ | 使用レベル | 1-5（5が最高） |

#### attachments 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| file_id | string | ○ | ファイルID | 事前にファイルアップロードAPIで取得したID |

### 2.4 リクエスト例（一般ユーザーによる更新）

```json
{
  "task": "APIドキュメント作成と修正",
  "hours": 5.5,
  "status": "submitted",
  "details": {
    "description": "作業実績更新APIのドキュメントを作成し、レビュー指摘を反映",
    "achievements": "API仕様書の修正版を完成させた",
    "issues": "",
    "next_actions": "他APIとの整合性確認を行う",
    "related_skills": [
      {
        "skill_id": "S020",
        "level_used": 4
      },
      {
        "skill_id": "S021",
        "level_used": 3
      }
    ],
    "attachments": [
      {
        "file_id": "F001"
      },
      {
        "file_id": "F002"
      }
    ]
  }
}
```

### 2.5 リクエスト例（承認者による承認）

```json
{
  "status": "approved",
  "review_comment": "ドキュメントの品質が高く、わかりやすい仕様書になっています。良い成果物です。"
}
```

### 2.6 リクエスト例（承認者による却下）

```json
{
  "status": "rejected",
  "review_comment": "他APIとの整合性に問題があります。特にエラーコードの定義が統一されていないため、修正をお願いします。"
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| record_id | string | 実績ID | |
| user_id | string | ユーザーID | |
| date | string | 作業日 | ISO 8601形式（YYYY-MM-DD） |
| project_id | string | プロジェクトID | |
| project_name | string | プロジェクト名 | |
| category | string | 作業カテゴリ | |
| task | string | 作業内容 | |
| hours | number | 作業時間（時間） | |
| status | string | ステータス | "draft", "submitted", "approved", "rejected" |
| details | object | 詳細情報 | |
| review_comment | string | レビューコメント | status="approved"または"rejected"の場合のみ |
| created_at | string | 作成日時 | ISO 8601形式 |
| created_by | string | 作成者ID | |
| updated_at | string | 更新日時 | ISO 8601形式 |
| updated_by | string | 更新者ID | |
| reviewed_at | string | レビュー日時 | ISO 8601形式<br>status="approved"または"rejected"の場合のみ |
| reviewed_by | string | レビュー者ID | status="approved"または"rejected"の場合のみ |

#### details オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| description | string | 詳細説明 | |
| achievements | string | 成果物・達成事項 | |
| issues | string | 課題・問題点 | |
| next_actions | string | 次のアクション | |
| related_skills | array | 関連スキル | |
| attachments | array | 添付ファイル | |

#### related_skills 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| name | string | スキル名 | |
| category | string | スキルカテゴリ | |
| level_used | number | 使用レベル | 1-5（5が最高） |

#### attachments 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| file_id | string | ファイルID | |
| file_name | string | ファイル名 | |
| file_type | string | ファイルタイプ | |
| file_size | number | ファイルサイズ（バイト） | |
| upload_date | string | アップロード日時 | ISO 8601形式 |

### 3.2 正常時レスポンス例（一般ユーザーによる更新）

```json
{
  "record_id": "WR003",
  "user_id": "U12345",
  "date": "2025-05-28",
  "project_id": "P001",
  "project_name": "スキルレポートWEB化PJT",
  "category": "開発",
  "task": "APIドキュメント作成と修正",
  "hours": 5.5,
  "status": "submitted",
  "details": {
    "description": "作業実績更新APIのドキュメントを作成し、レビュー指摘を反映",
    "achievements": "API仕様書の修正版を完成させた",
    "issues": "",
    "next_actions": "他APIとの整合性確認を行う",
    "related_skills": [
      {
        "skill_id": "S020",
        "name": "API設計",
        "category": "technical",
        "level_used": 4
      },
      {
        "skill_id": "S021",
        "name": "ドキュメント作成",
        "category": "technical",
        "level_used": 3
      }
    ],
    "attachments": [
      {
        "file_id": "F001",
        "file_name": "api_spec_draft.pdf",
        "file_type": "application/pdf",
        "file_size": 1245678,
        "upload_date": "2025-05-28T14:30:00+09:00"
      },
      {
        "file_id": "F002",
        "file_name": "api_spec_revised.pdf",
        "file_type": "application/pdf",
        "file_size": 1356789,
        "upload_date": "2025-05-28T16:45:00+09:00"
      }
    ]
  },
  "review_comment": null,
  "created_at": "2025-05-28T15:45:00+09:00",
  "created_by": "U12345",
  "updated_at": "2025-05-28T17:30:00+09:00",
  "updated_by": "U12345",
  "reviewed_at": null,
  "reviewed_by": null
}
```

### 3.3 正常時レスポンス例（承認者による承認）

```json
{
  "record_id": "WR003",
  "user_id": "U12345",
  "date": "2025-05-28",
  "project_id": "P001",
  "project_name": "スキルレポートWEB化PJT",
  "category": "開発",
  "task": "APIドキュメント作成と修正",
  "hours": 5.5,
  "status": "approved",
  "details": {
    "description": "作業実績更新APIのドキュメントを作成し、レビュー指摘を反映",
    "achievements": "API仕様書の修正版を完成させた",
    "issues": "",
    "next_actions": "他APIとの整合性確認を行う",
    "related_skills": [
      {
        "skill_id": "S020",
        "name": "API設計",
        "category": "technical",
        "level_used": 4
      },
      {
        "skill_id": "S021",
        "name": "ドキュメント作成",
        "category": "technical",
        "level_used": 3
      }
    ],
    "attachments": [
      {
        "file_id": "F001",
        "file_name": "api_spec_draft.pdf",
        "file_type": "application/pdf",
        "file_size": 1245678,
        "upload_date": "2025-05-28T14:30:00+09:00"
      },
      {
        "file_id": "F002",
        "file_name": "api_spec_revised.pdf",
        "file_type": "application/pdf",
        "file_size": 1356789,
        "upload_date": "2025-05-28T16:45:00+09:00"
      }
    ]
  },
  "review_comment": "ドキュメントの品質が高く、わかりやすい仕様書になっています。良い成果物です。",
  "created_at": "2025-05-28T15:45:00+09:00",
  "created_by": "U12345",
  "updated_at": "2025-05-28T17:30:00+09:00",
  "updated_by": "U12345",
  "reviewed_at": "2025-05-29T10:15:00+09:00",
  "reviewed_by": "U67890"
}
```

### 3.4 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_DATE | 日付が不正です | 不正な日付形式 |
| 400 Bad Request | FUTURE_DATE | 未来の日付は指定できません | 未来日の指定 |
| 400 Bad Request | INVALID_PROJECT_ID | プロジェクトIDが不正です | 存在しないプロジェクトID |
| 400 Bad Request | INVALID_CATEGORY | カテゴリが不正です | 存在しないカテゴリ |
| 400 Bad Request | INVALID_HOURS | 作業時間が不正です | 0.5単位でない、または範囲外 |
| 400 Bad Request | INVALID_STATUS | ステータスが不正です | 存在しないステータス |
| 400 Bad Request | INVALID_STATUS_TRANSITION | ステータス遷移が不正です | 許可されていないステータス遷移 |
| 400 Bad Request | INVALID_SKILL_ID | スキルIDが不正です | 存在しないスキルID |
| 400 Bad Request | INVALID_SKILL_LEVEL | スキルレベルが不正です | 1-5の範囲外 |
| 400 Bad Request | INVALID_FILE_ID | ファイルIDが不正です | 存在しないファイルID |
| 400 Bad Request | DUPLICATE_RECORD | 重複する作業実績があります | 同一日・プロジェクト・カテゴリの実績が存在 |
| 400 Bad Request | DAILY_HOURS_EXCEEDED | 1日の作業時間上限を超えています | 1日の合計作業時間が24時間を超過 |
| 400 Bad Request | MISSING_REVIEW_COMMENT | レビューコメントが必要です | 承認/却下時にレビューコメントがない |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他ユーザーの情報更新権限なし |
| 403 Forbidden | NOT_REVIEWER | レビュー権限がありません | 承認/却下権限がない |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 404 Not Found | RECORD_NOT_FOUND | 作業実績が見つかりません | 指定された実績IDが存在しない |
| 409 Conflict | LOCKED_PERIOD | ロックされた期間です | 締め切り済み期間への更新 |
| 409 Conflict | ALREADY_APPROVED | 既に承認済みです | 承認済み実績の再承認 |
| 409 Conflict | ALREADY_REJECTED | 既に却下済みです | 却下済み実績の再却下 |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.5 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_STATUS_TRANSITION",
    "message": "ステータス遷移が不正です",
    "details": "承認済み状態から下書き状態への変更はできません。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - ユーザーIDの権限チェック（自身または部下のIDかどうか）
   - 実績IDの存在チェック
2. リクエストパラメータの検証
   - 日付の妥当性チェック（未来日でないこと）
   - プロジェクトID・カテゴリの存在チェック
   - 作業時間の妥当性チェック（0.5単位、範囲内）
   - ステータスの妥当性チェックとステータス遷移の検証
   - 関連スキル・添付ファイルの妥当性チェック
3. 重複チェック
   - 同一日・プロジェクト・カテゴリの作業実績が既に存在しないか確認（自身の実績は除く）
4. 日次作業時間チェック
   - 指定された日付の合計作業時間が24時間を超えないか確認
5. 期間ロックチェック
   - 指定された日付が締め切り済み期間でないか確認
6. 作業実績情報の更新
   - work_records テーブルの基本情報を更新
   - work_record_details テーブルの詳細情報を更新
   - work_record_skills テーブルの関連スキル情報を更新（全削除後に再登録）
   - work_record_attachments テーブルの添付ファイル情報を更新（全削除後に再登録）
   - work_record_reviews テーブルにレビュー情報を登録（承認/却下時）
7. レスポンスの生成
   - 更新結果を整形
8. レスポンス返却

### 4.2 権限チェック

- 自身の作業実績は常に更新可能（ただし、承認/却下済みの実績は更新不可）
- 他ユーザーの作業実績更新には以下のいずれかの条件を満たす必要がある
  - 対象ユーザーの直属の上長である
  - 作業実績更新権限（PERM_UPDATE_WORK_RECORDS）を持っている
  - 管理者権限（ROLE_ADMIN）を持っている
  - プロジェクト管理者として登録されている（project_managersテーブルに登録あり）
- 承認/却下操作には以下のいずれかの条件を満たす必要がある
  - 対象ユーザーの直属の上長である
  - 作業実績承認権限（PERM_APPROVE_WORK_RECORDS）を持っている
  - 管理者権限（ROLE_ADMIN）を持っている
  - プロジェクト管理者として登録されている（project_managersテーブルに登録あり）

### 4.3 ステータス遷移ルール

| 現在のステータス | 変更可能なステータス | 備考 |
|----------------|-------------------|------|
| draft | draft, submitted | 作成者のみ可能 |
| submitted | draft, submitted, approved, rejected | draft, submittedは作成者のみ可能<br>approved, rejectedは承認者のみ可能 |
| approved | approved | 変更不可（固定） |
| rejected | draft, submitted, rejected | draft, submittedは作成者のみ可能<br>rejectedは承認者のみ可能 |

### 4.4 日付の扱い

- 日付はISO 8601形式（YYYY-MM-DD）で指定
- 未来日の指定は不可
- 過去日の指定は可能だが、締め切り済み期間（通常、月次締め後）は更新不可

### 4.5 作業時間の扱い

- 作業時間は0.5時間単位で指定（例: 0.5, 1.0, 1.5, ...）
- 最小値は0.5時間、最大値は24.0時間
- 1日の合計作業時間が24時間を超える場合はエラー

### 4.6 承認/却下処理

- 承認/却下時にはレビューコメントが必須
- 承認/却下操作は承認権限を持つユーザーのみ可能
- 承認/却下時には通知が自動的に送信される
- 承認済み実績は更新不可（固定）
- 却下された実績は作成者が修正して再提出可能

### 4.7 添付ファイルの扱い

- 添付ファイルは事前にファイルアップロードAPI（API-051）でアップロードし、取得したファイルIDを指定
- ファイルIDの存在チェックと、そのファイルへのアクセス権限チェックを実施
- 更新時は既存の添付ファイル情報を全て削除し、リクエストで指定された添付ファイル情報を再登録

### 4.8 関連スキルの扱い

- 関連スキルはスキルマスタに存在するスキルIDを指定
- 使用レベルは1-5の範囲で指定（1: 初級、5: 上級）
- 更新時は既存の関連スキル情報を全て削除し、リクエストで指定された関連スキル情報を再登録

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-041](API仕様書_API-041.md) | 作業実績取得API | 作業実績情報取得 |
| [API-042](API仕様書_API-042.md) | 作業実績登録API | 作業実績情報登録 |
| [API-051](API仕様書_API-051.md) | ファイルアップロードAPI | ファイルアップロード |
| [API-101](API仕様書_API-101.md) | 一括登録検証API | 一括登録データ検証 |
| [API-102](API仕様書_API-102.md) | 一括登録実行API | 一括登録実行 |
| [API-201](API仕様書_API-201.md) | 通知一覧取得API | 通知一覧取得 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| work_records | 作業実績情報 | 更新（U） |
| work_record_details | 作業実績詳細情報 | 更新（U） |
| work_record_skills | 作業実績関連スキル | 削除・作成（DC） |
| work_record_attachments | 作業実績添付ファイル | 削除・作成（DC） |
| work_record_reviews | 作業実績レビュー情報 | 作成（C） |
| projects | プロジェクト情報 | 参照（R） |
| project_managers | プロジェクト管理者情報 | 参照（R） |
| work_categories | 作業カテゴリ情報 | 参照（R） |
| skill_masters | スキルマスタ | 参照（R） |
| files | ファイル情報 | 参照（R） |
| period_locks | 期間ロック情報 | 参照（R） |
| notifications | 通知情報 | 作成（C） |

### 5.3 注意事項・補足

- 作業実績は0.5時間単位で記録
- 1日の作業時間合計が24時間を超える場合はエラー
- 同一日・プロジェクト・カテゴリの作業実績が既に存在する場合は重複エラー（自身の実績は除く）
- 締め切り済み期間（通常、月次締め後）への更新は不可
- 添付ファイルは事前にファイルアップロードAPIでアップロードし、取得したファイルIDを指定
- ステータスが変更された場合、関係者への通知が自動的に送信される
- 承認済み実績は更新不可（固定）
- 却下された実績は作成者が修正して再提出可能
- 関連スキルの使用は、スキル習熟度の評価や推移分析に利用される
- 承認/却下時にはレビューコメントが必須

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import { useForm, Controller, useFieldArray } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import {
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  FormHelperText,
  Grid,
  Typography,
  Paper,
  Divider,
  Box,
  Chip,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Snackbar,
  Alert,
  Rating,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { Add as AddIcon, Delete as DeleteIcon, CloudUpload as CloudUploadIcon } from '@mui/icons-material';

// バリデーションスキーマ（一般ユーザー用）
const userUpdateSchema = yup.object().shape({
  date: yup.date()
    .required('作業日は必須です')
    .max(new Date(), '未来の日付は指定できません'),
  project_id: yup.string()
    .required('プロジェクトは必須です'),
  category: yup.string()
    .required('作業カテゴリは必須です'),
  task: yup.string()
    .required('作業内容は必須です')
    .max(100, '作業内容は100文字以内で入力してください'),
  hours: yup.number()
    .required('作業時間は必須です')
    .min(0.5, '作業時間は0.5時間以上で入力してください')
    .max(24, '作業時間は24時間以内で入力してください')
    .test(
      'is-half-hour',
      '作業時間は0.5時間単位で入力してください',
      value => value !== undefined && (value * 2) % 1 === 0
    ),
  status: yup.string()
    .required('ステータスは必須です')
    .oneOf(['draft', 'submitted'], '無効なステータスです'),
  details: yup.object().shape({
    description: yup.string()
      .max(1000, '詳細説明は1000文字以内で入力してください'),
    achievements: yup.string()
      .max(1000, '成果物・達成事項は1000文
