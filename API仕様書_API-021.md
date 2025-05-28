# API仕様書：API-021 スキル情報取得API

## 1. 基本情報

- **API ID**: API-021
- **API名称**: スキル情報取得API
- **概要**: ユーザーのスキル情報を取得する
- **エンドポイント**: `/api/skills/{user_id}`
- **HTTPメソッド**: GET
- **リクエスト形式**: URLパス・クエリパラメータ
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-SKILL](画面設計書_SCR-SKILL.md)
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
| user_id | string | ○ | ユーザーID | 自身のIDまたは閲覧権限のあるユーザーID |

### 2.3 クエリパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| year | number | - | 対象年度 | 指定がない場合は最新年度<br>例: 2025 |
| category | string | - | スキルカテゴリ | 指定がない場合は全カテゴリ<br>例: "technical", "business", "language" |
| include_history | boolean | - | 履歴を含めるか | true: 過去の履歴を含める<br>false: 最新のみ（デフォルト） |

### 2.4 リクエスト例

```
GET /api/skills/U12345?year=2025&include_history=true HTTP/1.1
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
| year | number | 対象年度 | |
| last_updated | string | 最終更新日時 | ISO 8601形式 |
| skills | array | スキル情報の配列 | |
| history | array | 過去のスキル履歴 | include_history=trueの場合のみ |

#### skills 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| category | string | スキルカテゴリ | "technical", "business", "language"など |
| name | string | スキル名 | |
| level | number | スキルレベル | 1-5（5が最高） |
| experience_years | number | 経験年数 | 小数点以下1桁まで（例: 2.5） |
| description | string | 詳細説明 | ユーザーによる補足情報 |
| projects | array | 関連プロジェクト | |
| certifications | array | 関連資格 | |
| last_used_date | string | 最終使用日 | ISO 8601形式（YYYY-MM-DD） |
| self_assessment | object | 自己評価情報 | |

#### projects 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| project_id | string | プロジェクトID | |
| name | string | プロジェクト名 | |
| period | string | 期間 | "2024/04-2024/09"形式 |
| role | string | 役割 | |

#### certifications 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| certification_id | string | 資格ID | |
| name | string | 資格名 | |
| acquisition_date | string | 取得日 | ISO 8601形式（YYYY-MM-DD） |

#### self_assessment オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| strengths | string | 強み | |
| weaknesses | string | 弱み | |
| improvement_plan | string | 改善計画 | |

#### history 配列要素（include_history=trueの場合のみ）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| year | number | 年度 | |
| skills | array | その年度のスキル情報 | 上記skillsと同じ構造 |
| updated_at | string | 更新日時 | ISO 8601形式 |

### 3.2 正常時レスポンス例

```json
{
  "user_id": "U12345",
  "year": 2025,
  "last_updated": "2025-05-15T10:30:00+09:00",
  "skills": [
    {
      "skill_id": "S001",
      "category": "technical",
      "name": "Java",
      "level": 4,
      "experience_years": 5.5,
      "description": "Spring Boot、JUnit、Gradleを使用した開発経験あり",
      "projects": [
        {
          "project_id": "P001",
          "name": "顧客管理システム開発",
          "period": "2023/04-2023/09",
          "role": "バックエンド開発リーダー"
        },
        {
          "project_id": "P002",
          "name": "ECサイトリニューアル",
          "period": "2024/01-2024/06",
          "role": "アプリケーションアーキテクト"
        }
      ],
      "certifications": [
        {
          "certification_id": "C001",
          "name": "Oracle Certified Professional, Java SE 11 Developer",
          "acquisition_date": "2022-06-15"
        }
      ],
      "last_used_date": "2025-04-30",
      "self_assessment": {
        "strengths": "大規模アプリケーションの設計・実装経験が豊富",
        "weaknesses": "最新のJava機能（モジュール化など）の活用が不十分",
        "improvement_plan": "Java 17の新機能を学習し、既存プロジェクトに適用する"
      }
    },
    {
      "skill_id": "S002",
      "category": "technical",
      "name": "React",
      "level": 3,
      "experience_years": 2.0,
      "description": "Hooks、Redux、TypeScriptを使用した開発経験あり",
      "projects": [
        {
          "project_id": "P002",
          "name": "ECサイトリニューアル",
          "period": "2024/01-2024/06",
          "role": "フロントエンド開発者"
        }
      ],
      "certifications": [],
      "last_used_date": "2025-04-30",
      "self_assessment": {
        "strengths": "UIコンポーネント設計が得意",
        "weaknesses": "パフォーマンス最適化の知識が不足",
        "improvement_plan": "React Profilerを使ったパフォーマンス分析を学ぶ"
      }
    },
    {
      "skill_id": "S003",
      "category": "business",
      "name": "プロジェクト管理",
      "level": 3,
      "experience_years": 3.0,
      "description": "5名程度の小規模チームのリーダー経験あり",
      "projects": [
        {
          "project_id": "P001",
          "name": "顧客管理システム開発",
          "period": "2023/04-2023/09",
          "role": "バックエンド開発リーダー"
        }
      ],
      "certifications": [
        {
          "certification_id": "C002",
          "name": "PMP (Project Management Professional)",
          "acquisition_date": "2023-11-20"
        }
      ],
      "last_used_date": "2024-09-30",
      "self_assessment": {
        "strengths": "タスク管理とチーム内コミュニケーションが得意",
        "weaknesses": "リスク管理の経験が少ない",
        "improvement_plan": "リスク管理手法を学び、次のプロジェクトで実践する"
      }
    },
    {
      "skill_id": "S004",
      "category": "language",
      "name": "英語",
      "level": 3,
      "experience_years": 10.0,
      "description": "技術文書の読み書き、海外チームとの打ち合わせ経験あり",
      "projects": [],
      "certifications": [
        {
          "certification_id": "C003",
          "name": "TOEIC 750点",
          "acquisition_date": "2022-03-10"
        }
      ],
      "last_used_date": "2025-05-10",
      "self_assessment": {
        "strengths": "技術文書の読解力が高い",
        "weaknesses": "スピーキングに自信がない",
        "improvement_plan": "オンライン英会話を週1回受講する"
      }
    }
  ],
  "history": [
    {
      "year": 2024,
      "skills": [
        {
          "skill_id": "S001",
          "category": "technical",
          "name": "Java",
          "level": 3,
          "experience_years": 4.5,
          "description": "Spring Bootを使用した開発経験あり",
          "projects": [
            {
              "project_id": "P001",
              "name": "顧客管理システム開発",
              "period": "2023/04-2023/09",
              "role": "バックエンド開発者"
            }
          ],
          "certifications": [
            {
              "certification_id": "C001",
              "name": "Oracle Certified Professional, Java SE 11 Developer",
              "acquisition_date": "2022-06-15"
            }
          ],
          "last_used_date": "2024-03-31",
          "self_assessment": {
            "strengths": "基本的な実装スキルは高い",
            "weaknesses": "アーキテクチャ設計の経験が少ない",
            "improvement_plan": "設計パターンを学び、実践する"
          }
        },
        {
          "skill_id": "S002",
          "category": "technical",
          "name": "React",
          "level": 2,
          "experience_years": 1.0,
          "description": "基本的なコンポーネント開発の経験あり",
          "projects": [],
          "certifications": [],
          "last_used_date": "2024-03-31",
          "self_assessment": {
            "strengths": "UIデザインの実装が得意",
            "weaknesses": "状態管理の知識が不足",
            "improvement_plan": "Reduxを学習する"
          }
        }
      ],
      "updated_at": "2024-05-20T14:30:00+09:00"
    }
  ]
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他ユーザーのスキル情報閲覧権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 404 Not Found | SKILL_DATA_NOT_FOUND | 指定された年度のスキル情報が見つかりません | 指定年度のデータなし |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "権限がありません",
    "details": "他ユーザーのスキル情報を閲覧する権限がありません。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - 自身のスキル情報または閲覧権限（PERM_VIEW_SKILLS）の確認
2. リクエストパラメータの検証
   - user_idの存在確認
   - yearの形式チェック（指定されている場合）
   - categoryの値チェック（指定されている場合）
3. スキル情報の取得
   - 指定されたuser_idのスキル情報を取得
   - yearが指定されている場合は該当年度のデータを取得
   - categoryが指定されている場合は該当カテゴリのみ取得
   - include_historyがtrueの場合は過去の履歴も取得
4. レスポンスの生成
   - 取得したスキル情報を整形
5. レスポンス返却

### 4.2 スキル情報取得ルール

- 自身のスキル情報は常に閲覧可能
- 他ユーザーのスキル情報閲覧には権限（PERM_VIEW_SKILLS）が必要
- 管理者（ROLE_ADMIN）は全ユーザーのスキル情報を閲覧可能
- 上長は自部門のメンバーのスキル情報を閲覧可能
- スキルレベルは1-5の5段階評価（1:初級、2:初中級、3:中級、4:中上級、5:上級）
- 経験年数は0.5年単位で記録
- 過去5年分のスキル履歴を保持

### 4.3 パフォーマンス要件

- レスポンスタイム：平均200ms以内
- キャッシュ：ユーザーごとに1時間キャッシュ
- 同時リクエスト：最大50リクエスト/秒

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-022](API仕様書_API-022.md) | スキル情報更新API | ユーザースキル情報更新 |
| [API-023](API仕様書_API-023.md) | スキルマスタ取得API | スキルマスタ情報取得 |
| [API-025](API仕様書_API-025.md) | スキル検索API | 条件指定によるスキル検索 |
| [API-026](API仕様書_API-026.md) | スキルマップ生成API | スキルマップデータ生成 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| user_skills | ユーザースキル情報 | 参照（R） |
| skill_masters | スキルマスタ | 参照（R） |
| skill_categories | スキルカテゴリ | 参照（R） |
| user_skill_history | スキル履歴 | 参照（R） |
| projects | プロジェクト情報 | 参照（R） |
| user_projects | ユーザープロジェクト関連 | 参照（R） |
| certifications | 資格情報 | 参照（R） |
| user_certifications | ユーザー資格関連 | 参照（R） |

