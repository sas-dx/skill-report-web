# API仕様書：API-041 作業実績取得API

## 1. 基本情報

- **API ID**: API-041
- **API名称**: 作業実績取得API
- **概要**: ユーザーの作業実績情報を取得する
- **エンドポイント**: `/api/work-records/{user_id}`
- **HTTPメソッド**: GET
- **リクエスト形式**: URLパラメータ
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
| Accept | - | レスポンス形式 | application/json |

### 2.2 パスパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| user_id | string | ○ | ユーザーID | 自身のIDまたは部下のIDを指定可能 |

### 2.3 クエリパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| year | number | - | 年度 | 指定がない場合は現在の年度<br>例: 2025 |
| month | number | - | 月 | 1-12の範囲<br>指定がない場合は全ての月 |
| start_date | string | - | 開始日 | ISO 8601形式（YYYY-MM-DD）<br>month指定時は無視 |
| end_date | string | - | 終了日 | ISO 8601形式（YYYY-MM-DD）<br>month指定時は無視 |
| project_id | string | - | プロジェクトID | 特定のプロジェクトの実績のみを取得 |
| category | string | - | 作業カテゴリ | 特定のカテゴリの実績のみを取得 |
| include_details | boolean | - | 詳細情報を含めるか | true/false<br>デフォルト: false |
| page | number | - | ページ番号 | 1以上の整数<br>デフォルト: 1 |
| per_page | number | - | 1ページあたりの件数 | 1-100の範囲<br>デフォルト: 20 |

### 2.4 リクエスト例

