/**
 * 要求仕様ID: PLT.1-WEB.1
 * 設計書: 設定管理システムReact Context Provider
 * 実装内容: アプリケーション全体で設定を利用するためのContext Provider
 */

'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { AppConfig, ProjectConfig } from '@/types/config';
import { initializeConfig, getConfig } from '@/lib/config';

interface ConfigContextType {
  appConfig: AppConfig;
  projectConfig: ProjectConfig;
  isLoading: boolean;
  error: string | null;
  reloadConfig: () => Promise<void>;
}

const ConfigContext = createContext<ConfigContextType | null>(null);

export function ConfigProvider({ children }: { children: React.ReactNode }) {
  const [appConfig, setAppConfig] = useState<AppConfig | null>(null);
  const [projectConfig, setProjectConfig] = useState<ProjectConfig | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadConfig = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      // 環境を判定
      const environment = process.env.NODE_ENV === 'production' ? 'production' : 
                         process.env.NODE_ENV === 'test' ? 'test' : 'development';
      
      // 設定システムを初期化（YAMLファイルから読み込み）
      await initializeConfig(environment);
      
      // 初期化された設定を取得
      const configManager = getConfig();
      const app = configManager.getAppConfig();
      const project = configManager.getProjectConfig();
      
      setAppConfig(app);
      setProjectConfig(project);
      
      console.log('Configuration loaded successfully:', {
        environment,
        appName: app.app.name,
        projectName: project.project.name
      });
    } catch (err) {
      console.error('Configuration loading failed:', err);
      setError(err instanceof Error ? err.message : '設定の読み込みに失敗しました');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadConfig();
  }, []);

  if (isLoading || !appConfig || !projectConfig) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">設定を読み込み中...</p>
          {process.env.NODE_ENV === 'development' && (
            <p className="text-xs text-gray-400 mt-2">
              YAMLファイルから設定を読み込んでいます...
            </p>
          )}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center max-w-md">
          <div className="text-red-600 mb-4 text-4xl">⚠️</div>
          <h2 className="text-lg font-semibold text-red-600 mb-2">設定エラー</h2>
          <p className="text-red-600 mb-4 text-sm">{error}</p>
          {process.env.NODE_ENV === 'development' && (
            <div className="text-xs text-gray-500 mb-4 p-3 bg-gray-50 rounded">
              <p>開発環境では以下を確認してください：</p>
              <ul className="list-disc list-inside mt-2 text-left">
                <li>config/global/default.yaml が存在するか</li>
                <li>config/projects/skill-report-web.yaml が存在するか</li>
                <li>YAMLファイルの構文が正しいか</li>
              </ul>
            </div>
          )}
          <button 
            onClick={loadConfig}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
          >
            再試行
          </button>
        </div>
      </div>
    );
  }

  return (
    <ConfigContext.Provider 
      value={{
        appConfig,
        projectConfig,
        isLoading,
        error,
        reloadConfig: loadConfig
      }}
    >
      {children}
    </ConfigContext.Provider>
  );
}

export function useConfig() {
  const context = useContext(ConfigContext);
  if (!context) {
    throw new Error('useConfig must be used within a ConfigProvider');
  }
  return context;
}

// 便利なフック
export function useAppConfig() {
  const { appConfig } = useConfig();
  return appConfig;
}

export function useProjectConfig() {
  const { projectConfig } = useConfig();
  return projectConfig;
}

export function useTheme() {
  const { appConfig } = useConfig();
  return appConfig.ui.theme;
}

export function useBranding() {
  const { projectConfig } = useConfig();
  return projectConfig.branding;
}

export function useNavigation() {
  const { projectConfig } = useConfig();
  return projectConfig.navigation;
}

export function useScreenConfig(screenKey: string) {
  const { projectConfig } = useConfig();
  return projectConfig.screens[screenKey];
}

export function useBusinessConfig() {
  const { projectConfig } = useConfig();
  return projectConfig.business;
}

export function useAPIConfig() {
  const { appConfig } = useConfig();
  return appConfig.api;
}

export function useSecurityConfig() {
  const { appConfig } = useConfig();
  return appConfig.security;
}

// 設定更新用Hook
export function useConfigUpdater() {
  const { reloadConfig } = useConfig();
  
  const updateAppConfig = (updates: Partial<AppConfig>) => {
    const configManager = getConfig();
    configManager.updateAppConfig(updates);
    reloadConfig();
  };

  const updateProjectConfig = (updates: Partial<ProjectConfig>) => {
    const configManager = getConfig();
    configManager.updateProjectConfig(updates);
    reloadConfig();
  };

  const resetToDefaults = () => {
    const configManager = getConfig();
    configManager.resetToDefaults();
    reloadConfig();
  };

  return {
    updateAppConfig,
    updateProjectConfig,
    resetToDefaults,
    reload: reloadConfig
  };
}

// 設定検証用Hook
export function useConfigValidation() {
  const [validationResult, setValidationResult] = useState<any>(null);
  
  const validateConfig = () => {
    const configManager = getConfig();
    const result = configManager.validateConfig();
    setValidationResult(result);
    return result;
  };

  useEffect(() => {
    validateConfig();
  }, []);

  return {
    validationResult,
    validateConfig,
    isValid: validationResult?.isValid ?? true,
    errors: validationResult?.errors ?? [],
    warnings: validationResult?.warnings ?? []
  };
}

// 環境別設定用Hook
export function useEnvironmentConfig() {
  const { appConfig } = useConfig();
  
  const isDevelopment = process.env.NODE_ENV === 'development';
  const isProduction = process.env.NODE_ENV === 'production';
  const isTest = process.env.NODE_ENV === 'test';
  
  const isMockEnabled = appConfig.api.mockEnabled || isDevelopment;
  const isDebugMode = isDevelopment;
  
  return {
    environment: process.env.NODE_ENV,
    isDevelopment,
    isProduction,
    isTest,
    isMockEnabled,
    isDebugMode
  };
}
