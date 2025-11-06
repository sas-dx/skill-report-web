/**
 * 要求仕様ID: PLT.1-WEB.1
 * 設計書: 設定管理システム型定義
 * 実装内容: アプリケーション設定の型安全性を保証する型定義
 */

// ===== 基本設定型 =====
export interface AppConfig {
  app: AppInfo;
  api: APIConfig;
  ui: UIConfig;
  data: DataConfig;
  security: SecurityConfig;
}

export interface ProjectConfig {
  project: ProjectInfo;
  requirements: RequirementConfig;
  business: BusinessConfig;
  screens: ScreenConfig;
  navigation: NavigationConfig;
  branding: BrandingConfig;
}

// ===== アプリケーション情報 =====
export interface AppInfo {
  name: string;
  version: string;
  description: string;
  organization?: string;
  developmentPeriod?: string;
}

// ===== API設定 =====
export interface APIConfig {
  baseUrl: string;
  timeout: number;
  retryCount: number;
  endpoints: Record<string, string>;
  mockEnabled?: boolean;
}

// ===== UI設定 =====
export interface UIConfig {
  theme: ThemeConfig;
  layout: LayoutConfig;
  components: ComponentConfig;
}

export interface ThemeConfig {
  primary: string;
  secondary: string;
  accent: string;
  success: string;
  warning: string;
  error: string;
  background: string;
  surface: string;
  text: string;
}

export interface LayoutConfig {
  header: {
    height: string;
    background: string;
    showLogo: boolean;
    showTitle: boolean;
  };
  sidebar: {
    width: string;
    collapsedWidth: string;
    background: string;
  };
  content: {
    padding: string;
    maxWidth: string;
  };
}

export interface ComponentConfig {
  button: {
    defaultSize: 'sm' | 'md' | 'lg';
    defaultVariant: 'primary' | 'secondary' | 'outline';
  };
  input: {
    defaultSize: 'sm' | 'md' | 'lg';
  };
  modal: {
    defaultSize: 'sm' | 'md' | 'lg' | 'xl';
  };
}

// ===== データ設定 =====
export interface DataConfig {
  provider: 'mock' | 'api' | 'hybrid';
  sources: Record<string, 'mock' | 'api'>;
  cache: {
    enabled: boolean;
    ttl: number;
  };
}

// ===== セキュリティ設定 =====
export interface SecurityConfig {
  jwt: {
    expiresIn: string;
  };
  session: {
    timeout: number;
  };
  authentication: {
    required: boolean;
  };
  passwordPolicy?: {
    minLength: number;
    requireUppercase: boolean;
    requireLowercase: boolean;
    requireNumbers: boolean;
    requireSymbols: boolean;
  };
}

// ===== プロジェクト情報 =====
export interface ProjectInfo {
  id: string;
  name: string;
  systemTitle: string;
  version: string;
  description: string;
  organization: string;
  developmentPeriod: string;
}

// ===== 要求仕様設定 =====
export interface RequirementConfig {
  categories: RequirementCategory[];
}

export interface RequirementCategory {
  id: string;
  name: string;
  description: string;
}

// ===== 業務設定 =====
export interface BusinessConfig {
  skillLevels: SkillLevel[];
  goalTypes: GoalType[];
  skillCategories: SkillCategory[];
  reportFormats: string[];
  notificationChannels: string[];
}

export interface SkillLevel {
  value: number;
  label: string;
  description: string;
  symbol?: string;
}

export interface GoalType {
  value: string;
  label: string;
  description?: string;
}

export interface SkillCategory {
  name: string;
  key: string;
  icon: string;
}

// ===== 画面設定 =====
export interface ScreenConfig {
  [screenKey: string]: ScreenInfo;
}

export interface ScreenInfo {
  specId: string;
  screenId: string;
  title: string;
  description: string;
  layoutType: 'login' | 'dashboard' | 'form' | 'detail' | 'list';
  options?: Record<string, boolean>;
  formFields?: FormFieldGroup[];
}

export interface FormFieldGroup {
  groupName: string;
  fields: FormField[];
}

export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'tel' | 'select' | 'textarea' | 'checkbox' | 'radio';
  required: boolean;
  readonly?: boolean;
  options?: string[];
  validation?: {
    pattern?: string;
    minLength?: number;
    maxLength?: number;
  };
}

// ===== ナビゲーション設定 =====
export interface NavigationConfig {
  sidebarItems: NavigationItem[];
}

export interface NavigationItem {
  name: string;
  key: string;
  icon: string;
  route: string;
  specId: string;
  children?: NavigationItem[];
  badge?: {
    text: string;
    variant: 'primary' | 'secondary' | 'success' | 'warning' | 'error';
  };
}

// ===== ブランディング設定 =====
export interface BrandingConfig {
  companyName: string;
  systemName: string;
  logoText: string;
  primaryColor: string;
  secondaryColor: string;
  accentColor: string;
  logo?: {
    url: string;
    alt: string;
    width: number;
    height: number;
  };
}

// ===== 環境別設定 =====
export interface EnvironmentConfig {
  development: Partial<AppConfig>;
  production: Partial<AppConfig>;
  test: Partial<AppConfig>;
}

// ===== 設定管理用ヘルパー型 =====
export type ConfigKey = keyof AppConfig | keyof ProjectConfig;
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// ===== 設定検証用型 =====
export interface ConfigValidationResult {
  isValid: boolean;
  errors: ConfigValidationError[];
  warnings: ConfigValidationWarning[];
}

export interface ConfigValidationError {
  path: string;
  message: string;
  value?: any;
}

export interface ConfigValidationWarning {
  path: string;
  message: string;
  suggestion?: string;
}

// ===== React Context用型 =====
export interface ConfigContextValue {
  appConfig: AppConfig;
  projectConfig: ProjectConfig;
  isLoading: boolean;
  error: string | null;
  reload: () => Promise<void>;
}

// ===== 設定更新用型 =====
export interface ConfigUpdateRequest {
  path: string;
  value: any;
  environment?: 'development' | 'production' | 'test';
}

export interface ConfigUpdateResult {
  success: boolean;
  message: string;
  updatedConfig?: Partial<AppConfig | ProjectConfig>;
}
