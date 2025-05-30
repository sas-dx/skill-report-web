# API定義書：API-024 スキルマスタ更新API

## 1. 基本情報

- **API ID**: API-024
- **API名称**: スキルマスタ更新API
- **概要**: スキルマスタ情報を更新する
- **エンドポイント**: `/api/skill-masters`
- **HTTPメソッド**: PUT
- **リクエスト形式**: JSON
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-SKILL-M](画面設計書_SCR-SKILL-M.md)
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
| skills | array | ○ | スキルマスタ情報の配列 | |

#### skills 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| skill_id | string | ○ | スキルID | 新規登録時は空文字列 |
| category | string | ○ | スキルカテゴリ | "technical", "business", "language", "soft", "management" |
| name | string | ○ | スキル名 | 最大100文字 |
| description | string | ○ | 説明 | 最大500文字 |
| synonyms | array | - | 同義語 | 最大5件 |
| related_skills | array | - | 関連スキル | 最大10件 |
| operation | string | ○ | 操作種別 | "create", "update", "delete" |

#### related_skills 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| skill_id | string | ○ | 関連スキルID | |
| relation_type | string | ○ | 関連タイプ | "parent", "child", "related" |

### 2.3 リクエスト例

```json
{
  "skills": [
    {
      "skill_id": "S001",
      "category": "technical",
      "name": "Java",
      "description": "オブジェクト指向プログラミング言語。エンタープライズアプリケーション開発に広く使用されている。",
      "synonyms": ["Java SE", "Java EE", "JDK"],
      "related_skills": [
        {
          "skill_id": "S002",
          "relation_type": "related"
        },
        {
          "skill_id": "S003",
          "relation_type": "related"
        }
      ],
      "operation": "update"
    },
    {
      "skill_id": "",
      "category": "technical",
      "name": "Kotlin",
      "description": "JVM上で動作する静的型付けプログラミング言語。Javaとの相互運用性が高い。",
      "synonyms": ["KT"],
      "related_skills": [
        {
          "skill_id": "S001",
          "relation_type": "related"
        }
      ],
      "operation": "create"
    },
    {
      "skill_id": "S010",
      "operation": "delete"
    }
  ]
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| success | boolean | 処理結果 | true: 成功 |
| updated_at | string | 更新日時 | ISO 8601形式 |
| results | array | 更新結果の配列 | |

#### results 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | 新規作成の場合は新たに生成されたID |
| name | string | スキル名 | |
| operation | string | 操作種別 | "create", "update", "delete" |
| status | string | 処理状態 | "success", "error" |
| message | string | メッセージ | エラー時のみ設定 |

### 3.2 正常時レスポンス例

```json
{
  "success": true,
  "updated_at": "2025-05-28T15:30:00+09:00",
  "results": [
    {
      "skill_id": "S001",
      "name": "Java",
      "operation": "update",
      "status": "success"
    },
    {
      "skill_id": "S100",
      "name": "Kotlin",
      "operation": "create",
      "status": "success"
    },
    {
      "skill_id": "S010",
      "name": "COBOL",
      "operation": "delete",
      "status": "success"
    }
  ]
}
```

### 3.3 エラー時レスポンス（全体エラー）

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | スキルマスタ更新権限なし |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例（全体エラー）

```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "権限がありません",
    "details": "スキルマスタを更新する権限がありません。"
  }
}
```

### 3.5 部分エラー時レスポンス

一部のスキルの更新に失敗した場合、全体としては200 OKを返し、個別のエラーはresults配列内で表現します。

```json
{
  "success": true,
  "updated_at": "2025-05-28T15:30:00+09:00",
  "results": [
    {
      "skill_id": "S001",
      "name": "Java",
      "operation": "update",
      "status": "success"
    },
    {
      "skill_id": "",
      "name": "Kotlin",
      "operation": "create",
      "status": "error",
      "message": "同名のスキルが既に存在します"
    },
    {
      "skill_id": "S999",
      "name": "",
      "operation": "delete",
      "status": "error",
      "message": "指定されたスキルIDが存在しません"
    }
  ]
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - スキルマスタ更新権限（PERM_UPDATE_SKILL_MASTERS）の確認
2. リクエストパラメータの検証
   - スキル情報の各項目の形式・値チェック
3. スキルマスタ情報の更新
   - 操作種別に応じた処理（作成/更新/削除）
   - 関連スキル情報の更新
   - 同義語情報の更新
4. レスポンスの生成
   - 更新結果を整形
5. レスポンス返却

### 4.2 スキルマスタ更新ルール

- スキルマスタの更新には管理者権限（ROLE_ADMIN）または専用の更新権限（PERM_UPDATE_SKILL_MASTERS）が必要
- 操作種別は以下の3種類
  - create: 新規作成（skill_idは空文字列）
  - update: 更新（既存のskill_idを指定）
  - delete: 削除（skill_idのみ指定）
- 同一カテゴリ内で同名のスキルは登録不可
- 削除対象のスキルが他のスキルから参照されている場合は削除不可
- 削除対象のスキルがユーザースキルとして登録されている場合は削除不可
- 関連スキルの相互参照（循環参照）は許可しない
- 同義語は最大5件まで登録可能
- 関連スキルは最大10件まで登録可能
- スキルマスタの更新はトランザクションで管理し、全体が成功または失敗する
- 部分的なエラーが発生した場合は、エラーが発生したスキルのみ更新をスキップし、他のスキルは更新を続行

### 4.3 バリデーションルール

- スキル名：必須、1-100文字
- カテゴリ：必須、定義された値のいずれか
- 説明：必須、1-500文字
- 同義語：任意、最大5件、各1-50文字
- 関連スキル：任意、最大10件
- 関連タイプ：必須、"parent", "child", "related"のいずれか

### 4.4 トランザクション管理

- スキルマスタの更新は単一トランザクションで処理
- 関連テーブル（同義語、関連スキル）も同一トランザクションで更新
- 全体エラー発生時は全ての更新をロールバック
- 部分エラー発生時は該当スキルのみロールバックし、他のスキルは更新を続行

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-021](API仕様書_API-021.md) | スキル情報取得API | ユーザースキル情報取得 |
| [API-022](API仕様書_API-022.md) | スキル情報更新API | ユーザースキル情報更新 |
| [API-023](API仕様書_API-023.md) | スキルマスタ取得API | スキルマスタ情報取得 |
| [API-025](API仕様書_API-025.md) | スキル検索API | 条件指定によるスキル検索 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| skill_masters | スキルマスタ | 作成（C）、更新（U）、削除（D） |
| skill_categories | スキルカテゴリ | 参照（R） |
| skill_synonyms | スキル同義語 | 作成（C）、更新（U）、削除（D） |
| skill_relations | スキル関連情報 | 作成（C）、更新（U）、削除（D） |
| skill_popularity | スキル人気度 | 参照（R） |
| user_skills | ユーザースキル情報 | 参照（R） |

