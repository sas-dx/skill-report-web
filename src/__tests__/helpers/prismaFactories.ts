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

/**
 * 部署のテストデータを作成
 */
export function createMockDepartment(overrides?: Partial<any>) {
  return {
    department_code: 'DEPT_001',
    department_name: '開発部',
    department_name_short: '開発',
    parent_department_id: null,
    department_level: 1,
    department_type: 'ENGINEERING',
    manager_id: 'emp_001',
    deputy_manager_id: null,
    cost_center_code: 'CC_001',
    budget_amount: 10000000,
    location: '本社',
    phone_number: '03-1234-5678',
    email_address: 'dev@example.com',
    establishment_date: new Date('2020-01-01'),
    abolition_date: null,
    department_status: 'ACTIVE',
    sort_order: 1,
    description: '開発部門',
    is_deleted: false,
    created_at: new Date('2024-01-01'),
    updated_at: new Date('2024-01-01'),
    ...overrides,
  }
}

/**
 * 複数の部署を作成
 */
export function createMockDepartments(count: number, baseOverrides?: Partial<any>) {
  return Array.from({ length: count }, (_, index) =>
    createMockDepartment({
      department_code: `DEPT_${String(index + 1).padStart(3, '0')}`,
      department_name: `部署${index + 1}`,
      sort_order: index + 1,
      ...baseOverrides,
    })
  )
}

/**
 * 社員のテストデータを作成
 */
export function createMockEmployee(overrides?: Partial<any>) {
  return {
    employee_code: 'EMP001',
    full_name: '山田太郎',
    full_name_kana: 'ヤマダタロウ',
    email: 'yamada@example.com',
    phone: '090-1234-5678',
    hire_date: new Date('2020-04-01'),
    birth_date: new Date('1990-01-01'),
    gender: 'MALE',
    department_id: 'DEPT_001',
    position_id: 'pos_001',
    employment_type: 'FULL_TIME',
    employee_status: 'ACTIVE',
    is_deleted: false,
    created_at: new Date('2024-01-01'),
    updated_at: new Date('2024-01-01'),
    ...overrides,
  }
}

/**
 * 複数の社員を作成
 */
export function createMockEmployees(count: number, baseOverrides?: Partial<any>) {
  return Array.from({ length: count }, (_, index) =>
    createMockEmployee({
      employee_code: `EMP${String(index + 1).padStart(3, '0')}`,
      full_name: `社員${index + 1}`,
      full_name_kana: `シャイン${index + 1}`,
      email: `employee${index + 1}@example.com`,
      ...baseOverrides,
    })
  )
}

/**
 * 資格のテストデータを作成
 */
export function createMockCertification(overrides?: Partial<any>) {
  return {
    certification_code: 'CERT_001',
    certification_name: '基本情報技術者試験',
    certification_name_en: 'Fundamental Information Technology Engineer Examination',
    issuer: 'IPA',
    issuer_country: 'JP',
    certification_category: 'IT',
    certification_level: 'BASIC',
    validity_period_months: null,
    renewal_required: false,
    renewal_requirements: null,
    exam_fee: 7500,
    exam_language: 'ja',
    exam_format: 'CBT',
    official_url: 'https://www.ipa.go.jp/shiken/kubun/fe.html',
    description: '情報処理技術者としての基本的な知識・技能',
    skill_category_id: 'CAT_001',
    is_recommended: true,
    is_active: true,
    is_deleted: false,
    created_at: new Date('2024-01-01'),
    updated_at: new Date('2024-01-01'),
    ...overrides,
  }
}

/**
 * 複数の資格を作成
 */
export function createMockCertifications(count: number, baseOverrides?: Partial<any>) {
  return Array.from({ length: count }, (_, index) =>
    createMockCertification({
      certification_code: `CERT_${String(index + 1).padStart(3, '0')}`,
      certification_name: `資格${index + 1}`,
      ...baseOverrides,
    })
  )
}

/**
 * プロジェクト記録のテストデータを作成
 */
