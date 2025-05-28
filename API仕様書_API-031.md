# API仕様書：API-031 キャリア目標取得API

## 1. 基本情報

- **API ID**: API-031
- **API名称**: キャリア目標取得API
- **概要**: ユーザーのキャリア目標情報を取得する
- **エンドポイント**: `/api/career-goals/{user_id}`
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
| include_history | boolean | - | 過去の履歴を含めるか | true/false<br>デフォルト: false |

### 2.4 リクエスト例

```
GET /api/career-goals/U12345?year=2025&include_history=true HTTP/1.1
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
| career_goals | array | キャリア目標情報の配列 | |
| history | array | 過去のキャリア目標履歴 | include_history=trueの場合のみ |
| last_updated | string | 最終更新日時 | ISO 8601形式 |
| last_updated_by | string | 最終更新者 | |

#### career_goals 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| goal_id | string | 目標ID | |
| goal_type | string | 目標タイプ | "short_term", "mid_term", "long_term" |
| title | string | 目標タイトル | |
| description | string | 目標詳細 | |
| target_date | string | 目標達成予定日 | ISO 8601形式（YYYY-MM-DD） |
| status | string | 目標ステータス | "not_started", "in_progress", "completed", "postponed", "cancelled" |
| priority | number | 優先度 | 1-5（5が最高） |
| related_skills | array | 関連スキル | |
| action_plans | array | 行動計画 | |
| feedback | array | フィードバック | |
| created_at | string | 作成日時 | ISO 8601形式 |
| updated_at | string | 更新日時 | ISO 8601形式 |

#### related_skills 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| name | string | スキル名 | |
| category | string | スキルカテゴリ | |
| target_level | number | 目標レベル | 1-5（5が最高） |
| current_level | number | 現在のレベル | 1-5（5が最高） |

#### action_plans 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| action_id | string | 行動計画ID | |
| title | string | タイトル | |
| description | string | 詳細 | |
| due_date | string | 期限 | ISO 8601形式（YYYY-MM-DD） |
| status | string | ステータス | "not_started", "in_progress", "completed" |
| completed_date | string | 完了日 | ISO 8601形式（YYYY-MM-DD）、完了時のみ |

#### feedback 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| feedback_id | string | フィードバックID | |
| commenter_id | string | コメント者ID | |
| commenter_name | string | コメント者名 | |
| comment | string | コメント内容 | |
| created_at | string | 作成日時 | ISO 8601形式 |

#### history 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| year | number | 年度 | |
| career_goals | array | その年度のキャリア目標情報 | career_goals配列と同じ構造 |
| last_updated | string | 最終更新日時 | ISO 8601形式 |

### 3.2 正常時レスポンス例

```json
{
  "user_id": "U12345",
  "year": 2025,
  "career_goals": [
    {
      "goal_id": "G001",
      "goal_type": "short_term",
      "title": "Reactの実践的スキル習得",
      "description": "実務でReactを使用したプロジェクトに参加し、実践的なスキルを身につける",
      "target_date": "2025-12-31",
      "status": "in_progress",
      "priority": 5,
      "related_skills": [
        {
          "skill_id": "S007",
          "name": "React",
          "category": "technical",
          "target_level": 4,
          "current_level": 2
        },
        {
          "skill_id": "S008",
          "name": "TypeScript",
          "category": "technical",
          "target_level": 3,
          "current_level": 2
        }
      ],
      "action_plans": [
        {
          "action_id": "A001",
          "title": "Reactの公式チュートリアルを完了する",
          "description": "Reactの公式ドキュメントに沿ってチュートリアルを実施",
          "due_date": "2025-06-30",
          "status": "completed",
          "completed_date": "2025-06-15"
        },
        {
          "action_id": "A002",
          "title": "社内のReactプロジェクトに参加する",
          "description": "プロジェクトマネージャーに相談し、Reactを使用するプロジェクトにアサインしてもらう",
          "due_date": "2025-07-31",
          "status": "in_progress",
          "completed_date": null
        }
      ],
      "feedback": [
        {
          "feedback_id": "F001",
          "commenter_id": "U67890",
          "commenter_name": "鈴木 花子",
          "comment": "Reactの学習計画が具体的で良いと思います。実際のプロジェクト参加も良い経験になるでしょう。",
          "created_at": "2025-05-15T10:30:00+09:00"
        }
      ],
      "created_at": "2025-04-01T09:00:00+09:00",
      "updated_at": "2025-06-15T15:45:00+09:00"
    },
    {
      "goal_id": "G002",
      "goal_type": "mid_term",
      "title": "フロントエンドアーキテクト資格取得",
      "description": "フロントエンド開発のアーキテクチャ設計スキルを向上させ、認定資格を取得する",
      "target_date": "2026-06-30",
      "status": "not_started",
      "priority": 3,
      "related_skills": [
        {
          "skill_id": "S015",
          "name": "フロントエンドアーキテクチャ",
          "category": "technical",
          "target_level": 4,
          "current_level": 2
        }
      ],
      "action_plans": [
        {
          "action_id": "A003",
          "title": "アーキテクチャ設計の書籍を3冊読む",
          "description": "推奨書籍リストから選定して学習する",
          "due_date": "2025-09-30",
          "status": "not_started",
          "completed_date": null
        }
      ],
      "feedback": [],
      "created_at": "2025-04-01T09:15:00+09:00",
      "updated_at": "2025-04-01T09:15:00+09:00"
    },
    {
      "goal_id": "G003",
      "goal_type": "long_term",
      "title": "テックリード職への昇進",
      "description": "技術的なリーダーシップスキルを磨き、チームのテックリードとして活躍する",
      "target_date": "2027-12-31",
      "status": "not_started",
      "priority": 4,
      "related_skills": [
        {
          "skill_id": "S030",
          "name": "技術リーダーシップ",
          "category": "soft",
          "target_level": 4,
          "current_level": 2
        },
        {
          "skill_id": "S031",
          "name": "コードレビュー",
          "category": "technical",
          "target_level": 5,
          "current_level": 3
        }
      ],
      "action_plans": [
        {
          "action_id": "A004",
          "title": "社内勉強会でリーダーを務める",
          "description": "フロントエンド技術の勉強会を企画・運営する",
          "due_date": "2025-12-31",
          "status": "not_started",
          "completed_date": null
        }
      ],
      "feedback": [],
      "created_at": "2025-04-01T09:30:00+09:00",
      "updated_at": "2025-04-01T09:30:00+09:00"
    }
  ],
  "history": [
    {
      "year": 2024,
      "career_goals": [
        {
          "goal_id": "G001-2024",
          "goal_type": "short_term",
          "title": "JavaScript基礎の習得",
          "description": "モダンJavaScriptの基礎を習得し、簡単なWebアプリケーションを開発できるようになる",
          "target_date": "2024-12-31",
          "status": "completed",
          "priority": 5,
          "related_skills": [
            {
              "skill_id": "S005",
              "name": "JavaScript",
              "category": "technical",
              "target_level": 3,
              "current_level": 3
            }
          ],
          "action_plans": [
            {
              "action_id": "A001-2024",
              "title": "JavaScript入門コースを受講",
              "description": "オンライン学習プラットフォームでJavaScript入門コースを受講",
              "due_date": "2024-06-30",
              "status": "completed",
              "completed_date": "2024-06-20"
            }
          ],
          "feedback": [],
          "created_at": "2024-04-01T09:00:00+09:00",
          "updated_at": "2024-12-15T15:45:00+09:00"
        }
      ],
      "last_updated": "2024-12-15T15:45:00+09:00"
    }
  ],
  "last_updated": "2025-06-15T15:45:00+09:00",
  "last_updated_by": "U12345"
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_YEAR | 年度が不正です | 存在しない年度指定 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他ユーザーの情報閲覧権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 404 Not Found | CAREER_GOALS_NOT_FOUND | キャリア目標が見つかりません | 指定された年度のキャリア目標が存在しない |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "権限がありません",
    "details": "指定されたユーザーのキャリア目標情報を閲覧する権限がありません。"
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
3. キャリア目標情報の取得
   - 指定されたユーザーIDと年度のキャリア目標を取得
   - include_history=trueの場合は過去の履歴も取得
4. レスポンスの生成
   - 取得したキャリア目標情報を整形
5. レスポンス返却

### 4.2 権限チェック

- 自身のキャリア目標は常に閲覧可能
- 他ユーザーのキャリア目標閲覧には以下のいずれかの条件を満たす必要がある
  - 対象ユーザーの直属の上長である
  - キャリア目標閲覧権限（PERM_VIEW_CAREER_GOALS）を持っている
  - 管理者権限（ROLE_ADMIN）を持っている

### 4.3 年度の扱い

- 年度は4月1日から翌年3月31日までの期間
- 年度の指定がない場合は、リクエスト時点の年度を使用
- 過去の年度のキャリア目標は読み取り専用
- 未来の年度のキャリア目標は作成可能だが、現在の年度が優先表示される

### 4.4 関連データの取得

- 関連スキル情報はスキルマスタから最新の情報を取得
- 現在のスキルレベルはユーザースキル情報から取得
- フィードバック情報は直近の3件のみデフォルトで取得（全件取得オプションあり）

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-021](API仕様書_API-021.md) | スキル情報取得API | ユーザースキル情報取得 |
| [API-023](API仕様書_API-023.md) | スキルマスタ取得API | スキルマスタ情報取得 |
| [API-032](API仕様書_API-032.md) | キャリア目標更新API | キャリア目標情報更新 |
| [API-033](API仕様書_API-033.md) | 目標進捗取得API | 目標進捗情報取得 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| career_goals | キャリア目標情報 | 参照（R） |
| career_goal_skills | キャリア目標関連スキル | 参照（R） |
| career_goal_actions | キャリア目標行動計画 | 参照（R） |
| career_goal_feedback | キャリア目標フィードバック | 参照（R） |
| user_skills | ユーザースキル情報 | 参照（R） |
| skill_masters | スキルマスタ | 参照（R） |

