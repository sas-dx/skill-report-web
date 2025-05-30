# API定義書：API-062 レポート取得API

## 1. 基本情報

- **API ID**: API-062
- **API名称**: レポート取得API
- **概要**: 生成されたレポートの情報取得、状態確認、ダウンロードを行う
- **エンドポイント**: `/api/reports/{report_id}`
- **HTTPメソッド**: GET
- **リクエスト形式**: -
- **レスポンス形式**: JSON / ファイル（ダウンロード時）
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
| Accept | - | レスポンス形式 | application/json |

### 2.2 パスパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| report_id | string | ○ | レポートID | API-061で生成されたレポートID |

### 2.3 クエリパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| action | string | - | 実行アクション | "status", "download", "cancel"<br>デフォルト: なし（レポート情報取得） |

### 2.4 リクエスト例（レポート情報取得）

```
GET /api/reports/RPT-2025052801
```

### 2.5 リクエスト例（レポート状態確認）

```
GET /api/reports/RPT-2025052801?action=status
```

### 2.6 リクエスト例（レポートダウンロード）

```
GET /api/reports/RPT-2025052801?action=download
```

### 2.7 リクエスト例（レポート生成キャンセル）

```
GET /api/reports/RPT-2025052801?action=cancel
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）- レポート情報取得

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| report_id | string | レポートID | |
| report_type | string | レポートタイプ | "skill", "training", "certification", "career", "work", "summary" |
| title | string | レポートタイトル | |
| description | string | レポート説明 | |
| status | string | レポート生成状態 | "queued", "processing", "completed", "failed", "cancelled" |
| progress | number | 進捗率 | 0-100の範囲 |
| error_message | string | エラーメッセージ | status="failed"の場合のみ |
| created_at | string | 作成日時 | ISO 8601形式 |
| created_by | string | 作成者ID | |
| completed_at | string | 完了日時 | ISO 8601形式<br>status="completed"または"failed"の場合のみ |
| target_users | array | 対象ユーザーID配列 | |
| period | object | 対象期間 | |
| filters | object | フィルター条件 | |
| grouping | array | グループ化条件 | |
| sort | object | ソート条件 | |
| output_format | string | 出力形式 | "pdf", "excel", "csv", "json" |
| file_size | number | ファイルサイズ | バイト単位<br>status="completed"の場合のみ |
| download_url | string | ダウンロードURL | status="completed"の場合のみ |
| download_count | number | ダウンロード回数 | |
| expiry_date | string | 有効期限 | ISO 8601形式 |

### 3.2 正常時レスポンス例（レポート情報取得）

```json
{
  "report_id": "RPT-2025052801",
  "report_type": "skill",
  "title": "技術スキル分布レポート",
  "description": "部門別の技術スキル分布状況",
  "status": "completed",
  "progress": 100,
  "created_at": "2025-05-28T10:15:30+09:00",
  "created_by": "U12345",
  "completed_at": "2025-05-28T10:20:45+09:00",
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
  "file_size": 2456789,
  "download_url": "/api/reports/RPT-2025052801/download",
  "download_count": 0,
  "expiry_date": "2025-06-27T23:59:59+09:00"
}
```

### 3.3 正常時レスポンス（200 OK）- レポート状態確認

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| report_id | string | レポートID | |
| status | string | レポート生成状態 | "queued", "processing", "completed", "failed", "cancelled" |
| progress | number | 進捗率 | 0-100の範囲 |
| message | string | 状態メッセージ | |
| error_message | string | エラーメッセージ | status="failed"の場合のみ |
| estimated_completion_time | string | 推定完了時間 | ISO 8601形式<br>status="queued"または"processing"の場合のみ |
| completed_at | string | 完了日時 | ISO 8601形式<br>status="completed"または"failed"の場合のみ |
| download_url | string | ダウンロードURL | status="completed"の場合のみ |

### 3.4 正常時レスポンス例（レポート状態確認 - 処理中）

```json
{
  "report_id": "RPT-2025052801",
  "status": "processing",
  "progress": 65,
  "message": "データ集計中...",
  "estimated_completion_time": "2025-05-28T10:20:30+09:00"
}
```

### 3.5 正常時レスポンス例（レポート状態確認 - 完了）

```json
{
  "report_id": "RPT-2025052801",
  "status": "completed",
  "progress": 100,
  "message": "レポート生成が完了しました",
  "completed_at": "2025-05-28T10:20:45+09:00",
  "download_url": "/api/reports/RPT-2025052801/download"
}
```

### 3.6 正常時レスポンス（200 OK）- レポートダウンロード

レポートファイルのバイナリデータが返却されます。レスポンスヘッダには以下の情報が含まれます。

| ヘッダ名 | 説明 | 備考 |
|---------|------|------|
| Content-Type | ファイルのMIMEタイプ | 出力形式に応じたMIMEタイプ |
| Content-Disposition | ファイルのダウンロード情報 | attachment; filename="レポート名.拡張子" |
| Content-Length | ファイルサイズ | バイト単位 |

### 3.7 正常時レスポンス（200 OK）- レポート生成キャンセル

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| report_id | string | レポートID | |
| status | string | レポート生成状態 | "cancelled" |
| message | string | 状態メッセージ | |
| cancelled_at | string | キャンセル日時 | ISO 8601形式 |

### 3.8 正常時レスポンス例（レポート生成キャンセル）

```json
{
  "report_id": "RPT-2025052801",
  "status": "cancelled",
  "message": "レポート生成がキャンセルされました",
  "cancelled_at": "2025-05-28T10:18:30+09:00"
}
```

### 3.9 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_ACTION | アクションが不正です | 存在しないアクション |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | レポート参照権限なし |
| 404 Not Found | REPORT_NOT_FOUND | レポートが見つかりません | 指定されたレポートIDが存在しない |
| 409 Conflict | CANNOT_CANCEL | キャンセルできません | 既に完了または失敗したレポート |
| 410 Gone | REPORT_EXPIRED | レポートの有効期限が切れています | 保存期間を過ぎたレポート |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.10 エラー時レスポンス例

```json
{
  "error": {
    "code": "REPORT_NOT_FOUND",
    "message": "レポートが見つかりません",
    "details": "指定されたレポートIDは存在しないか、アクセス権限がありません"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー（レポート情報取得）

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - レポート参照権限のチェック
2. レポートIDの存在チェック
   - 指定されたレポートIDの存在確認
   - レポート作成者または権限を持つユーザーかどうかの確認
3. レポート情報の取得
   - reports テーブルから基本情報を取得
   - report_details テーブルから詳細情報を取得
   - report_users テーブルから対象ユーザー情報を取得
4. レスポンスの生成
   - レポート情報を含むレスポンスを生成
5. レスポンス返却

### 4.2 処理フロー（レポート状態確認）

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - レポート参照権限のチェック
2. レポートIDの存在チェック
   - 指定されたレポートIDの存在確認
   - レポート作成者または権限を持つユーザーかどうかの確認
3. レポート状態の取得
   - reports テーブルから状態情報を取得
4. レスポンスの生成
   - レポート状態情報を含むレスポンスを生成
5. レスポンス返却

### 4.3 処理フロー（レポートダウンロード）

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - レポート参照権限のチェック
2. レポートIDの存在チェック
   - 指定されたレポートIDの存在確認
   - レポート作成者または権限を持つユーザーかどうかの確認
3. レポート状態の確認
   - レポート生成が完了しているかどうかの確認
4. レポートファイルの取得
   - ファイルストレージからレポートファイルを取得
5. ダウンロード回数の更新
   - reports テーブルのダウンロード回数をインクリメント
6. レスポンスの生成
   - レポートファイルのバイナリデータを含むレスポンスを生成
   - 適切なレスポンスヘッダを設定
7. レスポンス返却

### 4.4 処理フロー（レポート生成キャンセル）

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - レポート参照権限のチェック
2. レポートIDの存在チェック
   - 指定されたレポートIDの存在確認
   - レポート作成者または権限を持つユーザーかどうかの確認
3. レポート状態の確認
   - レポートがキャンセル可能な状態（queued または processing）かどうかの確認
4. レポート生成タスクのキャンセル
   - 非同期処理キューからタスクを削除
   - reports テーブルの状態を "cancelled" に更新
5. レスポンスの生成
   - キャンセル結果を含むレスポンスを生成
6. レスポンス返却

### 4.5 権限チェック

- レポート参照には以下のいずれかの条件を満たす必要がある
  - レポートの作成者である
  - レポート参照権限（PERM_VIEW_REPORTS）を持っている
  - 管理者権限（ROLE_ADMIN）を持っている
  - レポートの対象ユーザーに含まれており、かつ自身のみのデータを含むレポートである

### 4.6 レポート状態

- queued: レポート生成タスクがキューに登録された状態
- processing: レポート生成処理が実行中の状態
- completed: レポート生成が正常に完了した状態
- failed: レポート生成中にエラーが発生した状態
- cancelled: レポート生成がユーザーによってキャンセルされた状態

### 4.7 出力形式別MIMEタイプ

- pdf: application/pdf
- excel: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
- csv: text/csv
- json: application/json

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-061](API仕様書_API-061.md) | レポート生成API | レポート生成リクエスト |
| [API-051](API仕様書_API-051.md) | 研修記録取得API | 研修データの取得 |
| [API-053](API仕様書_API-053.md) | 資格情報取得API | 資格データの取得 |
| [API-021](API仕様書_API-021.md) | スキル情報取得API | スキルデータの取得 |
| [API-031](API仕様書_API-031.md) | キャリア目標取得API | キャリアデータの取得 |
| [API-041](API仕様書_API-041.md) | 作業実績取得API | 作業実績データの取得 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| reports | レポート基本情報 | 参照/更新（RU） |
| report_details | レポート詳細情報 | 参照（R） |
| report_users | レポート対象ユーザー | 参照（R） |
| files | ファイル情報 | 参照（R） |

### 5.3 注意事項・補足

- レポートの保存期間は生成から30日間
- 保存期間を過ぎたレポートは自動的に削除される
- レポートダウンロード時には、ダウンロード回数がインクリメントされる
- レポート生成のキャンセルは、状態が "queued" または "processing" の場合のみ可能
- 状態が "completed", "failed", "cancelled" のレポートはキャンセルできない
- レポートファイルのダウンロードは、状態が "completed" の場合のみ可能
- 大容量のレポートファイルのダウンロードには時間がかかる場合がある
- レポートの進捗率（progress）は、レポート生成処理の進行状況を0-100の範囲で表す
- 推定完了時間（estimated_completion_time）は、現在の処理状況から算出された予測値であり、実際の完了時間と異なる場合がある

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Button,
  Typography,
  Paper,
  Box,
  Chip,
  CircularProgress,
  Grid,
  Card,
  CardContent,
  CardActions,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Alert,
  LinearProgress,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions
} from '@mui/material';
import {
  Description as DescriptionIcon,
  CloudDownload as CloudDownloadIcon,
  Cancel as CancelIcon,
  Refresh as RefreshIcon,
  ArrowBack as ArrowBackIcon,
  AccessTime as AccessTimeIcon,
  Person as PersonIcon,
  FilterList as FilterIcon,
  Sort as SortIcon,
  Category as CategoryIcon,
  DateRange as DateRangeIcon,
  Error as ErrorIcon,
  CheckCircle as CheckCircleIcon
} from '@mui/icons-material';

