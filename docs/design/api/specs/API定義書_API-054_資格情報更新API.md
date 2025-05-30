# API定義書：API-054 資格情報更新API

## 1. 基本情報

- **API ID**: API-054
- **API名称**: 資格情報更新API
- **概要**: ユーザーの資格情報を新規登録または更新する
- **エンドポイント**: `/api/certifications/{user_id}`
- **HTTPメソッド**: PUT
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
| certification_id | string | - | 資格ID | 更新時は必須、新規登録時は不要 |
| name | string | ○ | 資格名 | 最大100文字 |
| category | string | ○ | 資格カテゴリ | "technical", "business", "management", "language", "other" |
| issuing_organization | string | ○ | 発行組織 | 最大100文字 |
| description | string | ○ | 資格説明 | 最大1000文字 |
| level | string | ○ | レベル | "basic", "intermediate", "advanced", "expert" |
| status | string | ○ | 取得状態 | "acquired", "expired", "planned" |
| acquisition_date | string | - | 取得日 | ISO 8601形式（YYYY-MM-DD）<br>status="acquired"または"expired"の場合は必須 |
| expiry_date | string | - | 有効期限 | ISO 8601形式（YYYY-MM-DD） |
| planned_date | string | - | 取得予定日 | ISO 8601形式（YYYY-MM-DD）<br>status="planned"の場合は必須 |
| certification_number | string | - | 認定番号 | 最大50文字<br>status="acquired"または"expired"の場合のみ有効 |
| score | number | - | 取得スコア | 0-1000の範囲<br>status="acquired"または"expired"の場合のみ有効 |
| related_skills | array | - | 関連スキル | |
| attachments | array | - | 添付ファイル | |

#### related_skills 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| skill_id | string | ○ | スキルID | |
| level | number | ○ | スキルレベル | 1-5（5が最高） |

#### attachments 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| file_id | string | ○ | ファイルID | 事前にファイルアップロードAPIで取得したID |

### 2.4 リクエスト例（新規登録）

```json
{
  "name": "Microsoft Azure Administrator Associate",
  "category": "technical",
  "issuing_organization": "Microsoft",
  "description": "Azureの管理と運用に関する知識と技術を証明する資格",
  "level": "intermediate",
  "status": "planned",
  "planned_date": "2025-09-20",
  "related_skills": [
    {
      "skill_id": "S501",
      "level": 3
    },
    {
      "skill_id": "S502",
      "level": 2
    }
  ],
  "attachments": []
}
```

### 2.5 リクエスト例（更新）

