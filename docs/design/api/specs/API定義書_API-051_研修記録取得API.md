# API定義書：API-051 研修記録取得API

## 1. 基本情報

- **API ID**: API-051
- **API名称**: 研修記録取得API
- **概要**: 指定されたユーザーの研修記録情報を取得する
- **エンドポイント**: `/api/trainings/{user_id}`
- **HTTPメソッド**: GET
- **リクエスト形式**: URL Path Parameter + Query Parameter
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-TRAINING](画面設計書_SCR-TRAINING.md)
- **作成日**: 2025/05/28
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/28 初版作成

---

## 2. リクエスト仕様

### 2.1 パスパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| user_id | string | ○ | 取得対象のユーザーID | 半角英数字、4〜20文字 |

### 2.2 クエリパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| year | number | - | 取得対象年度 | 西暦4桁<br>指定なしの場合は全年度 |
| status | string | - | 研修ステータス | "planned", "registered", "completed", "cancelled"のいずれか<br>複数指定する場合はカンマ区切り |
| category | string | - | 研修カテゴリ | "technical", "business", "management", "communication", "other"のいずれか<br>複数指定する場合はカンマ区切り |
| from_date | string | - | 開始日 | ISO 8601形式（YYYY-MM-DD）<br>指定した日付以降の研修を取得 |
| to_date | string | - | 終了日 | ISO 8601形式（YYYY-MM-DD）<br>指定した日付以前の研修を取得 |
| include_details | boolean | - | 詳細情報を含めるか | デフォルト：false |
| page | number | - | ページ番号 | 1以上の整数<br>デフォルト：1 |
| per_page | number | - | 1ページあたりの件数 | 1〜50の整数<br>デフォルト：20 |
| sort_by | string | - | ソート項目 | "date", "category", "name", "status"のいずれか<br>デフォルト："date" |
| sort_order | string | - | ソート順 | "asc"（昇順）, "desc"（降順）のいずれか<br>デフォルト："desc" |

### 2.3 リクエスト例

