/**
 * 要求仕様ID: PRO.1-BASE.1
 * 対応設計書: docs/design/components/共通部品定義書.md
 * 実装内容: Selectコンポーネント（部署・役職選択用）
 */
'use client';

import React from 'react';

interface SelectOption {
  value: string;
  label: string;
}

interface SelectProps {
  value?: string;
  onChange?: (value: string) => void;
  options?: SelectOption[];
  placeholder?: string;
  disabled?: boolean;
  className?: string;
  error?: boolean;
  children?: React.ReactNode;
}

export function Select({
  value = '',
  onChange,
  options,
  placeholder = '選択してください',
  disabled = false,
  className = '',
  error = false,
  children
}: SelectProps) {
  const baseClasses = `
    w-full px-3 py-2 border rounded-md shadow-sm
    focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
    disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed
    transition-colors duration-200
  `;

  const errorClasses = error
    ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
    : 'border-gray-300';

  const combinedClasses = `${baseClasses} ${errorClasses} ${className}`.trim();

  return (
    <select
      value={value}
      onChange={(e) => onChange?.(e.target.value)}
      disabled={disabled}
      className={combinedClasses}
    >
      {!children && (
        <option value="" disabled>
          {placeholder}
        </option>
      )}
      {children || options?.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
}
