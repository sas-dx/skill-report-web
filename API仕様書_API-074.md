# API仕様書：API-074 マスタデータ更新API

## 1. 基本情報

- **API ID**: API-074
- **API名称**: マスタデータ更新API
- **概要**: システムで使用するマスタデータを更新する
- **エンドポイント**: `/api/system/masters/{master_type}`
- **HTTPメソッド**: PUT
- **リクエスト形式**: URL Path Parameter + JSON
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **権限要件**: 管理者権限
- **利用画面**: [SCR-ADMIN](画面設計書_SCR-ADMIN.md)
- **作成日**: 2025/05/29
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/29 初版作成

---

## 2. リクエスト仕様

### 2.1 パスパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| master_type | string | ○ | マスタデータ種別 | 指定可能な値:<br>"departments", "positions", "skills", "skill_categories", "work_categories", "training_categories", "project_types", "employment_types", "notification_types", "languages", "countries", "prefectures" |

### 2.2 リクエストヘッダ

| ヘッダ名 | 説明 | 必須 | 備考 |
|---------|------|------|------|
| Authorization | 認証トークン | ○ | Bearer {JWT} |
| Content-Type | コンテンツタイプ | ○ | application/json |

### 2.3 リクエストボディ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| items | array | ○ | 更新するマスタデータ項目の配列 | 詳細は以下参照 |
| operation | string | - | 操作種別 | "update"（更新）, "create"（新規作成）, "delete"（削除）のいずれか<br>デフォルト："update" |
| comment | string | - | 更新コメント | 変更履歴に記録される |

#### items 配列要素（共通項目）

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| id | string | ○ | ID | 更新時は必須<br>新規作成時は省略可（自動生成） |
| name | string | ○ | 名称 | 1〜100文字 |
| code | string | ○ | コード | 半角英数字、1〜50文字<br>マスタデータ種別内で一意 |
| description | string | - | 説明 | 0〜500文字 |
| sort_order | number | - | 表示順 | 1以上の整数<br>指定なしの場合は自動採番 |
| is_active | boolean | - | 有効フラグ | デフォルト：true |

#### マスタデータ種別ごとの追加項目

##### departments（部署）

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| parent_id | string | - | 親部署ID | 既存の部署ID |
| manager_id | string | - | 部署管理者ID | 既存のユーザーID |

##### positions（役職）

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| level | number | ○ | 役職レベル | 1以上の整数 |
| is_manager | boolean | - | 管理職フラグ | デフォルト：false |

##### skills（スキル）

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| category_id | string | ○ | スキルカテゴリID | 既存のスキルカテゴリID |
| level_criteria | object | - | レベル基準 | 詳細は以下参照 |
| related_skills | array | - | 関連スキルID | 既存のスキルIDの配列 |

##### level_criteria オブジェクト

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| level1 | string | - | レベル1基準 | 0〜200文字 |
| level2 | string | - | レベル2基準 | 0〜200文字 |
| level3 | string | - | レベル3基準 | 0〜200文字 |
| level4 | string | - | レベル4基準 | 0〜200文字 |

##### skill_categories（スキルカテゴリ）

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| parent_id | string | - | 親カテゴリID | 既存のスキルカテゴリID |
| color | string | - | 表示色 | カラーコード（#RRGGBB） |

### 2.4 リクエスト例（スキル更新）

```json
{
  "operation": "update",
  "items": [
    {
      "id": "java",
      "name": "Java",
      "code": "SKILL_JAVA",
      "description": "Javaプログラミング言語に関するスキル（Java 17対応）",
      "sort_order": 10,
      "is_active": true,
      "category_id": "programming_languages",
      "level_criteria": {
        "level1": "基本的な文法を理解し、簡単なプログラムを作成できる",
        "level2": "オブジェクト指向の概念を理解し、実務で基本的な開発ができる",
        "level3": "フレームワークを活用した複雑なアプリケーション開発ができる",
        "level4": "アーキテクチャ設計や最適化、チューニングができる"
      },
      "related_skills": ["spring", "junit", "maven", "gradle"]
    }
  ],
  "comment": "Java 17対応の説明を追加"
}
```

### 2.5 リクエスト例（部署新規作成）

```json
{
  "operation": "create",
  "items": [
    {
      "name": "データサイエンス課",
      "code": "DEV_DS",
      "description": "データ分析・機械学習を担当する課",
      "sort_order": 30,
      "is_active": true,
      "parent_id": "dept_dev"
    }
  ],
  "comment": "データサイエンス課の新設"
}
```

### 2.6 リクエスト例（スキル削除）