// 型定義
interface ReportDetail {
  report_id: string;
  report_type: string;
  title: string;
  description: string;
  status: 'queued' | 'processing' | 'completed' | 'failed' | 'cancelled';
  progress: number;
  error_message?: string;
  created_at: string;
  created_by: string;
  completed_at?: string;
  target_users: string[];
  period?: {
    start_date?: string;
    end_date?: string;
    fiscal_year?: number;
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
  file_size?: number;
  download_url?: string;
  download_count: number;
  expiry_date: string;
}

interface ReportStatus {
  report_id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed' | 'cancelled';
  progress: number;
  message: string;
  error_message?: string;
  estimated_completion_time?: string;
  completed_at?: string;
  download_url?: string;
}

const ReportDetailPage: React.FC = () => {
  const { reportId } = useParams<{ reportId: string }>();
  const navigate = useNavigate();
  const [report, setReport] = useState<ReportDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [statusPolling, setStatusPolling] = useState<boolean>(false);
  const [cancelDialogOpen, setCancelDialogOpen] = useState<boolean>(false);
  
  // レポート情報の取得
  const fetchReportDetail = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.get(`/api/reports/${reportId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Accept': 'application/json'
        }
      });
      
      setReport(response.data);
      
      // レポートが処理中の場合はステータスポーリングを開始
      if (response.data.status === 'queued' || response.data.status === 'processing') {
        setStatusPolling(true);
      } else {
        setStatusPolling(false);
      }
      
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const errorData = err.response.data;
        setError(errorData.error?.message || 'レポート情報の取得に失敗しました');
      } else {
        setError('レポート情報の取得中にエラーが発生しました');
      }
      setStatusPolling(false);
    } finally {
      setLoading(false);
    }
  };
  
  // レポート状態の確認
  const checkReportStatus = async () => {
    if (!reportId || !statusPolling) return;
    
    try {
      const response = await axios.get<ReportStatus>(`/api/reports/${reportId}?action=status`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Accept': 'application/json'
        }
      });
      
      // レポート状態の更新
      if (report) {
        setReport({
          ...report,
          status: response.data.status,
          progress: response.data.progress,
          completed_at: response.data.completed_at,
          download_url: response.data.download_url
        });
      }
      
      // 処理が完了またはエラーの場合はポーリングを停止
      if (response.data.status !== 'queued' && response.data.status !== 'processing') {
        setStatusPolling(false);
        // 完全な情報を取得するために再度レポート詳細を取得
        fetchReportDetail();
      }
      
    } catch (err) {
      console.error('レポート状態の確認中にエラーが発生しました', err);
      setStatusPolling(false);
    }
  };
  
  // レポートのダウンロード
  const downloadReport = () => {
    if (!report || !report.download_url) return;
    
    // 新しいタブでダウンロードURLを開く
    window.open(`/api/reports/${reportId}?action=download`, '_blank');
  };
  
  // レポート生成のキャンセル
  const cancelReportGeneration = async () => {
    try {
      const response = await axios.get(`/api/reports/${reportId}?action=cancel`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Accept': 'application/json'
        }
      });
      
      // レポート状態の更新
      if (report) {
        setReport({
          ...report,
          status: 'cancelled',
          progress: 0
        });
      }
      
      setStatusPolling(false);
      setCancelDialogOpen(false);
      
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const errorData = err.response.data;
        setError(errorData.error?.message || 'レポート生成のキャンセルに失敗しました');
      } else {
        setError('レポート生成のキャンセル中にエラーが発生しました');
      }
      setCancelDialogOpen(false);
    }
  };
  
  // 初回レンダリング時にレポート情報を取得
  useEffect(() => {
    fetchReportDetail();
    
    // コンポーネントのクリーンアップ時にポーリングを停止
    return () => {
      setStatusPolling(false);
    };
  }, [reportId]);
  
  // ステータスポーリングの設定
  useEffect(() => {
    let intervalId: NodeJS.Timeout;
    
    if (statusPolling) {
      // 5秒ごとにレポート状態を確認
      intervalId = setInterval(checkReportStatus, 5000);
    }
    
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [statusPolling, report]);
  
  // レポートタイプの表示名を取得
  const getReportTypeName = (type: string): string => {
    switch (type) {
      case 'skill': return 'スキルレポート';
      case 'training': return '研修レポート';
      case 'certification': return '資格レポート';
      case 'career': return 'キャリアレポート';
      case 'work': return '作業実績レポート';
      case 'summary': return '総合サマリーレポート';
      default: return type;
    }
  };
  
  // レポート状態の表示情報を取得
  const getStatusInfo = (status: string): { label: string; color: 'default' | 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning' } => {
    switch (status) {
      case 'queued':
        return { label: '待機中', color: 'info' };
      case 'processing':
        return { label: '処理中', color: 'primary' };
      case 'completed':
        return { label: '完了', color: 'success' };
      case 'failed':
        return { label: '失敗', color: 'error' };
      case 'cancelled':
        return { label: 'キャンセル', color: 'warning' };
      default:
        return { label: status, color: 'default' };
    }
  };
  
  // 出力形式の表示名を取得
  const getOutputFormatName = (format: string): string => {
    switch (format) {
      case 'pdf': return 'PDF';
      case 'excel': return 'Excel';
      case 'csv': return 'CSV';
      case 'json': return 'JSON';
      default: return format;
    }
  };
  
  // ファイルサイズの表示形式を整形
  const formatFileSize = (bytes?: number): string => {
    if (bytes === undefined) return '-';
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`;
  };
  
  // 日時の表示形式を整形
  const formatDateTime = (dateTime?: string): string => {
    if (!dateTime) return '-';
    return new Date(dateTime).toLocaleString('ja-JP', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };
  
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }
  
  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">{error}</Alert>
        <Box sx={{ mt: 2 }}>
          <Button
            variant="outlined"
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/reports')}
          >
            レポート一覧に戻る
          </Button>