```json
{
  "certification_id": "CERT004",
  "name": "Google Cloud Professional Cloud Architect",
  "category": "technical",
  "issuing_organization": "Google Cloud",
  "description": "Google Cloudのアーキテクチャ設計に関する専門知識を証明する資格",
  "level": "advanced",
  "status": "acquired",
  "acquisition_date": "2025-08-10",
  "expiry_date": "2028-08-09",
  "certification_number": "GCP-PCA-123456",
  "score": 920,
  "related_skills": [
    {
      "skill_id": "S401",
      "level": 4
    },
    {
      "skill_id": "S402",
      "level": 3
    }
  ],
  "attachments": [
    {
      "file_id": "F008"
    },
    {
      "file_id": "F009"
    }
  ]
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| certification_id | string | 資格ID | |
| user_id | string | ユーザーID | |
| name | string | 資格名 | |
| category | string | 資格カテゴリ | "technical", "business", "management", "language", "other" |
| issuing_organization | string | 発行組織 | |
| description | string | 資格説明 | |
| level | string | レベル | "basic", "intermediate", "advanced", "expert" |
| status | string | 取得状態 | "acquired", "expired", "planned" |
| acquisition_date | string | 取得日 | ISO 8601形式（YYYY-MM-DD）<br>status="acquired"または"expired"の場合のみ |
| expiry_date | string | 有効期限 | ISO 8601形式（YYYY-MM-DD）<br>有効期限がある場合のみ |
| planned_date | string | 取得予定日 | ISO 8601形式（YYYY-MM-DD）<br>status="planned"の場合のみ |
| certification_number | string | 認定番号 | status="acquired"または"expired"の場合のみ |
| score | number | 取得スコア | status="acquired"または"expired"の場合のみ |
| related_skills | array | 関連スキル | |
| attachments | array | 添付ファイル | |
| created_at | string | 作成日時 | ISO 8601形式 |
| updated_at | string | 更新日時 | ISO 8601形式 |
| created_by | string | 作成者ID | |
| updated_by | string | 更新者ID | |

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
  "certification_id": "CERT004",
  "user_id": "U12345",
  "name": "Google Cloud Professional Cloud Architect",
  "category": "technical",
  "issuing_organization": "Google Cloud",
  "description": "Google Cloudのアーキテクチャ設計に関する専門知識を証明する資格",
  "level": "advanced",
  "status": "acquired",
  "acquisition_date": "2025-08-10",
  "expiry_date": "2028-08-09",
  "planned_date": null,
  "certification_number": "GCP-PCA-123456",
  "score": 920,
  "related_skills": [
    {
      "skill_id": "S401",
      "name": "Google Cloud Platform",
      "category": "technical",
      "level": 4
    },
    {
      "skill_id": "S402",
      "name": "クラウドアーキテクチャ",
      "category": "technical",
      "level": 3
    }
  ],
  "attachments": [
    {
      "file_id": "F008",
      "file_name": "gcp_certificate.pdf",
      "file_type": "application/pdf",
      "file_size": 456789,
      "upload_date": "2025-08-11T10:30:00+09:00"
    },
    {
      "file_id": "F009",
      "file_name": "gcp_score_report.pdf",
      "file_type": "application/pdf",
      "file_size": 234567,
      "upload_date": "2025-08-11T10:35:00+09:00"
    }
  ],
  "created_at": "2025-05-10T11:30:00+09:00",
  "updated_at": "2025-08-11T10:45:00+09:00",
  "created_by": "U12345",
  "updated_by": "U12345"
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_DATE | 日付が不正です | 不正な日付形式 |
| 400 Bad Request | INVALID_CATEGORY | カテゴリが不正です | 存在しないカテゴリ |
| 400 Bad Request | INVALID_LEVEL | レベルが不正です | 存在しないレベル |
| 400 Bad Request | INVALID_STATUS | 取得状態が不正です | 存在しない取得状態 |
| 400 Bad Request | INVALID_SCORE | 取得スコアが不正です | 0-1000の範囲外 |
| 400 Bad Request | INVALID_SKILL_ID | スキルIDが不正です | 存在しないスキルID |
| 400 Bad Request | INVALID_SKILL_LEVEL | スキルレベルが不正です | 1-5の範囲外 |
| 400 Bad Request | INVALID_FILE_ID | ファイルIDが不正です | 存在しないファイルID |
| 400 Bad Request | MISSING_ACQUISITION_INFO | 取得情報が不足しています | 取得済状態なのに取得日が未指定 |
| 400 Bad Request | MISSING_PLANNED_DATE | 取得予定日が未指定です | 取得予定状態なのに取得予定日が未指定 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他ユーザーの情報更新権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 404 Not Found | CERTIFICATION_NOT_FOUND | 資格情報が見つかりません | 指定された資格IDが存在しない |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "MISSING_ACQUISITION_INFO",
    "message": "取得情報が不足しています",
    "details": "取得済状態の場合は取得日を指定してください"
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
   - 取得状態に応じた必須パラメータの存在チェック
   - 関連スキル・添付ファイルの妥当性チェック
3. 資格情報の存在チェック
   - certification_idが指定されている場合、該当する資格情報の存在チェック
4. 資格情報の登録/更新
   - 新規登録の場合：
     - certifications テーブルに基本情報を登録
     - certification_details テーブルに詳細情報を登録
     - certification_skills テーブルに関連スキル情報を登録
     - certification_attachments テーブルに添付ファイル情報を登録
   - 更新の場合：
     - certifications テーブルの基本情報を更新
     - certification_details テーブルの詳細情報を更新
     - certification_skills テーブルの関連スキル情報を更新（既存データを削除して再登録）
     - certification_attachments テーブルの添付ファイル情報を更新（既存データを削除して再登録）
5. レスポンスの生成
   - 登録/更新結果を整形
6. レスポンス返却

### 4.2 権限チェック

- 自身の資格情報は常に登録/更新可能
- 他ユーザーの資格情報登録/更新には以下のいずれかの条件を満たす必要がある
  - 対象ユーザーの直属の上長である
  - 資格情報更新権限（PERM_UPDATE_CERTIFICATIONS）を持っている
  - 管理者権限（ROLE_ADMIN）を持っている
  - 研修管理者として登録されている（training_managersテーブルに登録あり）

### 4.3 日付の扱い

- 日付はISO 8601形式（YYYY-MM-DD）で指定
- 取得状態が "acquired"（取得済）または "expired"（期限切れ）の場合、acquisition_date（取得日）が必須
- 取得状態が "planned"（取得予定）の場合、planned_date（取得予定日）が必須

### 4.4 取得状態による必須パラメータ

- 取得状態が "acquired"（取得済）または "expired"（期限切れ）の場合
  - acquisition_date（取得日）が必須
  - certification_number（認定番号）は任意
  - score（取得スコア）は任意
  - planned_date（取得予定日）は無視される
- 取得状態が "planned"（取得予定）の場合
  - planned_date（取得予定日）が必須
  - acquisition_date, certification_number, scoreは無視される

### 4.5 添付ファイルの扱い

- 添付ファイルは事前にファイルアップロードAPI（API-051）でアップロードし、取得したファイルIDを指定
- ファイルIDの存在チェックと、そのファイルへのアクセス権限チェックを実施
- 更新時に添付ファイルを指定しない場合、既存の添付ファイル情報は削除される

### 4.6 関連スキルの扱い

- 関連スキルはスキルマスタに存在するスキルIDを指定
- スキルレベルは1-5の範囲で指定（1: 初級、5: 上級）
- 更新時に関連スキルを指定しない場合、既存の関連スキル情報は削除される

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-051](API仕様書_API-051.md) | 研修記録取得API | 研修記録情報取得 |
| [API-052](API仕様書_API-052.md) | 研修記録登録API | 研修記録情報登録 |
| [API-053](API仕様書_API-053.md) | 資格情報取得API | 資格情報取得 |
| [API-061](API仕様書_API-061.md) | レポート生成API | 資格レポート生成 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| certifications | 資格情報 | 作成/更新（CU） |
| certification_details | 資格詳細情報 | 作成/更新（CU） |
| certification_skills | 資格関連スキル | 作成/更新（CU） |
| certification_attachments | 資格添付ファイル | 作成/更新（CU） |
| training_managers | 研修管理者情報 | 参照（R） |
| skill_masters | スキルマスタ | 参照（R） |
| files | ファイル情報 | 参照（R） |

### 5.3 注意事項・補足

- 資格は、取得済（acquired）、期限切れ（expired）、取得予定（planned）の3つの状態で管理
- 取得済または期限切れの資格のみ、取得日、認定番号、取得スコアが設定可能
- 取得予定の資格のみ、取得予定日が設定可能
- 関連スキルは、資格に関連するスキルを表す
- 添付ファイルには、資格証明書、スコアレポートなどを登録可能
- 資格カテゴリは、技術（technical）、ビジネス（business）、マネジメント（management）、言語（language）、その他（other）の5種類
- レベルは、基本（basic）、中級（intermediate）、上級（advanced）、専門家（expert）の4段階
- 資格情報の登録/更新時に、関連するスキル情報の自動更新は行わない（別途スキル情報更新APIを使用）

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
  Switch,
  FormControlLabel
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { Add as AddIcon, Delete as DeleteIcon, CloudUpload as CloudUploadIcon } from '@mui/icons-material';

// バリデーションスキーマ
const schema = yup.object().shape({
  certification_id: yup.string(),
  name: yup.string()
    .required('資格名は必須です')
    .max(100, '資格名は100文字以内で入力してください'),
  category: yup.string()
    .required('カテゴリは必須です')
    .oneOf(['technical', 'business', 'management', 'language', 'other'], '無効なカテゴリです'),
  issuing_organization: yup.string()
    .required('発行組織は必須です')
    .max(100, '発行組織は100文字以内で入力してください'),
  description: yup.string()
    .required('資格説明は必須です')
    .max(1000, '資格説明は1000文字以内で入力してください'),
  level: yup.string()
    .required('レベルは必須です')
    .oneOf(['basic', 'intermediate', 'advanced', 'expert'], '無効なレベルです'),
  status: yup.string()
    .required('取得状態は必須です')
    .oneOf(['acquired', 'expired', 'planned'], '無効な取得状態です'),
  acquisition_date: yup.date()
    .nullable()
    .when('status', {
      is: (val: string) => val === 'acquired' || val === 'expired',
      then: yup.date().required('取得日は必須です')
    }),
  expiry_date: yup.date()
    .nullable(),
  planned_date: yup.date()
    .nullable()
    .when('status', {
      is: 'planned',
      then: yup.date().required('取得予定日は必須です')
    }),
  certification_number: yup.string()
    .nullable()
    .max(50, '認定番号は50文字以内で入力してください'),
  score: yup.number()
    .nullable()
    .transform((value) => (isNaN(value) ? undefined : value))
    .min(0, '取得スコアは0以上で入力してください')
    .max(1000, '取得スコアは1000以下で入力してください'),
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
interface CertificationFormData {
  certification_id?: string;
  name: string;
  category: string;
  issuing_organization: string;
  description: string;
  level: string;
  status: string;
  acquisition_date?: Date | null;
  expiry_date?: Date | null;
  planned_date?: Date | null;
  certification_number?: string | null;
  score?: number | null;
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

const CertificationForm: React.FC = () => {
  const { userId, certificationId } = useParams<{ userId: string; certificationId?: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState<boolean>(false);
  const [initialLoading, setInitialLoading] = useState<boolean>(!!certificationId);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean>(false);
  
  // スキル一覧（実際の実装ではAPIから取得）
  const [skills, setSkills] = useState<Skill[]>([
    { id: 'S101', name: 'AWS', category: 'technical' },
    { id: 'S102', name: 'クラウドアーキテクチャ', category: 'technical' },
    { id: 'S401', name: 'Google Cloud Platform', category: 'technical' },
    { id: 'S402', name: 'クラウドセキュリティ', category: 'technical' },
    { id: 'S201', name: '情報セキュリティ', category: 'technical' },
    { id: 'S202', name: 'リスク管理', category: 'management' },
    { id: 'S301', name: '英語', category: 'language' }
  ]);
  
  // アップロード済みファイル一覧（実際の実装ではAPIから取得）
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  
  // フォーム設定
  const { control, handleSubmit, watch, setValue, formState: { errors }, reset } = useForm<CertificationFormData>({
    resolver: yupResolver(schema),
    defaultValues: {
      name: '',
      category: 'technical',
      issuing_organization: '',
      description: '',
      level: 'intermediate',
      status: 'planned',
      acquisition_date: null,
      expiry_date: null,
      planned_date: null,
      certification_number: null,
      score: null,
      related_skills: [],
      attachments: []
    }
  });
  
  // 関連スキルのフィールド配列
  const { fields: skillFields, append: appendSkill, remove: removeSkill } = useFieldArray({
    control,
    name: 'related_skills'
  });
  
  // 添付ファイルのフィールド配列
  const { fields: attachmentFields, append: appendAttachment, remove: removeAttachment } = useFieldArray({
    control,
    name: 'attachments'
  });
  
  // 現在の取得状態を監視
  const currentStatus = watch('status');
  
  // 初期データの取得（更新時）
  useEffect(() => {
    if (certificationId) {
      const fetchCertification = async () => {
        try {
          setInitialLoading(true);
          const response = await axios.get(`/api/certifications/${userId}/${certificationId}`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
              'Accept': 'application/json'
            }
          });
          
          const data = response.data;
          
          // 日付文字列をDate型に変換
          const formData: CertificationFormData = {
            certification_id: data.certification_id,
            name: data.name,
            category: data.category,
            issuing_organization: data.issuing_organization,
            description: data.description,
            level: data.level,
            status: data.status,
            acquisition_date: data.acquisition_date ? new Date(data.acquisition_date) : null,
            expiry_date: data.expiry_date ? new Date(data.expiry_date) : null,
            planned_date: data.planned_date ? new Date(data.planned_date) : null,
            certification_number: data.certification_number,
            score: data.score,
            related_skills: data.related_skills.map((skill: any) => ({
              skill_id: skill.skill_id,
              level: skill.level
            })),
            attachments: data.attachments.map((attachment: any) => ({
              file_id: attachment.file_id
            }))
          };
          
          reset(formData);
          
          //
