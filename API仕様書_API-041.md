# API仕様書：API-041 作業実績取得API

## 1. 基本情報

- **API ID**: API-041
- **API名称**: 作業実績取得API
- **概要**: 指定されたユーザーの作業実績情報を取得する
- **エンドポイント**: `/api/work-records/{user_id}`
- **HTTPメソッド**: GET
- **リクエスト形式**: URL Path Parameter + Query Parameter
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-WORK](画面設計書_SCR-WORK.md)
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
| year | number | - | 取得対象年度 | 西暦4桁<br>指定なしの場合は最新年度 |
| from_date | string | - | 開始日 | ISO 8601形式（YYYY-MM-DD）<br>指定した日付以降の実績を取得 |
| to_date | string | - | 終了日 | ISO 8601形式（YYYY-MM-DD）<br>指定した日付以前の実績を取得 |
| project_id | string | - | プロジェクトID | 特定プロジェクトの実績のみ取得 |
| category | string | - | 作業カテゴリ | "development", "meeting", "learning", "management", "other"のいずれか |
| page | number | - | ページ番号 | 1以上の整数<br>デフォルト：1 |
| per_page | number | - | 1ページあたりの件数 | 1〜100の整数<br>デフォルト：20 |
| sort_by | string | - | ソート項目 | "date", "project", "hours", "category"のいずれか<br>デフォルト："date" |
| sort_order | string | - | ソート順 | "asc"（昇順）, "desc"（降順）のいずれか<br>デフォルト："desc" |

### 2.3 リクエスト例

```
GET /api/work-records/tanaka.taro?year=2025&from_date=2025-04-01&to_date=2025-04-30&project_id=PRJ-2025-001&category=development&page=1&per_page=20&sort_by=date&sort_order=desc
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
| records | array | 作業実績レコードの配列 | 詳細は以下参照 |
| summary | object | 集計情報 | 詳細は以下参照 |

#### records 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| record_id | string | レコードID | UUID形式 |
| date | string | 作業日 | ISO 8601形式（YYYY-MM-DD） |
| project_id | string | プロジェクトID | |
| project_name | string | プロジェクト名 | |
| category | string | 作業カテゴリ | "development", "meeting", "learning", "management", "other"のいずれか |
| task | string | 作業タスク | |
| description | string | 作業内容 | |
| hours | number | 作業時間（時間） | 小数点第1位まで（0.5時間単位） |
| achievements | array | 成果物 | 文字列の配列 |
| skills_used | array | 使用スキル | スキルIDの配列 |
| created_at | string | 登録日時 | ISO 8601形式 |
| updated_at | string | 更新日時 | ISO 8601形式 |

#### summary オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total_hours | number | 合計作業時間 | 小数点第1位まで |
| by_category | object | カテゴリ別集計 | カテゴリごとの作業時間 |
| by_project | array | プロジェクト別集計 | プロジェクトごとの作業時間 |
| by_date | object | 日付別集計 | 日付ごとの作業時間 |

### 3.2 正常時レスポンス例

```json
{
  "user_id": "tanaka.taro",
  "total_count": 45,
  "page": 1,
  "per_page": 20,
  "total_pages": 3,
  "records": [
    {
      "record_id": "rec-12345-abcde-67890",
      "date": "2025-04-30",
      "project_id": "PRJ-2025-001",
      "project_name": "顧客ポータル開発",
      "category": "development",
      "task": "ユーザー認証機能実装",
      "description": "JWT認証の実装とセッション管理機能の開発。ユーザーロールに基づくアクセス制御も実装。",
      "hours": 7.5,
      "achievements": [
        "認証処理のコード実装完了",
        "ユニットテスト作成"
      ],
      "skills_used": ["java", "spring-security", "jwt"],
      "created_at": "2025-04-30T18:30:45+09:00",
      "updated_at": "2025-04-30T18:30:45+09:00"
    },
    {
      "record_id": "rec-67890-fghij-12345",
      "date": "2025-04-29",
      "project_id": "PRJ-2025-001",
      "project_name": "顧客ポータル開発",
      "category": "meeting",
      "task": "朝会・進捗報告",
      "description": "チーム朝会での進捗報告と課題共有。認証機能の設計レビューを実施。",
      "hours": 1.0,
      "achievements": [
        "認証機能の設計承認取得"
      ],
      "skills_used": ["communication", "presentation"],
      "created_at": "2025-04-29T17:45:20+09:00",
      "updated_at": "2025-04-29T17:45:20+09:00"
    },
    // 以下、残りのレコード...
  ],
  "summary": {
    "total_hours": 160.5,
    "by_category": {
      "development": 120.0,
      "meeting": 20.5,
      "learning": 10.0,
      "management": 5.0,
      "other": 5.0
    },
    "by_project": [
      {
        "project_id": "PRJ-2025-001",
        "project_name": "顧客ポータル開発",
        "hours": 140.5
      },
      {
        "project_id": "PRJ-2025-002",
        "project_name": "社内研修",
        "hours": 20.0
      }
    ],
    "by_date": {
      "2025-04-30": 8.0,
      "2025-04-29": 8.0,
      "2025-04-28": 8.0,
      // 以下、日付ごとの集計...
    }
  }
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他者の作業実績閲覧権限なし |
| 404 Not Found | USER_NOT_FOUND | 指定されたユーザーが見つかりません | 存在しないユーザーID |
| 404 Not Found | NO_RECORDS_FOUND | 指定された条件の作業実績が見つかりません | 条件に合致するレコードなし |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "パラメータが不正です",
    "details": "from_dateとto_dateの期間は最大1年間までです。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - 作業実績閲覧権限の確認
   - 他者の作業実績閲覧権限の確認（自分以外のuser_idの場合）
2. リクエストパラメータの検証
   - user_idの形式チェック
   - 日付パラメータの形式チェック（指定されている場合）
   - ページネーションパラメータの範囲チェック
3. ユーザーの存在確認
   - 指定されたuser_idのユーザーが存在するか確認
4. 検索条件の構築
   - 指定されたパラメータに基づいて検索条件を構築
5. 作業実績データの取得
   - 検索条件に合致するレコードの総数を取得
   - ページネーション情報に基づいて対象レコードを取得
6. 集計情報の計算
   - カテゴリ別、プロジェクト別、日付別の集計を実施
7. レスポンスの生成
   - 取得したデータを整形してJSONレスポンスを生成
8. レスポンス返却

### 4.2 アクセス制御ルール

- 自分自身の作業実績：閲覧可能
- 部下の作業実績：マネージャーは閲覧可能
- 同一プロジェクトメンバーの作業実績：プロジェクトリーダーは閲覧可能
- 全社員の作業実績サマリー：管理者は閲覧可能

### 4.3 パフォーマンス要件

- 応答時間：平均500ms以内
- タイムアウト：10秒
- キャッシュ：ユーザー別・日付範囲別に30分キャッシュ
- 同時リクエスト：最大50リクエスト/秒
- 最大レコード取得数：一度に最大100件まで

### 4.4 検索条件の組み合わせルール

- from_dateとto_dateの期間は最大1年間まで
- 年度指定（year）と日付範囲指定（from_date, to_date）が両方ある場合は日付範囲を優先
- カテゴリとプロジェクトの両方が指定された場合は、AND条件で絞り込み
- ソート条件は1つのみ指定可能

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-042](API仕様書_API-042.md) | 作業実績登録API | 作業実績情報の登録 |
| [API-043](API仕様書_API-043.md) | 作業実績更新API | 作業実績情報の更新 |
| [API-101](API仕様書_API-101.md) | 一括登録検証API | 一括登録データの検証 |
| [API-102](API仕様書_API-102.md) | 一括登録実行API | 一括登録の実行 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| work_records | 作業実績情報 | 参照（R） |
| projects | プロジェクト情報 | 参照（R） |
| work_categories | 作業カテゴリ | 参照（R） |
| skills | スキル情報 | 参照（R） |
| project_members | プロジェクトメンバー | 参照（R） |

