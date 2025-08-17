/**
 * 要求仕様ID: TRN.1-ATT.1
 * 対応設計書: docs/design/database/seed-data/training-seed.md
 * 実装内容: 研修・資格情報のシードデータ
 */
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('研修・資格情報のシードデータを作成中...');

  // 既存のEmployeeを確認
  const existingEmployee = await prisma.employee.findFirst();
  
  if (!existingEmployee) {
    console.log('Employeeデータが存在しないため、サンプルEmployeeを作成します');
    
    // サンプルEmployeeの作成
    await prisma.employee.create({
      data: {
        id: 'emp_001',
        employee_code: 'E001',
        full_name: '山田太郎',
        full_name_kana: 'ヤマダタロウ',
        email: 'yamada.taro@example.com',
        phone: '090-1234-5678',
        hire_date: new Date('2020-04-01'),
        birth_date: new Date('1990-01-15'),
        gender: '男性',
        department_id: 'dept-001',
        position_id: 'pos-001',
        job_type_id: 'job-001',
        employment_status: '正社員',
        employee_status: 'ACTIVE',
        is_deleted: false
      }
    });
    
    console.log('サンプルEmployeeを作成しました');
  }

  // 既存のTrainingHistoryを確認
  const existingTrainings = await prisma.trainingHistory.findMany();
  
  if (existingTrainings.length === 0) {
    console.log('TrainingHistoryデータが存在しないため、サンプルデータを作成します');
    
    // サンプル研修履歴の作成
    const trainingHistories = [
      {
        id: 'trn-001',
        training_history_id: 'TRN-001',
        employee_id: 'emp_001',
        training_name: 'React.js基礎研修',
        training_type: '社内研修',
        training_category: 'フロントエンド',
        provider_name: '自社',
        start_date: new Date('2025-04-01'),
        end_date: new Date('2025-04-05'),
        duration_hours: 40,
        attendance_status: 'completed',
        completion_rate: 100,
        certificate_obtained: true,
        skills_acquired: JSON.stringify(['React', 'JavaScript', 'TypeScript']),
        learning_objectives: 'React.jsの基礎から応用まで学習',
        tenant_id: 'default',
        created_by: 'system',
        updated_by: 'system',
        is_deleted: false
      },
      {
        id: 'trn-002',
        training_history_id: 'TRN-002',
        employee_id: 'emp_001',
        training_name: 'AWS認定ソリューションアーキテクト研修',
        training_type: '外部研修',
        training_category: 'クラウド',
        provider_name: 'AWS',
        start_date: new Date('2025-05-01'),
        end_date: new Date('2025-05-31'),
        duration_hours: 80,
        attendance_status: 'in_progress',
        completion_rate: 60,
        certificate_obtained: false,
        skills_acquired: JSON.stringify(['AWS', 'クラウドアーキテクチャ', 'インフラ設計']),
        learning_objectives: 'AWS認定資格取得のための研修',
        tenant_id: 'default',
        created_by: 'system',
        updated_by: 'system',
        is_deleted: false
      },
      {
        id: 'trn-003',
        training_history_id: 'TRN-003',
        employee_id: 'emp_001',
        training_name: 'プロジェクトマネジメント基礎',
        training_type: '社内研修',
        training_category: 'マネジメント',
        provider_name: '自社',
        start_date: new Date('2025-06-15'),
        end_date: new Date('2025-06-20'),
        duration_hours: 30,
        attendance_status: 'planned',
        completion_rate: 0,
        certificate_obtained: false,
        skills_acquired: JSON.stringify([]),
        learning_objectives: 'プロジェクトマネジメントの基礎を学ぶ',
        tenant_id: 'default',
        created_by: 'system',
        updated_by: 'system',
        is_deleted: false
      }
    ];
    
    for (const training of trainingHistories) {
      await prisma.trainingHistory.create({
        data: training
      });
    }
    
    console.log(`${trainingHistories.length}件の研修履歴データを作成しました`);
  }

  // 既存のCertificationを確認
  const existingCertifications = await prisma.certification.findMany();
  
  if (existingCertifications.length === 0) {
    console.log('Certificationデータが存在しないため、サンプルデータを作成します');
    
    // サンプル資格マスタの作成
    const certifications = [
      {
        certification_code: 'CERT-001',
        certification_name: '基本情報技術者試験',
        certification_name_en: 'Fundamental Information Technology Engineer Examination',
        issuer: 'IPA',
        issuer_country: '日本',
        certification_category: 'IT基礎',
        certification_level: '初級',
        validity_period_months: null,
        renewal_required: false,
        is_active: true,
        is_deleted: false
      },
      {
        certification_code: 'CERT-002',
        certification_name: 'AWS認定ソリューションアーキテクト',
        certification_name_en: 'AWS Certified Solutions Architect',
        issuer: 'Amazon Web Services',
        issuer_country: 'アメリカ',
        certification_category: 'クラウド',
        certification_level: '中級',
        validity_period_months: 36,
        renewal_required: true,
        is_active: true,
        is_deleted: false
      }
    ];
    
    for (const cert of certifications) {
      await prisma.certification.create({
        data: cert
      });
    }
    
    console.log(`${certifications.length}件の資格マスタデータを作成しました`);
  }

  // 既存のPDUを確認
  const existingPDUs = await prisma.pDU.findMany();
  
  if (existingPDUs.length === 0) {
    console.log('PDUデータが存在しないため、サンプルデータを作成します');
    
    // サンプル資格情報の作成
    const pduRecords = [
      {
        id: 'pdu-001',
        pdu_id: 'PDU-001',
        employee_id: 'emp_001',
        certification_id: 'CERT-001',
        activity_type: 'CERTIFICATION',
        activity_name: '基本情報技術者試験',
        activity_date: new Date('2024-10-15'),
        pdu_points: 40,
        pdu_category: 'EDUCATION',
        certificate_number: '12345-ABCDE',
        approval_status: 'active',
        tenant_id: 'default',
        created_by: 'system',
        updated_by: 'system',
        is_deleted: false
      },
      {
        id: 'pdu-002',
        pdu_id: 'PDU-002',
        employee_id: 'emp_001',
        certification_id: 'CERT-002',
        activity_type: 'CERTIFICATION',
        activity_name: 'AWS認定ソリューションアーキテクト',
        activity_date: new Date('2025-03-20'),
        pdu_points: 60,
        pdu_category: 'EDUCATION',
        certificate_number: 'AWS-12345',
        approval_status: 'active',
        tenant_id: 'default',
        created_by: 'system',
        updated_by: 'system',
        is_deleted: false
      }
    ];
    
    for (const pdu of pduRecords) {
      await prisma.pDU.create({
        data: pdu
      });
    }
    
    console.log(`${pduRecords.length}件の資格情報データを作成しました`);
  }

  console.log('研修・資格情報のシードデータ作成が完了しました');
}

main()
  .catch((e) => {
    console.error('シードデータ作成中にエラーが発生しました:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
