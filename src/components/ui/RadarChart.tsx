// CAR.1-PLAN.1: レーダーチャートコンポーネント
'use client';

import React from 'react';

interface SkillData {
  label: string;
  current: number;
  target: number;
}

interface RadarChartProps {
  data: SkillData[];
  size?: number;
}

export const RadarChart: React.FC<RadarChartProps> = ({ 
  data, 
  size = 300 
}) => {
  const center = size / 2;
  const radius = (size / 2) - 40;
  const levels = 5;

  // 角度計算（上から時計回り）
  const getAngle = (index: number) => {
    return (index * 2 * Math.PI) / data.length - Math.PI / 2;
  };

  // 座標計算
  const getCoordinates = (angle: number, distance: number) => {
    return {
      x: center + Math.cos(angle) * distance,
      y: center + Math.sin(angle) * distance
    };
  };

  // レベル線の生成
  const levelLines = Array.from({ length: levels }, (_, i) => {
    const levelRadius = (radius / levels) * (i + 1);
    const points = data.map((_, index) => {
      const angle = getAngle(index);
      const coords = getCoordinates(angle, levelRadius);
      return `${coords.x},${coords.y}`;
    }).join(' ');

    return (
      <polygon
        key={i}
        points={points}
        fill="none"
        stroke="#e5e7eb"
        strokeWidth="1"
      />
    );
  });

  // 軸線の生成
  const axisLines = data.map((_, index) => {
    const angle = getAngle(index);
    const coords = getCoordinates(angle, radius);
    return (
      <line
        key={index}
        x1={center}
        y1={center}
        x2={coords.x}
        y2={coords.y}
        stroke="#e5e7eb"
        strokeWidth="1"
      />
    );
  });

  // 現在スキルのポリゴン
  const currentPoints = data.map((item, index) => {
    const angle = getAngle(index);
    const distance = (radius / 4) * item.current;
    const coords = getCoordinates(angle, distance);
    return `${coords.x},${coords.y}`;
  }).join(' ');

  // 目標スキルのポリゴン
  const targetPoints = data.map((item, index) => {
    const angle = getAngle(index);
    const distance = (radius / 4) * item.target;
    const coords = getCoordinates(angle, distance);
    return `${coords.x},${coords.y}`;
  }).join(' ');

  // ラベルの配置
  const labels = data.map((item, index) => {
    const angle = getAngle(index);
    const labelDistance = radius + 25;
    const coords = getCoordinates(angle, labelDistance);
    
    return (
      <text
        key={index}
        x={coords.x}
        y={coords.y}
        textAnchor="middle"
        dominantBaseline="middle"
        className="text-xs font-medium text-gray-700"
      >
        {item.label}
      </text>
    );
  });

  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size} className="overflow-visible">
        {/* レベル線 */}
        {levelLines}
        
        {/* 軸線 */}
        {axisLines}
        
        {/* 目標スキル（背景） */}
        <polygon
          points={targetPoints}
          fill="rgba(59, 130, 246, 0.1)"
          stroke="#3b82f6"
          strokeWidth="2"
          strokeDasharray="5,5"
        />
        
        {/* 現在スキル */}
        <polygon
          points={currentPoints}
          fill="rgba(16, 185, 129, 0.2)"
          stroke="#10b981"
          strokeWidth="2"
        />
        
        {/* データポイント - 現在スキル */}
        {data.map((item, index) => {
          const angle = getAngle(index);
          const distance = (radius / 4) * item.current;
          const coords = getCoordinates(angle, distance);
          return (
            <circle
              key={`current-${index}`}
              cx={coords.x}
              cy={coords.y}
              r="4"
              fill="#10b981"
              stroke="white"
              strokeWidth="2"
            />
          );
        })}
        
        {/* データポイント - 目標スキル */}
        {data.map((item, index) => {
          const angle = getAngle(index);
          const distance = (radius / 4) * item.target;
          const coords = getCoordinates(angle, distance);
          return (
            <circle
              key={`target-${index}`}
              cx={coords.x}
              cy={coords.y}
              r="4"
              fill="#3b82f6"
              stroke="white"
              strokeWidth="2"
            />
          );
        })}
        
        {/* ラベル */}
        {labels}
      </svg>
      
      {/* 凡例 */}
      <div className="flex items-center gap-6 mt-4">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-green-500 rounded-full"></div>
          <span className="text-sm text-gray-600">現在スキル</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 border-2 border-blue-500 border-dashed rounded-full bg-blue-100"></div>
          <span className="text-sm text-gray-600">目標スキル</span>
        </div>
      </div>
    </div>
  );
};
