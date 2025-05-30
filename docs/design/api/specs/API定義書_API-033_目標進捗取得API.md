# API定義書：API-033 目標進捗取得API

## 1. 基本情報

- **API ID**: API-033
- **API名称**: 目標進捗取得API
- **概要**: ユーザーの目標進捗情報を取得する
- **エンドポイント**: `/api/goal-progress/{user_id}`
- **HTTPメソッド**: GET
- **リクエスト形式**: URLパラメータ
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-CAREER](画面設計書_SCR-CAREER.md)
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
| goal_id | string | - | 目標ID | 特定の目標の進捗のみを取得する場合に指定 |
| include_completed | boolean | - | 完了した目標を含めるか | true/false<br>デフォルト: true |
| include_details | boolean | - | 詳細情報を含めるか | true/false<br>デフォルト: false |

### 2.4 リクエスト例

```
GET /api/goal-progress/U12345?year=2025&include_details=true HTTP/1.1
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
| year | number | 年度 | |
| goal_progress | array | 目標進捗情報の配列 | |
| summary | object | 進捗サマリー | |
| last_updated | string | 最終更新日時 | ISO 8601形式 |

#### goal_progress 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| goal_id | string | 目標ID | |
| goal_type | string | 目標タイプ | "short_term", "mid_term", "long_term" |
| title | string | 目標タイトル | |
| status | string | 目標ステータス | "not_started", "in_progress", "completed", "postponed", "cancelled" |
| priority | number | 優先度 | 1-5（5が最高） |
| target_date | string | 目標達成予定日 | ISO 8601形式（YYYY-MM-DD） |
| progress_rate | number | 進捗率 | 0-100（%） |
| remaining_days | number | 残り日数 | |
| action_plan_progress | object | 行動計画の進捗状況 | |
| skill_progress | array | スキル進捗状況 | include_details=trueの場合のみ |
| milestone_progress | array | マイルストーン進捗状況 | include_details=trueの場合のみ |
| recent_updates | array | 最近の更新情報 | include_details=trueの場合のみ |

#### action_plan_progress オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total | number | 行動計画の総数 | |
| completed | number | 完了した行動計画の数 | |
| in_progress | number | 進行中の行動計画の数 | |
| not_started | number | 未着手の行動計画の数 | |
| completion_rate | number | 完了率 | 0-100（%） |

#### skill_progress 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| name | string | スキル名 | |
| category | string | スキルカテゴリ | |
| target_level | number | 目標レベル | 1-5（5が最高） |
| current_level | number | 現在のレベル | 1-5（5が最高） |
| progress_rate | number | 進捗率 | 0-100（%） |
| last_updated | string | 最終更新日時 | ISO 8601形式 |

#### milestone_progress 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| milestone_id | string | マイルストーンID | |
| title | string | タイトル | |
| due_date | string | 期限 | ISO 8601形式（YYYY-MM-DD） |
| status | string | ステータス | "not_started", "in_progress", "completed" |
| completion_date | string | 完了日 | ISO 8601形式（YYYY-MM-DD）、完了時のみ |

#### recent_updates 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| update_id | string | 更新ID | |
| update_type | string | 更新タイプ | "status_change", "action_completed", "skill_level_up", "feedback_added" |
| description | string | 更新内容 | |
| updated_at | string | 更新日時 | ISO 8601形式 |
| updated_by | string | 更新者 | |

#### summary オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total_goals | number | 目標の総数 | |
| completed_goals | number | 完了した目標の数 | |
| in_progress_goals | number | 進行中の目標の数 | |
| not_started_goals | number | 未着手の目標の数 | |
| postponed_goals | number | 延期された目標の数 | |
| cancelled_goals | number | 中止された目標の数 | |
| overall_progress_rate | number | 全体の進捗率 | 0-100（%） |
| short_term_progress_rate | number | 短期目標の進捗率 | 0-100（%） |
| mid_term_progress_rate | number | 中期目標の進捗率 | 0-100（%） |
| long_term_progress_rate | number | 長期目標の進捗率 | 0-100（%） |

### 3.2 正常時レスポンス例

```json
{
  "user_id": "U12345",
  "year": 2025,
  "goal_progress": [
    {
      "goal_id": "G001",
      "goal_type": "short_term",
      "title": "Reactの実践的スキル習得",
      "status": "in_progress",
      "priority": 5,
      "target_date": "2025-12-31",
      "progress_rate": 45,
      "remaining_days": 217,
      "action_plan_progress": {
        "total": 3,
        "completed": 1,
        "in_progress": 1,
        "not_started": 1,
        "completion_rate": 33.3
      },
      "skill_progress": [
        {
          "skill_id": "S007",
          "name": "React",
          "category": "technical",
          "target_level": 4,
          "current_level": 2,
          "progress_rate": 50,
          "last_updated": "2025-05-15T10:30:00+09:00"
        },
        {
          "skill_id": "S008",
          "name": "TypeScript",
          "category": "technical",
          "target_level": 3,
          "current_level": 2,
          "progress_rate": 66.7,
          "last_updated": "2025-05-10T14:20:00+09:00"
        }
      ],
      "milestone_progress": [
        {
          "milestone_id": "M001",
          "title": "Reactの基本概念の理解",
          "due_date": "2025-06-30",
          "status": "completed",
          "completion_date": "2025-06-15"
        },
        {
          "milestone_id": "M002",
          "title": "実際のプロジェクトでReactを使用",
          "due_date": "2025-09-30",
          "status": "in_progress",
          "completion_date": null
        }
      ],
      "recent_updates": [
        {
          "update_id": "U001",
          "update_type": "action_completed",
          "description": "Reactの公式チュートリアルを完了しました",
          "updated_at": "2025-06-15T15:45:00+09:00",
          "updated_by": "U12345"
        },
        {
          "update_id": "U002",
          "update_type": "skill_level_up",
          "description": "Reactのスキルレベルが1から2に上がりました",
          "updated_at": "2025-05-15T10:30:00+09:00",
          "updated_by": "U12345"
        }
      ]
    },
    {
      "goal_id": "G002",
      "goal_type": "mid_term",
      "title": "フロントエンドアーキテクト資格取得",
      "status": "not_started",
      "priority": 3,
      "target_date": "2026-06-30",
      "progress_rate": 0,
      "remaining_days": 398,
      "action_plan_progress": {
        "total": 1,
        "completed": 0,
        "in_progress": 0,
        "not_started": 1,
        "completion_rate": 0
      },
      "skill_progress": [
        {
          "skill_id": "S015",
          "name": "フロントエンドアーキテクチャ",
          "category": "technical",
          "target_level": 4,
          "current_level": 2,
          "progress_rate": 50,
          "last_updated": "2025-04-01T09:15:00+09:00"
        }
      ],
      "milestone_progress": [],
      "recent_updates": []
    }
  ],
  "summary": {
    "total_goals": 3,
    "completed_goals": 0,
    "in_progress_goals": 1,
    "not_started_goals": 2,
    "postponed_goals": 0,
    "cancelled_goals": 0,
    "overall_progress_rate": 15,
    "short_term_progress_rate": 45,
    "mid_term_progress_rate": 0,
    "long_term_progress_rate": 0
  },
  "last_updated": "2025-06-15T15:45:00+09:00"
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_YEAR | 年度が不正です | 存在しない年度指定 |
| 400 Bad Request | INVALID_GOAL_ID | 目標IDが不正です | 存在しない目標ID |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他ユーザーの情報閲覧権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 404 Not Found | GOAL_PROGRESS_NOT_FOUND | 目標進捗が見つかりません | 指定された条件の目標進捗が存在しない |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_GOAL_ID",
    "message": "目標IDが不正です",
    "details": "指定された目標ID 'G999' は存在しません。"
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
   - 年度の妥当性チェック
   - 目標IDの存在チェック（指定されている場合）
3. 目標進捗情報の取得
   - 指定されたユーザーIDと年度の目標進捗を取得
   - 目標IDが指定されている場合は、その目標の進捗のみを取得
   - include_completedがfalseの場合は、完了した目標を除外
   - include_detailsがtrueの場合は、詳細情報も取得
4. 進捗率の計算
   - 各目標の進捗率を計算
   - 全体の進捗率を計算
5. レスポンスの生成
   - 取得した目標進捗情報を整形
6. レスポンス返却

### 4.2 権限チェック

- 自身の目標進捗は常に閲覧可能
- 他ユーザーの目標進捗閲覧には以下のいずれかの条件を満たす必要がある
  - 対象ユーザーの直属の上長である
  - 目標進捗閲覧権限（PERM_VIEW_GOAL_PROGRESS）を持っている
  - 管理者権限（ROLE_ADMIN）を持っている

### 4.3 進捗率の計算方法

#### 目標の進捗率

1. 行動計画の完了率（行動計画の完了数 / 行動計画の総数）
2. 関連スキルの進捗率（現在のレベル / 目標レベル）の平均
3. マイルストーンの完了率（完了したマイルストーン数 / マイルストーンの総数）
4. 上記3つの指標の加重平均を計算
   - 行動計画の完了率: 50%
   - 関連スキルの進捗率: 30%
   - マイルストーンの完了率: 20%

#### 全体の進捗率

1. 各目標の進捗率を優先度で重み付けして平均
2. 目標タイプ別（短期・中期・長期）の進捗率も同様に計算

### 4.4 残り日数の計算

1. 目標達成予定日と現在日時の差分を日数で計算
2. 負の値になる場合（期限超過）は、超過日数としてマイナス値で表示

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-021](API仕様書_API-021.md) | スキル情報取得API | ユーザースキル情報取得 |
| [API-031](API仕様書_API-031.md) | キャリア目標取得API | キャリア目標情報取得 |
| [API-032](API仕様書_API-032.md) | キャリア目標更新API | キャリア目標情報更新 |
| [API-034](API仕様書_API-034.md) | 目標進捗更新API | 目標進捗情報更新 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| career_goals | キャリア目標情報 | 参照（R） |
| career_goal_skills | キャリア目標関連スキル | 参照（R） |
| career_goal_actions | キャリア目標行動計画 | 参照（R） |
| career_goal_milestones | キャリア目標マイルストーン | 参照（R） |
| career_goal_updates | キャリア目標更新履歴 | 参照（R） |
| user_skills | ユーザースキル情報 | 参照（R） |
| skill_masters | スキルマスタ | 参照（R） |

