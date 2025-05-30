# API定義書：API-204 全通知既読API

## 1. 基本情報

- **API ID**: API-204
- **API名称**: 全通知既読API
- **概要**: ユーザーの全ての未読通知を一括で既読状態に更新する
- **エンドポイント**: `/api/notifications/read-all`
- **HTTPメソッド**: PUT
- **リクエスト形式**: JSON
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-NOTIFY](画面設計書_SCR-NOTIFY.md)
- **作成日**: 2025/05/28
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/28 初版作成

---

## 2. リクエスト仕様

### 2.1 リクエストパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| filter_type | string | - | 通知種別フィルター | "all", "system", "certification", "goal", "training", "other"のいずれか<br>デフォルト："all" |
| before_date | string | - | 指定日時以前の通知のみ対象 | ISO 8601形式<br>指定しない場合は全ての未読通知が対象 |

### 2.2 リクエスト例

```json
{
  "filter_type": "certification",
  "before_date": "2025-05-25T00:00:00+09:00"
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| updated_count | number | 更新された通知数 | 既読状態に更新された通知の件数 |
| updated_at | string | 更新日時 | ISO 8601形式 |

### 3.2 正常時レスポンス例

```json
{
  "updated_count": 15,
  "updated_at": "2025-05-28T15:45:30+09:00"
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 通知更新権限なし |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |
| 503 Service Unavailable | SERVICE_UNAVAILABLE | サービスが一時的に利用できません | システム過負荷/メンテナンス中 |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "パラメータが不正です",
    "details": "before_dateの形式が不正です。ISO 8601形式（YYYY-MM-DDThh:mm:ss+hh:mm）で指定してください。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - 通知更新権限の確認
2. リクエストパラメータの検証
   - filter_typeの値チェック
   - before_dateの形式チェック
3. 対象通知の抽出
   - ユーザーIDに紐づく未読通知の抽出
   - フィルター条件による絞り込み
4. 一括既読処理
   - トランザクション開始
   - 対象通知の既読状態一括更新
   - 更新履歴の一括記録
   - トランザクション終了（コミットまたはロールバック）
5. レスポンスの生成
   - 更新件数の集計
   - 更新日時の設定
6. レスポンス返却

### 4.2 一括更新ルール

- 既に既読状態の通知は対象外（カウントに含まれない）
- 更新対象が0件の場合も正常終了（updated_count=0）
- 大量通知の場合はバックグラウンド処理で非同期実行
- 更新履歴はバッチ処理でまとめて記録

### 4.3 パフォーマンス要件

- 処理時間：1000件の通知で3秒以内
- タイムアウト：30秒
- 同時処理数：最大10リクエスト
- 更新上限：1回の処理で最大10,000件まで

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-201](API仕様書_API-201.md) | 通知一覧取得API | 通知一覧の取得 |
| [API-202](API仕様書_API-202.md) | 通知詳細取得API | 通知の詳細情報取得 |
| [API-203](API仕様書_API-203.md) | 通知状態更新API | 個別通知の既読状態更新 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| notifications | 通知情報 | 参照（R） |
| notification_reads | 通知既読状態 | 参照/作成/更新（R/C/U） |
| notification_read_logs | 既読状態変更履歴 | 作成（C） |

### 5.3 注意事項・補足

- 大量の通知を一括で既読にする場合に使用
- 処理負荷が高いため、短時間での連続呼び出しは制限
- 未読カウンターは自動的に更新される
- 通知種別ごとの一括既読も可能（filter_typeで指定）
- 処理完了後、通知一覧の再取得を推奨

---

## 6. サンプルコード

### 6.1 全通知既読化例（JavaScript/Fetch API）

```javascript
/**
 * 全ての未読通知を既読状態に更新する関数
 * @param {Object} options - オプション
 * @param {string} [options.filterType] - 通知種別フィルター
 * @param {string} [options.beforeDate] - 指定日時以前の通知のみ対象
 * @returns {Promise<Object>} 更新結果
 */
async function markAllNotificationsAsRead(options = {}) {
  try {
    const response = await fetch('https://api.example.com/api/notifications/read-all', {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        filter_type: options.filterType || 'all',
        before_date: options.beforeDate || undefined
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error.message || '通知の一括既読化に失敗しました');
    }
    
    return await response.json();
  } catch (error) {
    console.error('通知一括既読化エラー:', error);
    throw error;
  }
}
```

