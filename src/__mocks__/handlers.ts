import { http, HttpResponse } from 'msw'

/**
 * MSW v2 APIハンドラー
 * テスト用のモックAPIレスポンスを定義
 */
export const handlers = [
  // 認証API
  http.post('/api/auth/login', async ({ request }) => {
    const { email, password } = await request.json() as { email: string; password: string }

    if (email === 'user@example.com' && password === 'password') {
      return HttpResponse.json(
        {
          success: true,
          token: 'mock-jwt-token',
          user: {
            id: 1,
            name: 'テストユーザー',
            email: 'user@example.com',
            role: 'user'
          }
        },
        { status: 200 }
      )
    }

    return HttpResponse.json(
      {
        success: false,
        error: '認証に失敗しました'
      },
      { status: 401 }
    )
  }),

  http.post('/api/auth/logout', () => {
    return HttpResponse.json({ success: true }, { status: 200 })
  }),

  // スキル管理API
  http.get('/api/skills/:userId', () => {
    return HttpResponse.json({
      success: true,
      data: [
        {
          id: 1,
          name: 'JavaScript',
          category: 'プログラミング言語',
          level: '○',
          experience: '3年'
        },
        {
          id: 2,
          name: 'TypeScript',
          category: 'プログラミング言語',
          level: '◎',
          experience: '2年'
        }
      ]
    })
  }),

  http.post('/api/skills/:userId', async ({ request }) => {
    const skill = await request.json() as Record<string, unknown>
    return HttpResponse.json(
      {
        success: true,
        data: {
          id: Date.now(),
          ...skill,
          createdAt: new Date().toISOString()
        }
      },
      { status: 201 }
    )
  }),

  http.put('/api/skills/:userId/:skillId', async ({ request, params }) => {
    const { skillId } = params
    const skill = await request.json() as Record<string, unknown>
    return HttpResponse.json({
      success: true,
      data: {
        id: Number(skillId),
        ...skill,
        updatedAt: new Date().toISOString()
      }
    })
  }),

  http.delete('/api/skills/:userId/:skillId', () => {
    return HttpResponse.json(
      { success: true },
      { status: 200 }
    )
  }),

  // キャリアプランAPI
  http.get('/api/career/init', () => {
    return HttpResponse.json({
      success: true,
      data: {
        career_goal: {
          target_position: 'pos_001',
          target_date: '2027-12-31',
          target_description: 'シニアエンジニアを目指す',
          current_level: 'JUNIOR',
          target_level: 'SENIOR',
          progress_percentage: 30.5
        },
        skill_categories: [
          {
            id: 'CAT_001',
            name: 'プログラミング',
            short_name: 'プログラミング',
            type: 'TECHNICAL'
          }
        ],
        positions: [
          {
            id: 'pos_001',
            name: 'シニアエンジニア',
            short_name: 'SE',
            level: 3
          }
        ]
      },
      timestamp: new Date().toISOString()
    })
  }),

  // プロフィールAPI
  http.get('/api/profile/:userId', () => {
    return HttpResponse.json({
      success: true,
      data: {
        id: 1,
        name: 'テストユーザー',
        email: 'user@example.com',
        department: '開発部',
        position: 'エンジニア',
        joinDate: '2020-04-01'
      }
    })
  }),

  http.put('/api/profile/:userId', async ({ request }) => {
    const profile = await request.json() as Record<string, unknown>
    return HttpResponse.json({
      success: true,
      data: {
        ...profile,
        updatedAt: new Date().toISOString()
      }
    })
  })
]
