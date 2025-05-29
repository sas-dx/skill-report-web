# API仕様書：API-201 通知一覧取得API

## 1. 基本情報

- **API ID**: API-201
- **API名称**: 通知一覧取得API
- **概要**: ユーザー向けの通知・アラート情報の一覧を取得する
- **エンドポイント**: `/api/notifications`
- **HTTPメソッド**: GET
- **リクエスト形式**: URL パラメータ
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
| read_status | string | - | 既読状態フィルター | "all", "read", "unread"のいずれか<br>デフォルト："all" |
| page | number | - | ページ番号 | 1以上の整数<br>デフォルト：1 |
| size | number | - | 1ページあたりの件数 | 1～100の整数<br>デフォルト：10 |
| sort | string | - | ソート条件 | "date_desc", "date_asc", "priority_desc"のいずれか<br>デフォルト："date_desc" |
| from_date | string | - | 開始日 | YYYY-MM-DD形式 |
| to_date | string | - | 終了日 | YYYY-MM-DD形式 |

### 2.2 リクエスト例

```
GET /api/notifications?filter_type=certification&read_status=unread&page=1&size=10 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| notifications | array | 通知一覧 | 通知オブジェクトの配列 |
| total_count | number | 総件数 | フィルター条件に合致する全通知数 |
| page_info | object | ページング情報 | ページネーション情報 |

#### notifications 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| id | string | 通知ID | |
| type | string | 通知種別 | "system", "certification", "goal", "training", "other"のいずれか |
| priority | string | 重要度 | "high", "medium", "low"のいずれか |
| title | string | タイトル | |
| summary | string | 概要 | 通知の短い説明（一覧表示用） |
| date | string | 通知日時 | ISO 8601形式 |
| is_read | boolean | 既読状態 | true: 既読, false: 未読 |
| action_required | boolean | アクション要否 | true: 要アクション, false: 情報のみ |
| link | string | 関連リンク | 詳細画面へのリンクパス（任意） |

#### page_info オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| current_page | number | 現在のページ番号 | |
| page_size | number | 1ページあたりの件数 | |
| total_pages | number | 総ページ数 | |
| has_next | boolean | 次ページ有無 | |
| has_previous | boolean | 前ページ有無 | |

### 3.2 正常時レスポンス例

```json
{
  "notifications": [
    {
      "id": "notif_20250520001",
      "type": "certification",
      "priority": "high",
      "title": "資格Aの期限が近づいています",
      "summary": "資格Aの有効期限が2025年6月30日に到来します。更新手続きを行ってください。",
      "date": "2025-05-20T10:30:00+09:00",
      "is_read": false,
      "action_required": true,
      "link": "/certifications/details/cert001"
    },
    {
      "id": "notif_20250519001",
      "type": "goal",
      "priority": "medium",
      "title": "目標Bの進捗報告期限が近づいています",
      "summary": "目標Bの四半期進捗報告期限が2025年5月31日です。進捗状況を更新してください。",
      "date": "2025-05-19T09:15:00+09:00",
      "is_read": true,
      "action_required": true,
      "link": "/goals/progress/goal002"
    },
    {
      "id": "notif_20250518001",
      "type": "system",
      "priority": "low",
      "title": "システムメンテナンスのお知らせ",
      "summary": "2025年5月25日 23:00～翌2:00にシステムメンテナンスを実施します。",
      "date": "2025-05-18T14:00:00+09:00",
      "is_read": true,
      "action_required": false,
      "link": null
    }
  ],
  "total_count": 25,
  "page_info": {
    "current_page": 1,
    "page_size": 10,
    "total_pages": 3,
    "has_next": true,
    "has_previous": false
  }
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 通知閲覧権限なし |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "パラメータが不正です",
    "details": "filter_typeには'all', 'system', 'certification', 'goal', 'training', 'other'のいずれかを指定してください。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - 通知閲覧権限の確認
2. リクエストパラメータの検証
   - パラメータ形式チェック
   - 値の範囲チェック
3. 通知データの取得
   - ユーザーIDに紐づく通知の抽出
   - フィルター条件による絞り込み
   - ソート処理
   - ページング処理
4. レスポンスの生成
   - 通知データの整形
   - ページング情報の設定
5. レスポンス返却

### 4.2 フィルタリングルール

| フィルター種別 | 説明 | 適用条件 |
|--------------|------|---------|
| filter_type | 通知種別によるフィルタリング | 指定された種別に完全一致 |
| read_status | 既読状態によるフィルタリング | "read": is_read=true<br>"unread": is_read=false<br>"all": 条件なし |
| from_date | 開始日によるフィルタリング | 通知日時 >= from_date 00:00:00 |
| to_date | 終了日によるフィルタリング | 通知日時 <= to_date 23:59:59 |

### 4.3 ソートルール

| ソート条件 | 説明 |
|-----------|------|
| date_desc | 通知日時の降順（新しい順） |
| date_asc | 通知日時の昇順（古い順） |
| priority_desc | 重要度の降順（重要な順） |

### 4.4 パフォーマンス要件

- レスポンスタイム：平均300ms以内
- キャッシュ：ユーザー別に5分間
- 最大取得件数：1リクエストあたり100件まで

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-202](API仕様書_API-202.md) | 通知詳細取得API | 通知の詳細情報取得 |
| [API-203](API仕様書_API-203.md) | 通知状態更新API | 通知の既読状態更新 |
| [API-204](API仕様書_API-204.md) | 全通知既読API | 全通知の一括既読化 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| notifications | 通知情報 | 参照（R） |
| notification_reads | 通知既読状態 | 参照（R） |
| notification_settings | ユーザー通知設定 | 参照（R） |