```
GET /api/trainings/tanaka.taro?year=2025&status=completed,registered&category=technical&from_date=2025-01-01&to_date=2025-12-31&include_details=true&page=1&per_page=20&sort_by=date&sort_order=desc
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| total_count | number | 総レコード数 | 検索条件に合致する全レコード数 |
| page | number | 現在のページ番号 | |
| per_page | number | 1ページあたりの件数 | |
| total_pages | number | 総ページ数 | |
| trainings | array | 研修記録の配列 | 詳細は以下参照 |
| summary | object | 集計情報 | 詳細は以下参照 |

#### trainings 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| training_id | string | 研修ID | UUID形式 |
| training_name | string | 研修名 | |
| category | string | 研修カテゴリ | "technical", "business", "management", "communication", "other"のいずれか |
| format | string | 研修形式 | "online", "offline", "hybrid", "self_study"のいずれか |
| start_date | string | 開始日 | ISO 8601形式（YYYY-MM-DD） |
| end_date | string | 終了日 | ISO 8601形式（YYYY-MM-DD） |
| duration_hours | number | 研修時間（時間） | |
| status | string | ステータス | "planned", "registered", "completed", "cancelled"のいずれか |
| completion_date | string | 修了日 | ISO 8601形式（YYYY-MM-DD）<br>status="completed"の場合のみ |
| provider | string | 提供元 | |
| related_skills | array | 関連スキル | スキルIDの配列 |
| details | object | 詳細情報 | include_details=trueの場合のみ<br>詳細は以下参照 |

#### details オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| description | string | 研修内容 | |
| objectives | array | 学習目標 | 文字列の配列 |
| materials | array | 教材情報 | 詳細は以下参照 |
| evaluation | object | 評価情報 | status="completed"の場合のみ<br>詳細は以下参照 |
| feedback | string | フィードバック | status="completed"の場合のみ |
| notes | string | 備考 | |

#### materials 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| title | string | 教材タイトル | |
| type | string | 教材種別 | "document", "video", "exercise", "other"のいずれか |
| url | string | URL | |

#### evaluation オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| score | number | 評価スコア | 0-100 |
| passed | boolean | 合格フラグ | |
| certificate_id | string | 認定証ID | 認定証がある場合のみ |
| certificate_url | string | 認定証URL | 認定証がある場合のみ |
| evaluator | string | 評価者 | |
| comments | string | 評価コメント | |

#### summary オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total_trainings | number | 研修総数 | |
| total_hours | number | 総研修時間 | |
| completed_trainings | number | 修了済研修数 | |
| planned_trainings | number | 予定研修数 | |
| by_category | object | カテゴリ別集計 | カテゴリごとの研修数 |
| by_year | object | 年度別集計 | 年度ごとの研修数 |
| completion_rate | number | 修了率（%） | 小数点第1位まで |

### 3.2 正常時レスポンス例

```json
{
  "user_id": "tanaka.taro",
  "total_count": 15,
  "page": 1,
  "per_page": 20,
  "total_pages": 1,
  "trainings": [
    {
      "training_id": "tr-12345-abcde-67890",
      "training_name": "Kubernetes実践ワークショップ",
      "category": "technical",
      "format": "hybrid",
      "start_date": "2025-05-15",
      "end_date": "2025-05-16",
      "duration_hours": 16,
      "status": "completed",
      "completion_date": "2025-05-16",
      "provider": "クラウドネイティブ技術研究所",
      "related_skills": ["kubernetes", "docker", "container-orchestration"],
      "details": {
        "description": "Kubernetesの基本概念から実践的なデプロイメント、運用管理までを学ぶハンズオン形式のワークショップ。マイクロサービスアーキテクチャの実装方法も含む。",
        "objectives": [
          "Kubernetesの基本概念と構成要素を理解する",
          "コンテナ化されたアプリケーションのデプロイと管理ができるようになる",
          "マイクロサービスアーキテクチャの実装方法を習得する"
        ],
        "materials": [
          {
            "title": "Kubernetes実践ガイド",
            "type": "document",
            "url": "https://example.com/materials/k8s-guide.pdf"
          },
          {
            "title": "ハンズオン演習環境",
            "type": "exercise",
            "url": "https://k8s-workshop.example.com/"
          }
        ],
        "evaluation": {
          "score": 92,
          "passed": true,
          "certificate_id": "CERT-K8S-2025-12345",
          "certificate_url": "https://example.com/certificates/CERT-K8S-2025-12345",
          "evaluator": "山田 講師",
          "comments": "実践的な理解度が高く、演習でも優れたソリューションを実装していました。特にスケーリングとセルフヒーリングの概念理解が素晴らしい。"
        },
        "feedback": "実際のプロジェクトで活用できる実践的な内容で非常に有益だった。特にトラブルシューティングの部分が参考になった。",
        "notes": "次回はAdvancedコースの受講を検討"
      }
    },
    {
      "training_id": "tr-67890-fghij-12345",
      "training_name": "プロジェクトマネジメント基礎",
      "category": "management",
      "format": "online",
      "start_date": "2025-04-10",
      "end_date": "2025-04-11",
      "duration_hours": 8,
      "status": "completed",
      "completion_date": "2025-04-11",
      "provider": "PMラーニングセンター",
      "related_skills": ["project-management", "team-leadership", "agile-methodology"],
      "details": {
        "description": "プロジェクトマネジメントの基礎知識とスキルを習得するオンライン研修。アジャイル手法とウォーターフォール手法の比較も含む。",
        "objectives": [
          "プロジェクト計画の立て方を習得する",
          "リスク管理の基本を理解する",
          "チームマネジメントの基礎を学ぶ"
        ],
        "materials": [
          {
            "title": "PMハンドブック",
            "type": "document",
            "url": "https://example.com/materials/pm-handbook.pdf"
          },
          {
            "title": "ケーススタディ動画",
            "type": "video",
            "url": "https://example.com/videos/pm-case-studies"
          }
        ],
        "evaluation": {
          "score": 85,
          "passed": true,
          "certificate_id": "CERT-PM-2025-67890",
          "certificate_url": "https://example.com/certificates/CERT-PM-2025-67890",
          "evaluator": "佐藤 講師",
          "comments": "基本的な概念をしっかり理解しています。実践的なケーススタディでも適切な判断ができていました。"
        },
        "feedback": "オンライン形式でも双方向のディスカッションが活発で学びが多かった。実務での応用方法がより具体的だとさらに良かった。",
        "notes": "今後はアジャイル開発の専門研修も検討したい"
      }
    }
  ],
  "summary": {
    "total_trainings": 15,
    "total_hours": 120,
    "completed_trainings": 10,
    "planned_trainings": 5,
    "by_category": {
      "technical": 8,
      "business": 2,
      "management": 3,
      "communication": 1,
      "other": 1
    },
    "by_year": {
      "2023": 3,
      "2024": 5,
      "2025": 7
    },
    "completion_rate": 66.7
  }
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他者の研修記録閲覧権限なし |
| 404 Not Found | USER_NOT_FOUND | 指定されたユーザーが見つかりません | 存在しないユーザーID |
| 404 Not Found | NO_TRAININGS_FOUND | 指定された条件の研修記録が見つかりません | 条件に合致するレコードなし |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "パラメータが不正です",
    "details": "指定されたstatusの値が不正です。'planned', 'registered', 'completed', 'cancelled'のいずれかを指定してください。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - 研修記録閲覧権限の確認
   - 他者の研修記録閲覧権限の確認（自分以外のuser_idの場合）
2. リクエストパラメータの検証
   - user_idの形式チェック
   - 日付パラメータの形式チェック（指定されている場合）
   - ステータス・カテゴリの値チェック
   - ページネーションパラメータの範囲チェック
3. ユーザーの存在確認
   - 指定されたuser_idのユーザーが存在するか確認
4. 検索条件の構築
   - 指定されたパラメータに基づいて検索条件を構築
5. 研修記録データの取得
   - 検索条件に合致するレコードの総数を取得
   - ページネーション情報に基づいて対象レコードを取得
6. 詳細情報の取得（include_details=trueの場合）
   - 各研修の詳細情報を取得
7. 集計情報の計算
   - カテゴリ別、年度別の集計を実施
   - 修了率の計算
8. レスポンスの生成
   - 取得したデータを整形してJSONレスポンスを生成
9. レスポンス返却

### 4.2 アクセス制御ルール

- 自分自身の研修記録：閲覧可能
- 部下の研修記録：マネージャーは閲覧可能
- 同部署の研修記録サマリー：部署管理者は閲覧可能
- 全社員の研修記録サマリー：人事担当者・管理者は閲覧可能
- 詳細情報（評価情報含む）：本人・直属の上司・人事担当者のみ閲覧可能

### 4.3 パフォーマンス要件

- 応答時間：平均300ms以内
- タイムアウト：5秒
- キャッシュ：ユーザー別・検索条件別に30分キャッシュ
- 同時リクエスト：最大30リクエスト/秒
- 最大レコード取得数：一度に最大50件まで

### 4.4 検索条件の組み合わせルール

- 複数のステータスやカテゴリを指定する場合はOR条件で検索
- 年度指定（year）と日付範囲指定（from_date, to_date）が両方ある場合は日付範囲を優先
- ソート条件は1つのみ指定可能

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-052](API仕様書_API-052.md) | 研修記録登録API | 研修記録情報の登録 |
| [API-053](API仕様書_API-053.md) | 資格情報取得API | 資格情報取得 |
| [API-054](API仕様書_API-054.md) | 資格情報更新API | 資格情報更新 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| trainings | 研修情報 | 参照（R） |
| user_trainings | ユーザー研修履歴 | 参照（R） |
| training_materials | 研修教材 | 参照（R） |
| training_evaluations | 研修評価 | 参照（R） |
| skills | スキル情報 | 参照（R） |
| training_categories | 研修カテゴリ | 参照（R） |

