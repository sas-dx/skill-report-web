/**
 * 要求仕様ID: PLT.1-WEB.1
 * 設計書: 設定管理システムコアライブラリ
 * 実装内容: 型安全な設定管理システムの実装
 */

import { 
  AppConfig, 
  ProjectConfig, 
  ConfigValidationResult,
  ConfigValidationError,
  ConfigValidationWarning,
  DeepPartial 
} from '@/types/config';

// ===== デフォルト設定 =====
const DEFAULT_APP_CONFIG: AppConfig = {
  app: {
    name: "年間スキル報告書システム",
    version: "1.0.0",
    description: "AI駆動開発による年間スキル報告書のWEB化システム",
    organization: "SAS Institute Japan",
    developmentPeriod: "2025年5月-7月"
  },
  api: {
    baseUrl: process.env.NEXT_PUBLIC_API_BASE_URL || "/api",
    timeout: 10000,
    retryCount: 3,
    endpoints: {
      auth: "/auth",
      profile: "/profile",
      skills: "/skills",
      career: "/career",
      work: "/work",
      training: "/training",
      reports: "/reports"
    },
    mockEnabled: process.env.NODE_ENV === 'development'
  },
  ui: {
    theme: {
      primary: "#3399cc",
      secondary: "#f0f0f0",
      accent: "#ff6b35",
      success: "#10b981",
      warning: "#f59e0b",
      error: "#ef4444",
      background: "#ffffff",
      surface: "#f9fafb",
      text: "#111827"
    },
    layout: {
      header: {
        height: "4rem",
        background: "#ffffff",
        showLogo: true,
        showTitle: true
      },
      sidebar: {
        width: "16rem",
        collapsedWidth: "4rem",
        background: "#f9fafb"
      },
      content: {
        padding: "1.5rem",
        maxWidth: "1200px"
      }
    },
    components: {
      button: {
        defaultSize: "md",
        defaultVariant: "primary"
      },
      input: {
        defaultSize: "md"
      },
      modal: {
        defaultSize: "md"
      }
    }
  },
  data: {
    provider: process.env.NODE_ENV === 'development' ? 'mock' : 'api',
    sources: {
      profile: 'api',
      skills: 'api',
      career: 'api',
      work: 'api',
      training: 'api',
      reports: 'api'
    },
    cache: {
      enabled: true,
      ttl: 300000 // 5分
    }
  },
  security: {
    jwt: {
      expiresIn: "1h"
    },
    session: {
      timeout: 3600 // 1時間
    },
    authentication: {
      required: true
    },
    passwordPolicy: {
      minLength: 8,
      requireUppercase: true,
      requireLowercase: true,
      requireNumbers: true,
      requireSymbols: false
    }
  }
};

