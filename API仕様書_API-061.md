# API仕様書：API-061 レポート生成API

## 1. 基本情報

- **API ID**: API-061
- **API名称**: レポート生成API
- **概要**: 指定された条件に基づいてレポートを生成する
- **エンドポイント**: `/api/reports`
- **HTTPメソッド**: POST
- **リクエスト形式**: JSON
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-REPORT](画面設計書_SCR-REPORT.md)
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

### 2.2 リクエストボディ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| report_type | string | ○ | レポートタイプ | "skill", "training", "certification", "career", "work", "summary" |
| title | string | ○ | レポートタイトル | 最大100文字 |
| description | string | - | レポート説明 | 最大500文字 |
| target_users | array | ○ | 対象ユーザーID配列 | 最大100件 |
| period | object | - | 対象期間 | |
| filters | object | - | フィルター条件 | レポートタイプに応じた条件 |
| grouping | array | - | グループ化条件 | |
| sort | object | - | ソート条件 | |
| output_format | string | ○ | 出力形式 | "pdf", "excel", "csv", "json" |
| notification | boolean | - | 完了通知フラグ | デフォルト: false |

#### period オブジェクト

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| start_date | string | - | 開始日 | ISO 8601形式（YYYY-MM-DD） |
| end_date | string | - | 終了日 | ISO 8601形式（YYYY-MM-DD） |
| fiscal_year | number | - | 年度 | 西暦 |

#### filters オブジェクト（レポートタイプ別）

**skill レポートの場合**

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| skill_categories | array | - | スキルカテゴリ配列 | |
| skill_levels | array | - | スキルレベル配列 | 1-5の範囲 |
| skill_ids | array | - | スキルID配列 | |
| min_level | number | - | 最小レベル | 1-5の範囲 |

**training レポートの場合**

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| training_categories | array | - | 研修カテゴリ配列 | |
| training_status | array | - | 研修状態配列 | "planned", "completed", "cancelled" |
| providers | array | - | 提供元配列 | |
| min_duration | number | - | 最小研修時間 | 時間単位 |

**certification レポートの場合**

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| certification_categories | array | - | 資格カテゴリ配列 | |
| certification_levels | array | - | 資格レベル配列 | "basic", "intermediate", "advanced", "expert" |
| certification_status | array | - | 資格状態配列 | "acquired", "expired", "planned" |
| issuing_organizations | array | - | 発行組織配列 | |

**career レポートの場合**

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| goal_categories | array | - | 目標カテゴリ配列 | |
| goal_status | array | - | 目標状態配列 | "in_progress", "completed", "cancelled" |
| min_progress | number | - | 最小進捗率 | 0-100の範囲 |

**work レポートの場合**

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| work_categories | array | - | 作業カテゴリ配列 | |
| project_ids | array | - | プロジェクトID配列 | |
| min_hours | number | - | 最小作業時間 | 時間単位 |
| technologies | array | - | 使用技術配列 | |

**summary レポートの場合**

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| include_skills | boolean | - | スキル情報含むフラグ | デフォルト: true |
| include_trainings | boolean | - | 研修情報含むフラグ | デフォルト: true |
| include_certifications | boolean | - | 資格情報含むフラグ | デフォルト: true |
| include_career | boolean | - | キャリア情報含むフラグ | デフォルト: true |
| include_work | boolean | - | 作業実績含むフラグ | デフォルト: true |
| top_skills_count | number | - | 表示するトップスキル数 | デフォルト: 10 |

#### grouping 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| field | string | ○ | グループ化フィールド | "department", "position", "skill_category", "training_category", "certification_category", "year", "month", "quarter" |
| sort_order | string | - | グループ内ソート順 | "asc", "desc"<br>デフォルト: "asc" |

#### sort オブジェクト

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| field | string | ○ | ソートフィールド | レポートタイプに応じたフィールド |
| order | string | - | ソート順 | "asc", "desc"<br>デフォルト: "asc" |

### 2.3 リクエスト例（スキルレポート）

```json
{
  "report_type": "skill",
  "title": "技術スキル分布レポート",
  "description": "部門別の技術スキル分布状況",
  "target_users": ["U12345", "U12346", "U12347", "U12348", "U12349"],
  "period": {
    "fiscal_year": 2025
  },
  "filters": {
    "skill_categories": ["technical"],
    "min_level": 3
  },
  "grouping": [
    {
      "field": "department",
      "sort_order": "asc"
    },
    {
      "field": "skill_category",
      "sort_order": "desc"
    }
  ],
  "sort": {
    "field": "level",
    "order": "desc"
  },
  "output_format": "pdf",
  "notification": true
}
```

