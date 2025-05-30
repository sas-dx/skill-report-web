# API定義書：API-012 プロフィール更新API

## 1. 基本情報

- **API ID**: API-012
- **API名称**: プロフィール更新API
- **概要**: ユーザーのプロフィール情報を更新する
- **エンドポイント**: `/api/profiles/{user_id}`
- **HTTPメソッド**: PUT
- **リクエスト形式**: JSON
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-PROFILE-EDIT](画面設計書_SCR-PROFILE-EDIT.md)
- **作成日**: 2025/05/28
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/28 初版作成

---

## 2. リクエスト仕様

### 2.1 リクエストヘッダ

| ヘッダ名 | 必須 | 説明 | 備考 |
|---------|------|------|------|
| Authorization | ○ | 認証トークン | Bearer {JWT} 形式 |
| Content-Type | ○ | コンテンツタイプ | application/json |
| Accept | - | レスポンス形式 | application/json |

### 2.2 パスパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| user_id | string | ○ | ユーザーID | "me"を指定した場合は認証済みユーザー自身のプロフィール情報を更新<br>他ユーザーのプロフィール情報更新には管理者権限が必要 |

### 2.3 リクエストボディ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| display_name | string | - | 表示名 | 1-50文字 |
| first_name | string | - | 名 | 1-30文字 |
| last_name | string | - | 姓 | 1-30文字 |
| first_name_kana | string | - | 名（カナ） | 1-30文字、カタカナのみ |
| last_name_kana | string | - | 姓（カナ） | 1-30文字、カタカナのみ |
| contact_info | object | - | 連絡先情報 | |
| profile_image | string | - | プロフィール画像（Base64） | 最大5MB、JPEG/PNG形式 |
| skills | array | - | スキル情報 | 管理者のみ更新可能 |

#### contact_info オブジェクト

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| phone | string | - | 電話番号 | 数字、ハイフン可 |
| extension | string | - | 内線番号 | 数字のみ |
| mobile | string | - | 携帯電話番号 | 数字、ハイフン可 |
| emergency_contact | string | - | 緊急連絡先 | 数字、ハイフン可 |
| address | object | - | 住所情報 | |

#### address オブジェクト

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| postal_code | string | - | 郵便番号 | 数字、ハイフン可 |
| prefecture | string | - | 都道府県 | 1-10文字 |
| city | string | - | 市区町村 | 1-30文字 |
| street_address | string | - | 番地・建物名 | 1-100文字 |

#### skills 配列要素（管理者のみ更新可能）

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| skill_id | string | ○ | スキルID | 既存のスキルID |
| level | number | ○ | レベル | 1-5の整数値 |
| years_of_experience | number | ○ | 経験年数 | 0.5単位の数値 |
| last_used_date | string | ○ | 最終使用日 | ISO 8601形式（YYYY-MM-DD） |

### 2.4 リクエスト例（基本情報更新）

```json
{
  "display_name": "田中 太郎",
  "first_name": "太郎",
  "last_name": "田中",
  "first_name_kana": "タロウ",
  "last_name_kana": "タナカ",
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
  }
}
```

### 2.5 リクエスト例（スキル情報更新、管理者のみ）

