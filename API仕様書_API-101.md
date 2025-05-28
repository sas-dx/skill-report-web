# API仕様書：API-101 一括登録検証API

## 1. 基本情報

- **API ID**: API-101
- **API名称**: 一括登録検証API
- **概要**: アップロードされたCSV/Excelファイルの内容を検証し、登録前の確認データを返却する
- **エンドポイント**: `/api/work/bulk/validate`
- **HTTPメソッド**: POST
- **リクエスト形式**: multipart/form-data
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
| file | File | ○ | アップロードファイル | CSV(.csv)またはExcel(.xlsx)形式<br>最大サイズ：10MB |
| validate_only | boolean | - | 検証のみ実施フラグ | デフォルト：true |

### 2.2 リクエスト例

```
POST /api/work/bulk/validate HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="work_records.xlsx"
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

(バイナリデータ)
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="validate_only"

true
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| validation_id | string | 検証ID | 一括登録実行時に使用するID |
| total_count | number | 総レコード数 | ファイル内の全レコード数 |
| valid_count | number | 有効レコード数 | 検証に合格したレコード数 |
| error_count | number | エラーレコード数 | 検証に失敗したレコード数 |
| validation_result | array | 検証結果詳細 | 各レコードの検証結果 |

#### validation_result 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| row_number | number | 行番号 | ファイル内の行番号（ヘッダー除く） |
| project_id | string | プロジェクトID | |
| project_name | string | プロジェクト名 | |
| work_date | string | 作業日 | YYYY-MM-DD形式 |
| work_content | string | 作業内容 | |
| work_hours | number | 工数 | 小数点第1位まで（0.5時間単位） |
| status | string | 検証ステータス | "OK", "ERROR"のいずれか |
| errors | array | エラー内容 | エラーがある場合のみ |

#### errors 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| field | string | エラー項目 | エラーが発生した項目名 |
| code | string | エラーコード | エラー種別を示すコード |
| message | string | エラーメッセージ | 人間可読なエラー内容 |

### 3.2 正常時レスポンス例

```json
{
  "validation_id": "val_20250528123456",
  "total_count": 100,
  "valid_count": 98,
  "error_count": 2,
  "validation_result": [
    {
      "row_number": 1,
      "project_id": "PRJ001",
      "project_name": "スキル報告書システム開発",
      "work_date": "2025-05-20",
      "work_content": "要件定義",
      "work_hours": 8.0,
      "status": "OK"
    },
    {
      "row_number": 2,
      "project_id": "PRJ002",
      "project_name": "社内研修",
      "work_date": "2025-05-21",
      "work_content": "新人研修",
      "work_hours": 4.5,
      "status": "OK"
    },
    {
      "row_number": 3,
      "project_id": "PRJ003",
      "project_name": "顧客サポート",
      "work_date": "2025-05-22",
      "work_content": "問い合わせ対応",
      "work_hours": 12.0,
      "status": "ERROR",
      "errors": [
        {
          "field": "work_hours",
          "code": "INVALID_HOURS",
          "message": "作業時間は0.5～8.0の範囲で入力してください"
        }
      ]
    },
    {
      "row_number": 4,
      "project_id": "INVALID",
      "project_name": "不明プロジェクト",
      "work_date": "2025-05-23",
      "work_content": "テスト",
      "work_hours": 2.0,
      "status": "ERROR",
      "errors": [
        {
          "field": "project_id",
          "code": "INVALID_PROJECT",
          "message": "存在しないプロジェクトIDです"
        }
      ]
    }
  ]
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_FILE_FORMAT | 対応していないファイル形式です | CSV/Excel以外のファイル |
| 400 Bad Request | FILE_TOO_LARGE | ファイルサイズが上限を超えています | 10MBを超えるファイル |
| 400 Bad Request | EMPTY_FILE | ファイルが空です | データが含まれていないファイル |
| 400 Bad Request | INVALID_HEADER | ヘッダー行が不正です | テンプレートと異なるヘッダー |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 作業実績登録権限なし |
| 413 Payload Too Large | FILE_TOO_LARGE | ファイルサイズが上限を超えています | 10MBを超えるファイル |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_FILE_FORMAT",
    "message": "対応していないファイル形式です",
    "details": "アップロードできるのはCSV(.csv)またはExcel(.xlsx)ファイルのみです。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - 作業実績登録権限の確認
2. アップロードファイルの基本検証
   - ファイル形式チェック（CSV/Excel）
   - ファイルサイズチェック（10MB以下）
   - ヘッダー行の検証
3. データ内容の検証
   - 必須項目チェック
   - データ型・形式チェック
   - 業務ルールチェック（日付範囲、工数上限など）
   - マスタ整合性チェック（プロジェクトIDなど）
4. 検証結果の生成
   - 検証IDの発行
   - 検証結果の一時保存（30分間有効）
5. レスポンス返却

### 4.2 検証ルール

| 項目 | 検証内容 | エラーコード |
|------|---------|------------|
| プロジェクトID | 必須、マスタに存在 | REQUIRED_FIELD, INVALID_PROJECT |
| 作業日 | 必須、日付形式(YYYY-MM-DD)、過去1年以内 | REQUIRED_FIELD, INVALID_DATE_FORMAT, DATE_OUT_OF_RANGE |
| 作業内容 | 必須、1000文字以内 | REQUIRED_FIELD, TEXT_TOO_LONG |
| 工数 | 必須、数値、0.5～8.0の範囲、0.5単位 | REQUIRED_FIELD, INVALID_NUMBER, INVALID_HOURS |

### 4.3 パフォーマンス要件

- 処理時間：1000件のデータで30秒以内
- タイムアウト：60秒
- 同時処理数：最大10リクエスト
- 検証結果の保持期間：30分

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-102](API仕様書_API-102.md) | 一括登録実行API | 検証後の登録処理 |
| [API-103](API仕様書_API-103.md) | テンプレート取得API | 登録用テンプレート取得 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| projects | プロジェクトマスタ | 参照（R） |
| work_bulk_validation | 検証結果一時保存 | 作成（C） |

