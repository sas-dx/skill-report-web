# API定義書：API-072 システム設定更新API

## 1. 基本情報

- **API ID**: API-072
- **API名称**: システム設定更新API
- **概要**: システム設定情報を更新する
- **エンドポイント**: `/api/system/settings`
- **HTTPメソッド**: PUT
- **リクエスト形式**: JSON
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **権限要件**: 管理者権限
- **利用画面**: [SCR-ADMIN](画面設計書_SCR-ADMIN.md)
- **作成日**: 2025/05/29
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/29 初版作成

---

## 2. リクエスト仕様

### 2.1 リクエストヘッダ

| ヘッダ名 | 説明 | 必須 | 備考 |
|---------|------|------|------|
| Authorization | 認証トークン | ○ | Bearer {JWT} |
| Content-Type | コンテンツタイプ | ○ | application/json |

### 2.2 リクエストボディ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| category | string | ○ | 設定カテゴリ | "general", "security", "notification", "integration", "appearance"のいずれか |
| settings | array | ○ | 更新する設定項目の配列 | 詳細は以下参照 |
| comment | string | - | 更新コメント | 変更履歴に記録される |

#### settings 配列要素

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| key | string | ○ | 設定キー | 既存の設定キーであること |
| value | string/number/boolean/object | ○ | 設定値 | 設定項目の型に応じた値 |

### 2.3 リクエスト例

