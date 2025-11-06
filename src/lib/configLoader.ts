/**
 * 要求仕様ID: PLT.1-WEB.1
 * 設計書: 設定ファイルローダー
 * 実装内容: YAMLファイルから設定を読み込む機能
 */

import { AppConfig, ProjectConfig, DeepPartial } from '@/types/config';

// ===== 設定ファイルパス =====
const CONFIG_PATHS = {
  global: '/config/global/default.yaml',
  project: '/config/projects/skill-report-web.yaml',
  environment: {
    development: '/config/environments/development.yaml',
    production: '/config/environments/production.yaml',
    test: '/config/environments/test.yaml'
  }
} as const;

// ===== YAML解析用インターフェース =====
interface YAMLProjectConfig {
  project_info?: {
    name?: string;
    system_title?: string;
    version?: string;
    description?: string;
    organization?: string;
    development_period?: string;
  };
  requirement_id_system?: {
    categories?: Record<string, string>;
  };
  screens?: Record<string, {
    spec_id?: string;
    screen_id?: string;
    title?: string;
    description?: string;
    layout_type?: string;
    [key: string]: any;
  }>;
  navigation?: {
    sidebar_items?: Array<{
      name?: string;
      key?: string;
      icon?: string;
      route?: string;
      spec_id?: string;
    }>;
  };
  branding?: {
    company_name?: string;
    system_name?: string;
    logo_text?: string;
    primary_color?: string;
    secondary_color?: string;
    accent_color?: string;
  };
  skills?: {
    categories?: Array<{
      name?: string;
      key?: string;
      icon?: string;
    }>;
    levels?: Record<number, string>;
  };
  form_fields?: {
    profile?: Record<string, Array<{
      name?: string;
      label?: string;
      type?: string;
      required?: boolean;
      readonly?: boolean;
    }>>;
  };
  reports?: {
    formats?: string[];
  };
  notifications?: {
    channels?: string[];
  };
}

interface YAMLGlobalConfig {
  app?: {
    name?: string;
    version?: string;
    description?: string;
  };
  api?: {
    base_url?: string;
    timeout?: number;
    retry_count?: number;
    endpoints?: Record<string, string>;
    mock_enabled?: boolean;
  };
  ui?: {
    theme?: Record<string, string>;
    layout?: Record<string, any>;
    components?: Record<string, any>;
  };
  data?: {
    provider?: string;
    sources?: Record<string, string>;
    cache?: {
      enabled?: boolean;
      ttl?: number;
    };
  };
  security?: {
    jwt?: {
      expires_in?: string;
    };
    session?: {
      timeout?: number;
    };
    authentication?: {
      required?: boolean;
    };
    password_policy?: {
      min_length?: number;
      require_uppercase?: boolean;
      require_lowercase?: boolean;
      require_numbers?: boolean;
      require_symbols?: boolean;
    };
  };
}

// ===== 設定ファイルローダークラス =====
export class ConfigFileLoader {
  private static instance: ConfigFileLoader;

  private constructor() {}

  public static getInstance(): ConfigFileLoader {
    if (!ConfigFileLoader.instance) {
      ConfigFileLoader.instance = new ConfigFileLoader();
    }
    return ConfigFileLoader.instance;
  }

  // ===== メイン読み込み関数 =====
  public async loadConfigs(environment?: 'development' | 'production' | 'test'): Promise<{
    appConfig: DeepPartial<AppConfig>;
    projectConfig: DeepPartial<ProjectConfig>;
  }> {
    try {
      // 並列でファイル読み込み
      const [globalConfig, projectConfig, envConfig] = await Promise.all([
        this.loadGlobalConfig(),
        this.loadProjectConfig(),
        environment ? this.loadEnvironmentConfig(environment) : Promise.resolve({})
      ]);

      // グローバル設定をアプリ設定に変換
      const appConfig = this.transformGlobalToAppConfig(globalConfig);

      // 環境設定をマージ
      const mergedAppConfig = this.deepMerge(appConfig, envConfig);

      return {
        appConfig: mergedAppConfig,
        projectConfig: this.transformYAMLToProjectConfig(projectConfig)
      };
    } catch (error) {
      console.error('Failed to load configuration files:', error);
      throw new Error('設定ファイルの読み込みに失敗しました');
    }
  }

  // ===== 個別ファイル読み込み =====
  private async loadGlobalConfig(): Promise<YAMLGlobalConfig> {
    try {
      const response = await fetch(CONFIG_PATHS.global);
      if (!response.ok) {
        throw new Error(`Failed to load global config: ${response.status}`);
      }
      const yamlText = await response.text();
      return this.parseYAML(yamlText);
    } catch (error) {
      console.warn('Global config not found, using defaults');
      return {};
    }
  }

  private async loadProjectConfig(): Promise<YAMLProjectConfig> {
    try {
      const response = await fetch(CONFIG_PATHS.project);
      if (!response.ok) {
        throw new Error(`Failed to load project config: ${response.status}`);
      }
      const yamlText = await response.text();
      return this.parseYAML(yamlText);
    } catch (error) {
      console.warn('Project config not found, using defaults');
      return {};
    }
  }

