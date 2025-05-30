# API定義書：API-042 作業実績登録API

## 1. 基本情報

- **API ID**: API-042
- **API名称**: 作業実績登録API
- **概要**: ユーザーの作業実績情報を新規登録する
- **エンドポイント**: `/api/work-records/{user_id}`
- **HTTPメソッド**: POST
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

### 2.3 リクエストボディ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| date | string | ○ | 作業日 | ISO 8601形式（YYYY-MM-DD） |
| project_id | string | ○ | プロジェクトID | |
| category | string | ○ | 作業カテゴリ | |
| task | string | ○ | 作業内容 | 最大100文字 |
| hours | number | ○ | 作業時間（時間） | 0.5単位、0.5〜24.0の範囲 |
| status | string | ○ | ステータス | "draft", "submitted" |
| details | object | - | 詳細情報 | |

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

### 2.4 リクエスト例

```json
{
  "date": "2025-05-28",
  "project_id": "P001",
  "category": "開発",
  "task": "APIドキュメント作成",
  "hours": 4.5,
  "status": "submitted",
  "details": {
    "description": "作業実績登録APIのドキュメントを作成",
    "achievements": "API仕様書の初版を完成させた",
    "issues": "他APIとの整合性確認が必要",
    "next_actions": "レビュー後に修正対応予定",
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
      }
    ]
  }
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（201 Created）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| record_id | string | 作成された実績ID | |
| user_id | string | ユーザーID | |
| date | string | 作業日 | ISO 8601形式（YYYY-MM-DD） |
| project_id | string | プロジェクトID | |
| project_name | string | プロジェクト名 | |
| category | string | 作業カテゴリ | |
| task | string | 作業内容 | |
| hours | number | 作業時間（時間） | |
| status | string | ステータス | "draft", "submitted" |
| details | object | 詳細情報 | |
| created_at | string | 作成日時 | ISO 8601形式 |
| created_by | string | 作成者ID | |

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

### 3.2 正常時レスポンス例

```json
{
  "record_id": "WR003",
  "user_id": "U12345",
  "date": "2025-05-28",
  "project_id": "P001",
  "project_name": "スキルレポートWEB化PJT",
  "category": "開発",
  "task": "APIドキュメント作成",
  "hours": 4.5,
  "status": "submitted",
  "details": {
    "description": "作業実績登録APIのドキュメントを作成",
    "achievements": "API仕様書の初版を完成させた",
    "issues": "他APIとの整合性確認が必要",
    "next_actions": "レビュー後に修正対応予定",
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
      }
    ]
  },
  "created_at": "2025-05-28T15:45:00+09:00",
  "created_by": "U12345"
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_DATE | 日付が不正です | 不正な日付形式 |
| 400 Bad Request | FUTURE_DATE | 未来の日付は指定できません | 未来日の指定 |
| 400 Bad Request | INVALID_PROJECT_ID | プロジェクトIDが不正です | 存在しないプロジェクトID |
| 400 Bad Request | INVALID_CATEGORY | カテゴリが不正です | 存在しないカテゴリ |
| 400 Bad Request | INVALID_HOURS | 作業時間が不正です | 0.5単位でない、または範囲外 |
| 400 Bad Request | INVALID_STATUS | ステータスが不正です | 存在しないステータス |
| 400 Bad Request | INVALID_SKILL_ID | スキルIDが不正です | 存在しないスキルID |
| 400 Bad Request | INVALID_SKILL_LEVEL | スキルレベルが不正です | 1-5の範囲外 |
| 400 Bad Request | INVALID_FILE_ID | ファイルIDが不正です | 存在しないファイルID |
| 400 Bad Request | DUPLICATE_RECORD | 重複する作業実績があります | 同一日・プロジェクト・カテゴリの実績が存在 |
| 400 Bad Request | DAILY_HOURS_EXCEEDED | 1日の作業時間上限を超えています | 1日の合計作業時間が24時間を超過 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他ユーザーの情報登録権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 409 Conflict | LOCKED_PERIOD | ロックされた期間です | 締め切り済み期間への登録 |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "DAILY_HOURS_EXCEEDED",
    "message": "1日の作業時間上限を超えています",
    "details": "2025-05-28の合計作業時間が24時間を超えています。現在の合計: 20.5時間、追加しようとした時間: 4.5時間"
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
   - 日付の妥当性チェック（未来日でないこと）
   - プロジェクトID・カテゴリの存在チェック
   - 作業時間の妥当性チェック（0.5単位、範囲内）
   - ステータスの妥当性チェック
   - 関連スキル・添付ファイルの妥当性チェック
3. 重複チェック
   - 同一日・プロジェクト・カテゴリの作業実績が既に存在しないか確認