### 2.4 リクエスト例（研修レポート）

```json
{
  "report_type": "training",
  "title": "2025年度研修実績レポート",
  "description": "2025年度の研修受講状況と評価",
  "target_users": ["U12345", "U12346", "U12347", "U12348", "U12349"],
  "period": {
    "start_date": "2025-04-01",
    "end_date": "2026-03-31"
  },
  "filters": {
    "training_status": ["completed"],
    "min_duration": 8
  },
  "grouping": [
    {
      "field": "training_category",
      "sort_order": "asc"
    },
    {
      "field": "quarter",
      "sort_order": "asc"
    }
  ],
  "sort": {
    "field": "completion_date",
    "order": "desc"
  },
  "output_format": "excel",
  "notification": true
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（202 Accepted）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| report_id | string | 生成されたレポートID | |
| status | string | レポート生成状態 | "queued", "processing", "completed", "failed" |
| report_type | string | レポートタイプ | |
| title | string | レポートタイトル | |
| created_at | string | 作成日時 | ISO 8601形式 |
| created_by | string | 作成者ID | |
| estimated_completion_time | string | 推定完了時間 | ISO 8601形式 |
| status_url | string | 状態確認URL | |
| download_url | string | ダウンロードURL | レポート生成完了後に有効 |

### 3.2 正常時レスポンス例

```json
{
  "report_id": "RPT-2025052801",
  "status": "queued",
  "report_type": "skill",
  "title": "技術スキル分布レポート",
  "created_at": "2025-05-28T10:15:30+09:00",
  "created_by": "U12345",
  "estimated_completion_time": "2025-05-28T10:20:30+09:00",
  "status_url": "/api/reports/RPT-2025052801/status",
  "download_url": null
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_REPORT_TYPE | レポートタイプが不正です | 存在しないレポートタイプ |
| 400 Bad Request | INVALID_OUTPUT_FORMAT | 出力形式が不正です | 存在しない出力形式 |
| 400 Bad Request | INVALID_DATE | 日付が不正です | 不正な日付形式 |
| 400 Bad Request | INVALID_DATE_RANGE | 日付範囲が不正です | 開始日が終了日より後の日付 |
| 400 Bad Request | TOO_MANY_USERS | ユーザー数が上限を超えています | 100件を超えるユーザー指定 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | レポート生成権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 429 Too Many Requests | TOO_MANY_REQUESTS | リクエスト数が上限を超えています | 短時間に多数のレポート生成リクエスト |
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
   - レポート生成権限のチェック
2. リクエストパラメータの検証
   - 必須パラメータの存在チェック
   - 各パラメータの形式・値の妥当性チェック
   - レポートタイプに応じたフィルター条件の妥当性チェック
   - 対象ユーザーの存在チェック
3. レポート生成タスクの登録
   - reports テーブルにレポート情報を登録
   - report_details テーブルに詳細情報を登録
   - report_users テーブルに対象ユーザー情報を登録
   - 非同期処理キューにレポート生成タスクを登録
4. レスポンスの生成
   - レポートIDと状態情報を含むレスポンスを生成
5. レスポンス返却
6. 非同期処理（バックグラウンド）
   - レポートタイプに応じたデータ取得
   - レポート生成処理
   - 生成されたレポートの保存
   - レポート状態の更新
   - 通知フラグがtrueの場合、完了通知の送信

### 4.2 権限チェック

- レポート生成には以下のいずれかの条件を満たす必要がある
  - 自身のみを対象とするレポートの場合は常に生成可能
  - 他ユーザーを含むレポートの場合：
    - レポート生成権限（PERM_GENERATE_REPORTS）を持っている
    - 管理者権限（ROLE_ADMIN）を持っている
    - 対象ユーザーの直属の上長である

### 4.3 レポートタイプ別処理

#### skill レポート
- ユーザーのスキル情報を取得
- フィルター条件に基づいてデータを絞り込み
- グループ化条件に基づいてデータをグループ化
- ソート条件に基づいてデータをソート
- スキルレベルの分布、平均値、最大値、最小値などの統計情報を計算
- 指定された出力形式でレポートを生成

#### training レポート
- ユーザーの研修記録を取得
- フィルター条件に基づいてデータを絞り込み
- グループ化条件に基づいてデータをグループ化
- ソート条件に基づいてデータをソート
- 研修時間の合計、平均評価点数などの統計情報を計算
- 指定された出力形式でレポートを生成

#### certification レポート
- ユーザーの資格情報を取得
- フィルター条件に基づいてデータを絞り込み
- グループ化条件に基づいてデータをグループ化
- ソート条件に基づいてデータをソート
- 資格取得数、有効期限切れ数などの統計情報を計算
- 指定された出力形式でレポートを生成

#### career レポート
- ユーザーのキャリア目標情報を取得
- フィルター条件に基づいてデータを絞り込み
- グループ化条件に基づいてデータをグループ化
- ソート条件に基づいてデータをソート
- 目標達成率、進捗状況などの統計情報を計算
- 指定された出力形式でレポートを生成

#### work レポート
- ユーザーの作業実績情報を取得
- フィルター条件に基づいてデータを絞り込み
- グループ化条件に基づいてデータをグループ化
- ソート条件に基づいてデータをソート
- 作業時間の合計、プロジェクト別割合などの統計情報を計算
- 指定された出力形式でレポートを生成

#### summary レポート
- 指定されたデータ（スキル、研修、資格、キャリア、作業実績）を取得
- 各データの主要な統計情報を計算
- ユーザー別のサマリー情報を生成
- 指定された出力形式でレポートを生成

### 4.4 出力形式別処理

- pdf: PDFライブラリを使用してPDF形式のレポートを生成
- excel: Excelライブラリを使用してExcel形式のレポートを生成
- csv: CSV形式のレポートを生成
- json: JSON形式のレポートデータを生成

### 4.5 非同期処理

- レポート生成は非同期で実行
- 処理状態は "queued"（キュー登録済）→ "processing"（処理中）→ "completed"（完了）または "failed"（失敗）と遷移
- 処理状態はAPI-062（レポート取得API）で確認可能
- 処理完了後、通知フラグがtrueの場合は通知を送信

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-062](API仕様書_API-062.md) | レポート取得API | 生成されたレポートの取得 |
| [API-051](API仕様書_API-051.md) | 研修記録取得API | 研修データの取得 |
| [API-053](API仕様書_API-053.md) | 資格情報取得API | 資格データの取得 |
| [API-021](API仕様書_API-021.md) | スキル情報取得API | スキルデータの取得 |
| [API-031](API仕様書_API-031.md) | キャリア目標取得API | キャリアデータの取得 |
| [API-041](API仕様書_API-041.md) | 作業実績取得API | 作業実績データの取得 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| reports | レポート基本情報 | 作成（C） |
| report_details | レポート詳細情報 | 作成（C） |
| report_users | レポート対象ユーザー | 作成（C） |
| skills | スキル情報 | 参照（R） |
| trainings | 研修記録情報 | 参照（R） |
| certifications | 資格情報 | 参照（R） |
| career_goals | キャリア目標情報 | 参照（R） |
| work_records | 作業実績情報 | 参照（R） |
| departments | 部門情報 | 参照（R） |
| positions | 役職情報 | 参照（R） |
| files | ファイル情報 | 作成（C） |

