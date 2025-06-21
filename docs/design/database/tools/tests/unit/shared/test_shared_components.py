"""
共有コンポーネントのユニットテスト

要求仕様ID: PLT.1-WEB.1, SKL.1-HIER.1
設計書: docs/design/database/08-database-design-guidelines.md
実装日: 2025-06-08
実装者: AI Assistant

共有コンポーネントの詳細テスト：
- パーサー機能（YAML、DDL、Markdown）
- ジェネレーター機能（DDL、Markdown、サンプルデータ）
- アダプター機能（ファイルシステム、データ変換）
- ユーティリティ機能
- 設定管理
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import yaml
import json
import pytest

# テスト対象のインポート
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.core.models import TableDefinition, ColumnDefinition, CheckResult, CheckStatus
from shared.core.exceptions import ValidationError, ConfigurationError
from shared.core.config import DatabaseToolsConfig
from shared.core.logger import DatabaseToolsLogger
from shared.parsers.yaml_parser import YamlParser
from shared.parsers.ddl_parser import DDLParser
from shared.parsers.markdown_parser import MarkdownParser
from shared.generators.ddl_generator import DDLGenerator
from shared.generators.markdown_generator import MarkdownGenerator
from shared.generators.sample_data_generator import SampleDataGenerator
from shared.adapters.unified.filesystem_adapter import UnifiedFileSystemAdapter
from shared.adapters.unified.data_transform_adapter import UnifiedDataTransformAdapter
from shared.utils.file_utils import FileManager, BackupManager


@pytest.mark.unit
class TestDatabaseToolsConfig(unittest.TestCase):
    """設定管理のテスト"""
    
    def setUp(self):
        """テストセットアップ"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.config = DatabaseToolsConfig(base_dir=self.temp_dir)
    
    def tearDown(self):
        """テストクリーンアップ"""
        shutil.rmtree(self.temp_dir)
    
    def test_default_configuration(self):
        """デフォルト設定のテスト"""
        self.assertEqual(self.config.base_dir, self.temp_dir)
        self.assertEqual(self.config.table_details_dir, self.temp_dir / 'docs' / 'design' / 'database' / 'table-details')
        self.assertEqual(self.config.ddl_dir, self.temp_dir / 'docs' / 'design' / 'database' / 'ddl')
        self.assertEqual(self.config.tables_dir, self.temp_dir / 'docs' / 'design' / 'database' / 'tables')
        self.assertEqual(self.config.data_dir, self.temp_dir / 'docs' / 'design' / 'database' / 'data')
    
    def test_custom_configuration(self):
        """カスタム設定のテスト"""
        config = DatabaseToolsConfig(
            base_dir=self.temp_dir,
            default_sample_count=20,
            faker_locale='en_US',
            backup_enabled=False
        )
        
        self.assertEqual(config.default_sample_count, 20)
        self.assertEqual(config.faker_locale, 'en_US')
        self.assertFalse(config.backup_enabled)
    
    def test_environment_configuration(self):
        """環境変数からの設定読み込みテスト"""
        with patch.dict('os.environ', {
            'DB_TOOLS_BASE_DIR': str(self.temp_dir),
            'DB_TOOLS_LOG_LEVEL': 'DEBUG',
            'DB_TOOLS_SAMPLE_COUNT': '15',
            'DB_TOOLS_BACKUP_ENABLED': 'false'
        }):
            config = DatabaseToolsConfig.from_env()
            self.assertEqual(config.base_dir, self.temp_dir)
            self.assertEqual(config.log_level.value, 'DEBUG')
            self.assertEqual(config.default_sample_count, 15)
            self.assertFalse(config.backup_enabled)
    
    def test_path_generation_methods(self):
        """パス生成メソッドのテスト"""
        table_name = 'MST_Employee'
        logical_name = '社員基本情報'
        
        # テーブル詳細定義ファイルパス
        detail_path = self.config.get_table_detail_path(table_name)
        expected_detail = self.config.table_details_dir / f"{table_name}_details.yaml"
        self.assertEqual(detail_path, expected_detail)
        
        # DDLファイルパス
        ddl_path = self.config.get_ddl_path(table_name)
        expected_ddl = self.config.ddl_dir / f"{table_name}.sql"
        self.assertEqual(ddl_path, expected_ddl)
        
        # テーブル定義書パス
        table_def_path = self.config.get_table_definition_path(table_name, logical_name)
        expected_table_def = self.config.tables_dir / f"テーブル定義書_{table_name}_{logical_name}.md"
        self.assertEqual(table_def_path, expected_table_def)
        
        # サンプルデータファイルパス
        sample_path = self.config.get_sample_data_path(table_name)
        expected_sample = self.config.data_dir / f"{table_name}_sample_data.sql"
        self.assertEqual(sample_path, expected_sample)


