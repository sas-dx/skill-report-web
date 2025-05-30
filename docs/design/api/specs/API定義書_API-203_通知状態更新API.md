# API定義書：API-203 通知状態更新API

## 1. 基本情報

- **API ID**: API-203
- **API名称**: 通知状態更新API
- **概要**: 指定された通知IDの既読状態を更新する
- **エンドポイント**: `/api/notifications/{id}/read`
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

### 2.1 パスパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| id | string | ○ | 通知ID | 更新対象の通知の一意識別子 |

### 2.2 リクエストボディ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| is_read | boolean | ○ | 既読状態 | true: 既読, false: 未読 |

### 2.3 リクエスト例

```json
{
  "is_read": true
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| id | string | 通知ID | |
| is_read | boolean | 更新後の既読状態 | true: 既読, false: 未読 |
| updated_at | string | 更新日時 | ISO 8601形式 |

### 3.2 正常時レスポンス例

```json
{
  "id": "notif_20250520001",
  "is_read": true,
  "updated_at": "2025-05-28T15:30:45+09:00"
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 通知更新権限なし |
| 404 Not Found | NOTIFICATION_NOT_FOUND | 通知が見つかりません | 指定IDの通知が存在しない |
| 409 Conflict | ALREADY_UPDATED | 既に更新されています | 既に同じ状態に更新済み |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "NOTIFICATION_NOT_FOUND",
    "message": "通知が見つかりません",
    "details": "指定されたID 'notif_20250520999' の通知は存在しないか、削除された可能性があります。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - 通知更新権限の確認
2. パスパラメータとリクエストボディの検証
   - 通知IDの形式チェック
   - is_readパラメータの型チェック
3. 通知データの取得
   - 指定IDの通知レコード取得
   - ユーザーIDとの紐付け確認（他ユーザーの通知は更新不可）
4. 既読状態の更新
   - 現在の状態と異なる場合のみ更新処理
   - 更新日時の記録
5. レスポンスの生成
   - 更新結果の整形
6. レスポンス返却

### 4.2 既読状態管理ルール

- 既読状態はユーザーごとに管理
- 同一通知に対する複数回の更新は可能（既読→未読→既読など）
- 更新履歴はログとして保存（監査目的）
- 通知の削除状態に関わらず既読状態は更新可能

### 4.3 パフォーマンス要件

- レスポンスタイム：平均100ms以内
- 同時処理数：最大100リクエスト/秒
- キャッシュ：既読状態更新時にユーザー通知キャッシュを無効化

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-201](API仕様書_API-201.md) | 通知一覧取得API | 通知一覧の取得 |
| [API-202](API仕様書_API-202.md) | 通知詳細取得API | 通知の詳細情報取得 |
| [API-204](API仕様書_API-204.md) | 全通知既読API | 全通知の一括既読化 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| notifications | 通知情報 | 参照（R） |
| notification_reads | 通知既読状態 | 参照/作成/更新（R/C/U） |
| notification_read_logs | 既読状態変更履歴 | 作成（C） |

### 5.3 注意事項・補足

- 通知詳細取得API（API-202）でも自動的に既読状態に更新される
- 未読→既読の更新は通知カウンターに影響する
- 既読→未読の更新は通知カウンターに影響する
- 通知の削除状態に関わらず既読状態は更新可能
- 大量の通知を一括で既読にする場合はAPI-204を使用

---

## 6. サンプルコード

### 6.1 通知状態更新例（JavaScript/Fetch API）

```javascript
/**
 * 通知の既読状態を更新する関数
 * @param {string} notificationId - 通知ID
 * @param {boolean} isRead - 既読状態（true: 既読, false: 未読）
 * @returns {Promise<Object>} 更新結果
 */
async function updateNotificationReadStatus(notificationId, isRead) {
  try {
    const response = await fetch(`https://api.example.com/api/notifications/${notificationId}/read`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        is_read: isRead
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error.message || '通知状態の更新に失敗しました');
    }
    
    return await response.json();
  } catch (error) {
    console.error('通知状態更新エラー:', error);
    throw error;
  }
}
```

### 6.2 通知一覧での既読切替例（React）

```jsx
import React from 'react';
import { updateNotificationReadStatus } from '../api/notificationApi';

