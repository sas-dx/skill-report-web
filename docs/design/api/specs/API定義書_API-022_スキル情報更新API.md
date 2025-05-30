# API定義書：API-022 スキル情報更新API

## 1. 基本情報

- **API ID**: API-022
- **API名称**: スキル情報更新API
- **概要**: ユーザーのスキル情報を更新する
- **エンドポイント**: `/api/skills/{user_id}`
- **HTTPメソッド**: PUT
- **リクエスト形式**: JSON
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
| Content-Type | ○ | リクエスト形式 | application/json |
| Accept | - | レスポンス形式 | application/json |

### 2.2 パスパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| user_id | string | ○ | ユーザーID | 自身のIDまたは更新権限のあるユーザーID |

### 2.3 リクエストボディ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| year | number | ○ | 対象年度 | 例: 2025 |
| skills | array | ○ | スキル情報の配列 | |

#### skills 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| skill_id | string | ○ | スキルID | 新規登録時は空文字列 |
| category | string | ○ | スキルカテゴリ | "technical", "business", "language", "soft", "management" |
| name | string | ○ | スキル名 | 最大50文字 |
| level | number | ○ | スキルレベル | 1-5（5が最高） |
| experience_years | number | ○ | 経験年数 | 小数点以下1桁まで（例: 2.5） |
| description | string | - | 詳細説明 | 最大500文字 |
| projects | array | - | 関連プロジェクト | 最大10件 |
| certifications | array | - | 関連資格 | 最大5件 |
| last_used_date | string | ○ | 最終使用日 | ISO 8601形式（YYYY-MM-DD） |
| self_assessment | object | ○ | 自己評価情報 | |

#### projects 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| project_id | string | ○ | プロジェクトID | |
| name | string | - | プロジェクト名 | project_idが指定されている場合は不要 |
| period | string | - | 期間 | "2024/04-2024/09"形式 |
| role | string | - | 役割 | 最大50文字 |

#### certifications 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| certification_id | string | ○ | 資格ID | |
| name | string | - | 資格名 | certification_idが指定されている場合は不要 |
| acquisition_date | string | - | 取得日 | ISO 8601形式（YYYY-MM-DD） |

#### self_assessment オブジェクト

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| strengths | string | ○ | 強み | 最大200文字 |
| weaknesses | string | ○ | 弱み | 最大200文字 |
| improvement_plan | string | ○ | 改善計画 | 最大300文字 |

### 2.4 リクエスト例

