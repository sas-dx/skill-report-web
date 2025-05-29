# API仕様書：API-011 プロフィール取得API

## 1. 基本情報

- **API ID**: API-011
- **API名称**: プロフィール取得API
- **概要**: ユーザーのプロフィール情報を取得する
- **エンドポイント**: `/api/profiles/{user_id}`
- **HTTPメソッド**: GET
- **リクエスト形式**: URLパラメータ
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-PROFILE](画面設計書_SCR-PROFILE.md)
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
| user_id | string | ○ | ユーザーID | "me"を指定した場合は認証済みユーザー自身のプロフィール情報を取得<br>他ユーザーのプロフィール情報取得には適切な権限が必要 |

### 2.3 クエリパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| include_skills | boolean | - | スキル情報を含めるか | true: スキル情報を含める, false: 含めない<br>デフォルト: false |
| include_history | boolean | - | 履歴情報を含めるか | true: 履歴情報を含める, false: 含めない<br>デフォルト: false |

### 2.4 リクエスト例

```
GET /api/profiles/U12345?include_skills=true&include_history=false HTTP/1.1
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
| username | string | ユーザー名 | |
| email | string | メールアドレス | |
| display_name | string | 表示名 | |
| first_name | string | 名 | |
| last_name | string | 姓 | |
| first_name_kana | string | 名（カナ） | |
| last_name_kana | string | 姓（カナ） | |
| employee_id | string | 社員番号 | |
| department | object | 部署情報 | |
| position | object | 役職情報 | |
| join_date | string | 入社日 | ISO 8601形式（YYYY-MM-DD） |
| profile_image | string | プロフィール画像URL | |
| contact_info | object | 連絡先情報 | |
| skills | array | スキル情報 | include_skills=trueの場合のみ |
| history | object | 履歴情報 | include_history=trueの場合のみ |
| last_updated | string | 最終更新日時 | ISO 8601形式 |

#### department オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| department_id | string | 部署ID | |
| name | string | 部署名 | |
| code | string | 部署コード | |
| parent_id | string | 親部署ID | |

#### position オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| position_id | string | 役職ID | |
| name | string | 役職名 | |
| level | number | 役職レベル | |
| is_manager | boolean | 管理職フラグ | |

#### contact_info オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| phone | string | 電話番号 | |
| extension | string | 内線番号 | |
| mobile | string | 携帯電話番号 | |
| emergency_contact | string | 緊急連絡先 | |
| address | object | 住所情報 | |

#### address オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| postal_code | string | 郵便番号 | |
| prefecture | string | 都道府県 | |
| city | string | 市区町村 | |
| street_address | string | 番地・建物名 | |

#### skills 配列要素（include_skills=trueの場合のみ）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| name | string | スキル名 | |
| category | string | カテゴリ | |
| level | number | レベル | 1-5の整数値 |
| years_of_experience | number | 経験年数 | |
| last_used_date | string | 最終使用日 | ISO 8601形式（YYYY-MM-DD） |

#### history オブジェクト（include_history=trueの場合のみ）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| department_history | array | 部署履歴 | |
| position_history | array | 役職履歴 | |
| education | array | 学歴 | |
| certifications | array | 資格 | |

### 3.2 正常時レスポンス例（基本情報のみ）

```json
{
  "user_id": "U12345",
  "username": "tanaka.taro",
  "email": "tanaka.taro@example.com",
  "display_name": "田中 太郎",
  "first_name": "太郎",
  "last_name": "田中",
  "first_name_kana": "タロウ",
  "last_name_kana": "タナカ",
  "employee_id": "EMP001234",
  "department": {
    "department_id": "D100",
    "name": "情報システム部",
    "code": "IS",
    "parent_id": "D001"
  },
  "position": {
    "position_id": "P200",
    "name": "主任",
    "level": 3,
    "is_manager": false
  },
  "join_date": "2020-04-01",
  "profile_image": "https://example.com/profiles/U12345/image.jpg",
  "contact_info": {
    "phone": "03-1234-5678",
    "extension": "1234",
    "mobile": "090-1234-5678",
    "emergency_contact": "03-8765-4321",
    "address": {
      "postal_code": "100-0001",
      "prefecture": "東京都",
      "city": "千代田区",
      "street_address": "丸の内1-1-1 サンプルビル10F"
    }
  },
  "last_updated": "2025-05-15T10:30:00+09:00"
}
```

### 3.3 正常時レスポンス例（スキル情報を含む）

```json
{
  "user_id": "U12345",
  "username": "tanaka.taro",
  "email": "tanaka.taro@example.com",
  "display_name": "田中 太郎",
  "first_name": "太郎",
  "last_name": "田中",
  "first_name_kana": "タロウ",
  "last_name_kana": "タナカ",
  "employee_id": "EMP001234",
  "department": {
    "department_id": "D100",
    "name": "情報システム部",
    "code": "IS",
    "parent_id": "D001"
  },
  "position": {
    "position_id": "P200",
    "name": "主任",
    "level": 3,
    "is_manager": false
  },
  "join_date": "2020-04-01",
  "profile_image": "https://example.com/profiles/U12345/image.jpg",
  "contact_info": {
    "phone": "03-1234-5678",
    "extension": "1234",
    "mobile": "090-1234-5678",
    "emergency_contact": "03-8765-4321",
    "address": {
      "postal_code": "100-0001",
      "prefecture": "東京都",
      "city": "千代田区",
      "street_address": "丸の内1-1-1 サンプルビル10F"
    }
  },
  "skills": [
    {
      "skill_id": "SKILL_JAVA",
      "name": "Java",
      "category": "プログラミング言語",
      "level": 4,
      "years_of_experience": 5,
      "last_used_date": "2025-05-01"
    },
    {
      "skill_id": "SKILL_SPRING",
      "name": "Spring Framework",
      "category": "フレームワーク",
      "level": 3,
      "years_of_experience": 3,
      "last_used_date": "2025-05-01"
    },
    {
      "skill_id": "SKILL_SQL",
      "name": "SQL",
      "category": "データベース",
      "level": 4,
      "years_of_experience": 5,
      "last_used_date": "2025-05-01"
    }
  ],
  "last_updated": "2025-05-15T10:30:00+09:00"
}
```

### 3.4 正常時レスポンス例（履歴情報を含む）

```json
{
  "user_id": "U12345",
  "username": "tanaka.taro",
  "email": "tanaka.taro@example.com",
  "display_name": "田中 太郎",
  "first_name": "太郎",
  "last_name": "田中",
  "first_name_kana": "タロウ",
  "last_name_kana": "タナカ",
  "employee_id": "EMP001234",
  "department": {
    "department_id": "D100",
    "name": "情報システム部",
    "code": "IS",
    "parent_id": "D001"
  },
  "position": {
    "position_id": "P200",
    "name": "主任",
    "level": 3,
    "is_manager": false
  },
  "join_date": "2020-04-01",
  "profile_image": "https://example.com/profiles/U12345/image.jpg",
  "contact_info": {
    "phone": "03-1234-5678",
    "extension": "1234",
    "mobile": "090-1234-5678",
    "emergency_contact": "03-8765-4321",
    "address": {
      "postal_code": "100-0001",
      "prefecture": "東京都",
      "city": "千代田区",
      "street_address": "丸の内1-1-1 サンプルビル10F"
    }
  },
  "history": {
    "department_history": [
      {
        "department_id": "D100",
        "name": "情報システム部",
        "start_date": "2022-04-01",
        "end_date": null
      },
      {
        "department_id": "D200",
        "name": "営業部",
        "start_date": "2020-04-01",
        "end_date": "2022-03-31"
      }
    ],
    "position_history": [
      {
        "position_id": "P200",
        "name": "主任",
        "start_date": "2023-04-01",
        "end_date": null
      },
      {
        "position_id": "P100",
        "name": "一般社員",
        "start_date": "2020-04-01",
        "end_date": "2023-03-31"
      }
    ],
    "education": [
      {
        "school_name": "サンプル大学",
        "degree": "学士（情報工学）",
        "field_of_study": "情報工学",
        "start_date": "2016-04-01",
        "end_date": "2020-03-31"
      }
    ],
    "certifications": [
      {
        "name": "応用情報技術者",
        "issuer": "IPA",
        "issue_date": "2021-06-15",
        "expiration_date": null
      },
      {
        "name": "TOEIC 800点",
        "issuer": "ETS",
        "issue_date": "2022-03-20",
        "expiration_date": null
      }
    ]
  },
  "last_updated": "2025-05-15T10:30:00+09:00"
}
```

### 3.5 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他ユーザーのプロフィール閲覧権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.6 エラー時レスポンス例

```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "権限がありません",
    "details": "他のユーザーのプロフィール情報を閲覧する権限がありません。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - 他ユーザーのプロフィール情報取得の場合は権限チェック（PERM_VIEW_PROFILES）
