# API仕様書：API-202 通知詳細取得API

## 1. 基本情報

- **API ID**: API-202
- **API名称**: 通知詳細取得API
- **概要**: 指定された通知IDの詳細情報を取得する
- **エンドポイント**: `/api/notifications/{id}`
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

### 2.1 パスパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| id | string | ○ | 通知ID | 取得対象の通知の一意識別子 |

### 2.2 リクエスト例

```
GET /api/notifications/notif_20250520001 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| id | string | 通知ID | |
| type | string | 通知種別 | "system", "certification", "goal", "training", "other"のいずれか |
| priority | string | 重要度 | "high", "medium", "low"のいずれか |
| title | string | タイトル | |
| summary | string | 概要 | 通知の短い説明 |
| content | string | 詳細内容 | 通知の詳細内容（HTML形式可） |
| date | string | 通知日時 | ISO 8601形式 |
| is_read | boolean | 既読状態 | true: 既読, false: 未読 |
| action_required | boolean | アクション要否 | true: 要アクション, false: 情報のみ |
| action_deadline | string | アクション期限 | ISO 8601形式（任意） |
| action_type | string | アクション種別 | "update", "confirm", "submit"など（任意） |
| link | string | 関連リンク | 詳細画面へのリンクパス（任意） |
| related_items | array | 関連項目 | 関連する項目情報（任意） |
| attachments | array | 添付ファイル | 添付ファイル情報（任意） |
| created_at | string | 作成日時 | ISO 8601形式 |
| updated_at | string | 更新日時 | ISO 8601形式 |

#### related_items 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| id | string | 関連項目ID | |
| type | string | 関連項目種別 | "certification", "goal", "training"など |
| name | string | 関連項目名 | |
| link | string | 関連項目リンク | 関連項目へのリンクパス |

#### attachments 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| id | string | 添付ファイルID | |
| name | string | ファイル名 | |
| size | number | ファイルサイズ | バイト単位 |
| mime_type | string | MIMEタイプ | |
| url | string | ダウンロードURL | |

### 3.2 正常時レスポンス例

```json
{
  "id": "notif_20250520001",
  "type": "certification",
  "priority": "high",
  "title": "資格Aの期限が近づいています",
  "summary": "資格Aの有効期限が2025年6月30日に到来します。更新手続きを行ってください。",
  "content": "<p>資格Aの有効期限が2025年6月30日に到来します。</p><p>更新手続きを行うには、以下の手順に従ってください：</p><ol><li>更新申請書をダウンロード</li><li>必要事項を記入</li><li>上長の承認を得る</li><li>人事部に提出（6月15日締切）</li></ol><p>ご不明点は人事部（<a href='mailto:jinji@example.com'>jinji@example.com</a>）までお問い合わせください。</p>",
  "date": "2025-05-20T10:30:00+09:00",
  "is_read": false,
  "action_required": true,
  "action_deadline": "2025-06-15T23:59:59+09:00",
  "action_type": "submit",
  "link": "/certifications/details/cert001",
  "related_items": [
    {
      "id": "cert001",
      "type": "certification",
      "name": "資格A",
      "link": "/certifications/details/cert001"
    }
  ],
  "attachments": [
    {
      "id": "file001",
      "name": "更新申請書.pdf",
      "size": 258420,
      "mime_type": "application/pdf",
      "url": "/api/files/download/file001"
    },
    {
      "id": "file002",
      "name": "更新手続きガイド.pdf",
      "size": 524288,
      "mime_type": "application/pdf",
      "url": "/api/files/download/file002"
    }
  ],
  "created_at": "2025-05-20T10:30:00+09:00",
  "updated_at": "2025-05-20T10:30:00+09:00"
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | リクエストパラメータの形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 通知閲覧権限なし |
| 404 Not Found | NOTIFICATION_NOT_FOUND | 通知が見つかりません | 指定IDの通知が存在しない |
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
   - 通知閲覧権限の確認
2. パスパラメータの検証
   - 通知IDの形式チェック
3. 通知データの取得
   - 指定IDの通知レコード取得
   - ユーザーIDとの紐付け確認（他ユーザーの通知は参照不可）
4. 関連データの取得
   - 関連項目情報の取得
   - 添付ファイル情報の取得
5. レスポンスの生成
   - 通知データの整形
6. レスポンス返却

### 4.2 自動既読化処理

- 通知詳細取得時に自動的に既読状態に更新
- 既読状態の更新はバックグラウンドで非同期処理
- 既読状態の更新に失敗してもレスポンス返却には影響しない
- 既読状態の更新履歴はログに記録

### 4.3 パフォーマンス要件

- レスポンスタイム：平均200ms以内
- キャッシュ：ユーザー別に5分間（既読状態変更時に無効化）
- 添付ファイルURL：署名付きURLで30分間有効

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-201](API仕様書_API-201.md) | 通知一覧取得API | 通知一覧の取得 |
| [API-203](API仕様書_API-203.md) | 通知状態更新API | 通知の既読状態更新 |
| [API-204](API仕様書_API-204.md) | 全通知既読API | 全通知の一括既読化 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| notifications | 通知情報 | 参照（R） |
| notification_reads | 通知既読状態 | 参照/作成/更新（R/C/U） |
| notification_attachments | 添付ファイル情報 | 参照（R） |
| notification_related_items | 関連項目情報 | 参照（R） |

### 5.3 注意事項・補足