```json
{
  "operation": "delete",
  "items": [
    {
      "id": "obsolete_skill"
    }
  ],
  "comment": "廃止されたスキルの削除"
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| success | boolean | 処理結果 | true: 成功 |
| master_type | string | マスタデータ種別 | |
| operation | string | 操作種別 | "update", "create", "delete"のいずれか |
| affected_count | number | 影響を受けたレコード数 | |
| items | array | 更新されたマスタデータ項目 | 詳細は以下参照 |
| updated_at | string | 更新日時 | ISO 8601形式 |
| updated_by | string | 更新者 | ユーザーID |
| message | string | 処理結果メッセージ | |

#### items 配列要素

更新後のマスタデータ項目。フォーマットは[API-073 マスタデータ取得API](API仕様書_API-073.md)のレスポンス仕様と同様。

### 3.2 正常時レスポンス例（スキル更新）

```json
{
  "success": true,
  "master_type": "skills",
  "operation": "update",
  "affected_count": 1,
  "items": [
    {
      "id": "java",
      "name": "Java",
      "code": "SKILL_JAVA",
      "description": "Javaプログラミング言語に関するスキル（Java 17対応）",
      "sort_order": 10,
      "is_active": true,
      "category_id": "programming_languages",
      "level_criteria": {
        "level1": "基本的な文法を理解し、簡単なプログラムを作成できる",
        "level2": "オブジェクト指向の概念を理解し、実務で基本的な開発ができる",
        "level3": "フレームワークを活用した複雑なアプリケーション開発ができる",
        "level4": "アーキテクチャ設計や最適化、チューニングができる"
      },
      "related_skills": ["spring", "junit", "maven", "gradle"],
      "created_at": "2025-01-15T10:00:00+09:00",
      "updated_at": "2025-05-29T10:15:30+09:00"
    }
  ],
  "updated_at": "2025-05-29T10:15:30+09:00",
  "updated_by": "admin.user",
  "message": "スキルデータが正常に更新されました。"
}
```

### 3.3 正常時レスポンス例（部署新規作成）

```json
{
  "success": true,
  "master_type": "departments",
  "operation": "create",
  "affected_count": 1,
  "items": [
    {
      "id": "dept_dev_ds",
      "name": "データサイエンス課",
      "code": "DEV_DS",
      "description": "データ分析・機械学習を担当する課",
      "sort_order": 30,
      "is_active": true,
      "parent_id": "dept_dev",
      "manager_id": null,
      "level": 2,
      "has_children": false,
      "created_at": "2025-05-29T10:15:30+09:00",
      "updated_at": "2025-05-29T10:15:30+09:00"
    }
  ],
  "updated_at": "2025-05-29T10:15:30+09:00",
  "updated_by": "admin.user",
  "message": "部署データが正常に作成されました。"
}
```

### 3.4 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 400 Bad Request | VALIDATION_ERROR | 検証エラーが発生しました | マスタデータ項目の検証エラー |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | マスタデータ更新権限なし |
| 404 Not Found | MASTER_TYPE_NOT_FOUND | 指定されたマスタデータ種別が見つかりません | 存在しないmaster_type |
| 404 Not Found | ITEM_NOT_FOUND | 指定された項目が見つかりません | 更新/削除対象のIDが存在しない |
| 409 Conflict | DUPLICATE_CODE | コードが重複しています | 既に同じコードが存在する |
| 409 Conflict | CONCURRENT_UPDATE | 他のユーザーによる更新が競合しています | 同時更新の競合 |
| 409 Conflict | REFERENCE_CONSTRAINT | 参照制約違反です | 削除対象が他で参照されている |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.5 エラー時レスポンス例

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "検証エラーが発生しました",
    "details": [
      {
        "field": "items[0].name",
        "message": "名称は必須項目です。"
      },
      {
        "field": "items[0].category_id",
        "message": "指定されたスキルカテゴリIDは存在しません。"
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
   - マスタデータ更新権限の確認
2. リクエストパラメータの検証
   - master_typeの値チェック
   - 必須パラメータの存在確認
   - 各項目の形式チェック
3. マスタデータ項目の検証
   - 更新/削除対象の存在確認
   - コードの一意性チェック
   - 参照整合性チェック
4. 排他制御
   - 同時更新の競合チェック
5. マスタデータの更新
   - 操作種別に応じた処理（更新/作成/削除）
   - 更新履歴の記録
6. レスポンスの生成
   - 更新結果を整形してJSONレスポンスを生成
7. レスポンス返却

### 4.2 アクセス制御ルール

- マスタデータの更新は管理者権限を持つユーザーのみ可能
- マスタデータ種別ごとに更新権限を細分化可能
  - departments: 組織管理者のみ更新可能
  - positions: 人事管理者のみ更新可能
  - skills: スキル管理者のみ更新可能
  - skill_categories: スキル管理者のみ更新可能
  - work_categories: 作業管理者のみ更新可能
  - training_categories: 研修管理者のみ更新可能
  - project_types: プロジェクト管理者のみ更新可能
  - employment_types: 人事管理者のみ更新可能
  - notification_types: システム管理者のみ更新可能
  - languages: システム管理者のみ更新可能
  - countries: システム管理者のみ更新可能
  - prefectures: システム管理者のみ更新可能
- 監査ログにはマスタデータの更新記録が残る

### 4.3 パフォーマンス要件

- 応答時間：平均300ms以内
- タイムアウト：5秒
- 同時リクエスト：最大5リクエスト/秒
- 更新後のキャッシュクリア：更新されたマスタデータ種別のキャッシュを即時クリア

### 4.4 マスタデータ更新ルール

| マスタデータ種別 | 作成 | 更新 | 削除 | 特記事項 |
|---------------|------|------|------|---------|
| departments | ○ | ○ | △ | 削除は子部署がない場合のみ可能<br>所属ユーザーがいる場合は論理削除のみ |
| positions | ○ | ○ | △ | 削除は該当役職のユーザーがいない場合のみ可能 |
| skills | ○ | ○ | △ | 削除は評価実績がない場合のみ可能<br>評価実績がある場合は論理削除のみ |
| skill_categories | ○ | ○ | △ | 削除は子カテゴリやスキルがない場合のみ可能 |
| work_categories | ○ | ○ | △ | 削除は作業実績がない場合のみ可能<br>作業実績がある場合は論理削除のみ |
| training_categories | ○ | ○ | △ | 削除は研修実績がない場合のみ可能<br>研修実績がある場合は論理削除のみ |
| project_types | ○ | ○ | △ | 削除はプロジェクト実績がない場合のみ可能<br>プロジェクト実績がある場合は論理削除のみ |
| employment_types | ○ | ○ | △ | 削除は該当雇用形態のユーザーがいない場合のみ可能 |
| notification_types | ○ | ○ | △ | 削除は通知実績がない場合のみ可能 |
| languages | ○ | ○ | △ | 削除は言語設定のユーザーがいない場合のみ可能 |
| countries | ○ | ○ | △ | 削除は国設定のユーザーがいない場合のみ可能 |
| prefectures | ○ | ○ | △ | 削除は都道府県設定のユーザーがいない場合のみ可能 |

### 4.5 階層構造の制約

- 階層構造を持つマスタデータ（departments, skill_categories）は循環参照不可
- 階層の深さに制限あり（最大5階層）
- 親子関係の変更時は子孫の階層レベルも自動更新

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-071](API仕様書_API-071.md) | システム設定取得API | システム設定情報の取得 |
| [API-072](API仕様書_API-072.md) | システム設定更新API | システム設定情報の更新 |
| [API-073](API仕様書_API-073.md) | マスタデータ取得API | マスタデータの取得 |
| [API-075](API仕様書_API-075.md) | マスタデータインポートAPI | マスタデータの一括インポート |
| [API-076](API仕様書_API-076.md) | マスタデータエクスポートAPI | マスタデータの一括エクスポート |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| departments | 部署情報 | 作成（C）, 更新（U）, 削除（D） |
| positions | 役職情報 | 作成（C）, 更新（U）, 削除（D） |
| skills | スキル情報 | 作成（C）, 更新（U）, 削除（D） |
| skill_categories | スキルカテゴリ情報 | 作成（C）, 更新（U）, 削除（D） |
| work_categories | 作業カテゴリ情報 | 作成（C）, 更新（U）, 削除（D） |
| training_categories | 研修カテゴリ情報 | 作成（C）, 更新（U）, 削除（D） |
| project_types | プロジェクト種別情報 | 作成（C）, 更新（U）, 削除（D） |
| employment_types | 雇用形態情報 | 作成（C）, 更新（U）, 削除（D） |
| notification_types | 通知種別情報 | 作成（C）, 更新（U）, 削除（D） |
| languages | 言語情報 | 作成（C）, 更新（U）, 削除（D） |
| countries | 国情報 | 作成（C）, 更新（U）, 削除（D） |
| prefectures | 都道府県情報 | 作成（C）, 更新（U）, 削除（D） |
| master_data_history | マスタデータ変更履歴 | 作成（C） |

### 5.3 注意事項・補足

- マスタデータの更新はシステム全体に影響するため、慎重に行う必要がある
- 一度に大量のマスタデータを更新する場合は、マスタデータインポートAPIの利用を推奨
- 削除操作は物理削除ではなく論理削除（is_active=false）が基本
- 物理削除は参照されていない場合のみ可能
- マスタデータの変更はすべて履歴として保存され、監査可能
- マスタデータの更新後はキャッシュがクリアされるため、一時的にパフォーマンスが低下する可能性あり

---

## 6. サンプルコード

### 6.1 マスタデータ更新例（JavaScript/Fetch API）

```javascript
/**
 * マスタデータを更新する関数
 * @param {string} masterType - マスタデータ種別
 * @param {Array} items - 更新するマスタデータ項目の配列
 * @param {string} [operation="update"] - 操作種別（"update", "create", "delete"）
 * @param {string} [comment=""] - 更新コメント
 * @returns {Promise<Object>} 更新結果
 */
