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

// CAR.1-PLAN.1: キャリア目標関連のデータ型
export interface CareerGoal {
  id: string;
  emp_no: string;
  goal_type: 'short' | 'medium' | 'long'; // 短期・中期・長期
  title: string;
  description: string;
  target_date: string;
  status: 'planning' | 'in_progress' | 'completed' | 'postponed';
  progress: number; // 0-100%
  skills_required: string[];
  created_at: string;
  updated_at: string;
}

export interface CareerPlan {
  id: string;
  emp_no: string;
  vision: string;
  current_position: string;
  target_position: string;
  target_year: number;
  goals: CareerGoal[];
  updated_at: string;
}

// WPM.1-DET.1: 作業実績関連のデータ型
export interface WorkProject {
  id: string;
  project_name: string;
  client_name?: string;
  start_date: string;
  end_date?: string;
  status: 'planning' | 'active' | 'completed' | 'suspended';
  role: string;
  team_size: number;
  technologies: string[];
  description: string;
}

export interface WorkRecord {
  id: string;
  emp_no: string;
  project: WorkProject;
  period_start: string;
  period_end?: string;
  responsibilities: string[];
  achievements: string[];
  skills_used: string[];
  skills_acquired: string[];
  challenges: string;
  lessons_learned: string;
  created_at: string;
  updated_at: string;
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

// キャリアプランモックデータ
export const mockCareerPlan: CareerPlan = {
  id: "career_001",
  emp_no: "EMP001",
  vision: "フルスタックエンジニアとして、技術とビジネスの両面で価値を提供できる人材になる",
  current_position: "主任",
  target_position: "シニアエンジニア・テックリード",
  target_year: 2027,
  goals: [],
  updated_at: "2025-05-20T10:30:00Z"
};

// キャリア目標モックデータ
export const mockCareerGoals: CareerGoal[] = [
  {
    id: "goal_001",
    emp_no: "EMP001",
    goal_type: "short",
    title: "React/Next.jsの習得",
    description: "モダンなフロントエンド開発技術を習得し、フルスタック開発能力を向上させる",
    target_date: "2025-12-31",
    status: "in_progress",
    progress: 65,
    skills_required: ["React", "Next.js", "TypeScript", "Tailwind CSS"],
    created_at: "2025-01-15T09:00:00Z",
    updated_at: "2025-05-20T14:30:00Z"
  },
  {
    id: "goal_002",
    emp_no: "EMP001",
    goal_type: "medium",
    title: "プロジェクトリーダー経験",
    description: "5名以上のチームでプロジェクトリーダーとして案件を成功に導く",
    target_date: "2026-06-30",
    status: "planning",
    progress: 15,
    skills_required: ["プロジェクト管理", "チームマネジメント", "コミュニケーション"],
    created_at: "2025-02-01T10:00:00Z",
    updated_at: "2025-05-15T16:45:00Z"
  },
  {
    id: "goal_003",
    emp_no: "EMP001",
    goal_type: "long",
    title: "技術アーキテクト認定取得",
    description: "システムアーキテクチャ設計能力を証明する資格を取得し、技術的リーダーシップを発揮する",
    target_date: "2027-12-31",
    status: "planning",
    progress: 5,
    skills_required: ["システム設計", "アーキテクチャパターン", "技術選定"],
    created_at: "2025-03-01T11:00:00Z",
    updated_at: "2025-04-20T13:20:00Z"
  }
];

// 作業実績モックデータ
export const mockWorkRecords: WorkRecord[] = [
  {
    id: "work_001",
    emp_no: "EMP001",
    project: {
      id: "proj_001",
      project_name: "ECサイトリニューアルプロジェクト",
      client_name: "株式会社サンプル商事",
      start_date: "2024-04-01",
      end_date: "2025-03-31",
      status: "active",
      role: "フロントエンドエンジニア",
      team_size: 8,
      technologies: ["React", "TypeScript", "Next.js", "Tailwind CSS", "PostgreSQL"],
      description: "既存ECサイトのモダン化とユーザビリティ向上を目的としたリニューアルプロジェクト"
    },
    period_start: "2024-04-01",
    period_end: "2025-03-31",
    responsibilities: [
      "商品一覧・詳細画面のフロントエンド開発",
      "ショッピングカート機能の実装",
      "レスポンシブデザインの対応",
      "パフォーマンス最適化"
    ],
    achievements: [
      "ページ読み込み速度を40%改善",
      "モバイル対応によりコンバージョン率15%向上",
      "コンポーネントの再利用性を高め開発効率20%向上"
    ],
    skills_used: ["React", "TypeScript", "Next.js", "Tailwind CSS", "Git"],
    skills_acquired: ["Next.js App Router", "Tailwind CSS", "パフォーマンス最適化"],
    challenges: "大規模なレガシーコードからの移行で、既存機能との互換性を保ちながらモダン化を進める必要があった",
    lessons_learned: "段階的な移行戦略の重要性と、チーム内でのコードレビュー文化の価値を実感した",
    created_at: "2024-04-01T09:00:00Z",
    updated_at: "2025-05-20T15:30:00Z"
  },
  {
    id: "work_002",
    emp_no: "EMP001",
    project: {
      id: "proj_002",
      project_name: "社内業務システム開発",
      start_date: "2023-10-01",
      end_date: "2024-03-31",
      status: "completed",
      role: "フルスタックエンジニア",
      team_size: 5,
      technologies: ["Java", "Spring Boot", "React", "MySQL", "Docker"],
      description: "人事・経理業務の効率化を目的とした社内システムの新規開発"
    },
    period_start: "2023-10-01",
    period_end: "2024-03-31",
    responsibilities: [
      "要件定義・基本設計への参画",
      "バックエンドAPI開発（Spring Boot）",
      "フロントエンド開発（React）",
      "データベース設計・実装"
    ],
    achievements: [
      "予定より1ヶ月早期にリリース完了",
      "業務処理時間を60%短縮",
      "ユーザー満足度調査で4.5/5.0の高評価"
    ],
    skills_used: ["Java", "Spring Boot", "React", "MySQL", "Docker", "Git"],
    skills_acquired: ["Spring Security", "JPA", "Docker Compose"],
    challenges: "複雑な業務ルールをシステムに落とし込む際の要件整理と、ユーザーとの認識合わせが困難だった",
    lessons_learned: "ユーザーとの密なコミュニケーションと、プロトタイプを使った早期検証の重要性を学んだ",
    created_at: "2023-10-01T09:00:00Z",
    updated_at: "2024-04-15T10:20:00Z"
  },
  {
    id: "work_003",
    emp_no: "EMP001",
    project: {
      id: "proj_003",
      project_name: "APIマイクロサービス化プロジェクト",
      start_date: "2023-01-01",
      end_date: "2023-09-30",
      status: "completed",
      role: "バックエンドエンジニア",
      team_size: 6,
      technologies: ["Java", "Spring Boot", "Docker", "Kubernetes", "PostgreSQL"],
      description: "モノリシックなシステムをマイクロサービスアーキテクチャに移行"
    },
    period_start: "2023-01-01",
    period_end: "2023-09-30",
    responsibilities: [
      "既存システムの分析・分割設計",
      "マイクロサービスのAPI設計・開発",
      "Docker化・Kubernetes環境構築",
      "データ移行・整合性確保"
    ],
    achievements: [
      "システムの可用性を99.9%に向上",
      "デプロイ頻度を週1回から日次に改善",
      "新機能開発速度を50%向上"
    ],
    skills_used: ["Java", "Spring Boot", "Docker", "Kubernetes", "PostgreSQL"],
    skills_acquired: ["マイクロサービス設計", "Kubernetes", "CI/CD"],
    challenges: "サービス間の依存関係の整理と、データ整合性を保ちながらの段階的移行が複雑だった",
    lessons_learned: "アーキテクチャ設計の重要性と、段階的な移行戦略の必要性を深く理解した",
    created_at: "2023-01-01T09:00:00Z",
    updated_at: "2023-10-15T14:45:00Z"
  }
];

// 目標タイプのラベル
export const goalTypeLabels = {
  short: "短期目標（1年以内）",
  medium: "中期目標（1-3年）",
  long: "長期目標（3年以上）"
};

// 目標ステータスのラベル
export const goalStatusLabels = {
  planning: "計画中",
  in_progress: "進行中",
  completed: "完了",
  postponed: "延期"
};

// プロジェクトステータスのラベル
export const projectStatusLabels = {
  planning: "計画中",
  active: "進行中",
  completed: "完了",
  suspended: "中断"
};
