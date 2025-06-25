#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MST_Certification制約問題修正ツール

YAMLファイルの制約定義をDDLに正しく反映させるための修正を実行します。

問題:
1. YAML読み込みツールで制約処理がコメントアウトされている
2. CHECK制約がDDLに反映されていない
3. is_deletedのデフォルト値が文字列'False'になっている

修正内容:
1. YAML読み込みツールの制約処理を有効化
2. DDL生成ツールの制約処理を強化
3. デフォルト値の型変換を修正
4. MST_CertificationのDDL・定義書を再生成
"""

import sys
import os
from pathlib import Path
import yaml
import re
from datetime import datetime

# プロジェクトルートを取得
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "docs/design/database/tools"))

def fix_yaml_loader():
    """YAML読み込みツールの制約処理を有効化"""
    yaml_loader_path = project_root / "docs/design/database/tools/table_generator/utils/yaml_loader.py"
    
    print("🔧 YAML読み込みツールの制約処理を有効化中...")
    
    with open(yaml_loader_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 制約処理のコメントアウトを解除
    content = content.replace(
        '# if \'business_constraints\' in yaml_data:\n#     table_def.business_constraints = self._parse_constraints(yaml_data[\'business_constraints\'])',
        'if \'constraints\' in yaml_data:\n    table_def.constraints = self._parse_constraints(yaml_data[\'constraints\'])'
    )
    
    # _parse_constraintsメソッドのコメントアウトを解除
    content = content.replace(
        '# def _parse_constraints(self, constraints_data: List[Dict[str, Any]]) -> List[ConstraintDefinition]:',
        'def _parse_constraints(self, constraints_data: List[Dict[str, Any]]) -> List[ConstraintDefinition]:'
    )
    
    # メソッド内容のコメントアウトを解除
    content = re.sub(
        r'#     """制約定義を解析（ConstraintDefinitionクラスが存在しないためコメントアウト）.*?#     return constraints',
        '''    """制約定義を解析
    
    Args:
        constraints_data (List[Dict[str, Any]]): 制約定義データ
        
    Returns:
        List[ConstraintDefinition]: 制約定義リスト
    """
    from shared.core.models import ConstraintDefinition
    constraints = []
    
    for const_data in constraints_data:
        try:
            constraint = ConstraintDefinition(
                name=const_data['name'],
                type=const_data['type'],
                columns=const_data.get('columns', []),
                condition=const_data.get('condition', ''),
                comment=const_data.get('comment', const_data.get('description', ''))
            )
            constraints.append(constraint)
            
        except KeyError as e:
            self.logger.error(f"制約定義に必須フィールドがありません: {e}")
        except Exception as e:
            self.logger.error(f"制約定義解析エラー: {e}")
    
    return constraints''',
        content,
        flags=re.DOTALL
    )
    
    with open(yaml_loader_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ YAML読み込みツールの制約処理を有効化しました")

def fix_ddl_generator():
    """DDL生成ツールの制約処理を強化"""
    ddl_generator_path = project_root / "docs/design/database/tools/table_generator/generators/ddl_generator.py"
    
    print("🔧 DDL生成ツールの制約処理を強化中...")
    
    with open(ddl_generator_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 制約処理部分を修正
    old_constraint_section = '''        # その他の制約
        if hasattr(table_def, 'constraints') and table_def.constraints:
            ddl_lines.append("-- その他の制約")
            for constraint in table_def.constraints:
                constraint_sql = self._generate_constraint_ddl(table_def.table_name, constraint)
                ddl_lines.append(constraint_sql)
            ddl_lines.append("")
        elif hasattr(table_def, 'business_constraints') and table_def.business_constraints:
            ddl_lines.append("-- その他の制約")
            for constraint in table_def.business_constraints:
                constraint_sql = self._generate_constraint_ddl(table_def.table_name, constraint)
                ddl_lines.append(constraint_sql)
            ddl_lines.append("")'''
    
    new_constraint_section = '''        # その他の制約
        constraints_to_process = []
        if hasattr(table_def, 'constraints') and table_def.constraints:
            constraints_to_process.extend(table_def.constraints)
        elif hasattr(table_def, 'business_constraints') and table_def.business_constraints:
            constraints_to_process.extend(table_def.business_constraints)
        
        if constraints_to_process:
            ddl_lines.append("-- その他の制約")
            for constraint in constraints_to_process:
                constraint_sql = self._generate_constraint_ddl(table_def.table_name, constraint)
                if constraint_sql and not constraint_sql.startswith("-- 未対応"):
                    ddl_lines.append(constraint_sql)
            ddl_lines.append("")'''
    
    content = content.replace(old_constraint_section, new_constraint_section)
    
    # _generate_constraint_ddlメソッドを強化
    old_constraint_method = '''    def _generate_constraint_ddl(self, table_name: str, constraint) -> str:
        """制約DDLを生成
        
        Args:
            table_name (str): テーブル名
            constraint: 制約定義
            
        Returns:
            str: 制約DDL
        """
        # 制約の種類に応じてDDLを生成
        if constraint.type.upper() == 'CHECK':
            return f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint.name} CHECK ({constraint.condition});"
        elif constraint.type.upper() == 'UNIQUE':
            columns = ', '.join(constraint.columns) if hasattr(constraint, 'columns') else constraint.condition
            return f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint.name} UNIQUE ({columns});"
        else:
            return f"-- 未対応の制約タイプ: {constraint.type}"'''
    
    new_constraint_method = '''    def _generate_constraint_ddl(self, table_name: str, constraint) -> str:
        """制約DDLを生成
        
        Args:
            table_name (str): テーブル名
            constraint: 制約定義
            
        Returns:
            str: 制約DDL
        """
        try:
            # 制約の種類に応じてDDLを生成
            if constraint.type.upper() == 'CHECK':
                if hasattr(constraint, 'condition') and constraint.condition:
                    return f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint.name} CHECK ({constraint.condition});"
                else:
                    self.logger.warning(f"CHECK制約 {constraint.name} に条件が設定されていません")
                    return f"-- CHECK制約 {constraint.name} に条件が設定されていません"
            elif constraint.type.upper() == 'UNIQUE':
                if hasattr(constraint, 'columns') and constraint.columns:
                    columns = ', '.join(constraint.columns)
                    return f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint.name} UNIQUE ({columns});"
                elif hasattr(constraint, 'condition') and constraint.condition:
                    return f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint.name} UNIQUE ({constraint.condition});"
                else:
                    self.logger.warning(f"UNIQUE制約 {constraint.name} にカラムが設定されていません")
                    return f"-- UNIQUE制約 {constraint.name} にカラムが設定されていません"
            else:
                self.logger.warning(f"未対応の制約タイプ: {constraint.type}")
                return f"-- 未対応の制約タイプ: {constraint.type}"
        except Exception as e:
            self.logger.error(f"制約DDL生成エラー ({constraint.name}): {e}")
            return f"-- 制約DDL生成エラー: {constraint.name}"'''
    
    content = content.replace(old_constraint_method, new_constraint_method)
    
    with open(ddl_generator_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ DDL生成ツールの制約処理を強化しました")

def fix_yaml_default_values():
    """YAMLファイルのデフォルト値を修正"""
    yaml_path = project_root / "docs/design/database/table-details/テーブル詳細定義YAML_MST_Certification.yaml"
    
    print("🔧 YAMLファイルのデフォルト値を修正中...")
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # is_deletedのデフォルト値を修正
    content = content.replace("default: 'False'", "default: false")
    
    # 改版履歴を追加
    current_time = datetime.now().strftime('%Y-%m-%d')
    new_version = f"4.1.{current_time.replace('-', '')}"
    
    revision_section = """revision_history:
- version: 1.0.0
  date: '2025-06-01'
  author: 開発チーム
  changes: 初版作成 - 資格情報マスタテーブルの詳細定義
- version: 2.0.0
  date: '2025-06-22'
  author: 自動変換ツール
  changes: テンプレート形式への自動変換
- version: 3.1.20250624
  date: '2025-06-24'
  author: 自動修正ツール
  changes: カラム順序を推奨順序に自動修正
- version: 3.2.20250624
  date: '2025-06-24'
  author: 主キー修正ツール
  changes: certification_id カラム削除、id を正しい主キーに設定
- version: 4.0.20250624
  date: '2025-06-24'
  author: カラム順序統一ツール
  changes: certification_id を主キーとして復活、指定されたカラム順序に統一"""
    
    new_revision_section = f"""{revision_section}
- version: {new_version}
  date: '{current_time}'
  author: 制約修正ツール
  changes: デフォルト値の型修正、制約処理の有効化"""
    
    content = re.sub(
        r'revision_history:.*?changes: certification_id を主キーとして復活、指定されたカラム順序に統一',
        new_revision_section,
        content,
        flags=re.DOTALL
    )
    
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ YAMLファイルのデフォルト値を修正しました")

def regenerate_files():
    """MST_CertificationのDDL・定義書を再生成"""
    print("🔧 MST_CertificationのDDL・定義書を再生成中...")
    
    try:
        # テーブル生成ツールを実行
        os.chdir(project_root / "docs/design/database/tools")
        
        # 直接生成ツールを実行
        result = os.system("python3 -m table_generator --table MST_Certification --verbose")
        
        if result == 0:
            print("✅ MST_CertificationのDDL・定義書を再生成しました")
        else:
            print("⚠️ 再生成中にエラーが発生しました")
            
    except Exception as e:
        print(f"❌ 再生成エラー: {e}")

def main():
    """メイン処理"""
    print("🚀 MST_Certification制約問題修正ツールを開始します")
    print("=" * 60)
    
    try:
        # 1. YAML読み込みツールの制約処理を有効化
        fix_yaml_loader()
        
        # 2. DDL生成ツールの制約処理を強化
        fix_ddl_generator()
        
        # 3. YAMLファイルのデフォルト値を修正
        fix_yaml_default_values()
        
        # 4. MST_CertificationのDDL・定義書を再生成
        regenerate_files()
        
        print("=" * 60)
        print("✅ 全ての修正が完了しました！")
        print()
        print("修正内容:")
        print("1. ✅ YAML読み込みツールの制約処理を有効化")
        print("2. ✅ DDL生成ツールの制約処理を強化")
        print("3. ✅ is_deletedのデフォルト値を'False'からfalseに修正")
        print("4. ✅ MST_CertificationのDDL・定義書を再生成")
        print()
        print("確認してください:")
        print("- docs/design/database/ddl/MST_Certification.sql")
        print("- docs/design/database/tables/テーブル定義書_MST_Certification_資格情報.md")
        
    except Exception as e:
        print(f"❌ 修正中にエラーが発生しました: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