```json
{
  "year": 2025,
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
          "period": "2023/04-2023/09",
          "role": "バックエンド開発リーダー"
        },
        {
          "project_id": "P002",
          "period": "2024/01-2024/06",
          "role": "アプリケーションアーキテクト"
        }
      ],
      "certifications": [
        {
          "certification_id": "C001",
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
      "skill_id": "",
      "category": "technical",
      "name": "Docker",
      "level": 3,
      "experience_years": 2.0,
      "description": "コンテナ化、Docker Compose、基本的なオーケストレーション経験あり",
      "projects": [
        {
          "project_id": "P002",
          "period": "2024/01-2024/06",
          "role": "インフラ担当"
        }
      ],
      "certifications": [],
      "last_used_date": "2025-04-30",
      "self_assessment": {
        "strengths": "開発環境の標準化と構築の自動化が得意",
        "weaknesses": "本番環境での運用経験が少ない",
        "improvement_plan": "Kubernetes基礎を学習し、クラスタ管理を理解する"
      }
    }
  ]
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| year | number | 対象年度 | |
| updated_at | string | 更新日時 | ISO 8601形式 |
| skills | array | 更新後のスキル情報の配列 | |

#### skills 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | 新規登録の場合は新たに生成されたID |
| category | string | スキルカテゴリ | |
| name | string | スキル名 | |
| level | number | スキルレベル | |
| experience_years | number | 経験年数 | |
| description | string | 詳細説明 | |
| projects | array | 関連プロジェクト | |
| certifications | array | 関連資格 | |
| last_used_date | string | 最終使用日 | ISO 8601形式（YYYY-MM-DD） |
| self_assessment | object | 自己評価情報 | |

※ projects、certifications、self_assessmentの構造はリクエストと同様

### 3.2 正常時レスポンス例

```json
{
  "user_id": "U12345",
  "year": 2025,
  "updated_at": "2025-05-28T15:30:00+09:00",
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
      "skill_id": "S005",
      "category": "technical",
      "name": "Docker",
      "level": 3,
      "experience_years": 2.0,
      "description": "コンテナ化、Docker Compose、基本的なオーケストレーション経験あり",
      "projects": [
        {
          "project_id": "P002",
          "name": "ECサイトリニューアル",
          "period": "2024/01-2024/06",
          "role": "インフラ担当"
        }
      ],
      "certifications": [],
      "last_used_date": "2025-04-30",
      "self_assessment": {
        "strengths": "開発環境の標準化と構築の自動化が得意",
        "weaknesses": "本番環境での運用経験が少ない",
        "improvement_plan": "Kubernetes基礎を学習し、クラスタ管理を理解する"
      }
    }
  ]
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_SKILL_LEVEL | スキルレベルが不正です | レベルが1-5の範囲外 |
| 400 Bad Request | INVALID_EXPERIENCE_YEARS | 経験年数が不正です | 負数または不正な小数 |
| 400 Bad Request | INVALID_DATE_FORMAT | 日付形式が不正です | 日付形式が不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他ユーザーのスキル情報更新権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 404 Not Found | SKILL_NOT_FOUND | スキルが見つかりません | 更新対象のスキルIDが存在しない |
| 404 Not Found | PROJECT_NOT_FOUND | プロジェクトが見つかりません | 指定されたプロジェクトIDが存在しない |
| 404 Not Found | CERTIFICATION_NOT_FOUND | 資格が見つかりません | 指定された資格IDが存在しない |
| 409 Conflict | DUPLICATE_SKILL | 重複するスキルが存在します | 同一カテゴリ・名称のスキルが既に存在 |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_SKILL_LEVEL",
    "message": "スキルレベルが不正です",
    "details": "スキルレベルは1から5の整数で指定してください。",
    "field": "skills[1].level",
    "value": 6
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - 自身のスキル情報または更新権限（PERM_UPDATE_SKILLS）の確認
2. リクエストパラメータの検証
   - user_idの存在確認
   - yearの形式チェック
   - スキル情報の各項目の形式・値チェック
3. スキル情報の更新
   - skill_idが指定されている場合は更新、空文字列の場合は新規登録
   - 関連プロジェクト・資格情報の関連付け
   - 自己評価情報の更新
4. 履歴情報の保存
   - 更新前のスキル情報を履歴として保存
5. レスポンスの生成
   - 更新後のスキル情報を整形
6. レスポンス返却

### 4.2 スキル情報更新ルール

- 自身のスキル情報は常に更新可能
- 他ユーザーのスキル情報更新には権限（PERM_UPDATE_SKILLS）が必要
- 管理者（ROLE_ADMIN）は全ユーザーのスキル情報を更新可能
- 上長は自部門のメンバーのスキル情報を更新可能（承認プロセス用）
- スキルレベルは1-5の5段階評価（1:初級、2:初中級、3:中級、4:中上級、5:上級）
- 経験年数は0.5年単位で記録（0.5刻み）
- 同一カテゴリ内で同名のスキルは登録不可
- スキル情報の更新時は、更新前の情報を履歴として保存
- 新規スキル登録時はスキルマスタに存在するスキルを優先的に使用
- プロジェクト・資格情報は既存のマスタデータから選択

### 4.3 バリデーションルール

- スキル名：必須、1-50文字
- スキルレベル：必須、1-5の整数
- 経験年数：必須、0以上、小数点以下1桁（0.5刻み）
- 詳細説明：任意、0-500文字
- 最終使用日：必須、有効な日付形式（YYYY-MM-DD）、未来日不可
- 自己評価（強み）：必須、1-200文字
- 自己評価（弱み）：必須、1-200文字
- 自己評価（改善計画）：必須、1-300文字
- プロジェクト：任意、最大10件
- 資格：任意、最大5件

### 4.4 トランザクション管理

