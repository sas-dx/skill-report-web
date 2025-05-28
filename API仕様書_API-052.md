# API仕様書：API-052 研修記録登録API

## 1. 基本情報

- **API ID**: API-052
- **API名称**: 研修記録登録API
- **概要**: ユーザーの研修記録情報を新規登録する
- **エンドポイント**: `/api/trainings/{user_id}`
- **HTTPメソッド**: POST
- **リクエスト形式**: JSON
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-TRAINING](画面設計書_SCR-TRAINING.md)
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

### 2.3 リクエストボディ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| name | string | ○ | 研修名 | 最大100文字 |
| category | string | ○ | 研修カテゴリ | "technical", "business", "management", "compliance", "other" |
| description | string | ○ | 研修内容 | 最大1000文字 |
| start_date | string | ○ | 開始日 | ISO 8601形式（YYYY-MM-DD） |
| end_date | string | ○ | 終了日 | ISO 8601形式（YYYY-MM-DD） |
| duration_hours | number | ○ | 研修時間（時間） | 0.5単位、0.5〜240.0の範囲 |
| location | string | ○ | 実施場所 | 最大100文字 |
| format | string | ○ | 実施形式 | "online", "offline", "hybrid" |
| provider | string | ○ | 提供元 | 最大100文字 |
| status | string | ○ | 受講状態 | "planned", "completed", "cancelled" |
| completion_date | string | - | 修了日 | ISO 8601形式（YYYY-MM-DD）<br>status="completed"の場合のみ有効 |
| score | number | - | 評価点数 | 0-100<br>status="completed"の場合のみ有効 |
| certificate | object | - | 修了証情報 | status="completed"の場合のみ有効 |
| feedback | string | - | フィードバック | 最大1000文字<br>status="completed"の場合のみ有効 |
| related_skills | array | - | 関連スキル | |
| attachments | array | - | 添付ファイル | |

#### certificate オブジェクト

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| certificate_id | string | ○ | 修了証ID | |
| issue_date | string | ○ | 発行日 | ISO 8601形式（YYYY-MM-DD） |
| expiry_date | string | - | 有効期限 | ISO 8601形式（YYYY-MM-DD） |
| file_id | string | - | ファイルID | 事前にファイルアップロードAPIで取得したID |

#### related_skills 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| skill_id | string | ○ | スキルID | |
| level | number | ○ | スキルレベル | 1-5（5が最高） |

#### attachments 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| file_id | string | ○ | ファイルID | 事前にファイルアップロードAPIで取得したID |

### 2.4 リクエスト例（計画中の研修）

```json
{
  "name": "クラウドセキュリティ基礎",
  "category": "technical",
  "description": "クラウド環境におけるセキュリティ対策の基礎を学ぶ研修",
  "start_date": "2025-06-15",
  "end_date": "2025-06-17",
  "duration_hours": 18,
  "location": "オンライン",
  "format": "online",
  "provider": "AWS Japan",
  "status": "planned",
  "related_skills": [
    {
      "skill_id": "S103",
      "level": 3
    },
    {
      "skill_id": "S104",
      "level": 2
    }
  ],
  "attachments": []
}
```

### 2.5 リクエスト例（完了した研修）

