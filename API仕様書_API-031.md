# API仕様書：API-031 キャリア目標取得API

## 1. 基本情報

- **API ID**: API-031
- **API名称**: キャリア目標取得API
- **概要**: 指定されたユーザーのキャリア目標情報を取得する
- **エンドポイント**: `/api/career-goals/{user_id}`
- **HTTPメソッド**: GET
- **リクエスト形式**: URL Path Parameter + Query Parameter
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-CAREER](画面設計書_SCR-CAREER.md)
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
| include_history | boolean | - | 過去のキャリア目標履歴を含めるか | デフォルト：false |
| include_templates | boolean | - | 推奨テンプレートを含めるか | デフォルト：false |

### 2.3 リクエスト例

```
GET /api/career-goals/tanaka.taro?year=2025&include_history=true&include_templates=true
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| year | number | 年度 | 西暦4桁 |
| last_updated_at | string | 最終更新日時 | ISO 8601形式 |
| status | string | ステータス | "draft", "submitted", "reviewed", "approved"のいずれか |
| career_vision | object | キャリアビジョン | 詳細は以下参照 |
| goals | array | 目標情報の配列 | 詳細は以下参照 |
| skill_development_plan | object | スキル開発計画 | 詳細は以下参照 |
| feedback | object | フィードバック情報 | status="reviewed"または"approved"の場合のみ |
| history | array | 過去のキャリア目標履歴 | include_history=trueの場合のみ |
| templates | array | 推奨テンプレート | include_templates=trueの場合のみ |

#### career_vision オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| short_term | string | 短期ビジョン（1年） | |
| mid_term | string | 中期ビジョン（3年） | |
| long_term | string | 長期ビジョン（5年以上） | |
| focus_areas | array | 注力領域 | 最大5つ |

#### goals 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| goal_id | string | 目標ID | UUID形式 |
| category | string | カテゴリ | "technical", "business", "management", "communication", "other"のいずれか |
| title | string | 目標タイトル | 100文字以内 |
| description | string | 目標詳細 | 1000文字以内 |
| priority | number | 優先度 | 1: 低, 2: 中, 3: 高 |
| target_date | string | 目標達成予定日 | ISO 8601形式（YYYY-MM-DD） |
| metrics | array | 評価指標 | 詳細は以下参照 |
| related_skills | array | 関連スキル | スキルIDの配列 |

#### metrics 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| metric_id | string | 指標ID | UUID形式 |
| name | string | 指標名 | 50文字以内 |
| target_value | string | 目標値 | 100文字以内 |
| current_value | string | 現在値 | 100文字以内 |
| unit | string | 単位 | 20文字以内 |

#### skill_development_plan オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| focus_skills | array | 注力スキル | スキルIDと目標レベルの配列 |
| training_plans | array | 研修計画 | 詳細は以下参照 |
| self_development | string | 自己啓発計画 | 1000文字以内 |

#### focus_skills 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| skill_name | string | スキル名 | |
| current_level | number | 現在レベル | 0-4 |
| target_level | number | 目標レベル | 1-4 |
| actions | array | 習得アクション | 文字列の配列 |

#### training_plans 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| training_id | string | 研修ID | |
| training_name | string | 研修名 | |
| category | string | カテゴリ | |
| scheduled_date | string | 予定日 | ISO 8601形式（YYYY-MM-DD） |
| status | string | ステータス | "planned", "registered", "completed", "cancelled"のいずれか |

#### feedback オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| reviewer_id | string | レビュアーID | |
| reviewer_name | string | レビュアー名 | |
| review_date | string | レビュー日 | ISO 8601形式 |
| comments | string | コメント | 2000文字以内 |
| suggestions | array | 提案 | 文字列の配列 |
| approval_status | string | 承認ステータス | "pending", "approved", "rejected"のいずれか |

### 3.2 正常時レスポンス例

```json
{
  "user_id": "tanaka.taro",
  "year": 2025,
  "last_updated_at": "2025-05-15T14:30:45+09:00",
  "status": "reviewed",
  "career_vision": {
    "short_term": "バックエンド開発のスキルを向上させ、チーム内での技術的リーダーシップを発揮する。マイクロサービスアーキテクチャの設計・実装経験を積む。",
    "mid_term": "フルスタックエンジニアとしての能力を高め、プロジェクト全体の技術設計を担当できるレベルに達する。クラウドネイティブ開発の専門性を確立する。",
    "long_term": "技術アーキテクトとして複数プロジェクトの技術戦略を策定し、後進の育成にも携わる。社内の技術標準化にも貢献する。",
    "focus_areas": ["バックエンド開発", "クラウドネイティブ", "アーキテクチャ設計", "技術リーダーシップ"]
  },
  "goals": [
    {
      "goal_id": "g-12345-abcde-67890",
      "category": "technical",
      "title": "マイクロサービスアーキテクチャの設計・実装スキル習得",
      "description": "実際のプロジェクトでマイクロサービスアーキテクチャを採用し、設計から実装までを経験する。特にサービス間通信、データ整合性、障害対応パターンについて理解を深める。",
      "priority": 3,
      "target_date": "2025-12-31",
      "metrics": [
        {
          "metric_id": "m-12345-abcde-11111",
          "name": "マイクロサービス設計ドキュメント作成",
          "target_value": "3件以上",
          "current_value": "1件",
          "unit": "件"
        },
        {
          "metric_id": "m-12345-abcde-22222",
          "name": "マイクロサービス実装完了",
          "target_value": "2サービス以上",
          "current_value": "0サービス",
          "unit": "サービス"
        }
      ],
      "related_skills": ["microservices", "api-design", "spring-cloud", "docker", "kubernetes"]
    },
    {
      "goal_id": "g-67890-fghij-12345",
      "category": "business",
      "title": "業務知識の拡充と要件定義スキルの向上",
      "description": "金融ドメインの業務知識を深め、顧客要件を技術要件に落とし込むスキルを向上させる。特に決済システムの知識を重点的に学習する。",
      "priority": 2,
      "target_date": "2025-09-30",
      "metrics": [
        {
          "metric_id": "m-67890-fghij-33333",
          "name": "業務知識研修受講",
          "target_value": "3コース",
          "current_value": "1コース",
          "unit": "コース"
        },
        {
          "metric_id": "m-67890-fghij-44444",
          "name": "要件定義ドキュメント作成",
          "target_value": "2件",
          "current_value": "0件",
          "unit": "件"
        }
      ],
      "related_skills": ["requirement-analysis", "financial-domain", "payment-systems"]
    }
  ],
  "skill_development_plan": {
    "focus_skills": [
      {
        "skill_id": "microservices",
        "skill_name": "マイクロサービス",
        "current_level": 1,
        "target_level": 3,
        "actions": [
          "社内研修「マイクロサービスアーキテクチャ入門」受講",
          "書籍「Microservices Patterns」を読破",
          "実際のプロジェクトでの実装経験を積む"
        ]
      },
      {
        "skill_id": "kubernetes",
        "skill_name": "Kubernetes",
        "current_level": 1,
        "target_level": 2,
        "actions": [
          "Kubernetes認定資格（CKA）取得",
          "社内クラウドネイティブ勉強会への参加",
          "小規模なアプリケーションをKubernetesにデプロイする練習"
        ]
      }
    ],
    "training_plans": [
      {
        "training_id": "t-12345",
        "training_name": "マイクロサービスアーキテクチャ入門",
        "category": "技術研修",
        "scheduled_date": "2025-06-15",
        "status": "registered"
      },
      {
        "training_id": "t-67890",
        "training_name": "Kubernetes実践ワークショップ",
        "category": "技術研修",
        "scheduled_date": "2025-08-20",
        "status": "planned"
      }
    ],
    "self_development": "技術書籍の読破（月1冊）、技術ブログの定期的な執筆（月2回）、社外技術コミュニティへの参加（四半期に1回）を継続的に行う。特にマイクロサービス、クラウドネイティブ技術に関する知識を深める。また、英語力向上のためオンライン英会話を週1回受講する。"
  },
  "feedback": {
    "reviewer_id": "yamada.manager",
    "reviewer_name": "山田 部長",
    "review_date": "2025-05-20T10:15:30+09:00",
    "comments": "技術的な目標設定は具体的で良いと思います。マイクロサービスの知識習得は今後のキャリアにとって重要です。一方で、チームメンバーとの協業やコミュニケーションに関する目標も追加すると良いでしょう。また、目標達成のためのタイムラインをより細かく設定することをお勧めします。",
    "suggestions": [
      "コミュニケーションスキル向上に関する目標の追加を検討してください",
      "四半期ごとの中間目標を設定するとより進捗管理がしやすくなります",
      "社外の技術コミュニティ活動も検討してみてはいかがでしょうか"
    ],
    "approval_status": "approved"
  },
  "history": [
    {
      "year": 2024,
      "last_updated_at": "2024-05-18T11:20:15+09:00",
      "status": "approved",
      "summary": {
        "career_vision_short": "Javaバックエンド開発のスキル向上とチーム開発での貢献",
        "main_goals": [
          "Spring Frameworkの実践的スキル習得",
          "コードレビュースキルの向上",
          "アジャイル開発手法の習得"
        ],
        "achievement_rate": 85
      }
    },
    {
      "year": 2023,
      "last_updated_at": "2023-05-15T10:45:30+09:00",
      "status": "approved",
      "summary": {
        "career_vision_short": "Webアプリケーション開発の基礎スキル習得",
        "main_goals": [
          "Java言語の基礎習得",
          "データベース設計の基礎習得",
          "チーム開発への参画"
        ],
        "achievement_rate": 90
      }
    }
  ],
  "templates": [
    {
      "template_id": "tpl-12345",
      "template_name": "バックエンド開発者キャリアパス",
      "description": "バックエンド開発者向けの標準的なキャリア目標テンプレート",
      "recommended_goals": [
        {
          "category": "technical",
          "title": "クラウドネイティブアプリケーション開発スキルの習得",
          "description": "クラウドネイティブ技術（コンテナ、オーケストレーション、サーバーレス等）を学び、実際のプロジェクトで活用する"
        },
        {
          "category": "technical",
          "title": "セキュアコーディングスキルの向上",
          "description": "OWASP Top 10を理解し、セキュリティを考慮したコーディング手法を習得する"
        }
      ]
    },
    {
      "template_id": "tpl-67890",
      "template_name": "テックリード育成パス",
      "description": "将来的にテックリードを目指す開発者向けのキャリア目標テンプレート",
      "recommended_goals": [
        {
          "category": "management",
          "title": "技術的意思決定プロセスの習得",
          "description": "アーキテクチャ選定や技術スタック決定などの技術的意思決定プロセスを学び、小規模な決定から実践する"
        },
        {
          "category": "communication",
          "title": "技術的なコミュニケーション能力の向上",
          "description": "技術的な内容を非技術者にも分かりやすく説明するスキルを習得し、社内勉強会などで実践する"
        }
      ]
    }
  ]
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他者のキャリア目標閲覧権限なし |
| 404 Not Found | USER_NOT_FOUND | 指定されたユーザーが見つかりません | 存在しないユーザーID |
| 404 Not Found | CAREER_GOAL_NOT_FOUND | 指定された年度のキャリア目標が見つかりません | 存在しない年度のデータ |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "権限がありません",
    "details": "他のユーザーのキャリア目標を閲覧するには適切な権限が必要です。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - キャリア目標閲覧権限の確認
   - 他者のキャリア目標閲覧権限の確認（自分以外のuser_idの場合）
2. リクエストパラメータの検証
   - user_idの形式チェック
   - yearの形式チェック（指定されている場合）
3. ユーザーの存在確認
   - 指定されたuser_idのユーザーが存在するか確認
4. キャリア目標情報の取得
   - 指定された年度のキャリア目標情報を取得
   - 年度指定がない場合は最新年度のデータを取得
5. 関連情報の取得
   - 関連スキル情報の取得
   - フィードバック情報の取得（status="reviewed"または"approved"の場合）
6. 履歴情報の取得（include_history=trueの場合）
   - 過去年度のキャリア目標サマリーを取得
7. テンプレート情報の取得（include_templates=trueの場合）
   - ユーザーの役割・スキルに基づいた推奨テンプレートを取得
8. レスポンスの生成
   - 取得したデータを整形してJSONレスポンスを生成
9. レスポンス返却

### 4.2 アクセス制御ルール

- 自分自身のキャリア目標：閲覧可能
- 部下のキャリア目標：マネージャーは閲覧可能
- 同部署のキャリア目標サマリー：部署管理者は閲覧可能
- 全社員のキャリア目標サマリー：人事担当者・管理者は閲覧可能
- フィードバック情報：本人・直属の上司・人事担当者のみ閲覧可能

### 4.3 パフォーマンス要件

- 応答時間：平均300ms以内
- タイムアウト：5秒
- キャッシュ：ユーザー別・年度別に1時間キャッシュ
- 同時リクエスト：最大50リクエスト/秒

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-032](API仕様書_API-032.md) | キャリア目標更新API | キャリア目標情報の更新 |
| [API-033](API仕様書_API-033.md) | 目標進捗取得API | 目標進捗情報取得 |
| [API-034](API仕様書_API-034.md) | 目標進捗更新API | 目標進捗情報更新 |
| [API-021](API仕様書_API-021.md) | スキル情報取得API | ユーザースキル情報取得 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| career_goals | キャリア目標情報 | 参照（R） |
| career_visions | キャリアビジョン情報 | 参照（R） |
| goals | 目標情報 | 参照（R） |
| goal_metrics | 目標評価指標 | 参照（R） |
| skill_development_plans | スキル開発計画 | 参照（R） |
| training_plans | 研修計画 | 参照（R） |
| goal_feedbacks | フィードバック情報 | 参照（R） |
| career_goal_history | キャリア目標履歴 | 参照（R） |
| career_goal_templates | キャリア目標テンプレート | 参照（R） |