### 5.3 注意事項・補足

- レポート生成は非同期処理のため、リクエスト時点では処理は完了していない
- レポート生成の進捗状況はAPI-062（レポート取得API）で確認可能
- 大量のデータを含むレポートの場合、生成に時間がかかる場合がある
- レポートの保存期間は生成から30日間
- 同時に実行可能なレポート生成タスク数には上限がある（ユーザーあたり5件）
- 出力形式によって、生成されるレポートの見た目や含まれる情報が異なる場合がある
- グループ化条件は最大3階層まで指定可能
- レポートタイプによって、利用可能なフィルター条件、グループ化条件、ソート条件が異なる

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useForm, Controller } from 'react-hook-form';
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
  Checkbox,
  FormControlLabel,
  CircularProgress,
  Snackbar,
  Alert,
  Autocomplete,
  Card,
  CardContent,
  CardActions,
  Tabs,
  Tab
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { Add as AddIcon, Delete as DeleteIcon, Description as DescriptionIcon } from '@mui/icons-material';

// バリデーションスキーマ
const schema = yup.object().shape({
  report_type: yup.string()
    .required('レポートタイプは必須です')
    .oneOf(['skill', 'training', 'certification', 'career', 'work', 'summary'], '無効なレポートタイプです'),
  title: yup.string()
    .required('レポートタイトルは必須です')
    .max(100, 'レポートタイトルは100文字以内で入力してください'),
  description: yup.string()
    .max(500, 'レポート説明は500文字以内で入力してください'),
  target_users: yup.array()
    .of(yup.string())
    .required('対象ユーザーは必須です')
    .min(1, '少なくとも1人のユーザーを選択してください')
    .max(100, '対象ユーザーは最大100人まで選択可能です'),
  period: yup.object().shape({
    start_date: yup.date().nullable(),
    end_date: yup.date().nullable()
      .when('start_date', {
        is: (start_date: Date | null) => start_date !== null,
        then: yup.date().min(
          yup.ref('start_date'),
          '終了日は開始日以降の日付を指定してください'
        )
      }),
    fiscal_year: yup.number().nullable()
      .integer('年度は整数で入力してください')
      .min(2000, '年度は2000以降で入力してください')
      .max(2100, '年度は2100以下で入力してください')
  }),
  output_format: yup.string()
    .required('出力形式は必須です')
    .oneOf(['pdf', 'excel', 'csv', 'json'], '無効な出力形式です'),
  notification: yup.boolean()
});

