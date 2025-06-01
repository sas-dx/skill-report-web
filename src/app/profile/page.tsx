// PRO.1-BASE.1: プロフィール画面
'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { Sidebar } from '@/components/dashboard/Sidebar';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Spinner } from '@/components/ui/Spinner';

interface UserProfile {
  emp_no: string;
  name: string;
  email: string;
  department: string;
  position: string;
  hire_date: string;
  phone?: string;
  emergency_contact?: string;
  skills_summary?: string;
}

export default function ProfilePage() {
  const router = useRouter();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [editedProfile, setEditedProfile] = useState<UserProfile | null>(null);

  const handleMenuClick = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSidebarClose = () => {
    setIsSidebarOpen(false);
  };

  // モックデータの読み込み
  useEffect(() => {
    const loadProfile = async () => {
      try {
        // TODO: 実際のAPI呼び出しに置き換える
        await new Promise(resolve => setTimeout(resolve, 1000)); // 模擬的な読み込み時間
        
        const mockProfile: UserProfile = {
          emp_no: 'EMP001',
          name: '山田 太郎',
          email: 'yamada.taro@company.com',
          department: '開発部',
          position: 'シニアエンジニア',
          hire_date: '2020-04-01',
          phone: '090-1234-5678',
          emergency_contact: '090-8765-4321',
          skills_summary: 'JavaScript, React, Node.js, AWS'
        };
        
        setProfile(mockProfile);
        setEditedProfile(mockProfile);
      } catch (error) {
        console.error('プロフィール読み込みエラー:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadProfile();
  }, []);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    setEditedProfile(profile);
    setIsEditing(false);
  };

  const handleSave = async () => {
    if (!editedProfile) return;
    
    setIsSaving(true);
    try {
      // TODO: 実際のAPI呼び出しに置き換える
      await new Promise(resolve => setTimeout(resolve, 1000)); // 模擬的な保存時間
      
      setProfile(editedProfile);
      setIsEditing(false);
    } catch (error) {
      console.error('プロフィール保存エラー:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleInputChange = (field: keyof UserProfile, value: string) => {
    if (!editedProfile) return;
    
    setEditedProfile({
      ...editedProfile,
      [field]: value
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <DashboardHeader 
          onMenuClick={handleMenuClick}
          title="プロフィール"
        />
        <div className="flex pt-16">
          <Sidebar 
            isOpen={isSidebarOpen}
            onClose={handleSidebarClose}
          />
          <div className="flex-1 lg:ml-64 flex items-center justify-center">
            <Spinner size="lg" />
          </div>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen bg-gray-50">
        <DashboardHeader 
          onMenuClick={handleMenuClick}
          title="プロフィール"
        />
        <div className="flex pt-16">
          <Sidebar 
            isOpen={isSidebarOpen}
            onClose={handleSidebarClose}
          />
          <div className="flex-1 lg:ml-64 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-xl font-semibold text-gray-900 mb-2">プロフィールが見つかりません</h2>
              <p className="text-gray-600">プロフィール情報の読み込みに失敗しました。</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー - 最上部に固定 */}
      <DashboardHeader 
        onMenuClick={handleMenuClick}
        title="プロフィール"
      />

      {/* メインレイアウト - ヘッダーの下 */}
      <div className="flex pt-16">
        {/* サイドバー */}
        <Sidebar 
          isOpen={isSidebarOpen}
          onClose={handleSidebarClose}
        />

        {/* メインコンテンツエリア */}
        <div className="flex-1 lg:ml-64">
          <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
            {/* ページヘッダー */}
            <div className="mb-8">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">プロフィール</h1>
                  <p className="text-gray-600 mt-1">個人情報とスキル概要を管理します</p>
                </div>
                <div className="flex space-x-3">
                  {!isEditing ? (
                    <Button onClick={handleEdit} variant="primary">
                      編集
                    </Button>
                  ) : (
                    <>
                      <Button onClick={handleCancel} variant="secondary">
                        キャンセル
                      </Button>
                      <Button 
                        onClick={handleSave} 
                        variant="primary"
                        disabled={isSaving}
                      >
                        {isSaving ? '保存中...' : '保存'}
                      </Button>
                    </>
                  )}
                </div>
              </div>
            </div>

            {/* プロフィール情報 */}
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">基本情報</h2>
              </div>
              
              <div className="px-6 py-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* 社員番号 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      社員番号
                    </label>
                    <Input
                      value={profile.emp_no}
                      disabled={true}
                      className="bg-gray-50"
                    />
                  </div>

                  {/* 氏名 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      氏名 <span className="text-red-500">*</span>
                    </label>
                    <Input
                      value={isEditing ? editedProfile?.name || '' : profile.name}
                      onChange={(e) => handleInputChange('name', e.target.value)}
                      disabled={!isEditing}
                      className={!isEditing ? 'bg-gray-50' : ''}
                    />
                  </div>

                  {/* メールアドレス */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      メールアドレス <span className="text-red-500">*</span>
                    </label>
                    <Input
                      type="email"
                      value={isEditing ? editedProfile?.email || '' : profile.email}
                      onChange={(e) => handleInputChange('email', e.target.value)}
                      disabled={!isEditing}
                      className={!isEditing ? 'bg-gray-50' : ''}
                    />
                  </div>

                  {/* 部署 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      部署
                    </label>
                    <Input
                      value={isEditing ? editedProfile?.department || '' : profile.department}
                      onChange={(e) => handleInputChange('department', e.target.value)}
                      disabled={!isEditing}
                      className={!isEditing ? 'bg-gray-50' : ''}
                    />
                  </div>

                  {/* 役職 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      役職
                    </label>
                    <Input
                      value={isEditing ? editedProfile?.position || '' : profile.position}
                      onChange={(e) => handleInputChange('position', e.target.value)}
                      disabled={!isEditing}
                      className={!isEditing ? 'bg-gray-50' : ''}
                    />
                  </div>

                  {/* 入社日 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      入社日
                    </label>
                    <Input
                      type="date"
                      value={isEditing ? editedProfile?.hire_date || '' : profile.hire_date}
                      onChange={(e) => handleInputChange('hire_date', e.target.value)}
                      disabled={!isEditing}
                      className={!isEditing ? 'bg-gray-50' : ''}
                    />
                  </div>

                  {/* 電話番号 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      電話番号
                    </label>
                    <Input
                      value={isEditing ? editedProfile?.phone || '' : profile.phone || ''}
                      onChange={(e) => handleInputChange('phone', e.target.value)}
                      disabled={!isEditing}
                      className={!isEditing ? 'bg-gray-50' : ''}
                    />
                  </div>

                  {/* 緊急連絡先 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      緊急連絡先
                    </label>
                    <Input
                      value={isEditing ? editedProfile?.emergency_contact || '' : profile.emergency_contact || ''}
                      onChange={(e) => handleInputChange('emergency_contact', e.target.value)}
                      disabled={!isEditing}
                      className={!isEditing ? 'bg-gray-50' : ''}
                    />
                  </div>
                </div>

                {/* スキル概要 */}
                <div className="mt-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    スキル概要
                  </label>
                  <textarea
                    value={isEditing ? editedProfile?.skills_summary || '' : profile.skills_summary || ''}
                    onChange={(e) => handleInputChange('skills_summary', e.target.value)}
                    disabled={!isEditing}
                    rows={4}
                    className={`w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 ${
                      !isEditing ? 'bg-gray-50' : ''
                    }`}
                    placeholder="保有スキルや専門分野を入力してください"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