### 5.3 注意事項・補足

- 通知は最大90日間保持、それ以前の通知は自動アーカイブ
- 通知種別ごとの表示制御はユーザー設定に基づく
- 重要度の高い通知は未読の場合、優先的に上位表示
- 通知数が多い場合はページングを活用
- 通知の詳細内容はAPI-202で取得

---

## 6. サンプルコード

### 6.1 リクエスト例（JavaScript/Fetch API）

```javascript
/**
 * 通知一覧を取得する関数
 * @param {Object} params - 検索条件パラメータ
 * @returns {Promise<Object>} 通知一覧データ
 */
async function fetchNotifications(params = {}) {
  // デフォルトパラメータ
  const defaultParams = {
    filter_type: 'all',
    read_status: 'all',
    page: 1,
    size: 10,
    sort: 'date_desc'
  };
  
  // パラメータのマージ
  const queryParams = { ...defaultParams, ...params };
  
  // URLパラメータの構築
  const queryString = Object.entries(queryParams)
    .filter(([_, value]) => value !== null && value !== undefined)
    .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
    .join('&');
  
  try {
    const response = await fetch(`https://api.example.com/api/notifications?${queryString}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`,
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error.message || '通知の取得に失敗しました');
    }
    
    return await response.json();
  } catch (error) {
    console.error('通知取得エラー:', error);
    throw error;
  }
}
```

### 6.2 通知一覧表示例（React）

```jsx
import React, { useState, useEffect } from 'react';
import { fetchNotifications } from '../api/notificationApi';