### 5.3 注意事項・補足

- スキルマスタの更新は管理者のみ実行可能
- スキルマスタの更新はシステム全体に影響するため、慎重に行う必要がある
- スキル名は一意であるが、カテゴリが異なれば同名のスキルが存在可能
- 人気度（popularity）は自動計算されるため、更新APIでは指定不可
- スキルマスタの更新履歴は別途ログテーブルに記録される
- 大量のスキルを一括更新する場合は、バッチ処理を推奨
- スキルマスタの更新後、キャッシュは自動的にクリアされる
- 削除対象のスキルがユーザースキルとして登録されている場合は、代替スキルへの移行を検討する必要がある

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

interface RelatedSkill {
  skill_id: string;
  relation_type: string;
}

interface Skill {
  skill_id: string;
  category: string;
  name: string;
  description: string;
  synonyms: string[];
  related_skills: RelatedSkill[];
  operation: 'create' | 'update' | 'delete';
}

interface SkillFormData {
  skills: Skill[];
}

interface UpdateResult {
  skill_id: string;
  name: string;
  operation: string;
  status: string;
  message?: string;
}

interface UpdateResponse {
  success: boolean;
  updated_at: string;
  results: UpdateResult[];
}

const SkillMasterEditForm: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState<boolean>(true);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<SkillFormData>({
    skills: []
  });
  const [categories, setCategories] = useState<any[]>([]);
  const [existingSkills, setExistingSkills] = useState<any[]>([]);
  const [results, setResults] = useState<UpdateResult[] | null>(null);
  
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // スキルマスタ情報を取得
        const response = await axios.get('/api/skill-masters', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Accept': 'application/json'
          }
        });
        
        // カテゴリ情報を設定
        setCategories(response.data.categories);
        
        // 既存のスキル情報を設定
        setExistingSkills(response.data.skills);
        
        // 初期フォームデータを設定（空の状態）
        setFormData({
          skills: []
        });
        
      } catch (err) {
        if (axios.isAxiosError(err) && err.response) {
          const errorData = err.response.data;
          setError(errorData.error?.message || 'スキルマスタの取得に失敗しました');
        } else {
          setError('スキルマスタの取得中にエラーが発生しました');
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchInitialData();
  }, []);
  
  const handleAddSkill = () => {
    setFormData({
      skills: [
        ...formData.skills,
        {
          skill_id: '',
          category: 'technical',
          name: '',
          description: '',
          synonyms: [],
          related_skills: [],
          operation: 'create'
        }
      ]
    });
  };
  
  const handleEditExistingSkill = (skill: any) => {
    // 既存のスキルを編集用に追加
    setFormData({
      skills: [
        ...formData.skills,
        {
          skill_id: skill.skill_id,
          category: skill.category,
          name: skill.name,
          description: skill.description,
          synonyms: skill.synonyms || [],
          related_skills: skill.related_skills.map((rs: any) => ({
            skill_id: rs.skill_id,
            relation_type: rs.relation_type
          })),
          operation: 'update'
        }
      ]
    });
  };
  
  const handleDeleteSkill = (skill: any) => {
    // 削除用にスキルを追加
    setFormData({
      skills: [
        ...formData.skills,
        {
          skill_id: skill.skill_id,
          category: '',
          name: skill.name,
          description: '',
          synonyms: [],
          related_skills: [],
          operation: 'delete'
        }
      ]
    });
  };
  
  const handleRemoveFromForm = (index: number) => {
    const updatedSkills = [...formData.skills];
    updatedSkills.splice(index, 1);
    setFormData({
      skills: updatedSkills
    });
  };
  
  const handleSkillChange = (index: number, field: keyof Skill, value: any) => {
    const updatedSkills = [...formData.skills];
    updatedSkills[index] = {
      ...updatedSkills[index],
      [field]: value
    };
    setFormData({
      skills: updatedSkills
    });
  };
  
  const handleAddSynonym = (skillIndex: number) => {
    const updatedSkills = [...formData.skills];
    const currentSkill = updatedSkills[skillIndex];
    
    if (currentSkill.synonyms.length >= 5) {
      alert('同義語は最大5件まで登録できます');
      return;
    }
    
    currentSkill.synonyms = [...currentSkill.synonyms, ''];
    setFormData({
      skills: updatedSkills
    });
  };
  
  const handleSynonymChange = (skillIndex: number, synonymIndex: number, value: string) => {
    const updatedSkills = [...formData.skills];
    updatedSkills[skillIndex].synonyms[synonymIndex] = value;
    setFormData({
      skills: updatedSkills
    });
  };
  
  const handleRemoveSynonym = (skillIndex: number, synonymIndex: number) => {
    const updatedSkills = [...formData.skills];
    updatedSkills[skillIndex].synonyms.splice(synonymIndex, 1);
    setFormData({
      skills: updatedSkills
    });
  };
  
  const handleAddRelatedSkill = (skillIndex: number) => {
    const updatedSkills = [...formData.skills];
    const currentSkill = updatedSkills[skillIndex];
    
    if (currentSkill.related_skills.length >= 10) {
      alert('関連スキルは最大10件まで登録できます');
      return;
    }
    
    currentSkill.related_skills = [
      ...currentSkill.related_skills,
      { skill_id: '', relation_type: 'related' }
    ];
    
    setFormData({
      skills: updatedSkills
    });
  };
  
  const handleRelatedSkillChange = (
    skillIndex: number,
    relatedIndex: number,
    field: keyof RelatedSkill,
    value: string
  ) => {
    const updatedSkills = [...formData.skills];
    updatedSkills[skillIndex].related_skills[relatedIndex] = {
      ...updatedSkills[skillIndex].related_skills[relatedIndex],
      [field]: value
    };
    setFormData({
      skills: updatedSkills
    });
  };
  
  const handleRemoveRelatedSkill = (skillIndex: number, relatedIndex: number) => {
    const updatedSkills = [...formData.skills];
    updatedSkills[skillIndex].related_skills.splice(relatedIndex, 1);
    setFormData({
      skills: updatedSkills
    });
  };
  
  const validateForm = (): boolean => {
    // 各スキルのバリデーション
    for (const skill of formData.skills) {
      if (skill.operation === 'delete') {
        // 削除の場合はskill_idのみ必要
        if (!skill.skill_id) {
          alert('削除対象のスキルIDが指定されていません');
          return false;
        }
        continue;
      }
      
      // 作成・更新の場合は必須項目をチェック
      if (!skill.name) {
        alert('スキル名は必須です');
        return false;
      }
      
      if (!skill.category) {
        alert('カテゴリは必須です');
        return false;
      }
      
      if (!skill.description) {
        alert('説明は必須です');
        return false;
      }
      
      // 関連スキルのバリデーション
      for (const related of skill.related_skills) {
        if (!related.skill_id) {
          alert('関連スキルIDは必須です');
          return false;
        }
        
        if (!related.relation_type) {
          alert('関連タイプは必須です');
          return false;
        }
        
        // 自己参照チェック
        if (skill.skill_id && related.skill_id === skill.skill_id) {
          alert('自分自身を関連スキルに指定することはできません');
          return false;
        }
      }
    }
    
    return true;
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // バリデーション
    if (!validateForm()) {
      return;
    }
    
    try {
      setSubmitting(true);
      setError(null);
      setResults(null);
      
      // APIリクエスト
      const response = await axios.put<UpdateResponse>('/api/skill-masters', formData, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });
      
      // 結果を表示
      setResults(response.data.results);
      
      // エラーがあるかチェック
      const hasErrors = response.data.results.some(result => result.status === 'error');
      
      if (!hasErrors) {
        // エラーがなければフォームをクリア
        setFormData({
          skills: []
        });
        
        // スキルマスタを再取得
        const refreshResponse = await axios.get('/api/skill-masters', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Accept': 'application/json'
          }
        });
        
        setExistingSkills(refreshResponse.data.skills);
      }
      
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const errorData = err.response.data;
        setError(errorData.error?.message || 'スキルマスタの更新に失敗しました');
      } else {
        setError('スキルマスタの更新中にエラーが発生しました');
      }
    } finally {
      setSubmitting(false);
    }
  };
  
  const renderSkillForm = (skill: Skill, index: number) => {
    if (skill.operation === 'delete') {
      // 削除の場合は確認表示のみ
      return (
        <div key={index} className="skill-form-item delete">
          <h3>スキル削除</h3>
          <p>以下のスキルを削除します：</p>
          <p><strong>ID:</strong> {skill.skill_id}</p>
          <p><strong>名前:</strong> {skill.name}</p>
          <button 
            type="button" 
            className="remove-button"
            onClick={() => handleRemoveFromForm(index)}
          >
            フォームから削除
          </button>
        </div>
      );
    }
    
    // 作成・更新の場合はフォームを表示
    return (
      <div key={index} className="skill-form-item">
        <h3>{skill.operation === 'create' ? 'スキル新規作成' : 'スキル更新'}</h3>
        
        {skill.skill_id && (
          <div className="form-group">
            <label>スキルID:</label>
            <input 
              type="text" 
              value={skill.skill_id} 
              readOnly 
              className="readonly"
            />
          </div>
        )}
        
        <div className="form-group">
          <label>カテゴリ:</label>
          <select
            value={skill.category}
            onChange={(e) => handleSkillChange(index, 'category', e.target.value)}
            required
          >
            {categories.map(cat => (
              <option key={cat.category_id} value={cat.name}>
                {cat.description}
              </option>
            ))}
          </select>
        </div>
        
        <div className="form-group">
          <label>スキル名:</label>
          <input 
            type="text" 
            value={skill.name} 
            onChange={(e) => handleSkillChange(index, 'name', e.target.value)}
            maxLength={100}
            required
          />
        </div>
        
        <div className="form-group">
          <label>説明:</label>
          <textarea 
            value={skill.description} 
            onChange={(e) => handleSkillChange(index, 'description', e.target.value)}
            maxLength={500}
            rows={3}
            required
          />
        </div>
        
        <div className="form-group">
          <label>同義語:</label>
          <div className="synonyms-container">
            {skill.synonyms.map((synonym, synonymIndex) => (
              <div key={synonymIndex} className="synonym-item">
                <input 
                  type="text" 
                  value={synonym} 
                  onChange={(e) => handleSynonymChange(index, synonymIndex, e.target.value)}
                  maxLength={50}
                />
                <button 
                  type="button" 
                  className="remove-button"
                  onClick={() => handleRemoveSynonym(index, synonymIndex)}
                >
                  削除
                </button>
              </div>
            ))}
            
            {skill.synonyms.length < 5 && (
              <button 
                type="button" 
                className="add-button"
                onClick={() => handleAddSynonym(index)}
              >
                同義語を追加
              </button>
            )}
          </div>
        </div>
        
        <div className="form-group">
          <label>関連スキル:</label>
          <div className="related-skills-container">
            {skill.related_skills.map((related, relatedIndex) => (
              <div key={relatedIndex} className="related-skill-item">
                <select
                  value={related.skill_id}
                  onChange={(e) => handleRelatedSkillChange(index, relatedIndex, 'skill_id', e.target.value)}
                  required
                >
                  <option value="">選択してください</option>
                  {existingSkills
                    .filter(s => s.skill_id !== skill.skill_id) // 自分自身は除外
                    .map(s => (
                      <option key={s.skill_id} value={s.skill_id}>
                        {s.name} ({s.category})
                      </option>
                    ))
                  }
                </select>
                
                <select
                  value={related.relation_type}
                  onChange={(e) => handleRelatedSkillChange(index, relatedIndex, 'relation_type', e.target.value)}
                  required
                >
                  <option value="parent">親スキル</option>
                  <option value="child">子スキル</option>
                  <option value="related">関連スキル</option>
                </select>
                
                <button 
                  type="button" 
                  className="remove-button"
                  onClick={() => handleRemoveRelatedSkill(index, relatedIndex)}
                >
                  削除
                </button>
              </div>
            ))}
            
            {skill.related_skills.length < 10 && (
              <button 
                type="button" 
                className="add-button"
                onClick={() => handleAddRelatedSkill(index)}
              >
                関連スキルを追加
              </button>
            )}
          </div>
        </div>
        
        <button 
          type="button" 
          className="remove-button"
          onClick={() => handleRemoveFromForm(index)}
        >
          フォームから削除
        </button>
      </div>
    );
  };
  
  const renderResults = () => {
    if (!results) return null;
    
    return (