```json
{
  "category": "security",
  "settings": [
    {
      "key": "password_policy",
      "value": {
        "min_length": 10,
        "require_uppercase": true,
        "require_lowercase": true,
        "require_number": true,
        "require_special_char": true,
        "password_expiry_days": 60,
        "prevent_reuse_count": 5
      }
    },
    {
      "key": "session_timeout_minutes",
      "value": 15
    }
  ],
  "comment": "セキュリティ強化のためパスワードポリシーとセッションタイムアウトを更新"
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| success | boolean | 処理結果 | true: 成功 |
| category | string | 更新したカテゴリ | |
| updated_settings | array | 更新された設定項目 | 詳細は以下参照 |
| updated_at | string | 更新日時 | ISO 8601形式 |
| updated_by | string | 更新者 | ユーザーID |
| requires_restart | boolean | 再起動必要フラグ | trueの場合はシステム再起動が必要 |
| message | string | 処理結果メッセージ | |

#### updated_settings 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| key | string | 設定キー | |
| old_value | string/number/boolean/object | 更新前の値 | |
| new_value | string/number/boolean/object | 更新後の値 | |

### 3.2 正常時レスポンス例

```json
{
  "success": true,
  "category": "security",
  "updated_settings": [
    {
      "key": "password_policy",
      "old_value": {
        "min_length": 8,
        "require_uppercase": true,
        "require_lowercase": true,
        "require_number": true,
        "require_special_char": true,
        "password_expiry_days": 90,
        "prevent_reuse_count": 3
      },
      "new_value": {
        "min_length": 10,
        "require_uppercase": true,
        "require_lowercase": true,
        "require_number": true,
        "require_special_char": true,
        "password_expiry_days": 60,
        "prevent_reuse_count": 5
      }
    },
    {
      "key": "session_timeout_minutes",
      "old_value": 30,
      "new_value": 15
    }
  ],
  "updated_at": "2025-05-29T10:15:30+09:00",
  "updated_by": "admin.user",
  "requires_restart": false,
  "message": "セキュリティ設定が正常に更新されました。"
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 400 Bad Request | VALIDATION_ERROR | 検証エラーが発生しました | 設定値の検証エラー |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 管理者権限なし |
| 404 Not Found | SETTING_NOT_FOUND | 指定された設定が見つかりません | 存在しない設定キー |
| 409 Conflict | CONCURRENT_UPDATE | 他のユーザーによる更新が競合しています | 同時更新の競合 |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "検証エラーが発生しました",
    "details": [
      {
        "key": "session_timeout_minutes",
        "message": "セッションタイムアウト値は5〜120の範囲で指定してください。"
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
   - 管理者権限の確認
   - システム設定更新権限の確認
2. リクエストパラメータの検証
   - categoryの値チェック
   - 必須パラメータの存在確認
   - 設定キーの存在確認
3. 設定値の検証
   - 各設定項目の型チェック
   - 各設定項目の値範囲チェック
   - 各設定項目の依存関係チェック
4. 排他制御
   - 同時更新の競合チェック
5. 設定値の更新
   - 更新前の値を保存
   - 設定値を更新
   - 更新履歴を記録
6. 再起動必要性の判定
   - 更新された設定が再起動を必要とするか判定
7. レスポンスの生成
   - 更新結果を整形してJSONレスポンスを生成
8. レスポンス返却

### 4.2 アクセス制御ルール

- システム設定情報の更新は管理者権限を持つユーザーのみ可能
- 機密情報（is_sensitive=true）の更新には追加の権限（ROLE_SYSTEM_ADMIN）が必要
- 監査ログには設定情報の更新記録が残る
- 設定カテゴリごとに更新権限を細分化可能
  - general: ROLE_ADMIN
  - security: ROLE_SECURITY_ADMIN
  - notification: ROLE_NOTIFICATION_ADMIN
  - integration: ROLE_INTEGRATION_ADMIN
  - appearance: ROLE_ADMIN

### 4.3 パフォーマンス要件

- 応答時間：平均300ms以内
- タイムアウト：5秒
- 同時リクエスト：最大5リクエスト/秒
- 更新後のキャッシュクリア：更新されたカテゴリのキャッシュを即時クリア

### 4.4 設定値検証ルール

| カテゴリ | 設定キー | 検証ルール |
|---------|---------|------------|
| general | system_name | 必須、1〜100文字 |
| general | company_name | 必須、1〜100文字 |
| general | fiscal_year_start_month | 必須、1〜12の整数 |
| general | timezone | 必須、有効なタイムゾーン識別子 |
| security | password_policy.min_length | 必須、8〜32の整数 |
| security | password_policy.password_expiry_days | 必須、0（無期限）または30〜365の整数 |
| security | session_timeout_minutes | 必須、5〜120の整数 |
| notification | email_notification_enabled | 必須、真偽値 |
| notification | notification_frequency | 必須、"realtime", "hourly", "daily"のいずれか |
| integration | api_key | 機密情報、32文字以上 |
| appearance | theme_color | 必須、有効なカラーコード（#RRGGBB） |

### 4.5 再起動が必要な設定項目

以下の設定項目が更新された場合、システムの再起動が必要：

- general.timezone
- security.jwt_secret
- integration.database_connection
- integration.ldap_settings
- system.cache_config
- system.log_level

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-071](API仕様書_API-071.md) | システム設定取得API | システム設定情報の取得 |
| [API-073](API仕様書_API-073.md) | マスタデータ取得API | マスタデータの取得 |
| [API-074](API仕様書_API-074.md) | マスタデータ更新API | マスタデータの更新 |
| [API-075](API仕様書_API-075.md) | システム設定履歴取得API | システム設定変更履歴の取得 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| system_settings | システム設定情報 | 更新（U） |
| system_setting_categories | 設定カテゴリ | 参照（R） |
| system_setting_history | 設定変更履歴 | 作成（C） |
| users | ユーザー情報 | 参照（R） |
| roles | 権限情報 | 参照（R） |

### 5.3 注意事項・補足

- システム設定は全ユーザーに影響するため、変更には十分な注意が必要
- 機密情報（APIキー、接続情報など）は暗号化して保存
- 設定変更はすべて履歴として保存され、監査可能
- 一部の設定はシステム再起動が必要な場合あり
- 設定値の変更はシステムの動作に直接影響するため、検証環境での事前確認を推奨
- 複数の設定を一度に更新する場合、すべての検証が成功した場合のみ更新を実行（トランザクション処理）

---

## 6. サンプルコード

### 6.1 システム設定更新例（JavaScript/Fetch API）

```javascript
/**
 * システム設定情報を更新する関数
 * @param {string} category - 設定カテゴリ
 * @param {Array} settings - 更新する設定項目の配列
 * @param {string} [comment] - 更新コメント
 * @returns {Promise<Object>} 更新結果
 */
async function updateSystemSettings(category, settings, comment = '') {
  try {
    // リクエストボディの構築
    const requestBody = {
      category,
      settings,
      comment
    };
    
    // APIリクエスト
    const response = await fetch('https://api.example.com/api/system/settings', {
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
      throw new Error(errorData.error.message || 'システム設定情報の更新に失敗しました');
    }
    
    return await response.json();
  } catch (error) {
    console.error('システム設定情報更新エラー:', error);
    throw error;
  }
}

// 使用例
async function updateSecuritySettings() {
  try {
    const result = await updateSystemSettings(
      'security',
      [
        {
          key: 'password_policy',
          value: {
            min_length: 10,
            require_uppercase: true,
            require_lowercase: true,
            require_number: true,
            require_special_char: true,
            password_expiry_days: 60,
            prevent_reuse_count: 5
          }
        },
        {
          key: 'session_timeout_minutes',
          value: 15
        }
      ],
      'セキュリティ強化のためパスワードポリシーとセッションタイムアウトを更新'
    );
    
    console.log('設定更新結果:', result);
    
    if (result.requires_restart) {
      // 再起動が必要な場合の処理
      showRestartNotification();
    }
    
    return result;
  } catch (error) {
    // エラーハンドリング
    handleUpdateError(error);
    throw error;
  }
}
```

### 6.2 システム設定編集コンポーネント例（React）

```jsx
import React, { useState, useEffect } from 'react';
import { getSystemSettings, updateSystemSettings } from '../api/systemApi';
import SettingForm from './SettingForm';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';
import SuccessMessage from '../common/SuccessMessage';
import ConfirmDialog from '../common/ConfirmDialog';
import { formatDateTime } from '../utils/dateUtils';

const SystemSettingsEditor = ({ category }) => {
  // 状態管理
  const [settingsData, setSettingsData] = useState(null);
  const [formValues, setFormValues] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showConfirm, setShowConfirm] = useState(false);
  const [updateComment, setUpdateComment] = useState('');
  const [validationErrors, setValidationErrors] = useState({});
  
  // 設定データの取得
  useEffect(() => {
    const fetchSettings = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const data = await getSystemSettings({
          category,
          includeSensitive: true
        });
        
        setSettingsData(data);
        
        // フォーム初期値の設定
        const initialValues = {};
        const categorySettings = data.settings.find(cat => cat.category === category);
        
        if (categorySettings && categorySettings.settings) {
          categorySettings.settings.forEach(setting => {
            initialValues[setting.key] = setting.value;
          });
        }
        
        setFormValues(initialValues);
      } catch (err) {
        setError(err.message || 'システム設定情報の取得に失敗しました');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchSettings();
  }, [category]);
  
  // 入力値変更ハンドラ
  const handleInputChange = (key, value) => {
    setFormValues({
      ...formValues,
      [key]: value
    });
    
    // 該当するフィールドのバリデーションエラーをクリア
    if (validationErrors[key]) {
      const newErrors = { ...validationErrors };
      delete newErrors[key];
      setValidationErrors(newErrors);
    }
  };
  
  // フォーム送信ハンドラ
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // 変更があるか確認
    const hasChanges = checkForChanges();
    if (!hasChanges) {
      setError('変更がありません。');
      return;
    }
    
    // バリデーション
    const errors = validateSettings();
    if (Object.keys(errors).length > 0) {
      setValidationErrors(errors);
      setError('入力内容に誤りがあります。');
      return;
    }
    
    // 確認ダイアログを表示
    setShowConfirm(true);
  };
  
  // 変更確認
  const checkForChanges = () => {
    const categorySettings = settingsData.settings.find(cat => cat.category === category);
    if (!categorySettings || !categorySettings.settings) return false;
    
    return categorySettings.settings.some(setting => {
      // オブジェクトの場合はJSON文字列化して比較
      if (typeof setting.value === 'object' && setting.value !== null) {
        return JSON.stringify(setting.value) !== JSON.stringify(formValues[setting.key]);
      }
      return setting.value !== formValues[setting.key];
    });
  };
  
  // 設定値のバリデーション
  const validateSettings = () => {
    const errors = {};
    const categorySettings = settingsData.settings.find(cat => cat.category === category);
    
    if (!categorySettings || !categorySettings.settings) return errors;
    
    categorySettings.settings.forEach(setting => {
      const value = formValues[setting.key];
      const validation = setting.validation;
      
      if (!validation) return;
      
      // 必須チェック
      if (validation.required && (value === undefined || value === null || value === '')) {
        errors[setting.key] = `${setting.display_name}は必須項目です。`;
        return;
      }
      
      // 型に応じたバリデーション
      switch (setting.data_type) {
        case 'string':
          if (validation.min && value.length < validation.min) {
            errors[setting.key] = `${setting.display_name}は${validation.min}文字以上で入力してください。`;
          } else if (validation.max && value.length > validation.max) {
            errors[setting.key] = `${setting.display_name}は${validation.max}文字以下で入力してください。`;
          } else if (validation.pattern && !new RegExp(validation.pattern).test(value)) {
            errors[setting.key] = `${setting.display_name}の形式が正しくありません。`;
          }
          break;
          
        case 'number':
          const numValue = Number(value);
          if (isNaN(numValue)) {
            errors[setting.key] = `${setting.display_name}は数値で入力してください。`;
          } else if (validation.min !== undefined && numValue < validation.min) {
            errors[setting.key] = `${setting.display_name}は${validation.min}以上で入力してください。`;
          } else if (validation.max !== undefined && numValue > validation.max) {
            errors[setting.key] = `${setting.display_name}は${validation.max}以下で入力してください。`;
          }
          break;
          
        case 'object':
          // オブジェクト型の個別バリデーションはカスタム実装
          if (setting.key === 'password_policy') {
            const policy = value;
            if (policy.min_length < 8 || policy.min_length > 32) {
              errors[setting.key] = 'パスワード最小長は8〜32の範囲で指定してください。';
            }
          }
          break;
      }
    });
    
    return errors;
  };
  
  // 設定更新の実行
  const executeUpdate = async () => {
    setShowConfirm(false);
    setIsSaving(true);
    setError(null);
    setSuccess(null);
    
    try {
      // 変更された設定のみを抽出
      const changedSettings = [];
      const categorySettings = settingsData.settings.find(cat => cat.category === category);
      
      categorySettings.settings.forEach(setting => {
        const oldValue = setting.value;
        const newValue = formValues[setting.key];
        
        // オブジェクトの場合はJSON文字列化して比較
        let hasChanged = false;
        if (typeof oldValue === 'object' && oldValue !== null) {
          hasChanged = JSON.stringify(oldValue) !== JSON.stringify(newValue);
        } else {
          hasChanged = oldValue !== newValue;
        }
        
        if (hasChanged) {
          changedSettings.push({
            key: setting.key,
            value: newValue
          });
        }
      });
      
      // 更新APIの呼び出し
      const result = await updateSystemSettings(
        category,
        changedSettings,
        updateComment
      );
      
      setSuccess(`${getCategoryDisplayName(category)}が正常に更新されました。`);
      
      // 再起動が必要な場合の通知
      if (result.requires_restart) {
        setSuccess(prev => `${prev} システムの再起動が必要です。`);
      }
      
      // 最新の設定を再取得
      const updatedData = await getSystemSettings({
        category,
        includeSensitive: true
      });
      
      setSettingsData(updatedData);
      
      // フォーム値を更新
      const updatedValues = {};
      const updatedCategorySettings = updatedData.settings.find(cat => cat.category === category);
      
      if (updatedCategorySettings && updatedCategorySettings.settings) {
        updatedCategorySettings.settings.forEach(setting => {
          updatedValues[setting.key] = setting.value;
        });
      }
      
      setFormValues(updatedValues);
      setUpdateComment('');
      
    } catch (err) {
      setError(err.message || 'システム設定の更新に失敗しました');
      
      // バリデーションエラーの処理
      if (err.details && Array.isArray(err.details)) {
        const validationErrors = {};
        err.details.forEach(detail => {
          validationErrors[detail.key] = detail.message;
        });
        setValidationErrors(validationErrors);
      }
    } finally {
      setIsSaving(false);
    }
  };
  
  // 確認ダイアログのキャンセル
  const handleConfirmCancel = () => {
    setShowConfirm(false);
  };
  
  if (isLoading) {
    return <LoadingSpinner message="システム設定情報を読み込み中..." />;
  }
  
  if (!settingsData) {
    return <ErrorMessage message="システム設定情報が取得できませんでした" />;
  }
  
  const categorySettings = settingsData.settings.find(cat => cat.category === category);
  if (!categorySettings || !categorySettings.settings) {
    return <ErrorMessage message={`${getCategoryDisplayName(category)}の設定情報が見つかりません`} />;
  }
  
  return (
    <div className="system-settings-editor">
      <h2>{getCategoryDisplayName(category)}の編集</h2>
      
      <div className="last-updated-info">
        最終更新: {formatDateTime(settingsData.last_updated_at)} by {settingsData.last_updated_by}
      </div>
      
      {error && <ErrorMessage message={error} />}
      {success && <SuccessMessage message={success} />}
      
      <form onSubmit={handleSubmit}>
        <SettingForm 
          settings={categorySettings.settings}
          values={formValues}
          onChange={handleInputChange}
          errors={validationErrors}
          disabled={isSaving}
        />
        
        <div className="form-actions">
          <button 
            type="submit" 
            className="btn btn-primary" 
            disabled={isSaving}
          >
            {isSaving ? '保存中...' : '設定を保存'}
          </button>
        </div>
      </form>
      
      {showConfirm && (
        <ConfirmDialog
          title="設定の更新"
          message={`${getCategoryDisplayName(category)}を更新します。よろしいですか？`}
          confirmLabel="更新する"
          cancelLabel="キャンセル"
          onConfirm={executeUpdate}
          onCancel={handleConfirmCancel}
        >
          <div className="update-comment-input">
            <label htmlFor="updateComment">更新コメント（任意）:</label>
            <textarea
              id="updateComment"
              value={updateComment}
              onChange={(e) => setUpdateComment(e.target.value)}
              rows={3}
              placeholder="変更内容の概要や理由を入力してください"
            />
          </div>
        </ConfirmDialog>
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

export default SystemSettingsEditor;
```

### 6.3 設定フォームコンポーネント例（React）

```jsx
import React from 'react';
import StringSettingInput from './inputs/StringSettingInput';
import NumberSettingInput from './inputs/NumberSettingInput';
import BooleanSettingInput from './inputs/BooleanSettingInput';
import SelectSettingInput from './inputs/SelectSettingInput';
import ObjectSettingInput from './inputs/ObjectSettingInput';

const SettingForm = ({ settings, values, onChange, errors, disabled }) => {
  // 設定項目の入力コンポーネントを取得
  const getInputComponent = (setting) => {
    const value = values[setting.key];
    const error = errors[setting.key];
    
    switch (setting.data_type) {
      case 'string':
        if (setting.options && setting.options.length > 0) {
          return (
            <SelectSettingInput
              setting={setting}
              value={value}
              onChange={(newValue) => onChange(setting.key, newValue)}
              error={error}
              disabled={disabled || setting.is_readonly}
            />
          );
        }
        return (
          <StringSettingInput
            setting={setting}
            value={value}
            onChange={(newValue) => onChange(setting.key, newValue)}
            error={error}
            disabled={disabled || setting.is_readonly}
          />
        );
        
      case 'number':
        return (
          <NumberSettingInput
            setting={setting}
            value={value}
            onChange={(newValue) => onChange(setting.key, newValue)}
            error={error}
            disabled={disabled || setting.is_readonly}
          />
        );
        
      case 'boolean':
        return (
          <BooleanSettingInput
            setting={setting}
            value={value}
            onChange={(newValue) => onChange(setting.key, newValue)}
            error={error}
            disabled={disabled || setting.is_readonly}
          />
        );
        
      case 'object':
      case 'array':
        return (
          <ObjectSettingInput
            setting={setting}
            value={value}
            onChange={(newValue) => onChange(setting.key, newValue)}
            error={error}
            disabled={disabled || setting.is_readonly}
          />
        );
        
      default:
        return (
          <div className="setting-unknown-type">
            未対応の設定タイプ: {setting.data_type}
          </div>
        );
    }