### 5.3 注意事項・補足

- 進捗率の計算は、目標の種類や内容によって異なる場合がある
- 残り日数は営業日ではなく暦日で計算
- 目標の状態が「延期」または「中止」の場合、進捗率の計算から除外
- 詳細情報（include_details=true）を含める場合、レスポンスサイズが大きくなるため注意
- 複数の目標を持つユーザーの場合、全体の進捗率は単純平均ではなく、優先度による重み付け平均
- 目標進捗情報は、キャリア目標情報と最新のスキル情報を組み合わせて動的に計算

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import {
  CircularProgress,
  LinearProgress,
  Typography,
  Box,
  Card,
  CardContent,
  CardHeader,
  Grid,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  Paper,
  Tab,
  Tabs,
  Switch,
  FormControlLabel
} from '@mui/material';
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

// 型定義
interface ActionPlanProgress {
  total: number;
  completed: number;
  in_progress: number;
  not_started: number;
  completion_rate: number;
}

interface SkillProgress {
  skill_id: string;
  name: string;
  category: string;
  target_level: number;
  current_level: number;
  progress_rate: number;
  last_updated: string;
}

interface MilestoneProgress {
  milestone_id: string;
  title: string;
  due_date: string;
  status: 'not_started' | 'in_progress' | 'completed';
  completion_date: string | null;
}

