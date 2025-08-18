/**
 * Excelレポート生成サービス
 * 要求仕様ID: RPT.1-EXCEL.1
 */

import ExcelJS from 'exceljs';
import { prisma } from '@/lib/prisma';
import path from 'path';
import fs from 'fs/promises';

interface ReportData {
  employee: {
    code: string;
    name: string;
    department: string;
    position: string;
    email: string;
  };
  skills: Array<{
    category: string;
    subcategory: string;
    skillName: string;
    level: number;
    evaluation: string;
    lastUpdated: Date;
  }>;
  projects: Array<{
    projectName: string;
    period: string;
    role: string;
    description: string;
    technologies: string[];
    achievements: string;
  }>;
  trainings: Array<{
    trainingName: string;
    provider: string;
    date: Date;
    duration: number;
    status: string;
    score?: number;
  }>;
  goals: Array<{
    goalName: string;
    targetDate: Date;
    progress: number;
    status: string;
  }>;
}

export class ExcelReportGenerator {
  private workbook: ExcelJS.Workbook;

  constructor() {
    this.workbook = new ExcelJS.Workbook();
    this.setupWorkbook();
  }

  /**
   * ワークブックの初期設定
   */
  private setupWorkbook() {
    this.workbook.creator = 'Skill Report System';
    this.workbook.lastModifiedBy = 'System';
    this.workbook.created = new Date();
    this.workbook.modified = new Date();
  }

  /**
   * 年間スキル報告書を生成
   */
  async generateAnnualReport(
    employeeId: string,
    year: number,
    tenantId: string
  ): Promise<Buffer> {
    try {
      // データを取得
      const reportData = await this.fetchReportData(employeeId, year, tenantId);

      // シート1: 基本情報
      this.createBasicInfoSheet(reportData);

      // シート2: スキル情報
      this.createSkillsSheet(reportData);

      // シート3: プロジェクト実績
      this.createProjectsSheet(reportData);

      // シート4: 研修・資格
      this.createTrainingsSheet(reportData);

      // Bufferとして出力
      const buffer = await this.workbook.xlsx.writeBuffer();
      return Buffer.from(buffer);
    } catch (error) {
      console.error('Excelレポート生成エラー:', error);
      throw error;
    }
  }

  /**
   * レポートデータを取得
   */
  private async fetchReportData(
    employeeId: string,
    year: number,
    tenantId: string
  ): Promise<ReportData> {
    // 従業員情報
    const employee = await prisma.employee.findFirst({
      where: {
        employee_code: employeeId,
        is_deleted: false,
      }
    });

    if (!employee) {
      throw new Error('従業員が見つかりません');
    }

    // スキル情報
    const skills = await prisma.skillRecord.findMany({
      where: {
        employee_id: employeeId,
        is_deleted: false,
      }
    });

    // プロジェクト実績
    const projects = await prisma.projectRecord.findMany({
      where: {
        employee_id: employeeId,
        start_date: {
          gte: new Date(year, 0, 1),
          lt: new Date(year + 1, 0, 1),
        },
        is_deleted: false,
      },
      orderBy: {
        start_date: 'desc',
      },
    });

    // 研修履歴
    const trainings = await prisma.trainingHistory.findMany({
      where: {
        employee_id: employeeId,
        start_date: {
          gte: new Date(year, 0, 1),
          lt: new Date(year + 1, 0, 1),
        },
        is_deleted: false,
      },
      orderBy: {
        start_date: 'desc',
      },
    });

    // キャリア目標
    const goals = await prisma.goalProgress.findMany({
      where: {
        employee_id: employeeId,
        is_deleted: false,
      },
    });

    // 部門情報を取得
    const department = employee?.department_id ? await prisma.department.findUnique({
      where: { department_code: employee.department_id }
    }) : null;

    // 位置情報を取得
    const position = employee?.position_id ? await prisma.position.findUnique({
      where: { position_code: employee.position_id }
    }) : null;

    // データを整形
    return {
      employee: {
        code: employee.employee_code,
        name: employee.full_name || '',
        department: department?.department_name || '',
        position: position?.position_name || '',
        email: employee.email || '',
      },
      skills: skills.map(s => ({
        category: (s as any).skill_category || '',
        subcategory: (s as any).skill_subcategory || '',
        skillName: (s as any).skill_name || '',
        level: s.skill_level || 0,
        evaluation: this.getEvaluationText(s.skill_level || 0),
        lastUpdated: s.updated_at,
      })),
      projects: projects.map(p => ({
        projectName: p.project_name || '',
        period: `${p.start_date?.toLocaleDateString('ja-JP')} ～ ${p.end_date?.toLocaleDateString('ja-JP') || '継続中'}`,
        role: (p as any).role || '',
        description: (p as any).description || '',
        technologies: (p as any).technologies ? (p as any).technologies.split(',') : [],
        achievements: p.achievements || '',
      })),
      trainings: trainings.map(t => ({
        trainingName: t.training_name || '',
        provider: t.provider_name || '',
        date: t.start_date || new Date(),
        duration: Number(t.duration_hours) || 0,
        status: t.attendance_status || '',
        score: t.test_score !== null ? Number(t.test_score) : undefined as any,
      })),
      goals: goals.map(g => ({
        goalName: g.goal_id || '',
        targetDate: g.target_date || new Date(),
        progress: Number((g as any).progress_percentage) || 0,
        status: g.achievement_status || '',
      })),
    };
  }

