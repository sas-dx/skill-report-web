/**
 * 統合テスト用テストデータファクトリー
 * 要求仕様ID: TEST-INT.1
 * 実装ガイド: docs/testing/04_統合テスト実装ガイド.md
 */

import { PrismaClient } from '@prisma/client'
import { hashPassword } from '@/lib/auth'

/**
 * テナントデータの作成
 */
export async function createTestTenant(
  prisma: PrismaClient,
  overrides: Partial<{
    tenant_code: string
    tenant_name: string
    domain_name: string
  }> = {}
) {
  const defaultData = {
    tenant_code: 'TEST_TENANT',
    tenant_name: 'テストテナント',
    tenant_name_en: 'Test Tenant',
    domain_name: 'test.example.com',
    status: 'active',
    ...overrides
  }

  return await prisma.tenant.create({
    data: defaultData
  })
}

/**
 * 部署データの作成
 */
export async function createTestDepartment(
  prisma: PrismaClient,
  overrides: Partial<{
    department_code: string
    department_name: string
  }> = {}
) {
  const defaultData = {
    department_code: overrides.department_code || `DEPT_${Date.now()}`,
    department_name: overrides.department_name || 'テスト部署',
    department_name_short: '試験部',
    department_level: 1,
    department_type: 'business',
    department_status: 'active',
    sort_order: 1
  }

  return await prisma.department.create({
    data: defaultData
  })
}

/**
 * 従業員データの作成
 */
export async function createTestEmployee(
  prisma: PrismaClient,
  overrides: Partial<{
    employee_code: string
    full_name: string
    email: string
    department_id?: string
  }> = {}
) {
  const timestamp = Date.now()
  const defaultData = {
    employee_code: overrides.employee_code || `EMP_${timestamp}`,
    full_name: overrides.full_name || 'テスト太郎',
    full_name_kana: 'テストタロウ',
    email: overrides.email || `test${timestamp}@example.com`,
    phone: '090-1234-5678',
    hire_date: new Date('2020-04-01'),
    birth_date: new Date('1990-01-01'),
    gender: 'male',
    department_id: overrides.department_id || 'DEPT001',
    position_id: 'POS001',
    job_type_id: 'JOB001',
    employment_status: 'regular',
    employee_status: 'active'
  }

  return await prisma.employee.create({
    data: defaultData
  })
}

/**
 * 認証ユーザーデータの作成
 */
export async function createTestUserAuth(
  prisma: PrismaClient,
  overrides: Partial<{
    login_id: string
    employee_id: string
    password?: string
  }> = {}
) {
  const timestamp = Date.now()
  const password = overrides.password || 'password123'
  const hashedPwd = await hashPassword(password)

  const defaultData = {
    login_id: overrides.login_id || `test_user_${timestamp}`,
    password_hash: hashedPwd,
    employee_id: overrides.employee_id || `EMP_${timestamp}`,
    account_status: 'active',
    failed_login_count: 0,
    mfa_enabled: false
  }

  return await prisma.userAuth.create({
    data: defaultData
  })
}

/**
 * スキルカテゴリデータの作成
 */
export async function createTestSkillCategory(
  prisma: PrismaClient,
  overrides: Partial<{
    category_code: string
    category_name: string
  }> = {}
) {
  const defaultData = {
    category_code: overrides.category_code || `CAT_${Date.now()}`,
    category_name: overrides.category_name || 'テストカテゴリ',
    category_name_en: 'Test Category',
    category_type: 'technical',
    category_level: 1,
    display_order: 1,
    category_status: 'active',
    is_system_category: false,
    is_leaf_category: true
  }

  return await prisma.skillCategory.create({
    data: defaultData
  })
}

/**
 * スキルアイテムデータの作成
 */
export async function createTestSkillItem(
  prisma: PrismaClient,
  overrides: Partial<{
    skill_code: string
    skill_name: string
    skill_category_id?: string
  }> = {}
) {
  const defaultData = {
    skill_code: overrides.skill_code || `SKILL_${Date.now()}`,
    skill_name: overrides.skill_name || 'テストスキル',
    skill_category_id: overrides.skill_category_id || 'CAT001',
    skill_type: 'technical',
    difficulty_level: 3,
    importance_level: 3
  }

  return await prisma.skillItem.create({
    data: defaultData
  })
}

/**
 * スキル（MST_Skill）データの作成
 */
export async function createTestSkill(
  prisma: PrismaClient,
  overrides: Partial<{
    skill_name: string
    category_id?: string
  }> = {}
) {
  const defaultData = {
    skill_name: overrides.skill_name || 'JavaScript',
    skill_name_en: 'JavaScript',
    category_id: overrides.category_id || 'CAT001',
    skill_type: 'programming',
    difficulty_level: 3,
    description: 'プログラミング言語',
    is_core_skill: true,
    display_order: 1,
    is_active: true
  }

  return await prisma.skill.create({
    data: defaultData
  })
}

/**
 * スキル記録データの作成
 */
export async function createTestSkillRecord(
  prisma: PrismaClient,
  employeeId: string,
  skillItemId: string,
  tenantId: string = 'TENANT001',
  createdBy: string = 'SYSTEM',
  overrides: Partial<{
    skill_level: number
    self_assessment?: number
  }> = {}
) {
  const defaultData = {
    employee_id: employeeId,
    skill_item_id: skillItemId,
    skill_level: overrides.skill_level || 3,
    self_assessment: overrides.self_assessment || 3,
    manager_assessment: 3,
    evidence_description: 'テストエビデンス',
    acquisition_date: new Date('2023-01-01'),
    last_used_date: new Date(),
    skill_status: 'active',
    learning_hours: 40,
    project_experience_count: 5,
    tenant_id: tenantId,
    created_by: createdBy,
    updated_by: createdBy
  }

  return await prisma.skillRecord.create({
    data: defaultData
  })
}

