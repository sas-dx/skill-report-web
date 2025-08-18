// @ts-nocheck
import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

export async function runWorkingSeed() {
  console.log('🌱 実動版マスタデータ投入を開始します...')

  let successCount = 0;
  let errorCount = 0;

  try {
    // パスワードハッシュ生成
    const passwordHash = await bcrypt.hash('password', 12);
    console.log('🔐 パスワードハッシュを生成しました');

    // ========================================
    // 基本マスタデータ（存在確認済み）
    // ========================================

    // 1. MST_Tenant
    try {
      console.log('📊 MST_Tenantデータを投入中...')
      await prisma.tenant.upsert({
        where: { tenant_id: 'default-tenant' },
        update: {},
        create: {
          tenant_id: 'default-tenant',
          tenant_code: 'DEFAULT',
          tenant_name: 'デフォルトテナント',
        },
      });
      successCount++;
    } catch (e) {
      console.log('  ⚠️ Tenantテーブルスキップ:', e.message);
      errorCount++;
    }

    // 2. MST_Department（部署）
    console.log('📊 MST_Departmentデータを投入中...')
    const departments = [
      { code: 'DEPT001', name: '経営企画部' },
      { code: 'DEPT002', name: 'システム開発部' },
      { code: 'DEPT003', name: '営業部' },
      { code: 'DEPT004', name: '人事部' },
      { code: 'DEPT005', name: '総務部' },
    ];
    for (const dept of departments) {
      try {
        await prisma.department.upsert({
          where: { department_code: dept.code },
          update: {},
          create: {
            department_code: dept.code,
            department_name: dept.name,
          },
        });
        successCount++;
      } catch (e) {
        console.log(`  ⚠️ Department ${dept.code} スキップ`);
        errorCount++;
      }
    }

    // 3. MST_Position（役職）
    console.log('📊 MST_Positionデータを投入中...')
    const positions = [
      { code: 'POS001', name: '社長' },
      { code: 'POS002', name: '取締役' },
      { code: 'POS003', name: '部長' },
      { code: 'POS004', name: '課長' },
      { code: 'POS005', name: '主任' },
      { code: 'POS006', name: '一般社員' },
    ];
    for (const pos of positions) {
      try {
        await prisma.position.upsert({
          where: { position_code: pos.code },
          update: {},
          create: {
            position_code: pos.code,
            position_name: pos.name,
          },
        });
        successCount++;
      } catch (e) {
        console.log(`  ⚠️ Position ${pos.code} スキップ`);
        errorCount++;
      }
    }

    // 4. MST_JobType（職種）
    console.log('📊 MST_JobTypeデータを投入中...')
    const jobTypes = [
      { code: 'SE', name: 'システムエンジニア' },
      { code: 'PM', name: 'プロジェクトマネージャー' },
      { code: 'PG', name: 'プログラマー' },
      { code: 'SA', name: 'システムアーキテクト' },
      { code: 'QA', name: '品質保証' },
    ];
    for (const job of jobTypes) {
      try {
        await prisma.jobType.upsert({
          where: { job_type_code: job.code },
          update: {},
          create: {
            job_type_code: job.code,
            job_type_name: job.name,
          },
        });
        successCount++;
      } catch (e) {
        console.log(`  ⚠️ JobType ${job.code} スキップ`);
        errorCount++;
      }
    }

    // 5. MST_Role（ロール）
    console.log('📊 MST_Roleデータを投入中...')
    const roles = [
      { code: 'ADMIN', name: '管理者' },
      { code: 'USER', name: '一般ユーザー' },
      { code: 'MANAGER', name: 'マネージャー' },
      { code: 'HR', name: '人事' },
      { code: 'VIEWER', name: '閲覧者' },
    ];
    for (const role of roles) {
      try {
        await prisma.role.upsert({
          where: { role_code: role.code },
          update: {},
          create: {
            role_code: role.code,
            role_name: role.name,
          },
        });
        successCount++;
      } catch (e) {
        console.log(`  ⚠️ Role ${role.code} スキップ`);
        errorCount++;
      }
    }

    // 6. MST_Permission（権限）
    console.log('📊 MST_Permissionデータを投入中...')
    const permissions = [
      { code: 'VIEW_ALL', name: '全データ閲覧' },
      { code: 'EDIT_ALL', name: '全データ編集' },
      { code: 'APPROVE', name: '承認' },
      { code: 'VIEW_OWN', name: '自データ閲覧' },
      { code: 'EDIT_OWN', name: '自データ編集' },
      { code: 'EXPORT', name: 'エクスポート' },
      { code: 'IMPORT', name: 'インポート' },
    ];
    for (const perm of permissions) {
      try {
        await prisma.permission.upsert({
          where: { permission_code: perm.code },
          update: {},
          create: {
            permission_code: perm.code,
            permission_name: perm.name,
          },
        });
        successCount++;
      } catch (e) {
        console.log(`  ⚠️ Permission ${perm.code} スキップ`);
        errorCount++;
      }
    }

    // ========================================
    // スキル関連マスタ
    // ========================================

    // 7. MST_SkillCategory（スキルカテゴリ）
    console.log('📊 MST_SkillCategoryデータを投入中...')
    const skillCategories = [
      { code: 'CAT001', name: 'プログラミング言語', status: 'active' },
      { code: 'CAT002', name: 'フレームワーク', status: 'active' },
      { code: 'CAT003', name: 'データベース', status: 'active' },
      { code: 'CAT004', name: 'クラウドサービス', status: 'active' },
      { code: 'CAT005', name: 'プロジェクト管理', status: 'active' },
      { code: 'CAT006', name: 'ビジネススキル', status: 'active' },
      { code: 'CAT007', name: 'ツール', status: 'active' },
    ];
    for (const cat of skillCategories) {
      try {
        await prisma.skillCategory.upsert({
          where: { category_code: cat.code },
          update: {},
          create: {
            category_code: cat.code,
            category_name: cat.name,
          },
        });
        successCount++;
      } catch (e) {
        console.log(`  ⚠️ SkillCategory ${cat.code} スキップ`);
        errorCount++;
      }
    }

    // 8. MST_SkillGrade（スキルグレード）
    console.log('📊 MST_SkillGradeデータを投入中...')
    const skillGrades = [
      { code: 'GRADE1', name: '初級', level: 1 },
      { code: 'GRADE2', name: '中級', level: 2 },
      { code: 'GRADE3', name: '上級', level: 3 },
      { code: 'GRADE4', name: 'エキスパート', level: 4 },
      { code: 'GRADE5', name: 'マスター', level: 5 },
    ];
    for (const grade of skillGrades) {
      try {
        await prisma.skillGrade.upsert({
          where: { grade_code: grade.code },
          update: {},
          create: {
            grade_code: grade.code,
            grade_name: grade.name,
            grade_level: grade.level,
          },
        });
        successCount++;
      } catch (e) {
        console.log(`  ⚠️ SkillGrade ${grade.code} スキップ`);
        errorCount++;
      }
    }

    // 9. MST_SkillItem（スキル項目）
    console.log('📊 MST_SkillItemデータを投入中...')
    const skillItems = [
      // プログラミング言語
      { code: 'SKILL001', name: 'Java', category: 'CAT001' },
      { code: 'SKILL002', name: 'Python', category: 'CAT001' },
      { code: 'SKILL003', name: 'JavaScript', category: 'CAT001' },
      { code: 'SKILL004', name: 'TypeScript', category: 'CAT001' },
      { code: 'SKILL005', name: 'C#', category: 'CAT001' },
      { code: 'SKILL006', name: 'Go', category: 'CAT001' },
      { code: 'SKILL007', name: 'Ruby', category: 'CAT001' },
      { code: 'SKILL008', name: 'PHP', category: 'CAT001' },
      // フレームワーク
      { code: 'SKILL009', name: 'Spring Boot', category: 'CAT002' },
      { code: 'SKILL010', name: 'React', category: 'CAT002' },
      { code: 'SKILL011', name: 'Next.js', category: 'CAT002' },
      { code: 'SKILL012', name: 'Vue.js', category: 'CAT002' },
      { code: 'SKILL013', name: 'Angular', category: 'CAT002' },
      { code: 'SKILL014', name: 'Express.js', category: 'CAT002' },
      { code: 'SKILL015', name: 'Django', category: 'CAT002' },
      // データベース
      { code: 'SKILL016', name: 'PostgreSQL', category: 'CAT003' },
      { code: 'SKILL017', name: 'MySQL', category: 'CAT003' },
      { code: 'SKILL018', name: 'Oracle', category: 'CAT003' },
      { code: 'SKILL019', name: 'MongoDB', category: 'CAT003' },
      { code: 'SKILL020', name: 'Redis', category: 'CAT003' },
      // クラウドサービス
      { code: 'SKILL021', name: 'AWS', category: 'CAT004' },
      { code: 'SKILL022', name: 'Azure', category: 'CAT004' },
      { code: 'SKILL023', name: 'GCP', category: 'CAT004' },
      { code: 'SKILL024', name: 'Docker', category: 'CAT004' },
      { code: 'SKILL025', name: 'Kubernetes', category: 'CAT004' },
      // プロジェクト管理
      { code: 'SKILL026', name: 'スクラム', category: 'CAT005' },
      { code: 'SKILL027', name: 'ウォーターフォール', category: 'CAT005' },
      { code: 'SKILL028', name: 'アジャイル', category: 'CAT005' },
      // ビジネススキル
      { code: 'SKILL029', name: 'プレゼンテーション', category: 'CAT006' },
      { code: 'SKILL030', name: 'ドキュメント作成', category: 'CAT006' },
      // ツール
      { code: 'SKILL031', name: 'Git', category: 'CAT007' },
      { code: 'SKILL032', name: 'JIRA', category: 'CAT007' },
      { code: 'SKILL033', name: 'Slack', category: 'CAT007' },
    ];
    for (const skill of skillItems) {
      try {
        await prisma.skillItem.upsert({
          where: { skill_code: skill.code },
          update: {},
          create: {
            skill_code: skill.code,
            skill_name: skill.name,
            skill_category_id: skill.category,
          },
        });
        successCount++;
      } catch (e) {
        console.log(`  ⚠️ SkillItem ${skill.code} スキップ`);
        errorCount++;
      }
    }

    // ========================================
    // 研修関連マスタ（存在するもののみ）
    // ========================================

    // 10. MST_TrainingProgram（研修プログラム）
    console.log('📊 MST_TrainingProgramデータを投入中...')
    const trainingPrograms = [
      {
        program_code: 'PROG001',
        program_name: '新人研修',
        program_description: '新入社員向け基礎研修',
        duration_days: 30,
        max_participants: 20,
        is_mandatory: true,
      },
      {
        program_code: 'PROG002',
        program_name: 'Java開発研修',
        program_description: 'Java開発スキル向上研修',
        duration_days: 5,
        max_participants: 15,
        is_mandatory: false,
      },
      {
        program_code: 'PROG003',
        program_name: 'AWS認定研修',
        program_description: 'AWS認定資格取得研修',
        duration_days: 3,
        max_participants: 10,
        is_mandatory: false,
      },
      {
        program_code: 'PROG004',
        program_name: 'リーダーシップ研修',
        program_description: '管理職向けリーダーシップ研修',
        duration_days: 2,
        max_participants: 12,
        is_mandatory: false,
      },
    ];
    for (const prog of trainingPrograms) {
      try {
        await prisma.trainingProgram.upsert({
          where: { program_code: prog.program_code },
          update: {},
          create: {
            program_code: prog.program_code,
            program_name: prog.program_name,
            program_description: prog.program_description,
            duration_days: prog.duration_days,
            max_participants: prog.max_participants,
            is_mandatory: prog.is_mandatory,
          },
        });
        successCount++;
      } catch (e) {
        console.log(`  ⚠️ TrainingProgram ${prog.program_code} スキップ`);
        errorCount++;
      }
    }

    // ========================================
    // 資格関連マスタ（存在するもののみ）
    // ========================================

    // 11. MST_Certification（資格）
    console.log('📊 MST_Certificationデータを投入中...')
    const certifications = [
      {
        certification_code: 'CERT001',
        certification_name: '基本情報技術者',
        certification_description: 'ITエンジニアの基礎資格',
        validity_years: null,
      },
      {
        certification_code: 'CERT002',
        certification_name: '応用情報技術者',
        certification_description: 'ITエンジニアの応用資格',
        validity_years: null,
      },
      {
        certification_code: 'CERT003',
        certification_name: 'プロジェクトマネージャ',
        certification_description: 'PM向け国家資格',
        validity_years: null,
      },
      {
        certification_code: 'CERT004',
        certification_name: 'AWS Certified Solutions Architect',
        certification_description: 'AWS認定ソリューションアーキテクト',
        validity_years: 3,
      },
      {
        certification_code: 'CERT005',
        certification_name: 'Azure Administrator',
        certification_description: 'Azure管理者認定',
        validity_years: 2,
      },
      {
        certification_code: 'CERT006',
        certification_name: 'TOEIC 700点以上',
        certification_description: '英語能力試験',
        validity_years: 2,
      },
    ];
    for (const cert of certifications) {
      try {
        await prisma.certification.upsert({
          where: { certification_code: cert.certification_code },
          update: {},
          create: {
            certification_code: cert.certification_code,
            certification_name: cert.certification_name,
            certification_description: cert.certification_description,
            validity_years: cert.validity_years,
          },
        });
        successCount++;
      } catch (e) {
        console.log(`  ⚠️ Certification ${cert.certification_code} スキップ`);
        errorCount++;
      }
    }

    // ========================================
    // 従業員とユーザー認証
    // ========================================

    console.log('📊 MST_Employeeデータを投入中...')
    const employees = [
      {
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
        position_id: 'POS004',
        job_type_id: 'SE',
        employment_status: 'FULL_TIME',
        employee_status: 'ACTIVE',
        manager_id: 'emp_002',  // 佐藤花子が上長
      },
      {
        id: 'emp_002',
        employee_code: '000002',
        full_name: '佐藤 花子',
        full_name_kana: 'サトウ ハナコ',
        email: 'sato.hanako@example.com',
        phone: '090-2345-6789',
        hire_date: new Date('2018-04-01'),
        birth_date: new Date('1985-03-20'),
        gender: 'F',
        department_id: 'DEPT002',  // システム開発部に変更
        position_id: 'POS003',  // 部長
        job_type_id: 'PM',
        employment_status: 'FULL_TIME',
        employee_status: 'ACTIVE',
        // manager_idなし（部長なので上長なし）
      },
      {
        id: 'emp_003',
        employee_code: '000003',
        full_name: '山田 太郎',
        full_name_kana: 'ヤマダ タロウ',
        email: 'yamada.taro@example.com',
        phone: '090-3456-7890',
        hire_date: new Date('2022-04-01'),
        birth_date: new Date('1998-07-10'),
        gender: 'M',
        department_id: 'DEPT002',
        position_id: 'POS006',
        job_type_id: 'PG',
        employment_status: 'FULL_TIME',
        employee_status: 'ACTIVE',
        manager_id: 'emp_001',  // 笹尾豊樹が上長
      },
      {
        id: 'emp_004',
        employee_code: '000004',
        full_name: '田中 美咲',
        full_name_kana: 'タナカ ミサキ',
        email: 'tanaka.misaki@example.com',
        phone: '090-4567-8901',
        hire_date: new Date('2021-04-01'),
        birth_date: new Date('1995-12-25'),
        gender: 'F',
        department_id: 'DEPT003',
        position_id: 'POS005',
        job_type_id: 'SE',
        employment_status: 'FULL_TIME',
        employee_status: 'ACTIVE',
        manager_id: 'emp_002',  // 佐藤花子が上長
      },
      {
        id: 'emp_test',
        employee_code: 'test-employee',
        full_name: 'テスト ユーザー',
        full_name_kana: 'テスト ユーザー',
        email: 'test@example.com',
        phone: '090-0000-0000',
        hire_date: new Date('2025-01-01'),
        birth_date: new Date('1995-01-01'),
        gender: 'M',
        department_id: 'DEPT002',
        position_id: 'POS005',
        job_type_id: 'SE',
        employment_status: 'FULL_TIME',
        employee_status: 'ACTIVE',
        manager_id: 'emp_001',  // 笹尾豊樹が上長
      },
    ];
    for (const emp of employees) {
      try {
        await prisma.employee.upsert({
          where: { id: emp.id },
          update: {},
          create: emp,
        });
        successCount++;
      } catch (e) {
        console.log(`  ⚠️ Employee ${emp.id} スキップ`);
        errorCount++;
      }
    }

    console.log('📊 MST_UserAuthデータを投入中...')
    const userAuths = [
      {
        user_id: 'USER000001',
        login_id: '000001',
        password_hash: passwordHash,
        password_salt: 'randomsalt123',
        employee_id: '000001',
        account_status: 'ACTIVE',
        failed_login_count: 0,
        session_timeout: 480,
      },
      {
        user_id: 'USER000002',
        login_id: '000002',
        password_hash: passwordHash,
        password_salt: 'randomsalt456',
        employee_id: '000002',
        account_status: 'ACTIVE',
        failed_login_count: 0,
        session_timeout: 480,
      },
      {
        user_id: 'USER000003',
        login_id: '000003',
        password_hash: passwordHash,
        password_salt: 'randomsalt789',
        employee_id: '000003',
        account_status: 'ACTIVE',
        failed_login_count: 0,
        session_timeout: 480,
      },
      {
        user_id: 'USER000004',
        login_id: '000004',
        password_hash: passwordHash,
        password_salt: 'randomsalt012',
        employee_id: '000004',
        account_status: 'ACTIVE',
        failed_login_count: 0,
        session_timeout: 480,
      },
      {
        user_id: 'USER_TEST_EMPLOYEE',
        login_id: 'test-employee',
        password_hash: passwordHash,
        password_salt: 'testsalt123',
        employee_id: 'test-employee',
        account_status: 'ACTIVE',
        failed_login_count: 0,
        session_timeout: 480,
      },
    ];
    for (const auth of userAuths) {
      try {
        await prisma.userAuth.upsert({
          where: { user_id: auth.user_id },
          update: {},
          create: auth,
        });
        successCount++;
      } catch (e) {
        console.log(`  ⚠️ UserAuth ${auth.user_id} スキップ`);
        errorCount++;
      }
    }

    // ========================================
    // 従業員のスキルレコード
    // ========================================
    
    console.log('📊 TRN_SkillRecordデータを投入中...')
    const skillRecords = [
      // 笹尾 豊樹のスキル
      {
        id: 'skill_rec_001',
        employee_id: '000001',
        skill_item_id: 'SKILL003', // JavaScript
        skill_category_id: 'CAT001',
        skill_level: 4, // エキスパート
        self_assessment: 4,
        manager_assessment: 4,
        evidence_description: 'React/Next.jsを使用した複数プロジェクトの開発経験',
        acquisition_date: new Date('2020-06-01'),
        last_used_date: new Date('2025-01-15'),
        learning_hours: 1500,
        project_experience_count: 8,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
      {
        id: 'skill_rec_002',
        employee_id: '000001',
        skill_item_id: 'SKILL004', // TypeScript
        skill_category_id: 'CAT001',
        skill_level: 3,
        self_assessment: 4,
        manager_assessment: 4,
        evidence_description: '型安全な開発を意識したプロジェクト実装経験',
        acquisition_date: new Date('2021-01-01'),
        last_used_date: new Date('2025-01-15'),
        learning_hours: 1200,
        project_experience_count: 6,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
      {
        id: 'skill_rec_003',
        employee_id: '000001',
        skill_item_id: 'SKILL011', // Next.js
        skill_category_id: 'CAT002',
        skill_level: 2,
        self_assessment: 3,
        manager_assessment: 3,
        evidence_description: 'Next.js 14のApp Routerを使用した開発',
        acquisition_date: new Date('2022-03-01'),
        last_used_date: new Date('2025-01-15'),
        learning_hours: 800,
        project_experience_count: 4,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
      {
        id: 'skill_rec_004',
        employee_id: '000001',
        skill_item_id: 'SKILL016', // PostgreSQL
        skill_category_id: 'CAT003',
        skill_level: 3,
        self_assessment: 3,
        manager_assessment: 3,
        evidence_description: 'Prisma ORMを使用したDB設計と実装',
        acquisition_date: new Date('2020-09-01'),
        last_used_date: new Date('2025-01-10'),
        learning_hours: 600,
        project_experience_count: 5,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
      {
        id: 'skill_rec_005',
        employee_id: '000001',
        skill_item_id: 'SKILL024', // Docker
        skill_category_id: 'CAT004',
        skill_level: 1,
        self_assessment: 2,
        manager_assessment: 2,
        evidence_description: '開発環境のコンテナ化経験',
        acquisition_date: new Date('2021-06-01'),
        last_used_date: new Date('2024-12-01'),
        learning_hours: 200,
        project_experience_count: 3,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
      
      // 佐藤 花子のスキル
      {
        id: 'skill_rec_006',
        employee_id: '000002',
        skill_item_id: 'SKILL001', // Java
        skill_category_id: 'CAT001',
        skill_level: 5, // マスター
        self_assessment: 5,
        manager_assessment: 5,
        evidence_description: '10年以上のJava開発経験、アーキテクト経験あり',
        acquisition_date: new Date('2012-04-01'),
        last_used_date: new Date('2025-01-10'),
        learning_hours: 5000,
        project_experience_count: 25,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
      {
        id: 'skill_rec_007',
        employee_id: '000002',
        skill_item_id: 'SKILL009', // Spring Boot
        skill_category_id: 'CAT002',
        skill_level: 5,
        self_assessment: 5,
        manager_assessment: 5,
        evidence_description: 'マイクロサービスアーキテクチャの設計と実装',
        acquisition_date: new Date('2015-01-01'),
        last_used_date: new Date('2025-01-05'),
        learning_hours: 3000,
        project_experience_count: 15,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
      {
        id: 'skill_rec_008',
        employee_id: '000002',
        skill_item_id: 'SKILL026', // スクラム
        skill_category_id: 'CAT005',
        skill_level: 4,
        self_assessment: 4,
        manager_assessment: 4,
        evidence_description: 'スクラムマスターとして複数プロジェクトを管理',
        acquisition_date: new Date('2018-01-01'),
        last_used_date: new Date('2025-01-15'),
        learning_hours: 1000,
        project_experience_count: 8,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
      
      // 山田 太郎のスキル
      {
        id: 'skill_rec_009',
        employee_id: '000003',
        skill_item_id: 'SKILL002', // Python
        skill_category_id: 'CAT001',
        skill_level: 2,
        self_assessment: 2,
        manager_assessment: 2,
        evidence_description: '機械学習プロジェクトでの使用経験',
        acquisition_date: new Date('2022-06-01'),
        last_used_date: new Date('2024-11-01'),
        learning_hours: 300,
        project_experience_count: 2,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
      {
        id: 'skill_rec_010',
        employee_id: '000003',
        skill_item_id: 'SKILL003', // JavaScript
        skill_category_id: 'CAT001',
        skill_level: 2,
        self_assessment: 2,
        manager_assessment: 2,
        evidence_description: 'フロントエンド開発の基礎習得',
        acquisition_date: new Date('2022-05-01'),
        last_used_date: new Date('2024-12-20'),
        learning_hours: 400,
        project_experience_count: 2,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
      {
        id: 'skill_rec_011',
        employee_id: '000003',
        skill_item_id: 'SKILL031', // Git
        skill_category_id: 'CAT007',
        skill_level: 2,
        self_assessment: 2,
        manager_assessment: 2,
        evidence_description: 'チーム開発でのGit使用経験',
        acquisition_date: new Date('2022-04-01'),
        last_used_date: new Date('2025-01-15'),
        learning_hours: 100,
        project_experience_count: 3,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
      
      // 田中 美咲のスキル
      {
        id: 'skill_rec_012',
        employee_id: '000004',
        skill_item_id: 'SKILL012', // Vue.js
        skill_category_id: 'CAT002',
        skill_level: 3,
        self_assessment: 3,
        manager_assessment: 3,
        evidence_description: 'SPAアプリケーションの開発経験',
        acquisition_date: new Date('2021-08-01'),
        last_used_date: new Date('2024-12-15'),
        learning_hours: 600,
        project_experience_count: 4,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
      {
        id: 'skill_rec_013',
        employee_id: '000004',
        skill_item_id: 'SKILL017', // MySQL
        skill_category_id: 'CAT003',
        skill_level: 3,
        self_assessment: 3,
        manager_assessment: 3,
        evidence_description: 'パフォーマンスチューニング経験あり',
        acquisition_date: new Date('2021-05-01'),
        last_used_date: new Date('2024-11-30'),
        learning_hours: 500,
        project_experience_count: 5,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
      {
        id: 'skill_rec_014',
        employee_id: '000004',
        skill_item_id: 'SKILL030', // ドキュメント作成
        skill_category_id: 'CAT006',
        skill_level: 3,
        self_assessment: 3,
        manager_assessment: 3,
        evidence_description: '設計書・仕様書の作成経験豊富',
        acquisition_date: new Date('2021-04-01'),
        last_used_date: new Date('2025-01-10'),
        learning_hours: 400,
        project_experience_count: 6,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
      
      // テストユーザーのスキル
      {
        id: 'skill_rec_015',
        employee_id: 'test-employee',
        skill_item_id: 'SKILL003', // JavaScript
        skill_category_id: 'CAT001',
        skill_level: 3,
        self_assessment: 3,
        manager_assessment: 3,
        evidence_description: 'テスト用スキルデータ',
        acquisition_date: new Date('2023-01-01'),
        last_used_date: new Date('2025-01-01'),
        learning_hours: 500,
        project_experience_count: 3,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
      {
        id: 'skill_rec_016',
        employee_id: 'test-employee',
        skill_item_id: 'SKILL010', // React
        skill_category_id: 'CAT002',
        skill_level: 2,
        self_assessment: 2,
        manager_assessment: 2,
        evidence_description: 'Reactコンポーネント開発経験',
        acquisition_date: new Date('2023-06-01'),
        last_used_date: new Date('2024-12-01'),
        learning_hours: 300,
        project_experience_count: 2,
        skill_status: 'ACTIVE',
        tenant_id: 'default-tenant',
        created_by: 'system',
        updated_by: 'system',
      },
    ];

    for (const skillRecord of skillRecords) {
      try {
        await prisma.skillRecord.upsert({
          where: { id: skillRecord.id },
          update: {},
          create: skillRecord,
        });
        successCount++;
      } catch (e) {
        console.log(`  ⚠️ SkillRecord ${skillRecord.id} スキップ`);
        errorCount++;
      }
    }

    // ========================================
    // レポート関連データ
    // ========================================
    
    // レポートテンプレート
    console.log('📊 レポートテンプレートデータを投入中...')
    const reportTemplates = [
      {
        id: 'template_001',
        tenant_id: 'default-tenant',
        template_key: 'skill_summary_report',
        template_name: 'スキル評価サマリーレポート',
        report_category: 'スキル管理',
        output_format: 'excel',
        language_code: 'ja',
        template_content: JSON.stringify({
          title: 'スキル評価サマリーレポート',
          sections: ['summary', 'skills', 'gaps']
        }),
        parameters_schema: JSON.stringify({
          startDate: { type: 'date', required: true },
          endDate: { type: 'date', required: true },
          departmentId: { type: 'string', required: false }
        }),
        is_default: true,
        is_active: true,
        version: '1.0'
      },
      {
        id: 'template_002',
        tenant_id: 'default-tenant',
        template_key: 'training_progress_report',
        template_name: '研修進捗レポート',
        report_category: '研修管理',
        output_format: 'pdf',
        language_code: 'ja',
        template_content: JSON.stringify({
          title: '研修進捗レポート',
          sections: ['overview', 'progress', 'completion']
        }),
        parameters_schema: JSON.stringify({
          startDate: { type: 'date', required: true },
          endDate: { type: 'date', required: true },
          trainingCategory: { type: 'string', required: false }
        }),
        is_default: false,
        is_active: true,
        version: '1.0'
      },
      {
        id: 'template_003',
        tenant_id: 'default-tenant',
        template_key: 'career_plan_report',
        template_name: 'キャリアプランレポート',
        report_category: 'キャリア管理',
        output_format: 'excel',
        language_code: 'ja',
        template_content: JSON.stringify({
          title: 'キャリアプランレポート',
          sections: ['goals', 'progress', 'action_plans']
        }),
        parameters_schema: JSON.stringify({
          employeeId: { type: 'string', required: false },
          year: { type: 'number', required: true }
        }),
        is_default: false,
        is_active: true,
        version: '1.0'
      },
      {
        id: 'template_004',
        tenant_id: 'default-tenant',
        template_key: 'work_performance_report',
        template_name: '作業実績レポート',
        report_category: '作業管理',
        output_format: 'csv',
        language_code: 'ja',
        template_content: JSON.stringify({
          title: '作業実績レポート',
          sections: ['summary', 'details', 'analysis']
        }),
        parameters_schema: JSON.stringify({
          startDate: { type: 'date', required: true },
          endDate: { type: 'date', required: true },
          projectId: { type: 'string', required: false }
        }),
        is_default: false,
        is_active: true,
        version: '1.0'
      },
      {
        id: 'template_005',
        tenant_id: 'default-tenant',
        template_key: 'comprehensive_analysis',
        template_name: '総合分析レポート',
        report_category: '分析',
        output_format: 'pdf',
        language_code: 'ja',
        template_content: JSON.stringify({
          title: '総合分析レポート',
          sections: ['overview', 'skills', 'training', 'career', 'recommendations']
        }),
        parameters_schema: JSON.stringify({
          startDate: { type: 'date', required: true },
          endDate: { type: 'date', required: true },
          includeTeamData: { type: 'boolean', required: false }
        }),
        is_default: false,
        is_active: true,
        version: '1.0'
      }
    ];

    for (const template of reportTemplates) {
      try {
        await prisma.reportTemplate.upsert({
          where: { id: template.id },
          update: {},
          create: template,
        });
        successCount++;
      } catch (e) {
        console.log(`  ⚠️ ReportTemplate ${template.id} スキップ:`, e.message);
        errorCount++;
      }
    }

    // レポート生成履歴
    console.log('📊 レポート生成履歴データを投入中...')
    const reportGenerations = [
      {
        id: 'report_gen_001',
        tenant_id: 'default-tenant',
        template_id: 'template_001',
        requested_by: 'test-employee',
        report_title: 'スキル評価サマリーレポート_2024年12月',
        report_category: 'スキル管理',
        output_format: 'excel',
        generation_status: 'COMPLETED',
        parameters: JSON.stringify({
          startDate: '2024-01-01',
          endDate: '2024-12-31'
        }),
        file_path: '/reports/skill_summary_2024_12.xlsx',
        file_size: 2048576, // 2MB
        download_count: 3,
        last_downloaded_at: new Date('2024-12-15T09:30:00Z'),
        requested_at: new Date('2024-12-10T10:00:00Z'),
        started_at: new Date('2024-12-10T10:01:00Z'),
        completed_at: new Date('2024-12-10T10:05:30Z'),
        processing_time_ms: 270000 // 4.5分
      },
      {
        id: 'report_gen_002',
        tenant_id: 'default-tenant',
        template_id: 'template_002',
        requested_by: 'test-employee',
        report_title: '研修進捗レポート_2024年Q4',
        report_category: '研修管理',
        output_format: 'pdf',
        generation_status: 'COMPLETED',
        parameters: JSON.stringify({
          startDate: '2024-10-01',
          endDate: '2024-12-31',
          trainingCategory: '技術研修'
        }),
        file_path: '/reports/training_progress_2024_q4.pdf',
        file_size: 1536000, // 1.5MB
        download_count: 1,
        last_downloaded_at: new Date('2024-12-12T14:20:00Z'),
        requested_at: new Date('2024-12-12T14:15:00Z'),
        started_at: new Date('2024-12-12T14:16:00Z'),
        completed_at: new Date('2024-12-12T14:18:45Z'),
        processing_time_ms: 165000 // 2分45秒
      },
      {
        id: 'report_gen_003',
        tenant_id: 'default-tenant',
        template_id: 'template_003',
        requested_by: 'test-employee',
        report_title: 'キャリアプランレポート_2024年',
        report_category: 'キャリア管理',
        output_format: 'excel',
        generation_status: 'PROCESSING',
        parameters: JSON.stringify({
          year: 2024
        }),
        requested_at: new Date('2024-12-17T08:00:00Z'),
        started_at: new Date('2024-12-17T08:01:00Z'),
        processing_time_ms: null
      },
      {
        id: 'report_gen_004',
        tenant_id: 'default-tenant',
        template_id: 'template_004',
        requested_by: 'test-employee',
        report_title: '作業実績レポート_2024年11月',
        report_category: '作業管理',
        output_format: 'csv',
        generation_status: 'FAILED',
        parameters: JSON.stringify({
          startDate: '2024-11-01',
          endDate: '2024-11-30'
        }),
        error_message: 'データアクセスエラー',
        error_details: 'プロジェクトデータの取得に失敗しました',
        requested_at: new Date('2024-12-05T16:30:00Z'),
        started_at: new Date('2024-12-05T16:31:00Z'),
        processing_time_ms: 30000 // 30秒でエラー
      }
    ];

    for (const generation of reportGenerations) {
      try {
        await prisma.reportGeneration.upsert({
          where: { id: generation.id },
          update: {},
          create: generation,
        });
        successCount++;
      } catch (e) {
        console.log(`  ⚠️ ReportGeneration ${generation.id} スキップ:`, e.message);
        errorCount++;
      }
    }

    // ========================================
    // 完了メッセージ
    // ========================================
    console.log('\n✅ 実動版マスタデータ投入が完了しました！\n')
    console.log('📊 投入結果:')
    console.log(`   成功: ${successCount}件`)
    console.log(`   スキップ: ${errorCount}件`)
    console.log('\n📋 投入されたマスタデータ:')
    console.log('   基本マスタ:')
    console.log('     - 部署: 最大5件')
    console.log('     - 役職: 最大6件')
    console.log('     - 職種: 最大5件')
    console.log('     - ロール: 最大5件')
    console.log('     - 権限: 最大7件')
    console.log('   スキル関連:')
    console.log('     - スキルカテゴリ: 最大7件')
    console.log('     - スキル項目: 最大33件')
    console.log('     - スキルグレード: 最大5件')
    console.log('     - スキルレコード: 最大16件')
    console.log('   研修・資格:')
    console.log('     - 研修プログラム: 最大4件')
    console.log('     - 資格: 最大6件')
    console.log('   レポート関連:')
    console.log('     - レポートテンプレート: 最大5件')
    console.log('     - レポート生成履歴: 最大4件')
    console.log('   ユーザー関連:')
    console.log('     - 従業員: 最大5件')
    console.log('     - ユーザー認証: 最大5件')
    console.log('\n🔐 ログイン情報:')
    console.log('   テストユーザー:')
    console.log('     ID: test-employee / PW: password')
    console.log('   一般ユーザー:')
    console.log('     ID: 000001 (笹尾 豊樹) / PW: password')
    console.log('     ID: 000002 (佐藤 花子) / PW: password')
    console.log('     ID: 000003 (山田 太郎) / PW: password')
    console.log('     ID: 000004 (田中 美咲) / PW: password')

  } catch (error) {
    console.error('❌ マスタデータ投入中にエラーが発生しました:', error)
    throw error
  } finally {
    await prisma.$disconnect()
  }
}

// 直接実行時
if (require.main === module) {
  runWorkingSeed()
    .then(() => {
      console.log('🎉 処理が正常に完了しました')
      process.exit(0)
    })
    .catch((e) => {
      console.error('❌ エラーが発生しました:', e)
      process.exit(1)
    })
}

// runSampleSeed関数をエクスポート（run-seed.ts用）
export async function runSampleSeed() {
  console.log('🔄 runSampleSeed経由でrunWorkingSeedを実行します...');
  return await runWorkingSeed();
}

// エクスポート
export default runWorkingSeed
