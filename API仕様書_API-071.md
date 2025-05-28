# API仕様書：API-071 システム設定取得API

## 1. 基本情報

- **API ID**: API-071
- **API名称**: システム設定取得API
- **概要**: システム設定情報を取得する
- **エンドポイント**: `/api/system/settings`
- **HTTPメソッド**: GET
- **リクエスト形式**: Query Parameter
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **権限要件**: 管理者権限
- **利用画面**: [SCR-ADMIN](画面設計書_SCR-ADMIN.md)
- **作成日**: 2025/05/28
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/28 初版作成

---

## 2. リクエスト仕様

### 2.1 クエリパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| category | string | - | 設定カテゴリ | "general", "security", "notification", "integration", "appearance"のいずれか<br>指定なしの場合は全カテゴリを取得 |
| include_sensitive | boolean | - | 機密情報を含めるか | デフォルト：false<br>trueの場合は追加の権限チェックあり |

### 2.2 リクエスト例

```
GET /api/system/settings?category=security&include_sensitive=true
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| settings | array | 設定情報の配列 | 詳細は以下参照 |
| last_updated_at | string | 最終更新日時 | ISO 8601形式 |
| last_updated_by | string | 最終更新者 | ユーザーID |

#### settings 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| category | string | 設定カテゴリ | "general", "security", "notification", "integration", "appearance"のいずれか |
| settings | array | カテゴリ内の設定項目 | 詳細は以下参照 |

#### settings[].settings 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| key | string | 設定キー | |
| value | string/number/boolean/object | 設定値 | 設定項目の型に応じた値 |
| data_type | string | データ型 | "string", "number", "boolean", "object", "array"のいずれか |
| display_name | string | 表示名 | |
| description | string | 説明 | |
| is_sensitive | boolean | 機密情報フラグ | trueの場合は機密情報として扱う |
| options | array | 選択肢 | 選択式の設定項目の場合のみ |
| validation | object | 検証ルール | 詳細は以下参照 |
| default_value | string/number/boolean/object | デフォルト値 | |
| updated_at | string | 更新日時 | ISO 8601形式 |

#### validation オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| required | boolean | 必須フラグ | |
| min | number | 最小値/最小文字数 | 数値/文字列の場合 |
| max | number | 最大値/最大文字数 | 数値/文字列の場合 |
| pattern | string | 正規表現パターン | 文字列の場合 |
| enum | array | 列挙値 | 選択式の場合 |

### 3.2 正常時レスポンス例

```json
{
  "settings": [
    {
      "category": "general",
      "settings": [
        {
          "key": "system_name",
          "value": "スキル報告書管理システム",
          "data_type": "string",
          "display_name": "システム名",
          "description": "システムの表示名",
          "is_sensitive": false,
          "validation": {
            "required": true,
            "min": 1,
            "max": 100
          },
          "default_value": "スキル報告書管理システム",
          "updated_at": "2025-04-01T10:30:00+09:00"
        },
        {
          "key": "company_name",
          "value": "株式会社テクノロジーイノベーション",
          "data_type": "string",
          "display_name": "会社名",
          "description": "会社名の表示設定",
          "is_sensitive": false,
          "validation": {
            "required": true,
            "min": 1,
            "max": 100
          },
          "default_value": "",
          "updated_at": "2025-04-01T10:30:00+09:00"
        },
        {
          "key": "fiscal_year_start_month",
          "value": 4,
          "data_type": "number",
          "display_name": "年度開始月",
          "description": "年度の開始月（1-12）",
          "is_sensitive": false,
          "options": [
            {"label": "1月", "value": 1},
            {"label": "2月", "value": 2},
            {"label": "3月", "value": 3},
            {"label": "4月", "value": 4},
            {"label": "5月", "value": 5},
            {"label": "6月", "value": 6},
            {"label": "7月", "value": 7},
            {"label": "8月", "value": 8},
            {"label": "9月", "value": 9},
            {"label": "10月", "value": 10},
            {"label": "11月", "value": 11},
            {"label": "12月", "value": 12}
          ],
          "validation": {
            "required": true,
            "min": 1,
            "max": 12,
            "enum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
          },
          "default_value": 4,
          "updated_at": "2025-04-01T10:30:00+09:00"
        }
      ]
    },
    {
      "category": "security",
      "settings": [
        {
          "key": "password_policy",
          "value": {
            "min_length": 8,
            "require_uppercase": true,
            "require_lowercase": true,
            "require_number": true,
            "require_special_char": true,
            "password_expiry_days": 90,
            "prevent_reuse_count": 5
          },
          "data_type": "object",
          "display_name": "パスワードポリシー",
          "description": "パスワードの要件設定",
          "is_sensitive": false,
          "validation": {
            "required": true
          },
          "default_value": {
            "min_length": 8,
            "require_uppercase": true,
            "require_lowercase": true,
            "require_number": true,
            "require_special_char": true,
            "password_expiry_days": 90,
            "prevent_reuse_count": 3
          },
          "updated_at": "2025-04-15T14:20:00+09:00"
        },
        {
          "key": "session_timeout_minutes",
          "value": 30,
          "data_type": "number",
          "display_name": "セッションタイムアウト",
          "description": "操作がない場合のセッションタイムアウト時間（分）",
          "is_sensitive": false,
          "validation": {
            "required": true,
            "min": 5,
            "max": 120
          },
          "default_value": 30,
          "updated_at": "2025-04-15T14:20:00+09:00"
        },
        {
          "key": "api_key",
          "value": "sk_live_xxxxxxxxxxxxxxxxxxxxx",
          "data_type": "string",
          "display_name": "API認証キー",
          "description": "外部システム連携用のAPIキー",
          "is_sensitive": true,
          "validation": {
            "required": true
          },
          "default_value": "",
          "updated_at": "2025-05-10T09:45:00+09:00"
        }
      ]
    }
  ],
  "last_updated_at": "2025-05-10T09:45:00+09:00",
  "last_updated_by": "admin.user"
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 管理者権限なし |
| 403 Forbidden | SENSITIVE_DATA_ACCESS_DENIED | 機密情報へのアクセス権限がありません | 機密情報アクセス権限なし |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "権限がありません",
    "details": "システム設定情報の取得には管理者権限が必要です。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - 管理者権限の確認
2. リクエストパラメータの検証
   - categoryの値チェック（指定されている場合）
3. 機密情報アクセス権限チェック
   - include_sensitive=trueの場合、追加の権限チェック
4. 設定情報の取得
   - 指定されたカテゴリの設定情報を取得
   - カテゴリ指定がない場合は全カテゴリの設定情報を取得
5. 機密情報のフィルタリング
   - include_sensitive=falseの場合、機密情報をマスク
6. レスポンスの生成
   - 取得したデータを整形してJSONレスポンスを生成
7. レスポンス返却

### 4.2 アクセス制御ルール

- システム設定情報の取得は管理者権限を持つユーザーのみ可能
- 機密情報（is_sensitive=true）の取得には追加の権限（ROLE_SYSTEM_ADMIN）が必要
- 監査ログには設定情報の参照記録が残る

### 4.3 パフォーマンス要件

- 応答時間：平均200ms以内
- タイムアウト：3秒
- キャッシュ：カテゴリ別に10分キャッシュ
- 同時リクエスト：最大10リクエスト/秒

### 4.4 設定カテゴリと主要設定項目

| カテゴリ | 説明 | 主要設定項目 |
|---------|------|------------|
| general | 一般設定 | システム名、会社名、年度開始月、タイムゾーン、言語設定など |
| security | セキュリティ設定 | パスワードポリシー、セッションタイムアウト、多要素認証設定、IPアドレス制限など |
| notification | 通知設定 | メール通知設定、プッシュ通知設定、通知頻度、通知テンプレートなど |
| integration | 外部連携設定 | API連携設定、SSO設定、外部サービス接続情報など |
| appearance | 外観設定 | テーマカラー、ロゴ設定、レイアウト設定など |

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-072](API仕様書_API-072.md) | システム設定更新API | システム設定情報の更新 |
| [API-073](API仕様書_API-073.md) | マスタデータ取得API | マスタデータの取得 |
| [API-074](API仕様書_API-074.md) | マスタデータ更新API | マスタデータの更新 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| system_settings | システム設定情報 | 参照（R） |
| system_setting_categories | 設定カテゴリ | 参照（R） |
| system_setting_history | 設定変更履歴 | 参照（R） |
| users | ユーザー情報 | 参照（R） |
| roles | 権限情報 | 参照（R） |

