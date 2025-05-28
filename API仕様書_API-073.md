# API仕様書：API-073 マスタデータ取得API

## 1. 基本情報

- **API ID**: API-073
- **API名称**: マスタデータ取得API
- **概要**: システムで使用するマスタデータを取得する
- **エンドポイント**: `/api/system/masters/{master_type}`
- **HTTPメソッド**: GET
- **リクエスト形式**: URL Path Parameter + Query Parameter
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
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

### 2.2 クエリパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| include_inactive | boolean | - | 無効データを含めるか | デフォルト：false |
| parent_id | string | - | 親ID | 階層構造を持つマスタデータの場合に指定 |
| search | string | - | 検索キーワード | 名称や説明などを部分一致検索 |
| sort_by | string | - | ソート項目 | "id", "name", "code", "sort_order"のいずれか<br>デフォルト："sort_order" |
| sort_order | string | - | ソート順 | "asc"（昇順）, "desc"（降順）のいずれか<br>デフォルト："asc" |
| page | number | - | ページ番号 | 1以上の整数<br>デフォルト：1 |
| per_page | number | - | 1ページあたりの件数 | 1〜100の整数<br>デフォルト：100 |

### 2.3 リクエスト例

```
GET /api/system/masters/skills?include_inactive=false&parent_id=skill_category_1&search=java&sort_by=name&sort_order=asc&page=1&per_page=50
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| master_type | string | マスタデータ種別 | |
| total_count | number | 総レコード数 | 検索条件に合致する全レコード数 |
| page | number | 現在のページ番号 | |
| per_page | number | 1ページあたりの件数 | |
| total_pages | number | 総ページ数 | |
| items | array | マスタデータ項目の配列 | 詳細は以下参照 |
| last_updated_at | string | 最終更新日時 | ISO 8601形式 |

#### items 配列要素（共通項目）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| id | string | ID | |
| name | string | 名称 | |
| code | string | コード | |
| description | string | 説明 | |
| sort_order | number | 表示順 | |
| is_active | boolean | 有効フラグ | |
| created_at | string | 作成日時 | ISO 8601形式 |
| updated_at | string | 更新日時 | ISO 8601形式 |

#### マスタデータ種別ごとの追加項目

##### departments（部署）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| parent_id | string | 親部署ID | |
| manager_id | string | 部署管理者ID | |
| level | number | 階層レベル | |
| has_children | boolean | 子部署有無 | |

##### positions（役職）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| level | number | 役職レベル | |
| is_manager | boolean | 管理職フラグ | |

##### skills（スキル）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| category_id | string | スキルカテゴリID | |
| level_criteria | object | レベル基準 | 詳細は以下参照 |
| related_skills | array | 関連スキルID | |

##### level_criteria オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| level1 | string | レベル1基準 | |
| level2 | string | レベル2基準 | |
| level3 | string | レベル3基準 | |
| level4 | string | レベル4基準 | |

##### skill_categories（スキルカテゴリ）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| parent_id | string | 親カテゴリID | |
| level | number | 階層レベル | |
| has_children | boolean | 子カテゴリ有無 | |
| color | string | 表示色 | カラーコード（#RRGGBB） |

### 3.2 正常時レスポンス例（skills）

```json
{
  "master_type": "skills",
  "total_count": 120,
  "page": 1,
  "per_page": 50,
  "total_pages": 3,
  "items": [
    {
      "id": "java",
      "name": "Java",
      "code": "SKILL_JAVA",
      "description": "Javaプログラミング言語に関するスキル",
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
      "updated_at": "2025-04-01T15:30:00+09:00"
    },
    {
      "id": "javascript",
      "name": "JavaScript",
      "code": "SKILL_JS",
      "description": "JavaScriptプログラミング言語に関するスキル",
      "sort_order": 20,
      "is_active": true,
      "category_id": "programming_languages",
      "level_criteria": {
        "level1": "基本的な文法を理解し、簡単なスクリプトを作成できる",
        "level2": "DOM操作やイベント処理を理解し、実務で基本的な開発ができる",
        "level3": "フレームワークを活用した複雑なWebアプリケーション開発ができる",
        "level4": "高度な非同期処理やパフォーマンス最適化ができる"
      },
      "related_skills": ["typescript", "react", "vue", "angular", "node"],
      "created_at": "2025-01-15T10:00:00+09:00",
      "updated_at": "2025-04-01T15:30:00+09:00"
    }
  ],
  "last_updated_at": "2025-04-01T15:30:00+09:00"
}
```

### 3.3 正常時レスポンス例（departments）

```json
{
  "master_type": "departments",
  "total_count": 15,
  "page": 1,
  "per_page": 50,
  "total_pages": 1,
  "items": [
    {
      "id": "dept_dev",
      "name": "開発部",
      "code": "DEV",
      "description": "製品開発を担当する部署",
      "sort_order": 10,
      "is_active": true,
      "parent_id": null,
      "manager_id": "yamada.taro",
      "level": 1,
      "has_children": true,
      "created_at": "2025-01-15T10:00:00+09:00",
      "updated_at": "2025-04-01T15:30:00+09:00"
    },
    {
      "id": "dept_dev_web",
      "name": "Web開発課",
      "code": "DEV_WEB",
      "description": "Web製品開発を担当する課",
      "sort_order": 20,
      "is_active": true,
      "parent_id": "dept_dev",
      "manager_id": "suzuki.jiro",
      "level": 2,
      "has_children": false,
      "created_at": "2025-01-15T10:00:00+09:00",
      "updated_at": "2025-04-01T15:30:00+09:00"
    }
  ],
  "last_updated_at": "2025-04-01T15:30:00+09:00"
}
```

### 3.4 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | マスタデータ閲覧権限なし |
| 404 Not Found | MASTER_TYPE_NOT_FOUND | 指定されたマスタデータ種別が見つかりません | 存在しないmaster_type |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.5 エラー時レスポンス例

```json
{
  "error": {
    "code": "MASTER_TYPE_NOT_FOUND",
    "message": "指定されたマスタデータ種別が見つかりません",
    "details": "指定されたmaster_type「invalid_type」は存在しません。有効なmaster_typeを指定してください。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - マスタデータ閲覧権限の確認
2. リクエストパラメータの検証
   - master_typeの値チェック
   - クエリパラメータの形式チェック
3. マスタデータの取得
   - 指定されたmaster_typeに対応するマスタデータを取得
   - 検索条件に合致するレコードの総数を取得
   - ページネーション情報に基づいて対象レコードを取得
4. レスポンスの生成
   - 取得したデータを整形してJSONレスポンスを生成
5. レスポンス返却

### 4.2 アクセス制御ルール

- 基本的なマスタデータ（skills, departments等）は一般ユーザーも閲覧可能
- 管理用マスタデータは管理者権限を持つユーザーのみ閲覧可能
- マスタデータ種別ごとに閲覧権限を細分化可能
  - departments: 全ユーザー閲覧可能
  - positions: 全ユーザー閲覧可能
  - skills: 全ユーザー閲覧可能
  - skill_categories: 全ユーザー閲覧可能
  - work_categories: 全ユーザー閲覧可能
  - training_categories: 全ユーザー閲覧可能
  - project_types: 全ユーザー閲覧可能
  - employment_types: 人事担当者・管理者のみ閲覧可能
  - notification_types: 管理者のみ閲覧可能
  - languages: 全ユーザー閲覧可能
  - countries: 全ユーザー閲覧可能
  - prefectures: 全ユーザー閲覧可能

### 4.3 パフォーマンス要件

- 応答時間：平均200ms以内
- タイムアウト：3秒
- キャッシュ：マスタデータ種別ごとに30分キャッシュ
- 同時リクエスト：最大20リクエスト/秒

### 4.4 マスタデータ種別一覧

| マスタデータ種別 | 説明 | 主な用途 |
|---------------|------|---------|
| departments | 部署 | 組織構造、ユーザー所属部署 |
| positions | 役職 | ユーザー役職、権限管理 |
| skills | スキル | スキル評価、スキルマップ |
| skill_categories | スキルカテゴリ | スキルの分類 |
| work_categories | 作業カテゴリ | 作業実績の分類 |
| training_categories | 研修カテゴリ | 研修の分類 |
| project_types | プロジェクト種別 | プロジェクトの分類 |
| employment_types | 雇用形態 | ユーザーの雇用形態 |
| notification_types | 通知種別 | 通知の分類 |
| languages | 言語 | 多言語対応、ユーザー言語設定 |
| countries | 国 | 地域設定、住所情報 |
| prefectures | 都道府県 | 住所情報 |

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-071](API仕様書_API-071.md) | システム設定取得API | システム設定情報の取得 |
| [API-072](API仕様書_API-072.md) | システム設定更新API | システム設定情報の更新 |
| [API-074](API仕様書_API-074.md) | マスタデータ更新API | マスタデータの更新 |
| [API-075](API仕様書_API-075.md) | マスタデータインポートAPI | マスタデータの一括インポート |
| [API-076](API仕様書_API-076.md) | マスタデータエクスポートAPI | マスタデータの一括エクスポート |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| departments | 部署情報 | 参照（R） |
| positions | 役職情報 | 参照（R） |
| skills | スキル情報 | 参照（R） |
| skill_categories | スキルカテゴリ情報 | 参照（R） |
| work_categories | 作業カテゴリ情報 | 参照（R） |
| training_categories | 研修カテゴリ情報 | 参照（R） |
| project_types | プロジェクト種別情報 | 参照（R） |
| employment_types | 雇用形態情報 | 参照（R） |
| notification_types | 通知種別情報 | 参照（R） |
| languages | 言語情報 | 参照（R） |
| countries | 国情報 | 参照（R） |
| prefectures | 都道府県情報 | 参照（R） |
| master_data_history | マスタデータ変更履歴 | 参照（R） |

### 5.3 注意事項・補足

- マスタデータは頻繁に変更されないため、積極的にキャッシュを活用
- 階層構造を持つマスタデータ（departments, skill_categories等）はparent_idで親子関係を表現
- 無効化されたマスタデータ（is_active=false）は通常の検索結果には含まれない
- マスタデータの変更はすべて履歴として保存され、監査可能
- マスタデータの一部は多言語対応しており、ユーザーの言語設定に応じて表示名が変わる場合あり

---

## 6. サンプルコード

### 6.1 マスタデータ取得例（JavaScript/Fetch API）

```javascript
/**
 * マスタデータを取得する関数
 * @param {string} masterType - マスタデータ種別
 * @param {Object} options - 取得オプション
 * @param {boolean} [options.includeInactive] - 無効データを含めるか
 * @param {string} [options.parentId] - 親ID
 * @param {string} [options.search] - 検索キーワード
 * @param {string} [options.sortBy] - ソート項目
 * @param {string} [options.sortOrder] - ソート順
 * @param {number} [options.page] - ページ番号
 * @param {number} [options.perPage] - 1ページあたりの件数
 * @returns {Promise<Object>} マスタデータ
 */
async function getMasterData(masterType, options = {}) {
  try {
    // クエリパラメータの構築
    const queryParams = new URLSearchParams();
    if (options.includeInactive !== undefined) queryParams.append('include_inactive', options.includeInactive);
    if (options.parentId) queryParams.append('parent_id', options.parentId);
    if (options.search) queryParams.append('search', options.search);
    if (options.sortBy) queryParams.append('sort_by', options.sortBy);
    if (options.sortOrder) queryParams.append('sort_order', options.sortOrder);
    if (options.page) queryParams.append('page', options.page);
    if (options.perPage) queryParams.append('per_page', options.perPage);
    
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
    
    // APIリクエスト
    const response = await fetch(`https://api.example.com/api/system/masters/${masterType}${queryString}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`,
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error.message || 'マスタデータの取得に失敗しました');
    }
    
    return await response.json();
  } catch (error) {
    console.error('マスタデータ取得エラー:', error);
    throw error;
  }
}

