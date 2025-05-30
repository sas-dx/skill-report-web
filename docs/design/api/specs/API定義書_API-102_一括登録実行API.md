# API定義書：API-102 一括登録実行API

## 1. 基本情報

- **API ID**: API-102
- **API名称**: 一括登録実行API
- **概要**: 検証済みの作業実績データを一括でデータベースに登録する
- **エンドポイント**: `/api/work/bulk`
- **HTTPメソッド**: POST
- **リクエスト形式**: JSON
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-WORK-BULK](画面設計書_SCR-WORK-BULK.md)
- **作成日**: 2025/05/28
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/28 初版作成

---

## 2. リクエスト仕様

### 2.1 リクエストパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| validation_id | string | ○ | 検証ID | API-101で取得した検証ID |
| register_all | boolean | - | 全件登録フラグ | デフォルト：false（エラーなしレコードのみ登録） |
| ignore_warnings | boolean | - | 警告無視フラグ | デフォルト：false（警告ありレコードも登録） |

### 2.2 リクエスト例

```json
{
  "validation_id": "val_20250528123456",
  "register_all": false,
  "ignore_warnings": true
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| bulk_register_id | string | 一括登録ID | 登録処理の識別ID |
| total_count | number | 総レコード数 | 登録対象の全レコード数 |
| success_count | number | 成功レコード数 | 登録に成功したレコード数 |
| error_count | number | 失敗レコード数 | 登録に失敗したレコード数 |
| result_details | array | 登録結果詳細 | 各レコードの登録結果 |

#### result_details 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| row_number | number | 行番号 | ファイル内の行番号（ヘッダー除く） |
| record_id | string | 登録レコードID | 登録成功時のみ設定 |
| project_id | string | プロジェクトID | |
| work_date | string | 作業日 | YYYY-MM-DD形式 |
| work_hours | number | 工数 | 小数点第1位まで（0.5時間単位） |
| status | string | 登録ステータス | "SUCCESS", "ERROR", "SKIPPED"のいずれか |
| message | string | 結果メッセージ | エラー時はエラー内容、成功時は空 |

### 3.2 正常時レスポンス例

```json
{
  "bulk_register_id": "bulk_20250528123456",
  "total_count": 100,
  "success_count": 98,
  "error_count": 2,
  "result_details": [
    {
      "row_number": 1,
      "record_id": "wrk_20250528001",
      "project_id": "PRJ001",
      "work_date": "2025-05-20",
      "work_hours": 8.0,
      "status": "SUCCESS",
      "message": ""
    },
    {
      "row_number": 2,
      "record_id": "wrk_20250528002",
      "project_id": "PRJ002",
      "work_date": "2025-05-21",
      "work_hours": 4.5,
      "status": "SUCCESS",
      "message": ""
    },
    {
      "row_number": 3,
      "project_id": "PRJ003",
      "work_date": "2025-05-22",
      "work_hours": 12.0,
      "status": "ERROR",
      "message": "作業時間は0.5～8.0の範囲で入力してください"
    },
    {
      "row_number": 4,
      "project_id": "INVALID",
      "work_date": "2025-05-23",
      "work_hours": 2.0,
      "status": "ERROR",
      "message": "存在しないプロジェクトIDです"
    }
  ]
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_VALIDATION_ID | 無効な検証IDです | 存在しない/期限切れの検証ID |
| 400 Bad Request | NO_VALID_RECORDS | 有効なレコードがありません | 登録可能なレコードなし |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 作業実績登録権限なし |
| 409 Conflict | DUPLICATE_RECORD | 重複するレコードが存在します | 既存データとの重複 |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |
| 503 Service Unavailable | SERVICE_UNAVAILABLE | サービスが一時的に利用できません | システム過負荷/メンテナンス中 |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_VALIDATION_ID",
    "message": "無効な検証IDです",
    "details": "検証IDの有効期限が切れているか、存在しません。再度ファイルをアップロードして検証を行ってください。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - 作業実績登録権限の確認
2. 検証IDの有効性確認
   - 検証IDの存在確認
   - 有効期限チェック（30分以内）
3. 検証結果の取得
   - 検証済みデータの取得
   - 登録対象レコードの抽出（register_allとignore_warningsに基づく）
4. データベース登録処理
   - トランザクション開始
   - レコード単位での登録処理
   - 重複チェック
   - エラー発生時の個別ハンドリング
   - トランザクション終了（コミットまたはロールバック）
5. 登録結果の生成
   - 登録結果サマリーの作成
   - 詳細結果の作成
6. 登録ログの記録
7. レスポンス返却

### 4.2 登録ルール

- エラーのないレコードのみ登録（register_all=falseの場合）
- 警告のあるレコードも登録（ignore_warnings=trueの場合）
- 同一ユーザー・同一日・同一プロジェクトの重複チェック
- 登録処理はレコード単位で実施し、一部エラーでも処理継続
- 登録結果は監査目的で保存

### 4.3 パフォーマンス要件

- 処理時間：1000件のデータで60秒以内
- タイムアウト：120秒
- 同時処理数：最大5リクエスト
- 登録上限：1回の処理で最大1,000件まで

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-101](API仕様書_API-101.md) | 一括登録検証API | 登録前の検証処理 |
| [API-103](API仕様書_API-103.md) | テンプレート取得API | 登録用テンプレート取得 |
| [API-041](API仕様書_API-041.md) | 作業実績取得API | 登録後のデータ参照 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| work_records | 作業実績データ | 作成（C） |
| projects | プロジェクトマスタ | 参照（R） |
| work_bulk_validation | 検証結果一時保存 | 参照/更新（R/U） |
| work_bulk_log | 一括登録履歴 | 作成（C） |

