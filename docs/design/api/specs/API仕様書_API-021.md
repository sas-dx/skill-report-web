# API仕様書：API-021 スキル情報取得API

## 1. 基本情報

- **API ID**: API-021
- **API名称**: スキル情報取得API
- **概要**: 指定されたユーザーのスキル情報を取得する
- **エンドポイント**: `/api/skills/{user_id}`
- **HTTPメソッド**: GET
- **リクエスト形式**: URL Path Parameter + Query Parameter
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-SKILL](画面設計書_SCR-SKILL.md)
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
| include_history | boolean | - | 過去のスキル評価履歴を含めるか | デフォルト：false |
| detail_level | string | - | 詳細レベル | "summary", "standard", "detail"のいずれか<br>デフォルト："standard" |

### 2.3 リクエスト例

```
GET /api/skills/tanaka.taro?year=2025&include_history=true&detail_level=detail
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
| skills | array | スキル情報の配列 | 詳細は以下参照 |
| skill_summary | object | スキルサマリー情報 | 詳細は以下参照 |
| history | array | 過去のスキル評価履歴 | include_history=trueの場合のみ |

#### skills 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| category_id | string | スキルカテゴリID | |
| category_name | string | スキルカテゴリ名 | |
| items | array | スキル項目の配列 | 詳細は以下参照 |

#### items 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| skill_name | string | スキル名 | |
| level | number | スキルレベル | 0: 未評価, 1: 初級, 2: 中級, 3: 上級, 4: エキスパート |
| self_evaluation | string | 自己評価コメント | detail_level="detail"の場合のみ |
| manager_evaluation | string | 上長評価コメント | detail_level="detail"かつstatus="reviewed"または"approved"の場合のみ |
| experience_years | number | 経験年数 | |
| last_used_date | string | 最終使用日 | ISO 8601形式（YYYY-MM-DD） |
| projects | array | 関連プロジェクト | detail_level="detail"の場合のみ |

#### skill_summary オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total_skills | number | 総スキル数 | |
| average_level | number | 平均スキルレベル | 小数点第2位まで |
| top_skills | array | トップスキル（レベル3以上） | 最大5件 |
| improvement_areas | array | 改善推奨スキル | 最大5件 |
| skill_distribution | object | スキルレベル分布 | レベルごとの件数 |

### 3.2 正常時レスポンス例

```json
{
  "user_id": "tanaka.taro",
  "year": 2025,
  "last_updated_at": "2025-05-15T14:30:45+09:00",
  "status": "reviewed",
  "skills": [
    {
      "category_id": "programming",
      "category_name": "プログラミング言語",
      "items": [
        {
          "skill_id": "java",
          "skill_name": "Java",
          "level": 3,
          "self_evaluation": "Spring Bootを用いたWebアプリケーション開発経験あり。並列処理やパフォーマンスチューニングも実施。",
          "manager_evaluation": "プロジェクトでのコード品質が高く、チーム内でも技術的なリードができている。",
          "experience_years": 5,
          "last_used_date": "2025-04-30",
          "projects": ["販売管理システム刷新", "顧客ポータル開発"]
        },
        {
          "skill_id": "typescript",
          "skill_name": "TypeScript",
          "level": 2,
          "self_evaluation": "React/Next.jsでのフロントエンド開発経験あり。型定義の活用は得意。",
          "manager_evaluation": "基本的な実装は問題ないが、より高度な型活用やパフォーマンス最適化の経験を積むと良い。",
          "experience_years": 2,
          "last_used_date": "2025-05-10",
          "projects": ["顧客ポータル開発"]
        }
      ]
    },
    {
      "category_id": "framework",
      "category_name": "フレームワーク",
      "items": [
        {
          "skill_id": "spring",
          "skill_name": "Spring Framework",
          "level": 3,
          "self_evaluation": "DI、AOP、Spring MVC、Spring Bootの実務経験あり。マイクロサービス構築も経験。",
          "manager_evaluation": "設計面での知識も深く、適切なアーキテクチャ選定ができている。",
          "experience_years": 4,
          "last_used_date": "2025-04-30",
          "projects": ["販売管理システム刷新", "在庫管理API開発"]
        }
      ]
    }
  ],
  "skill_summary": {
    "total_skills": 15,
    "average_level": 2.47,
    "top_skills": [
      {"skill_id": "java", "skill_name": "Java", "level": 3},
      {"skill_id": "spring", "skill_name": "Spring Framework", "level": 3},
      {"skill_id": "sql", "skill_name": "SQL", "level": 3}
    ],
    "improvement_areas": [
      {"skill_id": "aws", "skill_name": "AWS", "level": 1},
      {"skill_id": "docker", "skill_name": "Docker", "level": 1}
    ],
    "skill_distribution": {
      "level0": 2,
      "level1": 3,
      "level2": 5,
      "level3": 4,
      "level4": 1
    }
  },
  "history": [
    {
      "year": 2024,
      "last_updated_at": "2024-05-20T11:20:15+09:00",
      "status": "approved",
      "average_level": 2.13,
      "skill_distribution": {
        "level0": 3,
        "level1": 4,
        "level2": 5,
        "level3": 2,
        "level4": 0
      }
    },
    {
      "year": 2023,
      "last_updated_at": "2023-05-18T10:45:30+09:00",
      "status": "approved",
      "average_level": 1.86,
      "skill_distribution": {
        "level0": 4,
        "level1": 5,
        "level2": 4,
        "level3": 1,
        "level4": 0
      }
    }
  ]
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他者のスキル情報閲覧権限なし |
| 404 Not Found | USER_NOT_FOUND | 指定されたユーザーが見つかりません | 存在しないユーザーID |
| 404 Not Found | SKILL_DATA_NOT_FOUND | 指定された年度のスキル情報が見つかりません | 存在しない年度のデータ |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "権限がありません",
    "details": "他のユーザーのスキル情報を閲覧するには適切な権限が必要です。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - スキル情報閲覧権限の確認
   - 他者のスキル情報閲覧権限の確認（自分以外のuser_idの場合）
2. リクエストパラメータの検証
   - user_idの形式チェック
   - yearの形式チェック（指定されている場合）
   - detail_levelの値チェック
3. ユーザーの存在確認
   - 指定されたuser_idのユーザーが存在するか確認
4. スキル情報の取得
   - 指定された年度のスキル情報を取得
   - 年度指定がない場合は最新年度のデータを取得
5. 詳細レベルに応じたデータの絞り込み
   - detail_level="summary"の場合、概要情報のみ
   - detail_level="standard"の場合、標準的な情報
   - detail_level="detail"の場合、詳細情報を含む
6. 履歴情報の取得（include_history=trueの場合）
   - 過去年度のスキル評価サマリーを取得
7. レスポンスの生成
   - 取得したデータを整形してJSONレスポンスを生成
8. レスポンス返却

### 4.2 アクセス制御ルール

- 自分自身のスキル情報：閲覧可能
- 部下のスキル情報：マネージャーは閲覧可能
- 同部署のスキル情報：部署管理者は閲覧可能
- 全社員のスキル情報：人事担当者・管理者は閲覧可能
- 詳細レベル"detail"：本人・直属の上司・人事担当者のみ閲覧可能

### 4.3 パフォーマンス要件

- 応答時間：平均500ms以内
- タイムアウト：10秒
- キャッシュ：ユーザー別・年度別に1時間キャッシュ
- 同時リクエスト：最大100リクエスト/秒

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-022](API仕様書_API-022.md) | スキル情報更新API | スキル情報の更新 |
| [API-023](API仕様書_API-023.md) | スキルマスタ取得API | スキルマスタ情報取得 |
| [API-025](API仕様書_API-025.md) | スキル検索API | 条件指定によるスキル検索 |
| [API-026](API仕様書_API-026.md) | スキルマップ生成API | スキルマップデータ生成 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| skills | スキル情報 | 参照（R） |
| skill_evaluations | スキル評価情報 | 参照（R） |
| skill_categories | スキルカテゴリ | 参照（R） |
| skill_masters | スキルマスタ | 参照（R） |
| skill_history | スキル履歴 | 参照（R） |
| projects | プロジェクト情報 | 参照（R） |