4. 日次作業時間チェック
   - 指定された日付の合計作業時間が24時間を超えないか確認
5. 期間ロックチェック
   - 指定された日付が締め切り済み期間でないか確認
6. 作業実績情報の登録
   - work_records テーブルに基本情報を登録
   - work_record_details テーブルに詳細情報を登録
   - work_record_skills テーブルに関連スキル情報を登録
   - work_record_attachments テーブルに添付ファイル情報を登録
7. レスポンスの生成
   - 登録結果を整形
8. レスポンス返却

### 4.2 権限チェック

- 自身の作業実績は常に登録可能
- 他ユーザーの作業実績登録には以下のいずれかの条件を満たす必要がある
  - 対象ユーザーの直属の上長である
  - 作業実績登録権限（PERM_CREATE_WORK_RECORDS）を持っている
  - 管理者権限（ROLE_ADMIN）を持っている
  - プロジェクト管理者として登録されている（project_managersテーブルに登録あり）

### 4.3 日付の扱い

- 日付はISO 8601形式（YYYY-MM-DD）で指定
- 未来日の指定は不可
- 過去日の指定は可能だが、締め切り済み期間（通常、月次締め後）は登録不可

### 4.4 作業時間の扱い

- 作業時間は0.5時間単位で指定（例: 0.5, 1.0, 1.5, ...）
- 最小値は0.5時間、最大値は24.0時間
- 1日の合計作業時間が24時間を超える場合はエラー

### 4.5 ステータスの扱い

- 登録時のステータスは "draft"（下書き）または "submitted"（提出済み）のみ指定可能
- "approved"（承認済み）または "rejected"（却下）は承認者のみが設定可能（API-043で対応）

### 4.6 添付ファイルの扱い

- 添付ファイルは事前にファイルアップロードAPI（API-051）でアップロードし、取得したファイルIDを指定
- ファイルIDの存在チェックと、そのファイルへのアクセス権限チェックを実施

### 4.7 関連スキルの扱い

- 関連スキルはスキルマスタに存在するスキルIDを指定
- 使用レベルは1-5の範囲で指定（1: 初級、5: 上級）

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-041](API仕様書_API-041.md) | 作業実績取得API | 作業実績情報取得 |
| [API-043](API仕様書_API-043.md) | 作業実績更新API | 作業実績情報更新 |
| [API-051](API仕様書_API-051.md) | ファイルアップロードAPI | ファイルアップロード |
| [API-101](API仕様書_API-101.md) | 一括登録検証API | 一括登録データ検証 |
| [API-102](API仕様書_API-102.md) | 一括登録実行API | 一括登録実行 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| work_records | 作業実績情報 | 作成（C） |
| work_record_details | 作業実績詳細情報 | 作成（C） |
| work_record_skills | 作業実績関連スキル | 作成（C） |
| work_record_attachments | 作業実績添付ファイル | 作成（C） |
| projects | プロジェクト情報 | 参照（R） |
| project_managers | プロジェクト管理者情報 | 参照（R） |
| work_categories | 作業カテゴリ情報 | 参照（R） |
| skill_masters | スキルマスタ | 参照（R） |
| files | ファイル情報 | 参照（R） |
| period_locks | 期間ロック情報 | 参照（R） |

### 5.3 注意事項・補足

- 作業実績は0.5時間単位で記録
- 1日の作業時間合計が24時間を超える場合はエラー
- 同一日・プロジェクト・カテゴリの作業実績が既に存在する場合は重複エラー
- 締め切り済み期間（通常、月次締め後）への登録は不可
- 添付ファイルは事前にファイルアップロードAPIでアップロードし、取得したファイルIDを指定
- ステータスが "submitted"（提出済み）の場合、上長への通知が自動的に送信される
- 関連スキルの使用は、スキル習熟度の評価や推移分析に利用される

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
  Rating
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { Add as AddIcon, Delete as DeleteIcon, CloudUpload as CloudUploadIcon } from '@mui/icons-material';

// バリデーションスキーマ
const schema = yup.object().shape({
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
      .max(1000, '成果物・達成事項は1000文字以内で入力してください'),
    issues: yup.string()
      .max(1000, '課題・問題点は1000文字以内で入力してください'),
    next_actions: yup.string()
      .max(1000, '次のアクションは1000文字以内で入力してください'),
    related_skills: yup.array().of(
      yup.object().shape({
        skill_id: yup.string()
          .required('スキルIDは必須です'),
        level_used: yup.number()
          .required('使用レベルは必須です')
          .min(1, '使用レベルは1以上で入力してください')
          .max(5, '使用レベルは5以下で入力してください')
          .integer('使用レベルは整数で入力してください')
      })
    ),
    attachments: yup.array().of(
      yup.object().shape({
        file_id: yup.string()
          .required('ファイルIDは必須です')
      })
    )
  })
});