### 5.3 注意事項・補足

- システム設定は全ユーザーに影響するため、変更には十分な注意が必要
- 機密情報（APIキー、接続情報など）は暗号化して保存
- 設定変更はすべて履歴として保存され、監査可能
- 一部の設定はシステム再起動が必要な場合あり
- 設定値の変更はシステムの動作に直接影響するため、検証環境での事前確認を推奨

---

## 6. サンプルコード

### 6.1 システム設定取得例（JavaScript/Fetch API）

```javascript
/**
 * システム設定情報を取得する関数
 * @param {Object} options - 取得オプション
 * @param {string} [options.category] - 設定カテゴリ
 * @param {boolean} [options.includeSensitive] - 機密情報を含めるか
 * @returns {Promise<Object>} システム設定情報
 */
async function getSystemSettings(options = {}) {
  try {
    // クエリパラメータの構築
    const queryParams = new URLSearchParams();
    if (options.category) queryParams.append('category', options.category);
    if (options.includeSensitive !== undefined) queryParams.append('include_sensitive', options.includeSensitive);
    
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
    
    // APIリクエスト
    const response = await fetch(`https://api.example.com/api/system/settings${queryString}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${getAdminAuthToken()}`,
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error.message || 'システム設定情報の取得に失敗しました');
    }
    
    return await response.json();
  } catch (error) {
    console.error('システム設定情報取得エラー:', error);
    throw error;
  }
}
```

### 6.2 システム設定表示コンポーネント例（React）

```jsx
import React, { useState, useEffect } from 'react';
import { getSystemSettings } from '../api/systemApi';
import SettingCategoryTabs from './SettingCategoryTabs';
import SettingsList from './SettingsList';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';
import { formatDateTime } from '../utils/dateUtils';