interface RecentUpdate {
  update_id: string;
  update_type: 'status_change' | 'action_completed' | 'skill_level_up' | 'feedback_added';
  description: string;
  updated_at: string;
  updated_by: string;
}

interface GoalProgress {
  goal_id: string;
  goal_type: 'short_term' | 'mid_term' | 'long_term';
  title: string;
  status: 'not_started' | 'in_progress' | 'completed' | 'postponed' | 'cancelled';
  priority: number;
  target_date: string;
  progress_rate: number;
  remaining_days: number;
  action_plan_progress: ActionPlanProgress;
  skill_progress?: SkillProgress[];
  milestone_progress?: MilestoneProgress[];
  recent_updates?: RecentUpdate[];
}

interface ProgressSummary {
  total_goals: number;
  completed_goals: number;
  in_progress_goals: number;
  not_started_goals: number;
  postponed_goals: number;
  cancelled_goals: number;
  overall_progress_rate: number;
  short_term_progress_rate: number;
  mid_term_progress_rate: number;
  long_term_progress_rate: number;
}

interface GoalProgressResponse {
  user_id: string;
  year: number;
  goal_progress: GoalProgress[];
  summary: ProgressSummary;
  last_updated: string;
}

const GoalProgressView: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const [year, setYear] = useState<number>(new Date().getFullYear());
  const [includeCompleted, setIncludeCompleted] = useState<boolean>(true);
  const [includeDetails, setIncludeDetails] = useState<boolean>(true);
  const [progressData, setProgressData] = useState<GoalProgressResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<number>(0);
  
  useEffect(() => {
    const fetchGoalProgress = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await axios.get<GoalProgressResponse>(
          `/api/goal-progress/${userId}`,
          {
            params: {
              year,
              include_completed: includeCompleted,
              include_details: includeDetails
            },
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
              'Accept': 'application/json'
            }
          }
        );
        
        setProgressData(response.data);
        
      } catch (err) {
        if (axios.isAxiosError(err) && err.response) {
          const errorData = err.response.data;
          setError(errorData.error?.message || '目標進捗の取得に失敗しました');
        } else {
          setError('目標進捗の取得中にエラーが発生しました');
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchGoalProgress();
  }, [userId, year, includeCompleted, includeDetails]);
  
  const handleYearChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setYear(parseInt(e.target.value, 10));
  };
  
  const handleCompletedToggle = () => {
    setIncludeCompleted(!includeCompleted);
  };
  
  const handleDetailsToggle = () => {
    setIncludeDetails(!includeDetails);
  };
  
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };
  
  const getGoalTypeLabel = (goalType: string): string => {
    const labels: Record<string, string> = {
      'short_term': '短期目標（1年以内）',
      'mid_term': '中期目標（1-3年）',
      'long_term': '長期目標（3-5年）'
    };
    return labels[goalType] || goalType;
  };
  
  const getStatusLabel = (status: string): string => {
    const labels: Record<string, string> = {
      'not_started': '未着手',
      'in_progress': '進行中',
      'completed': '完了',
      'postponed': '延期',
      'cancelled': '中止'
    };
    return labels[status] || status;
  };
  
  const getStatusColor = (status: string): string => {
    const colors: Record<string, string> = {
      'not_started': '#6c757d', // グレー
      'in_progress': '#007bff', // 青
      'completed': '#28a745', // 緑
      'postponed': '#ffc107', // 黄
      'cancelled': '#dc3545' // 赤
    };
    return colors[status] || '#6c757d';
  };
  
  const getProgressColor = (rate: number): string => {
    if (rate < 25) return '#dc3545'; // 赤
    if (rate < 50) return '#ffc107'; // 黄
    if (rate < 75) return '#17a2b8'; // 青
    return '#28a745'; // 緑
  };
  
  const renderSkillLevel = (current: number, target: number, maxLevel: number = 5) => {
    return (
      <div className="skill-level-progress">
        <div className="level-bars">
          {Array.from({ length: maxLevel }).map((_, index) => (
            <div 
              key={index} 
              className={`level-bar ${
                index < current ? 'filled' : 
                index < target ? 'target' : 'empty'
              }`}
              title={`現在: ${current}、目標: ${target}`}
            />
          ))}
        </div>
        <div className="level-text">
          <span className="current">{current}</span>
          <span className="separator">/</span>
          <span className="target">{target}</span>
        </div>
      </div>
    );
  };
  
  const renderProgressCircle = (rate: number) => {
    return (
      <Box position="relative" display="inline-flex">
        <CircularProgress
          variant="determinate"
          value={rate}
          size={80}
          thickness={5}
          style={{ color: getProgressColor(rate) }}
        />
        <Box
          top={0}
          left={0}
          bottom={0}
          right={0}
          position="absolute"
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <Typography variant="h6" component="div" color="textSecondary">
            {`${Math.round(rate)}%`}
          </Typography>
        </Box>
      </Box>
    );
  };
  
  const renderGoalCard = (goal: GoalProgress) => {
    return (
      <Card key={goal.goal_id} className="goal-progress-card" elevation={3}>
        <CardHeader
          title={goal.title}
          subheader={
            <div className="goal-card-subheader">
              <Chip 
                label={getGoalTypeLabel(goal.goal_type)} 
                size="small" 
                className={`goal-type-chip ${goal.goal_type}`}
              />
              <Chip 
                label={getStatusLabel(goal.status)} 
                size="small"
                style={{ backgroundColor: getStatusColor(goal.status), color: 'white' }}
              />
              <span className="priority-indicator">
                優先度: {Array.from({ length: goal.priority }).map((_, i) => '★').join('')}
              </span>
            </div>
          }
          action={renderProgressCircle(goal.progress_rate)}
        />
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="textSecondary">
                目標達成予定日: {new Date(goal.target_date).toLocaleDateString()}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                残り日数: {goal.remaining_days > 0 ? `${goal.remaining_days}日` : `${Math.abs(goal.remaining_days)}日超過`}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2">
                行動計画の進捗:
              </Typography>
              <Box display="flex" alignItems="center">
                <Box width="100%" mr={1}>
                  <LinearProgress 
                    variant="determinate" 
                    value={goal.action_plan_progress.completion_rate}
