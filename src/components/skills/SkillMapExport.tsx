/**
 * 要求仕様ID: SKL.1-HIER.1
 * 対応設計書: docs/design/screens/specs/画面設計書_SCR-SKILLMAP_スキルマップ画面.md
 * 実装内容: スキルマップエクスポート機能
 */
'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';

interface SkillMapExportProps {
  onExport: (format: 'excel' | 'csv' | 'pdf') => Promise<void>;
}

export function SkillMapExport({ onExport }: SkillMapExportProps) {
  const [isExporting, setIsExporting] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);

  const handleExport = async (format: 'excel' | 'csv' | 'pdf') => {
    try {
      setIsExporting(true);
      setShowDropdown(false);
      await onExport(format);
    } catch (error) {
      console.error('エクスポートエラー:', error);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="relative">
      <Button
        onClick={() => setShowDropdown(!showDropdown)}
        variant="primary"
        size="sm"
        disabled={isExporting}
      >
        {isExporting ? 'エクスポート中...' : 'エクスポート'}
        <svg
          className="ml-2 h-4 w-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </Button>

      {showDropdown && (
        <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border border-gray-200">
          <div className="py-1">
            <button
              onClick={() => handleExport('excel')}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              <div className="flex items-center">
                <svg className="mr-3 h-4 w-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" />
                </svg>
                Excel形式 (.xlsx)
              </div>
            </button>
            <button
              onClick={() => handleExport('csv')}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              <div className="flex items-center">
                <svg className="mr-3 h-4 w-4 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
                CSV形式 (.csv)
              </div>
            </button>
            <button
              onClick={() => handleExport('pdf')}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              <div className="flex items-center">
                <svg className="mr-3 h-4 w-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
                </svg>
                PDF形式 (.pdf)
              </div>
            </button>
          </div>
        </div>
      )}

      {/* オーバーレイ（ドロップダウンを閉じるため） */}
      {showDropdown && (
        <div
          className="fixed inset-0 z-0"
          onClick={() => setShowDropdown(false)}
        />
      )}
    </div>
  );
}
