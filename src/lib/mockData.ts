// PRO.1-BASE.1, SKL.1-HIER.1: モックデータ定義
// 実際のAPIが実装されるまでの仮データ

export interface ProfileData {
  emp_no: string;
  name_kanji: string;
  name_kana: string;
  name_english: string;
  email: string;
  birth_date: string;
  join_date: string;
  dept_name: string;
  position_name: string;
  manager_name: string;
  phone: string;
  emergency_contact: string;
  address: string;
  updated_at: string;
  updated_by: string;
}

export interface SkillCategory {
  id: string;
  name: string;
  skills: SkillItem[];
}

export interface SkillItem {
  id: string;
  name: string;
  category: string;
  subcategory?: string;
  level: number; // 0: 未評価, 1: ×, 2: △, 3: ○, 4: ◎
  acquired_date?: string;
  remarks?: string;
  children?: SkillItem[];
}

export interface CertificationData {
  id: string;
  cert_name: string;
  acquired_date: string;
  expire_date?: string;
  score?: string;
  issuer: string;
  cert_number?: string;
}

export interface UpdateHistory {
  id: string;
  updated_at: string;
  updated_by: string;
  section: string;
  changes: string;
}

// プロフィールモックデータ
export const mockProfileData: ProfileData = {
  emp_no: "EMP001",
  name_kanji: "山田太郎",
  name_kana: "ヤマダタロウ",
  name_english: "Taro Yamada",
  email: "yamada.taro@example.com",
  birth_date: "1990-04-15",
  join_date: "2020-04-01",
  dept_name: "開発部",
  position_name: "主任",
  manager_name: "佐藤花子",
  phone: "090-1234-5678",
  emergency_contact: "090-8765-4321",
  address: "東京都渋谷区1-1-1",
  updated_at: "2025-05-20T10:30:00Z",
  updated_by: "山田太郎"
};

// 更新履歴モックデータ
export const mockUpdateHistory: UpdateHistory[] = [
  {
    id: "1",
    updated_at: "2025-05-20T10:30:00Z",
    updated_by: "山田太郎",
    section: "基本情報",
    changes: "電話番号を更新"
  },
  {
    id: "2",
    updated_at: "2025-04-15T14:20:00Z",
    updated_by: "佐藤花子",
    section: "所属情報",
    changes: "役職を主任に変更"
  },
  {
    id: "3",
    updated_at: "2025-03-10T09:15:00Z",
    updated_by: "山田太郎",
    section: "連絡先",
    changes: "住所を更新"
  }
];

