"""
AI駆動コード生成機能

要求仕様ID: PLT.1-WEB.1, SKL.1-HIER.1
設計書: docs/design/database/08-database-design-guidelines.md
実装内容: 自然言語からYAML定義・DDL・TypeScript型定義の自動生成
"""

import json
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from ..core.logger import get_logger
from ..core.exceptions import AIGenerationError
from ..utils.validation import validate_yaml_structure

logger = get_logger(__name__)

@dataclass
class GenerationRequest:
    """生成リクエスト"""
    description: str
    table_name: Optional[str] = None
    target_format: str = "yaml"  # yaml, ddl, typescript, prisma
    context: Optional[Dict[str, Any]] = None

@dataclass
class GenerationResult:
    """生成結果"""
    success: bool
    content: str
    format: str
    metadata: Dict[str, Any]
    suggestions: List[str]

class AICodeGenerator:
    """AI駆動コード生成
    
    自然言語の説明からデータベース定義を自動生成する機能を提供
    """
    
    def __init__(self):
        """初期化"""
        self.templates = self._load_templates()
        self.patterns = self._load_patterns()
        
    def generate_from_description(self, request: GenerationRequest) -> GenerationResult:
        """説明文からコード生成
        
        Args:
            request: 生成リクエスト
            
        Returns:
            GenerationResult: 生成結果
        """
        try:
            logger.info(f"AI生成開始: {request.description}")
            
            # 自然言語解析
            parsed_info = self._parse_natural_language(request.description)
            
            # コンテキスト情報の統合
            if request.context:
                parsed_info.update(request.context)
            
            # フォーマット別生成
            if request.target_format == "yaml":
                content = self._generate_yaml(parsed_info, request.table_name)
            elif request.target_format == "ddl":
                content = self._generate_ddl(parsed_info, request.table_name)
            elif request.target_format == "typescript":
                content = self._generate_typescript(parsed_info, request.table_name)
            elif request.target_format == "prisma":
                content = self._generate_prisma(parsed_info, request.table_name)
            else:
                raise AIGenerationError(f"未対応フォーマット: {request.target_format}")
            
            # 品質チェック
            suggestions = self._analyze_quality(content, request.target_format)
            
            return GenerationResult(
                success=True,
                content=content,
                format=request.target_format,
                metadata=parsed_info,
                suggestions=suggestions
            )
            
        except Exception as e:
            logger.error(f"AI生成エラー: {str(e)}")
            return GenerationResult(
                success=False,
                content="",
                format=request.target_format,
                metadata={},
                suggestions=[f"生成エラー: {str(e)}"]
            )
    
    def _parse_natural_language(self, description: str) -> Dict[str, Any]:
        """自然言語解析
        
        Args:
            description: 説明文
            
        Returns:
            Dict[str, Any]: 解析結果
        """
        info = {
            'table_name': '',
            'columns': [],
            'indexes': [],
            'foreign_keys': [],
            'business_rules': [],
            'notes': []
        }
        
        # テーブル名抽出
        table_patterns = [
            r'(\w+)テーブル',
            r'(\w+)の情報',
            r'(\w+)マスタ',
            r'(\w+)管理'
        ]
        
        for pattern in table_patterns:
            match = re.search(pattern, description)
            if match:
                info['table_name'] = match.group(1)
                break
        
        # カラム情報抽出
        column_patterns = [
            r'(\w+)(?:カラム|フィールド|項目)',
            r'(\w+)(?:を|の)(?:格納|保存|管理)',
            r'(\w+)(?:ID|番号|名前|日時)'
        ]
        
        for pattern in column_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                if match not in [col['name'] for col in info['columns']]:
                    column_type = self._infer_column_type(match, description)
                    info['columns'].append({
                        'name': match,
                        'type': column_type,
                        'nullable': self._infer_nullable(match, description),
                        'comment': f"{match}の情報"
                    })
        
        # ビジネスルール抽出
        rule_keywords = ['必須', '一意', '制約', 'ルール', '条件']
        for keyword in rule_keywords:
            if keyword in description:
                info['business_rules'].append(f"{keyword}に関する制約が存在")
        
        return info
    
    def _infer_column_type(self, column_name: str, context: str) -> str:
        """カラム型推論
        
        Args:
            column_name: カラム名
            context: コンテキスト
            
        Returns:
            str: 推論されたデータ型
        """
        # ID系
        if 'id' in column_name.lower() or 'ID' in column_name:
            return 'INTEGER'
        
        # 日時系
        if any(keyword in column_name for keyword in ['日時', 'date', 'time', '作成', '更新']):
            return 'TIMESTAMP'
        
        # 数値系
        if any(keyword in column_name for keyword in ['数', 'count', 'amount', 'price', 'level']):
            return 'INTEGER'
        
        # 真偽値系
        if any(keyword in column_name for keyword in ['フラグ', 'flag', '有効', 'enabled']):
            return 'BOOLEAN'
        
        # デフォルトは文字列
        return 'VARCHAR(255)'
    
    def _infer_nullable(self, column_name: str, context: str) -> bool:
        """NULL許可推論
        
        Args:
            column_name: カラム名
            context: コンテキスト
            
        Returns:
            bool: NULL許可フラグ
        """
        # 必須項目
        required_keywords = ['id', 'ID', '必須', 'required']
        if any(keyword in column_name or keyword in context for keyword in required_keywords):
            return False
        
        return True
    
    def _generate_yaml(self, info: Dict[str, Any], table_name: Optional[str]) -> str:
        """YAML定義生成
        
        Args:
            info: 解析情報
            table_name: テーブル名
            
        Returns:
            str: YAML定義
        """
        name = table_name or info.get('table_name', 'NewTable')
        
        yaml_content = f"""# テーブル詳細定義
table_name: "{name}"
logical_name: "{name}テーブル"
category: "マスタ系"
priority: "中"
requirement_id: "REQ.1-FUNC.1"
comment: "AI生成による{name}テーブル定義"

# 🔴 改版履歴（絶対省略禁止）
revision_history:
  - version: "1.0.0"
    date: "2025-06-26"
    author: "AI生成システム"
    changes: "初版作成 - AI駆動による自動生成"

# 🔴 テーブル概要・目的（絶対省略禁止）
overview: |
  このテーブルは{name}の情報を管理するテーブルです。
  
  主な目的：
  - {name}の基本情報管理
  - データの一意性保証
  - 関連システムとの連携
  
  このテーブルはスキル報告書システムの{name}管理において重要な役割を果たし、
  他のテーブルとの連携により包括的な情報管理を実現します。

# カラム定義
columns:"""

        # カラム定義追加
        for col in info.get('columns', []):
            yaml_content += f"""
  - name: "{col['name']}"
    type: "{col['type']}"
    nullable: {str(col['nullable']).lower()}
    primary_key: false
    unique: false
    default: null
    comment: "{col['comment']}"
    requirement_id: "REQ.1-FUNC.1" """

        # 標準カラム追加
        yaml_content += """
  - name: "created_at"
    type: "TIMESTAMP"
    nullable: false
    primary_key: false
    unique: false
    default: "CURRENT_TIMESTAMP"
    comment: "作成日時"
    requirement_id: "REQ.1-FUNC.1"
  - name: "updated_at"
    type: "TIMESTAMP"
    nullable: false
    primary_key: false
    unique: false
    default: "CURRENT_TIMESTAMP"
    comment: "更新日時"
    requirement_id: "REQ.1-FUNC.1"

# インデックス定義
indexes:
  - name: "idx_{}_created_at"
    columns: ["created_at"]
    unique: false
    comment: "作成日時インデックス"

# 外部キー定義
foreign_keys: []

# 🔴 特記事項（絶対省略禁止）
notes:
  - "AI生成による自動作成テーブル定義"
  - "実際の業務要件に応じて詳細調整が必要"
  - "パフォーマンス要件に応じたインデックス最適化を検討"

# 🔴 業務ルール（絶対省略禁止）
rules:
  - "データの一意性・整合性を保証する"
  - "作成日時・更新日時は自動設定される"
  - "削除は論理削除を基本とする"

# サンプルデータ（推奨）
sample_data: []""".format(name.lower())

        return yaml_content
    
    def _generate_ddl(self, info: Dict[str, Any], table_name: Optional[str]) -> str:
        """DDL生成
        
        Args:
            info: 解析情報
            table_name: テーブル名
            
        Returns:
            str: DDL文
        """
        name = table_name or info.get('table_name', 'NewTable')
        
        ddl = f"""-- {name}テーブル DDL
-- AI生成による自動作成
-- 生成日時: 2025-06-26

CREATE TABLE {name} (
    id SERIAL PRIMARY KEY,"""

        # カラム定義追加
        for col in info.get('columns', []):
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            ddl += f"""
    {col['name']} {col['type']} {nullable},"""

        # 標準カラム追加
        ddl += """
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- インデックス作成
CREATE INDEX idx_{}_created_at ON {}(created_at);

-- コメント追加
COMMENT ON TABLE {} IS 'AI生成による{}テーブル';""".format(name.lower(), name, name, name)

        return ddl
    
    def _generate_typescript(self, info: Dict[str, Any], table_name: Optional[str]) -> str:
        """TypeScript型定義生成
        
        Args:
            info: 解析情報
            table_name: テーブル名
            
        Returns:
            str: TypeScript型定義
        """
        name = table_name or info.get('table_name', 'NewTable')
        
        ts_content = f"""// {name}テーブル TypeScript型定義
// AI生成による自動作成

export interface {name} {{
  id: number;"""

        # カラム定義追加
        for col in info.get('columns', []):
            ts_type = self._convert_to_typescript_type(col['type'])
            optional = "?" if col['nullable'] else ""
            ts_content += f"""
  {col['name']}{optional}: {ts_type};"""

        # 標準カラム追加
        ts_content += """
  createdAt: Date;
  updatedAt: Date;
}

// 作成用型定義
export interface Create{} extends Omit<{}, 'id' | 'createdAt' | 'updatedAt'> {{}}

// 更新用型定義
export interface Update{} extends Partial<Omit<{}, 'id' | 'createdAt' | 'updatedAt'>> {{}}""".format(name, name, name, name)

        return ts_content
    
    def _generate_prisma(self, info: Dict[str, Any], table_name: Optional[str]) -> str:
        """Prismaスキーマ生成
        
        Args:
            info: 解析情報
            table_name: テーブル名
            
        Returns:
            str: Prismaスキーマ
        """
        name = table_name or info.get('table_name', 'NewTable')
        
        prisma_content = f"""// {name}テーブル Prismaスキーマ
// AI生成による自動作成

model {name} {{
  id        Int      @id @default(autoincrement())"""

        # カラム定義追加
        for col in info.get('columns', []):
            prisma_type = self._convert_to_prisma_type(col['type'])
            optional = "?" if col['nullable'] else ""
            prisma_content += f"""
  {col['name']}{optional}  {prisma_type}"""

        # 標準カラム追加
        prisma_content += f"""
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  @@map("{name.lower()}")
}}"""

        return prisma_content
    
    def _convert_to_typescript_type(self, sql_type: str) -> str:
        """SQL型からTypeScript型への変換"""
        type_mapping = {
            'INTEGER': 'number',
            'SERIAL': 'number',
            'VARCHAR': 'string',
            'TEXT': 'string',
            'TIMESTAMP': 'Date',
            'BOOLEAN': 'boolean',
            'DECIMAL': 'number',
            'FLOAT': 'number'
        }
        
        base_type = sql_type.split('(')[0].upper()
        return type_mapping.get(base_type, 'string')
    
    def _convert_to_prisma_type(self, sql_type: str) -> str:
        """SQL型からPrisma型への変換"""
        type_mapping = {
            'INTEGER': 'Int',
            'SERIAL': 'Int',
            'VARCHAR': 'String',
            'TEXT': 'String',
            'TIMESTAMP': 'DateTime',
            'BOOLEAN': 'Boolean',
            'DECIMAL': 'Decimal',
            'FLOAT': 'Float'
        }
        
        base_type = sql_type.split('(')[0].upper()
        return type_mapping.get(base_type, 'String')
    
    def _analyze_quality(self, content: str, format: str) -> List[str]:
        """品質分析・改善提案
        
        Args:
            content: 生成されたコンテンツ
            format: フォーマット
            
        Returns:
            List[str]: 改善提案リスト
        """
        suggestions = []
        
        if format == "yaml":
            # YAML品質チェック
            if "revision_history" not in content:
                suggestions.append("改版履歴セクションの追加を推奨")
            if "overview" not in content:
                suggestions.append("概要セクションの詳細化を推奨")
            if len(content.split('\n')) < 50:
                suggestions.append("より詳細な定義の追加を推奨")
        
        elif format == "ddl":
            # DDL品質チェック
            if "PRIMARY KEY" not in content:
                suggestions.append("主キーの明示的定義を推奨")
            if "INDEX" not in content:
                suggestions.append("適切なインデックスの追加を推奨")
        
        elif format == "typescript":
            # TypeScript品質チェック
            if "export" not in content:
                suggestions.append("エクスポート文の追加を推奨")
            if "interface" not in content:
                suggestions.append("インターフェース定義の追加を推奨")
        
        return suggestions
    
    def _load_templates(self) -> Dict[str, str]:
        """テンプレート読み込み"""
        return {
            'yaml_base': '',
            'ddl_base': '',
            'typescript_base': '',
            'prisma_base': ''
        }
    
    def _load_patterns(self) -> Dict[str, List[str]]:
        """パターン読み込み"""
        return {
            'table_patterns': [],
            'column_patterns': [],
            'type_patterns': []
        }

# 使用例
if __name__ == "__main__":
    generator = AICodeGenerator()
    
    request = GenerationRequest(
        description="ユーザーテーブルに名前、メールアドレス、年齢のカラムを追加",
        table_name="users",
        target_format="yaml"
    )
    
    result = generator.generate_from_description(request)
    
    if result.success:
        print("生成成功:")
        print(result.content)
        print("\n改善提案:")
        for suggestion in result.suggestions:
            print(f"- {suggestion}")
    else:
        print("生成失敗:")
        print(result.suggestions)