  private async loadEnvironmentConfig(environment: 'development' | 'production' | 'test'): Promise<DeepPartial<AppConfig>> {
    try {
      const response = await fetch(CONFIG_PATHS.environment[environment]);
      if (!response.ok) {
        throw new Error(`Failed to load environment config: ${response.status}`);
      }
      const yamlText = await response.text();
      const yamlConfig = this.parseYAML(yamlText);
      return this.transformGlobalToAppConfig(yamlConfig);
    } catch (error) {
      console.warn(`Environment config for ${environment} not found, using defaults`);
      return {};
    }
  }

  // ===== YAML解析 =====
  private parseYAML(yamlText: string): any {
    try {
      // 簡易YAML解析（本格的な実装ではjs-yamlライブラリを使用）
      const lines = yamlText.split('\n');
      const result: any = {};
      let currentPath: string[] = [];
      let currentObject = result;

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#')) continue;

        const indent = line.length - line.trimStart().length;
        const colonIndex = trimmed.indexOf(':');
        
        if (colonIndex === -1) continue;

        const key = trimmed.substring(0, colonIndex).trim();
        const value = trimmed.substring(colonIndex + 1).trim();

        // インデントレベルに基づいてパスを調整
        const level = Math.floor(indent / 2);
        currentPath = currentPath.slice(0, level);
        currentPath.push(key);

        // オブジェクトの参照を更新
        currentObject = result;
        for (let i = 0; i < currentPath.length - 1; i++) {
          const pathKey = currentPath[i];
          if (pathKey && !currentObject[pathKey]) {
            currentObject[pathKey] = {};
          }
          if (pathKey) {
            currentObject = currentObject[pathKey];
          }
        }

        // 値を設定
        if (value) {
          currentObject[key] = this.parseValue(value);
        } else {
          currentObject[key] = {};
        }
      }

      return result;
    } catch (error) {
      console.error('YAML parsing failed:', error);
      return {};
    }
  }

  private parseValue(value: string): any {
    // 文字列の値を適切な型に変換
    if (value === 'true') return true;
    if (value === 'false') return false;
    if (value === 'null') return null;
    if (/^\d+$/.test(value)) return parseInt(value, 10);
    if (/^\d+\.\d+$/.test(value)) return parseFloat(value);
    if (value.startsWith('"') && value.endsWith('"')) {
      return value.slice(1, -1);
    }
    if (value.startsWith("'") && value.endsWith("'")) {
      return value.slice(1, -1);
    }
    return value;
  }

  // ===== 設定変換 =====
  private transformGlobalToAppConfig(yamlConfig: YAMLGlobalConfig): DeepPartial<AppConfig> {
    const appConfig: DeepPartial<AppConfig> = {};

    if (yamlConfig.app) {
      const app: any = {};
      if (yamlConfig.app.name) app.name = yamlConfig.app.name;
      if (yamlConfig.app.version) app.version = yamlConfig.app.version;
      if (yamlConfig.app.description) app.description = yamlConfig.app.description;
      if (Object.keys(app).length > 0) appConfig.app = app;
    }

    if (yamlConfig.api) {
      const api: any = {};
      if (yamlConfig.api.base_url) api.baseUrl = yamlConfig.api.base_url;
      if (yamlConfig.api.timeout) api.timeout = yamlConfig.api.timeout;
      if (yamlConfig.api.retry_count) api.retryCount = yamlConfig.api.retry_count;
      if (yamlConfig.api.endpoints) api.endpoints = yamlConfig.api.endpoints;
      if (yamlConfig.api.mock_enabled !== undefined) api.mockEnabled = yamlConfig.api.mock_enabled;
      if (Object.keys(api).length > 0) appConfig.api = api;
    }

    if (yamlConfig.ui?.theme) {
      const theme: any = {};
      if (yamlConfig.ui.theme.primary) theme.primary = yamlConfig.ui.theme.primary;
      if (yamlConfig.ui.theme.secondary) theme.secondary = yamlConfig.ui.theme.secondary;
      if (yamlConfig.ui.theme.accent) theme.accent = yamlConfig.ui.theme.accent;
      if (yamlConfig.ui.theme.success) theme.success = yamlConfig.ui.theme.success;
      if (yamlConfig.ui.theme.warning) theme.warning = yamlConfig.ui.theme.warning;
      if (yamlConfig.ui.theme.error) theme.error = yamlConfig.ui.theme.error;
      if (yamlConfig.ui.theme.background) theme.background = yamlConfig.ui.theme.background;
      if (yamlConfig.ui.theme.surface) theme.surface = yamlConfig.ui.theme.surface;
      if (yamlConfig.ui.theme.text) theme.text = yamlConfig.ui.theme.text;
      if (Object.keys(theme).length > 0) {
        appConfig.ui = { theme };
      }
    }

    if (yamlConfig.data) {
      const data: any = {};
      if (yamlConfig.data.provider) data.provider = yamlConfig.data.provider;
      if (yamlConfig.data.sources) data.sources = yamlConfig.data.sources;
      if (yamlConfig.data.cache) data.cache = yamlConfig.data.cache;
      if (Object.keys(data).length > 0) appConfig.data = data;
    }

    if (yamlConfig.security) {
      const security: any = {
        jwt: {
          expiresIn: yamlConfig.security.jwt?.expires_in || '1h'
        },
        session: {
          timeout: yamlConfig.security.session?.timeout || 3600
        },
        authentication: {
          required: yamlConfig.security.authentication?.required ?? true
        }
      };

      if (yamlConfig.security.password_policy) {
        security.passwordPolicy = {
          minLength: yamlConfig.security.password_policy.min_length || 8,
          requireUppercase: yamlConfig.security.password_policy.require_uppercase ?? true,
          requireLowercase: yamlConfig.security.password_policy.require_lowercase ?? true,
          requireNumbers: yamlConfig.security.password_policy.require_numbers ?? true,
          requireSymbols: yamlConfig.security.password_policy.require_symbols ?? false
        };
      }

      appConfig.security = security;
    }

    return appConfig;
  }

  private transformYAMLToProjectConfig(yamlConfig: YAMLProjectConfig): DeepPartial<ProjectConfig> {
    const projectConfig: DeepPartial<ProjectConfig> = {};

    if (yamlConfig.project_info) {
      const project: any = {
        id: 'skill-report-web'
      };
      if (yamlConfig.project_info.name) project.name = yamlConfig.project_info.name;
      if (yamlConfig.project_info.system_title) project.systemTitle = yamlConfig.project_info.system_title;
      if (yamlConfig.project_info.version) project.version = yamlConfig.project_info.version;
      if (yamlConfig.project_info.description) project.description = yamlConfig.project_info.description;
      if (yamlConfig.project_info.organization) project.organization = yamlConfig.project_info.organization;
      if (yamlConfig.project_info.development_period) project.developmentPeriod = yamlConfig.project_info.development_period;
      projectConfig.project = project;
    }

    if (yamlConfig.requirement_id_system?.categories) {
      projectConfig.requirements = {
        categories: Object.entries(yamlConfig.requirement_id_system.categories).map(([id, description]) => ({
          id,
          name: id,
          description
        }))
      };
    }

    if (yamlConfig.screens) {
      projectConfig.screens = {};
      for (const [key, screen] of Object.entries(yamlConfig.screens)) {
        projectConfig.screens[key] = {
          specId: screen.spec_id || '',
          screenId: screen.screen_id || '',
          title: screen.title || '',
          description: screen.description || '',
          layoutType: screen.layout_type as any || 'detail'
        };
      }
    }

    if (yamlConfig.navigation?.sidebar_items) {
      projectConfig.navigation = {
        sidebarItems: yamlConfig.navigation.sidebar_items.map(item => ({
          name: item.name || '',
          key: item.key || '',
          icon: item.icon || '',
          route: item.route || '',
          specId: item.spec_id || ''
        }))
      };
    }

    if (yamlConfig.branding) {
      projectConfig.branding = {
        companyName: yamlConfig.branding.company_name || '',
        systemName: yamlConfig.branding.system_name || '',
        logoText: yamlConfig.branding.logo_text || '',
        primaryColor: yamlConfig.branding.primary_color || '#3399cc',
        secondaryColor: yamlConfig.branding.secondary_color || '#f0f0f0',
        accentColor: yamlConfig.branding.accent_color || '#ff6b35'
      };
    }

    if (yamlConfig.skills) {
      const business: any = {};
      
      if (yamlConfig.skills.categories) {
        business.skillCategories = yamlConfig.skills.categories.map(cat => ({
          name: cat.name || '',
          key: cat.key || '',
          icon: cat.icon || ''
        }));
      }

      if (yamlConfig.skills.levels) {
        business.skillLevels = Object.entries(yamlConfig.skills.levels).map(([value, label]) => ({
          value: parseInt(value, 10),
          label,
          description: `${label}レベル`,
          symbol: '⭐'.repeat(parseInt(value, 10))
        }));
      }

      if (yamlConfig.reports?.formats) {
        business.reportFormats = yamlConfig.reports.formats;
      }

      if (yamlConfig.notifications?.channels) {
        business.notificationChannels = yamlConfig.notifications.channels;
      }

      if (Object.keys(business).length > 0) {
        projectConfig.business = business;
      }
    }

    return projectConfig;
  }

  // ===== ユーティリティ =====
  private deepMerge<T>(target: T, source: any): T {
    const result = { ...target };
    
    for (const key in source) {
      if (source[key] !== undefined) {
        if (typeof source[key] === 'object' && source[key] !== null && !Array.isArray(source[key])) {
          result[key as keyof T] = this.deepMerge(result[key as keyof T] || {} as any, source[key]);
        } else {
          result[key as keyof T] = source[key];
        }
      }
    }
    
    return result;
  }
}

// ===== エクスポート用関数 =====
export const loadConfigFiles = async (environment?: 'development' | 'production' | 'test') => {
  const loader = ConfigFileLoader.getInstance();
  return loader.loadConfigs(environment);
};

export const getConfigLoader = () => ConfigFileLoader.getInstance();