// スキルカテゴリモックデータ
export const mockSkillCategories: SkillCategory[] = [
  {
    id: "tech",
    name: "技術スキル",
    skills: [
      {
        id: "programming",
        name: "プログラミング言語",
        category: "技術スキル",
        level: 0,
        children: [
          {
            id: "java",
            name: "Java",
            category: "技術スキル",
            subcategory: "プログラミング言語",
            level: 3,
            acquired_date: "2020-06-01",
            remarks: "Spring Frameworkを使用した開発経験あり",
            children: [
              {
                id: "java-se",
                name: "Java SE",
                category: "技術スキル",
                subcategory: "Java",
                level: 4,
                acquired_date: "2020-06-01"
              },
              {
                id: "java-ee",
                name: "Java EE",
                category: "技術スキル",
                subcategory: "Java",
                level: 3,
                acquired_date: "2021-03-15"
              },
              {
                id: "spring",
                name: "Spring Framework",
                category: "技術スキル",
                subcategory: "Java",
                level: 3,
                acquired_date: "2021-06-01"
              }
            ]
          },
          {
            id: "javascript",
            name: "JavaScript",
            category: "技術スキル",
            subcategory: "プログラミング言語",
            level: 3,
            acquired_date: "2021-01-15",
            children: [
              {
                id: "es6",
                name: "ES6+",
                category: "技術スキル",
                subcategory: "JavaScript",
                level: 3,
                acquired_date: "2021-01-15"
              },
              {
                id: "typescript",
                name: "TypeScript",
                category: "技術スキル",
                subcategory: "JavaScript",
                level: 2,
                acquired_date: "2022-04-01"
              },
              {
                id: "react",
                name: "React",
                category: "技術スキル",
                subcategory: "JavaScript",
                level: 3,
                acquired_date: "2022-01-10"
              }
            ]
          },
          {
            id: "python",
            name: "Python",
            category: "技術スキル",
            subcategory: "プログラミング言語",
            level: 2,
            acquired_date: "2023-02-01",
            children: [
              {
                id: "django",
                name: "Django",
                category: "技術スキル",
                subcategory: "Python",
                level: 2,
                acquired_date: "2023-03-15"
              },
              {
                id: "flask",
                name: "Flask",
                category: "技術スキル",
                subcategory: "Python",
                level: 1,
                acquired_date: "2023-06-01"
              }
            ]
          }
        ]
      },
      {
        id: "database",
        name: "データベース",
        category: "技術スキル",
        level: 0,
        children: [
          {
            id: "mysql",
            name: "MySQL",
            category: "技術スキル",
            subcategory: "データベース",
            level: 3,
            acquired_date: "2020-08-01"
          },
          {
            id: "postgresql",
            name: "PostgreSQL",
            category: "技術スキル",
            subcategory: "データベース",
            level: 2,
            acquired_date: "2022-05-01"
          },
          {
            id: "oracle",
            name: "Oracle Database",
            category: "技術スキル",
            subcategory: "データベース",
            level: 2,
            acquired_date: "2021-09-01"
          }
        ]
      }
    ]
  },
  {
    id: "development",
    name: "開発スキル",
    skills: [
      {
        id: "methodology",
        name: "開発手法",
        category: "開発スキル",
        level: 0,
        children: [
          {
            id: "agile",
            name: "アジャイル開発",
            category: "開発スキル",
            subcategory: "開発手法",
            level: 3,
            acquired_date: "2021-04-01"
          },
          {
            id: "waterfall",
            name: "ウォーターフォール開発",
            category: "開発スキル",
            subcategory: "開発手法",
            level: 4,
            acquired_date: "2020-04-01"
          }
        ]
      },
      {
        id: "tools",
        name: "開発ツール",
        category: "開発スキル",
        level: 0,
        children: [
          {
            id: "git",
            name: "Git",
            category: "開発スキル",
            subcategory: "開発ツール",
            level: 4,
            acquired_date: "2020-04-01"
          },
          {
            id: "docker",
            name: "Docker",
            category: "開発スキル",
            subcategory: "開発ツール",
            level: 3,
            acquired_date: "2021-08-01"
          },
          {
            id: "jenkins",
            name: "Jenkins",
            category: "開発スキル",
            subcategory: "開発ツール",
            level: 2,
            acquired_date: "2022-03-01"
          }
        ]
      }
    ]
  },
  {
    id: "business",
    name: "業務スキル",
    skills: [
      {
        id: "domain",
        name: "業務知識",
        category: "業務スキル",
        level: 0,
        children: [
          {
            id: "finance",
            name: "金融業務",
            category: "業務スキル",
            subcategory: "業務知識",
            level: 2,
            acquired_date: "2021-01-01"
          },
          {
            id: "ecommerce",
            name: "EC業務",
            category: "業務スキル",
            subcategory: "業務知識",
            level: 3,
            acquired_date: "2020-06-01"
          }
        ]
      }
    ]
  },
  {
    id: "management",
    name: "管理スキル",
    skills: [
      {
        id: "project",
        name: "プロジェクト管理",
        category: "管理スキル",
        level: 0,
        children: [
          {
            id: "planning",
            name: "計画立案",
            category: "管理スキル",
            subcategory: "プロジェクト管理",
            level: 3,
            acquired_date: "2022-01-01"
          },
          {
            id: "risk-management",
            name: "リスク管理",
            category: "管理スキル",
            subcategory: "プロジェクト管理",
            level: 2,
            acquired_date: "2022-06-01"
          }
        ]
      }
    ]
  },
  {
    id: "productivity",
    name: "生産スキル",
    skills: [
      {
        id: "communication",
        name: "コミュニケーション",
        category: "生産スキル",
        level: 0,
        children: [
          {
            id: "presentation",
            name: "プレゼンテーション",
            category: "生産スキル",
            subcategory: "コミュニケーション",
            level: 3,
            acquired_date: "2021-03-01"
          },
          {
            id: "documentation",
            name: "ドキュメント作成",
            category: "生産スキル",
            subcategory: "コミュニケーション",
            level: 4,
            acquired_date: "2020-04-01"
          }
        ]
      }
    ]
  }
];

// 資格情報モックデータ
export const mockCertifications: CertificationData[] = [
  {
    id: "1",
    cert_name: "Oracle Certified Java Programmer, Gold SE 11",
    acquired_date: "2024-03-15",
    expire_date: "2027-03-14",
    score: "750点",
    issuer: "Oracle Corporation",
    cert_number: "OCP-JAVA-2024-001"
  },
  {
    id: "2",
    cert_name: "AWS Certified Solutions Architect - Associate",
    acquired_date: "2023-11-20",
    expire_date: "2026-11-19",
    issuer: "Amazon Web Services",
    cert_number: "AWS-SAA-2023-002"
  },
  {
    id: "3",
    cert_name: "基本情報技術者試験",
    acquired_date: "2020-12-20",
    issuer: "情報処理推進機構（IPA）",
    cert_number: "FE-2020-123456"
  },
  {
    id: "4",
    cert_name: "応用情報技術者試験",
    acquired_date: "2022-06-15",
    issuer: "情報処理推進機構（IPA）",
    cert_number: "AP-2022-789012"
  }
];

// スキルレベルの表示用ラベル
export const skillLevelLabels = {
  0: "未評価",
  1: "×",
  2: "△", 
  3: "○",
  4: "◎"
};

// スキルレベルの説明
export const skillLevelDescriptions = {
  0: "評価なし",
  1: "知識なし・経験なし",
  2: "基礎知識あり・簡単な作業可能",
  3: "実務経験あり・一人で作業可能",
  4: "専門知識あり・他者への指導可能"
};
