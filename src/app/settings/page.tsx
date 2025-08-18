'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card } from '@/components/ui/Card';
import { Select } from '@/components/ui/Select';
import {
  Settings,
  User,
  Bell,
  Palette,
  Shield,
  Save,
  Check,
  ArrowLeft,
  Home,
} from 'lucide-react';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`settings-tabpanel-${index}`}
      aria-labelledby={`settings-tab-${index}`}
      {...other}
    >
      {value === index && <div className="p-6">{children}</div>}
    </div>
  );
}

export default function SettingsPage() {
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  
  // プロファイル設定
  const [profile, setProfile] = useState({
    displayName: '',
    email: '',
    phone: '',
    department: '',
    position: '',
  });

  // 通知設定
  const [notifications, setNotifications] = useState({
    emailNotifications: true,
    pushNotifications: false,
    weeklyReport: true,
    monthlyReport: true,
    skillUpdateReminder: true,
    trainingReminder: true,
  });

  // 表示設定
  const [display, setDisplay] = useState({
    theme: 'light',
    language: 'ja',
    dateFormat: 'YYYY/MM/DD',
    itemsPerPage: '10',
    defaultView: 'dashboard',
  });

  // セキュリティ設定
  const [security, setSecurity] = useState({
    twoFactorAuth: false,
    sessionTimeout: '30',
    passwordExpiry: '90',
  });

  useEffect(() => {
    // 設定を読み込む
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      setLoading(true);
      // APIから設定を取得
      const response = await fetch('/api/dashboard/settings');
      if (response.ok) {
        const data = await response.json();
        // 設定を適用
        console.log('Settings loaded:', data);
      }
    } catch (error) {
      console.error('Failed to load settings:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveSettings = async () => {
    try {
      setLoading(true);
      // 設定を保存
      const response = await fetch('/api/dashboard/settings', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          profile,
          notifications,
          display,
          security,
        }),
      });

      if (response.ok) {
        setSaveSuccess(true);
        setTimeout(() => setSaveSuccess(false), 3000);
      }
    } catch (error) {
      console.error('Failed to save settings:', error);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 0, label: 'プロファイル', icon: User },
    { id: 1, label: '通知', icon: Bell },
    { id: 2, label: '表示', icon: Palette },
    { id: 3, label: 'セキュリティ', icon: Shield },
  ];

  return (
    <div className="container mx-auto max-w-6xl px-4 py-8">
      {/* ダッシュボードへ戻るボタン */}
      <div className="mb-4">
        <Button
          variant="outline"
          onClick={() => window.location.href = '/dashboard'}
          className="flex items-center"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          ダッシュボードへ戻る
        </Button>
      </div>

      <Card className="bg-white shadow-lg">
        <div className="border-b border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center">
              <Settings className="w-8 h-8 mr-3 text-gray-700" />
              <h1 className="text-3xl font-bold text-gray-900">設定</h1>
            </div>
            <Button
              variant="ghost"
              onClick={() => window.location.href = '/dashboard'}
              className="flex items-center text-gray-600 hover:text-gray-900"
            >
              <Home className="w-5 h-5 mr-2" />
              ホーム
            </Button>
          </div>

          {/* タブナビゲーション */}
          <div className="flex space-x-1 border-b border-gray-200">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setTabValue(tab.id)}
                  className={`flex items-center px-4 py-3 text-sm font-medium transition-colors duration-200 border-b-2 -mb-px ${
                    tabValue === tab.id
                      ? 'text-blue-600 border-blue-600'
                      : 'text-gray-500 border-transparent hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="w-4 h-4 mr-2" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* プロファイル設定 */}
        <TabPanel value={tabValue} index={0}>
          <h2 className="text-xl font-semibold mb-6">プロファイル設定</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                表示名
              </label>
              <Input
                type="text"
                value={profile.displayName}
                onChange={(e) => setProfile({ ...profile, displayName: e.target.value })}
                placeholder="山田 太郎"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                メールアドレス
              </label>
              <Input
                type="email"
                value={profile.email}
                onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                placeholder="example@company.com"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                電話番号
              </label>
              <Input
                type="tel"
                value={profile.phone}
                onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                placeholder="090-1234-5678"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                部署
              </label>
              <Input
                type="text"
                value={profile.department}
                onChange={(e) => setProfile({ ...profile, department: e.target.value })}
                placeholder="開発部"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                役職
              </label>
              <Input
                type="text"
                value={profile.position}
                onChange={(e) => setProfile({ ...profile, position: e.target.value })}
                placeholder="シニアエンジニア"
              />
            </div>
          </div>
        </TabPanel>

        {/* 通知設定 */}
        <TabPanel value={tabValue} index={1}>
          <h2 className="text-xl font-semibold mb-6">通知設定</h2>
          
          <div className="space-y-6">
            <Card className="p-6 bg-gray-50">
              <h3 className="text-lg font-medium mb-4">通知方法</h3>
              <div className="space-y-3">
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={notifications.emailNotifications}
                    onChange={(e) =>
                      setNotifications({ ...notifications, emailNotifications: e.target.checked })
                    }
                    className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <span className="ml-3 text-gray-700">メール通知</span>
                </label>
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={notifications.pushNotifications}
                    onChange={(e) =>
                      setNotifications({ ...notifications, pushNotifications: e.target.checked })
                    }
                    className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <span className="ml-3 text-gray-700">プッシュ通知</span>
                </label>
              </div>
            </Card>

            <Card className="p-6 bg-gray-50">
              <h3 className="text-lg font-medium mb-4">定期レポート</h3>
              <div className="space-y-3">
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={notifications.weeklyReport}
                    onChange={(e) =>
                      setNotifications({ ...notifications, weeklyReport: e.target.checked })
                    }
                    className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <span className="ml-3 text-gray-700">週次レポート</span>
                </label>
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={notifications.monthlyReport}
                    onChange={(e) =>
                      setNotifications({ ...notifications, monthlyReport: e.target.checked })
                    }
                    className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <span className="ml-3 text-gray-700">月次レポート</span>
                </label>
              </div>
              
              <hr className="my-4 border-gray-300" />
              
              <h3 className="text-lg font-medium mb-4">リマインダー</h3>
              <div className="space-y-3">
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={notifications.skillUpdateReminder}
                    onChange={(e) =>
                      setNotifications({ ...notifications, skillUpdateReminder: e.target.checked })
                    }
                    className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <span className="ml-3 text-gray-700">スキル更新リマインダー</span>
                </label>
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={notifications.trainingReminder}
                    onChange={(e) =>
                      setNotifications({ ...notifications, trainingReminder: e.target.checked })
                    }
                    className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <span className="ml-3 text-gray-700">研修リマインダー</span>
                </label>
              </div>
            </Card>
          </div>
        </TabPanel>

        {/* 表示設定 */}
        <TabPanel value={tabValue} index={2}>
          <h2 className="text-xl font-semibold mb-6">表示設定</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                テーマ
              </label>
              <Select
                value={display.theme}
                onChange={(value) => setDisplay({ ...display, theme: value })}
                options={[
                  { value: 'light', label: 'ライト' },
                  { value: 'dark', label: 'ダーク' },
                  { value: 'auto', label: '自動' },
                ]}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                言語
              </label>
              <Select
                value={display.language}
                onChange={(value) => setDisplay({ ...display, language: value })}
                options={[
                  { value: 'ja', label: '日本語' },
                  { value: 'en', label: 'English' },
                ]}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                日付形式
              </label>
              <Select
                value={display.dateFormat}
                onChange={(value) => setDisplay({ ...display, dateFormat: value })}
                options={[
                  { value: 'YYYY/MM/DD', label: 'YYYY/MM/DD' },
                  { value: 'YYYY-MM-DD', label: 'YYYY-MM-DD' },
                  { value: 'DD/MM/YYYY', label: 'DD/MM/YYYY' },
                  { value: 'MM/DD/YYYY', label: 'MM/DD/YYYY' },
                ]}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                1ページあたりの表示件数
              </label>
              <Select
                value={display.itemsPerPage}
                onChange={(value) => setDisplay({ ...display, itemsPerPage: value })}
                options={[
                  { value: '10', label: '10件' },
                  { value: '25', label: '25件' },
                  { value: '50', label: '50件' },
                  { value: '100', label: '100件' },
                ]}
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                デフォルト表示画面
              </label>
              <Select
                value={display.defaultView}
                onChange={(value) => setDisplay({ ...display, defaultView: value })}
                options={[
                  { value: 'dashboard', label: 'ダッシュボード' },
                  { value: 'profile', label: 'プロファイル' },
                  { value: 'skills', label: 'スキル管理' },
                  { value: 'work', label: '作業実績' },
                ]}
              />
            </div>
          </div>
        </TabPanel>

        {/* セキュリティ設定 */}
        <TabPanel value={tabValue} index={3}>
          <h2 className="text-xl font-semibold mb-6">セキュリティ設定</h2>
          
          <div className="space-y-6">
            <Card className="p-6 bg-gray-50">
              <label className="flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={security.twoFactorAuth}
                  onChange={(e) =>
                    setSecurity({ ...security, twoFactorAuth: e.target.checked })
                  }
                  className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                />
                <div className="ml-3">
                  <span className="text-gray-700 font-medium">二要素認証を有効にする</span>
                  <p className="text-sm text-gray-500 mt-1">
                    ログイン時に追加の認証コードが必要になります
                  </p>
                </div>
              </label>
            </Card>

            <Card className="p-6 bg-gray-50">
              <h3 className="text-lg font-medium mb-4">セッション設定</h3>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  セッションタイムアウト（分）
                </label>
                <Input
                  type="number"
                  value={security.sessionTimeout}
                  onChange={(e) =>
                    setSecurity({ ...security, sessionTimeout: e.target.value })
                  }
                  placeholder="30"
                />
                <p className="text-sm text-gray-500 mt-2">
                  無操作時に自動的にログアウトするまでの時間
                </p>
              </div>
            </Card>

            <Card className="p-6 bg-gray-50">
              <h3 className="text-lg font-medium mb-4">パスワードポリシー</h3>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  パスワード有効期限（日）
                </label>
                <Input
                  type="number"
                  value={security.passwordExpiry}
                  onChange={(e) =>
                    setSecurity({ ...security, passwordExpiry: e.target.value })
                  }
                  placeholder="90"
                />
                <p className="text-sm text-gray-500 mt-2">
                  パスワードの変更が必要になるまでの日数
                </p>
                <Button
                  variant="outline"
                  className="mt-4"
                  onClick={() => {
                    // パスワード変更画面へ遷移
                    window.location.href = '/change-password';
                  }}
                >
                  パスワードを変更
                </Button>
              </div>
            </Card>
          </div>
        </TabPanel>

        {/* 保存ボタン */}
        <div className="border-t border-gray-200 px-6 py-4 bg-gray-50">
          <div className="flex justify-end items-center">
            {saveSuccess && (
              <div className="flex items-center text-green-600 mr-4">
                <Check className="w-5 h-5 mr-2" />
                <span>設定を保存しました</span>
              </div>
            )}
            <Button
              onClick={handleSaveSettings}
              disabled={loading}
              className="flex items-center"
            >
              <Save className="w-4 h-4 mr-2" />
              設定を保存
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}