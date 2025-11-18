/**
 * APIレスポンス検証ヘルパー
 *
 * API Route Handlerのレスポンスを検証するためのヘルパー関数
 */

/**
 * 標準的なAPIレスポンス形式
 */
export interface StandardApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
  timestamp?: string
}

/**
 * レスポンスのステータスコードとボディを取得
 */
export async function getResponseData<T = any>(
  response: Response
): Promise<{ status: number; data: StandardApiResponse<T> }> {
  const status = response.status
  const data = await response.json()
  return { status, data }
}

/**
 * 成功レスポンスの基本検証
 */
export function expectSuccessResponse<T = any>(
  response: Response,
  data: StandardApiResponse<T>
) {
  expect(response.status).toBe(200)
  expect(data.success).toBe(true)
  expect(data).toHaveProperty('data')
  expect(data).toHaveProperty('timestamp')
}

/**
 * エラーレスポンスの基本検証
 */
export function expectErrorResponse(
  response: Response,
  data: StandardApiResponse,
  expectedStatus: number = 400
) {
  expect(response.status).toBe(expectedStatus)
  expect(data.success).toBe(false)
  expect(data).toHaveProperty('error')
}

/**
 * 認証エラーレスポンスの検証
 */
export function expectUnauthorizedResponse(
  response: Response,
  data: StandardApiResponse
) {
  expectErrorResponse(response, data, 401)
}

/**
 * 404エラーレスポンスの検証
 */
export function expectNotFoundResponse(
  response: Response,
  data: StandardApiResponse
) {
  expectErrorResponse(response, data, 404)
}

/**
 * バリデーションエラーレスポンスの検証
 */
export function expectValidationErrorResponse(
  response: Response,
  data: StandardApiResponse
) {
  expectErrorResponse(response, data, 400)
}

/**
 * サーバーエラーレスポンスの検証
 */
export function expectServerErrorResponse(
  response: Response,
  data: StandardApiResponse
) {
  expectErrorResponse(response, data, 500)
}

/**
 * レスポンスデータが配列であることを検証
 */
export function expectArrayResponse<T = any>(
  data: StandardApiResponse<T[]>
): asserts data is StandardApiResponse<T[]> {
  expect(data.data).toBeDefined()
  expect(Array.isArray(data.data)).toBe(true)
}

/**
 * レスポンスデータが指定された長さの配列であることを検証
 */
export function expectArrayResponseWithLength<T = any>(
  data: StandardApiResponse<T[]>,
  length: number
) {
  expectArrayResponse(data)
  expect(data.data).toHaveLength(length)
}

/**
 * レスポンスデータが空配列であることを検証
 */
export function expectEmptyArrayResponse<T = any>(
  data: StandardApiResponse<T[]>
) {
  expectArrayResponseWithLength(data, 0)
}

/**
 * レスポンスデータが特定のプロパティを持つことを検証
 */
export function expectResponseDataToHaveProperties(
  data: StandardApiResponse,
  properties: string[]
) {
  expect(data.data).toBeDefined()
  properties.forEach((prop) => {
    expect(data.data).toHaveProperty(prop)
  })
}

/**
 * レスポンスタイムスタンプが妥当な形式であることを検証
 */
export function expectValidTimestamp(data: StandardApiResponse) {
  if (data.timestamp) {
    expect(typeof data.timestamp).toBe('string')
    // ISO 8601形式のチェック
    expect(data.timestamp).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/)
  }
}

/**
 * 完全な成功レスポンスの検証（ステータス + 構造 + タイムスタンプ）
 */
export async function expectCompleteSuccessResponse<T = any>(
  response: Response,
  expectedProperties?: string[]
): Promise<StandardApiResponse<T>> {
  const { status, data } = await getResponseData<T>(response)

  expect(status).toBe(200)
  expect(data.success).toBe(true)
  expect(data).toHaveProperty('data')
  expect(data).toHaveProperty('timestamp')
  expectValidTimestamp(data)

  if (expectedProperties) {
    expectResponseDataToHaveProperties(data, expectedProperties)
  }

  return data
}

/**
 * ページネーション情報を含むレスポンスの検証
 */
export interface PaginatedResponse<T = any> {
  items: T[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

export function expectPaginatedResponse<T = any>(
  data: StandardApiResponse<PaginatedResponse<T>>
) {
  expect(data.data).toBeDefined()
  expect(data.data).toHaveProperty('items')
  expect(data.data).toHaveProperty('total')
  expect(data.data).toHaveProperty('page')
  expect(data.data).toHaveProperty('pageSize')
  expect(data.data).toHaveProperty('totalPages')
  expect(Array.isArray(data.data.items)).toBe(true)
  expect(typeof data.data.total).toBe('number')
  expect(typeof data.data.page).toBe('number')
  expect(typeof data.data.pageSize).toBe('number')
  expect(typeof data.data.totalPages).toBe('number')
}

/**
 * 作成成功レスポンスの検証（201 Created）
 */
export async function expectCreatedResponse<T = any>(
  response: Response,
  expectedProperties?: string[]
): Promise<StandardApiResponse<T>> {
  const { status, data } = await getResponseData<T>(response)

  expect(status).toBe(201)
  expect(data.success).toBe(true)
  expect(data).toHaveProperty('data')

  if (expectedProperties) {
    expectResponseDataToHaveProperties(data, expectedProperties)
  }

  return data
}

/**
 * 更新成功レスポンスの検証（200 OK）
 */
export async function expectUpdatedResponse<T = any>(
  response: Response
): Promise<StandardApiResponse<T>> {
  return expectCompleteSuccessResponse<T>(response)
}

/**
 * 削除成功レスポンスの検証（200 OK または 204 No Content）
 */
export async function expectDeletedResponse(response: Response) {
  expect([200, 204]).toContain(response.status)

  if (response.status === 200) {
    const data = await response.json()
    expect(data.success).toBe(true)
  }
}