  /**
   * 基本情報シートを作成
   */
  private createBasicInfoSheet(data: ReportData) {
    const sheet = this.workbook.addWorksheet('基本情報');

    // ヘッダー設定
    sheet.columns = [
      { header: '項目', key: 'item', width: 20 },
      { header: '内容', key: 'value', width: 40 },
    ];

    // データ追加
    sheet.addRows([
      { item: '社員番号', value: data.employee.code },
      { item: '氏名', value: data.employee.name },
      { item: '所属', value: data.employee.department },
      { item: '役職', value: data.employee.position },
      { item: 'メールアドレス', value: data.employee.email },
      { item: '報告書作成日', value: new Date().toLocaleDateString('ja-JP') },
    ]);

    // スタイル設定
    this.applyBasicStyles(sheet);
  }

  /**
   * スキル情報シートを作成
   */
  private createSkillsSheet(data: ReportData) {
    const sheet = this.workbook.addWorksheet('スキル情報');

    sheet.columns = [
      { header: 'カテゴリ', key: 'category', width: 20 },
      { header: 'サブカテゴリ', key: 'subcategory', width: 20 },
      { header: 'スキル名', key: 'skillName', width: 30 },
      { header: 'レベル', key: 'level', width: 10 },
      { header: '評価', key: 'evaluation', width: 10 },
      { header: '最終更新日', key: 'lastUpdated', width: 15 },
    ];

    // データ追加
    data.skills.forEach(skill => {
      sheet.addRow({
        category: skill.category,
        subcategory: skill.subcategory,
        skillName: skill.skillName,
        level: skill.level,
        evaluation: skill.evaluation,
        lastUpdated: skill.lastUpdated.toLocaleDateString('ja-JP'),
      });
    });

    this.applyBasicStyles(sheet);
  }

  /**
   * プロジェクト実績シートを作成
   */
  private createProjectsSheet(data: ReportData) {
    const sheet = this.workbook.addWorksheet('プロジェクト実績');

    sheet.columns = [
      { header: 'プロジェクト名', key: 'projectName', width: 30 },
      { header: '期間', key: 'period', width: 25 },
      { header: '役割', key: 'role', width: 20 },
      { header: '概要', key: 'description', width: 40 },
      { header: '使用技術', key: 'technologies', width: 30 },
      { header: '成果', key: 'achievements', width: 40 },
    ];

    data.projects.forEach(project => {
      sheet.addRow({
        projectName: project.projectName,
        period: project.period,
        role: project.role,
        description: project.description,
        technologies: project.technologies.join(', '),
        achievements: project.achievements,
      });
    });

    this.applyBasicStyles(sheet);
  }

  /**
   * 研修・資格シートを作成
   */
  private createTrainingsSheet(data: ReportData) {
    const sheet = this.workbook.addWorksheet('研修・資格');

    sheet.columns = [
      { header: '研修名', key: 'trainingName', width: 30 },
      { header: '提供元', key: 'provider', width: 25 },
      { header: '受講日', key: 'date', width: 15 },
      { header: '時間', key: 'duration', width: 10 },
      { header: 'ステータス', key: 'status', width: 15 },
      { header: 'スコア', key: 'score', width: 10 },
    ];

    data.trainings.forEach(training => {
      sheet.addRow({
        trainingName: training.trainingName,
        provider: training.provider,
        date: training.date.toLocaleDateString('ja-JP'),
        duration: `${training.duration}時間`,
        status: training.status,
        score: training.score || '-',
      });
    });

    this.applyBasicStyles(sheet);
  }