const NotificationItem = ({ notification, onStatusChange }) => {
  const [isUpdating, setIsUpdating] = useState(false);
  const [error, setError] = useState(null);
  
  // 既読/未読切替ハンドラ
  const handleReadStatusToggle = async () => {
    try {
      setIsUpdating(true);
      setError(null);
      
      // 現在の状態と逆の状態に更新
      const newStatus = !notification.is_read;
      
      // API呼び出し
      const result = await updateNotificationReadStatus(notification.id, newStatus);
      
      // 親コンポーネントに状態変更を通知
      onStatusChange(notification.id, result.is_read);
      
    } catch (err) {
      setError(err.message);
      showErrorToast(`通知状態の更新に失敗しました: ${err.message}`);
    } finally {
      setIsUpdating(false);
    }
  };
  
  return (
    <div className={`notification-item ${notification.is_read ? 'read' : 'unread'}`}>
      <div className="notification-content">
        <h3 className="notification-title">{notification.title}</h3>
        <p className="notification-summary">{notification.summary}</p>
        <span className="notification-date">{formatDate(notification.date)}</span>
      </div>
      
      <div className="notification-actions">
        <button 
          className="read-toggle-button"
          onClick={handleReadStatusToggle}
          disabled={isUpdating}
        >
          {isUpdating ? (
            <span className="loading-spinner"></span>
          ) : notification.is_read ? (
            <span className="mark-as-unread">未読にする</span>
          ) : (
            <span className="mark-as-read">既読にする</span>
          )}
        </button>
        
        <a href={`/notifications/${notification.id}`} className="view-details-link">
          詳細を見る
        </a>
      </div>
      
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default NotificationItem;
```

### 6.3 通知状態管理例（TypeScript/Redux）

```typescript
// Action Types
const UPDATE_NOTIFICATION_STATUS_REQUEST = 'UPDATE_NOTIFICATION_STATUS_REQUEST';
const UPDATE_NOTIFICATION_STATUS_SUCCESS = 'UPDATE_NOTIFICATION_STATUS_SUCCESS';
const UPDATE_NOTIFICATION_STATUS_FAILURE = 'UPDATE_NOTIFICATION_STATUS_FAILURE';

// Action Interfaces
interface UpdateNotificationStatusRequestAction {
  type: typeof UPDATE_NOTIFICATION_STATUS_REQUEST;
  payload: {
    id: string;
    isRead: boolean;
  };
}

interface UpdateNotificationStatusSuccessAction {
  type: typeof UPDATE_NOTIFICATION_STATUS_SUCCESS;
  payload: {
    id: string;
    isRead: boolean;
    updatedAt: string;
  };
}

interface UpdateNotificationStatusFailureAction {
  type: typeof UPDATE_NOTIFICATION_STATUS_FAILURE;
  payload: {
    id: string;
    error: string;
  };
}

type NotificationActionTypes = 
  | UpdateNotificationStatusRequestAction
  | UpdateNotificationStatusSuccessAction
  | UpdateNotificationStatusFailureAction;

// Action Creators
export const updateNotificationStatus = (id: string, isRead: boolean): ThunkAction<
  Promise<void>,
  RootState,
  unknown,
  NotificationActionTypes
> => async (dispatch) => {
  try {
    dispatch({
      type: UPDATE_NOTIFICATION_STATUS_REQUEST,
      payload: { id, isRead }
    });
    
    const result = await updateNotificationReadStatus(id, isRead);
    
    dispatch({
      type: UPDATE_NOTIFICATION_STATUS_SUCCESS,
      payload: {
        id,
        isRead: result.is_read,
        updatedAt: result.updated_at
      }
    });
    
    // 未読カウンターの更新
    dispatch(updateUnreadCount(isRead ? -1 : 1));
    
  } catch (error) {
    dispatch({
      type: UPDATE_NOTIFICATION_STATUS_FAILURE,
      payload: {
        id,
        error: error.message
      }
    });
    
    throw error;
  }
};

// Reducer
const notificationsReducer = (state = initialState, action: NotificationActionTypes): NotificationsState => {
  switch (action.type) {
    case UPDATE_NOTIFICATION_STATUS_SUCCESS:
      return {
        ...state,
        items: state.items.map(notification => 
          notification.id === action.payload.id
            ? { ...notification, is_read: action.payload.isRead, updated_at: action.payload.updatedAt }
            : notification
        ),
        loading: {
          ...state.loading,
          [action.payload.id]: false
        },
        errors: {
          ...state.errors,
          [action.payload.id]: null
        }
      };
      
    case UPDATE_NOTIFICATION_STATUS_REQUEST:
      return {
        ...state,
        loading: {
          ...state.loading,
          [action.payload.id]: true
        }
      };
      
    case UPDATE_NOTIFICATION_STATUS_FAILURE:
      return {
        ...state,
        loading: {
          ...state.loading,
          [action.payload.id]: false
        },
        errors: {
          ...state.errors,
          [action.payload.id]: action.payload.error
        }
      };
      
    default:
      return state;
  }
};