### 5.3 注意事項・補足

- スキル情報は年度ごとに管理
- 年度の切り替えは4月1日
- 過去3年分のスキル履歴を保持
- スキルレベルの定義：
  - レベル0：未評価/該当なし
  - レベル1：初級（基本的な知識あり）
  - レベル2：中級（実務で活用可能）
  - レベル3：上級（他者に指導可能）
  - レベル4：エキスパート（社内トップレベル）
- 自己評価と上長評価の両方が揃った場合のみ"reviewed"ステータスとなる
- 部門長の承認後に"approved"ステータスとなる

---

## 6. サンプルコード

### 6.1 スキル情報取得例（JavaScript/Fetch API）

```javascript
/**
 * ユーザーのスキル情報を取得する関数
 * @param {string} userId - ユーザーID
 * @param {Object} options - オプション
 * @param {number} [options.year] - 取得対象年度
 * @param {boolean} [options.includeHistory] - 過去のスキル評価履歴を含めるか
 * @param {string} [options.detailLevel] - 詳細レベル
 * @returns {Promise<Object>} スキル情報
 */
async function getUserSkills(userId, options = {}) {
  try {
    // クエリパラメータの構築
    const queryParams = new URLSearchParams();
    if (options.year) queryParams.append('year', options.year);
    if (options.includeHistory !== undefined) queryParams.append('include_history', options.includeHistory);
    if (options.detailLevel) queryParams.append('detail_level', options.detailLevel);
    
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
    
    // APIリクエスト
    const response = await fetch(`https://api.example.com/api/skills/${userId}${queryString}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`,
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error.message || 'スキル情報の取得に失敗しました');
    }
    
    return await response.json();
  } catch (error) {
    console.error('スキル情報取得エラー:', error);
    throw error;
  }
}
```

### 6.2 スキル情報表示コンポーネント例（React）

```jsx
import React, { useState, useEffect } from 'react';
import { getUserSkills } from '../api/skillApi';
import SkillCategoryCard from './SkillCategoryCard';
import SkillSummaryChart from './SkillSummaryChart';
import SkillHistoryGraph from './SkillHistoryGraph';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';