### 5.3 注意事項・補足

- 研修記録は過去5年分を参照可能
- 研修ステータスの遷移：planned → registered → completed/cancelled
- 研修形式（format）は以下の定義に従う
  - online: オンライン研修（リアルタイム）
  - offline: 対面研修
  - hybrid: オンライン・対面併用
  - self_study: 自己学習（eラーニング等）
- 評価スコアは0-100の範囲で設定
- 認定証がある場合は証明書IDとURLを記録
- 研修記録は人材育成計画やスキル評価と連携
- 集計情報は指定された検索条件に基づいて計算

---

## 6. サンプルコード

### 6.1 研修記録取得例（JavaScript/Fetch API）

```javascript
/**
 * ユーザーの研修記録情報を取得する関数
 * @param {string} userId - ユーザーID
 * @param {Object} options - 検索オプション
 * @param {number} [options.year] - 取得対象年度
 * @param {string|string[]} [options.status] - 研修ステータス（単一または配列）
 * @param {string|string[]} [options.category] - 研修カテゴリ（単一または配列）
 * @param {string} [options.fromDate] - 開始日（YYYY-MM-DD）
 * @param {string} [options.toDate] - 終了日（YYYY-MM-DD）
 * @param {boolean} [options.includeDetails] - 詳細情報を含めるか
 * @param {number} [options.page] - ページ番号
 * @param {number} [options.perPage] - 1ページあたりの件数
 * @param {string} [options.sortBy] - ソート項目
 * @param {string} [options.sortOrder] - ソート順
 * @returns {Promise<Object>} 研修記録情報
 */
async function getUserTrainings(userId, options = {}) {
  try {
    // クエリパラメータの構築
    const queryParams = new URLSearchParams();
    if (options.year) queryParams.append('year', options.year);
    
    // 配列パラメータの処理
    if (options.status) {
      const statusValue = Array.isArray(options.status) ? options.status.join(',') : options.status;
      queryParams.append('status', statusValue);
    }
    
    if (options.category) {
      const categoryValue = Array.isArray(options.category) ? options.category.join(',') : options.category;
      queryParams.append('category', categoryValue);
    }
    
    if (options.fromDate) queryParams.append('from_date', options.fromDate);
    if (options.toDate) queryParams.append('to_date', options.toDate);
    if (options.includeDetails !== undefined) queryParams.append('include_details', options.includeDetails);
    if (options.page) queryParams.append('page', options.page);
    if (options.perPage) queryParams.append('per_page', options.perPage);
    if (options.sortBy) queryParams.append('sort_by', options.sortBy);
    if (options.sortOrder) queryParams.append('sort_order', options.sortOrder);
    
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
    
    // APIリクエスト
    const response = await fetch(`https://api.example.com/api/trainings/${userId}${queryString}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`,
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error.message || '研修記録情報の取得に失敗しました');
    }
    
    return await response.json();
  } catch (error) {
    console.error('研修記録情報取得エラー:', error);
    throw error;
  }
}
```

### 6.2 研修記録一覧表示コンポーネント例（React）

```jsx
import React, { useState, useEffect } from 'react';
import { getUserTrainings } from '../api/trainingApi';
import TrainingList from './TrainingList';
import TrainingSummary from './TrainingSummary';
import FilterPanel from './FilterPanel';
import Pagination from '../common/Pagination';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';
import { formatDate } from '../utils/dateUtils';