```
GET /api/work-records/U12345?year=2025&month=5&include_details=true HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| user_name | string | ユーザー名 | |
| year | number | 年度 | |
| month | number | 月 | month指定時のみ |
| period | object | 期間情報 | start_date, end_date指定時のみ |
| work_records | array | 作業実績情報の配列 | |
| summary | object | 集計情報 | |
| pagination | object | ページネーション情報 | |

#### period オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| start_date | string | 開始日 | ISO 8601形式（YYYY-MM-DD） |
| end_date | string | 終了日 | ISO 8601形式（YYYY-MM-DD） |

#### work_records 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| record_id | string | 実績ID | |
| date | string | 作業日 | ISO 8601形式（YYYY-MM-DD） |
| project_id | string | プロジェクトID | |
| project_name | string | プロジェクト名 | |
| category | string | 作業カテゴリ | |
| task | string | 作業内容 | |
| hours | number | 作業時間（時間） | 0.5単位 |
| status | string | ステータス | "draft", "submitted", "approved", "rejected" |
| details | object | 詳細情報 | include_details=trueの場合のみ |
| created_at | string | 作成日時 | ISO 8601形式 |
| updated_at | string | 更新日時 | ISO 8601形式 |

#### details オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| description | string | 詳細説明 | |
| achievements | string | 成果物・達成事項 | |
| issues | string | 課題・問題点 | |
| next_actions | string | 次のアクション | |
| related_skills | array | 関連スキル | |
| attachments | array | 添付ファイル | |
| comments | array | コメント | |

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

#### comments 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| comment_id | string | コメントID | |
| commenter_id | string | コメント者ID | |
| commenter_name | string | コメント者名 | |
| comment | string | コメント内容 | |
| created_at | string | 作成日時 | ISO 8601形式 |

#### summary オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total_records | number | 実績の総数 | |
| total_hours | number | 合計作業時間 | |
| by_project | array | プロジェクト別集計 | |
| by_category | array | カテゴリ別集計 | |
| by_status | array | ステータス別集計 | |
| by_date | array | 日付別集計 | |

#### by_project 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| project_id | string | プロジェクトID | |
| project_name | string | プロジェクト名 | |
| hours | number | 作業時間 | |
| percentage | number | 割合（%） | |

#### by_category 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| category | string | 作業カテゴリ | |
| hours | number | 作業時間 | |
| percentage | number | 割合（%） | |

#### by_status 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| status | string | ステータス | |
| count | number | 件数 | |
| hours | number | 作業時間 | |
| percentage | number | 割合（%） | |

#### by_date 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| date | string | 日付 | ISO 8601形式（YYYY-MM-DD） |
| hours | number | 作業時間 | |
| record_count | number | 実績件数 | |

#### pagination オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| current_page | number | 現在のページ番号 | |
| per_page | number | 1ページあたりの件数 | |
| total_pages | number | 総ページ数 | |
| total_records | number | 総レコード数 | |

### 3.2 正常時レスポンス例

```json
{
  "user_id": "U12345",
  "user_name": "山田 太郎",
  "year": 2025,
  "month": 5,
  "work_records": [
    {
      "record_id": "WR001",
      "date": "2025-05-01",
      "project_id": "P001",
      "project_name": "スキルレポートWEB化PJT",
      "category": "開発",
      "task": "フロントエンド実装",
      "hours": 7.5,
      "status": "approved",
      "details": {
        "description": "Reactコンポーネントの実装とテスト",
        "achievements": "ユーザープロフィール画面のコンポーネント5つを実装完了",
        "issues": "IE11での表示崩れがあり、対応が必要",
        "next_actions": "レスポンシブデザインの調整を行う",
        "related_skills": [
          {
            "skill_id": "S007",
            "name": "React",
            "category": "technical",
            "level_used": 3
          },
          {
            "skill_id": "S008",
            "name": "TypeScript",
            "category": "technical",
            "level_used": 3
          }
        ],
        "attachments": [
          {
            "file_id": "F001",
            "file_name": "component_design.pdf",
            "file_type": "application/pdf",
            "file_size": 2457600,
            "upload_date": "2025-05-01T18:30:00+09:00"
          }
        ],
        "comments": [
          {
            "comment_id": "C001",
            "commenter_id": "U67890",
            "commenter_name": "鈴木 花子",
            "comment": "コンポーネントの分割が適切で、再利用性が高いです。良い実装です。",
            "created_at": "2025-05-02T10:15:00+09:00"
          }
        ]
      },
      "created_at": "2025-05-01T18:30:00+09:00",
      "updated_at": "2025-05-02T10:15:00+09:00"
    },
    {
      "record_id": "WR002",
      "date": "2025-05-02",
      "project_id": "P001",
      "project_name": "スキルレポートWEB化PJT",
      "category": "会議",
      "task": "週次進捗会議",
      "hours": 1.5,
      "status": "approved",
      "details": {
        "description": "プロジェクトの週次進捗会議に参加",
        "achievements": "フロントエンド実装の進捗を報告",
        "issues": "",
        "next_actions": "来週の作業計画を共有",
        "related_skills": [],
        "attachments": [],
        "comments": []
      },
      "created_at": "2025-05-02T17:45:00+09:00",
      "updated_at": "2025-05-03T09:10:00+09:00"
    }
  ],
  "summary": {
    "total_records": 20,
    "total_hours": 160,
    "by_project": [
      {
        "project_id": "P001",
        "project_name": "スキルレポートWEB化PJT",
        "hours": 120,
        "percentage": 75
      },
      {
        "project_id": "P002",
        "project_name": "社内研修",
        "hours": 40,
        "percentage": 25
      }
    ],
    "by_category": [
      {
        "category": "開発",
        "hours": 100,
        "percentage": 62.5
      },
      {
        "category": "設計",
        "hours": 30,
        "percentage": 18.75
      },
      {
        "category": "会議",
        "hours": 20,
        "percentage": 12.5
      },
      {
        "category": "その他",
        "hours": 10,
        "percentage": 6.25
      }
    ],
    "by_status": [
      {
        "status": "approved",
        "count": 18,
        "hours": 150,
        "percentage": 93.75
      },
      {
        "status": "submitted",
        "count": 2,
        "hours": 10,
        "percentage": 6.25
      }
    ],
    "by_date": [
      {
        "date": "2025-05-01",
        "hours": 8,
        "record_count": 1
      },
      {
        "date": "2025-05-02",
        "hours": 8,
        "record_count": 2
      }
    ]
  },
  "pagination": {
    "current_page": 1,
    "per_page": 20,
    "total_pages": 1,
    "total_records": 20
  }
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_YEAR | 年度が不正です | 存在しない年度指定 |
| 400 Bad Request | INVALID_MONTH | 月が不正です | 1-12の範囲外 |
| 400 Bad Request | INVALID_DATE_RANGE | 日付範囲が不正です | 開始日>終了日など |
| 400 Bad Request | INVALID_PROJECT_ID | プロジェクトIDが不正です | 存在しないプロジェクトID |
| 400 Bad Request | INVALID_CATEGORY | カテゴリが不正です | 存在しないカテゴリ |
| 400 Bad Request | INVALID_PAGE | ページ番号が不正です | 1未満のページ番号 |
| 400 Bad Request | INVALID_PER_PAGE | 1ページあたりの件数が不正です | 1-100の範囲外 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他ユーザーの情報閲覧権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 404 Not Found | WORK_RECORDS_NOT_FOUND | 作業実績が見つかりません | 指定された条件の作業実績が存在しない |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_DATE_RANGE",
    "message": "日付範囲が不正です",
    "details": "開始日は終了日より前の日付を指定してください。"
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
   - 年度・月・日付範囲の妥当性チェック
   - プロジェクトID・カテゴリの存在チェック
   - ページネーションパラメータの妥当性チェック
3. 作業実績情報の取得
   - 指定されたユーザーIDと条件に合致する作業実績を取得
   - include_detailsがtrueの場合は、詳細情報も取得
4. 集計情報の計算
   - プロジェクト別、カテゴリ別、ステータス別、日付別の集計
5. ページネーション処理
   - 指定されたページ番号と1ページあたりの件数に基づいて結果を絞り込み
6. レスポンスの生成
   - 取得した作業実績情報を整形
7. レスポンス返却

### 4.2 権限チェック

- 自身の作業実績は常に閲覧可能
- 他ユーザーの作業実績閲覧には以下のいずれかの条件を満たす必要がある
  - 対象ユーザーの直属の上長である
  - 作業実績閲覧権限（PERM_VIEW_WORK_RECORDS）を持っている
  - 管理者権限（ROLE_ADMIN）を持っている
  - プロジェクト管理者として登録されている（project_managersテーブルに登録あり）

### 4.3 年度・月・日付範囲の扱い

- 年度は4月1日から翌年3月31日までの期間
- 年度の指定がない場合は、リクエスト時点の年度を使用
- 月の指定がある場合は、その月の1日から月末までの期間で絞り込み
- 日付範囲（start_date, end_date）の指定がある場合は、月の指定を無視して日付範囲で絞り込み
- 日付範囲の指定がある場合、start_date ≤ end_dateであることを検証

### 4.4 集計情報の計算方法

- プロジェクト別集計: 各プロジェクトごとの作業時間と全体に対する割合を計算
- カテゴリ別集計: 各カテゴリごとの作業時間と全体に対する割合を計算
- ステータス別集計: 各ステータスごとの件数、作業時間、全体に対する割合を計算
- 日付別集計: 各日付ごとの作業時間と実績件数を計算

### 4.5 ページネーション処理

- 指定されたページ番号と1ページあたりの件数に基づいて結果を絞り込み
- ページ番号のデフォルトは1
- 1ページあたりの件数のデフォルトは20、最大100
- 総ページ数は「総レコード数 ÷ 1ページあたりの件数」の切り上げ

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-042](API仕様書_API-042.md) | 作業実績登録API | 作業実績情報登録 |
| [API-043](API仕様書_API-043.md) | 作業実績更新API | 作業実績情報更新 |
| [API-101](API仕様書_API-101.md) | 一括登録検証API | 一括登録データ検証 |
| [API-102](API仕様書_API-102.md) | 一括登録実行API | 一括登録実行 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| work_records | 作業実績情報 | 参照（R） |
| work_record_details | 作業実績詳細情報 | 参照（R） |
| work_record_skills | 作業実績関連スキル | 参照（R） |
| work_record_attachments | 作業実績添付ファイル | 参照（R） |
| work_record_comments | 作業実績コメント | 参照（R） |
| projects | プロジェクト情報 | 参照（R） |
| project_managers | プロジェクト管理者情報 | 参照（R） |
| work_categories | 作業カテゴリ情報 | 参照（R） |