- スキル情報の更新は単一トランザクションで処理
- 関連テーブル（プロジェクト関連、資格関連）も同一トランザクションで更新
- エラー発生時は全ての更新をロールバック

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-021](API仕様書_API-021.md) | スキル情報取得API | ユーザースキル情報取得 |
| [API-023](API仕様書_API-023.md) | スキルマスタ取得API | スキルマスタ情報取得 |
| [API-025](API仕様書_API-025.md) | スキル検索API | 条件指定によるスキル検索 |
| [API-026](API仕様書_API-026.md) | スキルマップ生成API | スキルマップデータ生成 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| user_skills | ユーザースキル情報 | 作成（C）、更新（U）、削除（D） |
| skill_masters | スキルマスタ | 参照（R） |
| skill_categories | スキルカテゴリ | 参照（R） |
| user_skill_history | スキル履歴 | 作成（C） |
| projects | プロジェクト情報 | 参照（R） |
| user_projects | ユーザープロジェクト関連 | 作成（C）、更新（U）、削除（D） |
| certifications | 資格情報 | 参照（R） |
| user_certifications | ユーザー資格関連 | 作成（C）、更新（U）、削除（D） |

### 5.3 注意事項・補足

- スキル情報は年度ごとに管理され、前年度からコピーして作成される
- スキルカテゴリは「technical（技術）」「business（業務知識）」「language（言語）」「soft（ソフトスキル）」「management（マネジメント）」の5種類
- スキルレベルの定義は以下の通り
  - レベル1：基本的な知識を有し、指導のもとで作業可能
  - レベル2：基本的なタスクを独力で実行可能
  - レベル3：一般的なタスクを独力で実行可能、他者への基本的な指導可能
  - レベル4：複雑なタスクを実行可能、他者への指導可能
  - レベル5：専門家レベル、高度な問題解決と他者への指導が可能
- 関連プロジェクトは最大10件まで登録可能
- 関連資格は最大5件まで登録可能
- スキル情報の更新は履歴として保存され、過去5年分の履歴を参照可能
- スキル情報の一括更新（複数スキルの同時更新）が可能
- 既存スキルの削除は、リクエストから該当スキルを除外することで実現（明示的な削除APIは提供しない）

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

interface Certification {
  certification_id: string;
  name?: string;
  acquisition_date?: string;
}

interface Project {
  project_id: string;
  name?: string;
  period?: string;
  role?: string;
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

interface SkillFormData {
  year: number;
  skills: Skill[];
}

const SkillEditForm: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState<boolean>(true);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<SkillFormData>({
    year: new Date().getFullYear(),
    skills: []
  });
  
