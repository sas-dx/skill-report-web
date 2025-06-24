/**
 * 要求仕様ID: CAR.1-PLAN.1
 * API-700: キャリア初期データ取得API テストファイル
 * 実装日: 2025-06-24
 * 実装者: システム開発チーム
 */

import { NextRequest } from 'next/server';

// テストヘルパー関数
function createMockRequest(headers: Record<string, string> = {}) {
  const defaultHeaders: Record<string, string> = {
    'x-user-id': 'emp_001',
    ...headers
  };

  return {
    headers: {
      get: (name: string) => defaultHeaders[name.toLowerCase()] || null
    }
  } as unknown as NextRequest;
}

// モックレスポンスデータ
const mockCareerGoalResponse = {
  id: 'plan_001',
  target_position: 'pos_001',
  target_date: '2027-12-31',
  target_description: 'シニアエンジニアを目指す',
  current_level: 'JUNIOR',
  target_level: 'SENIOR',
  progress_percentage: 30.5,
  plan_status: 'ACTIVE',
  last_review_date: '2025-06-01',
  next_review_date: '2025-12-01'
};

const mockSkillCategoriesResponse = [
  {
    id: 'CAT_001',
    name: 'プログラミング',
    short_name: 'プログラミング',
    type: 'TECHNICAL',
    parent_id: null,
    level: 1,
    description: 'プログラミングスキル',
    icon_url: '/icons/programming.svg',
    color_code: '#3399cc'
  }
];

const mockPositionsResponse = [
  {
    id: 'pos_001',
    name: 'シニアエンジニア',
    short_name: 'SE',
    level: 3,
    rank: 3,
    category: 'ENGINEER',
    authority_level: 3,
    is_management: false,
    is_executive: false,
    description: 'シニアレベルのエンジニア'
  }
];

// 動的インポートでGET関数を取得
async function importGETFunction() {
  const module = await import('./route');
  return module.GET;
}