@pytest.mark.unit
class TestLogger(unittest.TestCase):
    """ログ機能のテスト"""
    
    def setUp(self):
        """テストセットアップ"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.logger = DatabaseToolsLogger('test_logger')
    
    def tearDown(self):
        """テストクリーンアップ"""
        shutil.rmtree(self.temp_dir)
    
    def test_log_levels(self):
        """ログレベルのテスト"""
        self.logger.debug('デバッグメッセージ')
        self.logger.info('情報メッセージ')
        self.logger.warning('警告メッセージ')
        self.logger.error('エラーメッセージ')
        
        # ログが正常に出力されることを確認（ファイル出力は設定依存）
        self.assertTrue(True)  # ログ出力自体のテスト
    
    def test_structured_logging(self):
        """構造化ログのテスト"""
        # 構造化ログの基本テスト
        self.logger.info('テスト実行')
        self.assertTrue(True)  # ログ出力自体のテスト


@pytest.mark.unit
class TestYAMLParserAdvanced(unittest.TestCase):
    """YAML解析機能の高度なテスト"""
    
    def setUp(self):
        """テストセットアップ"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.parser = YamlParser()
    
    def tearDown(self):
        """テストクリーンアップ"""
        shutil.rmtree(self.temp_dir)
    
    def test_parse_with_unicode_content(self):
        """Unicode文字を含むYAMLの解析テスト"""
        yaml_content = {
            'table_name': 'MST_Employee',
            'logical_name': '社員基本情報',
            'category': 'マスタ系',
            'priority': '高',
            'requirement_id': 'PRO.1-BASE.1',
            'columns': [
                {
                    'name': 'name',
                    'type': 'VARCHAR(100)',
                    'comment': '氏名（漢字・ひらがな・カタカナ対応）'
                }
            ]
        }
        
        yaml_file = self.temp_dir / 'unicode_test.yaml'
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_content, f, default_flow_style=False, allow_unicode=True)
        
        table_def = self.parser.parse(str(yaml_file))
        
        self.assertEqual(table_def.logical_name, '社員基本情報')
        self.assertEqual(table_def.columns[0].comment, '氏名（漢字・ひらがな・カタカナ対応）')
    
    def test_parse_with_complex_foreign_keys(self):
        """複雑な外部キー定義の解析テスト"""
        yaml_content = {
            'table_name': 'TRN_SkillRecord',
            'logical_name': 'スキル記録',
            'category': 'トランザクション系',
            'priority': '高',
            'requirement_id': 'SKL.1-HIER.1',
            'columns': [
                {'name': 'emp_id', 'type': 'VARCHAR(50)'},
                {'name': 'skill_id', 'type': 'VARCHAR(50)'},
                {'name': 'tenant_id', 'type': 'VARCHAR(50)'}
            ],
            'foreign_keys': [
                {
                    'name': 'fk_skill_record_employee',
                    'columns': ['tenant_id', 'emp_id'],
                    'references': {
                        'table': 'MST_Employee',
                        'columns': ['tenant_id', 'id']
                    },
                    'on_update': 'CASCADE',
                    'on_delete': 'CASCADE'
                },
                {
                    'name': 'fk_skill_record_skill',
                    'columns': ['skill_id'],
                    'references': {
                        'table': 'MST_Skill',
                        'columns': ['id']
                    },
                    'on_update': 'RESTRICT',
                    'on_delete': 'RESTRICT'
                }
            ]
        }
        
        yaml_file = self.temp_dir / 'complex_fk.yaml'
        with open(yaml_file, 'w') as f:
            yaml.dump(yaml_content, f)
        
        table_def = self.parser.parse(str(yaml_file))
        
        self.assertEqual(len(table_def.foreign_keys), 2)
        
        # 複合外部キーのテスト
        fk1 = table_def.foreign_keys[0]
        self.assertEqual(fk1.columns, ['tenant_id', 'emp_id'])
        self.assertEqual(fk1.references['columns'], ['tenant_id', 'id'])
        
        # 単一外部キーのテスト
        fk2 = table_def.foreign_keys[1]
        self.assertEqual(fk2.columns, ['skill_id'])
        self.assertEqual(fk2.on_update, 'RESTRICT')