### 5.3 注意事項・補足

- キャリア目標情報は年度ごとに管理
- 年度の切り替えは4月1日
- 過去5年分のキャリア目標履歴を保持
- キャリアビジョンは短期（1年）、中期（3年）、長期（5年以上）の3段階で設定
- 目標は優先度（高・中・低）で管理
- 目標には具体的な評価指標（メトリクス）を設定
- 自己評価と上長評価の両方が揃った場合のみ"reviewed"ステータスとなる
- 部門長の承認後に"approved"ステータスとなる
- テンプレートはユーザーの役割・スキルに基づいて推奨される

---

## 6. サンプルコード

### 6.1 キャリア目標取得例（JavaScript/Fetch API）

```javascript
/**
 * ユーザーのキャリア目標情報を取得する関数
 * @param {string} userId - ユーザーID
 * @param {Object} options - オプション
 * @param {number} [options.year] - 取得対象年度
 * @param {boolean} [options.includeHistory] - 過去のキャリア目標履歴を含めるか
 * @param {boolean} [options.includeTemplates] - 推奨テンプレートを含めるか
 * @returns {Promise<Object>} キャリア目標情報
 */
async function getUserCareerGoals(userId, options = {}) {
  try {
    // クエリパラメータの構築
    const queryParams = new URLSearchParams();
    if (options.year) queryParams.append('year', options.year);
    if (options.includeHistory !== undefined) queryParams.append('include_history', options.includeHistory);
    if (options.includeTemplates !== undefined) queryParams.append('include_templates', options.includeTemplates);
    
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
    
    // APIリクエスト
    const response = await fetch(`https://api.example.com/api/career-goals/${userId}${queryString}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`,
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error.message || 'キャリア目標情報の取得に失敗しました');
    }
    
    return await response.json();
  } catch (error) {
    console.error('キャリア目標情報取得エラー:', error);
    throw error;
  }
}
```

### 6.2 キャリア目標表示コンポーネント例（React）

```jsx
import React, { useState, useEffect } from 'react';
import { getUserCareerGoals } from '../api/careerApi';
import CareerVisionCard from './CareerVisionCard';
import GoalsList from './GoalsList';
import SkillDevelopmentPlan from './SkillDevelopmentPlan';
import FeedbackSection from './FeedbackSection';
import HistoryTimeline from './HistoryTimeline';
import TemplateSelector from './TemplateSelector';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';

