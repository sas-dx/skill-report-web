import { setupServer } from 'msw/node'
import { handlers } from './handlers'

/**
 * MSW v2 テスト用サーバー
 * Node.js環境（Jest）で使用
 */
export const server = setupServer(...handlers)
