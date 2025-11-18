# MSW（Mock Service Worker）個別使用例

このドキュメントでは、MSW v2を個別のテストファイルで使用する方法を説明します。

## 📋 背景

現在、MSW v2はESM-onlyの依存関係が多く、Jestのグローバルセットアップ（`jest.setup.js`）での統合に課題があります。そのため、MSWが必要なテストでは**個別にセットアップ**する方法を推奨します。

## 🎯 使用ケース

MSWは以下の場合に有効です：

1. **外部API呼び出しのモック**
   - fetch()を使った外部サービスとの通信
   - クライアントサイドでのAPI呼び出し

2. **Next.js Client Componentのテスト**
   - useEffect内でのfetch処理
   - SWR/React Queryを使用したデータフェッチ

3. **統合テスト**
   - 複数のコンポーネント間のAPI通信
   - E2Eテストに近い統合テスト

> **注意**: Next.js Route HandlersやServer Componentsのテストには、**Prismaモックを推奨**します。

## 📝 基本的な使用方法

### Step 1: ハンドラーのインポート

既存のハンドラー（`src/__mocks__/handlers.ts`）を使用できます：

```typescript
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'

// 既存のハンドラーをインポート（オプション）
// import { handlers } from '@/__mocks__/handlers'
```

### Step 2: テストファイルでサーバーをセットアップ

```typescript
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'

// MSWサーバーをセットアップ
const server = setupServer(
  // このテスト専用のハンドラーを定義
  http.get('/api/users', () => {
    return HttpResponse.json({
      success: true,
      data: [
        { id: 1, name: 'ユーザー1' },
        { id: 2, name: 'ユーザー2' },
      ],
    })
  })
)

// テスト前後のライフサイクル
beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

### Step 3: テストを記述

```typescript
describe('ユーザー一覧コンポーネント', () => {
  it('APIからユーザーデータを取得して表示する', async () => {
    // Arrange: コンポーネントをレンダリング
    render(<UserList />)

    // Act: データの読み込みを待つ
    await waitFor(() => {
      expect(screen.getByText('ユーザー1')).toBeInTheDocument()
    })

    // Assert: データが表示されることを確認
    expect(screen.getByText('ユーザー2')).toBeInTheDocument()
  })
})
```

## 💡 実践例

### 例1: 外部API呼び出しのモック

```typescript
/**
 * 外部天気APIを呼び出すサービス関数のテスト
 */
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'
import { getWeatherData } from '@/lib/services/weather'

