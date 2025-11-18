/**
 * 統合テスト用アサーションヘルパー関数
 * 共通のアサーションロジックを提供し、テストコードの可読性と保守性を向上
 */

/**
 * ISO8601形式の日付文字列かチェック
 * @param dateString チェックする日付文字列
 * @returns ISO8601形式の場合true
 */
export function isISO8601(dateString: string | null | undefined): boolean {
  if (!dateString) return false
  return /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z?$/.test(dateString)
}

/**
 * APIレスポンスの基本構造を検証
 * @param responseData レスポンスデータ
 * @param expectedSuccess 期待される成功フラグ
 */
export function assertResponseStructure(
  responseData: any,
  expectedSuccess: boolean = true
) {
  expect(responseData).toHaveProperty('success')
  expect(responseData.success).toBe(expectedSuccess)

  if (expectedSuccess) {
    expect(responseData).toHaveProperty('data')
  } else {
    expect(responseData).toHaveProperty('error')
    expect(responseData.error).toHaveProperty('code')
    expect(responseData.error).toHaveProperty('message')
  }
}

/**
 * エラーレスポンスの構造を検証
 * @param responseData レスポンスデータ
 * @param expectedErrorCode 期待されるエラーコード
 * @param expectedStatus 期待されるHTTPステータスコード
 */
export function assertErrorResponse(
  response: Response,
  responseData: any,
  expectedErrorCode: string,
  expectedStatus: number
) {
  expect(response.status).toBe(expectedStatus)
  expect(responseData.success).toBe(false)
  expect(responseData.error.code).toBe(expectedErrorCode)
}

/**
 * ページネーション情報の構造を検証
 * @param pagination ページネーション情報
 * @param expectedLimit 期待されるlimit値
 * @param expectedOffset 期待されるoffset値
 */
export function assertPaginationStructure(
  pagination: any,
  expectedLimit?: number,
  expectedOffset?: number
) {
  expect(pagination).toHaveProperty('limit')
  expect(pagination).toHaveProperty('offset')
  expect(pagination).toHaveProperty('hasMore')

  if (expectedLimit !== undefined) {
    expect(pagination.limit).toBe(expectedLimit)
  }

  if (expectedOffset !== undefined) {
    expect(pagination.offset).toBe(expectedOffset)
  }

  expect(typeof pagination.hasMore).toBe('boolean')
}

/**
 * 日付フィールドがISO8601形式であることを検証
 * @param obj オブジェクト
 * @param dateFields 検証する日付フィールド名の配列
 */
export function assertDateFieldsISO8601(
  obj: any,
  dateFields: string[]
) {
  dateFields.forEach(field => {
    if (obj[field] !== null && obj[field] !== undefined) {
      expect(isISO8601(obj[field])).toBe(true)
    }
  })
}

/**
 * 配列の各要素が指定されたプロパティを持つことを検証
 * @param array 検証する配列
 * @param requiredProperties 必須プロパティの配列
 */
export function assertArrayItemsHaveProperties(
  array: any[],
  requiredProperties: string[]
) {
  array.forEach(item => {
    requiredProperties.forEach(prop => {
      expect(item).toHaveProperty(prop)
    })
  })
}

/**
 * サマリー情報の構造を検証（通知、レポート等で使用）
 * @param summary サマリー情報
 * @param expectedFields 期待されるフィールド配列
 */
export function assertSummaryStructure(
  summary: any,
  expectedFields: string[] = ['total']
) {
  expectedFields.forEach(field => {
    expect(summary).toHaveProperty(field)
    expect(typeof summary[field]).toBe('number')
  })
}

/**
 * バリデーションエラーレスポンスの構造を検証
 * @param responseData レスポンスデータ
 * @param expectedFieldErrors 期待されるフィールドエラー
 */
export function assertValidationError(
  response: Response,
  responseData: any,
  expectedFieldErrors?: Array<{ field: string; message?: string }>
) {
  expect(response.status).toBe(400)
  expect(responseData.success).toBe(false)
  expect(responseData.error.code).toBe('VALIDATION_ERROR')
  expect(responseData.error.details).toBeDefined()
  expect(Array.isArray(responseData.error.details)).toBe(true)

  if (expectedFieldErrors) {
    expectedFieldErrors.forEach(expectedError => {
      const matchingError = responseData.error.details.find(
        (detail: any) => detail.field === expectedError.field
      )
      expect(matchingError).toBeDefined()

      if (expectedError.message) {
        expect(matchingError.message).toBe(expectedError.message)
      }
    })
  }
}

/**
 * 認証エラーレスポンスの検証
 * @param response レスポンス
 * @param responseData レスポンスデータ
 */
export function assertAuthenticationError(
  response: Response,
  responseData: any
) {
  assertErrorResponse(response, responseData, 'AUTHENTICATION_ERROR', 401)
}

/**
 * 認可エラーレスポンスの検証
 * @param response レスポンス
 * @param responseData レスポンスデータ
 */
export function assertAuthorizationError(
  response: Response,
  responseData: any
) {
  assertErrorResponse(response, responseData, 'AUTHORIZATION_ERROR', 403)
}

/**
 * Not Foundエラーレスポンスの検証
 * @param response レスポンス
 * @param responseData レスポンスデータ
 */
export function assertNotFoundError(
  response: Response,
  responseData: any
) {
  assertErrorResponse(response, responseData, 'NOT_FOUND', 404)
}

/**
 * ソート順を検証（降順）
 * @param items アイテム配列
 * @param fieldGetter フィールド取得関数
 */
export function assertDescendingOrder<T>(
  items: T[],
  fieldGetter: (item: T) => any
) {
  for (let i = 0; i < items.length - 1; i++) {
    const current = fieldGetter(items[i])
    const next = fieldGetter(items[i + 1])
    expect(current >= next).toBe(true)
  }
}

/**
 * ソート順を検証（昇順）
 * @param items アイテム配列
 * @param fieldGetter フィールド取得関数
 */
export function assertAscendingOrder<T>(
  items: T[],
  fieldGetter: (item: T) => any
) {
  for (let i = 0; i < items.length - 1; i++) {
    const current = fieldGetter(items[i])
    const next = fieldGetter(items[i + 1])
    expect(current <= next).toBe(true)
  }
}

/**
 * オブジェクトが必須フィールドを持つことを検証
 * @param obj 検証するオブジェクト
 * @param requiredFields 必須フィールド配列
 */
export function assertRequiredFields(
  obj: any,
  requiredFields: string[]
) {
  requiredFields.forEach(field => {
    expect(obj).toHaveProperty(field)
    expect(obj[field]).not.toBeNull()
    expect(obj[field]).not.toBeUndefined()
  })
}

/**
 * 成功レスポンスの検証（201 Created）
 * @param response レスポンス
 * @param responseData レスポンスデータ
 */
export function assertCreatedResponse(
  response: Response,
  responseData: any
) {
  expect(response.status).toBe(201)
  assertResponseStructure(responseData, true)
}

/**
 * 成功レスポンスの検証（200 OK）
 * @param response レスポンス
 * @param responseData レスポンスデータ
 */
export function assertSuccessResponse(
  response: Response,
  responseData: any
) {
  expect(response.status).toBe(200)
  assertResponseStructure(responseData, true)
}
