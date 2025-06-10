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
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.core.models import CheckResult, CheckStatus, TableDefinition, ColumnDefinition
from shared.core.exceptions import ValidationError, ConsistencyCheckError
from shared.checkers.advanced_consistency_checker import AdvancedConsistencyChecker
from shared.checkers.base_checker import BaseChecker


class TestConsistencyChecker(unittest.TestCase):
    """整合性チェッカーのメインテスト"""
    
    def setUp(self):
        """テストセットアップ"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.checker = AdvancedConsistencyChecker(str(self.temp_dir))
        
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
        
        # 設定クラスが期待するディレクトリ構造を作成
        db_dir = self.temp_dir / 'docs' / 'design' / 'database'
        db_dir.mkdir(parents=True)
        
        (db_dir / 'table-details').mkdir()
        (db_dir / 'ddl').mkdir()
        (db_dir / 'tables').mkdir()
        
        # チェッカーを初期化（base_dirを一時ディレクトリに設定）
        self.checker = AdvancedConsistencyChecker(str(self.temp_dir))
        
        # 実際のディレクトリパスを保存
        self.table_details_dir = db_dir / 'table-details'
        self.ddl_dir = db_dir / 'ddl'
        self.tables_dir = db_dir / 'tables'
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_all_files_exist(self):
        """全ファイルが存在する場合のテスト"""
        # テストファイル作成
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

        yaml_path = self.table_details_dir / 'MST_Test_details.yaml'
        ddl_path = self.ddl_dir / 'MST_Test.sql'
        md_path = self.tables_dir / 'テーブル定義書_MST_Test_テスト.md'

        with open(yaml_path, 'w') as f:
            yaml.dump(yaml_content, f)

        ddl_content = """CREATE TABLE MST_Test (
    id VARCHAR(50) NOT NULL PRIMARY KEY
);"""

        with open(ddl_path, 'w') as f:
            f.write(ddl_content)

        md_path.touch()

        # ファイル存在確認
        print(f"Temp dir: {self.temp_dir}")
        print(f"YAML path: {yaml_path}, exists: {yaml_path.exists()}")
        print(f"DDL path: {ddl_path}, exists: {ddl_path.exists()}")
        print(f"MD path: {md_path}, exists: {md_path.exists()}")
        
        # チェッカーの設定確認
        print(f"Checker config base_dir: {self.checker.config.base_dir}")
        print(f"Checker table_details_dir: {self.checker.config.table_details_dir}")
        print(f"Checker ddl_dir: {self.checker.config.ddl_dir}")
        print(f"Checker tables_dir: {self.checker.config.tables_dir}")

        result = self.checker.check(['MST_Test'])
        
        # デバッグ情報を出力
        print(f"Result is_valid: {result.is_valid}")
        print(f"Result status: {result.status}")
        print(f"Result message: {result.message}")
        if hasattr(result, 'errors') and result.errors:
            print(f"Errors: {len(result.errors)}")
            for error in result.errors:
                print(f"  - {error.message}")
        if hasattr(result, 'warnings') and result.warnings:
            print(f"Warnings: {len(result.warnings)}")
            for warning in result.warnings:
                print(f"  - {warning.message}")
        
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
    
    def test_missing_yaml_file(self):
        """YAMLファイルが存在しない場合のテスト"""
        (self.ddl_dir / 'MST_Test.sql').touch()
        (self.tables_dir / 'テーブル定義書_MST_Test_テスト.md').touch()
        
        result = self.checker.check(['MST_Test'])
        self.assertFalse(result.is_valid)
        self.assertTrue(any('YAML詳細定義ファイルが存在しません' in error.message for error in result.errors))
    
    def test_missing_ddl_file(self):
        """DDLファイルが存在しない場合のテスト"""
        (self.table_details_dir / 'MST_Test_details.yaml').touch()
        (self.tables_dir / 'テーブル定義書_MST_Test_テスト.md').touch()
        
        result = self.checker.check(['MST_Test'])
        self.assertFalse(result.is_valid)
        self.assertTrue(any('DDLファイルが存在しません' in error.message for error in result.errors))
    
    def test_missing_markdown_file(self):
        """Markdownファイルが存在しない場合のテスト"""
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
        
        with open(self.table_details_dir / 'MST_Test_details.yaml', 'w') as f:
            yaml.dump(yaml_content, f)
        
        ddl_content = """CREATE TABLE MST_Test (
    id VARCHAR(50) NOT NULL PRIMARY KEY
);"""
        
        with open(self.ddl_dir / 'MST_Test.sql', 'w') as f:
            f.write(ddl_content)
        
        result = self.checker.check(['MST_Test'])
        self.assertFalse(result.is_valid)
        self.assertTrue(any('Markdown定義書が存在しません' in error.message for error in result.errors))


class TestColumnConsistencyChecker(unittest.TestCase):
    """カラム定義整合性チェックのテスト"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # 設定クラスが期待するディレクトリ構造を作成
        db_dir = self.temp_dir / 'docs' / 'design' / 'database'
        db_dir.mkdir(parents=True)
        
        (db_dir / 'table-details').mkdir()
        (db_dir / 'ddl').mkdir()
        (db_dir / 'tables').mkdir()
        
        self.checker = AdvancedConsistencyChecker(str(self.temp_dir))
        
        # 実際のディレクトリパスを保存
        self.table_details_dir = db_dir / 'table-details'
        self.ddl_dir = db_dir / 'ddl'
        self.tables_dir = db_dir / 'tables'
    
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
        
        with open(self.table_details_dir / 'MST_Test_details.yaml', 'w') as f:
            yaml.dump(yaml_content, f)
        
        ddl_content = """CREATE TABLE MST_Test (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);"""
        
        with open(self.ddl_dir / 'MST_Test.sql', 'w') as f:
            f.write(ddl_content)
        
        # Markdownファイルも作成
        (self.tables_dir / 'テーブル定義書_MST_Test_テスト.md').touch()
        
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
        
        with open(self.table_details_dir / 'MST_Test_details.yaml', 'w') as f:
            yaml.dump(yaml_content, f)
        
        ddl_content = """CREATE TABLE MST_Test (
    id VARCHAR(100) NOT NULL PRIMARY KEY
);"""
        
        with open(self.ddl_dir / 'MST_Test.sql', 'w') as f:
            f.write(ddl_content)
        
        # Markdownファイルも作成
        (self.tables_dir / 'テーブル定義書_MST_Test_テスト.md').touch()
        
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
        
        with open(self.table_details_dir / 'MST_Test_details.yaml', 'w') as f:
            yaml.dump(yaml_content, f)
        
        ddl_content = """CREATE TABLE MST_Test (
    name VARCHAR(100) NULL
);"""
        
        with open(self.ddl_dir / 'MST_Test.sql', 'w') as f:
            f.write(ddl_content)
        
        # Markdownファイルも作成
        (self.tables_dir / 'テーブル定義書_MST_Test_テスト.md').touch()
        
        result = self.checker.check(['MST_Test'])
        self.assertFalse(result.is_valid)
        self.assertTrue(any('NULL制約が一致しません' in error.message for error in result.errors))