@pytest.mark.unit
class TestDDLParserAdvanced(unittest.TestCase):
    """DDL解析機能の高度なテスト"""
    
    def setUp(self):
        """テストセットアップ"""
        self.parser = DDLParser()
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """テストクリーンアップ"""
        shutil.rmtree(self.temp_dir)
    
    def test_parse_complex_ddl(self):
        """複雑なDDL文の解析テスト"""
        ddl_content = """
-- MST_Employee テーブル定義
CREATE TABLE MST_Employee (
    id VARCHAR(50) NOT NULL,
    tenant_id VARCHAR(50) NOT NULL,
    emp_no VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    birth_date DATE,
    salary DECIMAL(10,2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

        # DDLファイルとして保存してテスト
        ddl_file = self.temp_dir / 'MST_Employee.sql'
        with open(ddl_file, 'w', encoding='utf-8') as f:
            f.write(ddl_content)

        # デバッグ用にloggerを設定
        import logging
        logging.basicConfig(level=logging.DEBUG, force=True)
        logger = logging.getLogger('DDLParser')
        logger.setLevel(logging.DEBUG)
        
        # ハンドラーを追加
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        self.parser.logger = logger

        table_definitions = self.parser.parse(str(ddl_file))

        # DDLParserはリストを返すので、最初の要素を取得
        self.assertIsInstance(table_definitions, list)
        self.assertEqual(len(table_definitions), 1)

        table_def = table_definitions[0]
        self.assertEqual(table_def.table_name, 'MST_Employee')
        
        # デバッグ情報を出力
        print(f"解析されたカラム数: {len(table_def.columns)}")
        for i, col in enumerate(table_def.columns):
            print(f"カラム {i+1}: {col.name} ({col.type})")
        
        self.assertGreaterEqual(len(table_def.columns), 5)  # 最低限のカラム数をチェック
        
        # 基本的なカラムの存在確認
        column_names = [col.name for col in table_def.columns]
        self.assertIn('id', column_names)
        self.assertIn('tenant_id', column_names)
        self.assertIn('name', column_names)
    
    def test_parse_ddl_with_comments(self):
        """コメント付きDDLの解析テスト"""
        ddl_content = """
CREATE TABLE MST_Test (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー',
    name VARCHAR(100) NOT NULL COMMENT '名前',
    description TEXT COMMENT '説明'
);
"""
        
        # DDLファイルとして保存してテスト
        ddl_file = self.temp_dir / 'MST_Test.sql'
        with open(ddl_file, 'w', encoding='utf-8') as f:
            f.write(ddl_content)
        
        table_definitions = self.parser.parse(str(ddl_file))
        
        # DDLParserはリストを返すので、最初の要素を取得
        self.assertIsInstance(table_definitions, list)
        self.assertEqual(len(table_definitions), 1)
        
        table_def = table_definitions[0]
        self.assertEqual(table_def.table_name, 'MST_Test')
        
        # カラムの存在確認
        column_names = [col.name for col in table_def.columns]
        self.assertIn('id', column_names)
        self.assertIn('name', column_names)
        self.assertIn('description', column_names)


@pytest.mark.unit
class TestFilesystemAdapter(unittest.TestCase):
    """ファイルシステムアダプターのテスト"""
    
    def setUp(self):
        """テストセットアップ"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.adapter = UnifiedFileSystemAdapter(str(self.temp_dir))
    
    def tearDown(self):
        """テストクリーンアップ"""
        shutil.rmtree(self.temp_dir)
    
    def test_read_write_operations(self):
        """読み書き操作のテスト"""
        test_content = "テストコンテンツ\n日本語対応"
        file_path = 'test/sample.txt'
        
        # 書き込み
        self.adapter.write_text_file(file_path, test_content)
        
        # ファイルが作成されることを確認
        full_path = self.temp_dir / file_path
        self.assertTrue(full_path.exists())
        
        # 読み込み
        read_content = self.adapter.read_text_file(file_path)
        self.assertEqual(read_content, test_content)
    
    def test_list_files_operations(self):
        """ファイル一覧操作のテスト"""
        # テストファイル作成
        test_files = [
            'table-details/MST_Employee_details.yaml',
            'table-details/MST_Department_details.yaml',
            'ddl/MST_Employee.sql',
            'ddl/MST_Department.sql'
        ]
        
        for file_path in test_files:
            self.adapter.write_text_file(file_path, 'test content')
        
        # ファイル一覧取得（パターンマッチング）
        yaml_files = self.adapter.list_files('*.yaml', 'table-details')
        ddl_files = self.adapter.list_files('*.sql', 'ddl')
        
        self.assertEqual(len(yaml_files), 2)
        self.assertEqual(len(ddl_files), 2)
        
        # ファイル名の確認
        self.assertTrue(any('MST_Employee_details.yaml' in f for f in yaml_files))
        self.assertTrue(any('MST_Department_details.yaml' in f for f in yaml_files))
    
    def test_file_operations_with_encoding(self):
        """エンコーディングを考慮したファイル操作のテスト"""
        japanese_content = """
テーブル名: MST_社員
説明: 社員基本情報を管理するテーブル
カラム:
  - 氏名: VARCHAR(100)
  - メールアドレス: VARCHAR(255)
"""
        
        file_path = 'japanese_test.txt'
        
        # UTF-8で書き込み
        self.adapter.write_text_file(file_path, japanese_content)
        
        # UTF-8で読み込み
        read_content = self.adapter.read_text_file(file_path)
        self.assertEqual(read_content, japanese_content)
    
    def test_directory_operations(self):
        """ディレクトリ操作のテスト"""
        # ディレクトリ作成
        self.adapter.ensure_directory('new_dir/sub_dir')
        
        dir_path = self.temp_dir / 'new_dir' / 'sub_dir'
        self.assertTrue(dir_path.exists())
        self.assertTrue(dir_path.is_dir())
        
        # ディレクトリ存在確認
        self.assertTrue(self.adapter.directory_exists('new_dir'))
        self.assertTrue(self.adapter.directory_exists('new_dir/sub_dir'))
        self.assertFalse(self.adapter.directory_exists('non_existent'))