### 5.3 注意事項・補足

- スキル情報は年度ごとに管理され、前年度からコピーして作成される
- スキルカテゴリは「technical（技術）」「business（業務知識）」「language（言語）」「soft（ソフトスキル）」「management（マネジメント）」の5種類
- スキルレベルの定義は以下の通り
  - レベル1：基本的な知識を有し、指導のもとで作業可能
  - レベル2：基本的なタスクを独力で実行可能
  - レベル3：一般的なタスクを独力で実行可能、他者への基本的な指導可能
  - レベル4：複雑なタスクを実行可能、他者への指導可能
  - レベル5：専門家レベル、高度な問題解決と他者への指導が可能
- 関連プロジェクトは最大10件まで表示
- 関連資格は最大5件まで表示
- 履歴データは最大5年分まで取得可能

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useSearchParams } from 'react-router-dom';

interface Certification {
  certification_id: string;
  name: string;
  acquisition_date: string;
}

interface Project {
  project_id: string;
  name: string;
  period: string;
  role: string;
}

interface SelfAssessment {
  strengths: string;
  weaknesses: string;
  improvement_plan: string;
}

interface Skill {
  skill_id: string;
  category: string;
  name: string;
  level: number;
  experience_years: number;
  description: string;
  projects: Project[];
  certifications: Certification[];
  last_used_date: string;
  self_assessment: SelfAssessment;
}

