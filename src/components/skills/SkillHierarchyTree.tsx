/**
 * 要求仕様ID: SKL.1-HIER.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_SKL_Skill_スキル管理画面.md
 * 実装内容: スキル階層ツリーコンポーネント
 */

'use client';

import React, { useState } from 'react';
import { ChevronRightIcon, ChevronDownIcon } from '@/components/ui/Icons';
import { SkillHierarchy, UserSkill, SKILL_LEVELS } from '@/types/skills';

interface SkillHierarchyTreeProps {
  hierarchy: SkillHierarchy[];
  userSkills: UserSkill[];
  selectedSkillId?: string;
  onSkillSelect: (skill: SkillHierarchy) => void;
  searchTerm?: string;
}

interface TreeNodeProps {
  node: SkillHierarchy;
  userSkills: UserSkill[];
  selectedSkillId?: string | undefined;
  onSkillSelect: (skill: SkillHierarchy) => void;
  searchTerm?: string | undefined;
  level: number;
}

const TreeNode: React.FC<TreeNodeProps> = ({
  node,
  userSkills,
  selectedSkillId,
  onSkillSelect,
  searchTerm,
  level
}) => {
  const [isExpanded, setIsExpanded] = useState(level < 2); // 最初の2階層は展開

  const hasChildren = node.children && node.children.length > 0;
  const isLeafNode = level === 2; // スキル項目レベル
  const isSelected = selectedSkillId === node.id;

  // ユーザーのスキルレベルを取得
  const userSkill = userSkills.find(skill => skill.skillId === node.id);
  const skillLevel = userSkill?.level;

  // 検索ハイライト
  const highlightText = (text: string) => {
    if (!searchTerm) return text;
    
    const regex = new RegExp(`(${searchTerm})`, 'gi');
    const parts = text.split(regex);
    
    return parts.map((part, index) => 
      regex.test(part) ? (
        <mark key={index} className="bg-yellow-200 px-1 rounded">
          {part}
        </mark>
      ) : part
    );
  };

  const handleToggle = () => {
    if (hasChildren) {
      setIsExpanded(!isExpanded);
    }
  };

  const handleSelect = () => {
    if (isLeafNode) {
      onSkillSelect(node);
    } else {
      handleToggle();
    }
  };

  const getIndentClass = (level: number) => {
    const indents = ['pl-0', 'pl-4', 'pl-8'];
    return indents[level] || 'pl-8';
  };

  const getNodeIcon = () => {
    if (!hasChildren) return null;
    
    return isExpanded ? (
      <ChevronDownIcon className="h-4 w-4 text-gray-500" />
    ) : (
      <ChevronRightIcon className="h-4 w-4 text-gray-500" />
    );
  };

  const getSkillLevelBadge = () => {
    if (!isLeafNode || !skillLevel) return null;
    
    const levelInfo = SKILL_LEVELS[skillLevel];
    return (
      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ml-2 ${levelInfo.color}`}>
        {levelInfo.symbol}
      </span>
    );
  };

  return (
    <div>
      <div
        className={`
          flex items-center py-2 px-2 cursor-pointer rounded-md transition-colors
          ${getIndentClass(level)}
          ${isSelected ? 'bg-blue-100 text-blue-900' : 'hover:bg-gray-50'}
          ${isLeafNode ? 'hover:bg-blue-50' : ''}
        `}
        onClick={handleSelect}
        role="treeitem"
        aria-expanded={hasChildren ? isExpanded : undefined}
        aria-selected={isSelected}
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            handleSelect();
          }
        }}
      >
        <div className="flex items-center min-w-0 flex-1">
          {/* 展開/折りたたみアイコン */}
          <div className="flex-shrink-0 w-4 h-4 mr-2">
            {getNodeIcon()}
          </div>
          
          {/* ノード名 */}
          <span className={`
            text-sm truncate
            ${level === 0 ? 'font-semibold text-gray-900' : ''}
            ${level === 1 ? 'font-medium text-gray-800' : ''}
            ${level === 2 ? 'text-gray-700' : ''}
          `}>
            {highlightText(node.name)}
          </span>
          
          {/* スキルレベルバッジ */}
          {getSkillLevelBadge()}
        </div>
      </div>

      {/* 子ノード */}
      {hasChildren && isExpanded && (
        <div role="group">
          {node.children!.map((child) => (
            <TreeNode
              key={child.id}
              node={child}
              userSkills={userSkills}
              selectedSkillId={selectedSkillId}
              onSkillSelect={onSkillSelect}
              searchTerm={searchTerm}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export const SkillHierarchyTree: React.FC<SkillHierarchyTreeProps> = ({
  hierarchy,
  userSkills,
  selectedSkillId,
  onSkillSelect,
  searchTerm
}) => {
  return (
    <div 
      className="bg-white border border-gray-200 rounded-lg p-4 h-full overflow-y-auto"
      role="tree"
      aria-label="スキル階層ツリー"
    >
      <div className="mb-3">
        <h3 className="text-sm font-medium text-gray-900">スキル階層</h3>
        <p className="text-xs text-gray-500 mt-1">
          スキル項目をクリックして詳細を表示
        </p>
      </div>
      
      <div className="space-y-1">
        {hierarchy.map((node) => (
          <TreeNode
            key={node.id}
            node={node}
            userSkills={userSkills}
            selectedSkillId={selectedSkillId}
            onSkillSelect={onSkillSelect}
            searchTerm={searchTerm}
            level={0}
          />
        ))}
      </div>
      
      {hierarchy.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <p className="text-sm">スキル階層データがありません</p>
        </div>
      )}
    </div>
  );
};