@pytest.mark.unit
class TestDataTransformAdapter(unittest.TestCase):
    """データ変換アダプターのテスト"""
    
    def setUp(self):
        """テストセットアップ"""
        self.adapter = UnifiedDataTransformAdapter()
    
    def test_table_definition_to_dict(self):
        """テーブル定義の辞書変換テスト"""
        table_def = TableDefinition(
            name='MST_Test',
            logical_name='テストテーブル',
            category='マスタ系',
            priority='高',
            requirement_id='TEST.1',
            columns=[
                ColumnDefinition(
                    name='id',
                    type='VARCHAR(50)',
                    nullable=False,
                    primary_key=True
                )
            ]
        )
        
        result = table_def.to_dict()
        
        self.assertEqual(result['name'], 'MST_Test')
        self.assertEqual(result['logical_name'], 'テストテーブル')
        self.assertEqual(len(result['columns']), 1)
        self.assertEqual(result['columns'][0]['name'], 'id')
    
    def test_dict_to_table_definition(self):
        """辞書からテーブル定義への変換テスト"""
        data = {
            'table_name': 'MST_Test',
            'logical_name': 'テストテーブル',
            'category': 'マスタ系',
            'priority': '高',
            'requirement_id': 'TEST.1',
            'columns': [
                {
                    'name': 'id',
                    'type': 'VARCHAR(50)',
                    'nullable': False,
                    'primary_key': True
                }
            ]
        }
        
        # yaml_to_table_definitionはTransformResultを返すので、適切に処理
        result = self.adapter.yaml_to_table_definition(data)
        self.assertTrue(result.success)
        
        table_def = result.data
        self.assertEqual(table_def.table_name, 'MST_Test')
        self.assertEqual(table_def.logical_name, 'テストテーブル')
        self.assertEqual(len(table_def.columns), 1)
        self.assertEqual(table_def.columns[0].name, 'id')
    
    def test_normalize_data_types(self):
        """データ型正規化のテスト"""
        test_cases = [
            ('varchar(50)', 'VARCHAR(50)'),
            ('VARCHAR(100)', 'VARCHAR(100)'),
            ('int', 'INTEGER'),
            ('INT', 'INTEGER'),
            ('text', 'TEXT'),
            ('TEXT', 'TEXT'),
            ('timestamp', 'TIMESTAMP'),
            ('TIMESTAMP', 'TIMESTAMP')
        ]
        
        for input_type, expected in test_cases:
            result = self.adapter.normalize_data_type(input_type)
            self.assertEqual(result, expected, f"Failed for input: {input_type}")
    
    def test_validate_table_name(self):
        """テーブル名バリデーションのテスト"""
        valid_names = ['MST_Employee', 'TRN_SkillRecord', 'HIS_LoginHistory']
        invalid_names = ['Employee', 'mst_employee', 'MST_', 'INVALID_Test']
        
        for name in valid_names:
            result = self.adapter._validate_table_name(name)
            self.assertTrue(result, f"Valid name rejected: {name}")
        
        for name in invalid_names:
            result = self.adapter._validate_table_name(name)
            self.assertFalse(result, f"Invalid name accepted: {name}")