### 5.3 注意事項・補足

- 作業実績は日付単位で管理
- 作業時間は0.5時間単位で記録（0.5, 1.0, 1.5, ...）
- 1日の作業時間合計は最大24時間まで
- 過去2年分の作業実績を参照可能
- 未来日付の作業実績は登録不可
- プロジェクトが終了していても過去の作業実績は参照可能
- 集計情報は指定された検索条件に基づいて計算
- 大量データの場合はページネーションを活用

---

## 6. サンプルコード

### 6.1 作業実績取得例（JavaScript/Fetch API）

```javascript
/**
 * ユーザーの作業実績情報を取得する関数
 * @param {string} userId - ユーザーID
 * @param {Object} options - 検索オプション
 * @param {number} [options.year] - 取得対象年度
 * @param {string} [options.fromDate] - 開始日（YYYY-MM-DD）
 * @param {string} [options.toDate] - 終了日（YYYY-MM-DD）
 * @param {string} [options.projectId] - プロジェクトID
 * @param {string} [options.category] - 作業カテゴリ
 * @param {number} [options.page] - ページ番号
 * @param {number} [options.perPage] - 1ページあたりの件数
 * @param {string} [options.sortBy] - ソート項目
 * @param {string} [options.sortOrder] - ソート順
 * @returns {Promise<Object>} 作業実績情報
 */
async function getUserWorkRecords(userId, options = {}) {
  try {
    // クエリパラメータの構築
    const queryParams = new URLSearchParams();
    if (options.year) queryParams.append('year', options.year);
    if (options.fromDate) queryParams.append('from_date', options.fromDate);
    if (options.toDate) queryParams.append('to_date', options.toDate);
    if (options.projectId) queryParams.append('project_id', options.projectId);
    if (options.category) queryParams.append('category', options.category);
    if (options.page) queryParams.append('page', options.page);
    if (options.perPage) queryParams.append('per_page', options.perPage);
    if (options.sortBy) queryParams.append('sort_by', options.sortBy);
    if (options.sortOrder) queryParams.append('sort_order', options.sortOrder);
    
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
    
    // APIリクエスト
    const response = await fetch(`https://api.example.com/api/work-records/${userId}${queryString}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`,
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error.message || '作業実績情報の取得に失敗しました');
    }
    
    return await response.json();
  } catch (error) {
    console.error('作業実績情報取得エラー:', error);
    throw error;
  }
}
```

### 6.2 作業実績一覧表示コンポーネント例（React）

```jsx
import React, { useState, useEffect } from 'react';
import { getUserWorkRecords } from '../api/workRecordApi';
import WorkRecordTable from './WorkRecordTable';
import WorkSummaryCharts from './WorkSummaryCharts';
import FilterPanel from './FilterPanel';
import Pagination from '../common/Pagination';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';
import { formatDate } from '../utils/dateUtils';

