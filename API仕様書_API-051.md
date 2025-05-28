# API仕様書：API-051 研修記録取得API

## 1. 基本情報

- **API ID**: API-051
- **API名称**: 研修記録取得API
- **概要**: ユーザーの研修記録情報を取得する
- **エンドポイント**: `/api/trainings/{user_id}`
- **HTTPメソッド**: GET
- **リクエスト形式**: -
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
| Accept | - | レスポンス形式 | application/json |

### 2.2 パスパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| user_id | string | ○ | ユーザーID | 自身のIDまたは部下のIDを指定可能 |

### 2.3 クエリパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| year | number | - | 年度 | 指定がない場合は全期間 |
| category | string | - | 研修カテゴリ | 指定がない場合は全カテゴリ |
| status | string | - | 受講状態 | "planned", "completed", "cancelled"<br>指定がない場合は全状態 |
| page | number | - | ページ番号 | デフォルト: 1 |
| per_page | number | - | 1ページあたりの件数 | デフォルト: 20、最大: 100 |
| sort | string | - | ソート項目 | "date", "category", "name", "status"<br>デフォルト: "date" |
| order | string | - | ソート順 | "asc", "desc"<br>デフォルト: "desc" |

### 2.4 リクエスト例

```
GET /api/trainings/U12345?year=2025&category=technical&status=completed&page=1&per_page=20&sort=date&order=desc
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total | number | 総件数 | |
| page | number | 現在のページ番号 | |
| per_page | number | 1ページあたりの件数 | |
| total_pages | number | 総ページ数 | |
| trainings | array | 研修記録一覧 | |

#### trainings 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| training_id | string | 研修ID | |
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
| updated_at | string | 更新日時 | ISO 8601形式 |

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
  "total": 42,
  "page": 1,
  "per_page": 20,
  "total_pages": 3,
  "trainings": [
    {
      "training_id": "TR001",
      "name": "クラウドアーキテクチャ設計基礎",
      "category": "technical",
      "description": "AWSを活用したクラウドアーキテクチャの設計手法を学ぶ研修",
      "start_date": "2025-04-15",
      "end_date": "2025-04-17",
      "duration_hours": 24,
      "location": "オンライン",
      "format": "online",
      "provider": "AWS Japan",
      "status": "completed",
      "completion_date": "2025-04-17",
      "score": 92,
      "certificate": {
        "certificate_id": "CERT-AWS-123456",
        "issue_date": "2025-04-18",
        "expiry_date": "2028-04-17",
        "file_id": "F001"
      },
      "feedback": "クラウド設計の基本概念から実践的なアーキテクチャパターンまで幅広く学ぶことができた。特にセキュリティ設計の部分が業務に役立つと感じた。",
      "related_skills": [
        {
          "skill_id": "S101",
          "name": "AWS",
          "category": "technical",
          "level": 4
        },
        {
          "skill_id": "S102",
          "name": "クラウドアーキテクチャ",
          "category": "technical",
          "level": 3
        }
      ],
      "attachments": [
        {
          "file_id": "F001",
          "file_name": "aws_certificate.pdf",
          "file_type": "application/pdf",
          "file_size": 245678,
          "upload_date": "2025-04-18T10:30:00+09:00"
        },
        {
          "file_id": "F002",
          "file_name": "training_materials.zip",
          "file_type": "application/zip",
          "file_size": 3456789,
          "upload_date": "2025-04-18T10:35:00+09:00"
        }
      ],
      "created_at": "2025-04-10T09:15:00+09:00",
      "updated_at": "2025-04-18T10:45:00+09:00"
    },
    {
      "training_id": "TR002",
      "name": "プロジェクトマネジメント基礎",
      "category": "management",
      "description": "ITプロジェクトのマネジメント手法を学ぶ研修",
      "start_date": "2025-05-20",
      "end_date": "2025-05-22",
      "duration_hours": 18,
      "location": "本社会議室",
      "format": "offline",
      "provider": "社内研修",
      "status": "planned",
      "completion_date": null,
      "score": null,
      "certificate": null,
      "feedback": null,
      "related_skills": [
        {
          "skill_id": "S201",
          "name": "プロジェクトマネジメント",
          "category": "management",
          "level": 2
        }
      ],
      "attachments": [],
      "created_at": "2025-04-25T14:20:00+09:00",
      "updated_at": "2025-04-25T14:20:00+09:00"
    }
  ]
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | クエリパラメータ形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他ユーザーの情報参照権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "権限がありません",
    "details": "指定されたユーザーの研修記録を参照する権限がありません"
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
   - クエリパラメータの妥当性チェック
3. 研修記録情報の取得
   - trainings テーブルから基本情報を取得
   - training_details テーブルから詳細情報を取得
   - training_skills テーブルから関連スキル情報を取得
   - training_attachments テーブルから添付ファイル情報を取得
   - training_certificates テーブルから修了証情報を取得
4. 検索条件による絞り込み
   - 年度、カテゴリ、受講状態による絞り込み
5. ソート処理
   - 指定されたソート項目・ソート順でソート
6. ページング処理
   - 指定されたページ番号・1ページあたりの件数でページング
7. レスポンスの生成
   - 取得結果を整形
8. レスポンス返却

### 4.2 権限チェック

- 自身の研修記録は常に参照可能
- 他ユーザーの研修記録参照には以下のいずれかの条件を満たす必要がある
  - 対象ユーザーの直属の上長である
  - 研修記録参照権限（PERM_VIEW_TRAINING_RECORDS）を持っている
  - 管理者権限（ROLE_ADMIN）を持っている
  - 研修管理者として登録されている（training_managersテーブルに登録あり）

### 4.3 検索条件の扱い

- 年度（year）: 指定された年度に開始または終了した研修を検索
- カテゴリ（category）: 指定されたカテゴリに属する研修を検索
- 受講状態（status）: 指定された状態の研修を検索

### 4.4 ソート処理

- date: 開始日でソート
- category: 研修カテゴリでソート
- name: 研修名でソート
- status: 受講状態でソート

### 4.5 ページング処理

- page: 取得するページ番号（1から開始）
- per_page: 1ページあたりの件数（デフォルト: 20、最大: 100）

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-052](API仕様書_API-052.md) | 研修記録登録API | 研修記録情報登録 |
| [API-053](API仕様書_API-053.md) | 資格情報取得API | 資格情報取得 |
| [API-054](API仕様書_API-054.md) | 資格情報更新API | 資格情報更新 |
| [API-061](API仕様書_API-061.md) | レポート生成API | 研修レポート生成 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| trainings | 研修記録情報 | 参照（R） |
| training_details | 研修記録詳細情報 | 参照（R） |
| training_skills | 研修記録関連スキル | 参照（R） |
| training_attachments | 研修記録添付ファイル | 参照（R） |
| training_certificates | 研修修了証情報 | 参照（R） |
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

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useSearchParams } from 'react-router-dom';
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
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Pagination,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Grid,
  Card,
  CardContent,
  CardActions,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import {
  FilterList as FilterIcon,
  Sort as SortIcon,
  Description as DescriptionIcon,
  School as SchoolIcon,
  CalendarToday as CalendarIcon,
  LocationOn as LocationIcon,
  AccessTime as TimeIcon,
  Attachment as AttachmentIcon,
  Download as DownloadIcon,
  Star as StarIcon
} from '@mui/icons-material';

// 型定義
interface TrainingRecord {
  training_id: string;
  name: string;
  category: string;
  description: string;
  start_date: string;
  end_date: string;
  duration_hours: number;
  location: string;
  format: string;
  provider: string;
  status: string;
  completion_date: string | null;
  score: number | null;
  certificate: {
    certificate_id: string;
    issue_date: string;
    expiry_date: string;
    file_id: string;
  } | null;
  feedback: string | null;
  related_skills: Array<{
    skill_id: string;
    name: string;
    category: string;
    level: number;
  }>;
  attachments: Array<{
    file_id: string;
    file_name: string;
    file_type: string;
    file_size: number;
    upload_date: string;
  }>;
  created_at: string;
  updated_at: string;
}

interface TrainingResponse {
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
  trainings: TrainingRecord[];
}

const TrainingRecordList: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const [searchParams, setSearchParams] = useSearchParams();
  const [trainings, setTrainings] = useState<TrainingRecord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState<number>(0);
  const [page, setPage] = useState<number>(parseInt(searchParams.get('page') || '1', 10));
  const [perPage, setPerPage] = useState<number>(parseInt(searchParams.get('per_page') || '20', 10));
  const [totalPages, setTotalPages] = useState<number>(0);
  const [year, setYear] = useState<string>(searchParams.get('year') || '');
  const [category, setCategory] = useState<string>(searchParams.get('category') || '');
  const [status, setStatus] = useState<string>(searchParams.get('status') || '');
  const [sort, setSort] = useState<string>(searchParams.get('sort') || 'date');
  const [order, setOrder] = useState<string>(searchParams.get('order') || 'desc');
  const [selectedTraining, setSelectedTraining] = useState<TrainingRecord | null>(null);
  const [detailDialogOpen, setDetailDialogOpen] = useState<boolean>(false);
  const [filterDialogOpen, setFilterDialogOpen] = useState<boolean>(false);

  // 研修記録データの取得
  const fetchTrainings = async () => {
    try {
      setLoading(true);
      setError(null);

      // クエリパラメータの構築
      const params = new URLSearchParams();
      if (year) params.append('year', year);
      if (category) params.append('category', category);
      if (status) params.append('status', status);
      params.append('page', page.toString());
      params.append('per_page', perPage.toString());
      params.append('sort', sort);
      params.append('order', order);

      // APIリクエスト
      const response = await axios.get<TrainingResponse>(
        `/api/trainings/${userId}?${params.toString()}`,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Accept': 'application/json'
          }
        }
      );

      // レスポンスデータの設定
      setTrainings(response.data.trainings);
      setTotal(response.data.total);
      setPage(response.data.page);
      setPerPage(response.data.per_page);
      setTotalPages(response.data.total_pages);

      // URLのクエリパラメータを更新
      setSearchParams(params);
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const errorData = err.response.data;
        setError(errorData.error?.message || '研修記録の取得に失敗しました');
      } else {
        setError('研修記録の取得中にエラーが発生しました');
      }
    } finally {
      setLoading(false);
    }
  };

  // 初回レンダリング時とフィルター変更時にデータ取得
  useEffect(() => {
    fetchTrainings();
  }, [userId, page, perPage, sort, order]);

  // フィルター適用
  const applyFilters = () => {
    setPage(1); // フィルター変更時は1ページ目に戻る
    fetchTrainings();
    setFilterDialogOpen(false);
  };

  // フィルターリセット
  const resetFilters = () => {
    setYear('');
    setCategory('');
    setStatus('');
    setPage(1);
    setFilterDialogOpen(false);
    // リセット後にデータ再取得
    setTimeout(() => {
      fetchTrainings();
    }, 0);
  };

  // 研修詳細ダイアログを開く
  const openDetailDialog = (training: TrainingRecord) => {
    setSelectedTraining(training);
    setDetailDialogOpen(true);
  };

  // 研修カテゴリの表示名を取得
  const getCategoryLabel = (category: string): string => {
    switch (category) {
      case 'technical': return '技術';
      case 'business': return 'ビジネス';
      case 'management': return 'マネジメント';
      case 'compliance': return 'コンプライアンス';
      case 'other': return 'その他';
      default: return category;
    }
  };

  // 研修状態の表示名とカラーを取得
  const getStatusInfo = (status: string): { label: string; color: 'default' | 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning' } => {
    switch (status) {
      case 'planned':
        return { label: '計画中', color: 'info' };
      case 'completed':
        return { label: '完了', color: 'success' };
      case 'cancelled':
        return { label: 'キャンセル', color: 'error' };
      default:
        return { label: status, color: 'default' };
    }
  };

  // 実施形式の表示名を取得
  const getFormatLabel = (format: string): string => {
    switch (format) {
      case 'online': return 'オンライン';
      case 'offline': return '対面';
      case 'hybrid': return 'ハイブリッド';
      default: return format;
    }
  };

  // ファイルサイズの表示形式を整形
  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`;
  };

  // ファイルダウンロード処理
  const downloadFile = async (fileId: string, fileName: string) => {
    try {
      const response = await axios.get(`/api/files/${fileId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', fileName);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (err) {
      console.error('ファイルのダウンロードに失敗しました', err);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        研修記録一覧
      </Typography>

      {/* フィルター・ソートボタン */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Button
          variant="outlined"
          startIcon={<FilterIcon />}
          onClick={() => setFilterDialogOpen(true)}
        >
          フィルター
        </Button>
        <Box>
          <FormControl variant="outlined" size="small" sx={{ minWidth: 120, mr: 1 }}>
            <InputLabel>並び順</InputLabel>
            <Select
              value={sort}
              onChange={(e) => setSort(e.target.value)}
              label="並び順"
            >
              <MenuItem value="date">日付</MenuItem>
              <MenuItem value="category">カテゴリ</MenuItem>
              <MenuItem value="name">研修名</MenuItem>
              <MenuItem value="status">状態</MenuItem>
            </Select>
          </FormControl>
          <Button
            variant="outlined"
            startIcon={<SortIcon />}
            onClick={() => setOrder(order === 'asc' ? 'desc' : 'asc')}
          >
            {order === 'asc' ?