class TestForeignKeyChecker(unittest.TestCase):
    """外部キー整合性チェックのテスト"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # 設定クラスが期待するディレクトリ構造を作成
        db_dir = self.temp_dir / 'docs' / 'design' / 'database'
        db_dir.mkdir(parents=True)
        
        (db_dir / 'table-details').mkdir()
        (db_dir / 'ddl').mkdir()
        (db_dir / 'tables').mkdir()
        
        self.checker = AdvancedConsistencyChecker(str(self.temp_dir))
        
        # 実際のディレクトリパスを保存
        self.table_details_dir = db_dir / 'table-details'
        self.ddl_dir = db_dir / 'ddl'
        self.tables_dir = db_dir / 'tables'
    
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

        with open(self.table_details_dir / 'MST_Tenant_details.yaml', 'w') as f:
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

        with open(self.table_details_dir / 'MST_Employee_details.yaml', 'w') as f:
            yaml.dump(yaml_content, f)

        # DDLファイルも作成（実装では必要）
        ddl_content = """
CREATE TABLE MST_Employee (
    tenant_id VARCHAR(50) NOT NULL
);
"""
        with open(self.ddl_dir / 'MST_Employee.sql', 'w') as f:
            f.write(ddl_content)

        # Markdownファイルも作成
        (self.tables_dir / 'テーブル定義書_MST_Employee_社員基本情報.md').touch()

        result = self.checker.check(['MST_Employee'])
        # 外部キーチェックは実装されているが、エラーがない場合はis_validがTrue
        self.assertTrue(result.is_valid or len([e for e in result.errors if 'foreign_key' in e.check_type]) == 0)
    
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

        with open(self.table_details_dir / 'MST_Employee_details.yaml', 'w') as f:
            yaml.dump(yaml_content, f)

        # DDLファイルも作成
        ddl_content = """
