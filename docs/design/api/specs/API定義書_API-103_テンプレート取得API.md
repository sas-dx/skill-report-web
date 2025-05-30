# API定義書：API-103 テンプレート取得API

## 1. 基本情報

- **API ID**: API-103
- **API名称**: テンプレート取得API
- **概要**: 作業実績一括登録用のテンプレートファイル（CSV/Excel）を取得する
- **エンドポイント**: `/api/work/bulk/template`
- **HTTPメソッド**: GET
- **リクエスト形式**: URL パラメータ
- **レスポンス形式**: ファイル（CSV/Excel）
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
| format | string | - | ファイル形式 | "csv"または"xlsx"<br>デフォルト："xlsx" |
| with_sample | boolean | - | サンプルデータ含有フラグ | デフォルト：false |
| project_id | string | - | プロジェクトID | 特定プロジェクト用テンプレート |

### 2.2 リクエスト例

```
GET /api/work/bulk/template?format=xlsx&with_sample=true HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| ヘッダ名 | 値 | 説明 |
|---------|-----|------|
| Content-Type | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet | Excel形式の場合 |
| Content-Type | text/csv | CSV形式の場合 |
| Content-Disposition | attachment; filename="work_record_template_YYYYMMDD.xlsx" | ファイル名指定（Excel） |
| Content-Disposition | attachment; filename="work_record_template_YYYYMMDD.csv" | ファイル名指定（CSV） |
| Content-Length | [ファイルサイズ] | ファイルサイズ（バイト） |

### 3.2 レスポンス内容

テンプレートファイルには以下の列が含まれます：

| 列名 | 説明 | データ型 | 必須 | 備考 |
|------|------|---------|------|------|
| プロジェクトID | プロジェクトの識別子 | 文字列 | ○ | 有効なプロジェクトIDを指定 |
| プロジェクト名 | プロジェクトの名称 | 文字列 | - | 参考情報（入力不要） |
| 作業日 | 作業を実施した日付 | 日付 | ○ | YYYY/MM/DD形式 |
| 作業内容 | 実施した作業の内容 | 文字列 | ○ | 1000文字以内 |
| 工数 | 作業に費やした時間 | 数値 | ○ | 0.5～8.0の範囲、0.5単位 |
| 備考 | 補足情報 | 文字列 | - | 500文字以内 |

### 3.3 サンプルデータ（with_sample=trueの場合）

テンプレートファイルには以下のようなサンプルデータが含まれます：

```
プロジェクトID,プロジェクト名,作業日,作業内容,工数,備考
PRJ001,スキル報告書システム開発,2025/05/20,要件定義,7.5,キックオフミーティング含む
PRJ002,社内研修,2025/05/21,新人研修,4.0,午後のみ
PRJ003,顧客サポート,2025/05/22,問い合わせ対応,8.0,緊急対応あり
```

### 3.4 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_FORMAT | 無効なファイル形式です | formatパラメータ不正 |
| 400 Bad Request | INVALID_PROJECT | 無効なプロジェクトIDです | project_idパラメータ不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | テンプレート取得権限なし |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.5 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_FORMAT",
    "message": "無効なファイル形式です",
    "details": "formatパラメータには'csv'または'xlsx'を指定してください。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - テンプレート取得権限の確認
2. リクエストパラメータの検証
   - format値の検証（csv/xlsx）
   - project_id指定時の存在確認
3. テンプレートファイルの生成
   - ヘッダー行の設定
   - サンプルデータの追加（with_sample=trueの場合）
   - プロジェクト固有情報の設定（project_id指定時）
4. ファイル形式の変換
   - 指定形式（CSV/Excel）に変換
5. レスポンスヘッダーの設定
   - Content-Type
   - Content-Disposition
   - Content-Length
6. ファイルのストリーミング返却

### 4.2 テンプレート生成ルール

- ヘッダー行は日本語表記
- 日付形式はYYYY/MM/DD形式で統一
- Excel形式の場合は以下の追加機能あり：
  - 各列のデータ型設定
  - 入力規則（バリデーション）設定
  - 条件付き書式（エラー表示）
  - プロジェクトIDの入力候補リスト
  - 説明シートの追加
- CSV形式の場合はUTF-8エンコーディング、BOM付き

### 4.3 パフォーマンス要件

- レスポンスタイム：平均500ms以内
- ファイルサイズ：最大100KB程度
- キャッシュ：1時間（プロジェクトマスタ更新時に無効化）

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-101](API仕様書_API-101.md) | 一括登録検証API | テンプレートを使用したデータ検証 |
| [API-102](API仕様書_API-102.md) | 一括登録実行API | テンプレートを使用したデータ登録 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| projects | プロジェクトマスタ | 参照（R） |
| template_settings | テンプレート設定 | 参照（R） |

### 5.3 注意事項・補足

- テンプレートのフォーマットは定期的に見直し・更新
- 古いバージョンのテンプレートも一定期間サポート
- Excel形式推奨（入力規則によるエラー低減効果）
- 大量データ入力時はCSV形式推奨（処理効率）
- 日本語を含むCSVファイルはUTF-8エンコーディング、BOM付きで出力

---

## 6. サンプルコード

### 6.1 テンプレートダウンロード例（JavaScript）

```javascript
// テンプレートダウンロードボタンのイベントハンドラ
document.getElementById('downloadTemplateButton').addEventListener('click', async () => {
  // フォーマット選択の取得
  const format = document.querySelector('input[name="format"]:checked').value;
  // サンプルデータ含有オプションの取得
  const withSample = document.getElementById('withSampleCheckbox').checked;
  
  try {
    // URLの構築
    const url = `https://api.example.com/api/work/bulk/template?format=${format}&with_sample=${withSample}`;
    
    // 認証トークンの取得
    const token = getAuthToken();
    
    // Fetch APIを使用したファイルダウンロード
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      // エラーレスポンスの処理
      const errorData = await response.json();
      throw new Error(errorData.error.message);
    }
    
    // ファイル名の取得
    const contentDisposition = response.headers.get('Content-Disposition');
    const filenameMatch = contentDisposition && contentDisposition.match(/filename="(.+)"/);
    const filename = filenameMatch ? filenameMatch[1] : `work_record_template.${format}`;
    
    // Blobとしてレスポンスを取得
    const blob = await response.blob();
    
    // ダウンロードリンクの作成
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(blob);
    downloadLink.download = filename;
    
    // リンクをクリックしてダウンロード開始
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    
    // 成功メッセージ表示
    showSuccessMessage(`テンプレートファイル（${format}形式）のダウンロードが完了しました。`);
    
  } catch (error) {
    console.error('テンプレートダウンロードエラー:', error);
    showErrorMessage(`テンプレートのダウンロードに失敗しました: ${error.message}`);
  }
});
```

### 6.2 プロジェクト固有テンプレート取得例（TypeScript）

```typescript
interface TemplateOptions {
  format: 'csv' | 'xlsx';
  withSample: boolean;
  projectId?: string;
}