2. リクエストパラメータの検証
   - user_idの形式チェック
   - クエリパラメータの型チェック
3. 対象ユーザーの存在確認
   - 指定されたuser_idのユーザーが存在するか確認
   - "me"の場合は認証済みユーザーのIDに置換
   - 存在しない場合は404エラー
4. プロフィール情報の取得
   - ユーザーの基本情報取得
   - 部署・役職情報の取得
   - 連絡先情報の取得
   - include_skills=trueの場合はスキル情報も取得
   - include_history=trueの場合は履歴情報も取得
5. レスポンスの生成
   - 取得した情報を整形
6. レスポンス返却

### 4.2 プロフィール情報取得ルール

- 自分自身のプロフィールは常に閲覧可能
- 他ユーザーのプロフィール閲覧には権限（PERM_VIEW_PROFILES）が必要
- 管理者は全ユーザーのプロフィールを閲覧可能
- 部門管理者は自部門のユーザーのプロフィールを閲覧可能
- スキル情報・履歴情報は明示的に要求された場合のみ含める
- 個人情報（住所、緊急連絡先など）は権限に応じて制限される場合あり

### 4.3 パフォーマンス要件

- レスポンスタイム：平均200ms以内
- キャッシュ：プロフィール情報は30分間キャッシュ
- 同時リクエスト：最大50リクエスト/秒

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-012](API仕様書_API-012.md) | プロフィール更新API | ユーザープロフィール情報更新 |
| [API-013](API仕様書_API-013.md) | 組織情報取得API | 組織情報一覧取得 |
| [API-021](API仕様書_API-021.md) | スキル情報取得API | ユーザースキル情報取得 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー基本情報 | 参照（R） |
| user_profiles | ユーザープロフィール情報 | 参照（R） |
| departments | 部署情報 | 参照（R） |
| positions | 役職情報 | 参照（R） |
| user_skills | ユーザースキル情報 | 参照（R） |
| department_history | 部署履歴 | 参照（R） |
| position_history | 役職履歴 | 参照（R） |
| education_history | 学歴情報 | 参照（R） |
| certification_history | 資格情報 | 参照（R） |