### 6.2 通知一覧画面での一括既読ボタン実装例（React）

```jsx
import React, { useState } from 'react';
import { markAllNotificationsAsRead } from '../api/notificationApi';

const NotificationHeader = ({ onAllRead, unreadCount }) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  
  // 全て既読にするハンドラ
  const handleMarkAllAsRead = async () => {
    if (unreadCount === 0) {
      // 未読通知がない場合は何もしない
      return;
    }
    
    try {
      setIsProcessing(true);
      setError(null);
      
      // API呼び出し
      const result = await markAllNotificationsAsRead();
      
      // 成功メッセージ表示
      showSuccessToast(`${result.updated_count}件の通知を既読にしました`);
      
      // 親コンポーネントに通知
      onAllRead(result.updated_count);
      
    } catch (err) {
      setError(err.message);
      showErrorToast(`通知の一括既読化に失敗しました: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };
  
  return (
    <div className="notification-header">
      <h2 className="notification-title">通知一覧</h2>
      
      <div className="notification-actions">
        <span className="unread-badge">
          未読: {unreadCount}件
        </span>
        
        <button 
          className="mark-all-read-button"
          onClick={handleMarkAllAsRead}
          disabled={isProcessing || unreadCount === 0}
        >
          {isProcessing ? (
            <span className="loading-spinner"></span>
          ) : (
            <span>すべて既読にする</span>
          )}
        </button>
      </div>
      
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default NotificationHeader;
```

### 6.3 種別別一括既読機能実装例（TypeScript）

```typescript
interface MarkAsReadOptions {
  filterType?: 'all' | 'system' | 'certification' | 'goal' | 'training' | 'other';
  beforeDate?: string;
}

interface MarkAsReadResult {
  updated_count: number;
  updated_at: string;
}

/**
 * 通知種別ごとの一括既読機能コンポーネント
 */
const NotificationBulkActions: React.FC = () => {
  const [selectedType, setSelectedType] = useState<string>('all');
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [result, setResult] = useState<MarkAsReadResult | null>(null);
  
  // 種別選択ハンドラ
  const handleTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedType(e.target.value);
  };
  
  // 選択種別の一括既読処理
  const handleMarkSelectedTypeAsRead = async () => {
    try {
      setIsProcessing(true);
      
      const options: MarkAsReadOptions = {
        filterType: selectedType as any
      };
      
      // API呼び出し
      const result = await markAllNotificationsAsRead(options);
      setResult(result);
      
      // 成功メッセージ
      if (result.updated_count > 0) {
        const typeText = selectedType === 'all' ? 'すべての' : 
                        selectedType === 'system' ? 'システム' :
                        selectedType === 'certification' ? '資格' :
                        selectedType === 'goal' ? '目標' :
                        selectedType === 'training' ? '研修' : 'その他の';
                        
        showSuccessMessage(`${typeText}通知 ${result.updated_count}件を既読にしました`);
        
        // 通知一覧の再取得
        refreshNotificationList();
      } else {
        showInfoMessage('既読にする未読通知はありませんでした');
      }
    } catch (error) {
      showErrorMessage(`一括既読処理に失敗しました: ${error.message}`);
    } finally {
      setIsProcessing(false);
    }
  };
  
  return (
    <div className="notification-bulk-actions">
      <h3>種別別一括既読</h3>
      
      <div className="action-controls">
        <select 
          value={selectedType}
          onChange={handleTypeChange}
          disabled={isProcessing}
        >
          <option value="all">すべての通知</option>
          <option value="system">システム通知</option>
          <option value="certification">資格関連</option>
          <option value="goal">目標関連</option>
          <option value="training">研修関連</option>
          <option value="other">その他</option>
        </select>
        
        <button
          onClick={handleMarkSelectedTypeAsRead}
          disabled={isProcessing}
          className="bulk-action-button"
        >
          {isProcessing ? '処理中...' : '選択種別を既読にする'}
        </button>
      </div>
      
      {result && result.updated_count > 0 && (
        <div className="result-message">
          <p>{result.updated_count}件の通知を既読にしました</p>
          <p className="timestamp">処理日時: {formatDateTime(result.updated_at)}</p>
        </div>
      )}
    </div>
  );
};