// 使用例：スキルデータの取得
async function getSkillsData() {
  try {
    const skillsData = await getMasterData('skills', {
      includeInactive: false,
      parentId: 'programming_languages',
      sortBy: 'name',
      sortOrder: 'asc'
    });
    
    console.log(`取得したスキル数: ${skillsData.total_count}`);
    console.log('スキル一覧:', skillsData.items);
    
    return skillsData;
  } catch (error) {
    console.error('スキルデータ取得エラー:', error);
    throw error;
  }
}

// 使用例：部署データの階層構造取得
async function getDepartmentHierarchy() {
  try {
    // 最上位部署の取得
    const topLevelDepartments = await getMasterData('departments', {
      parentId: null,
      sortBy: 'sort_order',
      sortOrder: 'asc'
    });
    
    // 子部署を持つ部署について子部署を取得
    const departmentHierarchy = await Promise.all(
      topLevelDepartments.items
        .filter(dept => dept.has_children)
        .map(async (dept) => {
          const childDepartments = await getMasterData('departments', {
            parentId: dept.id,
            sortBy: 'sort_order',
            sortOrder: 'asc'
          });
          
          return {
            ...dept,
            children: childDepartments.items
          };
        })
    );
    
    console.log('部署階層構造:', departmentHierarchy);
    return departmentHierarchy;
  } catch (error) {
    console.error('部署階層構造取得エラー:', error);
    throw error;
  }
}
```

### 6.2 マスタデータ選択コンポーネント例（React）

```jsx
import React, { useState, useEffect } from 'react';
import { getMasterData } from '../api/masterDataApi';
import Select from '../common/Select';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';