### 5.3 注意事項・補足

- プロフィール画像URLは有効期限付きの署名付きURLで提供
- 個人情報は適切なアクセス制御のもとで提供
- 部署・役職情報は最新の組織情報に基づいて提供
- スキル情報は概要のみ提供し、詳細はスキル情報取得APIで取得
- 履歴情報は直近5年分のみ提供

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Department {
  department_id: string;
  name: string;
  code: string;
  parent_id: string;
}

interface Position {
  position_id: string;
  name: string;
  level: number;
  is_manager: boolean;
}

interface Address {
  postal_code: string;
  prefecture: string;
  city: string;
  street_address: string;
}

interface ContactInfo {
  phone: string;
  extension: string;
  mobile: string;
  emergency_contact: string;
  address: Address;
}

interface Skill {
  skill_id: string;
  name: string;
  category: string;
  level: number;
  years_of_experience: number;
  last_used_date: string;
}

interface History {
  department_history: Array<{
    department_id: string;
    name: string;
    start_date: string;
    end_date: string | null;
  }>;
  position_history: Array<{
    position_id: string;
    name: string;
    start_date: string;
    end_date: string | null;
  }>;
  education: Array<{
    school_name: string;
    degree: string;
    field_of_study: string;
    start_date: string;
    end_date: string;
  }>;
  certifications: Array<{
    name: string;
    issuer: string;
    issue_date: string;
    expiration_date: string | null;
  }>;
}

interface UserProfile {
  user_id: string;
  username: string;
  email: string;
  display_name: string;
  first_name: string;
  last_name: string;
  first_name_kana: string;
  last_name_kana: string;
  employee_id: string;
  department: Department;
  position: Position;
  join_date: string;
  profile_image: string;
  contact_info: ContactInfo;
  skills?: Skill[];
  history?: History;
  last_updated: string;
}