### 5.3 注意事項・補足

- 作業実績は0.5時間単位で記録
- 1日の作業時間合計が8時間を超える場合は警告表示（フロントエンド側で対応）
- 詳細情報（include_details=true）を含める場合、レスポンスサイズが大きくなるため注意
- 添付ファイルの実体は別APIで取得（/api/files/{file_id}）
- 過去の作業実績は編集不可（読み取り専用）となる場合がある（承認済みの場合など）
- プロジェクト別・カテゴリ別の集計は、全期間の合計値を表示

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Box,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Chip,
  Pagination,
  CircularProgress,
  Alert,
  Tabs,
  Tab,
  Card,
  CardContent,
  Divider
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer
} from 'recharts';
import { DatePicker } from '@mui/x-date-pickers';

// 型定義
interface WorkRecord {
  record_id: string;
  date: string;
  project_id: string;
  project_name: string;
  category: string;
  task: string;
  hours: number;
  status: 'draft' | 'submitted' | 'approved' | 'rejected';
  details?: {
    description: string;
    achievements: string;
    issues: string;
    next_actions: string;
    related_skills: Array<{
      skill_id: string;
      name: string;
      category: string;
      level_used: number;
    }>;
    attachments: Array<{
      file_id: string;
      file_name: string;
      file_type: string;
      file_size: number;
      upload_date: string;
    }>;
    comments: Array<{
      comment_id: string;
      commenter_id: string;
      commenter_name: string;
      comment: string;
      created_at: string;
    }>;
  };
  created_at: string;
  updated_at: string;
}