const MasterDataSelect = ({ 
  masterType, 
  value, 
  onChange, 
  label, 
  placeholder = '選択してください', 
  required = false,
  parentId = null,
  includeInactive = false,
  disabled = false
}) => {
  // 状態管理
  const [options, setOptions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // マスタデータの取得
  useEffect(() => {
    const fetchMasterData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const data = await getMasterData(masterType, {
          includeInactive,
          parentId,
          sortBy: 'sort_order',
          sortOrder: 'asc',
          perPage: 100 // 十分な数を取得
        });
        
        // 選択肢の形式に変換
        const selectOptions = data.items.map(item => ({
          value: item.id,
          label: item.name,
          data: item // 元のデータも保持
        }));
        
        setOptions(selectOptions);
      } catch (err) {
        setError(err.message || 'マスタデータの取得に失敗しました');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchMasterData();
  }, [masterType, parentId, includeInactive]);
  
  // 選択変更ハンドラ
  const handleChange = (selectedValue) => {
    // 選択された値に対応するマスタデータ項目を取得
    const selectedOption = options.find(option => option.value === selectedValue);
    
    // 値と元のデータを親コンポーネントに渡す
    onChange(selectedValue, selectedOption ? selectedOption.data : null);
  };
  
  if (isLoading) {
    return <LoadingSpinner size="small" />;
  }
  
  if (error) {
    return <ErrorMessage message={error} />;
  }
  
  return (
    <div className="master-data-select">
      {label && (
        <label className={required ? 'required' : ''}>
          {label}
        </label>
      )}
      <Select
        options={options}
        value={value}
        onChange={handleChange}
        placeholder={placeholder}
        disabled={disabled || options.length === 0}
      />
      {options.length === 0 && !isLoading && !error && (
        <div className="no-options-message">
          選択可能な{getMasterTypeName(masterType)}がありません
        </div>
      )}
    </div>
  );
};

// マスタデータ種別の表示名を取得
function getMasterTypeName(masterType) {
  const masterTypeMap = {
    'departments': '部署',
    'positions': '役職',
    'skills': 'スキル',
    'skill_categories': 'スキルカテゴリ',
    'work_categories': '作業カテゴリ',
    'training_categories': '研修カテゴリ',
    'project_types': 'プロジェクト種別',
    'employment_types': '雇用形態',
    'notification_types': '通知種別',
    'languages': '言語',
    'countries': '国',
    'prefectures': '都道府県'
  };
  
  return masterTypeMap[masterType] || masterType;
}

export default MasterDataSelect;
```

### 6.3 マスタデータ階層表示コンポーネント例（React）

```jsx
import React, { useState, useEffect } from 'react';
import { getMasterData } from '../api/masterDataApi';
import TreeView from '../common/TreeView';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';

const MasterDataTree = ({ 
  masterType, 
  onSelect, 
  selectedId = null,
  includeInactive = false
}) => {
  // 状態管理
  const [treeData, setTreeData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // 階層構造を持つマスタデータかチェック
  const isHierarchicalMaster = ['departments', 'skill_categories'].includes(masterType);
  
  // マスタデータの取得と階層構造の構築
  useEffect(() => {
    const fetchMasterData = async () => {
      if (!isHierarchicalMaster) {
        setError(`${getMasterTypeName(masterType)}は階層構造をサポートしていません`);
        setIsLoading(false);
        return;
      }
      
      try {
        setIsLoading(true);
        setError(null);
        
        // 最上位の項目を取得
        const topLevelData = await getMasterData(masterType, {
          includeInactive,
          parentId: null,
          sortBy: 'sort_order',
          sortOrder: 'asc',
          perPage: 100
        });
        
        // 階層構造の構築
        const buildTreeData = async (items) => {
          const result = [];
          
          for (const item of items) {
            const treeNode = {
              id: item.id,
              label: item.name,
              data: item,
              children: []
            };
            
            // 子を持つ場合は子を取得
            if (item.has_children) {
              const childrenData = await getMasterData(masterType, {
                includeInactive,
                parentId: item.id,
                sortBy: 'sort_order',
                sortOrder: 'asc',
                perPage: 100
              });
              
              treeNode.children = await buildTreeData(childrenData.items);
            }
            
            result.push(treeNode);
          }
          
          return result;
        };
        
        const hierarchyData = await buildTreeData(topLevelData.items);
        setTreeData(hierarchyData);
      } catch (err) {
        setError(err.message || 'マスタデータの取得に失敗しました');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchMasterData();
  }, [masterType, includeInactive, isHierarchicalMaster]);
  
  // 選択変更ハンドラ
  const handleSelect = (nodeId, nodeData) => {
    if (onSelect) {
      onSelect(nodeId, nodeData);
    }
  };
  
  if (isLoading) {
    return <LoadingSpinner message={`${getMasterTypeName(masterType)}データを読み込み中...`} />;
  }
