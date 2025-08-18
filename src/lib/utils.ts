/**
 * 要求仕様ID: PLT.1-WEB.1
 * 対応設計書: docs/design/components/共通部品定義書.md
 * 実装内容: 共通ユーティリティ関数
 */

import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * 表示名からアイコン用のイニシャルを生成する
 * @param displayName - 表示名（例: "山田太郎", "佐藤花子"）
 * @returns イニシャル（例: "山田", "佐藤"）
 */
export function generateInitials(displayName: string): string {
  if (!displayName || displayName.trim() === '') {
    return '未';
  }

  const trimmedName = displayName.trim();
  
  // 日本語名の場合（スペース区切りまたは連続した文字）
  if (/[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]/.test(trimmedName)) {
    // スペースで区切られている場合
    if (trimmedName.includes(' ')) {
      const parts = trimmedName.split(' ').filter(part => part.length > 0);
      if (parts.length >= 2) {
        // 姓名の最初の文字を取得
        const firstPart = parts[0];
        const secondPart = parts[1];
        if (firstPart && secondPart) {
          return firstPart.charAt(0) + secondPart.charAt(0);
        }
      } else if (parts.length === 1) {
        // 1つの部分のみの場合、最初の2文字または1文字
        const part = parts[0];
        if (part) {
          return part.length >= 2 ? part.substring(0, 2) : part;
        }
      }
    } else {
      // スペースがない場合、最初の2文字を取得
      return trimmedName.length >= 2 ? trimmedName.substring(0, 2) : trimmedName;
    }
  }
  
  // 英語名の場合
  const parts = trimmedName.split(' ').filter(part => part.length > 0);
  if (parts.length >= 2) {
    // 姓名の最初の文字を大文字で取得
    const firstPart = parts[0];
    const secondPart = parts[1];
    if (firstPart && secondPart) {
      return (firstPart.charAt(0) + secondPart.charAt(0)).toUpperCase();
    }
  } else if (parts.length === 1) {
    // 1つの部分のみの場合、最初の2文字を大文字で取得
    const part = parts[0];
    if (part) {
      return part.length >= 2 
        ? part.substring(0, 2).toUpperCase() 
        : part.toUpperCase();
    }
  }
  
  return '未';
}

/**
 * 表示名からアイコンの背景色を生成する
 * @param displayName - 表示名
 * @returns Tailwind CSSクラス名
 */
export function generateAvatarColor(displayName: string): string {
  if (!displayName || displayName.trim() === '') {
    return 'bg-gray-500';
  }

  // 表示名のハッシュ値を計算
  let hash = 0;
  for (let i = 0; i < displayName.length; i++) {
    const char = displayName.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // 32bit整数に変換
  }

  // 色のパレット（視認性の良い色を選択）
  const colors = [
    'bg-blue-500',
    'bg-green-500', 
    'bg-purple-500',
    'bg-pink-500',
    'bg-indigo-500',
    'bg-yellow-500',
    'bg-red-500',
    'bg-teal-500',
    'bg-orange-500',
    'bg-cyan-500'
  ];

  // ハッシュ値から色を選択
  const colorIndex = Math.abs(hash) % colors.length;
  return colors[colorIndex] || 'bg-gray-500';
}

/**
 * ファイルサイズを人間が読みやすい形式に変換
 * @param bytes - バイト数
 * @returns フォーマットされた文字列（例: "1.2 MB"）
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * 日付を相対的な時間表現に変換
 * @param date - 日付
 * @returns 相対時間（例: "2時間前", "3日前"）
 */
export function formatRelativeTime(date: Date | string): string {
  const now = new Date();
  const targetDate = typeof date === 'string' ? new Date(date) : date;
  const diffInSeconds = Math.floor((now.getTime() - targetDate.getTime()) / 1000);

  if (diffInSeconds < 60) {
    return 'たった今';
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60);
    return `${minutes}分前`;
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600);
    return `${hours}時間前`;
  } else if (diffInSeconds < 2592000) {
    const days = Math.floor(diffInSeconds / 86400);
    return `${days}日前`;
  } else if (diffInSeconds < 31536000) {
    const months = Math.floor(diffInSeconds / 2592000);
    return `${months}ヶ月前`;
  } else {
    const years = Math.floor(diffInSeconds / 31536000);
    return `${years}年前`;
  }
}

/**
 * 数値を3桁区切りでフォーマット
 * @param num - 数値
 * @returns フォーマットされた文字列（例: "1,234,567"）
 */
export function formatNumber(num: number): string {
  return num.toLocaleString('ja-JP');
}

/**
 * パーセンテージを安全にフォーマット
 * @param value - 値
 * @param total - 全体
 * @param decimals - 小数点以下の桁数（デフォルト: 1）
 * @returns パーセンテージ文字列（例: "75.5%"）
 */
export function formatPercentage(value: number, total: number, decimals: number = 1): string {
  if (total === 0) return '0%';
  const percentage = (value / total) * 100;
  return `${percentage.toFixed(decimals)}%`;
}

/**
 * 文字列を指定した長さで切り詰める
 * @param str - 文字列
 * @param maxLength - 最大長
 * @param suffix - 切り詰め時の接尾辞（デフォルト: "..."）
 * @returns 切り詰められた文字列
 */
export function truncateString(str: string, maxLength: number, suffix: string = '...'): string {
  if (str.length <= maxLength) return str;
  return str.substring(0, maxLength - suffix.length) + suffix;
}

/**
 * スキルレベルを表示用文字列に変換
 * @param level - スキルレベル（1-4）
 * @returns 表示用文字列（"×", "△", "○", "◎"）
 */
export function formatSkillLevel(level: number): string {
  switch (level) {
    case 1: return '×';
    case 2: return '△';
    case 3: return '○';
    case 4: return '◎';
    default: return '×';
  }
}

/**
 * スキルレベルの色クラスを取得
 * @param level - スキルレベル（1-4）
 * @returns Tailwind CSSクラス名
 */
export function getSkillLevelColor(level: number): string {
  switch (level) {
    case 1: return 'text-red-500';
    case 2: return 'text-yellow-500';
    case 3: return 'text-blue-500';
    case 4: return 'text-green-500';
    default: return 'text-gray-500';
  }
}