### 5.3 注意事項・補足

- キャリア目標は短期（1年以内）、中期（1-3年）、長期（3-5年）の3種類に分類
- 各目標タイプごとに複数の目標を設定可能
- 目標の優先度は1-5の範囲で設定（5が最高優先度）
- 関連スキルは目標達成に必要なスキルを指定
- 行動計画は目標達成のための具体的なステップ
- フィードバックは上長や同僚からのコメント
- 過去の履歴は最大5年分まで保持

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

interface RelatedSkill {
  skill_id: string;
  name: string;
  category: string;
  target_level: number;
  current_level: number;
}

interface ActionPlan {
  action_id: string;
  title: string;
  description: string;
  due_date: string;
  status: 'not_started' | 'in_progress' | 'completed';
  completed_date: string | null;
}

interface Feedback {
  feedback_id: string;
  commenter_id: string;
  commenter_name: string;
  comment: string;
  created_at: string;
}

interface CareerGoal {
  goal_id: string;
  goal_type: 'short_term' | 'mid_term' | 'long_term';
  title: string;
  description: string;
  target_date: string;
  status: 'not_started' | 'in_progress' | 'completed' | 'postponed' | 'cancelled';
  priority: number;
  related_skills: RelatedSkill[];
  action_plans: ActionPlan[];
  feedback: Feedback[];
  created_at: string;
  updated_at: string;
}