// 型定義
interface WorkRecordFormData {
  date: Date;
  project_id: string;
  category: string;
  task: string;
  hours: number;
  status: 'draft' | 'submitted';
  details?: {
    description?: string;
    achievements?: string;
    issues?: string;
    next_actions?: string;
    related_skills?: Array<{
      skill_id: string;
      level_used: number;
    }>;
    attachments?: Array<{
      file_id: string;
    }>;
  };
}

interface Project {
  id: string;
  name: string;
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

const WorkRecordCreateForm: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean>(false);
  
  // プロジェクト一覧（実際の実装ではAPIから取得）
  const [projects, setProjects] = useState<Project[]>([]);
  
  // カテゴリ一覧（実際の実装ではAPIから取得）
  const [categories, setCategories] = useState<string[]>([]);
  
  // スキル一覧（実際の実装ではAPIから取得）
  const [skills, setSkills] = useState<Skill[]>([]);
  
  // アップロード済みファイル一覧
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  
  // React Hook Formの設定
  const { control, handleSubmit, watch, setValue, formState: { errors } } = useForm<WorkRecordFormData>({
    resolver: yupResolver(schema),
    defaultValues: {
      date: new Date(),
      status: 'draft',
      hours: 1,
      details: {
        related_skills: [],
        attachments: []
      }
    }
  });
  
  // 関連スキルのフィールド配列
  const { fields: skillFields, append: appendSkill, remove: removeSkill } = useFieldArray({
    control,
    name: 'details.related_skills'
  });
  
  // 添付ファイルのフィールド配列
  const { fields: attachmentFields, append: appendAttachment, remove: removeAttachment } = useFieldArray({
    control,
    name: 'details.attachments'
  });
  
  useEffect(() => {
    // プロジェクト一覧、カテゴリ一覧、スキル一覧の取得（実際の実装ではAPIから取得）
    setProjects([
      { id: 'P001', name: 'スキルレポートWEB化PJT' },
      { id: 'P002', name: '社内研修' }
    ]);
    
    setCategories(['開発', '設計', '会議', 'レビュー', '調査', 'その他']);
    
    setSkills([
      { id: 'S007', name: 'React', category: 'technical' },
      { id: 'S008', name: 'TypeScript', category: 'technical' },
      { id: 'S020', name: 'API設計', category: 'technical' },
      { id: 'S021', name: 'ドキュメント作成', category: 'technical' }
    ]);
  }, []);
  
  // ファイルアップロード処理（実際の実装ではファイルアップロードAPIを使用）
  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;
    
    try {
      setLoading(true);
      
      // 実際の実装ではファイルアップロードAPIを呼び出す
      // ここではモックデータを使用
      const mockUploadedFile: UploadedFile = {
        file_id: `F${Math.floor(Math.random() * 1000)}`,
        file_name: files[0].name,
        file_type: files[0].type,
        file_size: files[0].size,
        upload_date: new Date().toISOString()
      };
      
      setUploadedFiles([...uploadedFiles, mockUploadedFile]);
      appendAttachment({ file_id: mockUploadedFile.file_id });
      
    } catch (err) {
      setError('ファイルのアップロードに失敗しました');
    } finally {
      setLoading(false);
    }
  };
  
  // フォーム送信処理
  const onSubmit = async (data: WorkRecordFormData) => {
    try {
      setLoading(true);
      setError(null);
      
      // 日付をISO 8601形式（YYYY-MM-DD）に変換
      const formattedDate = data.date.toISOString().split('T')[0];
      
      // リクエストデータの構築
      const requestData = {
        ...data,
        date: formattedDate
      };
      
      // APIリクエスト
      const response = await axios.post(
        `/api/work-records/${userId}`,
        requestData,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      setSuccess(true);
      
      // 登録成功後、作業実績一覧画面に遷移
      setTimeout(() => {
        navigate(`/work-records/${userId}`);
      }, 2000);
      
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const errorData = err.response.data;
        setError(errorData.error?.message || '作業実績の登録に失敗しました');
      } else {
        setError('作業実績の登録中にエラーが発生しました');
      }
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
      <Typography variant="h5" component="h1" gutterBottom>
        作業実績登録
      </Typography>
      <Divider sx={{ mb: 3 }} />
      
      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid container spacing={3}>
          {/* 基本情報 */}
          <Grid item xs={12}>
            <Typography variant="h6" gutterBottom>
              基本情報
            </Typography>
          </Grid>
          
          {/* 作業日 */}
          <Grid item xs={12} sm={6}>
            <Controller
              name="date"
