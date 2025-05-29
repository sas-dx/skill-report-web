# API仕様書：API-025 スキル検索API

## 1. 基本情報

- **API ID**: API-025
- **API名称**: スキル検索API
- **概要**: 条件指定によるスキル検索を行う
- **エンドポイント**: `/api/skills/search`
- **HTTPメソッド**: POST
- **リクエスト形式**: JSON
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-SKILL-SEARCH](画面設計書_SCR-SKILL-SEARCH.md)
- **作成日**: 2025/05/28
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/28 初版作成

---

## 2. リクエスト仕様

### 2.1 リクエストヘッダ

| ヘッダ名 | 必須 | 説明 | 備考 |
|---------|------|------|------|
| Authorization | ○ | 認証トークン | Bearer {JWT} 形式 |
| Content-Type | ○ | リクエスト形式 | application/json |
| Accept | - | レスポンス形式 | application/json |

### 2.2 リクエストボディ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| skill_conditions | array | - | スキル条件の配列 | 指定なしの場合は全ユーザーが対象 |
| department_id | string | - | 部署ID | 指定された部署に所属するユーザーのみ対象 |
| position_id | string | - | 役職ID | 指定された役職のユーザーのみ対象 |
| project_id | string | - | プロジェクトID | 指定されたプロジェクトに参加しているユーザーのみ対象 |
| certification_id | string | - | 資格ID | 指定された資格を保有するユーザーのみ対象 |
| experience_years | object | - | 経験年数条件 | |
| keyword | string | - | キーワード | ユーザー名、スキル名、説明などの部分一致検索 |
| page | number | - | ページ番号 | デフォルト: 1 |
| size | number | - | 1ページあたりの件数 | デフォルト: 20、最大: 100 |
| sort | string | - | ソート条件 | "name", "department", "skill_level"<br>デフォルト: "name" |
| order | string | - | ソート順 | "asc"（昇順）, "desc"（降順）<br>デフォルト: "asc" |

#### skill_conditions 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| skill_id | string | ○ | スキルID | |
| category | string | - | スキルカテゴリ | 指定がない場合はスキルIDのみで検索 |
| min_level | number | - | 最小レベル | 1-5の範囲、指定がない場合は1 |
| max_level | number | - | 最大レベル | 1-5の範囲、指定がない場合は5 |
| condition_type | string | - | 条件タイプ | "must"（必須）, "should"（いずれか）<br>デフォルト: "must" |

#### experience_years オブジェクト

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| min | number | - | 最小経験年数 | 0以上 |
| max | number | - | 最大経験年数 | min以上 |

### 2.3 リクエスト例