const UserSkillsView = ({ userId, year }) => {
  const [skillData, setSkillData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [detailLevel, setDetailLevel] = useState('standard');
  const [includeHistory, setIncludeHistory] = useState(false);
  
  // スキル情報の取得
  useEffect(() => {
    const fetchSkillData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const data = await getUserSkills(userId, {
          year,
          detailLevel,
          includeHistory
        });
        
        setSkillData(data);
      } catch (err) {
        setError(err.message || 'スキル情報の取得に失敗しました');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchSkillData();
  }, [userId, year, detailLevel, includeHistory]);
  
  // 詳細レベル変更ハンドラ
  const handleDetailLevelChange = (e) => {
    setDetailLevel(e.target.value);
  };
  
  // 履歴表示切替ハンドラ
  const handleHistoryToggle = () => {
    setIncludeHistory(!includeHistory);
  };
  
  if (isLoading) {
    return <LoadingSpinner message="スキル情報を読み込み中..." />;
  }
  
  if (error) {
    return <ErrorMessage message={error} />;
  }
  
  if (!skillData) {
    return <div className="no-data-message">スキル情報がありません</div>;
  }
  
  return (
    <div className="user-skills-container">
      <div className="skill-header">
        <h2>{year}年度 スキル情報</h2>
        <div className="skill-status">
          ステータス: <span className={`status-badge status-${skillData.status}`}>
            {skillData.status === 'draft' && '下書き'}
            {skillData.status === 'submitted' && '提出済'}
            {skillData.status === 'reviewed' && 'レビュー済'}
            {skillData.status === 'approved' && '承認済'}
          </span>
        </div>
        <div className="last-updated">
          最終更新: {new Date(skillData.last_updated_at).toLocaleString('ja-JP')}
        </div>
      </div>
      
      <div className="skill-controls">
        <div className="detail-level-selector">
          <label htmlFor="detailLevel">詳細レベル:</label>
          <select 
            id="detailLevel" 
            value={detailLevel} 
            onChange={handleDetailLevelChange}
          >
            <option value="summary">サマリー</option>
            <option value="standard">標準</option>
            <option value="detail">詳細</option>
          </select>
        </div>
        
        <div className="history-toggle">
          <label>
            <input 
              type="checkbox" 
              checked={includeHistory} 
              onChange={handleHistoryToggle} 
            />
            履歴を表示
          </label>
        </div>
      </div>
      
      <div className="skill-summary-section">
        <h3>スキルサマリー</h3>
        <div className="summary-stats">
          <div className="stat-item">
            <span className="stat-label">総スキル数</span>
            <span className="stat-value">{skillData.skill_summary.total_skills}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">平均レベル</span>
            <span className="stat-value">{skillData.skill_summary.average_level.toFixed(2)}</span>
          </div>
        </div>
        
        <SkillSummaryChart distribution={skillData.skill_summary.skill_distribution} />
        
        <div className="top-skills">
          <h4>トップスキル</h4>
          <ul>
            {skillData.skill_summary.top_skills.map(skill => (
              <li key={skill.skill_id}>
                {skill.skill_name} (レベル{skill.level})
              </li>
            ))}
          </ul>
        </div>
        
        <div className="improvement-areas">
          <h4>改善推奨スキル</h4>
          <ul>
            {skillData.skill_summary.improvement_areas.map(skill => (
              <li key={skill.skill_id}>
                {skill.skill_name} (現在レベル{skill.level})
              </li>
            ))}
          </ul>
        </div>
      </div>
      
      <div className="skill-categories-section">
        <h3>スキルカテゴリ</h3>
        {skillData.skills.map(category => (
          <SkillCategoryCard 
            key={category.category_id}
            category={category}
            detailLevel={detailLevel}
          />
        ))}
      </div>
      
      {includeHistory && skillData.history && skillData.history.length > 0 && (
        <div className="skill-history-section">
          <h3>スキル履歴</h3>
          <SkillHistoryGraph 
            currentYear={skillData.year}
            currentLevel={skillData.skill_summary.average_level}
            history={skillData.history}
          />
          
          <table className="history-table">
            <thead>
              <tr>
                <th>年度</th>
                <th>ステータス</th>
                <th>平均レベル</th>
                <th>最終更新日</th>
              </tr>
            </thead>
            <tbody>
              {skillData.history.map(item => (
                <tr key={item.year}>
                  <td>{item.year}</td>
                  <td>{item.status}</td>
                  <td>{item.average_level.toFixed(2)}</td>
                  <td>{new Date(item.last_updated_at).toLocaleDateString('ja-JP')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default UserSkillsView;
```

### 6.3 スキルレベル比較ユーティリティ例（TypeScript）

```typescript
/**
 * スキルレベル比較ユーティリティ
 */
export class SkillComparisonUtil {
  /**
   * 2つの年度間のスキル成長を分析
   * @param currentYearData 現在年度のスキルデータ
   * @param previousYearData 前年度のスキルデータ
   * @returns 成長分析結果
   */
  public static analyzeGrowth(
    currentYearData: SkillData,
    previousYearData: SkillData
  ): SkillGrowthAnalysis {
    // 平均レベルの変化
    const averageLevelChange = 
      currentYearData.skill_summary.average_level - 
      previousYearData.skill_summary.average_level;
    
    // スキルレベル分布の変化
    const distributionChange = {
      level0: this.calculateChange(
        currentYearData.skill_summary.skill_distribution.level0,
        previousYearData.skill_summary.skill_distribution.level0
      ),
      level1: this.calculateChange(
        currentYearData.skill_summary.skill_distribution.level1,
        previousYearData.skill_summary.skill_distribution.level1
      ),
      level2: this.calculateChange(
        currentYearData.skill_summary.skill_distribution.level2,
        previousYearData.skill_summary.skill_distribution.level2
      ),
      level3: this.calculateChange(
        currentYearData.skill_summary.skill_distribution.level3,
        previousYearData.skill_summary.skill_distribution.level3
      ),
      level4: this.calculateChange(
        currentYearData.skill_summary.skill_distribution.level4,
        previousYearData.skill_summary.skill_distribution.level4
      )
    };
    
    // 最も成長したスキル
    const improvedSkills = this.findImprovedSkills(
      currentYearData.skills,
      previousYearData.skills
    );
    
    // 新規獲得スキル
    const newSkills = this.findNewSkills(
      currentYearData.skills,
      previousYearData.skills
    );
    
    return {
      averageLevelChange,
      distributionChange,
      improvedSkills,
      newSkills,
      growthRate: this.calculateGrowthRate(averageLevelChange, previousYearData.skill_summary.average_level)
    };
  }
  
  /**
   * 変化量を計算
   */
  private static calculateChange(current: number, previous: number): number {
    return current - previous;
  }
  
  /**
   * 成長率を計算
   */
  private static calculateGrowthRate(change: number, previousValue: number): number {
    if (previousValue === 0) return 0;
    return (change / previousValue) * 100;
  }
  
  /**
   * 向上したスキルを特定
   */
  private static findImprovedSkills(
    currentSkills: SkillCategory[],
    previousSkills: SkillCategory[]
  ): ImprovedSkill[] {
    const improvedSkills: ImprovedSkill[] = [];
    
    // 全カテゴリのスキルをフラット化
    const currentSkillsFlat = this.flattenSkills(currentSkills);
    const previousSkillsFlat = this.flattenSkills(previousSkills);
    
    // 前年度から向上したスキルを特定
    currentSkillsFlat.forEach(currentSkill => {
      const previousSkill = previousSkillsFlat.find(
        s => s.skill_id === currentSkill.skill_id
      );
      
      if (previousSkill && currentSkill.level > previousSkill.level) {
        improvedSkills.push({
          skill_id: currentSkill.skill_id,
          skill_name: currentSkill.skill_name,
          previous_level: previousSkill.level,
          current_level: currentSkill.level,
          improvement: currentSkill.level - previousSkill.level
        });
      }
    });
    
    // 改善幅の大きい順にソート
    return improvedSkills.sort((a, b) => b.improvement - a.improvement);
  }
  
  /**
   * 新規獲得スキルを特定
   */
  private static findNewSkills(
    currentSkills: SkillCategory[],
    previousSkills: SkillCategory[]
  ): NewSkill[] {
    const newSkills: NewSkill[] = [];
    
    // 全カテゴリのスキルをフラット化
    const currentSkillsFlat = this.flattenSkills(currentSkills);
    const previousSkillsFlat = this.flattenSkills(previousSkills);
    
    // 前年度になかった新規スキルを特定
    currentSkillsFlat.forEach(currentSkill => {
      const previousSkill = previousSkillsFlat.find(
        s => s.skill_id === currentSkill.skill_id
      );
      
      if (!previousSkill && currentSkill.level > 0) {
        newSkills.push({
          skill_id: currentSkill.skill_id,
          skill_name: currentSkill.skill_name,
          level: currentSkill.level,
          category_name: currentSkill.category_name
        });
      }
    });
    
    // レベルの高い順にソート
    return newSkills.sort((a, b) => b.level - a.level);
  }
  
  /**
   * スキル