```json
{
  "name": "アジャイル開発実践",
  "category": "management",
  "description": "スクラム手法を用いたアジャイル開発の実践的な手法を学ぶ研修",
  "start_date": "2025-05-10",
  "end_date": "2025-05-12",
  "duration_hours": 24,
  "location": "本社会議室",
  "format": "offline",
  "provider": "アジャイルコーチング株式会社",
  "status": "completed",
  "completion_date": "2025-05-12",
  "score": 88,
  "certificate": {
    "certificate_id": "CERT-AGILE-789012",
    "issue_date": "2025-05-13",
    "expiry_date": "2028-05-12",
    "file_id": "F003"
  },
  "feedback": "実践的な演習が多く、チーム開発におけるアジャイル手法の適用方法を具体的に学ぶことができた。特にスプリントプランニングとレトロスペクティブの進め方が参考になった。",
  "related_skills": [
    {
      "skill_id": "S301",
      "level": 4
    },
    {
      "skill_id": "S302",
      "level": 3
    }
  ],
  "attachments": [
    {
      "file_id": "F003"
    },
    {
      "file_id": "F004"
    }
  ]
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（201 Created）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| training_id | string | 作成された研修ID | |
| user_id | string | ユーザーID | |
| name | string | 研修名 | |
| category | string | 研修カテゴリ | "technical", "business", "management", "compliance", "other" |
| description | string | 研修内容 | |
| start_date | string | 開始日 | ISO 8601形式（YYYY-MM-DD） |
| end_date | string | 終了日 | ISO 8601形式（YYYY-MM-DD） |
| duration_hours | number | 研修時間（時間） | |
| location | string | 実施場所 | |
| format | string | 実施形式 | "online", "offline", "hybrid" |
| provider | string | 提供元 | |
| status | string | 受講状態 | "planned", "completed", "cancelled" |
| completion_date | string | 修了日 | ISO 8601形式（YYYY-MM-DD）<br>status="completed"の場合のみ |
| score | number | 評価点数 | 0-100<br>status="completed"の場合のみ |
| certificate | object | 修了証情報 | status="completed"の場合のみ |
| feedback | string | フィードバック | status="completed"の場合のみ |
| related_skills | array | 関連スキル | |
| attachments | array | 添付ファイル | |
| created_at | string | 作成日時 | ISO 8601形式 |
| created_by | string | 作成者ID | |

#### certificate オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| certificate_id | string | 修了証ID | |
| issue_date | string | 発行日 | ISO 8601形式（YYYY-MM-DD） |
| expiry_date | string | 有効期限 | ISO 8601形式（YYYY-MM-DD） |
| file_id | string | ファイルID | |

#### related_skills 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| name | string | スキル名 | |
| category | string | スキルカテゴリ | |
| level | number | スキルレベル | 1-5（5が最高） |

#### attachments 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| file_id | string | ファイルID | |
| file_name | string | ファイル名 | |
| file_type | string | ファイルタイプ | |
| file_size | number | ファイルサイズ（バイト） | |
| upload_date | string | アップロード日時 | ISO 8601形式 |

### 3.2 正常時レスポンス例

```json
{
  "training_id": "TR003",
  "user_id": "U12345",
  "name": "アジャイル開発実践",
  "category": "management",
  "description": "スクラム手法を用いたアジャイル開発の実践的な手法を学ぶ研修",
  "start_date": "2025-05-10",
  "end_date": "2025-05-12",
  "duration_hours": 24,
  "location": "本社会議室",
  "format": "offline",
  "provider": "アジャイルコーチング株式会社",
  "status": "completed",
  "completion_date": "2025-05-12",
  "score": 88,
  "certificate": {
    "certificate_id": "CERT-AGILE-789012",
    "issue_date": "2025-05-13",
    "expiry_date": "2028-05-12",
    "file_id": "F003"
  },
  "feedback": "実践的な演習が多く、チーム開発におけるアジャイル手法の適用方法を具体的に学ぶことができた。特にスプリントプランニングとレトロスペクティブの進め方が参考になった。",
  "related_skills": [
    {
      "skill_id": "S301",
      "name": "アジャイル開発",
      "category": "management",
      "level": 4
    },
    {
      "skill_id": "S302",
      "name": "スクラム",
      "category": "management",
      "level": 3
    }
  ],
  "attachments": [
    {
      "file_id": "F003",
      "file_name": "agile_certificate.pdf",
      "file_type": "application/pdf",
      "file_size": 345678,
      "upload_date": "2025-05-13T10:30:00+09:00"
    },
    {
      "file_id": "F004",
      "file_name": "agile_training_materials.zip",
      "file_type": "application/zip",
      "file_size": 2345678,
      "upload_date": "2025-05-13T10:35:00+09:00"
    }
  ],
  "created_at": "2025-05-13T10:45:00+09:00",
  "created_by": "U12345"
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_DATE | 日付が不正です | 不正な日付形式 |
| 400 Bad Request | INVALID_DATE_RANGE | 日付範囲が不正です | 開始日が終了日より後の日付 |
| 400 Bad Request | INVALID_CATEGORY | カテゴリが不正です | 存在しないカテゴリ |
| 400 Bad Request | INVALID_FORMAT | 実施形式が不正です | 存在しない実施形式 |
| 400 Bad Request | INVALID_STATUS | 受講状態が不正です | 存在しない受講状態 |
| 400 Bad Request | INVALID_DURATION | 研修時間が不正です | 0.5単位でない、または範囲外 |
| 400 Bad Request | INVALID_SCORE | 評価点数が不正です | 0-100の範囲外 |
| 400 Bad Request | INVALID_SKILL_ID | スキルIDが不正です | 存在しないスキルID |
| 400 Bad Request | INVALID_SKILL_LEVEL | スキルレベルが不正です | 1-5の範囲外 |
| 400 Bad Request | INVALID_FILE_ID | ファイルIDが不正です | 存在しないファイルID |
| 400 Bad Request | MISSING_COMPLETION_INFO | 修了情報が不足しています | 完了状態なのに修了日が未指定 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他ユーザーの情報登録権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_DATE_RANGE",
    "message": "日付範囲が不正です",
    "details": "開始日は終了日以前の日付を指定してください"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - ユーザーIDの権限チェック（自身または部下のIDかどうか）
2. リクエストパラメータの検証
   - ユーザーIDの存在チェック
   - 必須パラメータの存在チェック
   - 各パラメータの形式・値の妥当性チェック
   - 日付範囲の妥当性チェック（開始日 ≤ 終了日）
   - 受講状態に応じた必須パラメータの存在チェック
   - 関連スキル・添付ファイルの妥当性チェック
3. 研修記録情報の登録
   - trainings テーブルに基本情報を登録
   - training_details テーブルに詳細情報を登録
   - training_skills テーブルに関連スキル情報を登録
   - training_attachments テーブルに添付ファイル情報を登録
   - training_certificates テーブルに修了証情報を登録（該当する場合）
4. レスポンスの生成
   - 登録結果を整形
5. レスポンス返却

### 4.2 権限チェック

- 自身の研修記録は常に登録可能
- 他ユーザーの研修記録登録には以下のいずれかの条件を満たす必要がある
  - 対象ユーザーの直属の上長である
  - 研修記録登録権限（PERM_CREATE_TRAINING_RECORDS）を持っている
  - 管理者権限（ROLE_ADMIN）を持っている
  - 研修管理者として登録されている（training_managersテーブルに登録あり）

### 4.3 日付の扱い

- 日付はISO 8601形式（YYYY-MM-DD）で指定
- 開始日は終了日以前の日付である必要がある
- 修了日は開始日以降、終了日以降の日付である必要がある

### 4.4 受講状態による必須パラメータ

- 受講状態が "completed"（完了）の場合
  - completion_date（修了日）が必須
  - score（評価点数）は任意
  - certificate（修了証情報）は任意
  - feedback（フィードバック）は任意
- 受講状態が "planned"（計画中）または "cancelled"（キャンセル）の場合
  - completion_date, score, certificate, feedbackは無視される

### 4.5 研修時間の扱い

- 研修時間は0.5時間単位で指定（例: 0.5, 1.0, 1.5, ...）
- 最小値は0.5時間、最大値は240.0時間（10日間相当）

### 4.6 添付ファイルの扱い

- 添付ファイルは事前にファイルアップロードAPI（API-051）でアップロードし、取得したファイルIDを指定
- ファイルIDの存在チェックと、そのファイルへのアクセス権限チェックを実施

### 4.7 関連スキルの扱い

- 関連スキルはスキルマスタに存在するスキルIDを指定
- スキルレベルは1-5の範囲で指定（1: 初級、5: 上級）
- 関連スキルは、研修を通じて習得または向上したスキルを表す

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-051](API仕様書_API-051.md) | 研修記録取得API | 研修記録情報取得 |
| [API-053](API仕様書_API-053.md) | 資格情報取得API | 資格情報取得 |
| [API-054](API仕様書_API-054.md) | 資格情報更新API | 資格情報更新 |
| [API-061](API仕様書_API-061.md) | レポート生成API | 研修レポート生成 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| trainings | 研修記録情報 | 作成（C） |
| training_details | 研修記録詳細情報 | 作成（C） |
| training_skills | 研修記録関連スキル | 作成（C） |
| training_attachments | 研修記録添付ファイル | 作成（C） |
| training_certificates | 研修修了証情報 | 作成（C） |
| training_managers | 研修管理者情報 | 参照（R） |
| skill_masters | スキルマスタ | 参照（R） |
| files | ファイル情報 | 参照（R） |

