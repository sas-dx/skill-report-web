/**
 * Prisma テストデータファクトリ
 *
 * Prismaモデルのテストデータを生成するファクトリ関数
 */

/**
 * キャリアプランのテストデータを作成
 */
export function createMockCareerPlan(overrides?: Partial<any>) {
  return {
    plan_id: 'plan_001',
    employee_id: 'emp_001',
    target_position_id: 'pos_001',
    target_date: new Date('2027-12-31'),
    target_description: 'シニアエンジニアを目指す',
    current_level: 'JUNIOR',
    target_level: 'SENIOR',
    progress_percentage: 30.5,
    plan_status: 'ACTIVE',
    last_review_date: new Date('2025-06-01'),
    next_review_date: new Date('2025-12-01'),
    is_deleted: false,
    created_at: new Date('2024-01-01'),
    updated_at: new Date('2025-06-01'),
    created_by: 'emp_001',
    updated_by: 'emp_001',
    ...overrides,
  }
}

/**
 * スキルカテゴリのテストデータを作成
 */
export function createMockSkillCategory(overrides?: Partial<any>) {
  return {
    category_id: 'CAT_001',
    category_name: 'プログラミング',
    short_name: 'プログラミング',
    category_type: 'TECHNICAL',
    parent_category_id: null,
    category_level: 1,
    category_description: 'プログラミングスキル',
    icon_url: '/icons/programming.svg',
    color_code: '#3399cc',
    is_deleted: false,
    created_at: new Date('2024-01-01'),
    updated_at: new Date('2024-01-01'),
    created_by: 'system',
    updated_by: 'system',
    ...overrides,
  }
}

/**
 * ポジションのテストデータを作成
 */
export function createMockPosition(overrides?: Partial<any>) {
  return {
    position_id: 'pos_001',
    position_name: 'シニアエンジニア',
    short_name: 'SE',
    position_level: 3,
    position_rank: 3,
    position_category: 'ENGINEER',
    authority_level: 3,
    is_management: false,
    is_executive: false,
    position_description: 'シニアレベルのエンジニア',
    is_deleted: false,
    created_at: new Date('2024-01-01'),
    updated_at: new Date('2024-01-01'),
    created_by: 'system',
    updated_by: 'system',
    ...overrides,
  }
}

/**
 * ユーザーのテストデータを作成
 */
export function createMockUser(overrides?: Partial<any>) {
  return {
    user_id: 1,
    employee_id: 'EMP001',
    name: 'テストユーザー',
    email: 'test@example.com',
    role: 'user',
    created_at: new Date('2024-01-01'),
    updated_at: new Date('2024-01-01'),
    ...overrides,
  }
}

/**
 * 複数のキャリアプランを作成
 */
export function createMockCareerPlans(count: number, baseOverrides?: Partial<any>) {
  return Array.from({ length: count }, (_, index) =>
    createMockCareerPlan({
      plan_id: `plan_${String(index + 1).padStart(3, '0')}`,
      employee_id: `emp_${String(index + 1).padStart(3, '0')}`,
      ...baseOverrides,
    })
  )
}

/**
 * 複数のスキルカテゴリを作成
 */
export function createMockSkillCategories(count: number, baseOverrides?: Partial<any>) {
  return Array.from({ length: count }, (_, index) =>
    createMockSkillCategory({
      category_id: `CAT_${String(index + 1).padStart(3, '0')}`,
      category_name: `スキルカテゴリ${index + 1}`,
      ...baseOverrides,
    })
  )
}

/**
 * 複数のポジションを作成
 */
export function createMockPositions(count: number, baseOverrides?: Partial<any>) {
  return Array.from({ length: count }, (_, index) =>
    createMockPosition({
      position_id: `pos_${String(index + 1).padStart(3, '0')}`,
      position_name: `ポジション${index + 1}`,
      position_level: index + 1,
      position_rank: index + 1,
      ...baseOverrides,
    })
  )
}

/**
 * 複数のユーザーを作成
 */
export function createMockUsers(count: number, baseOverrides?: Partial<any>) {
  return Array.from({ length: count }, (_, index) =>
    createMockUser({
      user_id: index + 1,
      employee_id: `EMP${String(index + 1).padStart(3, '0')}`,
      name: `テストユーザー${index + 1}`,
      email: `test${index + 1}@example.com`,
      ...baseOverrides,
    })
  )
}