const UserProfileComponent: React.FC<{ userId: string }> = ({ userId }) => {
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [includeSkills, setIncludeSkills] = useState<boolean>(false);
  const [includeHistory, setIncludeHistory] = useState<boolean>(false);

  useEffect(() => {
    fetchProfile();
  }, [userId, includeSkills, includeHistory]);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // APIリクエストURLの構築
      let url = `/api/profiles/${userId}`;
      const params = new URLSearchParams();
      
      if (includeSkills) {
        params.append('include_skills', 'true');
      }
      
      if (includeHistory) {
        params.append('include_history', 'true');
      }
      
      if (params.toString()) {
        url += `?${params.toString()}`;
      }
      
      // APIリクエスト
      const response = await axios.get<UserProfile>(url, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Accept': 'application/json'
        }
      });
      
      // データの設定
      setProfile(response.data);
      
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const errorData = err.response.data;
        setError(errorData.error?.message || 'プロフィール情報の取得に失敗しました');
      } else {
        setError('プロフィール情報の取得中にエラーが発生しました');
      }
    } finally {
      setLoading(false);
    }
  };

  const toggleSkills = () => {
    setIncludeSkills(!includeSkills);
  };

  const toggleHistory = () => {
    setIncludeHistory(!includeHistory);
  };

  if (loading) {
    return <div className="loading">プロフィール情報を読み込み中...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!profile) {
    return <div className="no-data">プロフィール情報がありません</div>;
  }

  return (
    <div className="user-profile">
      <div className="profile-header">
        <div className="profile-image">
          <img src={profile.profile_image} alt={profile.display_name} />
        </div>
        <div className="profile-info">
          <h2>{profile.display_name}</h2>
          <p className="employee-id">社員番号: {profile.employee_id}</p>
          <p className="department-position">{profile.department.name} / {profile.position.name}</p>
        </div>
      </div>
      
      <div className="profile-actions">
        <button onClick={toggleSkills}>
          {includeSkills ? 'スキル情報を隠す' : 'スキル情報を表示'}
        </button>
        <button onClick={toggleHistory}>
          {includeHistory ? '履歴情報を隠す' : '履歴情報を表示'}
        </button>
      </div>
      
      <div className="profile-section">
        <h3>基本情報</h3>
        <table className="profile-table">
          <tbody>
            <tr>
              <th>氏名</th>
              <td>{profile.last_name} {profile.first_name}</td>
            </tr>
            <tr>
              <th>氏名（カナ）</th>
              <td>{profile.last_name_kana} {profile.first_name_kana}</td>
            </tr>
            <tr>
              <th>メールアドレス</th>
              <td>{profile.email}</td>
            </tr>
            <tr>
              <th>入社日</th>
              <td>{new Date(profile.join_date).toLocaleDateString()}</td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div className="profile-section">
        <h3>連絡先情報</h3>
        <table className="profile-table">
          <tbody>
            <tr>
              <th>電話番号</th>
              <td>{profile.contact_info.phone}</td>
            </tr>
            <tr>
              <th>内線番号</th>
              <td>{profile.contact_info.extension}</td>
            </tr>
            <tr>
              <th>携帯電話</th>
              <td>{profile.contact_info.mobile}</td>
            </tr>
            <tr>
              <th>住所</th>
              <td>
                〒{profile.contact_info.address.postal_code}<br />
                {profile.contact_info.address.prefecture}
                {profile.contact_info.address.city}
                {profile.contact_info.address.street_address}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      {includeSkills && profile.skills && (
        <div className="profile-section">
          <h3>スキル情報</h3>
          <table className="skills-table">
            <thead>
              <tr>
                <th>スキル名</th>
                <th>カテゴリ</th>
                <th>レベル</th>
                <th>経験年数</th>
                <th>最終使用日</th>
              </tr>
            </thead>
            <tbody>
              {profile.skills.map(skill => (
                <tr key={skill.skill_id}>
                  <td>{skill.name}</td>
                  <td>{skill.category}</td>
                  <td>{skill.level}</td>
                  <td>{skill.years_of_experience}年</td>
                  <td>{new Date(skill.last_used_date).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      
      {includeHistory && profile.history && (
        <div className="profile-section">
          <h3>履歴情報</h3>
          
          <h4>部署履歴</h4>
          <table className="history-table">
            <thead>
              <tr>
                <th>部署名</th>
                <th>開始日</th>
                <th>終了日</th>
              </tr>
            </thead>
            <tbody>
              {profile.history.department_history.map((dept, index) => (
                <tr key={index}>
                  <td>{dept.name}</td>
                  <td>{new Date(dept.start_date).toLocaleDateString()}</td>