async function updateMasterData(masterType, items, operation = "update", comment = "") {
  try {
    // リクエストボディの構築
    const requestBody = {
      operation,
      items,
      comment
    };
    
    // APIリクエスト
    const response = await fetch(`https://api.example.com/api/system/masters/${masterType}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${getAdminAuthToken()}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error.message || 'マスタデータの更新に失敗しました');
    }
    
    return await response.json();
  } catch (error) {
    console.error('マスタデータ更新エラー:', error);
    throw error;
  }
}

// 使用例：スキルデータの更新
async function updateSkillData() {
  try {
    const result = await updateMasterData(
      'skills',
      [
        {
          id: 'java',
          name: 'Java',
          code: 'SKILL_JAVA',
          description: 'Javaプログラミング言語に関するスキル（Java 17対応）',
          sort_order: 10,
          is_active: true,
          category_id: 'programming_languages',
          level_criteria: {
            level1: '基本的な文法を理解し、簡単なプログラムを作成できる',
            level2: 'オブジェクト指向の概念を理解し、実務で基本的な開発ができる',
            level3: 'フレームワークを活用した複雑なアプリケーション開発ができる',
            level4: 'アーキテクチャ設計や最適化、チューニングができる'
          },
          related_skills: ['spring', 'junit', 'maven', 'gradle']
        }
      ],
      'update',
      'Java 17対応の説明を追加'
    );
    
    console.log('スキル更新結果:', result);
    return result;
  } catch (error) {
    console.error('スキル更新エラー:', error);
    throw error;
  }
}

// 使用例：新しい部署の作成
async function createNewDepartment() {
  try {
    const result = await updateMasterData(
      'departments',
      [
        {
          name: 'データサイエンス課',
          code: 'DEV_DS',
          description: 'データ分析・機械学習を担当する課',
          sort_order: 30,
          is_active: true,
          parent_id: 'dept_dev'
        }
      ],
      'create',
      'データサイエンス課の新設'
    );
    
    console.log('部署作成結果:', result);
    return result;
  } catch (error) {
    console.error('部署作成エラー:', error);
    throw error;
  }
}
```

### 6.2 マスタデータ編集コンポーネント例（React）

```jsx
import React, { useState, useEffect } from 'react';
import { getMasterData, updateMasterData } from '../api/masterDataApi';
import MasterDataForm from './MasterDataForm';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';
import SuccessMessage from '../common/SuccessMessage';
import ConfirmDialog from '../common/ConfirmDialog';

const MasterDataEditor = ({ 
  masterType, 
  itemId = null, // 編集対象のID（新規作成時はnull）
  onSaved = null, 
  onCancel = null 
}) => {
  // 状態管理
  const [formData, setFormData] = useState({});
  const [originalData, setOriginalData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showConfirm, setShowConfirm] = useState(false);
  const [updateComment, setUpdateComment] = useState('');
  const [validationErrors, setValidationErrors] = useState({});
  
  // 編集モード判定
  const isEditMode = !!itemId;
  
  // マスタデータの取得
  useEffect(() => {
    const fetchMasterData = async () => {
      if (!isEditMode) {
        // 新規作成モードの場合は初期値を設定
        setFormData(getInitialFormData(masterType));
        setIsLoading(false);
        return;
      }
      
      try {
        setIsLoading(true);
        setError(null);
        
        // 編集対象のマスタデータを取得
        const data = await getMasterData(masterType, {
          includeInactive: true
        });
        
        // 編集対象のアイテムを検索
        const targetItem = data.items.find(item => item.id === itemId);
        
        if (!targetItem) {
          throw new Error(`指定されたID「${itemId}」のマスタデータが見つかりません。`);
        }
        
        setOriginalData(targetItem);
        setFormData(targetItem);
      } catch (err) {
        setError(err.message || 'マスタデータの取得に失敗しました');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchMasterData();
  }, [masterType, itemId, isEditMode]);
  
  // 入力値変更ハンドラ
  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
    
    // 該当するフィールドのバリデーションエラーをクリア
    if (validationErrors[field]) {
      const newErrors = { ...validationErrors };
      delete newErrors[field];
      setValidationErrors(newErrors);
    }
  };
  
  // フォーム送信ハンドラ
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // バリデーション
    const errors = validateFormData(masterType, formData);
    if (Object.keys(