const WorkRecordsView = ({ userId }) => {
  // 状態管理
  const [workData, setWorkData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    year: new Date().getFullYear(),
    fromDate: formatDate(new Date(new Date().setDate(1))), // 当月1日
    toDate: formatDate(new Date()), // 今日
    projectId: '',
    category: '',
    page: 1,
    perPage: 20,
    sortBy: 'date',
    sortOrder: 'desc'
  });
  
  // 作業実績データの取得
  useEffect(() => {
    const fetchWorkRecords = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const data = await getUserWorkRecords(userId, filters);
        setWorkData(data);
      } catch (err) {
        setError(err.message || '作業実績情報の取得に失敗しました');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchWorkRecords();
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
  
  // ソート変更ハンドラ
  const handleSortChange = (sortBy) => {
    const sortOrder = filters.sortBy === sortBy && filters.sortOrder === 'asc' ? 'desc' : 'asc';
    setFilters({
      ...filters,
      sortBy,
      sortOrder
    });
  };
  
  if (isLoading) {
    return <LoadingSpinner message="作業実績情報を読み込み中..." />;
  }
  
  if (error) {
    return <ErrorMessage message={error} />;
  }
  
  if (!workData || workData.total_count === 0) {
    return (
      <div className="work-records-container">
        <FilterPanel 
          filters={filters} 
          onFilterChange={handleFilterChange} 
        />
        <div className="no-data-message">
          指定された条件に一致する作業実績はありません
        </div>
      </div>
    );
  }
  
  return (
    <div className="work-records-container">
      <h2>作業実績一覧</h2>
      
      <FilterPanel 
        filters={filters} 
        onFilterChange={handleFilterChange} 
      />
      
      <div className="summary-section">
        <h3>集計情報</h3>
        <div className="total-hours">
          合計作業時間: <span className="hours-value">{workData.summary.total_hours}時間</span>
        </div>
        
        <WorkSummaryCharts 
          categoryData={workData.summary.by_category}
          projectData={workData.summary.by_project}
          dateData={workData.summary.by_date}
        />
      </div>
      
      <div className="records-section">
        <h3>作業実績一覧</h3>
        <WorkRecordTable 
          records={workData.records}
          sortBy={filters.sortBy}
          sortOrder={filters.sortOrder}
          onSortChange={handleSortChange}
        />
        
        <Pagination 
          currentPage={workData.page}
          totalPages={workData.total_pages}
          onPageChange={handlePageChange}
        />
        
        <div className="records-info">
          全{workData.total_count}件中 {(workData.page - 1) * workData.per_page + 1}〜
          {Math.min(workData.page * workData.per_page, workData.total_count)}件を表示
        </div>
      </div>
    </div>
  );
};

export default WorkRecordsView;
```

### 6.3 作業実績集計ユーティリティ例（TypeScript）

```typescript
/**
 * 作業実績集計ユーティリティ
 */
export class WorkRecordAnalyzer {
  /**
   * 作業実績データから傾向を分析
   * @param workRecords 作業実績データ
   * @returns 分析結果
   */
  public static analyzeWorkTrends(workRecords: WorkRecord[]): WorkTrendAnalysis {
    if (!workRecords || workRecords.length === 0) {
      return {
        totalHours: 0,
        averageDailyHours: 0,
        mostActiveProject: null,
        mostUsedSkills: [],
        categoryDistribution: {},
        weekdayDistribution: {},
        recommendations: []
      };
    }
    
    // 合計作業時間
    const totalHours = this.calculateTotalHours(workRecords);
    
    // 日別の作業時間を集計
    const dateHoursMap = this.groupByDate(workRecords);
    const uniqueDates = Object.keys(dateHoursMap).length;
    
    // 平均日次作業時間
    const averageDailyHours = uniqueDates > 0 ? 
      totalHours / uniqueDates : 0;
    
    // プロジェクト別の作業時間を集計
    const projectHoursMap = this.groupByProject(workRecords);
    
    // 最も作業時間が多いプロジェクト
    const mostActiveProject = this.findMostActiveProject(projectHoursMap);
    
    // スキル別の使用頻度を集計
    const skillUsageMap = this.countSkillUsage(workRecords);
    
    // 最も使用頻度が高いスキル（上位5件）
    const mostUsedSkills = this.findMostUsedSkills(skillUsageMap, 5);
    
    // カテゴリ別の作業時間分布
    const categoryDistribution = this.calculateCategoryDistribution(workRecords);
    
    // 曜日別の作業時間分布
    const weekdayDistribution = this.calculateWeekdayDistribution(workRecords);
    
    // 分析に基づく推奨事項
    const recommendations = this.generateRecommendations({
      totalHours,
      averageDailyHours,
      categoryDistribution,
      weekdayDistribution
    });
    
    return {
      totalHours,
      averageDailyHours,
      mostActiveProject,
      mostUsedSkills,
      categoryDistribution,
      weekdayDistribution,
      recommendations
    };
  }
  
  /**
   * 合計作業時間を計算
   */
  private static calculateTotalHours(records: WorkRecord[]): number {
    return records.reduce((sum, record) => sum + record.hours, 0);
  }
  
  /**
   * 日付ごとに作業時間を集計
   */
  private static groupByDate(records: WorkRecord[]): Record<string, number> {
    return records.reduce((acc, record) => {
      const date = record.date;
      acc[date] = (acc[date] || 0) + record.hours;
      return acc;
    }, {} as Record<string, number>);
  }
  
  /**
   * プロジェクトごとに作業時間を集計
   */
  private static groupByProject(records: WorkRecord[]): Record<string, ProjectHours> {
    return records.reduce((acc, record) => {
      const projectId = record.project_id;
      if (!acc[projectId]) {
        acc[projectId] = {
          project_id: projectId,
          project_name: record.project_name,
          hours: 0
        };
      }
      acc[projectId].hours += record.hours;
      return acc;
    }, {} as Record<string, ProjectHours>);
  }
  
  /**
   * 最も作業時間が多いプロジェクトを特定
   */
  private static findMostActiveProject(
    projectHoursMap: Record<string, ProjectHours>
  ): ProjectHours | null {
    const projects = Object.values(projectHoursMap);
    if (projects.length === 0) return null;
    
    return projects.reduce((max, project) => 
      project.hours > max.hours ? project : max, projects[0]);
  }
  
  /**
   * スキルの使用頻度をカウント
   */
  private static countSkillUsage(records: WorkRecord[]): Record<string, number> {
    const skillUsage: Record<string, number> = {};
    
    records.forEach(record => {
      if (record.skills_used && record.skills_used.length > 0) {
        record.skills_used.forEach(skillId => {
          skillUsage[skillId] = (skillUsage[skillId] || 0) + 1;
        });
      }
    });
    
    return skillUsage;
  }
  
  /**
   * 最も使用頻度が高いスキルを特定
   */
  private static findMostUsedSkills(
    skillUsageMap: Record<string, number>, 
    limit: number
  ): SkillUsage[] {
    const skillUsages = Object.entries(skillUsageMap).map(([skillId, count]) => ({
      skill_id: skillId,
      count
    }));
    
    return skillUsages
      .sort((a, b) => b.count - a.count)
      .slice(0, limit);
  }
  
  /**
   * カテゴリ別の作業時間分布を計算
   */
  private static calculateCategoryDistribution(
    records: WorkRecord[]
  ): Record<string, number> {
    const distribution: Record<string, number> = {
      development: 0,
      meeting: 0,
      learning: 0,
      management: 0,
      other: 0
    };
    
    records.forEach(record => {
      if (distribution[record.category] !== undefined) {
        distribution[record.category] += record.hours;
      } else {
        distribution.other += record.hours;
      }
    });
    
    return distribution;
  }
  
  /**
   * 曜日別の作業時間分布を計算
   */
  private static calculateWeekdayDistribution(
    records: WorkRecord[]
  ): Record<string, number> {
    const weekdays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
    const distribution: Record<string, number> = {
      monday: 0,
      tuesday: 0,
      wednesday: 0,
      thursday: 0,
      friday: 0,
      saturday: 0,
      sunday: 0
    };
    
    records.forEach(record => {
      const date = new Date(record.date);
      const weekday = weekdays[date.getDay()];
      distribution[weekday] += record.hours;
    });
    
    return distribution;
  }
