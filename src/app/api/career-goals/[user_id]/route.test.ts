/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/api/specs/API定義書_API-032_キャリア目標更新API.md
 * テスト内容: キャリア目標更新API (API-032) のテスト
 */

import { NextRequest } from 'next/server';
import { PUT, OPTIONS } from './route';

// Jest型定義
declare global {
  var describe: (name: string, fn: () => void) => void;
  var test: (name: string, fn: () => Promise<void> | void) => void;
  var expect: (value: any) => any;
}

// モックデータ
const mockValidRequest = {
  year: 2025,
  operation_type: 'add' as const,
  career_goals: [
    {
      goal_type: 'short_term' as const,
      title: 'React.jsスキル向上',
      description: 'React.jsの基礎から応用まで習得する',
      target_date: '2025-12-31',
      status: 'not_started' as const,
      priority: 3,
      related_skills: [
        {
          skill_id: 'SKL001',
          target_level: 4
        }
      ],
      action_plans: [
        {
          title: 'React公式ドキュメント学習',
          description: 'React公式ドキュメントを一通り読む',
          due_date: '2025-08-31',
          status: 'not_started' as const
        }
      ],
      feedback: [
        {
          comment: '基礎から着実に学習していきましょう'
        }
      ]
    }
  ]
};

const mockUpdateRequest = {
  year: 2025,
  operation_type: 'update' as const,
  career_goals: [
    {
      goal_id: 'G123456789_abcdefghi',
      goal_type: 'short_term' as const,
      title: 'React.jsスキル向上（更新）',
      description: 'React.jsの基礎から応用まで習得する（進捗更新）',
      target_date: '2025-12-31',
      status: 'in_progress' as const,
      priority: 4
    }
  ]
};

const mockDeleteRequest = {
  year: 2025,
  operation_type: 'delete' as const,
  career_goals: [
    {
      goal_id: 'G123456789_abcdefghi'
    }
  ]
};

// テストヘルパー関数
function createMockRequest(body: any, headers: Record<string, string> = {}) {
  const defaultHeaders: Record<string, string> = {
    'authorization': 'Bearer mock-token',
    'content-type': 'application/json',
    ...headers
  };

  return {
    json: async () => body,
    headers: {
      get: (name: string) => defaultHeaders[name.toLowerCase()] || null
    }
  } as unknown as NextRequest;
}