- 通知詳細取得時に自動的に既読状態に更新される
- 添付ファイルのダウンロードURLは署名付きで、30分間有効
- HTML形式のコンテンツはXSS対策済み（許可タグのみ使用可）
- 通知種別によって表示項目が異なる場合がある
- 関連項目へのアクセス権限がない場合は表示されない

---

## 6. サンプルコード

### 6.1 通知詳細取得例（JavaScript/Fetch API）

```javascript
/**
 * 通知詳細を取得する関数
 * @param {string} notificationId - 通知ID
 * @returns {Promise<Object>} 通知詳細データ
 */
async function fetchNotificationDetail(notificationId) {
  try {
    const response = await fetch(`https://api.example.com/api/notifications/${notificationId}`, {
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
    console.error('通知詳細取得エラー:', error);
    throw error;
  }
}
```

### 6.2 通知詳細表示例（React）

```jsx
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchNotificationDetail } from '../api/notificationApi';
import { formatDate } from '../utils/dateUtils';

const NotificationDetail = () => {
  const { id } = useParams();
  const [notification, setNotification] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const loadNotificationDetail = async () => {
      try {
        setLoading(true);
        const data = await fetchNotificationDetail(id);
        setNotification(data);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    loadNotificationDetail();
  }, [id]);
  
  // 通知の優先度に応じたスタイルクラスを返す
  const getPriorityClass = (priority) => {
    switch (priority) {
      case 'high': return 'notification-high-priority';
      case 'medium': return 'notification-medium-priority';
      case 'low': return 'notification-low-priority';
      default: return '';
    }
  };
  
  // 通知種別に応じたアイコンを返す
  const getTypeIcon = (type) => {
    switch (type) {
      case 'system': return 'system-icon';
      case 'certification': return 'certification-icon';
      case 'goal': return 'goal-icon';
      case 'training': return 'training-icon';
      default: return 'info-icon';
    }
  };
  
  if (loading) return <div className="loading">読み込み中...</div>;
  if (error) return <div className="error">エラー: {error}</div>;
  if (!notification) return <div className="not-found">通知が見つかりません</div>;
  
  return (
    <div className="notification-detail-container">
      <div className="notification-header">
        <Link to="/notifications" className="back-link">← 通知一覧に戻る</Link>
        <div className={`notification-priority ${getPriorityClass(notification.priority)}`}>
          {notification.priority === 'high' ? '重要' : 
           notification.priority === 'medium' ? '中程度' : '低'}
        </div>
      </div>
      
      <div className="notification-meta">
        <div className={`notification-type ${getTypeIcon(notification.type)}`}>
          {notification.type === 'system' ? 'システム' : 
           notification.type === 'certification' ? '資格' : 
           notification.type === 'goal' ? '目標' : 
           notification.type === 'training' ? '研修' : 'その他'}
        </div>
        <div className="notification-date">
          {formatDate(notification.date, 'YYYY年MM月DD日 HH:mm')}
        </div>
      </div>
      
      <h1 className="notification-title">{notification.title}</h1>
      
      <div className="notification-summary">{notification.summary}</div>
      
      <div 
        className="notification-content"
        dangerouslySetInnerHTML={{ __html: notification.content }}
      />
      
      {notification.action_required && (
        <div className="notification-action-required">
          <h3>必要なアクション</h3>
          <div className="action-type">
            {notification.action_type === 'update' ? '更新' : 
             notification.action_type === 'confirm' ? '確認' : 
             notification.action_type === 'submit' ? '提出' : 'アクション'}
          </div>
          {notification.action_deadline && (
            <div className="action-deadline">
              期限: {formatDate(notification.action_deadline, 'YYYY年MM月DD日')}
            </div>
          )}
          {notification.link && (
            <Link to={notification.link} className="action-link">
              アクションを実行する →
            </Link>
          )}
        </div>
      )}
      
      {notification.related_items && notification.related_items.length > 0 && (
        <div className="related-items">
          <h3>関連項目</h3>
          <ul>
            {notification.related_items.map(item => (
              <li key={item.id}>
                <Link to={item.link}>
                  {item.name} ({item.type})
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}
      
      {notification.attachments && notification.attachments.length > 0 && (
        <div className="attachments">
          <h3>添付ファイル</h3>
          <ul>
            {notification.attachments.map(file => (
              <li key={file.id} className="attachment-item">
                <a 
                  href={file.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="attachment-link"
                >
                  {file.name} ({(file.size / 1024).toFixed(1)} KB)
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default NotificationDetail;
```

### 6.3 添付ファイルダウンロード例（TypeScript）

```typescript
interface Attachment {
  id: string;
  name: string;
  size: number;
  mime_type: string;
  url: string;
}

/**
 * 添付ファイルをダウンロードする関数
 * @param attachment 添付ファイル情報
 * @returns ダウンロード成功時はtrue、失敗時はfalse
 */
async function downloadAttachment(attachment: Attachment): Promise<boolean> {
  try {
    // ファイルのダウンロード
    const response = await fetch(attachment.url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`
      }
    });
    
    if (!response.ok) {
      throw new Error('ファイルのダウンロードに失敗しました');
    }
    
    // Blobとしてレスポンスを取得
    const blob = await response.blob();
    
    // ダウンロードリンクの作成
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = attachment.name;
    document.body.appendChild(a);
    
    // リンクをクリックしてダウンロード開始
    a.click();
    
    // 後処理
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    return true;
  } catch (error) {
    console.error('ファイルダウンロードエラー:', error);
    showErrorMessage(`ファイルのダウンロードに失敗しました: ${error.message}`);
    return false;
  }
}