interface WorkRecordsSummary {
  total_records: number;
  total_hours: number;
  by_project: Array<{
    project_id: string;
    project_name: string;
    hours: number;
    percentage: number;
  }>;
  by_category: Array<{
    category: string;
    hours: number;
    percentage: number;
  }>;
  by_status: Array<{
    status: string;
    count: number;
    hours: number;
    percentage: number;
  }>;
  by_date: Array<{
    date: string;
    hours: number;
    record_count: number;
  }>;
}

interface Pagination {
  current_page: number;
  per_page: number;
  total_pages: number;
  total_records: number;
}

interface WorkRecordsResponse {
  user_id: string;
  user_name: string;
  year: number;
  month?: number;
  period?: {
    start_date: string;
    end_date: string;
  };
  work_records: WorkRecord[];
  summary: WorkRecordsSummary;
  pagination: Pagination;
}

const WorkRecordsView: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const [year, setYear] = useState<number>(new Date().getFullYear());
  const [month, setMonth] = useState<number | null>(new Date().getMonth() + 1);
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [projectId, setProjectId] = useState<string | null>(null);
  const [category, setCategory] = useState<string | null>(null);
  const [includeDetails, setIncludeDetails] = useState<boolean>(false);
  const [page, setPage] = useState<number>(1);
  const [perPage, setPerPage] = useState<number>(20);
  
  const [workRecordsData, setWorkRecordsData] = useState<WorkRecordsResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<number>(0);
  
  // プロジェクト一覧（実際の実装ではAPIから取得）
  const [projects, setProjects] = useState<Array<{ id: string, name: string }>>([]);
  
  // カテゴリ一覧（実際の実装ではAPIから取得）
  const [categories, setCategories] = useState<string[]>([]);
  
  useEffect(() => {
    // プロジェクト一覧とカテゴリ一覧の取得（実際の実装ではAPIから取得）
    setProjects([
      { id: 'P001', name: 'スキルレポートWEB化PJT' },
      { id: 'P002', name: '社内研修' }
    ]);
    
    setCategories(['開発', '設計', '会議', 'レビュー', '調査', 'その他']);
    
    fetchWorkRecords();
  }, [userId, year, month, startDate, endDate, projectId, category, includeDetails, page, perPage]);
  
  const fetchWorkRecords = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // クエリパラメータの構築
      const params: Record<string, any> = {
        year,
        page,
        per_page: perPage,
        include_details: includeDetails
      };
      
      if (month !== null) {
        params.month = month;
      }
      
      if (startDate && endDate) {
        params.start_date = startDate.toISOString().split('T')[0];
        params.end_date = endDate.toISOString().split('T')[0];
      }
      
      if (projectId) {
        params.project_id = projectI