### 5.3 注意事項・補足

- 大量データ処理時はバックグラウンド処理を検討
- 登録処理は部分的に成功する可能性あり（一部成功、一部失敗）
- 登録履歴は管理者画面から参照可能
- 登録上限（1,000件）を超える場合は分割登録を推奨
- 登録処理の進捗状況は別APIで確認可能（大量データ時）

---

## 6. サンプルコード

### 6.1 リクエスト例（JavaScript/Fetch API）

```javascript
// 一括登録実行ボタンのイベントハンドラ
document.getElementById('registerButton').addEventListener('click', async () => {
  const validationId = getStoredValidationId(); // 保存済みの検証ID
  if (!validationId) {
    showErrorMessage('検証IDが見つかりません。再度ファイルをアップロードしてください。');
    return;
  }
  
  // 警告無視オプションの取得
  const ignoreWarnings = document.getElementById('ignoreWarningsCheckbox').checked;
  
  try {
    const response = await fetch('https://api.example.com/api/work/bulk', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        validation_id: validationId,
        register_all: false,
        ignore_warnings: ignoreWarnings
      })
    });
    
    const result = await response.json();
    if (response.ok) {
      // 登録成功時の処理
      displayRegistrationResults(result);
      showSuccessMessage(`${result.success_count}件のデータを登録しました。`);
    } else {
      // エラー処理
      showErrorMessage(result.error.message);
    }
  } catch (error) {
    console.error('API呼び出しエラー:', error);
    showErrorMessage('登録処理に失敗しました');
  }
});
```

### 6.2 登録結果表示例（JavaScript）

```javascript
function displayRegistrationResults(result) {
  const summaryElement = document.getElementById('registrationSummary');
  summaryElement.innerHTML = `
    <p>総レコード数: ${result.total_count}</p>
    <p>登録成功: ${result.success_count}</p>
    <p>登録失敗: ${result.error_count}</p>
  `;
  
  const tableElement = document.getElementById('registrationTable');
  tableElement.innerHTML = '<tr><th>行</th><th>プロジェクト</th><th>作業日</th><th>工数</th><th>状態</th><th>メッセージ</th></tr>';
  
  result.result_details.forEach(record => {
    const row = document.createElement('tr');
    row.className = record.status === 'ERROR' ? 'error-row' : 
                   (record.status === 'SKIPPED' ? 'warning-row' : 'success-row');
    
    row.innerHTML = `
      <td>${record.row_number}</td>
      <td>${record.project_id}</td>
      <td>${record.work_date}</td>
      <td>${record.work_hours}</td>
      <td>${record.status}</td>
      <td>${record.message || ''}</td>
    `;
    
    tableElement.appendChild(row);
  });
  
  // 登録完了後の操作ボタン表示
  document.getElementById('postRegistrationActions').style.display = 'block';
}
```

### 6.3 エラーハンドリング例（TypeScript）

```typescript
interface BulkRegistrationError {
  error: {
    code: string;
    message: string;
    details?: string;
  };
}

function handleRegistrationError(error: BulkRegistrationError): void {
  const errorCode = error.error.code;
  let userMessage = error.error.message;
  
  // エラーコードに応じた処理
  switch (errorCode) {
    case 'INVALID_VALIDATION_ID':
      // 検証IDが無効な場合は再検証を促す
      clearValidationData();
      showFileUploadForm();
      userMessage = '検証データの有効期限が切れました。ファイルを再アップロードしてください。';
      break;
      
    case 'NO_VALID_RECORDS':
      // 有効なレコードがない場合
      showValidationForm();
      userMessage = 'エラーのないレコードがありません。データを修正してから再度アップロードしてください。';
      break;
      
    case 'PERMISSION_DENIED':
      // 権限エラー
      redirectToHome();
      userMessage = '作業実績登録の権限がありません。管理者にお問い合わせください。';
      break;
      
    default:
      // その他のエラー
      console.error('登録エラー:', error);
      userMessage = 'エラーが発生しました。しばらく経ってから再度お試しください。';
  }
  
  showErrorMessage(userMessage);
}