const TrainingRecordsView = ({ userId }) => {
  // 状態管理
  const [trainingData, setTrainingData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    year: new Date().getFullYear(),
    status: [],
    category: [],
    fromDate: '',
    toDate: '',
    includeDetails: true,
    page: 1,
    perPage: 20,
    sortBy: 'date',
    sortOrder: 'desc'
  });
  
  // 研修記録データの取得
  useEffect(() => {
    const fetchTrainingRecords = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const data = await getUserTrainings(userId, filters);
        setTrainingData(data);
      } catch (err) {
        setError(err.message || '研修記録情報の取得に失敗しました');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchTrainingRecords();
  }, [userId, filters]);
  
  // フィルター変更ハンドラ
  const handleFilterChange = (newFilters) => {
    setFilters({
      ...filters,
      ...newFilters,
      page: 1 // フィルター変更時は1ページ目に戻す
    });
  };
  
  // ページ変更ハンドラ
  const handlePageChange = (newPage) => {
    setFilters({
      ...filters,
      page: newPage
    });
  };
  
  // ステータスフィルター変更ハンドラ
  const handleStatusFilterChange = (status, isChecked) => {
    const newStatus = [...filters.status];
    
    if (isChecked) {
      newStatus.push(status);
    } else {
      const index = newStatus.indexOf(status);
      if (index !== -1) {
        newStatus.splice(index, 1);
      }
    }
    
    setFilters({
      ...filters,
      status: newStatus,
      page: 1
    });
  };
  
  // カテゴリフィルター変更ハンドラ
  const handleCategoryFilterChange = (category, isChecked) => {
    const newCategory = [...filters.category];
    
    if (isChecked) {
      newCategory.push(category);
    } else {
      const index = newCategory.indexOf(category);
      if (index !== -1) {
        newCategory.splice(index, 1);
      }
    }
    
    setFilters({
      ...filters,
      category: newCategory,
      page: 1
    });
  };
  
  // 詳細表示切替ハンドラ
  const handleDetailsToggle = () => {
    setFilters({
      ...filters,
      includeDetails: !filters.includeDetails
    });
  };
  
  if (isLoading) {
    return <LoadingSpinner message="研修記録情報を読み込み中..." />;
  }
  
  if (error) {
    return <ErrorMessage message={error} />;
  }
  
  if (!trainingData || trainingData.total_count === 0) {
    return (
      <div className="training-records-container">
        <FilterPanel 
          filters={filters} 
          onFilterChange={handleFilterChange}
          onStatusChange={handleStatusFilterChange}
          onCategoryChange={handleCategoryFilterChange}
        />
        <div className="no-data-message">
          指定された条件に一致する研修記録はありません
        </div>
      </div>
    );
  }
  
  return (
    <div className="training-records-container">
      <h2>研修記録一覧</h2>
      
      <FilterPanel 
        filters={filters} 
        onFilterChange={handleFilterChange}
        onStatusChange={handleStatusFilterChange}
        onCategoryChange={handleCategoryFilterChange}
        onDetailsToggle={handleDetailsToggle}
      />
      
      <TrainingSummary summary={trainingData.summary} />
      
      <TrainingList 
        trainings={trainingData.trainings}
        showDetails={filters.includeDetails}
      />
      
      {trainingData.total_pages > 1 && (
        <Pagination 
          currentPage={trainingData.page}
          totalPages={trainingData.total_pages}
          onPageChange={handlePageChange}
        />
      )}
      
      <div className="records-info">
        全{trainingData.total_count}件中 {(trainingData.page - 1) * trainingData.per_page + 1}〜
        {Math.min(trainingData.page * trainingData.per_page, trainingData.total_count)}件を表示
      </div>
    </div>
  );
};

export default TrainingRecordsView;
```

### 6.3 研修記録詳細表示コンポーネント例（React）

```jsx
import React, { useState } from 'react';
import { formatDate } from '../utils/dateUtils';
import MaterialsList from './MaterialsList';
import EvaluationDetails from './EvaluationDetails';
import CertificateViewer from './CertificateViewer';

const TrainingDetailCard = ({ training }) => {
  const [expanded, setExpanded] = useState(false);
  
  // 展開/折りたたみ切替ハンドラ
  const toggleExpand = () => {
    setExpanded(!expanded);
  };
  
  // ステータスに応じたバッジクラス
  const getStatusBadgeClass = (status) => {
    switch (status) {
      case