const DEFAULT_PROJECT_CONFIG: ProjectConfig = {
  project: {
    id: "skill-report-web",
    name: "年間スキル報告書WEB化PJT",
    systemTitle: "年間スキル報告書システム",
    version: "1.0.0",
    description: "AI駆動開発による年間スキル報告書のWEB化システム",
    organization: "SAS Institute Japan",
    developmentPeriod: "2025年5月-7月"
  },
  requirements: {
    categories: [
      { id: "TNT", name: "Multi-Tenant", description: "マルチテナント基盤要件" },
      { id: "PLT", name: "Platform", description: "システム基盤要件" },
      { id: "ACC", name: "Access Control", description: "ユーザー権限管理" },
      { id: "PRO", name: "Profile", description: "個人プロフィール管理" },
      { id: "SKL", name: "Skill", description: "スキル情報管理" },
      { id: "CAR", name: "Career", description: "目標・キャリア管理" },
      { id: "WPM", name: "Work Performance Mgmt", description: "作業実績管理" },
      { id: "TRN", name: "Training", description: "研修・セミナー管理" },
      { id: "RPT", name: "Report", description: "レポート出力" },
      { id: "NTF", name: "Notification", description: "通知・連携サービス" }
    ]
  },
  business: {
    skillLevels: [
      { value: 1, label: "初級", description: "基本的な知識を持っている", symbol: "⭐" },
      { value: 2, label: "中級", description: "実務で活用できる", symbol: "⭐⭐" },
      { value: 3, label: "上級", description: "他者に指導できる", symbol: "⭐⭐⭐" },
      { value: 4, label: "エキスパート", description: "専門家レベル", symbol: "⭐⭐⭐⭐" }
    ],
    goalTypes: [
      { value: "skill", label: "スキル向上" },
      { value: "certification", label: "資格取得" },
      { value: "project", label: "プロジェクト参加" },
      { value: "leadership", label: "リーダーシップ" }
    ],
    skillCategories: [
      { name: "プログラミング言語", key: "programming", icon: "💻" },
      { name: "フレームワーク・ライブラリ", key: "framework", icon: "🔧" },
      { name: "データベース", key: "database", icon: "🗄️" },
      { name: "クラウド・インフラ", key: "cloud", icon: "☁️" },
      { name: "ツール・その他", key: "tools", icon: "🛠️" }
    ],
    reportFormats: ["Excel", "PDF", "CSV"],
    notificationChannels: ["メール", "システム内通知"]
  },
  screens: {
    login: {
      specId: "TNT.3-AUTH.1",
      screenId: "SCR_AUT_Login",
      title: "ログイン",
      description: "システムへのログイン画面",
      layoutType: "login",
      options: {
        showCompanyLogo: true,
        showSystemTitle: true
      }
    },
    home: {
      specId: "PLT.1-WEB.1",
      screenId: "SCR_CMN_Home",
      title: "ホーム",
      description: "ダッシュボード・ホーム画面",
      layoutType: "dashboard",
      options: {
        showWelcomeMessage: true,
        showQuickActions: true
      }
    },
    profile: {
      specId: "PRO.1-BASE.1",
      screenId: "SCR_PRO_Profile",
      title: "プロフィール",
      description: "個人プロフィール管理画面",
      layoutType: "form",
      options: {
        editableFields: true,
        showPhoto: true
      },
      formFields: [
        {
          groupName: "基本情報",
          fields: [
            { name: "emp_no", label: "社員番号", type: "text", required: true, readonly: true },
            { name: "name", label: "氏名", type: "text", required: true },
            { name: "email", label: "メールアドレス", type: "email", required: true },
            { name: "department", label: "部署", type: "select", required: true },
            { name: "position", label: "役職", type: "select", required: false }
          ]
        },
        {
          groupName: "連絡先情報",
          fields: [
            { name: "phone", label: "電話番号", type: "tel", required: false },
            { name: "extension", label: "内線番号", type: "text", required: false }
          ]
        }
      ]
    },
    skill: {
      specId: "SKL.1-HIER.1",
      screenId: "SCR_SKL_Skill",
      title: "スキル情報",
      description: "スキル管理・スキルマップ画面",
      layoutType: "detail",
      options: {
        showRadarChart: true,
        showSkillTree: true
      }
    },
    career: {
      specId: "CAR.1-PLAN.1",
      screenId: "SCR_CAR_Career",
      title: "キャリアプラン",
      description: "キャリア目標・進捗管理画面",
      layoutType: "detail",
      options: {
        showTimeline: true,
        showProgressChart: true
      }
    }
  },
  navigation: {
    sidebarItems: [
      { name: "ホーム", key: "ホーム", icon: "home", route: "/dashboard", specId: "PLT.1-WEB.1" },
      { name: "プロフィール", key: "プロフィール", icon: "user", route: "/profile", specId: "PRO.1-BASE.1" },
      { name: "スキル情報", key: "スキル", icon: "skills", route: "/skills", specId: "SKL.1-HIER.1" },
      { name: "キャリアプラン", key: "キャリア", icon: "career", route: "/career", specId: "CAR.1-PLAN.1" },
      { name: "作業実績", key: "作業実績", icon: "work", route: "/work", specId: "WPM.1-DET.1" },
      { name: "研修管理", key: "研修", icon: "training", route: "/training", specId: "TRN.1-ATT.1" },
      { name: "レポート", key: "レポート", icon: "reports", route: "/reports", specId: "RPT.1-EXCEL.1" }
    ]
  },
  branding: {
    companyName: "SAS Institute Japan",
    systemName: "年間スキル報告書システム",
    logoText: "SAS",
    primaryColor: "#3399cc",
    secondaryColor: "#f0f0f0",
    accentColor: "#ff6b35"
  }
};

// ===== 設定管理クラス =====
export class ConfigManager {
  private static instance: ConfigManager;
  private appConfig: AppConfig;
  private projectConfig: ProjectConfig;

  private constructor() {
    this.appConfig = { ...DEFAULT_APP_CONFIG };
    this.projectConfig = { ...DEFAULT_PROJECT_CONFIG };
  }

  public static getInstance(): ConfigManager {
    if (!ConfigManager.instance) {
      ConfigManager.instance = new ConfigManager();
    }
    return ConfigManager.instance;
  }

  // 設定取得
  public getAppConfig(): AppConfig {
    return { ...this.appConfig };
  }