interface SkillHistory {
  year: number;
  skills: Skill[];
  updated_at: string;
}

interface SkillData {
  user_id: string;
  year: number;
  last_updated: string;
  skills: Skill[];
  history?: SkillHistory[];
}

const SkillView: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [skillData, setSkillData] = useState<SkillData | null>(null);
  
  const year = searchParams.get('year') || new Date().getFullYear();
  const category = searchParams.get('category') || '';
  const includeHistory = searchParams.get('include_history') === 'true';
  
  useEffect(() => {
    const fetchSkillData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // APIリクエストURLの構築
        let url = `/api/skills/${userId}?year=${year}`;
        if (category) {
          url += `&category=${category}`;
        }
        if (includeHistory) {
          url += '&include_history=true';
        }
        
        // APIリクエスト
        const response = await axios.get<SkillData>(url, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Accept': 'application/json'
          }
        });
        
        // データの設定
        setSkillData(response.data);
        
      } catch (err) {
        if (axios.isAxiosError(err) && err.response) {
          const errorData = err.response.data;
          setError(errorData.error?.message || 'スキル情報の取得に失敗しました');
        } else {
          setError('スキル情報の取得中にエラーが発生しました');
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchSkillData();
  }, [userId, year, category, includeHistory]);
  
  const renderSkillLevel = (level: number) => {
    const maxLevel = 5;
    return (
      <div className="skill-level">
        {Array.from({ length: maxLevel }).map((_, index) => (
          <span 
            key={index} 
            className={`level-dot ${index < level ? 'filled' : 'empty'}`}
          />
        ))}
        <span className="level-text">{level}/5</span>
      </div>
    );
  };
  
  const renderSkillItem = (skill: Skill) => {
    return (
      <div key={skill.skill_id} className="skill-item">
        <div className="skill-header">
          <h3 className="skill-name">{skill.name}</h3>
          <span className="skill-category">{getCategoryLabel(skill.category)}</span>
        </div>
        
        <div className="skill-details">
          <div className="skill-metrics">
            {renderSkillLevel(skill.level)}
            <div className="experience-years">
              <span>経験年数: </span>
              <strong>{skill.experience_years}年</strong>
            </div>
            <div className="last-used">
              <span>最終使用: </span>
              <strong>{formatDate(skill.last_used_date)}</strong>
            </div>
          </div>
          
          <div className="skill-description">
            <p>{skill.description}</p>
          </div>
          
          {skill.projects.length > 0 && (
            <div className="related-projects">
              <h4>関連プロジェクト</h4>
              <ul>
                {skill.projects.map(project => (
                  <li key={project.project_id}>
                    <strong>{project.name}</strong>
                    <span className="project-period">{project.period}</span>
                    <span className="project-role">{project.role}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          {skill.certifications.length > 0 && (
            <div className="related-certifications">
              <h4>関連資格</h4>
              <ul>
                {skill.certifications.map(cert => (
                  <li key={cert.certification_id}>
                    <strong>{cert.name}</strong>
                    <span className="cert-date">取得日: {formatDate(cert.acquisition_date)}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          <div className="self-assessment">
            <h4>自己評価</h4>
            <div className="assessment-item">
              <span className="label">強み:</span>
              <p>{skill.self_assessment.strengths}</p>
            </div>
            <div className="assessment-item">
              <span className="label">弱み:</span>
              <p>{skill.self_assessment.weaknesses}</p>
            </div>
            <div className="assessment-item">
              <span className="label">改善計画:</span>
              <p>{skill.self_assessment.improvement_plan}</p>
            </div>
          </div>
        </div>
      </div>
    );
  };
  
  const getCategoryLabel = (category: string): string => {
    const categories: Record<string, string> = {
      'technical': '技術',
      'business': '業務知識',
      'language': '言語',
      'soft': 'ソフトスキル',
      'management': 'マネジメント'
    };
    return categories[category] || category;
  };
  
  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ja-JP');
  };
  
  if (loading) {
    return <div className="loading">スキル情報を読み込み中...</div>;
  }
  
  if (error) {
    return <div className="error">{error}</div>;
  }
  
  if (!skillData) {
    return <div className="no-data">スキル情報がありません</div>;
  }
  
  return (
    <div className="skill-view">
      <div className="skill-header-container">
        <h2>スキル情報 ({skillData.year}年度)</h2>
        <div className="last-updated">
          最終更新: {new Date(skillData.last_updated).toLocaleString()}
        </div>
      </div>
      
      <div className="skill-filter">
        <select 
          value={category}
          onChange={(e) => {
            const newSearchParams = new URLSearchParams(searchParams);
            newSearchParams.set('category', e.target.value);
            window.location.search = newSearchParams.toString();
          }}
        >
          <option value="">全カテゴリ</option>
          <option value="technical">技術</option>
          <option value="business">業務知識</option>
          <option value="language">言語</option>
          <option value="soft">ソフトスキル</option>
          <option value="management">マネジメント</option>
        </select>
        
        <select
          value={year.toString()}
          onChange={(e) => {
            const newSearchParams = new URLSearchParams(searchParams);
            newSearchParams.set('year', e.target.value);
            window.location.search = newSearchParams.toString();
          }}
        >
          {Array.from({ length: 5 }).map((_, index) => {
            const yearValue = new Date().getFullYear() - index;
            return (
              <option key={yearValue} value={yearValue}>
                {yearValue}年度
              </option>
            );
          })}
        </select>
        
        <label>
          <input 
            type="checkbox" 
            checked={includeHistory}
            onChange={(e) => {
              const newSearchParams = new URLSearchParams(searchParams);
              newSearchParams.set('include_history', e.target.checked.toString());
              window.location.search = newSearchParams.toString();
            }}
          />
          履歴を表示
        </label>
      </div>
      
      <div className="skills-container">
        {skillData.skills.length > 0 ? (
          skillData.skills.map(skill => renderSkillItem(skill))
        ) : (
          <div className="no-skills">
            この条件に該当するスキル情報はありません
          </div>
        )}
      </div>
      
      {includeHistory && skillData.history && skillData.history.length > 0 && (
        <div className="skill-history">
          <h3>スキル履歴</h3>
          {skillData.history.map(historyItem => (
            <div key={historyItem.year} className="history-year">
              <h4>{historyItem.year}年度</h4>
              <div className="history-skills">
                {historyItem.skills.map(skill => renderSkillItem(skill))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SkillView;
```

### 6.2 バックエンド実装例（Java/Spring Boot）

```java
package com.example.skillreport.
