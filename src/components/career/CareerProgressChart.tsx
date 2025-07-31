/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリア進捗チャートコンポーネント
 */

'use client';

import React from 'react';
import { CareerGoalData } from '@/types/career';

interface CareerProgressChartProps {
  careerGoal: CareerGoalData;
  year: number;
}

/**
 * キャリア進捗チャートコンポーネント
 */
export function CareerProgressChart({ careerGoal, year }: CareerProgressChartProps) {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          {year}年度 キャリア進捗状況
        </h3>
        
        {/* 進捗バー */}
        <div className="max-w-md mx-auto">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>進捗率</span>
            <span>{careerGoal.progress_percentage}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div 
              className="bg-blue-600 h-3 rounded-full transition-all duration-300"
              style={{ width: `${careerGoal.progress_percentage}%` }}
            ></div>
          </div>
        </div>

        {/* 目標情報 */}
        <div className="mt-6 bg-gray-50 rounded-lg p-4">
          <h4 className="font-medium text-gray-900 mb-2">目標詳細</h4>
          <div className="text-left space-y-2">
            <p className="text-sm text-gray-600">
              <span className="font-medium">目標職位:</span> {careerGoal.target_position}
            </p>
            <p className="text-sm text-gray-600">
              <span className="font-medium">現在レベル:</span> {careerGoal.current_level}
            </p>
            <p className="text-sm text-gray-600">
              <span className="font-medium">目標レベル:</span> {careerGoal.target_level}
            </p>
            <p className="text-sm text-gray-600">
              <span className="font-medium">目標期日:</span> {careerGoal.target_date ? new Date(careerGoal.target_date).toLocaleDateString('ja-JP') : '未設定'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