### 5.3 注意事項・補足

- 研修記録は、計画中（planned）、完了（completed）、キャンセル（cancelled）の3つの状態で管理
- 完了状態の研修のみ、修了日、評価点数、修了証情報、フィードバックが設定可能
- 関連スキルは、研修を通じて習得または向上したスキルを表す
- 添付ファイルには、修了証、研修資料、成果物などを登録可能
- 研修カテゴリは、技術（technical）、ビジネス（business）、マネジメント（management）、コンプライアンス（compliance）、その他（other）の5種類
- 実施形式は、オンライン（online）、オフライン（offline）、ハイブリッド（hybrid）の3種類
- 研修記録の登録時に、関連するスキル情報の自動更新は行わない（別途スキル情報更新APIを使用）

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState } from 'react';
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
  Switch,
  FormControlLabel
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { Add as AddIcon, Delete as DeleteIcon, CloudUpload as CloudUploadIcon } from '@mui/icons-material';

// バリデーションスキーマ
const schema = yup.object().shape({
  name: yup.string()
    .required('研修名は必須です')
    .max(100, '研修名は100文字以内で入力してください'),
  category: yup.string()
    .required('カテゴリは必須です')
    .oneOf(['technical', 'business', 'management', 'compliance', 'other'], '無効なカテゴリです'),
  description: yup.string()
    .required('研修内容は必須です')
    .max(1000, '研修内容は1000文字以内で入力してください'),
  start_date: yup.date()
    .required('開始日は必須です'),
  end_date: yup.date()
    .required('終了日は必須です')
    .min(yup.ref('start_date'), '終了日は開始日以降の日付を指定してください'),
  duration_hours: yup.number()
    .required('研修時間は必須です')
    .min(0.5, '研修時間は0.5時間以上で入力してください')
    .max(240, '研修時間は240時間以内で入力してください')
    .test(
      'is-half-hour',
      '研修時間は0.5時間単位で入力してください',
      value => value !== undefined && (value * 2) % 1 === 0
    ),
  location: yup.string()
    .required('実施場所は必須です')
    .max(100, '実施場所は100文字以内で入力してください'),
  format: yup.string()
    .required('実施形式は必須です')
    .oneOf(['online', 'offline', 'hybrid'], '無効な実施形式です'),
  provider: yup.string()
    .required('提供元は必須です')
    .max(100, '提供元は100文字以内で入力してください'),
  status: yup.string()
    .required('受講状態は必須です')
    .oneOf(['planned', 'completed', 'cancelled'], '無効な受講状態です'),
  completion_date: yup.date()
    .nullable()
    .when('status', {
      is: 'completed',
      then: yup.date().required('修了日は必須です').min(yup.ref('start_date'), '修了日は開始日以降の日付を指定してください')
    }),
  score: yup.number()
    .nullable()
    .when('status', {
      is: 'completed',
      then: yup.number().min(0, '評価点数は0以上で入力してください').max(100, '評価点数は100以下で入力してください')
    }),
  certificate: yup.object().shape({
    certificate_id: yup.string().when('../status', {
      is: 'completed',
      then: yup.string()
    }),
    issue_date: yup.date().when('../status', {
      is: 'completed',
      then: yup.date()
    }),
    expiry_date: yup.date().nullable(),
    file_id: yup.string().nullable()
  }).nullable(),
  feedback: yup.string()
    .nullable()
    .when('status', {
      is: 'completed',
      then: yup.string().max(1000, 'フィードバックは1000文字以内で入力してください')
    }),
  related_skills: yup.array().of(
    yup.object().shape({
      skill_id: yup.string()
        .required('スキルIDは必須です'),
      level: yup.number()
        .required('スキルレベルは必須です')
        .min(1, 'スキルレベルは1以上で入力してください')
        .max(5, 'スキルレベルは5以下で入力してください')
        .integer('スキルレベルは整数で入力してください')
    })
  ),
  attachments: yup.array().of(
    yup.object().shape({
      file_id: yup.string()
        .required('ファイルIDは必須です')
    })
  )
});

// 型定義
interface TrainingFormData {
  name: string;
  category: string;
  description: string;
  start_date: Date;
  end_date: Date;
  duration_hours: number;
  location: string;
  format: string;
  provider: string;
  status: string;
  completion_date?: Date | null;
  score?: number | null;
  certificate?: {
    certificate_id: string;
    issue_date: Date;
    expiry_date?: Date | null;
    file_id?: string | null;
  } | null;
  feedback?: string | null;
  related_skills: Array<{
    skill_id: string;
    level: number;
  }>;
  attachments: Array<{
    file_id: string;
  }>;
}

interface Skill {
  id: string;
  name: string;
  category: string;
}

interface UploadedFile {
  file_id: string;
  file_name: string;
  file_type: string;
  file_size: number;
  upload_date: string;
}

const TrainingRecordCreateForm: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean>(false);
  
  // スキル一覧（実際の実装ではAPIから取得）
  const [skills, setSkills] = useState<Skill[]>([
    { id: 'S101', name: 'AWS', category: 'technical' },
    { id: 'S102', name: 'クラウドアーキテクチャ', category: 'technical' },
    { id: 'S103', name: 'クラウドセキュリティ', category: 'technical' },
    { id: 'S104', name: 'ネットワークセキュリティ