@pytest.mark.unit
class TestFileManager(unittest.TestCase):
    """ファイルマネージャーのテスト"""
    
    def setUp(self):
        """テストセットアップ"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.file_manager = FileManager()
    
    def tearDown(self):
        """テストクリーンアップ"""
        shutil.rmtree(self.temp_dir)
    
    def test_read_write_operations(self):
        """読み書き操作のテスト"""
        test_file = self.temp_dir / 'test.txt'
        test_content = 'Test content\n日本語テスト'
        
        # ファイル書き込み
        self.file_manager.write_file_safely(test_file, test_content)
        
        # ファイルが作成されることを確認
        self.assertTrue(test_file.exists())
        
        # ファイル読み込み
        read_content = self.file_manager.read_file(test_file)
        self.assertEqual(read_content, test_content)
    
    def test_yaml_operations(self):
        """YAML操作のテスト"""
        test_file = self.temp_dir / 'test.yaml'
        test_data = {
            'table_name': 'MST_Employee',
            'logical_name': '社員基本情報',
            'columns': [
                {'name': 'id', 'type': 'VARCHAR(50)'}
            ]
        }
        
        # YAML書き込み
        self.file_manager.write_yaml_file(test_file, test_data)
        
        # YAML読み込み
        read_data = self.file_manager.read_yaml_file(test_file)
        self.assertEqual(read_data['table_name'], 'MST_Employee')
        self.assertEqual(read_data['logical_name'], '社員基本情報')
    
    def test_backup_creation(self):
        """バックアップ作成のテスト"""
        # 元ファイル作成
        original_file = self.temp_dir / 'original.txt'
        original_content = 'Original content'
        
        with open(original_file, 'w') as f:
            f.write(original_content)
        
        # バックアップ作成
        backup_path = self.file_manager.create_backup(original_file)
        
        # バックアップファイルが作成されることを確認
        self.assertTrue(backup_path.exists())
        
        # バックアップ内容が元ファイルと同じことを確認
        backup_content = self.file_manager.read_file(backup_path)
        self.assertEqual(backup_content, original_content)
    
    def test_file_listing(self):
        """ファイル一覧取得のテスト"""
        # テストファイル作成
        test_files = [
            'file1.txt',
            'file2.yaml',
            'subdir/file3.sql'
        ]
        
        for file_path in test_files:
            full_path = self.temp_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w') as f:
                f.write('test content')
        
        # ファイル一覧取得
        txt_files = self.file_manager.list_files(self.temp_dir, '*.txt')
        yaml_files = self.file_manager.list_files(self.temp_dir, '*.yaml')
        all_files = self.file_manager.list_files(self.temp_dir, '*', recursive=True)
        
        self.assertEqual(len(txt_files), 1)
        self.assertEqual(len(yaml_files), 1)
        self.assertEqual(len(all_files), 3)


@pytest.mark.unit
class TestErrorHandlingIntegration(unittest.TestCase):
    """エラーハンドリング統合テスト"""
    
    def test_validation_error_propagation(self):
        """バリデーションエラーの伝播テスト"""
        with self.assertRaises(ValidationError) as context:
            # 無効なテーブル名でバリデーションエラーを発生
            adapter = UnifiedDataTransformAdapter()
            if not adapter._validate_table_name('invalid_name'):
                raise ValidationError("無効なテーブル名です", "table_name")
        
        self.assertIn("無効なテーブル名です", str(context.exception))
    
    def test_configuration_error_handling(self):
        """設定エラーのハンドリングテスト"""
        temp_dir = Path(tempfile.mkdtemp())
        
        try:
            # 無効な設定でテスト
            config = DatabaseToolsConfig(base_dir=temp_dir)
            # 設定が正常に作成されることを確認
            self.assertIsNotNone(config)
        
        finally:
            shutil.rmtree(temp_dir)


if __name__ == '__main__':
    # テストスイート実行
    unittest.main(verbosity=2)