const NotificationList = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState({
    filter_type: 'all',
    read_status: 'all',
    page: 1,
    size: 10
  });
  const [pageInfo, setPageInfo] = useState({});
  
  // 通知データの取得
  useEffect(() => {
    const loadNotifications = async () => {
      try {
        setLoading(true);
        const result = await fetchNotifications(filter);
        setNotifications(result.notifications);
        setPageInfo(result.page_info);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    loadNotifications();
  }, [filter]);
  
  // フィルター変更ハンドラ
  const handleFilterChange = (name, value) => {
    setFilter(prev => ({
      ...prev,
      [name]: value,
      page: 1 // フィルター変更時は1ページ目に戻す
    }));
  };
  
  // ページ変更ハンドラ
  const handlePageChange = (newPage) => {
    setFilter(prev => ({
      ...prev,
      page: newPage
    }));
  };
  
  // 通知の優先度に応じたスタイルクラスを返す
  const getPriorityClass = (priority) => {
    switch (priority) {
      case 'high': return 'notification-high-priority';
      case 'medium': return 'notification-medium-priority';
      case 'low': return 'notification-low-priority';
      default: return '';
    }
  };
  
  if (loading) return <div className="loading">読み込み中...</div>;
  if (error) return <div className="error">エラー: {error}</div>;
  
  return (
    <div className="notification-container">
      {/* フィルターコントロール */}
      <div className="notification-filters">
        <select 
          value={filter.filter_type}
          onChange={(e) => handleFilterChange('filter_type', e.target.value)}
        >
          <option value="all">すべての種別</option>
          <option value="system">システム</option>
          <option value="certification">資格</option>
          <option value="goal">目標</option>
          <option value="training">研修</option>
          <option value="other">その他</option>
        </select>
        
        <select 
          value={filter.read_status}
          onChange={(e) => handleFilterChange('read_status', e.target.value)}
        >
          <option value="all">すべての状態</option>
          <option value="unread">未読のみ</option>
          <option value="read">既読のみ</option>
        </select>
      </div>
      
      {/* 通知一覧 */}
      <div className="notification-list">
        {notifications.length === 0 ? (
          <div className="no-notifications">通知はありません</div>
        ) : (
          notifications.map(notification => (
            <div 
              key={notification.id} 
              className={`notification-item ${!notification.is_read ? 'unread' : ''} ${getPriorityClass(notification.priority)}`}
            >
              <div className="notification-header">
                <span className="notification-type">{notification.type}</span>
                <span className="notification-date">{new Date(notification.date).toLocaleString()}</span>
              </div>
              <div className="notification-title">{notification.title}</div>
              <div className="notification-summary">{notification.summary}</div>
              {notification.action_required && (
                <div className="notification-action">アクションが必要です</div>
              )}
            </div>
          ))
        )}
      </div>
      
      {/* ページネーション */}
      {pageInfo.total_pages > 1 && (
        <div className="pagination">
          <button 
            disabled={!pageInfo.has_previous}
            onClick={() => handlePageChange(filter.page - 1)}
          >
            前へ
          </button>
          
          <span className="page-info">
            {filter.page} / {pageInfo.total_pages}
          </span>
          
          <button 
            disabled={!pageInfo.has_next}
            onClick={() => handlePageChange(filter.page + 1)}
          >
            次へ
          </button>
        </div>
      )}
    </div>
  );
};

export default NotificationList;
```

### 6.3 フィルタリング・ソート例（TypeScript）

```typescript
interface NotificationFilter {
  filter_type?: 'all' | 'system' | 'certification' | 'goal' | 'training' | 'other';
  read_status?: 'all' | 'read' | 'unread';
  page?: number;
  size?: number;
  sort?: 'date_desc' | 'date_asc' | 'priority_desc';
  from_date?: string;
  to_date?: string;
}

/**
 * 通知フィルターの状態を管理するカスタムフック
 */
function useNotificationFilter() {
  const [filter, setFilter] = useState<NotificationFilter>({
    filter_type: 'all',
    read_status: 'all',
    page: 1,
    size: 10,
    sort: 'date_desc'
  });
  
  // 単一フィルター項目の更新
  const updateFilter = (key: keyof NotificationFilter, value: any) => {
    setFilter(prev => ({
      ...prev,
      [key]: value,
      // フィルター条件変更時は1ページ目に戻す（ページ番号自体の変更時は除く）
      ...(key !== 'page' ? { page: 1 } : {})
    }));
  };
  
  // 日付範囲フィルターの設定
  const setDateRange = (fromDate: string | null, toDate: string | null) => {
    setFilter(prev => ({
      ...prev,
      from_date: fromDate || undefined,
      to_date: toDate || undefined,
      page: 1
    }));
  };
  
  // フィルターのリセット
  const resetFilter = () => {
    setFilter({
      filter_type: 'all',
      read_status: 'all',
      page: 1,
      size: 10,
      sort: 'date_desc'
    });
  };
  
  return {
    filter,
    updateFilter,
    setDateRange,
    resetFilter
  };
}
