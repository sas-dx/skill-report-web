// @ts-nocheck
// 要求仕様ID: PLT.1-DB.1 - データベース初期データ投入
// 設計書: docs/design/database/data/ 配下のサンプルデータSQLファイル群
// 自動生成日時: 2025-06-23 21:30:00
import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

export async function runSampleSeed() {
  console.log('🌱 データベースの初期データ投入を開始します...')

  try {
    // MST_Tenantデータ
    console.log('📊 MST_Tenantデータを投入中...')
    const tenantData = await Promise.all([
      prisma.tenant.upsert({
        where: { tenant_id: 'default-tenant' },
        update: {},
        create: {
          tenant_id: 'default-tenant',
          tenant_code: 'DEFAULT',
          tenant_name: 'デフォルトテナント',
        },
      }),
      prisma.tenant.upsert({
        where: { tenant_id: 'tenant_002' },
        update: {},
        create: {
          tenant_id: 'tenant_002',
          tenant_code: 'DEMO',
          tenant_name: 'デモテナント',
        },
      }),
    ])

    // MST_Departmentデータ
    console.log('📊 MST_Departmentデータを投入中...')
    const departmentData = await Promise.all([
      prisma.department.upsert({
        where: { department_code: 'DEPT001' },
        update: {},
        create: {
          department_code: 'DEPT001',
          department_name: '経営企画本部',
          department_name_short: '経営企画',
          department_level: 1,
          department_type: 'HEADQUARTERS',
          manager_id: '000001',
          cost_center_code: 'CC001',
          budget_amount: 50000000.0,
          location: '本社ビル 10F',
          phone_number: '03-1234-5678',
          email_address: 'planning@company.com',
          establishment_date: new Date('2020-04-01'),
          department_status: 'ACTIVE',
          sort_order: 1,
          description: '会社全体の経営戦略立案・推進を担当',
        },
      }),
      prisma.department.upsert({
        where: { department_code: 'DEPT002' },
        update: {},
        create: {
          department_code: 'DEPT002',
          department_name: 'システム開発部',
          department_name_short: 'システム開発',
          parent_department_id: 'DEPT001',
          department_level: 2,
          department_type: 'DEPARTMENT',
          manager_id: '000002',
          deputy_manager_id: '000003',
          cost_center_code: 'CC002',
          budget_amount: 120000000.0,
          location: '本社ビル 8F',
          phone_number: '03-1234-5679',
          email_address: 'dev@company.com',
          establishment_date: new Date('2020-04-01'),
          department_status: 'ACTIVE',
          sort_order: 2,
          description: '社内システムの開発・保守・運用を担当',
        },
      }),
    ])

    // MST_Positionデータ
    console.log('📊 MST_Positionデータを投入中...')
    const positionData = await Promise.all([
      prisma.position.upsert({
        where: { position_code: 'POS001' },
        update: {},
        create: {
          position_code: 'POS001',
          position_name: '代表取締役社長',
          position_name_short: '社長',
          position_level: 1,
          position_rank: 1,
          position_category: 'EXECUTIVE',
          authority_level: 10,
          approval_limit: 999999999.99,
          salary_grade: 'E1',
          allowance_amount: 500000.0,
          is_management: true,
          is_executive: true,
          requires_approval: true,
          can_hire: true,
          can_evaluate: true,
          position_status: 'ACTIVE',
          sort_order: 1,
          description: '会社の最高責任者として経営全般を統括',
        },
      }),
      prisma.position.upsert({
        where: { position_code: 'POS002' },
        update: {},
        create: {
          position_code: 'POS002',
          position_name: '取締役',
          position_name_short: '取締役',
          position_level: 2,
          position_rank: 1,
          position_category: 'EXECUTIVE',
          authority_level: 9,
          approval_limit: 100000000.0,
          salary_grade: 'E2',
          allowance_amount: 300000.0,
          is_management: true,
          is_executive: true,
          requires_approval: true,
          can_hire: true,
          can_evaluate: true,
          position_status: 'ACTIVE',
          sort_order: 2,
          description: '取締役会メンバーとして経営方針決定に参画',
        },
      }),
      prisma.position.upsert({
        where: { position_code: 'POS003' },
        update: {},
        create: {
          position_code: 'POS003',
          position_name: '部長',
          position_name_short: '部長',
          position_level: 3,
          position_rank: 1,
          position_category: 'MANAGER',
          authority_level: 7,
          approval_limit: 10000000.0,
          salary_grade: 'M1',
          allowance_amount: 100000.0,
          is_management: true,
          is_executive: false,
          requires_approval: true,
          can_hire: true,
          can_evaluate: true,
          position_status: 'ACTIVE',
          sort_order: 3,
          description: '部門の責任者として業務全般を管理',
        },
      }),
    ])

    // MST_JobTypeデータ
    console.log('📊 MST_JobTypeデータを投入中...')
    const jobTypeData = await Promise.all([
      prisma.jobType.upsert({
        where: { job_type_code: 'SE' },
        update: {},
        create: {
          job_type_code: 'SE',
          job_type_name: 'システムエンジニア',
          job_type_name_en: 'Systems Engineer',
          job_category: 'ENGINEERING',
          job_level: 'SENIOR',
          description: 'システムの設計・開発・テストを担当するエンジニア',
          required_experience_years: 3,
          salary_grade_min: 3,
          salary_grade_max: 6,
          career_path: 'SE → シニアSE → テックリード → エンジニアリングマネージャー',
          required_certifications: '["基本情報技術者", "応用情報技術者"]',
          required_skills: '["Java", "SQL", "システム設計", "要件定義"]',
          department_affinity: '["開発部", "システム部"]',
          remote_work_eligible: true,
          travel_frequency: 'LOW',
          sort_order: 1,
          is_active: true,
        },
      }),
      prisma.jobType.upsert({
        where: { job_type_code: 'PM' },
        update: {},
        create: {
          job_type_code: 'PM',
          job_type_name: 'プロジェクトマネージャー',
          job_type_name_en: 'Project Manager',
          job_category: 'MANAGEMENT',
          job_level: 'MANAGER',
          description: 'プロジェクトの計画・実行・管理を統括する責任者',
          required_experience_years: 5,
          salary_grade_min: 5,
          salary_grade_max: 8,
          career_path: 'SE → リーダー → PM → 部門マネージャー',
          required_certifications: '["PMP", "プロジェクトマネージャ試験"]',
          required_skills: '["プロジェクト管理", "リーダーシップ", "コミュニケーション", "リスク管理"]',
          department_affinity: '["開発部", "PMO"]',
          remote_work_eligible: true,
          travel_frequency: 'MEDIUM',
          sort_order: 2,
          is_active: true,
        },
      }),
      prisma.jobType.upsert({
        where: { job_type_code: 'QA' },
        update: {},
        create: {
          job_type_code: 'QA',
          job_type_name: '品質保証エンジニア',
          job_type_name_en: 'Quality Assurance Engineer',
          job_category: 'ENGINEERING',
          job_level: 'SENIOR',
          description: 'ソフトウェアの品質保証・テスト設計・実行を担当',
          required_experience_years: 2,
          salary_grade_min: 3,
          salary_grade_max: 6,
          career_path: 'QA → シニアQA → QAリード → QAマネージャー',
          required_certifications: '["JSTQB", "ソフトウェア品質技術者資格"]',
          required_skills: '["テスト設計", "自動化テスト", "品質管理", "バグ分析"]',
          department_affinity: '["品質保証部", "開発部"]',
          remote_work_eligible: true,
          travel_frequency: 'NONE',
          sort_order: 3,
          is_active: true,
        },
      }),
    ])

    // MST_Roleデータ
    console.log('📊 MST_Roleデータを投入中...')
    const roleData = await Promise.all([
      prisma.role.upsert({
        where: { role_code: 'ROLE001' },
        update: {},
        create: {
          role_code: 'ROLE001',
          role_name: 'システム管理者',
          role_name_short: 'システム管理者',
          role_category: 'SYSTEM',
          role_level: 1,
          is_system_role: true,
          is_tenant_specific: false,
          max_users: 5,
          role_priority: 1,
          role_status: 'ACTIVE',
          effective_from: new Date('2025-01-01'),
          sort_order: 1,
          description: 'システム全体の管理権限を持つ最上位ロール',
        },
      }),
    ])

    // MST_Permissionデータ
    console.log('📊 MST_Permissionデータを投入中...')
    const permissionData = await Promise.all([
      prisma.permission.upsert({
        where: { permission_code: 'PERM_USER_READ' },
        update: {},
        create: {
          permission_code: 'PERM_USER_READ',
          permission_name: 'ユーザー情報参照',
          permission_name_short: 'ユーザー参照',
          permission_category: 'DATA',
          resource_type: 'USER',
          action_type: 'READ',
          scope_level: 'TENANT',
          is_system_permission: true,
          requires_conditions: false,
          risk_level: 1,
          requires_approval: false,
          audit_required: true,
          permission_status: 'ACTIVE',
          effective_from: new Date('2025-01-01'),
          sort_order: 1,
          description: 'ユーザー情報の参照権限',
        },
      }),
    ])

    // MST_SkillCategoryデータ
    console.log('📊 MST_SkillCategoryデータを投入中...')
    const skillCategoryData = await Promise.all([
      prisma.skillCategory.upsert({
        where: { category_code: 'CAT001' },
        update: {},
        create: {
          category_code: 'CAT001',
          category_name: 'プログラミング言語',
          category_name_short: 'プログラミング',
          category_name_en: 'Programming Languages',
          category_type: 'TECHNICAL',
          category_level: 1,
          category_path: '/プログラミング言語',
          is_system_category: true,
          is_leaf_category: false,
          skill_count: 25,
          evaluation_method: 'LEVEL',
          max_level: 5,
          icon_url: '/icons/programming.svg',
          color_code: '#007ACC',
          display_order: 1,
          is_popular: true,
          category_status: 'ACTIVE',
          effective_from: new Date('2025-01-01'),
          description: '各種プログラミング言語のスキル',
        },
      }),
      prisma.skillCategory.upsert({
        where: { category_code: 'CAT002' },
        update: {},
        create: {
          category_code: 'CAT002',
          category_name: 'Java',
          category_name_short: 'Java',
          category_name_en: 'Java',
          category_type: 'TECHNICAL',
          parent_category_id: 'CAT001',
          category_level: 2,
          category_path: '/プログラミング言語/Java',
          is_system_category: true,
          is_leaf_category: true,
          skill_count: 8,
          evaluation_method: 'LEVEL',
          max_level: 5,
          icon_url: '/icons/java.svg',
          color_code: '#ED8B00',
          display_order: 1,
          is_popular: true,
          category_status: 'ACTIVE',
          effective_from: new Date('2025-01-01'),
          description: 'Java言語に関するスキル',
        },
      }),
      prisma.skillCategory.upsert({
        where: { category_code: 'CAT003' },
        update: {},
        create: {
          category_code: 'CAT003',
          category_name: 'コミュニケーション',
          category_name_short: 'コミュニケーション',
          category_name_en: 'Communication',
          category_type: 'SOFT',
          category_level: 1,
          category_path: '/コミュニケーション',
          is_system_category: true,
          is_leaf_category: true,
          skill_count: 12,
          evaluation_method: 'LEVEL',
          max_level: 4,
          icon_url: '/icons/communication.svg',
          color_code: '#28A745',
          display_order: 10,
          is_popular: true,
          category_status: 'ACTIVE',
          effective_from: new Date('2025-01-01'),
          description: 'コミュニケーション能力に関するスキル',
        },
      }),
    ])

    // MST_SkillItemデータ
    console.log('📊 MST_SkillItemデータを投入中...')
    const skillItemData = await Promise.all([
      prisma.skillItem.upsert({
        where: { skill_code: 'SKILL001' },
        update: {},
        create: {
          skill_code: 'SKILL001',
          skill_name: 'Java',
          skill_category_id: 'CAT001',
          skill_type: 'TECHNICAL',
          difficulty_level: 3,
          importance_level: 4,
        },
      }),
    ])

    // MST_Skillデータ（詳細スキル情報）
    console.log('📊 MST_Skillデータを投入中...')
    const skillData = await Promise.all([
      prisma.skill.upsert({
        where: { id: 'SKILL001' },
        update: {},
        create: {
          id: 'SKILL001',
          skill_name: 'React',
          skill_name_en: 'React',
          category_id: 'CAT_FRONTEND',
          skill_type: 'TECHNICAL',
          difficulty_level: 3,
          description: 'Reactライブラリを使用したフロントエンド開発スキル。コンポーネント設計、状態管理、Hooksの理解が含まれます。',
          evaluation_criteria: '{"level1":"基本的なコンポーネント作成","level2":"状態管理とイベント処理","level3":"Hooks活用とパフォーマンス最適化","level4":"複雑なアプリケーション設計","level5":"ライブラリ開発とベストプラクティス"}',
          required_experience_months: 6,
          related_skills: '["SKILL002", "SKILL003", "SKILL004"]',
          prerequisite_skills: '["SKILL_JS001", "SKILL_HTML001"]',
          certification_info: '{"name":"React Developer Certification","provider":"Meta","url":"https://developers.facebook.com/certification/"}',
          learning_resources: '["https://reactjs.org/docs/","https://react.dev/learn","https://egghead.io/courses/react"]',
          market_demand: 'HIGH',
          technology_trend: 'GROWING',
          is_core_skill: true,
          display_order: 1,
          is_active: true,
          effective_from: new Date('2024-01-01'),
        },
      }),
      prisma.skill.upsert({
        where: { id: 'SKILL002' },
        update: {},
        create: {
          id: 'SKILL002',
          skill_name: 'TypeScript',
          skill_name_en: 'TypeScript',
          category_id: 'CAT_FRONTEND',
          skill_type: 'TECHNICAL',
          difficulty_level: 3,
          description: 'TypeScriptを使用した型安全なJavaScript開発スキル。型定義、ジェネリクス、高度な型操作が含まれます。',
          evaluation_criteria: '{"level1":"基本的な型定義","level2":"インターフェースとクラス","level3":"ジェネリクスと高度な型","level4":"型レベルプログラミング","level5":"ライブラリ型定義作成"}',
          required_experience_months: 4,
          related_skills: '["SKILL001", "SKILL003"]',
          prerequisite_skills: '["SKILL_JS001"]',
          learning_resources: '["https://www.typescriptlang.org/docs/","https://typescript-jp.gitbook.io/deep-dive/"]',
          market_demand: 'VERY_HIGH',
          technology_trend: 'GROWING',
          is_core_skill: true,
          display_order: 2,
          is_active: true,
          effective_from: new Date('2024-01-01'),
        },
      }),
      prisma.skill.upsert({
        where: { id: 'SKILL003' },
        update: {},
        create: {
          id: 'SKILL003',
          skill_name: 'Node.js',
          skill_name_en: 'Node.js',
          category_id: 'CAT_BACKEND',
          skill_type: 'TECHNICAL',
          difficulty_level: 3,
          description: 'Node.jsを使用したサーバーサイド開発スキル。非同期処理、API開発、パフォーマンス最適化が含まれます。',
          evaluation_criteria: '{"level1":"基本的なサーバー構築","level2":"Express.jsでのAPI開発","level3":"非同期処理とストリーム","level4":"パフォーマンス最適化","level5":"スケーラブルアーキテクチャ設計"}',
          required_experience_months: 8,
          related_skills: '["SKILL001", "SKILL002", "SKILL004"]',
          prerequisite_skills: '["SKILL_JS001"]',
          learning_resources: '["https://nodejs.org/en/docs/","https://expressjs.com/","https://nodeschool.io/"]',
          market_demand: 'HIGH',
          technology_trend: 'STABLE',
          is_core_skill: true,
          display_order: 1,
          is_active: true,
          effective_from: new Date('2024-01-01'),
        },
      }),
    ])

    // MST_Employeeデータ
    console.log('📊 MST_Employeeデータを投入中...')
    const employeeData = await Promise.all([
      prisma.employee.upsert({
        where: { id: 'emp_001' },
        update: {},
        create: {
          id: 'emp_001',
          employee_code: '000001',
          full_name: '笹尾 豊樹',
          full_name_kana: 'ササオ トヨキ',
          email: 'sasao.toyoki@example.com',
          phone: '090-1234-5678',
          hire_date: new Date('2020-04-01'),
          birth_date: new Date('1990-01-15'),
          gender: 'M',
          department_id: 'DEPT002',
          position_id: 'POS002',
          job_type_id: 'SE',
          employment_status: 'FULL_TIME',
          manager_id: 'emp_002',
          employee_status: 'ACTIVE',
        },
      }),
      prisma.employee.upsert({
        where: { id: 'emp_002' },
        update: {},
        create: {
          id: 'emp_002',
          employee_code: '000002',
          full_name: '佐藤花子',
          full_name_kana: 'サトウハナコ',
          email: 'sato.hanako@example.com',
          phone: '090-2345-6789',
          hire_date: new Date('2018-04-01'),
          birth_date: new Date('1985-03-20'),
          gender: 'F',
          department_id: 'DEPT001',
          position_id: 'POS002',
          job_type_id: 'PM',
          employment_status: 'FULL_TIME',
          employee_status: 'ACTIVE',
        },
      }),
    ])

    // MST_EmployeeDepartmentデータ
    console.log('📊 MST_EmployeeDepartmentデータを投入中...')
    const employeeDepartmentData = await Promise.all([
      prisma.employeeDepartment.upsert({
        where: { id: 'EMP_DEPT_001' },
        update: {},
        create: {
          id: 'EMP_DEPT_001',
          employee_id: '000001',
          department_id: 'DEPT001',
          assignment_type: 'PRIMARY',
          start_date: new Date('2020-04-01'),
          assignment_ratio: 100.0,
          role_in_department: 'チームリーダー',
          reporting_manager_id: 'EMP000010',
          assignment_reason: '新卒入社時配属',
          assignment_status: 'ACTIVE',
          approval_status: 'APPROVED',
          approved_by: 'EMP000010',
          approved_at: new Date('2020-03-25'),
        },
      }),
      prisma.employeeDepartment.upsert({
        where: { id: 'EMP_DEPT_002' },
        update: {},
        create: {
          id: 'EMP_DEPT_002',
          employee_id: '000002',
          department_id: 'DEPT002',
          assignment_type: 'PRIMARY',
          start_date: new Date('2021-04-01'),
          assignment_ratio: 80.0,
          role_in_department: '開発担当',
          reporting_manager_id: 'EMP000011',
          assignment_reason: '新卒入社時配属',
          assignment_status: 'ACTIVE',
          approval_status: 'APPROVED',
          approved_by: 'EMP000011',
          approved_at: new Date('2021-03-25'),
        },
      }),
    ])

    // MST_EmployeeJobTypeデータ
    console.log('📊 MST_EmployeeJobTypeデータを投入中...')
    const employeeJobTypeData = await Promise.all([
      prisma.employeeJobType.upsert({
        where: { id: 'EJT_001' },
        update: {},
        create: {
          id: 'EJT_001',
          employee_id: '000001',
          job_type_id: 'JOB_001',
          assignment_type: 'PRIMARY',
          assignment_ratio: 100.0,
          effective_start_date: new Date('2024-04-01'),
          assignment_reason: 'NEW_HIRE',
          assignment_status: 'ACTIVE',
          proficiency_level: 'INTERMEDIATE',
          target_proficiency_level: 'ADVANCED',
          target_achievement_date: new Date('2025-03-31'),
          certification_requirements: '["基本情報技術者試験", "AWS認定"]',
          skill_requirements: '["Java", "Spring Boot", "AWS", "Docker"]',
          experience_requirements: '["Webアプリケーション開発", "チーム開発"]',
          development_plan: '{"short_term": "AWS認定取得", "medium_term": "チームリーダー経験", "long_term": "アーキテクト昇格"}',
          training_plan: '["TRN_PROG_002", "TRN_PROG_006"]',
          mentor_id: 'EMP000010',
          supervisor_id: 'EMP000005',
          performance_rating: 'GOOD',
          last_evaluation_date: new Date('2024-03-31'),
          next_evaluation_date: new Date('2024-06-30'),
          evaluation_frequency: 'QUARTERLY',
          career_path: 'シニアエンジニア → テックリード → アーキテクト',
          strengths: '技術習得力、問題解決能力、チームワーク',
          improvement_areas: 'リーダーシップ、プレゼンテーション',
          achievements: '新人研修システム開発、パフォーマンス改善20%達成',
          goals: 'AWS認定取得、チームリーダー経験積む',
          workload_percentage: 100.0,
          billable_flag: true,
          cost_center: 'DEV001',
          budget_allocation: 5000000.0,
          hourly_rate: 3500.0,
          overtime_eligible: true,
          remote_work_eligible: true,
          travel_required: false,
          security_clearance_required: false,
          created_by: 'EMP000005',
          approved_by: 'EMP000008',
          approval_date: new Date('2024-03-25'),
          notes: '新卒採用、高いポテンシャルを持つ',
        },
      }),
    ])

    // MST_EmployeePositionデータ
    console.log('📊 MST_EmployeePositionデータを投入中...')
    const employeePositionData = await Promise.all([
      prisma.employeePosition.upsert({
        where: { id: 'EMP_POS_001' },
        update: {},
        create: {
          id: 'EMP_POS_001',
          employee_id: '000001',
          position_id: 'POS001',
          appointment_type: 'PRIMARY',
          start_date: new Date('2020-04-01'),
          appointment_reason: '新卒入社時任命',
          responsibility_scope: 'チーム運営、メンバー指導、プロジェクト管理',
          authority_level: 5,
          salary_grade: 'G5',
          appointment_status: 'ACTIVE',
          approval_status: 'APPROVED',
          approved_by: 'EMP000010',
          approved_at: new Date('2020-03-25'),
          performance_target: 'チーム生産性20%向上、メンバー育成2名',
          delegation_authority: '{"budget_approval": 1000000, "hiring_authority": true, "performance_evaluation": true}',
        },
      }),
    ])

    // MST_UserAuthデータ
    console.log('📊 MST_UserAuthデータを投入中...')
    
    // パスワードを正しくハッシュ化
    const passwordHash = await bcrypt.hash('password', 12);
    console.log('🔐 Generated password hash for "password":', passwordHash);
    
    const userAuthData = await Promise.all([
      prisma.userAuth.upsert({
        where: { user_id: 'USER000001' },
        update: {},
        create: {
          user_id: 'USER000001',
          login_id: '000001',
          password_hash: passwordHash,
          password_salt: 'randomsalt123',
          employee_id: '000001',
          account_status: 'ACTIVE',
          last_login_at: new Date('2025-06-01T09:00:00Z'),
          last_login_ip: '192.168.1.100',
          failed_login_count: 0,
          password_changed_at: new Date('2025-01-01T00:00:00Z'),
          password_expires_at: new Date('2025-12-31T23:59:59Z'),
          mfa_enabled: true,
          mfa_secret: 'JBSWY3DPEHPK3PXP',
          session_timeout: 480,
        },
      }),
      // テスト用ユーザー追加
      prisma.userAuth.upsert({
        where: { user_id: 'USER_TEST_EMPLOYEE' },
        update: {},
        create: {
          user_id: 'USER_TEST_EMPLOYEE',
          login_id: 'test-employee',
          password_hash: passwordHash,
          password_salt: 'testsalt123',
          employee_id: '000001',
          account_status: 'ACTIVE',
          last_login_at: new Date('2025-06-01T09:00:00Z'),
          last_login_ip: '192.168.1.100',
          failed_login_count: 0,
          password_changed_at: new Date('2025-01-01T00:00:00Z'),
          password_expires_at: new Date('2025-12-31T23:59:59Z'),
          mfa_enabled: false,
          session_timeout: 480,
        },
      }),
      prisma.userAuth.upsert({
        where: { user_id: 'USER000002' },
        update: {},
        create: {
          user_id: 'USER000002',
          login_id: '000002',
          password_hash: passwordHash,
          password_salt: 'randomsalt456',
          employee_id: '000002',
          account_status: 'ACTIVE',
          last_login_at: new Date('2025-06-01T10:30:00Z'),
          last_login_ip: '192.168.1.101',
          failed_login_count: 0,
          password_changed_at: new Date('2025-01-01T00:00:00Z'),
          password_expires_at: new Date('2025-12-31T23:59:59Z'),
          mfa_enabled: false,
          session_timeout: 480,
        },
      }),
    ])

    // MST_UserRoleデータ
    console.log('📊 MST_UserRoleデータを投入中...')
    const userRoleData = await Promise.all([
      prisma.userRole.upsert({
        where: { user_id_role_id: { user_id: 'USER000001', role_id: 'ROLE001' } },
        update: {},
        create: {
          id: 'USER_ROLE_001',
          user_id: 'USER000001',
          role_id: 'ROLE001',
          assignment_type: 'DIRECT',
          assigned_by: 'SYSTEM',
          assignment_reason: '新規ユーザー登録時の標準ロール割り当て',
          effective_from: new Date('2025-01-01T00:00:00Z'),
          is_primary_role: true,
          priority_order: 1,
          auto_assigned: true,
          requires_approval: false,
          assignment_status: 'ACTIVE',
          last_used_at: new Date('2025-06-01T09:00:00Z'),
          usage_count: 150,
        },
      }),
      prisma.userRole.upsert({
        where: { user_id_role_id: { user_id: 'USER000002', role_id: 'ROLE001' } },
        update: {},
        create: {
          id: 'USER_ROLE_002',
          user_id: 'USER000002',
          role_id: 'ROLE001',
          assignment_type: 'DIRECT',
          assigned_by: 'SYSTEM',
          assignment_reason: '新規ユーザー登録時の標準ロール割り当て',
          effective_from: new Date('2025-01-01T00:00:00Z'),
          is_primary_role: true,
          priority_order: 1,
          auto_assigned: true,
          requires_approval: false,
          assignment_status: 'ACTIVE',
          last_used_at: new Date('2025-06-01T10:30:00Z'),
          usage_count: 85,
        },
      }),
    ])

    // TRN_SkillRecordデータ
    console.log('📊 TRN_SkillRecordデータを投入中...')
    const skillRecordData = await Promise.all([
      prisma.skillRecord.upsert({
        where: { employee_id_skill_item_id: { employee_id: '000001', skill_item_id: 'SKILL001' } },
        update: {},
        create: {
          id: 'SR_EMP000001_SKILL001',
          employee_id: '000001',
          skill_item_id: 'SKILL001',
          skill_level: 4,
          self_assessment: 4,
          manager_assessment: 3,
          evidence_description: 'Javaを使用したWebアプリケーション開発プロジェクトを3件担当',
          acquisition_date: new Date('2020-06-01'),
          last_used_date: new Date('2025-05-30'),
          skill_category_id: 'CAT001',
          assessment_date: new Date('2025-04-01'),
          assessor_id: 'EMP000010',
          skill_status: 'ACTIVE',
          learning_hours: 120,
          project_experience_count: 3,
          tenant_id: 'tenant_001',
          created_by: 'USER000001',
          updated_by: 'USER000001',
        },
      }),
      prisma.skillRecord.upsert({
        where: { employee_id_skill_item_id: { employee_id: '000002', skill_item_id: 'SKILL001' } },
        update: {},
        create: {
          id: 'SR_EMP000002_SKILL001',
          employee_id: '000002',
          skill_item_id: 'SKILL001',
          skill_level: 3,
          self_assessment: 3,
          manager_assessment: 3,
          evidence_description: 'Javaを使用したWebアプリケーション開発プロジェクトを2件担当',
          acquisition_date: new Date('2018-08-01'),
          last_used_date: new Date('2025-05-25'),
          skill_category_id: 'CAT001',
          assessment_date: new Date('2025-04-01'),
          assessor_id: 'EMP000010',
          skill_status: 'ACTIVE',
          learning_hours: 80,
          project_experience_count: 2,
          tenant_id: 'tenant_001',
          created_by: 'USER000002',
          updated_by: 'USER000002',
        },
      }),
    ])

    // TRN_ProjectRecordデータ（作業実績）
    console.log('📊 TRN_ProjectRecordデータを投入中...')
    const projectRecordData = await Promise.all([
      prisma.projectRecord.upsert({
        where: { id: 'PR_001' },
        update: {},
        create: {
          id: 'PR_001',
          project_record_id: 'PR_EMP000001_001',
          employee_id: '000001',
          project_name: 'スキル報告書WEBシステム開発',
          project_code: 'SKILL-WEB-2024',
          client_name: '社内システム',
          project_type: 'WEB_APPLICATION',
          project_scale: 'MEDIUM',
          start_date: new Date('2024-01-15'),
          end_date: new Date('2024-12-31'),
          participation_rate: 80.0,
          role_title: 'フロントエンドエンジニア',
          responsibilities: 'React/TypeScriptによるUI開発、API連携、テスト作成',
          technologies_used: 'React, TypeScript, Next.js, Tailwind CSS, Prisma',
          skills_applied: 'フロントエンド開発, UI/UX設計, API設計',
          achievements: '新機能30件実装、ページ表示速度40%向上、テストカバレッジ85%達成',
          challenges_faced: 'レスポンシブ対応、パフォーマンス最適化、多言語対応',
          lessons_learned: 'React 18の新機能活用、TypeScriptの型安全性向上',
          team_size: 8,
          budget_range: '5000-10000万円',
          project_status: 'ACTIVE',
          evaluation_score: 4.0,
          evaluation_comment: 'パフォーマンス向上とテストカバレッジ達成が評価された',
          tenant_id: 'tenant_001',
          created_by: 'USER000001',
          updated_by: 'USER000001',
        },
      }),
      prisma.projectRecord.upsert({
        where: { id: 'PR_002' },
        update: {},
        create: {
          id: 'PR_002',
          project_record_id: 'PR_EMP000001_002',
          employee_id: '000001',
          project_name: 'レガシーシステム移行プロジェクト',
          project_code: 'LEGACY-MIG-2023',
          client_name: 'A社',
          project_type: 'SYSTEM_MIGRATION',
          project_scale: 'LARGE',
          start_date: new Date('2023-04-01'),
          end_date: new Date('2023-11-30'),
          participation_rate: 60.0,
          role_title: 'システムエンジニア',
          responsibilities: 'データ移行設計、テスト設計・実行、ドキュメント作成',
          technologies_used: 'Java, Spring Boot, PostgreSQL, Docker',
          skills_applied: 'システム設計, データベース設計, テスト設計',
          achievements: 'データ移行100%成功、性能要件クリア、予定より1週間早期完了',
          challenges_faced: 'データ整合性確保、性能チューニング、スケジュール調整',
          lessons_learned: 'データ移行のベストプラクティス習得、チーム連携の重要性',
          team_size: 12,
          budget_range: '1-5億円',
          project_status: 'COMPLETED',
          evaluation_score: 5.0,
          evaluation_comment: '予定より早期完了し顧客満足度も高い優秀なプロジェクト',
          tenant_id: 'tenant_001',
          created_by: 'USER000001',
          updated_by: 'USER000001',
        },
      }),
    ])

    // TRN_GoalProgressデータ（キャリア目標）
    console.log('📊 TRN_GoalProgressデータを投入中...')
    const goalProgressData = await Promise.all([
      prisma.goalProgress.upsert({
        where: { id: 'GP_001' },
        update: {},
        create: {
          id: 'GP_001',
          goal_id: 'GOAL_001',
          employee_id: '000001',
          goal_title: 'AWS認定ソリューションアーキテクト取得',
          goal_description: 'クラウドアーキテクチャの知識向上とキャリアアップのため',
          goal_category: 'CERTIFICATION',
          goal_type: 'SKILL_DEVELOPMENT',
          priority_level: 'HIGH',
          target_value: 1.0,
          current_value: 0.75,
          unit: '合格',
          start_date: new Date('2025-01-01'),
          target_date: new Date('2025-06-30'),
          progress_rate: 75.0,
          achievement_status: 'IN_PROGRESS',
          supervisor_id: 'EMP000010',
          approval_status: 'APPROVED',
          approved_at: new Date('2025-01-05'),
          approved_by: 'EMP000010',
          tenant_id: 'tenant_001',
          created_by: 'USER000001',
          updated_by: 'USER000001',
        },
      }),
      prisma.goalProgress.upsert({
        where: { id: 'GP_002' },
        update: {},
        create: {
          id: 'GP_002',
          goal_id: 'GOAL_002',
          employee_id: '000001',
          goal_title: 'チームリーダー経験の蓄積',
          goal_description: '小規模プロジェクトでのリーダーシップ経験を積む',
          goal_category: 'CAREER_DEVELOPMENT',
          goal_type: 'LEADERSHIP',
          priority_level: 'MEDIUM',
          target_value: 1.0,
          current_value: 0.4,
          unit: 'プロジェクト',
          start_date: new Date('2025-01-01'),
          target_date: new Date('2025-12-31'),
          progress_rate: 40.0,
          achievement_status: 'IN_PROGRESS',
          supervisor_id: 'EMP000010',
          approval_status: 'APPROVED',
          approved_at: new Date('2025-01-05'),
          approved_by: 'EMP000010',
          tenant_id: 'tenant_001',
          created_by: 'USER000001',
          updated_by: 'USER000001',
        },
      }),
    ])

    // MST_TrainingProgramデータ（研修プログラム）
    console.log('📊 MST_TrainingProgramデータを投入中...')
    const trainingProgramData = await Promise.all([
      prisma.trainingProgram.upsert({
        where: { training_program_id: 'TRN_PROG_001' },
        update: {},
        create: {
          training_program_id: 'TRN_PROG_001',
          program_code: 'AWS-SAA',
          program_name: 'AWS Solutions Architect Associate 認定対策',
          program_name_en: 'AWS Solutions Architect Associate Certification',
          program_description: 'AWS上でのソリューション設計・構築スキルを習得する研修',
          program_category: 'CERTIFICATION',
          program_type: 'ONLINE',
          target_audience: 'エンジニア',
          difficulty_level: 'INTERMEDIATE',
          duration_hours: 40.0,
          duration_days: 5,
          max_participants: 20,
          min_participants: 5,
          prerequisites: 'AWS基礎知識、1年以上のクラウド経験',
          learning_objectives: 'AWS認定試験合格、ソリューション設計力向上',
          curriculum_outline: 'EC2、S3、RDS、VPC、セキュリティ、監視',
          cost_per_participant: 150000.0,
          external_provider: 'AWS トレーニングパートナー',
          certification_provided: true,
          pdu_credits: 40.0,
          created_by: 'ADMIN',
        },
      }),
      prisma.trainingProgram.upsert({
        where: { training_program_id: 'TRN_PROG_002' },
        update: {},
        create: {
          training_program_id: 'TRN_PROG_002',
          program_code: 'REACT-ADV',
          program_name: 'React.js 実践開発研修',
          program_name_en: 'React.js Advanced Development Training',
          program_description: 'React.jsを使った実践的なWebアプリケーション開発研修',
          program_category: 'TECHNICAL',
          program_type: 'HANDS_ON',
          target_audience: 'フロントエンドエンジニア',
          difficulty_level: 'ADVANCED',
          duration_hours: 24.0,
          duration_days: 3,
          max_participants: 15,
          min_participants: 8,
          prerequisites: 'JavaScript ES6+、HTML/CSS、Git基礎',
          learning_objectives: 'React.js上級機能習得、実践的な開発経験',
          curriculum_outline: 'Hooks、Context API、パフォーマンス最適化、テスト',
          cost_per_participant: 98000.0,
          external_provider: '社内研修センター',
          certification_provided: false,
          created_by: 'ADMIN',
        },
      }),
    ])

    // TRN_TrainingHistoryデータ（研修履歴）
    console.log('📊 TRN_TrainingHistoryデータを投入中...')
    const trainingHistoryData = await Promise.all([
      prisma.trainingHistory.upsert({
        where: { id: 'TH_001' },
        update: {},
        create: {
          id: 'TH_001',
          training_history_id: 'TH_EMP000001_001',
          employee_id: '000001',
          training_program_id: 'TRN_PROG_001',
          training_name: 'AWS Solutions Architect Associate 認定対策',
          training_type: 'CERTIFICATION',
          training_category: 'CLOUD',
          provider_name: 'AWS トレーニングパートナー',
          instructor_name: '田中 太郎',
          start_date: new Date('2024-09-01'),
          end_date: new Date('2024-09-05'),
          duration_hours: 40.0,
          location: 'オンライン',
          cost: 150000.0,
          cost_covered_by: 'COMPANY',
          attendance_status: 'COMPLETED',
          completion_rate: 100.0,
          test_score: 850.0,
          grade: 'PASS',
          certificate_obtained: true,
          certificate_number: 'AWS-SAA-2024-000123',
          pdu_earned: 40.0,
          skills_acquired: 'AWS設計、セキュリティ、監視',
          learning_objectives: 'AWS認定試験合格、ソリューション設計力向上',
          learning_outcomes: 'AWS上での3層アーキテクチャ設計が可能になった',
          feedback: '実践的な演習が多く、理解が深まった。講師の説明も分かりやすかった。',
          satisfaction_score: 4.5,
          recommendation_score: 4.0,
          follow_up_required: false,
          tenant_id: 'tenant_001',
          created_by: 'USER000001',
          updated_by: 'USER000001',
        },
      }),
      prisma.trainingHistory.upsert({
        where: { id: 'TH_002' },
        update: {},
        create: {
          id: 'TH_002',
          training_history_id: 'TH_EMP000001_002',
          employee_id: '000001',
          training_program_id: 'TRN_PROG_002',
          training_name: 'React.js 実践開発研修',
          training_type: 'TECHNICAL',
          training_category: 'FRONTEND',
          provider_name: '社内研修センター',
          instructor_name: '佐藤 花子',
          start_date: new Date('2024-11-10'),
          end_date: new Date('2024-11-12'),
          duration_hours: 24.0,
          location: '本社研修室A',
          cost: 98000.0,
          cost_covered_by: 'COMPANY',
          attendance_status: 'COMPLETED',
          completion_rate: 100.0,
          test_score: 92.0,
          grade: 'EXCELLENT',
          certificate_obtained: false,
          skills_acquired: 'React Hooks、パフォーマンス最適化、テスト',
          learning_objectives: 'React.js上級機能習得、実践的な開発経験',
          learning_outcomes: '既存プロジェクトのパフォーマンスを20%改善できた',
          feedback: 'ハンズオン中心で実践的。同僚との情報共有も有意義だった。',
          satisfaction_score: 4.8,
          recommendation_score: 5.0,
          follow_up_required: true,
          follow_up_date: new Date('2024-12-15'),
          tenant_id: 'tenant_001',
          created_by: 'USER000001',
          updated_by: 'USER000001',
        },
      }),
    ])

    // HIS_AuditLogデータ（更新履歴）
    console.log('📊 HIS_AuditLogデータを投入中...')
    const auditLogData = await Promise.all([
      prisma.auditLog.upsert({
        where: { id: 'AUDIT_001' },
        update: {},
        create: {
          id: 'AUDIT_001',
          user_id: '000001',
          session_id: 'session_001',
          action_type: 'UPDATE',
          target_table: 'Employee',
          target_id: '000001',
          old_values: '{"department_id": "DEPT001"}',
          new_values: '{"department_id": "DEPT002"}',
          ip_address: '192.168.1.100',
          user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          result_status: 'SUCCESS',
          execution_time_ms: 150,
          is_deleted: false,
          tenant_id: 'tenant_001',
          created_at: new Date('2025-06-01T09:15:00Z'),
          updated_at: new Date('2025-06-01T09:15:00Z'),
          created_by: '000001',
          updated_by: '000001',
        },
      }),
      prisma.auditLog.upsert({
        where: { id: 'AUDIT_002' },
        update: {},
        create: {
          id: 'AUDIT_002',
          user_id: '000001',
          session_id: 'session_002',
          action_type: 'UPDATE',
          target_table: 'Employee',
          target_id: '000001',
          old_values: '{"position_id": "POS003"}',
          new_values: '{"position_id": "POS002"}',
          ip_address: '192.168.1.100',
          user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          result_status: 'SUCCESS',
          execution_time_ms: 120,
          is_deleted: false,
          tenant_id: 'tenant_001',
          created_at: new Date('2025-05-15T14:30:00Z'),
          updated_at: new Date('2025-05-15T14:30:00Z'),
          created_by: '000001',
          updated_by: '000001',
        },
      }),
      prisma.auditLog.upsert({
        where: { id: 'AUDIT_003' },
        update: {},
        create: {
          id: 'AUDIT_003',
          user_id: '000001',
          session_id: 'session_003',
          action_type: 'UPDATE',
          target_table: 'Employee',
          target_id: '000001',
          old_values: '{"full_name": "笹尾豊樹"}',
          new_values: '{"full_name": "笹尾 豊樹"}',
          ip_address: '192.168.1.100',
          user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          result_status: 'SUCCESS',
          execution_time_ms: 95,
          is_deleted: false,
          tenant_id: 'tenant_001',
          created_at: new Date('2025-07-01T11:20:00Z'),
          updated_at: new Date('2025-07-01T11:20:00Z'),
          created_by: '000001',
          updated_by: '000001',
        },
      }),
      prisma.auditLog.upsert({
        where: { id: 'AUDIT_004' },
        update: {},
        create: {
          id: 'AUDIT_004',
          user_id: '000001',
          session_id: 'session_004',
          action_type: 'UPDATE',
          target_table: 'Employee',
          target_id: '000001',
          old_values: '{"email": "sasao.toyoki.old@example.com"}',
          new_values: '{"email": "sasao.toyoki@example.com"}',
          ip_address: '192.168.1.100',
          user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          result_status: 'SUCCESS',
          execution_time_ms: 110,
          is_deleted: false,
          tenant_id: 'tenant_001',
          created_at: new Date('2025-06-20T15:45:00Z'),
          updated_at: new Date('2025-06-20T15:45:00Z'),
          created_by: '000001',
          updated_by: '000001',
        },
      }),
      prisma.auditLog.upsert({
        where: { id: 'AUDIT_005' },
        update: {},
        create: {
          id: 'AUDIT_005',
          user_id: '000002',
          session_id: 'session_005',
          action_type: 'UPDATE',
          target_table: 'Employee',
          target_id: '000002',
          old_values: '{"phone": "090-2345-6788"}',
          new_values: '{"phone": "090-2345-6789"}',
          ip_address: '192.168.1.101',
          user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          result_status: 'SUCCESS',
          execution_time_ms: 85,
          is_deleted: false,
          tenant_id: 'tenant_001',
          created_at: new Date('2025-06-15T13:30:00Z'),
          updated_at: new Date('2025-06-15T13:30:00Z'),
          created_by: '000002',
          updated_by: '000002',
        },
      }),
    ])

    console.log('✅ データベースの初期データ投入が完了しました！')
    console.log('📋 投入されたデータの詳細:')
    console.log('   - テナント: 2件')
    console.log('   - 部署: 2件')
    console.log('   - 役職: 3件')
    console.log('   - 職種: 3件')
    console.log('   - ロール: 1件')
    console.log('   - 権限: 1件')
    console.log('   - スキルカテゴリ: 3件')
    console.log('   - スキル項目: 1件')
    console.log('   - スキル詳細: 3件')
    console.log('   - 社員: 2件')
    console.log('   - 社員部署配属: 2件')
    console.log('   - 社員職種配属: 1件')
    console.log('   - 社員役職配属: 1件')
    console.log('   - ユーザー認証: 2件')
    console.log('   - ユーザーロール: 2件')
    console.log('   - スキル記録: 2件')
    console.log('   - プロジェクト記録: 2件')
    console.log('   - キャリア目標: 2件')
    console.log('   - 研修プログラム: 2件')
    console.log('   - 研修履歴: 2件')
    console.log('   - 監査ログ: 5件')
    console.log('')
    console.log('🔐 ログイン情報:')
    console.log('   テストユーザー（推奨）:')
    console.log('     ユーザーID: test-employee')
    console.log('     パスワード: password')
    console.log('   テストユーザー1:')
    console.log('     ユーザーID: 000001')
    console.log('     パスワード: password')
    console.log('   テストユーザー2:')
    console.log('     ユーザーID: 000002')
    console.log('     パスワード: password')

  } catch (error) {
    console.error('❌ 初期データ投入中にエラーが発生しました:', error)
    throw error
  }
}

if (require.main === module) {
  runSampleSeed()
    .then(async () => {
      await prisma.$disconnect()
    })
    .catch(async (e) => {
      console.error('❌ 初期データ投入中にエラーが発生しました:', e)
      await prisma.$disconnect()
      throw e
    })
}