  // マスタデータ
  const [skillMasters, setSkillMasters] = useState<any[]>([]);
  const [projectMasters, setProjectMasters] = useState<any[]>([]);
  const [certificationMasters, setCertificationMasters] = useState<any[]>([]);
  
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // 現在のスキル情報を取得
        const skillResponse = await axios.get(`/api/skills/${userId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Accept': 'application/json'
          }
        });
        
        // マスタデータを取得
        const [skillMastersResponse, projectsResponse, certificationsResponse] = await Promise.all([
          axios.get('/api/skill-masters', {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
          }),
          axios.get('/api/system/masters/projects', {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
          }),
          axios.get('/api/system/masters/certifications', {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
          })
        ]);
        
        // データをセット
        setFormData({
          year: skillResponse.data.year,
          skills: skillResponse.data.skills
        });
        
        setSkillMasters(skillMastersResponse.data.skills);
        setProjectMasters(projectsResponse.data.items);
        setCertificationMasters(certificationsResponse.data.items);
        
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
    
    fetchInitialData();
  }, [userId]);
  
  const handleSkillChange = (index: number, field: keyof Skill, value: any) => {
    const updatedSkills = [...formData.skills];
    updatedSkills[index] = {
      ...updatedSkills[index],
      [field]: value
    };
    setFormData({
      ...formData,
      skills: updatedSkills
    });
  };
  
  const handleSelfAssessmentChange = (index: number, field: keyof SelfAssessment, value: string) => {
    const updatedSkills = [...formData.skills];
    updatedSkills[index] = {
      ...updatedSkills[index],
      self_assessment: {
        ...updatedSkills[index].self_assessment,
        [field]: value
      }
    };
    setFormData({
      ...formData,
      skills: updatedSkills
    });
  };
  
  const handleAddProject = (skillIndex: number) => {
    const updatedSkills = [...formData.skills];
    const currentProjects = updatedSkills[skillIndex].projects || [];
    
    if (currentProjects.length >= 10) {
      alert('プロジェクトは最大10件まで登録できます');
      return;
    }
    
    updatedSkills[skillIndex].projects = [
      ...currentProjects,
      { project_id: '', period: '', role: '' }
    ];
    
    setFormData({
      ...formData,
      skills: updatedSkills
    });
  };
  
  const handleRemoveProject = (skillIndex: number, projectIndex: number) => {
    const updatedSkills = [...formData.skills];
    updatedSkills[skillIndex].projects.splice(projectIndex, 1);
    setFormData({
      ...formData,
      skills: updatedSkills
    });
  };
  
  const handleProjectChange = (skillIndex: number, projectIndex: number, field: keyof Project, value: string) => {
    const updatedSkills = [...formData.skills];
    updatedSkills[skillIndex].projects[projectIndex] = {
      ...updatedSkills[skillIndex].projects[projectIndex],
      [field]: value
    };
    
    // プロジェクトIDが変更された場合、マスタから名前を自動設定
    if (field === 'project_id' && value) {
      const selectedProject = projectMasters.find(p => p.project_id === value);
      if (selectedProject) {
        updatedSkills[skillIndex].projects[projectIndex].name = selectedProject.name;
      }
    }
    
    setFormData({
      ...formData,
      skills: updatedSkills
    });
  };
  
  const handleAddCertification = (skillIndex: number) => {
    const updatedSkills = [...formData.skills];
    const currentCertifications = updatedSkills[skillIndex].certifications || [];
    
    if (currentCertifications.length >= 5) {
      alert('資格は最大5件まで登録できます');
      return;
    }
    
    updatedSkills[skillIndex].certifications = [
      ...currentCertifications,
      { certification_id: '', acquisition_date: '' }
    ];
    
    setFormData({
      ...formData,
      skills: updatedSkills
    });
  };
  
  const handleRemoveCertification = (skillIndex: number, certIndex: number) => {
    const updatedSkills = [...formData.skills];
    updatedSkills[skillIndex].certifications.splice(certIndex, 1);
    setFormData({
      ...formData,
      skills: updatedSkills
    });
  };
  
  const handleCertificationChange = (skillIndex: number, certIndex: number, field: keyof Certification, value: string) => {
    const updatedSkills = [...formData.skills];
    updatedSkills[skillIndex].certifications[certIndex] = {
      ...updatedSkills[skillIndex].certifications[certIndex],
      [field]: value
    };
    
    // 資格IDが変更された場合、マスタから名前を自動設定
    if (field === 'certification_id' && value) {
      const selectedCert = certificationMasters.find(c => c.certification_id === value);
      if (selectedCert) {
        updatedSkills[skillIndex].certifications[certIndex].name = selectedCert.name;
      }
    }
    
    setFormData({
      ...formData,
      skills: updatedSkills
    });
  };
  
  const handleAddSkill = () => {
    setFormData({
      ...formData,
      skills: [
        ...formData.skills,
        {
          skill_id: '',
          category: 'technical',
          name: '',
          level: 1,
          experience_years: 0,
          description: '',
          projects: [],
          certifications: [],
          last_used_date: new Date().toISOString().split('T')[0],
          self_assessment: {
            strengths: '',
            weaknesses: '',
            improvement_plan: ''
          }
        }
      ]
    });
  };
  
  const handleRemoveSkill = (index: number) => {
    const updatedSkills = [...formData.skills];
    updatedSkills.splice(index, 1);
    setFormData({
      ...formData,
      skills: updatedSkills
    });
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      setSubmitting(true);
      setError(null);
      
      // APIリクエスト
      const response = await axios.put(`/api/skills/${userId}`, formData, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });
      
      // 成功時の処理
      alert('スキル情報を更新しました');
      navigate(`/skills/${