interface HistoryItem {
  year: number;
  career_goals: CareerGoal[];
  last_updated: string;
}

interface CareerGoalsResponse {
  user_id: string;
  year: number;
  career_goals: CareerGoal[];
  history?: HistoryItem[];
  last_updated: string;
  last_updated_by: string;
}

const CareerGoalsView: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const [year, setYear] = useState<number>(new Date().getFullYear());
  const [includeHistory, setIncludeHistory] = useState<boolean>(false);
  const [careerGoals, setCareerGoals] = useState<CareerGoalsResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const fetchCareerGoals = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await axios.get<CareerGoalsResponse>(
          `/api/career-goals/${userId}`,
          {
            params: {
              year,
              include_history: includeHistory
            },
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
              'Accept': 'application/json'
            }
          }
        );
        
        setCareerGoals(response.data);
        
      } catch (err) {
        if (axios.isAxiosError(err) && err.response) {
          const errorData = err.response.data;
          setError(errorData.error?.message || 'キャリア目標の取得に失敗しました');
        } else {
          setError('キャリア目標の取得中にエラーが発生しました');
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchCareerGoals();
  }, [userId, year, includeHistory]);
  
  const handleYearChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setYear(parseInt(e.target.value, 10));
  };
  
  const handleHistoryToggle = () => {
    setIncludeHistory(!includeHistory);
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
  
  const renderSkillLevel = (level: number, maxLevel: number = 5) => {
    return (
      <div className="skill-level">
        {Array.from({ length: maxLevel }).map((_, index) => (
          <span
            key={index}
            className={`level-dot ${index < level ? 'filled' : 'empty'}`}
            title={`レベル ${level}/${maxLevel}`}
          />
        ))}
        <span className="level-text">{level}/{maxLevel}</span>
      </div>
    );
  };
  
  const renderGoalCard = (goal: CareerGoal) => {
    return (
      <div key={goal.goal_id} className="goal-card">
        <div className="goal-header">
          <span className={`goal-type ${goal.goal_type}`}>
            {getGoalTypeLabel(goal.goal_type)}
          </span>
          <span 
            className="goal-status" 
            style={{ backgroundColor: getStatusColor(goal.status) }}
          >
            {getStatusLabel(goal.status)}
          </span>
          <span className="goal-priority">
            優先度: {Array.from({ length: goal.priority }).map((_, i) => '★').join('')}
          </span>
        </div>
        
        <h3 className="goal-title">{goal.title}</h3>
        <p className="goal-description">{goal.description}</p>
        
        <div className="goal-target-date">
          目標達成予定日: {new Date(goal.target_date).toLocaleDateString()}
        </div>
        
        {goal.related_skills.length > 0 && (
          <div className="related-skills-section">
            <h4>関連スキル</h4>
            <div className="related-skills-list">
              {goal.related_skills.map(skill => (
                <div key={skill.skill_id} className="related-skill-item">
                  <div className="skill-info">
                    <span className="skill-name">{skill.name}</span>
                    <span className="skill-category">{skill.category}</span>
                  </div>
                  <div className="skill-levels">
                    <div className="current-level">
                      <span>現在:</span>
                      {renderSkillLevel(skill.current_level)}
                    </div>
                    <div className="target-level">
                      <span>目標:</span>
                      {renderSkillLevel(skill.target_level)}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {goal.action_plans.length > 0 && (
          <div className="action-plans-section">
            <h4>行動計画</h4>
            <div className="action-plans-list">
              {goal.action_plans.map(plan => (
                <div key={plan.action_id} className="action-plan-item">
                  <div className="action-plan-header">
                    <h5>{plan.title}</h5>
                    <span className={`action-status ${plan.status}`}>
                      {getStatusLabel(plan.status)}
                    </span>
                  </div>
                  <p>{plan.description}</p>
                  <div className="action-dates">
                    <span>期限: {new Date(plan.due_date).toLocaleDateString()}</span>
                    {plan.completed_date && (
                      <span>完了日: {new Date(plan.completed_date).toLocaleDateString()}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {goal.feedback.length > 0 && (
          <div className="feedback-section">
            <h4>フィードバック</h4>
            <div className="feedback-list">
              {goal.feedback.map(item => (
                <div key={item.feedback_id} className="feedback-item">
                  <div className="feedback-header">
                    <span className="commenter-name">{item.commenter_name}</span>
                    <span className="feedback-date">
                      {new Date(item.created_at).toLocaleString()}
                    </span>
                  </div>
                  <p className="feedback-comment">{item.comment}</p>
                </div>
              ))}
            </div>
          </div>
        )}
        
        <div className="goal-footer