const SystemSettingsView = () => {
  // 状態管理
  const [settingsData, setSettingsData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeCategory, setActiveCategory] = useState('general');
  const [includeSensitive, setIncludeSensitive] = useState(false);
  
  // 設定データの取得
  useEffect(() => {
    const fetchSettings = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const data = await getSystemSettings({
          includeSensitive
        });
        
        setSettingsData(data);
      } catch (err) {
        setError(err.message || 'システム設定情報の取得に失敗しました');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchSettings();
  }, [includeSensitive]);
  
  // カテゴリ変更ハンドラ
  const handleCategoryChange = (category) => {
    setActiveCategory(category);
  };
  
  // 機密情報表示切替ハンドラ
  const handleSensitiveToggle = () => {
    setIncludeSensitive(!includeSensitive);
  };
  
  if (isLoading) {
    return <LoadingSpinner message="システム設定情報を読み込み中..." />;
  }
  
  if (error) {
    return <ErrorMessage message={error} />;
  }
  
  if (!settingsData) {
    return <div className="no-data-message">システム設定情報がありません</div>;
  }
  
  // 現在のカテゴリの設定を取得
  const currentCategorySettings = settingsData.settings.find(
    category => category.category === activeCategory
  );
  
  return (
    <div className="system-settings-container">
      <div className="settings-header">
        <h2>システム設定</h2>
        <div className="last-updated-info">
          最終更新: {formatDateTime(settingsData.last_updated_at)} by {settingsData.last_updated_by}
        </div>
        <div className="sensitive-toggle">
          <label>
            <input 
              type="checkbox" 
              checked={includeSensitive} 
              onChange={handleSensitiveToggle} 
            />
            機密情報を表示
          </label>
        </div>
      </div>
      
      <SettingCategoryTabs 
        categories={settingsData.settings.map(cat => ({
          id: cat.category,
          name: getCategoryDisplayName(cat.category),
          count: cat.settings.length
        }))}
        activeCategory={activeCategory}
        onCategoryChange={handleCategoryChange}
      />
      
      {currentCategorySettings && (
        <SettingsList 
          settings={currentCategorySettings.settings}
          categoryName={getCategoryDisplayName(currentCategorySettings.category)}
          readOnly={true}
        />
      )}
    </div>
  );
};

// カテゴリ表示名の取得
function getCategoryDisplayName(categoryId) {
  const categoryMap = {
    'general': '一般設定',
    'security': 'セキュリティ設定',
    'notification': '通知設定',
    'integration': '外部連携設定',
    'appearance': '外観設定'
  };
  
  return categoryMap[categoryId] || categoryId;
}

export default SystemSettingsView;
```

### 6.3 設定値表示コンポーネント例（React）

```jsx
import React from 'react';
import { formatDateTime } from '../utils/dateUtils';

// 設定項目の表示コンポーネント
const SettingItem = ({ setting }) => {
  // 設定値の表示形式を取得
  const getDisplayValue = (setting) => {
    // 機密情報の場合はマスク表示
    if (setting.is_sensitive && setting.value) {
      return '********';
    }
    
    // データ型に応じた表示形式
    switch (setting.data_type) {
      case 'boolean':
        return setting.value ? 'はい' : 'いいえ';
        
      case 'object':
      case 'array':
        return (
          <pre className="setting-json-value">
            {JSON.stringify(setting.value, null, 2)}
          </pre>
        );
        
      case 'number':
        // 選択肢がある場合はラベルを表示
        if (setting.options && setting.options.length > 0) {
          const option = setting.options.find(opt => opt.value === setting.value);
          return option ? option.label : setting.value;
        }
        return setting.value;
        
      default:
        return setting.value;
    }
  };
  
  return (
    <div className="setting-item">
      <div className="setting-header">
        <h4 className="setting-name">{setting.display_name}</h4>
        {setting.is_sensitive && (
          <span className="sensitive-badge">機密情報</span>
        )}
      </div>
      
      <div className="setting-description">
        {setting.description}
      </div>
      
      <div className="setting-value">
        <div className="value-label">現在の値:</div>
        <div className="value-content">
          {getDisplayValue(setting)}
        </div>
      </div>
      
      {setting.default_value !== undefined && (
        <div className="setting-default">
          <div className="default-label">デフォルト値:</div>
          <div className="default-content">
            {setting.data_type === 'object' || setting.data_type === 'array' 
              ? JSON.stringify(setting.default_value)
              : setting.default_value.toString()}
          </div>
        </div>
      )}
      
      <div className="setting-meta">
        <div className="setting-key">キー: {setting.key}</div>
        <div className="setting-updated">
          更新日時: {formatDateTime(setting.updated_at)}
        </div>
      </div>
    </div>
  );
};

export default SettingItem;
