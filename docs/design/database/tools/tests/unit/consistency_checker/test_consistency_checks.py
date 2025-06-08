"""
整合性チェック機能のユニットテスト

要求仕様ID: PLT.1-WEB.1, SKL.1-HIER.1
設計書: docs/design/database/08-database-design-guidelines.md
実装日: 2025-06-08
実装者: AI Assistant

整合性チェック機能の詳細テスト：
- テーブル存在整合性チェック
- カラム定義整合性チェック
- 外部キー整合性チェック
- データ型整合性チェック
- 孤立ファイル検出
- 命名規則チェック
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import yaml

# テスト対象のインポート
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from database_consistency_checker.core.consistency_checker import ConsistencyChecker
from database_consistency_checker.core.checkers import (
    TableExistenceChecker,
    ColumnConsistencyChecker,
    ForeignKeyChecker,
    DataTypeChecker,
    OrphanedFileChecker,
    NamingConventionChecker
)
from shared.core.exceptions import ValidationError, ConsistencyError
from shared.core.models import TableDefinition, ColumnDefinition


class TestConsistencyChecker(unittest.TestCase):
    """整合性チェッカーのメインテスト"""
    
    def setUp(self):
        """テストセットアップ"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.checker = ConsistencyChecker(str(self.temp_dir))
        
        # テスト用ディレクトリ構造作成
        (self.temp_dir / 'table-details').mkdir()
        (self.temp_dir / 'ddl').mkdir()
        (self.temp_dir / 'tables').mkdir()
        (self.temp_dir / 'data').mkdir()
        
        # テスト用ファイル作成
        self._create_test_files()
    
    def tearDown(self):
        """テストクリーンアップ"""
        shutil.rmtree(self.temp_dir)
    
    def _create_test_files(self):
        """テスト用ファイル作成"""
        # YAML詳細定義
        yaml_content = {
            'table_name': 'MST_Employee',
            'logical_name': '社員基本情報',
            'category': 'マスタ系',
            'priority': '最高',
            'requirement_id': 'PRO.1-BASE.1',
            'columns': [
                {
                    'name': 'id',
                    'type': 'VARCHAR(50)',
                    'nullable': False,
                    'primary_key': True,
                    'comment': 'プライマリキー（UUID）',
                    'requirement_id': 'PLT.1-WEB.1'
                },
                {
                    'name': 'tenant_id',
                    'type': 'VARCHAR(50)',
                    'nullable': False,
                    'comment': 'マルチテナント識別子',
                    'requirement_id': 'TNT.1-MGMT.1'
                }
            ],
            'indexes': [
                {
                    'name': 'idx_employee_tenant',
                    'columns': ['tenant_id'],
                    'unique': False,
                    'comment': 'テナント別検索用インデックス'
                }
            ],
            'foreign_keys': [
                {
                    'name': 'fk_employee_tenant',
                    'columns': ['tenant_id'],
                    'references': {
                        'table': 'MST_Tenant',
                        'columns': ['id']
                    },
                    'on_update': 'CASCADE',
                    'on_delete': 'RESTRICT'
                }
            ]
        }
        
        with open(self.temp_dir / 'table-details' / 'MST_Employee_details.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(yaml_content, f, default_flow_style=False, allow_unicode=True)
        
        # DDLファイル
        ddl_content = """-- MST_Employee テーブル定義
CREATE TABLE MST_Employee (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    tenant_id VARCHAR(50) NOT NULL,
    emp_no VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(tenant_id, emp_no),
    UNIQUE(tenant_id, email)
);

-- インデックス作成
CREATE INDEX idx_employee_tenant ON MST_Employee(tenant_id);

-- 外部キー制約
ALTER TABLE MST_Employee 
ADD CONSTRAINT fk_employee_tenant 
FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(id) 
ON UPDATE CASCADE ON DELETE RESTRICT;
"""
        
        with open(self.temp_dir / 'ddl' / 'MST_Employee.sql', 'w', encoding='utf-8') as f:
            f.write(ddl_content)
        
        # Markdownテーブル定義書
        md_content = """# テーブル定義書_MST_Employee_社員基本情報

## 基本情報
- **テーブル名**: MST_Employee
- **論理名**: 社員基本情報
- **カテゴリ**: マスタ系
- **優先度**: 最高
- **要求仕様ID**: PRO.1-BASE.1

## カラム定義
| カラム名 | データ型 | NULL | キー | デフォルト値 | コメント | 要求仕様ID |
|----------|----------|------|------|-------------|----------|------------|
| id | VARCHAR(50) | NOT NULL | PK | - | プライマリキー（UUID） | PLT.1-WEB.1 |
| tenant_id | VARCHAR(50) | NOT NULL | FK | - | マルチテナント識別子 | TNT.1-MGMT.1 |
"""
        
        with open(self.temp_dir / 'tables' / 'テーブル定義書_MST_Employee_社員基本情報.md', 'w', encoding='utf-8') as f:
            f.write(md_content)


class TestTableExistenceChecker(unittest.TestCase):
    """テーブル存在整合性チェックのテスト"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.checker = TableExistenceChecker(str(self.temp_dir))
        
        # テスト用ディレクトリ作成
        (self.temp_dir / 'table-details').mkdir()
        (self.temp_dir / 'ddl').mkdir()
        (self.temp_dir / 'tables').mkdir()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_all_files_exist(self):
        """全ファイルが存在する場合のテスト"""
        # テストファイル作成
        (self.temp_dir / 'table-details' / 'MST_Test_details.yaml').touch()
        (self.temp_dir / 'ddl' / 'MST_Test.sql').touch()
        (self.temp_dir / 'tables' / 'テーブル定義書_MST_Test_テスト.md').touch()
        
        result = self.checker.check(['MST_Test'])
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
    
    def test_missing_yaml_file(self):
        """YAMLファイルが存在しない場合のテスト"""
        (self.temp_dir / 'ddl' / 'MST_Test.sql').touch()
        (self.temp_dir / 'tables' / 'テーブル定義書_MST_Test_テスト.md').touch()
        
        result = self.checker.check(['MST_Test'])
        self.assertFalse(result.is_valid)
        self.assertTrue(any('YAML詳細定義ファイルが存在しません' in error.message for error in result.errors))
    
    def test_missing_ddl_file(self):
        """DDLファイルが存在しない場合のテスト"""
        (self.temp_dir / 'table-details' / 'MST_Test_details.yaml').touch()
        (self.temp_dir / 'tables' / 'テーブル定義書_MST_Test_テスト.md').touch()
        
        result = self.checker.check(['MST_Test'])
        self.assertFalse(result.is_valid)
        self.assertTrue(any('DDLファイルが存在しません' in error.message for error in result.errors))
    
    def test_missing_markdown_file(self):
        """Markdownファイルが存在しない場合のテスト"""
        (self.temp_dir / 'table-details' / 'MST_Test_details.yaml').touch()
        (self.temp_dir / 'ddl' / 'MST_Test.sql').touch()
        
        result = self.checker.check(['MST_Test'])
        self.assertFalse(result.is_valid)
        self.assertTrue(any('Markdown定義書が存在しません' in error.message for error in result.errors))


class TestColumnConsistencyChecker(unittest.TestCase):
    """カラム定義整合性チェックのテスト"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.checker = ColumnConsistencyChecker(str(self.temp_dir))
        
        # テスト用ディレクトリ作成
        (self.temp_dir / 'table-details').mkdir()
        (self.temp_dir / 'ddl').mkdir()
        (self.temp_dir / 'tables').mkdir()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_consistent_columns(self):
        """カラム定義が一致する場合のテスト"""
        # 一致するYAMLとDDLを作成
        yaml_content = {
            'table_name': 'MST_Test',
            'columns': [
                {
                    'name': 'id',
                    'type': 'VARCHAR(50)',
                    'nullable': False,
                    'primary_key': True
                },
                {
                    'name': 'name',
                    'type': 'VARCHAR(100)',
                    'nullable': False
                }
            ]
        }
        
        with open(self.temp_dir / 'table-details' / 'MST_Test_details.yaml', 'w') as f:
            yaml.dump(yaml_content, f)
        
        ddl_content = """CREATE TABLE MST_Test (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);"""
        
        with open(self.temp_dir / 'ddl' / 'MST_Test.sql', 'w') as f:
            f.write(ddl_content)
        
        result = self.checker.check(['MST_Test'])
        self.assertTrue(result.is_valid)
    
    def test_data_type_mismatch(self):
        """データ型が一致しない場合のテスト"""
        yaml_content = {
            'table_name': 'MST_Test',
            'columns': [
                {
                    'name': 'id',
                    'type': 'VARCHAR(50)',
                    'nullable': False,
                    'primary_key': True
                }
            ]
        }
        
        with open(self.temp_dir / 'table-details' / 'MST_Test_details.yaml', 'w') as f:
            yaml.dump(yaml_content, f)
        
        ddl_content = """CREATE TABLE MST_Test (
    id VARCHAR(100) NOT NULL PRIMARY KEY
);"""
        
        with open(self.temp_dir / 'ddl' / 'MST_Test.sql', 'w') as f:
            f.write(ddl_content)
        
        result = self.checker.check(['MST_Test'])
        self.assertFalse(result.is_valid)
        self.assertTrue(any('データ型が一致しません' in error.message for error in result.errors))
    
    def test_nullable_mismatch(self):
        """NULL制約が一致しない場合のテスト"""
        yaml_content = {
            'table_name': 'MST_Test',
            'columns': [
                {
                    'name': 'name',
                    'type': 'VARCHAR(100)',
                    'nullable': False
                }
            ]
        }
        
        with open(self.temp_dir / 'table-details' / 'MST_Test_details.yaml', 'w') as f:
            yaml.dump(yaml_content, f)
        
        ddl_content = """CREATE TABLE MST_Test (
    name VARCHAR(100) NULL
);"""
        
        with open(self.temp_dir / 'ddl' / 'MST_Test.sql', 'w') as f:
            f.write(ddl_content)
        
        result = self.checker.check(['MST_Test'])
        self.assertFalse(result.is_valid)
        self.assertTrue(any('NULL制約が一致しません' in error.message for error in result.errors))


class TestForeignKeyChecker(unittest.TestCase):
    """外部キー整合性チェックのテスト"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.checker = ForeignKeyChecker(str(self.temp_dir))
        
        # テスト用ディレクトリ作成
        (self.temp_dir / 'table-details').mkdir()
        (self.temp_dir / 'ddl').mkdir()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_valid_foreign_key(self):
        """有効な外部キーの場合のテスト"""
        # 参照先テーブル作成
        ref_yaml = {
            'table_name': 'MST_Tenant',
            'columns': [
                {
                    'name': 'id',
                    'type': 'VARCHAR(50)',
                    'nullable': False,
                    'primary_key': True
                }
            ]
        }
        
        with open(self.temp_dir / 'table-details' / 'MST_Tenant_details.yaml', 'w') as f:
            yaml.dump(ref_yaml, f)
        
        # 参照元テーブル作成
        yaml_content = {
            'table_name': 'MST_Employee',
            'columns': [
                {
                    'name': 'tenant_id',
                    'type': 'VARCHAR(50)',
                    'nullable': False
                }
            ],
            'foreign_keys': [
                {
                    'name': 'fk_employee_tenant',
                    'columns': ['tenant_id'],
                    'references': {
                        'table': 'MST_Tenant',
                        'columns': ['id']
                    }
                }
            ]
        }
        
        with open(self.temp_dir / 'table-details' / 'MST_Employee_details.yaml', 'w') as f:
            yaml.dump(yaml_content, f)
        
        result = self.checker.check(['MST_Employee'])
        self.assertTrue(result.is_valid)
    
    def test_missing_reference_table(self):
        """参照先テーブルが存在しない場合のテスト"""
        yaml_content = {
            'table_name': 'MST_Employee',
            'columns': [
                {
                    'name': 'tenant_id',
                    'type': 'VARCHAR(50)',
                    'nullable': False
                }
            ],
            'foreign_keys': [
                {
                    'name': 'fk_employee_tenant',
                    'columns': ['tenant_id'],
                    'references': {
                        'table': 'MST_NonExistent',
                        'columns': ['id']
                    }
                }
            ]
        }
        
        with open(self.temp_dir / 'table-details' / 'MST_Employee_details.yaml', 'w') as f:
            yaml.dump(yaml_content, f)
        
        result = self.checker.check(['MST_Employee'])
        self.assertFalse(result.is_valid)
        self.assertTrue(any('参照先テーブルが存在しません' in error.message for error in result.errors))
    
    def test_data_type_mismatch_in_foreign_key(self):
        """外部キーのデータ型が一致しない場合のテスト"""
        # 参照先テーブル（VARCHAR(100)）
        ref_yaml = {
            'table_name': 'MST_Tenant',
            'columns': [
                {
                    'name': 'id',
                    'type': 'VARCHAR(100)',
                    'nullable': False,
                    'primary_key': True
                }
            ]
        }
        
        with open(self.temp_dir / 'table-details' / 'MST_Tenant_details.yaml', 'w') as f:
            yaml.dump(ref_yaml, f)
        
        # 参照元テーブル（VARCHAR(50)）
        yaml_content = {
            'table_name': 'MST_Employee',
            'columns': [
                {
                    'name': 'tenant_id',
                    'type': 'VARCHAR(50)',
                    'nullable': False
                }
            ],
            'foreign_keys': [
                {
                    'name': 'fk_employee_tenant',
                    'columns': ['tenant_id'],
                    'references': {
                        'table': 'MST_Tenant',
                        'columns': ['id']
                    }
                }
            ]
        }
        
        with open(self.temp_dir / 'table-details' / 'MST_Employee_details.yaml', 'w') as f:
            yaml.dump(yaml_content, f)
        
        result = self.checker.check(['MST_Employee'])
        self.assertFalse(result.is_valid)
        self.assertTrue(any('参照先カラムのデータ型が一致しません' in error.message for error in result.errors))


class TestNamingConventionChecker(unittest.TestCase):
    """命名規則チェックのテスト"""
    
    def setUp(self):
        self.checker = NamingConventionChecker()
    
    def test_valid_table_names(self):
        """有効なテーブル名のテスト"""
        valid_names = [
            'MST_Employee',
            'TRN_SkillRecord',
            'HIS_LoginHistory',
            'SYS_Configuration',
            'WRK_BatchJob',
            'IF_ExternalData'
        ]
        
        for name in valid_names:
            result = self.checker.check_table_name(name)
            self.assertTrue(result.is_valid, f"テーブル名 {name} が無効と判定されました")
    
    def test_invalid_table_names(self):
        """無効なテーブル名のテスト"""
        invalid_names = [
            'Employee',  # プレフィックスなし
            'mst_employee',  # 小文字
            'MST_',  # プレフィックスのみ
            'INVALID_Employee',  # 無効なプレフィックス
            'MST-Employee'  # ハイフン使用
        ]
        
        for name in invalid_names:
            result = self.checker.check_table_name(name)
            self.assertFalse(result.is_valid, f"テーブル名 {name} が有効と判定されました")
    
    def test_valid_column_names(self):
        """有効なカラム名のテスト"""
        valid_names = [
            'id',
            'tenant_id',
            'emp_no',
            'skill_level',
            'created_at',
            'is_deleted'
        ]
        
        for name in valid_names:
            result = self.checker.check_column_name(name)
            self.assertTrue(result.is_valid, f"カラム名 {name} が無効と判定されました")
    
    def test_invalid_column_names(self):
        """無効なカラム名のテスト"""
        invalid_names = [
            'ID',  # 大文字
            'empNo',  # キャメルケース
            'emp-no',  # ハイフン使用
            'emp no',  # スペース使用
            '1st_name'  # 数字開始
        ]
        
        for name in invalid_names:
            result = self.checker.check_column_name(name)
            self.assertFalse(result.is_valid, f"カラム名 {name} が有効と判定されました")


class TestOrphanedFileChecker(unittest.TestCase):
    """孤立ファイル検出のテスト"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.checker = OrphanedFileChecker(str(self.temp_dir))
        
        # テスト用ディレクトリ作成
        (self.temp_dir / 'table-details').mkdir()
        (self.temp_dir / 'ddl').mkdir()
        (self.temp_dir / 'tables').mkdir()
        (self.temp_dir / 'data').mkdir()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_no_orphaned_files(self):
        """孤立ファイルがない場合のテスト"""
        # 完全なファイルセット作成
        (self.temp_dir / 'table-details' / 'MST_Test_details.yaml').touch()
        (self.temp_dir / 'ddl' / 'MST_Test.sql').touch()
        (self.temp_dir / 'tables' / 'テーブル定義書_MST_Test_テスト.md').touch()
        (self.temp_dir / 'data' / 'MST_Test_sample_data.sql').touch()
        
        result = self.checker.check()
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.warnings), 0)
    
    def test_orphaned_yaml_file(self):
        """孤立したYAMLファイルがある場合のテスト"""
        (self.temp_dir / 'table-details' / 'MST_Orphan_details.yaml').touch()
        
        result = self.checker.check()
        self.assertFalse(result.is_valid)
        self.assertTrue(any('孤立したYAML詳細定義ファイル' in warning.message for warning in result.warnings))
    
    def test_orphaned_ddl_file(self):
        """孤立したDDLファイルがある場合のテスト"""
        (self.temp_dir / 'ddl' / 'MST_Orphan.sql').touch()
        
        result = self.checker.check()
        self.assertFalse(result.is_valid)
        self.assertTrue(any('孤立したDDLファイル' in warning.message for warning in result.warnings))
    
    def test_orphaned_markdown_file(self):
        """孤立したMarkdownファイルがある場合のテスト"""
        (self.temp_dir / 'tables' / 'テーブル定義書_MST_Orphan_孤立.md').touch()
        
        result = self.checker.check()
        self.assertFalse(result.is_valid)
        self.assertTrue(any('孤立したMarkdown定義書' in warning.message for warning in result.warnings))


if __name__ == '__main__':
    # テストスイート実行
    unittest.main(verbosity=2)