/**
 * プロジェクト記録データの作成
 */
export async function createTestProjectRecord(
  prisma: PrismaClient,
  employeeId: string,
  tenantId: string = 'TENANT001',
  createdBy: string = 'SYSTEM',
  overrides: Partial<{
    project_name: string
    project_code?: string
  }> = {}
) {
  const timestamp = Date.now()
  const defaultData = {
    project_record_id: `PRJ_${timestamp}`,
    employee_id: employeeId,
    project_name: overrides.project_name || 'テストプロジェクト',
    project_code: overrides.project_code || `PRJ${timestamp}`,
    client_name: 'テスト株式会社',
    project_type: 'development',
    project_scale: 'medium',
    start_date: new Date('2023-01-01'),
    end_date: new Date('2023-12-31'),
    participation_rate: 80.0,
    role_title: 'エンジニア',
    responsibilities: 'システム開発',
    technologies_used: 'JavaScript, TypeScript, React',
    skills_applied: 'プログラミング, 設計',
    achievements: 'システムリリース成功',
    project_status: 'completed',
    evaluation_score: 4.5,
    is_confidential: false,
    is_public_reference: true,
    tenant_id: tenantId,
    created_by: createdBy,
    updated_by: createdBy
  }

  return await prisma.projectRecord.create({
    data: defaultData
  })
}

/**
 * 研修履歴データの作成
 */
export async function createTestTrainingHistory(
  prisma: PrismaClient,
  employeeId: string,
  tenantId: string = 'TENANT001',
  createdBy: string = 'SYSTEM',
  overrides: Partial<{
    training_name: string
  }> = {}
) {
  const timestamp = Date.now()
  const defaultData = {
    training_history_id: `TRN_${timestamp}`,
    employee_id: employeeId,
    training_program_id: 'TPROG001',
    training_name: overrides.training_name || 'テスト研修',
    training_type: 'technical',
    training_category: 'programming',
    provider_name: 'テスト研修機関',
    instructor_name: '講師A',
    start_date: new Date('2023-06-01'),
    end_date: new Date('2023-06-05'),
    duration_hours: 40.0,
    location: 'オンライン',
    cost: 100000.0,
    cost_covered_by: 'company',
    attendance_status: 'completed',
    completion_rate: 100.0,
    test_score: 85.0,
    grade: 'A',
    certificate_obtained: true,
    certificate_number: `CERT${timestamp}`,
    pdu_earned: 40.0,
    skills_acquired: 'プログラミング基礎',
    satisfaction_score: 4.5,
    manager_approval: true,
    tenant_id: tenantId,
    created_by: createdBy,
    updated_by: createdBy
  }

  return await prisma.trainingHistory.create({
    data: defaultData
  })
}

/**
 * 目標進捗データの作成
 */
export async function createTestGoalProgress(
  prisma: PrismaClient,
  employeeId: string,
  tenantId: string = 'TENANT001',
  createdBy: string = 'SYSTEM',
  overrides: Partial<{
    goal_title: string
  }> = {}
) {
  const timestamp = Date.now()
  const defaultData = {
    goal_id: `GOAL_${timestamp}`,
    employee_id: employeeId,
    goal_title: overrides.goal_title || 'テスト目標',
    goal_description: '目標の詳細説明',
    goal_category: 'skill',
    goal_type: 'individual',
    priority_level: 'high',
    target_value: 100.0,
    current_value: 50.0,
    unit: '%',
    start_date: new Date('2023-01-01'),
    target_date: new Date('2023-12-31'),
    progress_rate: 50.0,
    achievement_status: 'in_progress',
    supervisor_id: 'MGR001',
    approval_status: 'approved',
    tenant_id: tenantId,
    created_by: createdBy,
    updated_by: createdBy
  }

  return await prisma.goalProgress.create({
    data: defaultData
  })
}

/**
 * キャリアプランデータの作成
 */
export async function createTestCareerPlan(
  prisma: PrismaClient,
  employeeId: string,
  overrides: Partial<{
    plan_name: string
  }> = {}
) {
  const timestamp = Date.now()
  const defaultData = {
    career_plan_id: `CP_${timestamp}`,
    employee_id: employeeId,
    plan_name: overrides.plan_name || 'テストキャリアプラン',
    plan_description: 'キャリアプランの説明',
    plan_type: 'individual',
    current_level: 'junior',
    target_level: 'senior',
    plan_start_date: new Date('2023-01-01'),
    plan_end_date: new Date('2025-12-31'),
    required_skills: 'JavaScript, TypeScript, React',
    plan_status: 'active',
    progress_percentage: 30.0
  }

  return await prisma.careerPlan.create({
    data: defaultData
  })
}

/**
 * 完全なテストユーザー（従業員+認証）の作成
 */
export async function createTestUserComplete(
  prisma: PrismaClient,
  overrides: Partial<{
    employee_code: string
    login_id: string
    email: string
    password: string
    department_id?: string
  }> = {}
) {
  const timestamp = Date.now()
  const employeeCode = overrides.employee_code || `EMP_${timestamp}`
  const email = overrides.email || `test${timestamp}@example.com`

  // 従業員データ作成
  const employee = await createTestEmployee(prisma, {
    employee_code: employeeCode,
    email,
    department_id: overrides.department_id
  })

  // 認証データ作成
  const userAuth = await createTestUserAuth(prisma, {
    login_id: overrides.login_id || `user_${timestamp}`,
    employee_id: employee.id,
    password: overrides.password
  })

  return {
    employee,
    userAuth
  }
}