  public getProjectConfig(): ProjectConfig {
    return { ...this.projectConfig };
  }

  // 部分設定取得
  public getAppConfigSection<K extends keyof AppConfig>(section: K): AppConfig[K] {
    return this.appConfig[section];
  }

  public getProjectConfigSection<K extends keyof ProjectConfig>(section: K): ProjectConfig[K] {
    return this.projectConfig[section];
  }

  // 設定更新
  public updateAppConfig(updates: DeepPartial<AppConfig>): void {
    this.appConfig = this.deepMerge(this.appConfig, updates);
  }

  public updateProjectConfig(updates: DeepPartial<ProjectConfig>): void {
    this.projectConfig = this.deepMerge(this.projectConfig, updates);
  }

  // 環境別設定読み込み
  public async loadEnvironmentConfig(environment: 'development' | 'production' | 'test'): Promise<void> {
    try {
      // 環境別設定ファイルの読み込み（実装時に追加）
      console.log(`Loading configuration for environment: ${environment}`);
    } catch (error) {
      console.warn(`Failed to load environment config for ${environment}:`, error);
    }
  }

  // 設定検証
  public validateConfig(): ConfigValidationResult {
    const errors: ConfigValidationError[] = [];
    const warnings: ConfigValidationWarning[] = [];

    // アプリ設定検証
    if (!this.appConfig.app.name) {
      errors.push({ path: 'app.name', message: 'アプリケーション名は必須です' });
    }

    if (!this.appConfig.api.baseUrl) {
      errors.push({ path: 'api.baseUrl', message: 'API ベースURLは必須です' });
    }

    // プロジェクト設定検証
    if (!this.projectConfig.project.id) {
      errors.push({ path: 'project.id', message: 'プロジェクトIDは必須です' });
    }

    if (this.projectConfig.navigation.sidebarItems.length === 0) {
      warnings.push({ 
        path: 'navigation.sidebarItems', 
        message: 'ナビゲーション項目が設定されていません',
        suggestion: 'ナビゲーション項目を追加してください'
      });
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings
    };
  }

  // 設定リセット
  public resetToDefaults(): void {
    this.appConfig = { ...DEFAULT_APP_CONFIG };
    this.projectConfig = { ...DEFAULT_PROJECT_CONFIG };
  }

  // ディープマージユーティリティ
  private deepMerge<T>(target: T, source: DeepPartial<T>): T {
    const result = { ...target };
    
    for (const key in source) {
      if (source[key] !== undefined) {
        if (typeof source[key] === 'object' && source[key] !== null && !Array.isArray(source[key])) {
          result[key] = this.deepMerge(result[key], source[key] as any);
        } else {
          result[key] = source[key] as any;
        }
      }
    }
    
    return result;
  }
}

// ===== エクスポート用ヘルパー関数 =====
export const getConfig = () => ConfigManager.getInstance();

export const getAppConfig = () => getConfig().getAppConfig();

export const getProjectConfig = () => getConfig().getProjectConfig();

export const getTheme = () => getConfig().getAppConfigSection('ui').theme;

export const getNavigation = () => getConfig().getProjectConfigSection('navigation');

export const getBranding = () => getConfig().getProjectConfigSection('branding');

export const getScreenConfig = (screenKey: string) => {
  const screens = getConfig().getProjectConfigSection('screens');
  return screens[screenKey];
};

export const getBusinessConfig = () => getConfig().getProjectConfigSection('business');

// ===== 初期化関数 =====
export const initializeConfig = async (environment?: 'development' | 'production' | 'test') => {
  const config = getConfig();
  
  try {
    // YAMLファイルから設定を読み込み
    const { loadConfigFiles } = await import('./configLoader');
    const { appConfig, projectConfig } = await loadConfigFiles(environment);
    
    // 読み込んだ設定をマージ
    if (appConfig && Object.keys(appConfig).length > 0) {
      config.updateAppConfig(appConfig);
    }
    if (projectConfig && Object.keys(projectConfig).length > 0) {
      config.updateProjectConfig(projectConfig);
    }
  } catch (error) {
    console.warn('Failed to load YAML config files, using defaults:', error);
  }
  
  // 環境別設定の読み込み
  if (environment) {
    await config.loadEnvironmentConfig(environment);
  }
  
  const validation = config.validateConfig();
  
  if (!validation.isValid) {
    console.error('Configuration validation failed:', validation.errors);
    throw new Error('Invalid configuration');
  }
  
  if (validation.warnings.length > 0) {
    console.warn('Configuration warnings:', validation.warnings);
  }
  
  return config;
};
