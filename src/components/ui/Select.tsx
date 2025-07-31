'use client';

/**
 * 統合 Select コンポーネント
 * --------------------------------------------------
 * 要求仕様ID: CAR.1-PLAN.1, PRO.1-BASE.1
 * 対応設計書:
 *   - docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 *   - docs/design/components/共通部品定義書.md
 *
 * 特徴:
 *   1. `Select`   – カスタム UI・キーボード操作・アクセシビリティ対応の高機能版。
 *   2. `NativeSelect` – ネイティブ <select> ベースの軽量シンプル版。
 * --------------------------------------------------
 */

import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Check } from 'lucide-react';

/** option 型 */
export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

/** 共通 props */
interface CommonProps {
  /** プレースホルダー */
  placeholder?: string;
  /** 選択中の値 */
  value?: string;
  /** 選択肢 */
  options: SelectOption[];
  /** onChange コールバック */
  onChange?: (value: string) => void;
  /** onBlur コールバック */
  onBlur?: () => void;
  /** 無効化 */
  disabled?: boolean;
  /** エラー文字列 or boolean */
  error?: string | boolean;
  /** 追加クラス名 */
  className?: string;
  /** ARIA */
  'aria-label'?: string;
  'aria-describedby'?: string;
}

// =============================================================================
// 1. 高機能カスタム Select
// =============================================================================

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
}: CommonProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [focusedIndex, setFocusedIndex] = useState(-1);
  const selectRef = useRef<HTMLDivElement>(null);
  const selectedOption = options.find((o) => o.value === value);

  // ----- error handling -----
  const hasError = !!error;
  const errorMessage = typeof error === 'string' ? error : undefined;

  // ----- outside click -----
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (selectRef.current && !selectRef.current.contains(e.target as Node)) {
        setIsOpen(false);
        setFocusedIndex(-1);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // ----- keyboard -----
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (disabled) return;

    switch (e.key) {
      case 'Enter':
      case ' ':
        e.preventDefault();
        if (isOpen && focusedIndex >= 0) {
          const opt = options[focusedIndex];
          if (!opt.disabled) {
            onChange?.(opt.value);
            setIsOpen(false);
            setFocusedIndex(-1);
          }
        } else {
          openDropdown();
        }
        break;
      case 'Escape':
        setIsOpen(false);
        setFocusedIndex(-1);
        break;
      case 'ArrowDown':
        e.preventDefault();
        if (!isOpen) openDropdown();
        else setFocusedIndex((i) => Math.min(i + 1, options.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        if (isOpen) setFocusedIndex((i) => Math.max(i - 1, 0));
        break;
      case 'Tab':
        setIsOpen(false);
        setFocusedIndex(-1);
        onBlur?.();
        break;
    }
  };

  const openDropdown = () => {
    setIsOpen(true);
    setFocusedIndex(value ? options.findIndex((o) => o.value === value) : 0);
  };

  const handleOptionClick = (opt: SelectOption) => {
    if (opt.disabled) return;
    onChange?.(opt.value);
    setIsOpen(false);
    setFocusedIndex(-1);
  };

  // ----- styles -----
  const base =
    'relative w-full bg-white border rounded-md shadow-sm px-3 py-2 text-left cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200';
  const state = hasError
    ? 'border-red-300 focus:ring-red-500'
    : disabled
    ? 'border-gray-200 bg-gray-50 cursor-not-allowed text-gray-500'
    : 'border-gray-300 hover:border-gray-400';

  return (
    <div className={`relative ${className}`} ref={selectRef}>
      <div
        className={`${base} ${state}`}
        role="combobox"
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        aria-label={ariaLabel}
        aria-describedby={ariaDescribedBy}
        tabIndex={disabled ? -1 : 0}
        onClick={() => !disabled && (isOpen ? setIsOpen(false) : openDropdown())}
        onKeyDown={handleKeyDown}
      >
        <div className="flex items-center justify-between">
          <span className={selectedOption ? 'text-gray-900' : 'text-gray-500'}>
            {selectedOption ? selectedOption.label : placeholder}
          </span>
          <ChevronDown
            className={`h-5 w-5 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          />
        </div>
      </div>

      {isOpen && (
        <ul
          role="listbox"
          aria-label={ariaLabel}
          className="absolute z-10 mt-1 w-full max-h-60 overflow-auto rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none divide-y divide-gray-100"
        >
          {options.map((opt, i) => {
            const active = i === focusedIndex;
            const selected = opt.value === value;
            return (
              <li
                key={opt.value}
                role="option"
                aria-selected={selected}
                className={`relative select-none py-2 pl-3 pr-9 transition-colors ${
                  opt.disabled
                    ? 'text-gray-400 cursor-not-allowed'
                    : active
                    ? 'bg-blue-50 text-blue-900'
                    : selected
                    ? 'bg-blue-100 text-blue-900'
                    : 'text-gray-900 hover:bg-gray-50 cursor-pointer'
                }`}
                onClick={() => handleOptionClick(opt)}
              >
                <span className={`${selected ? 'font-semibold' : 'font-normal'} block truncate`}>
                  {opt.label}
                </span>
                {selected && (
                  <span className="absolute inset-y-0 right-0 flex items-center pr-4">
                    <Check className="h-5 w-5 text-blue-600" />
                  </span>
                )}
              </li>
            );
          })}
        </ul>
      )}

      {errorMessage && (
        <p className="mt-1 text-sm text-red-600" role="alert">
          {errorMessage}
        </p>
      )}
    </div>
  );
}

// =============================================================================
// 2. ネイティブ Select（軽量版）
// =============================================================================

export type NativeSelectProps = CommonProps;

export function NativeSelect({
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
}: NativeSelectProps) {
  const hasError = !!error;
  const errorMessage = typeof error === 'string' ? error : undefined;

  const base =
    'w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200 disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed';
  const state = hasError ? 'border-red-300 focus:ring-red-500' : 'border-gray-300';

  return (
    <div className={className}>
      <select
        value={value ?? ''}
        onChange={(e) => onChange?.(e.target.value)}
        onBlur={onBlur}
        disabled={disabled}
        aria-label={ariaLabel}
        aria-describedby={ariaDescribedBy}
        className={`${base} ${state}`}
      >
        <option value="" disabled>
          {placeholder}
        </option>
        {options.map((opt) => (
          <option key={opt.value} value={opt.value} disabled={opt.disabled}>
            {opt.label}
          </option>
        ))}
      </select>
      {errorMessage && (
        <p className="mt-1 text-sm text-red-600" role="alert">
          {errorMessage}
        </p>
      )}
    </div>
  );
}

// ----------------------------------------------------------------------------
// デフォルトエクスポート (互換性維持のため軽量版をエクスポート)
// ----------------------------------------------------------------------------
export default NativeSelect;