/**
 * 作業実績登録用テンプレートをダウンロードする
 * @param options テンプレートオプション
 * @returns ダウンロード成功時はtrue、失敗時はfalse
 */
async function downloadWorkRecordTemplate(options: TemplateOptions): Promise<boolean> {
  try {
    // URLパラメータの構築
    const params = new URLSearchParams();
    params.append('format', options.format);
    params.append('with_sample', options.withSample.toString());
    if (options.projectId) {
      params.append('project_id', options.projectId);
    }
    
    const url = `${API_BASE_URL}/api/work/bulk/template?${params.toString()}`;
    
    // ファイルダウンロード処理
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error.message || '不明なエラーが発生しました');
    }
    
    // ファイル名の取得と調整
    let filename = 'work_record_template';
    if (options.projectId) {
      filename += `_${options.projectId}`;
    }
    filename += `_${formatDate(new Date(), 'YYYYMMDD')}.${options.format}`;
    
    // ダウンロード処理
    const blob = await response.blob();
    saveFile(blob, filename);
    
    return true;
  } catch (error) {
    console.error('テンプレートダウンロードエラー:', error);
    showErrorNotification(`テンプレートのダウンロードに失敗しました: ${error.message}`);
    return false;
  }
}

/**
 * Blobデータをファイルとして保存する
 * @param blob ファイルデータ
 * @param filename ファイル名
 */
function saveFile(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
```

### 6.3 サーバーサイド実装例（Node.js/Express）

```javascript
/**
 * 作業実績登録用テンプレートを生成して返却するAPI
 */
router.get('/work/bulk/template', authenticate, async (req, res) => {
  try {
    // リクエストパラメータの取得
    const format = req.query.format === 'csv' ? 'csv' : 'xlsx';
    const withSample = req.query.with_sample === 'true';
    const projectId = req.query.project_id;
    
    // 権限チェック
    if (!hasPermission(req.user, 'work_record.template.download')) {
      return res.status(403).json({
        error: {
          code: 'PERMISSION_DENIED',
          message: '権限がありません',
          details: 'テンプレート取得には作業実績登録権限が必要です。'
        }
      });
    }
    
    // プロジェクトIDの検証（指定されている場合）
    if (projectId) {
      const project = await Project.findById(projectId);
      if (!project) {
        return res.status(400).json({
          error: {
            code: 'INVALID_PROJECT',
            message: '無効なプロジェクトIDです',
            details: '指定されたプロジェクトIDは存在しません。'
          }
        });
      }
    }
    
    // テンプレートデータの構築
    const templateData = buildTemplateData(withSample, projectId);
    
    // ファイル名の設定
    const dateStr = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const filename = `work_record_template_${dateStr}.${format}`;
    
    // ファイル形式に応じた処理
    if (format === 'csv') {
      // CSVファイルの生成
      const csvContent = generateCSV(templateData);
      
      // レスポンスヘッダーの設定
      res.setHeader('Content-Type', 'text/csv; charset=utf-8');
      res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
      
      // BOM付きUTF-8でCSVを返却
      return res.send('\ufeff' + csvContent);
    } else {
      // Excelファイルの生成
      const workbook = generateExcel(templateData, projectId);
      const buffer = await workbook.xlsx.writeBuffer();
      
      // レスポンスヘッダーの設定
      res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
      res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
      
      // Excelファイルを返却
      return res.send(buffer);
    }
  } catch (error) {
    console.error('テンプレート生成エラー:', error);
    return res.status(500).json({
      error: {
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました',
        details: 'テンプレートの生成中にエラーが発生しました。'
      }
    });
  }
});
