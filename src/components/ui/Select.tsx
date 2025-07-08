/**
 * 要求仕様ID: PLT.1-WEB.1
 * 対応設計書: docs/design/components/shared/共通部品定義書.md
 * 実装内容: Selectコンポーネント（ドロップダウン選択）
 */

import React from 'react';

interface SelectOption {
  value: string;
  label: string;
}

interface SelectProps {
  value?: string;
  onChange?: (value: string) => void;
  options: SelectOption[];
  placeholder?: string;
  disabled?: boolean;
  className?: string;
  required?: boolean;
}

export const Select: React.FC<SelectProps> = ({
  value = '',
  onChange,
  options = [],
  placeholder = '選択してください',
  disabled = false,
  className = '',
  required = false
}) => {
  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    if (onChange) {
      onChange(event.target.value);
    }
  };

  const baseClasses = `
    w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
    focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
    disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed
    text-sm
  `.trim().replace(/\s+/g, ' ');

  return (
    <select
      value={value}
      onChange={handleChange}
      disabled={disabled}
      required={required}
      className={`${baseClasses} ${className}`}
    >
      {placeholder && (
        <option value="" disabled>
          {placeholder}
        </option>
      )}
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
};