export function createMockProjectRecord(overrides?: Partial<any>) {
  return {
    record_id: 'REC_001',
    employee_id: 'emp_001',
    project_code: 'PRJ_001',
    project_name: 'WEBシステム開発',
    project_type: 'DEVELOPMENT',
    project_category: 'WEB',
    role: 'DEVELOPER',
    participation_start_date: new Date('2024-01-01'),
    participation_end_date: new Date('2024-12-31'),
    participation_months: 12,
    allocation_percentage: 80.0,
    project_scale: 'MEDIUM',
    team_size: 10,
    primary_skills_used: 'TypeScript,React,Next.js',
    technologies_used: 'Next.js,PostgreSQL,Prisma',
    business_domain: 'HR',
    achievements: 'システムの設計と実装を担当',
    challenges_faced: 'パフォーマンス最適化',
    lessons_learned: 'Next.js App Routerの活用',
    project_status: 'IN_PROGRESS',
    is_deleted: false,
    created_at: new Date('2024-01-01'),
    updated_at: new Date('2024-01-01'),
    created_by: 'emp_001',
    updated_by: 'emp_001',
    ...overrides,
  }
}

/**
 * 複数のプロジェクト記録を作成
 */
export function createMockProjectRecords(count: number, baseOverrides?: Partial<any>) {
  return Array.from({ length: count }, (_, index) =>
    createMockProjectRecord({
      record_id: `REC_${String(index + 1).padStart(3, '0')}`,
      project_code: `PRJ_${String(index + 1).padStart(3, '0')}`,
      project_name: `プロジェクト${index + 1}`,
      ...baseOverrides,
    })
  )
}

/**
 * スキルのテストデータを作成
 */
export function createMockSkill(overrides?: Partial<any>) {
  return {
    skill_id: 'SKILL_001',
    skill_code: 'JS_001',
    skill_name: 'JavaScript',
    skill_name_en: 'JavaScript',
    category_id: 'CAT_001',
    parent_skill_id: null,
    skill_type: 'TECHNICAL',
    skill_level: 1,
    proficiency_levels: '1:初級,2:中級,3:上級,4:エキスパート',
    description: 'JavaScript プログラミング言語',
    icon_url: '/icons/javascript.svg',
    color_code: '#F7DF1E',
    is_core_skill: true,
    is_certification_related: false,
    related_certifications: null,
    learning_resources: 'MDN Web Docs',
    assessment_criteria: '基本構文の理解、DOM操作、非同期処理',
    is_active: true,
    is_deleted: false,
    created_at: new Date('2024-01-01'),
    updated_at: new Date('2024-01-01'),
    created_by: 'system',
    updated_by: 'system',
    ...overrides,
  }
}

/**
 * 複数のスキルを作成
 */
export function createMockSkills(count: number, baseOverrides?: Partial<any>) {
  return Array.from({ length: count }, (_, index) =>
    createMockSkill({
      skill_id: `SKILL_${String(index + 1).padStart(3, '0')}`,
      skill_code: `CODE_${String(index + 1).padStart(3, '0')}`,
      skill_name: `スキル${index + 1}`,
      ...baseOverrides,
    })
  )
}

/**
 * 目標進捗のテストデータを作成
 */
export function createMockGoalProgress(overrides?: Partial<any>) {
  return {
    progress_id: 'PROG_001',
    employee_id: 'emp_001',
    goal_id: 'GOAL_001',
    goal_type: 'CAREER',
    target_value: 100,
    current_value: 50,
    progress_percentage: 50.0,
    status: 'IN_PROGRESS',
    start_date: new Date('2024-01-01'),
    target_date: new Date('2024-12-31'),
    actual_completion_date: null,
    last_updated_date: new Date('2024-06-01'),
    review_notes: '順調に進捗中',
    barriers: null,
    support_needed: null,
    is_deleted: false,
    created_at: new Date('2024-01-01'),
    updated_at: new Date('2024-06-01'),
    created_by: 'emp_001',
    updated_by: 'emp_001',
    ...overrides,
  }
}

/**
 * 複数の目標進捗を作成
 */
export function createMockGoalProgresses(count: number, baseOverrides?: Partial<any>) {
  return Array.from({ length: count }, (_, index) =>
    createMockGoalProgress({
      progress_id: `PROG_${String(index + 1).padStart(3, '0')}`,
      goal_id: `GOAL_${String(index + 1).padStart(3, '0')}`,
      ...baseOverrides,
    })
  )
}