```json
{
  "skill_conditions": [
    {
      "skill_id": "S001",
      "category": "technical",
      "min_level": 3,
      "max_level": 5,
      "condition_type": "must"
    },
    {
      "skill_id": "S002",
      "min_level": 2,
      "condition_type": "should"
    }
  ],
  "department_id": "D001",
  "experience_years": {
    "min": 2,
    "max": 10
  },
  "keyword": "Java",
  "page": 1,
  "size": 20,
  "sort": "skill_level",
  "order": "desc"
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total | number | 総件数 | |
| page | number | 現在のページ番号 | |
| size | number | 1ページあたりの件数 | |
| total_pages | number | 総ページ数 | |
| users | array | ユーザー情報の配列 | |

#### users 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| name | string | ユーザー名 | |
| department | object | 部署情報 | |
| position | object | 役職情報 | |
| skills | array | スキル情報の配列 | 検索条件に一致したスキルのみ |
| matched_skills_count | number | 一致したスキル数 | |
| total_skills_count | number | 保有スキル総数 | |
| profile_image_url | string | プロフィール画像URL | |
| last_updated | string | 最終更新日時 | ISO 8601形式 |

#### department オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| department_id | string | 部署ID | |
| name | string | 部署名 | |

#### position オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| position_id | string | 役職ID | |
| name | string | 役職名 | |

#### skills 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| category | string | スキルカテゴリ | |
| name | string | スキル名 | |
| level | number | スキルレベル | 1-5（5が最高） |
| experience_years | number | 経験年数 | |
| last_used_date | string | 最終使用日 | ISO 8601形式（YYYY-MM-DD） |
| match_type | string | 一致タイプ | "must", "should" |

### 3.2 正常時レスポンス例

```json
{
  "total": 42,
  "page": 1,
  "size": 20,
  "total_pages": 3,
  "users": [
    {
      "user_id": "U12345",
      "name": "山田 太郎",
      "department": {
        "department_id": "D001",
        "name": "システム開発部"
      },
      "position": {
        "position_id": "P003",
        "name": "シニアエンジニア"
      },
      "skills": [
        {
          "skill_id": "S001",
          "category": "technical",
          "name": "Java",
          "level": 4,
          "experience_years": 5.5,
          "last_used_date": "2025-04-30",
          "match_type": "must"
        },
        {
          "skill_id": "S002",
          "category": "technical",
          "name": "Spring Framework",
          "level": 3,
          "experience_years": 3.0,
          "last_used_date": "2025-04-30",
          "match_type": "should"
        }
      ],
      "matched_skills_count": 2,
      "total_skills_count": 12,
      "profile_image_url": "https://example.com/profiles/U12345.jpg",
      "last_updated": "2025-05-15T10:30:00+09:00"
    },
    {
      "user_id": "U67890",
      "name": "鈴木 花子",
      "department": {
        "department_id": "D001",
        "name": "システム開発部"
      },
      "position": {
        "position_id": "P002",
        "name": "エンジニア"
      },
      "skills": [
        {
          "skill_id": "S001",
          "category": "technical",
          "name": "Java",
          "level": 3,
          "experience_years": 2.5,
          "last_used_date": "2025-03-15",
          "match_type": "must"
        }
      ],
      "matched_skills_count": 1,
      "total_skills_count": 8,
      "profile_image_url": "https://example.com/profiles/U67890.jpg",
      "last_updated": "2025-04-20T14:45:00+09:00"
    }
  ]
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_SKILL_ID | スキルIDが不正です | 存在しないスキルID |
| 400 Bad Request | INVALID_DEPARTMENT_ID | 部署IDが不正です | 存在しない部署ID |
| 400 Bad Request | INVALID_POSITION_ID | 役職IDが不正です | 存在しない役職ID |
| 400 Bad Request | INVALID_PROJECT_ID | プロジェクトIDが不正です | 存在しないプロジェクトID |
| 400 Bad Request | INVALID_CERTIFICATION_ID | 資格IDが不正です | 存在しない資格ID |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | スキル検索権限なし |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_SKILL_ID",
    "message": "スキルIDが不正です",
    "details": "指定されたスキルID 'S999' は存在しません。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - スキル検索権限（PERM_SEARCH_SKILLS）の確認
2. リクエストパラメータの検証
   - 各パラメータの形式・値チェック
   - 存在チェック（スキルID、部署ID、役職ID、プロジェクトID、資格ID）
3. 検索条件の構築
   - スキル条件の解析
   - 部署・役職・プロジェクト・資格条件の解析
   - 経験年数条件の解析
   - キーワード条件の解析
4. ユーザースキル情報の検索
   - 条件に合致するユーザーの抽出
   - ページネーション処理
   - ソート処理
5. レスポンスの生成
   - 検索結果の整形
6. レスポンス返却

### 4.2 検索ルール

- スキル条件（skill_conditions）
  - condition_type="must"の場合、そのスキルを必ず保有している必要がある
  - condition_type="should"の場合、いずれかのスキルを保有していれば良い
  - min_level, max_levelで指定されたレベル範囲内のスキルが対象
- 部署条件（department_id）
  - 指定された部署に所属するユーザーのみ対象
  - 下位部署も含める
- 役職条件（position_id）
  - 指定された役職のユーザーのみ対象
- プロジェクト条件（project_id）
  - 指定されたプロジェクトに参加しているユーザーのみ対象
  - 過去のプロジェクト参加者も含める
- 資格条件（certification_id）
  - 指定された資格を保有するユーザーのみ対象
- 経験年数条件（experience_years）
  - min, maxで指定された経験年数範囲内のユーザーが対象
  - 各スキルの経験年数ではなく、職務経験年数全体が対象
- キーワード条件（keyword）
  - ユーザー名、スキル名、スキル説明などの部分一致検索
  - 複数キーワードはAND条件（スペース区切り）

### 4.3 検索パフォーマンス

- 検索条件が複雑な場合、処理時間が長くなる可能性がある
- 大量のユーザーデータに対する検索は、バックグラウンドジョブとして実行することも検討
- 検索結果はキャッシュされ、同一条件での再検索時に高速化
- 検索結果は最大1000件まで取得可能（ページネーションで分割）

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-021](API仕様書_API-021.md) | スキル情報取得API | ユーザースキル情報取得 |
| [API-023](API仕様書_API-023.md) | スキルマスタ取得API | スキルマスタ情報取得 |
| [API-026](API仕様書_API-026.md) | スキルマップ生成API | スキルマップデータ生成 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| departments | 部署情報 | 参照（R） |
| positions | 役職情報 | 参照（R） |
| user_skills | ユーザースキル情報 | 参照（R） |
| skill_masters | スキルマスタ | 参照（R） |
| skill_categories | スキルカテゴリ | 参照（R） |
| projects | プロジェクト情報 | 参照（R） |
| user_projects | ユーザープロジェクト関連 | 参照（R） |
| certifications | 資格情報 | 参照（R） |
| user_certifications | ユーザー資格関連 | 参照（R） |