  /**
   * 基本的なスタイルを適用
   */
  private applyBasicStyles(sheet: ExcelJS.Worksheet) {
    // ヘッダー行のスタイル
    const headerRow = sheet.getRow(1);
    headerRow.font = { bold: true, color: { argb: 'FFFFFFFF' } };
    headerRow.fill = {
      type: 'pattern',
      pattern: 'solid',
      fgColor: { argb: 'FF0066CC' },
    };
    headerRow.alignment = { vertical: 'middle', horizontal: 'center' };
    headerRow.height = 25;

    // ボーダー設定
    sheet.eachRow((row, rowNumber) => {
      row.eachCell((cell) => {
        cell.border = {
          top: { style: 'thin' },
          left: { style: 'thin' },
          bottom: { style: 'thin' },
          right: { style: 'thin' },
        };
      });
    });
  }

  /**
   * 評価テキストを取得
   */
  private getEvaluationText(level: number): string {
    if (level >= 4) return '◎';
    if (level >= 3) return '○';
    if (level >= 2) return '△';
    return '×';
  }
}

/**
 * レポート生成APIエンドポイント用関数
 */
export async function generateAnnualSkillReport(
  employeeId: string,
  year: number,
  tenantId: string
): Promise<Buffer> {
  const generator = new ExcelReportGenerator();
  return await generator.generateAnnualReport(employeeId, year, tenantId);
}

/**
 * 部門スキルマップを生成
 */
export async function generateDepartmentSkillMap(
  departmentId: string,
  tenantId: string
): Promise<Buffer> {
  const workbook = new ExcelJS.Workbook();
  const sheet = workbook.addWorksheet('部門スキルマップ');

  // 部門の全従業員を取得
  const employees = await prisma.employee.findMany({
    where: {
      department_id: departmentId,
      employee_status: 'ACTIVE',
      is_deleted: false,
    },
  });

  // スキル項目を取得
  const skillItems = await prisma.skillItem.findMany({
    where: {
      is_deleted: false,
    },
    orderBy: {
      skill_code: 'asc',
    },
  });

  // ヘッダー設定
  const headers = ['社員名'];
  skillItems.forEach(skill => {
    headers.push(skill.skill_name || '');
  });
  sheet.addRow(headers);

  // 各従業員のスキルレベルを取得
  for (const employee of employees) {
    const row = [employee.full_name || ''];
    
    for (const skill of skillItems) {
      const skillRecord = await prisma.skillRecord.findFirst({
        where: {
          employee_id: employee.employee_code,
          skill_item_id: skill.skill_code,
          tenant_id: tenantId,
          is_deleted: false,
        },
      });
      
      row.push(skillRecord ? String(skillRecord.skill_level || 0) : '0');
    }
    
    sheet.addRow(row);
  }

  // スタイル適用
  const headerRow = sheet.getRow(1);
  headerRow.font = { bold: true };
  headerRow.fill = {
    type: 'pattern',
    pattern: 'solid',
    fgColor: { argb: 'FFE0E0E0' },
  };

  // ヒートマップ風の条件付き書式
  for (let col = 2; col <= headers.length; col++) {
    for (let row = 2; row <= employees.length + 1; row++) {
      const cell = sheet.getCell(row, col);
      const value = parseInt(cell.value as string) || 0;
      
      // レベルに応じて色を設定
      if (value >= 4) {
        cell.fill = {
          type: 'pattern',
          pattern: 'solid',
          fgColor: { argb: 'FF00FF00' }, // 緑
        };
      } else if (value >= 3) {
        cell.fill = {
          type: 'pattern',
          pattern: 'solid',
          fgColor: { argb: 'FFFFFF00' }, // 黄
        };
      } else if (value >= 2) {
        cell.fill = {
          type: 'pattern',
          pattern: 'solid',
          fgColor: { argb: 'FFFFA500' }, // オレンジ
        };
      } else {
        cell.fill = {
          type: 'pattern',
          pattern: 'solid',
          fgColor: { argb: 'FFFF0000' }, // 赤
        };
      }
    }
  }

  const buffer = await workbook.xlsx.writeBuffer();
  return Buffer.from(buffer);
}