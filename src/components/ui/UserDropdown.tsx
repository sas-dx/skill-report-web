/**
 * 要求仕様ID: PLT.1-WEB.1
 * 対応設計書: docs/design/components/共通部品定義書.md
 * ユーザードロップダウンコンポーネント - プロフィール表示名対応
 */
'use client';

import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { ProfileData } from '../../hooks/useProfile';

interface User {
  id: string;
  name: string;
  email: string;
  department: string;
  role: string;
  avatar?: string;
}

interface UserDropdownProps {
  user?: User;
  profile?: ProfileData | null;
  loading?: boolean;
  error?: string | null;
  onLogout?: () => void;
}

export const UserDropdown: React.FC<UserDropdownProps> = ({
  user,
  profile,
  loading,
  error,
  onLogout,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // プロフィール情報からユーザー情報を構築（プロフィールデータを優先）
  const displayUser = profile ? {
    id: profile.id,
    name: profile.personalInfo?.displayName || 'ユーザー',
    email: profile.email || '',
    department: profile.organizationInfo?.departmentName || '未設定',
    role: profile.organizationInfo?.positionName || '未設定',
    avatar: undefined
  } : user || {
    id: 'unknown',
    name: 'ユーザー',
    email: '',
    department: '未設定',
    role: '未設定',
    avatar: undefined
  };

  // 外部クリックでドロップダウンを閉じる
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleLogout = () => {
    setIsOpen(false);
    onLogout?.();
  };

  // 表示名の処理 - 未設定の場合はアイコン表示用の文字を生成
  const getDisplayName = (name: string) => {
    if (!name || name === 'ユーザー' || name.trim() === '') {
      return '未設定';
    }
    return name;
  };

  // アイコン用の文字を生成（名前の最初の文字、または適切なアイコン文字）
  const getAvatarText = (name: string) => {
    if (!name || name === 'ユーザー' || name.trim() === '' || name === '未設定') {
      return '👤'; // ユーザーアイコン絵文字
    }
    
    // 「社員」で始まる場合は社員番号の最初の文字を使用
    if (name.startsWith('社員')) {
      const empCode = name.replace('社員', '');
      if (empCode) {
        return empCode.charAt(0).toUpperCase();
      }
      return '社';
    }
    
    // 通常の名前の場合は最初の文字を使用
    const firstChar = name.charAt(0);
    return firstChar.toUpperCase();
  };

  // アイコンの背景色を決定（未設定の場合はグレー）
  const getAvatarBgColor = (name: string) => {
    if (!name || name === 'ユーザー' || name.trim() === '') {
      return 'bg-gray-500';
    }
    return 'bg-blue-600';
  };

  const menuItems = [
    {
      id: 'profile',
      label: 'プロフィール',
      href: '/profile',
      icon: (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      ),
    },
    {
      id: 'settings',
      label: '設定',
      href: '/settings',
      icon: (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      ),
    },
    {
      id: 'help',
      label: 'ヘルプ',
      href: '/help',
      icon: (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
    },
  ];

  // ローディング中の表示
  if (loading) {
    return (
      <div className="flex items-center space-x-3 p-2">
        <div className="w-8 h-8 bg-gray-300 rounded-full animate-pulse"></div>
        <div className="hidden md:block">
          <div className="w-20 h-4 bg-gray-300 rounded animate-pulse mb-1"></div>
          <div className="w-16 h-3 bg-gray-300 rounded animate-pulse"></div>
        </div>
      </div>
    );
  }

  // エラー時の表示
  if (error) {
    return (
      <div className="flex items-center space-x-3 p-2">
        <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
          <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        </div>
        <div className="hidden md:block">
          <div className="text-sm font-medium text-red-600">エラー</div>
          <div className="text-xs text-red-500">プロフィール取得失敗</div>
        </div>
      </div>
    );
  }

  return (
    <div className="relative" ref={dropdownRef}>
      {/* ユーザーアバターボタン */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-3 p-2 text-sm rounded-full hover:bg-gray-100 transition-colors duration-150"
        aria-label="ユーザーメニューを開く"
      >
        {/* アバターアイコン */}
        <div className={`w-8 h-8 ${getAvatarBgColor(displayUser.name)} rounded-full flex items-center justify-center text-white font-medium text-sm`}>
          {displayUser.avatar ? (
            <img
              src={displayUser.avatar}
              alt={displayUser.name}
              className="w-8 h-8 rounded-full object-cover"
            />
          ) : (
            getAvatarText(displayUser.name)
          )}
        </div>
        
        {/* ユーザー名（デスクトップのみ表示） */}
        <div className="hidden md:block text-left">
          <div className="text-sm font-medium text-gray-900">{getDisplayName(displayUser.name)}</div>
          <div className="text-xs text-gray-500">{displayUser.department}</div>
        </div>

        {/* ドロップダウン矢印 */}
        <svg
          className={`w-4 h-4 text-gray-400 transition-transform duration-150 ${
            isOpen ? 'rotate-180' : ''
          }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* ドロップダウンメニュー */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
          {/* ユーザー情報ヘッダー */}
          <div className="px-4 py-3 border-b border-gray-200">
            <div className="flex items-center space-x-3">
              <div className={`w-10 h-10 ${getAvatarBgColor(displayUser.name)} rounded-full flex items-center justify-center text-white font-medium`}>
                {displayUser.avatar ? (
                  <img
                    src={displayUser.avatar}
                    alt={displayUser.name}
                    className="w-10 h-10 rounded-full object-cover"
                  />
                ) : (
                  getAvatarText(displayUser.name)
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-gray-900 truncate">
                  {getDisplayName(displayUser.name)}
                </div>
                <div className="text-xs text-gray-500 truncate">
                  {displayUser.email || '未設定'}
                </div>
                <div className="text-xs text-gray-400">
                  {displayUser.department} • {displayUser.role}
                </div>
              </div>
            </div>
          </div>

          {/* メニュー項目 */}
          <div className="py-1">
            {menuItems.map((item) => (
              <Link
                key={item.id}
                href={item.href}
                className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-150"
                onClick={() => setIsOpen(false)}
              >
                <span className="mr-3 text-gray-400">{item.icon}</span>
                {item.label}
              </Link>
            ))}
          </div>

          {/* 区切り線 */}
          <div className="border-t border-gray-200"></div>

          {/* ログアウト */}
          <div className="py-1">
            <button
              onClick={handleLogout}
              className="flex items-center w-full px-4 py-2 text-sm text-red-700 hover:bg-red-50 transition-colors duration-150"
            >
              <svg className="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              ログアウト
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
