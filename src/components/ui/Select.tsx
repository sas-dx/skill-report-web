/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: セレクトボックスUIコンポーネント
 */

'use client';

import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Check } from 'lucide-react';

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

interface SelectProps {
  options: SelectOption[];
  value?: string;
  placeholder?: string;
  disabled?: boolean;
  error?: string;
  className?: string;
  onChange?: (value: string) => void;
  onBlur?: () => void;
  'aria-label'?: string;
  'aria-describedby'?: string;
}

/**
 * セレクトボックスコンポーネント
 * アクセシビリティ対応済み、キーボード操作対応
 */
export function Select({
  options,
  value,
  placeholder = '選択してください',
  disabled = false,
  error,
  className = '',
  onChange,
  onBlur,
  'aria-label': ariaLabel,
  'aria-describedby': ariaDescribedBy,
}: SelectProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [focusedIndex, setFocusedIndex] = useState(-1);
  const selectRef = useRef<HTMLDivElement>(null);
  const listRef = useRef<HTMLUListElement>(null);

  // 選択されたオプションを取得
  const selectedOption = options.find(option => option.value === value);

  // 外部クリックでドロップダウンを閉じる
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (selectRef.current && !selectRef.current.contains(event.target as Node)) {
        setIsOpen(false);
        setFocusedIndex(-1);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // キーボード操作
  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (disabled) return;

    switch (event.key) {
      case 'Enter':
      case ' ':
        event.preventDefault();
        if (isOpen && focusedIndex >= 0) {
          const option = options[focusedIndex];
          if (option && !option.disabled) {
            onChange?.(option.value);
            setIsOpen(false);
            setFocusedIndex(-1);
          }
        } else {
          setIsOpen(true);
        }
        break;

      case 'Escape':
        setIsOpen(false);
        setFocusedIndex(-1);
        break;

      case 'ArrowDown':
        event.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
        } else {
          const nextIndex = Math.min(focusedIndex + 1, options.length - 1);
          setFocusedIndex(nextIndex);
        }
        break;

      case 'ArrowUp':
        event.preventDefault();
        if (isOpen) {
          const prevIndex = Math.max(focusedIndex - 1, 0);
          setFocusedIndex(prevIndex);
        }
        break;

      case 'Tab':
        setIsOpen(false);
        setFocusedIndex(-1);
        onBlur?.();
        break;
    }
  };

  // オプション選択
  const handleOptionClick = (option: SelectOption) => {
    if (option.disabled) return;
    
    onChange?.(option.value);
    setIsOpen(false);
    setFocusedIndex(-1);
  };

  // ドロップダウンの開閉
  const toggleDropdown = () => {
    if (disabled) return;
    setIsOpen(!isOpen);
    if (!isOpen) {
      setFocusedIndex(value ? options.findIndex(opt => opt.value === value) : 0);
    }
  };

  const baseClasses = `
    relative w-full bg-white border rounded-md shadow-sm px-3 py-2 text-left cursor-pointer
    focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
    transition-colors duration-200
  `;

  const stateClasses = error
    ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
    : disabled
    ? 'border-gray-200 bg-gray-50 cursor-not-allowed text-gray-500'
    : 'border-gray-300 hover:border-gray-400';

  return (
    <div className={`relative ${className}`} ref={selectRef}>
      {/* セレクトボタン */}
      <div
        className={`${baseClasses} ${stateClasses}`}
        onClick={toggleDropdown}
        onKeyDown={handleKeyDown}
        tabIndex={disabled ? -1 : 0}
        role="combobox"
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        aria-label={ariaLabel}
        aria-describedby={ariaDescribedBy}
      >
        <div className="flex items-center justify-between">
          <span className={selectedOption ? 'text-gray-900' : 'text-gray-500'}>
            {selectedOption ? selectedOption.label : placeholder}
          </span>
          <ChevronDown
            className={`h-5 w-5 text-gray-400 transition-transform duration-200 ${
              isOpen ? 'transform rotate-180' : ''
            }`}
          />
        </div>
      </div>

      {/* ドロップダウンリスト */}
      {isOpen && (
        <div className="absolute z-10 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none">
          <ul
            ref={listRef}
            role="listbox"
            aria-label={ariaLabel}
            className="divide-y divide-gray-100"
          >
            {options.map((option, index) => (
              <li
                key={option.value}
                role="option"
                aria-selected={option.value === value}
                className={`
                  relative cursor-pointer select-none py-2 pl-3 pr-9 transition-colors duration-150
                  ${option.disabled
                    ? 'text-gray-400 cursor-not-allowed'
                    : index === focusedIndex
                    ? 'bg-blue-50 text-blue-900'
                    : option.value === value
                    ? 'bg-blue-100 text-blue-900'
                    : 'text-gray-900 hover:bg-gray-50'
                  }
                `}
                onClick={() => handleOptionClick(option)}
              >
                <span
                  className={`block truncate ${
                    option.value === value ? 'font-semibold' : 'font-normal'
                  }`}
                >
                  {option.label}
                </span>

                {/* 選択チェックマーク */}
                {option.value === value && (
                  <span className="absolute inset-y-0 right-0 flex items-center pr-4">
                    <Check className="h-5 w-5 text-blue-600" />
                  </span>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* エラーメッセージ */}
      {error && (
        <p className="mt-1 text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}

/**
 * シンプルなセレクトコンポーネント（ネイティブselect要素ベース）
 */
interface SimpleSelectProps {
  options: SelectOption[];
  value?: string;
  placeholder?: string;
  disabled?: boolean;
  error?: string;
  className?: string;
  onChange?: (value: string) => void;
  onBlur?: () => void;
  'aria-label'?: string;
  'aria-describedby'?: string;
}

export function SimpleSelect({
  options,
  value,
  placeholder,
  disabled = false,
  error,
  className = '',
  onChange,
  onBlur,
  'aria-label': ariaLabel,
  'aria-describedby': ariaDescribedBy,
}: SimpleSelectProps) {
  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    onChange?.(event.target.value);
  };

  const baseClasses = `
    w-full px-3 py-2 border rounded-md shadow-sm
    focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
    transition-colors duration-200
  `;

  const stateClasses = error
    ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
    : disabled
    ? 'border-gray-200 bg-gray-50 cursor-not-allowed text-gray-500'
    : 'border-gray-300 hover:border-gray-400';

  return (
    <div className={className}>
      <select
        value={value || ''}
        onChange={handleChange}
        onBlur={onBlur}
        disabled={disabled}
        className={`${baseClasses} ${stateClasses}`}
        aria-label={ariaLabel}
        aria-describedby={ariaDescribedBy}
      >
        {placeholder && (
          <option value="" disabled>
            {placeholder}
          </option>
        )}
        {options.map((option) => (
          <option
            key={option.value}
            value={option.value}
            disabled={option.disabled}
          >
            {option.label}
          </option>
        ))}
      </select>

      {error && (
        <p className="mt-1 text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
