// Polyfill for Fetch API (required for MSW)
import 'whatwg-fetch'

// Polyfill for TextEncoder/TextDecoder (required for MSW)
import { TextEncoder, TextDecoder } from 'util'
global.TextEncoder = TextEncoder
global.TextDecoder = TextDecoder

// Polyfill for Streams API (required for MSW)
import { ReadableStream, WritableStream, TransformStream } from 'web-streams-polyfill'
global.ReadableStream = ReadableStream
global.WritableStream = WritableStream
global.TransformStream = TransformStream

import '@testing-library/jest-dom'

// Mock Next.js router
jest.mock('next/router', () => ({
  useRouter() {
    return {
      route: '/',
      pathname: '/',
      query: {},
      asPath: '/',
      push: jest.fn(),
      pop: jest.fn(),
      reload: jest.fn(),
      back: jest.fn(),
      prefetch: jest.fn().mockResolvedValue(undefined),
      beforePopState: jest.fn(),
      events: {
        on: jest.fn(),
        off: jest.fn(),
        emit: jest.fn(),
      },
      isFallback: false,
    }
  },
}))

// Mock Next.js navigation
jest.mock('next/navigation', () => ({
  useRouter() {
    return {
      push: jest.fn(),
      replace: jest.fn(),
      prefetch: jest.fn(),
      back: jest.fn(),
      forward: jest.fn(),
      refresh: jest.fn(),
    }
  },
  useSearchParams() {
    return new URLSearchParams()
  },
  usePathname() {
    return '/'
  },
}))

// Mock environment variables
process.env.NODE_ENV = 'test'
process.env.DATABASE_URL = 'postgresql://test_user:test_password@localhost:5434/skill_report_test_db'
process.env.TEST_DATABASE_URL = 'postgresql://test_user:test_password@localhost:5434/skill_report_test_db'
process.env.JWT_SECRET = 'test-jwt-secret-for-testing'
process.env.JWT_EXPIRES_IN = '24h'

// Mock Next.js Web APIs
global.Request = class MockRequest {
  constructor(input, init = {}) {
    this.url = typeof input === 'string' ? input : input.url
    this.method = init.method || 'GET'
    this.headers = new Headers(init.headers)
    this.body = init.body
  }
  
  async json() {
    return JSON.parse(this.body || '{}')
  }
  
  async text() {
    return this.body || ''
  }
}

global.Response = class MockResponse {
  constructor(body, init = {}) {
    this.body = body
    this.status = init.status || 200
    this.statusText = init.statusText || 'OK'
    this.headers = new Headers(init.headers)
    this.ok = this.status >= 200 && this.status < 300
  }
  
  static json(data, init = {}) {
    return new MockResponse(JSON.stringify(data), {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        ...init.headers
      }
    })
  }
  
  async json() {
    return JSON.parse(this.body)
  }
  
  async text() {
    return this.body
  }
}

global.Headers = class MockHeaders {
  constructor(init = {}) {
    this.map = new Map()
    if (init) {
      Object.entries(init).forEach(([key, value]) => {
        this.map.set(key.toLowerCase(), value)
      })
    }
  }
  
  get(name) {
    return this.map.get(name.toLowerCase())
  }
  
  set(name, value) {
    this.map.set(name.toLowerCase(), value)
  }
  
  has(name) {
    return this.map.has(name.toLowerCase())
  }
  
  delete(name) {
    this.map.delete(name.toLowerCase())
  }
  
  entries() {
    return this.map.entries()
  }
}

// Global test utilities
global.fetch = jest.fn()

// Prisma Mock Setup
// Prismaクライアントのモックをセットアップ
require('./src/__mocks__/prisma')

// MSW Server Setup (Mock Service Worker)
// APIモックサーバーのセットアップ
// TODO: MSW v2はESM-onlyの依存関係が多く、Jestとの統合に課題があります
// 将来的にJestのESMサポートが改善されたら、以下のコメントを解除してください
/*
// Use require() instead of import to ensure polyfills are loaded first
const { server } = require('./src/__mocks__/server')

beforeAll(() => {
  // MSWサーバーを起動（未処理のリクエストを警告表示）
  server.listen({ onUnhandledRequest: 'warn' })
})

afterEach(() => {
  // 各テスト後にハンドラーをリセット
  server.resetHandlers()
  // モックをクリア
  jest.clearAllMocks()
})

afterAll(() => {
  // すべてのテスト終了後にサーバーをクローズ
  server.close()
})
*/

// MSW統合が完了するまでの暫定対応
afterEach(() => {
  // モックをクリア
  jest.clearAllMocks()
})