// 型定義
interface ReportFormData {
  report_type: string;
  title: string;
  description?: string;
  target_users: string[];
  period?: {
    start_date?: Date | null;
    end_date?: Date | null;
    fiscal_year?: number | null;
  };
  filters?: any;
  grouping?: Array<{
    field: string;
    sort_order?: string;
  }>;
  sort?: {
    field: string;
    order?: string;
  };
  output_format: string;
  notification?: boolean;
}

interface User {
  id: string;
  name: string;
  department: string;
}

const ReportGenerationForm: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean>(false);
  const [reportId, setReportId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<number>(0);
  
  // ユーザー一覧（実際の実装ではAPIから取得）
  const [users, setUsers] = useState<User[]>([
    { id: 'U12345', name: '山田 太郎', department: '開発部' },
    { id: 'U12346', name: '鈴木 一郎', department: '営業部' },
    { id: 'U12347', name: '佐藤 次郎', department: '人事部' },
    { id: 'U12348', name: '田中 三郎', department: '開発部' },
    { id: 'U12349', name: '高橋 花子', department: '経理部' }
  ]);
  
  // フォーム設定
  const { control, handleSubmit, watch, setValue, formState: { errors } } = useForm<ReportFormData>({
    resolver: yupResolver(schema),
    defaultValues: {
      report_type: 'skill',
      title: '',
      description: '',
      target_users: [],
      period: {
        start_date: null,
        end_date: null,
        fiscal_year: new Date().getFullYear()
      },
      filters: {},
      grouping: [
        {
          field: 'department',
          sort_order: 'asc'
        }
      ],
      sort: {
        field: 'level',
        order: 'desc'
      },
      output_format: 'pdf',
      notification: true
    }
  });
  
  // 現在のレポートタイプを監視
  const currentReportType = watch('report_type');
  
  // レポート生成リクエスト送信
  const generateReport = async (data: ReportFormData) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.post('/api/reports', data, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });
      
      setReportId(response.data.report_id);
      setSuccess(true);
      
      // レポート詳細画面に遷移
      setTimeout(() => {
        navigate(`/reports/${response.data.report_id}`);
      }, 2000);
      
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const errorData = err.response.data;
        setError(errorData.error?.message || 'レポート生成リクエストに失敗しました');
      } else {
        setError('レポート生成リクエスト中にエラーが発生しました');
      }
    } finally {
      setLoading(false);
    }
  };
  
  // タブ切り替え
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };
  
  // レポートタイプに応じたフィルター設定コンポーネントを取得
  const getFilterComponent = () => {
    switch (currentReportType) {
      case 'skill':
        return (
          <SkillFilterComponent control={control} errors={errors} />
        );
      case 'training':
        return (
          <TrainingFilterComponent control={control} errors={errors} />
        );
      case 'certification':
        return (
          <CertificationFilterComponent control={control} errors={errors}