describe('キャリア目標更新API (API-032)', () => {
  describe('PUT /api/career-goals/{user_id}', () => {
    describe('正常系', () => {
      test('新規追加操作が成功する', async () => {
        const request = createMockRequest(mockValidRequest);
        const params = { user_id: 'USER001' };

        const response = await PUT(request, { params });
        const responseData = await response.json();

        expect(response.status).toBe(200);
        expect(responseData.user_id).toBe('USER001');
        expect(responseData.year).toBe(2025);
        expect(responseData.operation_type).toBe('add');
        expect(responseData.operation_result).toBe('success');
        expect(responseData.updated_goals).toHaveLength(1);
        expect(responseData.updated_goals[0].goal_type).toBe('short_term');
        expect(responseData.updated_goals[0].title).toBe('React.jsスキル向上');
        expect(responseData.updated_goals[0].status).toBe('not_started');
        expect(responseData.updated_goals[0].goal_id).toMatch(/^G\d+_[a-z0-9]+$/);
      });

      test('更新操作が成功する', async () => {
        const request = createMockRequest(mockUpdateRequest);
        const params = { user_id: 'USER001' };

        const response = await PUT(request, { params });
        const responseData = await response.json();

        expect(response.status).toBe(200);
        expect(responseData.operation_type).toBe('update');
        expect(responseData.updated_goals[0].goal_id).toBe('G123456789_abcdefghi');
        expect(responseData.updated_goals[0].title).toBe('React.jsスキル向上（更新）');
        expect(responseData.updated_goals[0].status).toBe('in_progress');
      });

      test('削除操作が成功する', async () => {
        const request = createMockRequest(mockDeleteRequest);
        const params = { user_id: 'USER001' };

        const response = await PUT(request, { params });
        const responseData = await response.json();

        expect(response.status).toBe(200);
        expect(responseData.operation_type).toBe('delete');
        expect(responseData.updated_goals[0].goal_id).toBe('G123456789_abcdefghi');
        expect(responseData.updated_goals[0].status).toBe('cancelled');
      });
    });

    describe('異常系', () => {
      test('認証ヘッダーがない場合は401エラー', async () => {
        const request = createMockRequest(mockValidRequest, { authorization: '' });
        const params = { user_id: 'USER001' };

        const response = await PUT(request, { params });
        const responseData = await response.json();

        expect(response.status).toBe(401);
        expect(responseData.error.code).toBe('UNAUTHORIZED');
        expect(responseData.error.message).toBe('認証が必要です');
      });

      test('ユーザーIDが空の場合は404エラー', async () => {
        const request = createMockRequest(mockValidRequest);
        const params = { user_id: '' };

        const response = await PUT(request, { params });
        const responseData = await response.json();

        expect(response.status).toBe(404);
        expect(responseData.error.code).toBe('USER_NOT_FOUND');
        expect(responseData.error.message).toBe('ユーザーが見つかりません');
      });

      test('過去年度の場合は400エラー', async () => {
        const pastYearRequest = {
          ...mockValidRequest,
          year: 2020
        };
        const request = createMockRequest(pastYearRequest);
        const params = { user_id: 'USER001' };

        const response = await PUT(request, { params });
        const responseData = await response.json();

        expect(response.status).toBe(400);
        expect(responseData.error.code).toBe('PAST_YEAR_MODIFICATION');
        expect(responseData.error.message).toBe('過去の年度は変更できません');
      });

      test('必須パラメータが不足している場合は400エラー', async () => {
        const invalidRequest = {
          year: 2025,
          operation_type: 'add' as const,
          career_goals: [
            {
              // goal_type が不足
              title: 'テスト目標',
              target_date: '2025-12-31',
              status: 'not_started' as const,
              priority: 3
            }
          ]
        };
        const request = createMockRequest(invalidRequest);
        const params = { user_id: 'USER001' };

        const response = await PUT(request, { params });
        const responseData = await response.json();

        expect(response.status).toBe(400);
        expect(responseData.error.code).toBe('INVALID_PARAMETER');
        expect(responseData.error.message).toBe('パラメータが不正です');
      });

      test('更新時にgoal_idが不足している場合は400エラー', async () => {
        const invalidUpdateRequest = {
          year: 2025,
          operation_type: 'update' as const,
          career_goals: [
            {
              // goal_id が不足
              goal_type: 'short_term' as const,
              title: 'テスト目標',
              target_date: '2025-12-31',
              status: 'not_started' as const,
              priority: 3
            }
          ]
        };
        const request = createMockRequest(invalidUpdateRequest);
        const params = { user_id: 'USER001' };

        const response = await PUT(request, { params });
        const responseData = await response.json();

        expect(response.status).toBe(400);
        expect(responseData.error.code).toBe('INVALID_PARAMETER');
        expect(responseData.error.details).toContain('更新・削除時は目標IDが必須です');
      });

      test('不正なJSONの場合は400エラー', async () => {
        const request = {
          json: async () => {
            throw new Error('Invalid JSON');
          },
          headers: {
            get: (name: string) => name === 'authorization' ? 'Bearer mock-token' : null
          }
        } as unknown as NextRequest;
        const params = { user_id: 'USER001' };

        const response = await PUT(request, { params });
        const responseData = await response.json();

        expect(response.status).toBe(400);
        expect(responseData.error.code).toBe('INVALID_PARAMETER');
        expect(responseData.error.details).toBe('リクエストボディの形式が正しくありません');
      });

      test('バリデーションエラーの場合は400エラー', async () => {
        const invalidRequest = {
          year: 'invalid', // 数値でない
          operation_type: 'invalid_operation', // 無効な操作タイプ
          career_goals: []
        };
        const request = createMockRequest(invalidRequest);
        const params = { user_id: 'USER001' };

        const response = await PUT(request, { params });
        const responseData = await response.json();

        expect(response.status).toBe(400);
        expect(responseData.error.code).toBe('INVALID_PARAMETER');
        expect(responseData.error.details).toContain('year');
        expect(responseData.error.details).toContain('operation_type');
      });
    });
  });

  describe('OPTIONS /api/career-goals/{user_id}', () => {
    test('CORS対応のOPTIONSリクエストが成功する', async () => {
      const request = {} as NextRequest;
      const response = await OPTIONS(request);

      expect(response.status).toBe(200);
      expect(response.headers.get('Access-Control-Allow-Origin')).toBe('*');
      expect(response.headers.get('Access-Control-Allow-Methods')).toBe('PUT, OPTIONS');
      expect(response.headers.get('Access-Control-Allow-Headers')).toBe('Content-Type, Authorization');
    });
  });
});