### 5.3 注意事項・補足

- 検証のみで実際のデータ登録は行わない
- 検証IDは30分間有効、期限切れ後は再検証が必要
- 大量データ処理時はタイムアウトに注意
- 検証エラーがあっても、エラーのない行は登録可能
- 日本語を含むCSVファイルはUTF-8エンコーディングを推奨

---

## 6. サンプルコード

### 6.1 リクエスト例（JavaScript/FormData）

```javascript
// ファイル選択イベントハンドラ
document.getElementById('fileInput').addEventListener('change', async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  
  const formData = new FormData();
  formData.append('file', file);
  formData.append('validate_only', 'true');
  
  try {
    const response = await fetch('https://api.example.com/api/work/bulk/validate', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`
      },
      body: formData
    });
    
    const result = await response.json();
    if (response.ok) {
      // 検証成功時の処理
      displayValidationResults(result);
      storeValidationId(result.validation_id);
    } else {
      // エラー処理
      showErrorMessage(result.error.message);
    }
  } catch (error) {
    console.error('API呼び出しエラー:', error);
    showErrorMessage('ファイルのアップロードに失敗しました');
  }
});
```

### 6.2 検証結果表示例（JavaScript）

```javascript
function displayValidationResults(result) {
  const summaryElement = document.getElementById('validationSummary');
  summaryElement.innerHTML = `
    <p>総レコード数: ${result.total_count}</p>
    <p>有効レコード数: ${result.valid_count}</p>
    <p>エラーレコード数: ${result.error_count}</p>
  `;
  
  const tableElement = document.getElementById('validationTable');
  tableElement.innerHTML = '<tr><th>行</th><th>プロジェクト</th><th>作業日</th><th>作業内容</th><th>工数</th><th>状態</th></tr>';
  
  result.validation_result.forEach(record => {
    const row = document.createElement('tr');
    row.className = record.status === 'ERROR' ? 'error-row' : '';
    
    row.innerHTML = `
      <td>${record.row_number}</td>
      <td>${record.project_name}</td>
      <td>${record.work_date}</td>
      <td>${record.work_content}</td>
      <td>${record.work_hours}</td>
      <td>${record.status}</td>
    `;
    
    if (record.errors && record.errors.length > 0) {
      const errorCell = document.createElement('td');
      errorCell.className = 'error-message';
      errorCell.textContent = record.errors.map(e => e.message).join(', ');
      row.appendChild(errorCell);
    }
    
    tableElement.appendChild(row);
  });
  
  // 検証完了後、登録ボタンを有効化
  document.getElementById('registerButton').disabled = result.valid_count === 0;
}