```json
{
  "skills": [
    {
      "skill_id": "SKILL_JAVA",
      "level": 4,
      "years_of_experience": 5,
      "last_used_date": "2025-05-01"
    },
    {
      "skill_id": "SKILL_SPRING",
      "level": 3,
      "years_of_experience": 3,
      "last_used_date": "2025-05-01"
    },
    {
      "skill_id": "SKILL_SQL",
      "level": 4,
      "years_of_experience": 5,
      "last_used_date": "2025-05-01"
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
| skills | array | スキル情報 | 管理者が更新した場合のみ |
| updated_by | string | 更新者 | 更新を行ったユーザーのID |
| updated_at | string | 更新日時 | ISO 8601形式 |
| change_summary | object | 変更内容サマリー | 更新された項目の概要 |

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

#### skills 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| name | string | スキル名 | |
| category | string | カテゴリ | |
| level | number | レベル | 1-5の整数値 |
| years_of_experience | number | 経験年数 | |
| last_used_date | string | 最終使用日 | ISO 8601形式（YYYY-MM-DD） |

#### change_summary オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| updated_fields | array | 更新された項目 | 項目名のリスト |
| profile_image_changed | boolean | 画像変更有無 | プロフィール画像が変更された場合true |
| skills_changed | boolean | スキル変更有無 | スキル情報が変更された場合true |

### 3.2 正常時レスポンス例

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
  "profile_image": "https://example.com/profiles/U12345/image.jpg?v=20250528154500",
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
  "updated_by": "U00001",
  "updated_at": "2025-05-28T15:45:00+09:00",
  "change_summary": {
    "updated_fields": [
      "display_name",
      "first_name",
      "last_name",
      "first_name_kana",
      "last_name_kana",
      "contact_info"
    ],
    "profile_image_changed": false,
    "skills_changed": false
  }
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_IMAGE | 画像形式が不正です | 不正な画像形式/サイズ |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他ユーザーのプロフィール更新権限なし |
| 403 Forbidden | SKILL_UPDATE_DENIED | スキル更新権限がありません | スキル更新権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 404 Not Found | SKILL_NOT_FOUND | スキルが見つかりません | 指定されたスキルIDが存在しない |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "パラメータが不正です",
    "details": "first_name_kana は全角カタカナで入力してください。",
    "invalid_fields": [
      {
        "field": "first_name_kana",
        "reason": "全角カタカナで入力してください"
      }
    ]
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - 他ユーザーのプロフィール情報更新の場合は権限チェック（PERM_MANAGE_PROFILES）
   - スキル情報更新の場合は権限チェック（PERM_MANAGE_SKILLS）
2. リクエストパラメータの検証
   - user_idの形式チェック
   - "me"の場合は認証済みユーザーのIDに置換
   - リクエストボディの各項目の形式チェック
3. 対象ユーザーの存在確認
   - 指定されたuser_idのユーザーが存在するか確認
   - 存在しない場合は404エラー
4. プロフィール画像の処理（画像更新時）
   - Base64デコード
   - 画像形式・サイズの検証
   - リサイズ・最適化処理
   - ストレージへの保存
5. スキル情報の検証（スキル更新時）
   - スキルIDの存在確認
   - レベル・経験年数の範囲チェック
6. プロフィール情報の更新
   - 変更項目の特定
   - データベース更新
   - 変更履歴の記録
7. レスポンスの生成
   - 更新後のプロフィール情報を取得・整形
   - 変更サマリーの生成
8. レスポンス返却

### 4.2 プロフィール更新ルール

- 自分自身のプロフィールは基本情報・連絡先情報のみ更新可能
- 他ユーザーのプロフィール更新には管理者権限（PERM_MANAGE_PROFILES）が必要
- スキル情報の更新には特別な権限（PERM_MANAGE_SKILLS）が必要
- 部署・役職情報は人事システム連携により自動更新されるため、このAPIでは更新不可
- プロフィール画像は最適化処理（リサイズ、圧縮）が行われる
- 更新されなかった項目は現在の値が維持される
- 全ての更新は監査ログに記録される

### 4.3 入力値検証ルール

- 氏名（漢字）：1-30文字
- 氏名（カナ）：1-30文字、全角カタカナのみ
- 表示名：1-50文字
- 電話番号：数字、ハイフン可、10-15文字
- 内線番号：数字のみ、1-10文字
- 携帯電話番号：数字、ハイフン可、10-15文字
- 郵便番号：数字、ハイフン可、7-8文字
- 都道府県：1-10文字
- 市区町村：1-30文字
- 番地・建物名：1-100文字
- プロフィール画像：最大5MB、JPEG/PNG形式
- スキルレベル：1-5の整数値
- 経験年数：0.5単位の数値、最大50年
- 最終使用日：ISO 8601形式（YYYY-MM-DD）、過去日付

### 4.4 パフォーマンス要件

- レスポンスタイム：平均500ms以内（画像処理を除く）
- 画像処理時間：平均2秒以内
- トランザクション：プロフィール更新は単一トランザクションで処理
- 同時リクエスト：最大20リクエスト/秒

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-011](API仕様書_API-011.md) | プロフィール取得API | ユーザープロフィール情報取得 |
| [API-013](API仕様書_API-013.md) | 組織情報取得API | 組織情報一覧取得 |
| [API-021](API仕様書_API-021.md) | スキル情報取得API | ユーザースキル情報取得 |
| [API-022](API仕様書_API-022.md) | スキル更新API | ユーザースキル情報更新 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー基本情報 | 参照/更新（R/U） |
| user_profiles | ユーザープロフィール情報 | 参照/更新（R/U） |
| departments | 部署情報 | 参照（R） |
| positions | 役職情報 | 参照（R） |
| user_skills | ユーザースキル情報 | 参照/更新（R/U） |
| skills | スキルマスタ | 参照（R） |
| profile_change_logs | プロフィール変更履歴 | 作成（C） |

### 5.3 注意事項・補足

- プロフィール画像はストレージに保存され、URLは有効期限付きの署名付きURLで提供
- 画像のキャッシュ制御のため、URLにはバージョン情報（タイムスタンプ）が付与される
- 個人情報は適切なアクセス制御・暗号化のもとで保存
- スキル情報の一括更新は専用のスキル更新API（API-022）を使用することを推奨
- 部署・役職情報の更新は人事システム連携APIを使用

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface ProfileUpdateRequest {
  display_name?: string;
  first_name?: string;
  last_name?: string;
  first_name_kana?: string;
  last_name_kana?: string;
  contact_info?: {
    phone?: string;
    extension?: string;
    mobile?: string;
    emergency_contact?: string;
    address?: {
      postal_code?: string;
      prefecture?: string;
      city?: string;
      street_address?: string;
    };
  };
  profile_image?: string;
}

interface ProfileUpdateResponse {
  user_id: string;
  username: string;
  email: string;
  display_name: string;
  first_name: string;
  last_name: string;
  first_name_kana: string;
  last_name_kana: string;
  employee_id: string;
  department: {
    department_id: string;
    name: string;
    code: string;
    parent_id: string;
  };
  position: {
    position_id: string;
    name: string;
    level: number;
    is_manager: boolean;
  };
  join_date: string;
  profile_image: string;
  contact_info: {
    phone: string;
    extension: string;
    mobile: string;
    emergency_contact: string;
    address: {
      postal_code: string;
      prefecture: string;
      city: string;
      street_address: string;
    };
  };
  updated_by: string;
  updated_at: string;
  change_summary: {
    updated_fields: string[];
    profile_image_changed: boolean;
    skills_changed: boolean;
  };
}

const ProfileUpdateForm: React.FC<{ userId: string; onSuccess: (data: ProfileUpdateResponse) => void }> = ({ userId, onSuccess }) => {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  
  // フォームの状態
  const [formData, setFormData] = useState<ProfileUpdateRequest>({
    display_name: '',
    first_name: '',
    last_name: '',
    first_name_kana: '',
    last_name_kana: '',
    contact_info: {
      phone: '',
      extension: '',
      mobile: '',
      emergency_contact: '',
      address: {
        postal_code: '',
        prefecture: '',
        city: '',
        street_address: ''
      }
    }
  });
  
  // プロフィール画像
  const [profileImage, setProfileImage] = useState<string | null>(null);
  
  // 初期データの取得
  useEffect(() => {
    fetchCurrentProfile();
  }, [userId]);
  
  const fetchCurrentProfile = async () => {
    try {
      setLoading(true);
      
      const response = await axios.get(`/api/profiles/${userId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Accept': 'application/json'
        }
      });
      
      const profileData = response.data;
      
      // フォームデータの初期化
      setFormData({
        display_name: profileData.display_name,
        first_name: profileData.first_name,
        last_name: profileData.last_name,
        first_name_kana: profileData.first_name_kana,
        last_name_kana: profileData.last_name_kana,
        contact_info: {
          phone: profileData.contact_info.phone,
          extension: profileData.contact_info.extension,
          mobile: profileData.contact_info.mobile,
          emergency_contact: profileData.contact_info.emergency_contact,
          address: {
            postal_code: profileData.contact_info.address.postal_code,
            prefecture: profileData.contact_info.address.prefecture,
            city: profileData.contact_info.address.city,
            street_address: profileData.contact_info.address.street_address
          }
        }
      });
      
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
  
  // 入力値の変更ハンドラ
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    
    // ネストされたフィールドの処理
    if (name.includes('.')) {
      const [parent, child] = name.split('.');
      
      if (parent === 'contact_info') {
        setFormData({
          ...formData,
          contact_info: {
            ...formData.contact_info,
            [child]: value
          }
        });
      } else if (parent === 'address') {
        setFormData({
          ...formData,
          contact_info: {
            ...formData.contact_info,
            address: {
              ...formData.contact_info?.address,
              [child]: value
            }
          }
        });
      }
    } else {
      // トップレベルのフィールド
      setFormData({
        ...formData,
        [name]: value
      });
    }
    
    // エラーをクリア
    if (fieldErrors[name]) {
      const newErrors = { ...fieldErrors };
      delete newErrors[name];
      setFieldErrors(newErrors);
    }
  };
  
  // 画像アップロードハンドラ
  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    
    if (!file) return;
    
    // ファイルサイズチェック
    if (file.size > 5 * 1024 * 1024) {
      setFieldErrors({
        ...fieldErrors,
        profile_image: '画像サイズは5MB以下にしてください'
      });
      return;
    }
    
    // ファイル形式チェック
    if (!['image/jpeg', 'image/png'].includes(file.type)) {
      setFieldErrors({
        ...fieldErrors,
        profile_image: 'JPEG/PNG形式の画像を選択してください'
      });
      return;
    }
    
    // FileReaderでBase64エンコード
    const reader = new FileReader();
    reader.onload = () => {
      const base64String = reader.result as string;
      setProfileImage(base64String);
    };
    reader.readAsDataURL(file);
    
    // エラーをクリア
    if (fieldErrors.profile_image) {
      const newErrors = { ...fieldErrors };
      delete newErrors.profile_image;
      setFieldErrors(newErrors);
    }
  };
  
  // フォーム送信ハンドラ
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setError(null);
      setFieldErrors({});
      
      // リクエストデータの準備
      const requestData: ProfileUpdateRequest = { ...formData };
      
      // 画像がある場合は追加
      if (profileImage) {
        requestData.profile_image = profileImage;
      }
      
      // APIリクエスト
      const response = await axios.put<ProfileUpdateResponse>(
        `/api/profiles/${userId}`,
        requestData,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
        }
      );
      
      // 成功時の処理
      onSuccess(response.data);
      
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const errorData = err.response.data;
        
        // フィールドエラーの処理
        if (errorData.error?.invalid_fields) {
          const newFieldErrors: Record<string, string> = {};
          errorData.error.invalid_fields.forEach((field: { field: string; reason: string }) => {
            newFieldErrors[field.field] = field.reason;
          });
          setFieldErrors(newFieldErrors);
        }
        
        setError(errorData.error?.message || 'プロフィール更新に失敗しました');
      } else {
        setError('プロフィール更新中にエラーが発生しました');
      }
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="profile-update-form">
      <h2>プロフィール情報更新</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit}>