### 5.3 注意事項・補足

- スキル検索は人材検索・プロジェクトアサイン・スキルギャップ分析などに活用
- 検索結果は権限に応じてフィルタリングされる
  - 一般ユーザーは自部門のユーザーのみ検索可能
  - 管理者は全ユーザーを検索可能
- 検索条件が多すぎる場合、パフォーマンスに影響する可能性がある
- 検索結果は最新のスキル情報に基づく（年度指定は不可）
- 検索履歴はログとして保存され、よく使われる検索条件は推奨検索条件として提示される
- エクスポート機能を利用する場合は別APIを使用（API-061 レポート生成API）

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState } from 'react';
import axios from 'axios';

interface SkillCondition {
  skill_id: string;
  category?: string;
  min_level?: number;
  max_level?: number;
  condition_type?: 'must' | 'should';
}

interface ExperienceYears {
  min?: number;
  max?: number;
}

interface SearchParams {
  skill_conditions?: SkillCondition[];
  department_id?: string;
  position_id?: string;
  project_id?: string;
  certification_id?: string;
  experience_years?: ExperienceYears;
  keyword?: string;
  page: number;
  size: number;
  sort: string;
  order: string;
}

interface SearchResult {
  total: number;
  page: number;
  size: number;
  total_pages: number;
  users: User[];
}

interface User {
  user_id: string;
  name: string;
  department: {
    department_id: string;
    name: string;
  };
  position: {
    position_id: string;
    name: string;
  };
  skills: Skill[];
  matched_skills_count: number;
  total_skills_count: number;
  profile_image_url: string;
  last_updated: string;
}

interface Skill {
  skill_id: string;
  category: string;
  name: string;
  level: number;
  experience_years: number;
  last_used_date: string;
  match_type: string;
}