describe('API-700: キャリア初期データ取得API', () => {
  describe('GET /api/career/init', () => {
    describe('正常系', () => {
      test('キャリア初期データを正常に取得できること', async () => {
        const GET = await importGETFunction();
        const request = createMockRequest();

        const response = await GET(request);
        const responseData = await response.json();

        expect(response.status).toBe(200);
        expect(responseData.success).toBe(true);
        expect(responseData.data).toHaveProperty('career_goal');
        expect(responseData.data).toHaveProperty('skill_categories');
        expect(responseData.data).toHaveProperty('positions');
      });

      test('ユーザーIDがヘッダーにない場合、デフォルトユーザーIDを使用すること', async () => {
        const GET = await importGETFunction();
        const request = createMockRequest({ 'x-user-id': '' });

        const response = await GET(request);
        const responseData = await response.json();

        expect(response.status).toBe(200);
        expect(responseData.success).toBe(true);
      });

      test('キャリアプランが存在しない場合、空のキャリア目標を返すこと', async () => {
        const GET = await importGETFunction();
        const request = createMockRequest({ 'x-user-id': 'emp_999' });

        const response = await GET(request);
        const responseData = await response.json();

        expect(response.status).toBe(200);
        expect(responseData.success).toBe(true);
        expect(responseData.data.career_goal).toHaveProperty('target_position');
        expect(responseData.data.career_goal).toHaveProperty('target_date');
        expect(responseData.data.career_goal).toHaveProperty('target_description');
      });
    });

    describe('レスポンス形式テスト', () => {
      test('レスポンスが正しい形式であること', async () => {
        const GET = await importGETFunction();
        const request = createMockRequest();

        const response = await GET(request);
        const responseData = await response.json();

        expect(responseData).toHaveProperty('success');
        expect(responseData).toHaveProperty('data');
        expect(responseData).toHaveProperty('timestamp');
        expect(typeof responseData.success).toBe('boolean');
        expect(typeof responseData.timestamp).toBe('string');
      });

      test('キャリア目標データの形式が正しいこと', async () => {
        const GET = await importGETFunction();
        const request = createMockRequest();

        const response = await GET(request);
        const responseData = await response.json();

        const careerGoal = responseData.data.career_goal;
        expect(careerGoal).toHaveProperty('target_position');
        expect(careerGoal).toHaveProperty('target_date');
        expect(careerGoal).toHaveProperty('target_description');
        expect(careerGoal).toHaveProperty('current_level');
        expect(careerGoal).toHaveProperty('target_level');
        expect(careerGoal).toHaveProperty('progress_percentage');
      });

      test('スキルカテゴリデータの形式が正しいこと', async () => {
        const GET = await importGETFunction();
        const request = createMockRequest();

        const response = await GET(request);
        const responseData = await response.json();

        const skillCategories = responseData.data.skill_categories;
        expect(Array.isArray(skillCategories)).toBe(true);
        
        if (skillCategories.length > 0) {
          const category = skillCategories[0];
          expect(category).toHaveProperty('id');
          expect(category).toHaveProperty('name');
          expect(category).toHaveProperty('short_name');
          expect(category).toHaveProperty('type');
          expect(category).toHaveProperty('level');
        }
      });

      test('ポジションデータの形式が正しいこと', async () => {
        const GET = await importGETFunction();
        const request = createMockRequest();

        const response = await GET(request);
        const responseData = await response.json();

        const positions = responseData.data.positions;
        expect(Array.isArray(positions)).toBe(true);
        
        if (positions.length > 0) {
          const position = positions[0];
          expect(position).toHaveProperty('id');
          expect(position).toHaveProperty('name');
          expect(position).toHaveProperty('short_name');
          expect(position).toHaveProperty('level');
          expect(position).toHaveProperty('category');
        }
      });
    });

    describe('パフォーマンステスト', () => {
      test('レスポンス時間が1秒以内であること', async () => {
        const GET = await importGETFunction();
        const request = createMockRequest();

        const startTime = Date.now();
        const response = await GET(request);
        const endTime = Date.now();
        const executionTime = endTime - startTime;

        expect(response.status).toBe(200);
        expect(executionTime).toBeLessThan(1000); // 1秒以内
      });

      test('複数回の連続リクエストが正常に処理されること', async () => {
        const GET = await importGETFunction();
        const request = createMockRequest();

        const promises = Array.from({ length: 5 }, () => GET(request));
        const responses = await Promise.all(promises);

        responses.forEach(response => {
          expect(response.status).toBe(200);
        });
      });
    });

    describe('エラーハンドリングテスト', () => {
      test('不正なヘッダーでもエラーにならないこと', async () => {
        const GET = await importGETFunction();
        const request = createMockRequest({ 'x-user-id': 'invalid-user-id' });

        const response = await GET(request);
        const responseData = await response.json();

        expect(response.status).toBe(200);
        expect(responseData.success).toBe(true);
      });

      test('空のヘッダーでもエラーにならないこと', async () => {
        const GET = await importGETFunction();
        const request = createMockRequest({});

        const response = await GET(request);
        const responseData = await response.json();

        expect(response.status).toBe(200);
        expect(responseData.success).toBe(true);
      });
    });

    describe('データ型テスト', () => {
      test('progress_percentageが数値型であること', async () => {
        const GET = await importGETFunction();
        const request = createMockRequest();

        const response = await GET(request);
        const responseData = await response.json();

        const progressPercentage = responseData.data.career_goal.progress_percentage;
        expect(typeof progressPercentage).toBe('number');
        expect(progressPercentage).toBeGreaterThanOrEqual(0);
        expect(progressPercentage).toBeLessThanOrEqual(100);
      });

      test('日付フィールドが正しい形式であること', async () => {
        const GET = await importGETFunction();
        const request = createMockRequest();

        const response = await GET(request);
        const responseData = await response.json();

        const careerGoal = responseData.data.career_goal;
        if (careerGoal.target_date) {
          expect(typeof careerGoal.target_date).toBe('string');
          // YYYY-MM-DD形式または空文字列
          expect(careerGoal.target_date).toMatch(/^\d{4}-\d{2}-\d{2}$|^$/);
        }
      });

      test('配列フィールドが正しい型であること', async () => {
        const GET = await importGETFunction();
        const request = createMockRequest();

        const response = await GET(request);
        const responseData = await response.json();

        expect(Array.isArray(responseData.data.skill_categories)).toBe(true);
        expect(Array.isArray(responseData.data.positions)).toBe(true);
      });
    });
  });
});
