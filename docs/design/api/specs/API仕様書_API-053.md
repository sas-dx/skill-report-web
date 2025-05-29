# API仕様書：API-053 資格情報取得API

## 1. 基本情報

- **API ID**: API-053
- **API名称**: 資格情報取得API
- **概要**: ユーザーの資格情報を取得する
- **エンドポイント**: `/api/certifications/{user_id}`
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
| category | string | - | 資格カテゴリ | 指定がない場合は全カテゴリ |
| status | string | - | 取得状態 | "acquired", "expired", "planned"<br>指定がない場合は全状態 |
| year | number | - | 取得年度 | 指定がない場合は全期間 |
| page | number | - | ページ番号 | デフォルト: 1 |
| per_page | number | - | 1ページあたりの件数 | デフォルト: 20、最大: 100 |
| sort | string | - | ソート項目 | "acquisition_date", "expiry_date", "name", "category"<br>デフォルト: "acquisition_date" |
| order | string | - | ソート順 | "asc", "desc"<br>デフォルト: "desc" |

### 2.4 リクエスト例

```
GET /api/certifications/U12345?category=technical&status=acquired&year=2025&page=1&per_page=20&sort=acquisition_date&order=desc
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
| certifications | array | 資格情報一覧 | |

#### certifications 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| certification_id | string | 資格ID | |
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
  "total": 15,
  "page": 1,
  "per_page": 20,
  "total_pages": 1,
  "certifications": [
    {
      "certification_id": "CERT001",
      "name": "AWS Certified Solutions Architect - Professional",
      "category": "technical",
      "issuing_organization": "Amazon Web Services",
      "description": "AWSのアーキテクチャ設計に関する高度な知識と技術を証明する資格",
      "level": "expert",
      "status": "acquired",
      "acquisition_date": "2025-03-15",
      "expiry_date": "2028-03-14",
      "certification_number": "AWS-P-12345678",
      "score": 850,
      "related_skills": [
        {
          "skill_id": "S101",
          "name": "AWS",
          "category": "technical",
          "level": 5
        },
        {
          "skill_id": "S102",
          "name": "クラウドアーキテクチャ",
          "category": "technical",
          "level": 4
        }
      ],
      "attachments": [
        {
          "file_id": "F005",
          "file_name": "aws_certification.pdf",
          "file_type": "application/pdf",
          "file_size": 456789,
          "upload_date": "2025-03-16T10:30:00+09:00"
        }
      ],
      "created_at": "2025-03-16T10:30:00+09:00",
      "updated_at": "2025-03-16T10:30:00+09:00"
    },
    {
      "certification_id": "CERT002",
      "name": "情報処理安全確保支援士",
      "category": "technical",
      "issuing_organization": "IPA（情報処理推進機構）",
      "description": "サイバーセキュリティ対策の専門家としての知識と技能を認定する国家資格",
      "level": "advanced",
      "status": "acquired",
      "acquisition_date": "2024-10-01",
      "expiry_date": null,
      "certification_number": "SC-987654",
      "score": null,
      "related_skills": [
        {
          "skill_id": "S201",
          "name": "情報セキュリティ",
          "category": "technical",
          "level": 4
        },
        {
          "skill_id": "S202",
          "name": "リスク管理",
          "category": "management",
          "level": 3
        }
      ],
      "attachments": [
        {
          "file_id": "F006",
          "file_name": "security_certification.pdf",
          "file_type": "application/pdf",
          "file_size": 345678,
          "upload_date": "2024-10-05T14:20:00+09:00"
        }
      ],
      "created_at": "2024-10-05T14:20:00+09:00",
      "updated_at": "2024-10-05T14:20:00+09:00"
    },
    {
      "certification_id": "CERT003",
      "name": "TOEIC",
      "category": "language",
      "issuing_organization": "ETS",
      "description": "英語によるコミュニケーション能力を評価する国際的な試験",
      "level": "intermediate",
      "status": "acquired",
      "acquisition_date": "2024-06-20",
      "expiry_date": "2026-06-19",
      "certification_number": "TOEIC-123456",
      "score": 820,
      "related_skills": [
        {
          "skill_id": "S301",
          "name": "英語",
          "category": "language",
          "level": 4
        }
      ],
      "attachments": [
        {
          "file_id": "F007",
          "file_name": "toeic_score.pdf",
          "file_type": "application/pdf",
          "file_size": 234567,
          "upload_date": "2024-06-25T09:15:00+09:00"
        }
      ],
      "created_at": "2024-06-25T09:15:00+09:00",
      "updated_at": "2024-06-25T09:15:00+09:00"
    },
    {
      "certification_id": "CERT004",
      "name": "Google Cloud Professional Cloud Architect",
      "category": "technical",
      "issuing_organization": "Google Cloud",
      "description": "Google Cloudのアーキテクチャ設計に関する専門知識を証明する資格",
      "level": "advanced",
      "status": "planned",
      "planned_date": "2025-08-15",
      "related_skills": [
        {
          "skill_id": "S401",
          "name": "Google Cloud Platform",
          "category": "technical",
          "level": 3
        }
      ],
      "attachments": [],
      "created_at": "2025-05-10T11:30:00+09:00",
      "updated_at": "2025-05-10T11:30:00+09:00"
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
    "details": "指定されたユーザーの資格情報を参照する権限がありません"
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
3. 資格情報の取得
   - certifications テーブルから基本情報を取得
   - certification_details テーブルから詳細情報を取得
   - certification_skills テーブルから関連スキル情報を取得
   - certification_attachments テーブルから添付ファイル情報を取得
4. 検索条件による絞り込み
   - カテゴリ、取得状態、取得年度による絞り込み
5. ソート処理
   - 指定されたソート項目・ソート順でソート
6. ページング処理
   - 指定されたページ番号・1ページあたりの件数でページング
7. レスポンスの生成
   - 取得結果を整形
8. レスポンス返却

### 4.2 権限チェック

- 自身の資格情報は常に参照可能
- 他ユーザーの資格情報参照には以下のいずれかの条件を満たす必要がある
  - 対象ユーザーの直属の上長である
  - 資格情報参照権限（PERM_VIEW_CERTIFICATIONS）を持っている
  - 管理者権限（ROLE_ADMIN）を持っている
  - 研修管理者として登録されている（training_managersテーブルに登録あり）

### 4.3 検索条件の扱い

- カテゴリ（category）: 指定されたカテゴリに属する資格を検索
- 取得状態（status）: 指定された状態の資格を検索
- 取得年度（year）: 指定された年度に取得または取得予定の資格を検索

### 4.4 ソート処理

- acquisition_date: 取得日でソート
- expiry_date: 有効期限でソート
- name: 資格名でソート
- category: 資格カテゴリでソート

### 4.5 ページング処理

- page: 取得するページ番号（1から開始）
- per_page: 1ページあたりの件数（デフォルト: 20、最大: 100）

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-051](API仕様書_API-051.md) | 研修記録取得API | 研修記録情報取得 |
| [API-052](API仕様書_API-052.md) | 研修記録登録API | 研修記録情報登録 |
| [API-054](API仕様書_API-054.md) | 資格情報更新API | 資格情報更新 |
| [API-061](API仕様書_API-061.md) | レポート生成API | 資格レポート生成 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| certifications | 資格情報 | 参照（R） |
| certification_details | 資格詳細情報 | 参照（R） |
| certification_skills | 資格関連スキル | 参照（R） |
| certification_attachments | 資格添付ファイル | 参照（R） |
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
  Timer as TimerIcon,
  Attachment as AttachmentIcon,
  Download as DownloadIcon,
  Star as StarIcon
} from '@mui/icons-material';

// 型定義
interface Certification {
  certification_id: string;
  name: string;
  category: string;
  issuing_organization: string;
  description: string;
  level: string;
  status: string;
  acquisition_date: string | null;
  expiry_date: string | null;
  planned_date: string | null;
  certification_number: string | null;
  score: number | null;
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

interface CertificationResponse {
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
  certifications: Certification[];
}

const CertificationList: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const [searchParams, setSearchParams] = useSearchParams();
  const [certifications, setCertifications] = useState<Certification[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState<number>(0);
  const [page, setPage] = useState<number>(parseInt(searchParams.get('page') || '1', 10));
  const [perPage, setPerPage] = useState<number>(parseInt(searchParams.get('per_page') || '20', 10));
  const [totalPages, setTotalPages] = useState<number>(0);
  const [category, setCategory] = useState<string>(searchParams.get('category') || '');
  const [status, setStatus] = useState<string>(searchParams.get('status') || '');
  const [year, setYear] = useState<string>(searchParams.get('year') || '');
  const [sort, setSort] = useState<string>(searchParams.get('sort') || 'acquisition_date');
  const [order, setOrder] = useState<string>(searchParams.get('order') || 'desc');
  const [selectedCertification, setSelectedCertification] = useState<Certification | null>(null);
  const [detailDialogOpen, setDetailDialogOpen] = useState<boolean>(false);
  const [filterDialogOpen, setFilterDialogOpen] = useState<boolean>(false);

  // 資格情報データの取得
  const fetchCertifications = async () => {
    try {
      setLoading(true);
      setError(null);

      // クエリパラメータの構築
      const params = new URLSearchParams();
      if (category) params.append('category', category);
      if (status) params.append('status', status);
      if (year) params.append('year', year);
      params.append('page', page.toString());
      params.append('per_page', perPage.toString());
      params.append('sort', sort);
      params.append('order', order);

      // APIリクエスト
      const response = await axios.get<CertificationResponse>(
        `/api/certifications/${userId}?${params.toString()}`,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Accept': 'application/json'
          }
        }
      );

      // レスポンスデータの設定
      setCertifications(response.data.certifications);
      setTotal(response.data.total);
      setPage(response.data.page);
      setPerPage(response.data.per_page);
      setTotalPages(response.data.total_pages);

      // URLのクエリパラメータを更新
      setSearchParams(params);
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const errorData = err.response.data;
        setError(errorData.error?.message || '資格情報の取得に失敗しました');
      } else {
        setError('資格情報の取得中にエラーが発生しました');
      }
    } finally {
      setLoading(false);
    }
  };

  // 初回レンダリング時とフィルター変更時にデータ取得
  useEffect(() => {
    fetchCertifications();
  }, [userId, page, perPage, sort, order]);

  // フィルター適用
  const applyFilters = () => {
    setPage(1); // フィルター変更時は1ページ目に戻る
    fetchCertifications();
    setFilterDialogOpen(false);
  };

  // フィルターリセット
  const resetFilters = () => {
    setCategory('');
    setStatus('');
    setYear('');
    setPage(1);
    setFilterDialogOpen(false);
    // リセット後にデータ再取得
    setTimeout(() => {
      fetchCertifications();
    }, 0);
  };

  // 資格詳細ダイアログを開く
  const openDetailDialog = (certification: Certification) => {
    setSelectedCertification(certification);
    setDetailDialogOpen(true);
  };

  // 資格カテゴリの表示名を取得
  const getCategoryLabel = (category: string): string => {
    switch (category) {
      case 'technical': return '技術';
      case 'business': return 'ビジネス';
      case 'management': return 'マネジメント';
      case 'language': return '言語';
      case 'other': return 'その他';
      default: return category;
    }
  };

  // 資格レベルの表示名を取得
  const getLevelLabel = (level: string): string => {
    switch (level) {
      case 'basic': return '基本';
      case 'intermediate': return '中級';
      case 'advanced': return '上級';
      case 'expert': return '専門家';
      default: return level;
    }
  };

  // 資格状態の表示名とカラーを取得
  const getStatusInfo = (status: string): { label: string; color: 'default' | 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning' } => {
    switch (status) {
      case 'acquired':
        return { label: '取得済', color: 'success' };
      case 'expired':
        return { label: '期限切れ', color: 'error' };
      case 'planned':
        return { label: '取得予定', color: 'info' };
      default:
        return { label: status, color: 'default' };
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
        資格情報一覧
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
              <MenuItem value="acquisition_date">取得日</MenuItem>
              <MenuItem value="expiry_date">有効期限</MenuItem>
              <MenuItem value="name">資格名</MenuItem>
              <MenuItem value="category">カテゴリ</MenuItem>
            </Select>
          </FormControl>
          <Button
            variant="outlined"
            startIcon={<SortIcon />}
            onClick={() => setOrder(order === 'asc' ? 'desc' : 'asc')}
          >
            {order === 'asc' ?