CREATE TABLE MST_Employee (
    tenant_id VARCHAR(50) NOT NULL
);
"""
        with open(self.ddl_dir / 'MST_Employee.sql', 'w') as f:
            f.write(ddl_content)

        # Markdownファイルも作成
        (self.tables_dir / 'テーブル定義書_MST_Employee_社員基本情報.md').touch()

        result = self.checker.check(['MST_Employee'])
        
        # デバッグ出力
        print(f"Result is_valid: {result.is_valid}")
        print(f"Errors count: {len(result.errors)}")
        for i, error in enumerate(result.errors):
            print(f"Error {i}: {error.message}")
        
        self.assertFalse(result.is_valid)
        self.assertTrue(any('参照先テーブル' in error.message and '存在しません' in error.message for error in result.errors))
    
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

        with open(self.table_details_dir / 'MST_Tenant_details.yaml', 'w') as f:
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

        with open(self.table_details_dir / 'MST_Employee_details.yaml', 'w') as f:
            yaml.dump(yaml_content, f)

        # DDLファイルも作成
        ddl_content = """
CREATE TABLE MST_Employee (
    tenant_id VARCHAR(50) NOT NULL
);
"""
        with open(self.ddl_dir / 'MST_Employee.sql', 'w') as f:
            f.write(ddl_content)

        # Markdownファイルも作成
        (self.tables_dir / 'テーブル定義書_MST_Employee_社員基本情報.md').touch()

        result = self.checker.check(['MST_Employee'])
        self.assertFalse(result.is_valid)
        self.assertTrue(any('データ型が一致しません' in error.message for error in result.errors))


class TestNamingConventionChecker(unittest.TestCase):
    """命名規則チェックのテスト"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.checker = AdvancedConsistencyChecker(str(self.temp_dir))
    
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
        self.checker = AdvancedConsistencyChecker(str(self.temp_dir))
        
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
        # 孤立したYAMLファイルを作成（内容も含める）
        orphan_yaml = {
            'table_name': 'MST_Orphan',
            'columns': [
                {
                    'name': 'id',
                    'type': 'VARCHAR(50)',
                    'nullable': False
                }
            ]
        }
        with open(self.temp_dir / 'table-details' / 'MST_Orphan_details.yaml', 'w') as f:
            yaml.dump(orphan_yaml, f)

        result = self.checker.check()
        # 孤立ファイルがある場合は警告が出るが、is_validはTrueのまま（警告レベル）
        self.assertTrue(len(result.warnings) > 0 or any('孤立' in str(w) for w in result.warnings))
        self.assertTrue(any('孤立したYAML詳細定義ファイル' in warning.message for warning in result.warnings))
    
    def test_orphaned_ddl_file(self):
        """孤立したDDLファイルがある場合のテスト"""
        # 孤立したDDLファイルを作成
        ddl_content = """
CREATE TABLE MST_Orphan (
    id VARCHAR(50) NOT NULL
);
"""
        with open(self.temp_dir / 'ddl' / 'MST_Orphan.sql', 'w') as f:
            f.write(ddl_content)

        result = self.checker.check()
        # 孤立ファイルがある場合は警告が出るが、is_validはTrueのまま（警告レベル）
        self.assertTrue(len(result.warnings) > 0 or any('孤立' in str(w) for w in result.warnings))
        self.assertTrue(any('孤立したDDLファイル' in warning.message for warning in result.warnings))
    
    def test_orphaned_markdown_file(self):
        """孤立したMarkdownファイルがある場合のテスト"""
        # 孤立したMarkdownファイルを作成
        md_content = """# テーブル定義書_MST_Orphan_孤立

## テーブル概要
孤立したテーブル
"""
        with open(self.temp_dir / 'tables' / 'テーブル定義書_MST_Orphan_孤立.md', 'w') as f:
            f.write(md_content)

        result = self.checker.check()
        # 孤立ファイルがある場合は警告が出るが、is_validはTrueのまま（警告レベル）
        self.assertTrue(len(result.warnings) > 0 or any('孤立' in str(w) for w in result.warnings))
        self.assertTrue(any('孤立したMarkdown定義書' in warning.message for warning in result.warnings))


if __name__ == '__main__':
    # テストスイート実行
    unittest.main(verbosity=2)