const UserCareerGoalsView = ({ userId, year }) => {
  const [careerData, setCareerData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [includeHistory, setIncludeHistory] = useState(false);
  const [includeTemplates, setIncludeTemplates] = useState(false);
  
  // キャリア目標情報の取得
  useEffect(() => {
    const fetchCareerData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const data = await getUserCareerGoals(userId, {
          year,
          includeHistory,
          includeTemplates
        });
        
        setCareerData(data);
      } catch (err) {
        setError(err.message || 'キャリア目標情報の取得に失敗しました');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchCareerData();
  }, [userId, year, includeHistory, includeTemplates]);
  
  // 履歴表示切替ハンドラ
  const handleHistoryToggle = () => {
    setIncludeHistory(!includeHistory);
  };
  
  // テンプレート表示切替ハンドラ
  const handleTemplatesToggle = () => {
    setIncludeTemplates(!includeTemplates);
  };
  
  if (isLoading) {
    return <LoadingSpinner message="キャリア目標情報を読み込み中..." />;
  }
  
  if (error) {
    return <ErrorMessage message={error} />;
  }
  
  if (!careerData) {
    return <div className="no-data-message">キャリア目標情報がありません</div>;
  }
  
  return (
    <div className="user-career-container">
      <div className="career-header">
        <h2>{year}年度 キャリア目標</h2>
        <div className="career-status">
          ステータス: <span className={`status-badge status-${careerData.status}`}>
            {careerData.status === 'draft' && '下書き'}
            {careerData.status === 'submitted' && '提出済'}
            {careerData.status === 'reviewed' && 'レビュー済'}
            {careerData.status === 'approved' && '承認済'}
          </span>
        </div>
        <div className="last-updated">
          最終更新: {new Date(careerData.last_updated_at).toLocaleString('ja-JP')}
        </div>
      </div>
      
      <div className="career-controls">
        <div className="history-toggle">
          <label>
            <input 
              type="checkbox" 
              checked={includeHistory} 
              onChange={handleHistoryToggle} 
            />
            履歴を表示
          </label>