const SkillSearch: React.FC = () => {
  const [searchParams, setSearchParams] = useState<SearchParams>({
    skill_conditions: [],
    page: 1,
    size: 20,
    sort: 'name',
    order: 'asc'
  });
  
  const [searchResults, setSearchResults] = useState<SearchResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  // スキルマスタ、部署、役職などのマスタデータ（APIから取得）
  const [skillMasters, setSkillMasters] = useState<any[]>([]);
  const [departments, setDepartments] = useState<any[]>([]);
  const [positions, setPositions] = useState<any[]>([]);
  const [projects, setProjects] = useState<any[]>([]);
  const [certifications, setCertifications] = useState<any[]>([]);
  
  // コンポーネントマウント時にマスタデータを取得
  React.useEffect(() => {
    const fetchMasterData = async () => {
      try {
        // スキルマスタ取得
        const skillResponse = await axios.get('/api/skill-masters', {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        setSkillMasters(skillResponse.data.skills);
        
        // 部署情報取得
        const deptResponse = await axios.get('/api/organizations', {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        setDepartments(deptResponse.data.departments);
        
        // 役職情報取得
        const posResponse = await axios.get('/api/system/masters/positions', {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        setPositions(posResponse.data.items);
        
        // プロジェクト情報取得
        const projResponse = await axios.get('/api/system/masters/projects', {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        setProjects(projResponse.data.items);
        
        // 資格情報取得
        const certResponse = await axios.get('/api/system/masters/certifications', {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        setCertifications(certResponse.data.items);
        
      } catch (err) {
        setError('マスタデータの取得に失敗しました');
        console.error(err);
      }
    };
    
    fetchMasterData();
  }, []);
  
  // スキル条件の追加
  const handleAddSkillCondition = () => {
    setSearchParams({
      ...searchParams,
      skill_conditions: [
        ...(searchParams.skill_conditions || []),
        {
          skill_id: '',
          min_level: 1,
          max_level: 5,
          condition_type: 'must'
        }
      ]
    });
  };
  
  // スキル条件の削除
  const handleRemoveSkillCondition = (index: number) => {
    const updatedConditions = [...(searchParams.skill_conditions || [])];
    updatedConditions.splice(index, 1);
    
    setSearchParams({
      ...searchParams,
      skill_conditions: updatedConditions
    });
  };
  
  // スキル条件の更新
  const handleSkillConditionChange = (index: number, field: keyof SkillCondition, value: any) => {
    const updatedConditions = [...(searchParams.skill_conditions || [])];
    updatedConditions[index] = {
      ...updatedConditions[index],
      [field]: value
    };
    
    // スキルIDが変更された場合、カテゴリも自動設定
    if (field === 'skill_id' && value) {
      const selectedSkill = skillMasters.find(s => s.skill_id === value);
      if (selectedSkill) {
        updatedConditions[index].category = selectedSkill.category;
      }
    }
    
    setSearchParams({
      ...searchParams,
      skill_conditions: updatedConditions
    });
  };
  
  // 検索パラメータの更新（一般）
  const handleParamChange = (field: keyof SearchParams, value: any) => {
    setSearchParams({
      ...searchParams,
      [field]: value
    });
  };
  
  // 経験年数条件の更新
  const handleExperienceYearsChange = (field: keyof ExperienceYears, value: number) => {
    setSearchParams({
      ...searchParams,
      experience_years: {
        ...(searchParams.experience_years || {}),
        [field]: value
      }
    });
  };
  
  // 検索実行
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setError(null);
      
      // 検索APIリクエスト
      const response = await axios.post<SearchResult>('/api/skills/search', searchParams, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
        }
      });
      
      setSearchResults(response.data);
      
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const errorData = err.response.data;
        setError(errorData.error?.message || '検索に失敗しました');
      } else {
        setError('検索中にエラーが発生しました');
      }
    } finally {
      setLoading(false);
    }
  };
  
  // ページ変更
  const handlePageChange = (newPage: number) => {
    if (searchResults && (newPage < 1 || newPage > searchResults.total_pages)) {
      return;
    }
    
    setSearchParams({
      ...searchParams,
      page: newPage
    });
    
    // 新しいページで検索を実行
    handleSearch(new Event('submit') as any);
  };
  
  // 検索条件フォームのレンダリング
  const renderSearchForm = () => {
    return (
      <form onSubmit={handleSearch} className="search-form">
        <div className="form-section">
          <h3>スキル条件</h3>
          
          {(searchParams.skill_conditions || []).map((condition, index) => (
            <div key={index} className="skill-condition">
              <select
                value={condition.skill_id}
                onChange={(e) => handleSkillConditionChange(index, 'skill_id', e.target.value)}
                required
              >
                <option value="">スキルを選択</option>
                {skillMasters.map(skill => (
                  <option key={skill.skill_id} value={skill.skill_id}>
                    {skill.name} ({skill.category})
                  </option>
                ))}
              </select>
              
              <div className="level-range">
                <label>レベル:</label>
                <select
                  value={condition.min_level}
                  onChange={(e) => handleSkillConditionChange(index, 'min_level', parseInt(e.target.value))}
                >
                  {[1, 2, 3, 4, 5].map(level => (
                    <option key={level} value={level}>{level}</option>
                  ))}
                </select>
                <span>〜</span>
                <select
                  value={condition.max_level}
                  onChange={(e) => handleSkillConditionChange(index, 'max_level', parseInt(e.target.value))}
                >
                  {[1, 2, 3, 4, 5].map(level => (
                    <option key={level} value={level}>{level}</option>
                  ))}
                </select>
              </div>
              
              <select
                value={condition.condition_type}
                onChange={(e) => handleSkillConditionChange(index, 'condition_type', e.target.value as 'must' | 'should')}
              >
                <option value="must">必須</option>
                <option value="should">いずれか</option>
              </select>
              
              <button 
                type="button" 
                onClick={() => handleRemoveSkillCondition(index)}
                className="remove-button"
              >
                削除
              </button>
            </div>
          ))}
          
          <button 
            type="button" 
            onClick={handleAddSkillCondition}
            className="add-button"
          >
            スキル条件を追加
          </button>
        </div>
        
        <div className="form-section">
          <h3>組織条件</h3>
          
          <div className="form-group">
            <label>部署:</label>
            <select
              value={searchParams.department_id || ''}
              onChange={(e) => handleParamChange('department_id', e.target.value || undefined)}
            >
              <option value="">指定なし</option>
              {departments.map(dept => (
                <option key={dept.department_id} value={dept.department_id}>
                  {dept.name}
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label>役職:</label>
            <select
              value={searchParams.position_id || ''}
              onChange={(e) => handleParamChange('position_id', e.target.value || undefined)}
            >
              <option value="">指定なし</option>
              {positions.map(pos => (
                <option key={pos.position_id} value={pos.position_id}>
                  {pos.name}
                </option>
              ))}
            </select>
          </div>
        </div>
        
        <div className="form-section">
          <h3>その他条件</h3>
          
          <div className="form-group">
            <label>プロジェクト:</label>
            <select
              value={searchParams.project_id || ''}
              onChange={(e) => handleParamChange('project_id', e.target.value || undefined)}
            >
              <option value="">指定なし</option>
              {projects.map(proj => (
                <option key={proj.project_id} value={proj.project_id}>
                  {proj.name}
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label>資格:</label>
            <select
              value={searchParams.certification_id || ''}
              onChange={(e) => handleParamChange('certification_id', e.target.value || undefined)}
            >
              <option value="">指定なし</option>
              {certifications.map(cert => (
                <option key={cert.certification_id} value={cert.