const server = setupServer(
  http.get('https://api.weather.example.com/current', () => {
    return HttpResponse.json({
      temperature: 25,
      condition: 'sunny',
      humidity: 60,
    })
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('天気データ取得', () => {
  it('外部APIから天気データを取得できる', async () => {
    const data = await getWeatherData('Tokyo')

    expect(data.temperature).toBe(25)
    expect(data.condition).toBe('sunny')
  })

  it('APIエラー時に適切にハンドリングする', async () => {
    // このテストだけエラーレスポンスを返す
    server.use(
      http.get('https://api.weather.example.com/current', () => {
        return new HttpResponse(null, { status: 500 })
      })
    )

    await expect(getWeatherData('Tokyo')).rejects.toThrow(
      'Weather API error'
    )
  })
})
```

### 例2: Next.js Client Componentのテスト

```typescript
/**
 * useEffectでfetchするコンポーネントのテスト
 */
import { render, screen, waitFor } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'
import { UserProfile } from '@/components/UserProfile'

const server = setupServer(
  http.get('/api/users/:userId', ({ params }) => {
    const { userId } = params
    return HttpResponse.json({
      success: true,
      data: {
        id: userId,
        name: 'テストユーザー',
        email: 'test@example.com',
        role: 'user',
      },
    })
  })
)

beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('UserProfile Component', () => {
  it('ユーザー情報を取得して表示する', async () => {
    render(<UserProfile userId={1} />)

    // ローディング状態を確認
    expect(screen.getByText('読み込み中...')).toBeInTheDocument()

    // データの読み込みを待つ
    await waitFor(() => {
      expect(screen.getByText('テストユーザー')).toBeInTheDocument()
    })

    // データが表示されることを確認
    expect(screen.getByText('test@example.com')).toBeInTheDocument()
  })

  it('エラー時にエラーメッセージを表示する', async () => {
    server.use(
      http.get('/api/users/:userId', () => {
        return HttpResponse.json(
          { success: false, error: 'User not found' },
          { status: 404 }
        )
      })
    )

    render(<UserProfile userId={999} />)

    await waitFor(() => {
      expect(screen.getByText('ユーザーが見つかりません')).toBeInTheDocument()
    })
  })
})
```

### 例3: 既存ハンドラーの再利用

```typescript
/**
 * 共通ハンドラーを使用したテスト
 */
import { setupServer } from 'msw/node'
import { handlers } from '@/__mocks__/handlers'
import { render, screen, waitFor } from '@testing-library/react'
import { LoginForm } from '@/components/LoginForm'

// 既存のハンドラーを使用
const server = setupServer(...handlers)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('LoginForm Component', () => {
  it('ログインに成功すると成功メッセージを表示', async () => {
    render(<LoginForm />)

    // フォーム入力
    fireEvent.change(screen.getByLabelText('メールアドレス'), {
      target: { value: 'user@example.com' },
    })
    fireEvent.change(screen.getByLabelText('パスワード'), {
      target: { value: 'password' },
    })

    // 送信
    fireEvent.click(screen.getByRole('button', { name: 'ログイン' }))

    // 成功メッセージを待つ
    await waitFor(() => {
      expect(screen.getByText('ログインに成功しました')).toBeInTheDocument()
    })
  })
})
```

## 🔧 高度な使用方法

### 動的なレスポンス

```typescript
let requestCount = 0

const server = setupServer(
  http.get('/api/data', () => {
    requestCount++

    if (requestCount === 1) {
      // 1回目: ローディング
      return HttpResponse.json({ loading: true })
    } else {
      // 2回目以降: データ
      return HttpResponse.json({ data: 'complete' })
    }
  })
)

beforeEach(() => {
  requestCount = 0 // リセット
})
```

### リクエストボディの検証

```typescript
http.post('/api/users', async ({ request }) => {
  const body = await request.json() as { name: string; email: string }

  // バリデーション
  if (!body.email.includes('@')) {
    return HttpResponse.json(
      { error: 'Invalid email' },
      { status: 400 }
    )
  }

  return HttpResponse.json({
    success: true,
    data: { id: 1, ...body },
  }, { status: 201 })
})
```

### 遅延シミュレーション

```typescript
import { delay } from 'msw'

http.get('/api/slow-endpoint', async () => {
  await delay(2000) // 2秒待つ

  return HttpResponse.json({ data: 'slow response' })
})
```

## ⚠️ 注意事項

### 1. Next.js Route Handlersには使用しない

Route Handlersのテストには**Prismaモックを推奨**します：

```typescript
// ❌ 推奨しない: MSWでRoute Handlersをモック
// ⭕ 推奨: Prismaモックを使用

import { prismaMock } from '@/__mocks__/prisma'

prismaMock.user.findMany.mockResolvedValue([...])
```

### 2. onUnhandledRequestの設定

開発中は警告を表示すると便利です：

```typescript
beforeAll(() => {
  server.listen({ onUnhandledRequest: 'warn' })
  // または 'error' でエラーにする
})
```

### 3. server.resetHandlers()の重要性

各テスト後は必ずハンドラーをリセットしてください：

```typescript
afterEach(() => {
  server.resetHandlers() // 必須
})
```

## 📚 参考資料

- [MSW公式ドキュメント](https://mswjs.io/)
- [MSW v2 Migration Guide](https://mswjs.io/docs/migrations/1.x-to-2.x)
- [Testing Library with MSW](https://testing-library.com/docs/react-testing-library/example-intro/#mock-service-worker)
- プロジェクト内: `docs/testing/03_ユニットテスト実装ガイド.md`

## 🎓 まとめ

- MSWは**個別のテストファイル**でセットアップする
- **外部API呼び出し**や**Client Component**のテストに有効
- **Route Handlers**には**Prismaモック**を使用
- `beforeAll`、`afterEach`、`afterAll`のライフサイクルを守る

---

Happy Testing! 🚀
