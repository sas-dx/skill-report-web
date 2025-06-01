// PLT.1-WEB.1: 共通ユーティリティ関数
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Tailwind CSSクラスを結合・マージするユーティリティ関数
 * @param inputs - クラス名の配列
 * @returns マージされたクラス名
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * 文字列を安全にHTMLエスケープする
 * @param str - エスケープする文字列
 * @returns エスケープされた文字列
 */
export function escapeHtml(str: string): string {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

/**
 * 日付を日本語形式でフォーマットする
 * @param date - フォーマットする日付
 * @returns フォーマットされた日付文字列
 */
export function formatDateJP(date: Date): string {
  return new Intl.DateTimeFormat('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(date);
}

/**
 * 日時を日本語形式でフォーマットする
 * @param date - フォーマットする日時
 * @returns フォーマットされた日時文字列
 */
export function formatDateTimeJP(date: Date): string {
  return new Intl.DateTimeFormat('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
}

/**
 * 文字列が空かどうかをチェックする
 * @param str - チェックする文字列
 * @returns 空の場合true
 */
export function isEmpty(str: string | null | undefined): boolean {
  return !str || str.trim().length === 0;
}

/**
 * 数値を3桁区切りでフォーマットする
 * @param num - フォーマットする数値
 * @returns フォーマットされた数値文字列
 */
export function formatNumber(num: number): string {
  return new Intl.NumberFormat('ja-JP').format(num);
}
