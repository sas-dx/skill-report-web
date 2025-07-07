#!/usr/bin/env python3
"""
データベースツール統合エントリーポイント v3.0
最終リファクタリング版 - シンプルで実用的なアーキテクチャ

使用例:
    python db_tools.py check --all
    python db_tools.py generate --table MST_Employee
    python db_tools.py validate --yaml-dir table-details
"""

import argparse
import sys
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
import json
from datetime import datetime

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseToolsConfig:
    """ツール設定管理"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.yaml_dir = self.base_dir / "table-details"
        self.ddl_dir = self.base_dir / "ddl"
        self.tables_dir = self.base_dir / "tables"
        
        # 必須セクション定義
        self.required_sections = [
            'revision_history',
            'overview',
            'notes',
            'rules'
        ]
        
        # 検証ルール
        self.validation_rules = {
            'overview_min_length': 50,
            'notes_min_items': 3,
            'rules_min_items': 3,
            'revision_history_min_items': 1
        }


class YAMLValidator:
    """YAML検証クラス"""
    
    def __init__(self, config: DatabaseToolsConfig):
        self.config = config
        
    def validate_file(self, yaml_path: Path) -> Dict[str, Any]:
        """YAMLファイルを検証"""
        result = {
            'file': str(yaml_path),
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            # 必須セクションチェック
            for section in self.config.required_sections:
                if section not in data:
                    result['errors'].append(f"必須セクション '{section}' が存在しません")
                    result['valid'] = False
                    
            # 詳細検証
            if 'overview' in data:
                overview = data['overview']
                if isinstance(overview, str) and len(overview.strip()) < self.config.validation_rules['overview_min_length']:
                    result['errors'].append(f"overview は最低{self.config.validation_rules['overview_min_length']}文字以上必要です")
                    result['valid'] = False
                    
            if 'notes' in data:
                notes = data['notes']
                if isinstance(notes, list) and len(notes) < self.config.validation_rules['notes_min_items']:
                    result['errors'].append(f"notes は最低{self.config.validation_rules['notes_min_items']}項目以上必要です")
                    result['valid'] = False
                    
            if 'rules' in data:
                rules = data['rules']
                if isinstance(rules, list) and len(rules) < self.config.validation_rules['rules_min_items']:
                    result['errors'].append(f"rules は最低{self.config.validation_rules['rules_min_items']}項目以上必要です")
                    result['valid'] = False
                    
        except yaml.YAMLError as e:
            result['errors'].append(f"YAML構文エラー: {e}")
            result['valid'] = False
        except Exception as e:
            result['errors'].append(f"ファイル読み込みエラー: {e}")
            result['valid'] = False
            
        return result
        
    def validate_directory(self, yaml_dir: Path) -> Dict[str, Any]:
        """ディレクトリ内の全YAMLファイルを検証"""
        results = {
            'total_files': 0,
            'valid_files': 0,
            'invalid_files': 0,
            'files': []
        }
        
        yaml_files = list(yaml_dir.glob("*.yaml")) + list(yaml_dir.glob("*.yml"))
        results['total_files'] = len(yaml_files)
        
        for yaml_file in yaml_files:
            file_result = self.validate_file(yaml_file)
            results['files'].append(file_result)
            
            if file_result['valid']:
                results['valid_files'] += 1
            else:
                results['invalid_files'] += 1
                
        return results


class TableGenerator:
    """テーブル生成クラス"""
    
    def __init__(self, config: DatabaseToolsConfig):
        self.config = config
        
    def generate_ddl(self, yaml_path: Path, output_path: Optional[Path] = None) -> bool:
        """YAMLからDDLを生成"""
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            table_name = data.get('table_name', 'UNKNOWN_TABLE')
            
            if not output_path:
                output_path = self.config.ddl_dir / f"{table_name}.sql"
                
            ddl_content = self._build_ddl(data)
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(ddl_content)
                
            logger.info(f"DDL生成完了: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"DDL生成エラー: {e}")
            return False
            
    def generate_markdown(self, yaml_path: Path, output_path: Optional[Path] = None) -> bool:
        """YAMLからMarkdown定義書を生成"""
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            table_name = data.get('table_name', 'UNKNOWN_TABLE')
            logical_name = data.get('logical_name', 'テーブル')
            
            if not output_path:
                output_path = self.config.tables_dir / f"テーブル定義書_{table_name}_{logical_name}.md"
                
            md_content = self._build_markdown(data)
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
                
            logger.info(f"Markdown生成完了: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Markdown生成エラー: {e}")
            return False
            
    def _build_ddl(self, data: Dict[str, Any]) -> str:
        """DDL文を構築"""
        table_name = data.get('table_name', 'UNKNOWN_TABLE')
        comment = data.get('comment', '')
        columns = data.get('columns', [])
        indexes = data.get('indexes', [])
        foreign_keys = data.get('foreign_keys', [])
        
        ddl_lines = [
            f"-- テーブル: {table_name}",
            f"-- 説明: {comment}",
            f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"CREATE TABLE {table_name} ("
        ]
        
        # カラム定義
        column_lines = []
        for col in columns:
            col_name = col.get('name', '')
            col_type = col.get('type', 'VARCHAR(255)')
            nullable = col.get('nullable', True)
            default = col.get('default', '')
            col_comment = col.get('comment', '')
            
            col_line = f"    {col_name} {col_type}"
            
            if not nullable:
                col_line += " NOT NULL"
                
            if default:
                col_line += f" DEFAULT {default}"
                
            if col_comment:
                col_line += f" -- {col_comment}"
                
            column_lines.append(col_line)
            
        ddl_lines.extend([line + "," if i < len(column_lines) - 1 else line for i, line in enumerate(column_lines)])
        ddl_lines.append(");")
        
        # インデックス
        if indexes:
            ddl_lines.append("")
            ddl_lines.append("-- インデックス")
            for idx in indexes:
                idx_name = idx.get('name', '')
                idx_columns = idx.get('columns', [])
                unique = idx.get('unique', False)
                
                idx_type = "UNIQUE INDEX" if unique else "INDEX"
                columns_str = ", ".join(idx_columns)
                ddl_lines.append(f"CREATE {idx_type} {idx_name} ON {table_name} ({columns_str});")
                
        # 外部キー
        if foreign_keys:
            ddl_lines.append("")
            ddl_lines.append("-- 外部キー制約")
            for fk in foreign_keys:
                fk_name = fk.get('name', '')
                fk_columns = fk.get('columns', [])
                ref_table = fk.get('references', {}).get('table', '')
                ref_columns = fk.get('references', {}).get('columns', [])
                
                fk_cols_str = ", ".join(fk_columns)
                ref_cols_str = ", ".join(ref_columns)
                ddl_lines.append(f"ALTER TABLE {table_name} ADD CONSTRAINT {fk_name}")
                ddl_lines.append(f"    FOREIGN KEY ({fk_cols_str}) REFERENCES {ref_table} ({ref_cols_str});")
                
        return "\n".join(ddl_lines)
        
    def _build_markdown(self, data: Dict[str, Any]) -> str:
        """Markdown定義書を構築"""
        table_name = data.get('table_name', 'UNKNOWN_TABLE')
        logical_name = data.get('logical_name', 'テーブル')
        comment = data.get('comment', '')
        overview = data.get('overview', '')
        columns = data.get('columns', [])
        
        md_lines = [
            f"# テーブル定義書: {table_name} ({logical_name})",
            "",
            "## エグゼクティブサマリー",
            "",
            overview if overview else f"このテーブル({table_name})の定義書です。",
            "",
            "## テーブル基本情報",
            "",
            f"- **物理名**: {table_name}",
            f"- **論理名**: {logical_name}",
            f"- **説明**: {comment}",
            f"- **生成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## カラム定義",
            "",
            "| カラム名 | データ型 | NULL許可 | デフォルト値 | 説明 |",
            "|----------|----------|----------|--------------|------|"
        ]
        
        for col in columns:
            col_name = col.get('name', '')
            col_type = col.get('type', '')
            nullable = "○" if col.get('nullable', True) else "×"
            default = col.get('default', '-')
            col_comment = col.get('comment', '')
            
            md_lines.append(f"| {col_name} | {col_type} | {nullable} | {default} | {col_comment} |")
            
        # 特記事項
        notes = data.get('notes', [])
        if notes:
            md_lines.extend([
                "",
                "## 特記事項",
                ""
            ])
            for note in notes:
                md_lines.append(f"- {note}")
                
        # 業務ルール
        rules = data.get('rules', [])
        if rules:
            md_lines.extend([
                "",
                "## 業務ルール",
                ""
            ])
            for rule in rules:
                md_lines.append(f"- {rule}")
                
        return "\n".join(md_lines)


class ConsistencyChecker:
    """整合性チェッククラス"""
    
    def __init__(self, config: DatabaseToolsConfig):
        self.config = config
        
    def check_all(self) -> Dict[str, Any]:
        """全体整合性チェック"""
        result = {
            'timestamp': datetime.now().isoformat(),
            'yaml_validation': {},
            'file_existence': {},
            'summary': {}
        }
        
        # YAML検証
        validator = YAMLValidator(self.config)
        result['yaml_validation'] = validator.validate_directory(self.config.yaml_dir)
        
        # ファイル存在チェック
        result['file_existence'] = self._check_file_existence()
        
        # サマリー作成
        result['summary'] = self._create_summary(result)
        
        return result
        
    def _check_file_existence(self) -> Dict[str, Any]:
        """ファイル存在チェック"""
        result = {
            'yaml_files': [],
            'ddl_files': [],
            'markdown_files': [],
            'missing_ddl': [],
            'missing_markdown': []
        }
        
        # YAMLファイル一覧
        yaml_files = list(self.config.yaml_dir.glob("*.yaml")) + list(self.config.yaml_dir.glob("*.yml"))
        result['yaml_files'] = [f.name for f in yaml_files]
        
        # 対応するDDL・Markdownファイルの存在チェック
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                table_name = data.get('table_name', '')
                logical_name = data.get('logical_name', '')
                
                # DDLファイルチェック
                ddl_file = self.config.ddl_dir / f"{table_name}.sql"
                if ddl_file.exists():
                    result['ddl_files'].append(ddl_file.name)
                else:
                    result['missing_ddl'].append(table_name)
                    
                # Markdownファイルチェック
                md_file = self.config.tables_dir / f"テーブル定義書_{table_name}_{logical_name}.md"
                if md_file.exists():
                    result['markdown_files'].append(md_file.name)
                else:
                    result['missing_markdown'].append(table_name)
                    
            except Exception as e:
                logger.warning(f"ファイル処理エラー {yaml_file}: {e}")
                
        return result
        
    def _create_summary(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """サマリー作成"""
        yaml_validation = result['yaml_validation']
        file_existence = result['file_existence']
        
        return {
            'total_yaml_files': yaml_validation['total_files'],
            'valid_yaml_files': yaml_validation['valid_files'],
            'invalid_yaml_files': yaml_validation['invalid_files'],
            'total_ddl_files': len(file_existence['ddl_files']),
            'missing_ddl_files': len(file_existence['missing_ddl']),
            'total_markdown_files': len(file_existence['markdown_files']),
            'missing_markdown_files': len(file_existence['missing_markdown']),
            'overall_health': 'GOOD' if yaml_validation['invalid_files'] == 0 and 
                             len(file_existence['missing_ddl']) == 0 and 
                             len(file_existence['missing_markdown']) == 0 else 'NEEDS_ATTENTION'
        }


def setup_argument_parser() -> argparse.ArgumentParser:
    """コマンドライン引数パーサー設定"""
    parser = argparse.ArgumentParser(
        description="データベースツール統合エントリーポイント v3.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 全体チェック
  python db_tools.py check --all
  
  # YAML検証
  python db_tools.py validate --yaml-dir table-details
  
  # テーブル生成
  python db_tools.py generate --table MST_Employee
  
  # 一括生成
  python db_tools.py generate --all
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='実行コマンド')
    
    # check コマンド
    check_parser = subparsers.add_parser('check', help='整合性チェック')
    check_parser.add_argument('--all', action='store_true', help='全体チェック実行')
    check_parser.add_argument('--output', help='結果出力ファイル')
    
    # validate コマンド
    validate_parser = subparsers.add_parser('validate', help='YAML検証')
    validate_parser.add_argument('--yaml-dir', help='YAMLディレクトリ')
    validate_parser.add_argument('--file', help='特定ファイル検証')
    
    # generate コマンド
    generate_parser = subparsers.add_parser('generate', help='ファイル生成')
    generate_parser.add_argument('--table', help='特定テーブル生成')
    generate_parser.add_argument('--all', action='store_true', help='全テーブル生成')
    generate_parser.add_argument('--ddl-only', action='store_true', help='DDLのみ生成')
    generate_parser.add_argument('--markdown-only', action='store_true', help='Markdownのみ生成')
    
    # 共通オプション
    parser.add_argument('--verbose', '-v', action='store_true', help='詳細ログ')
    parser.add_argument('--quiet', '-q', action='store_true', help='エラーのみ出力')
    
    return parser


def main():
    """メイン関数"""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # ログレベル設定
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
        
    config = DatabaseToolsConfig()
    
    try:
        if args.command == 'check':
            checker = ConsistencyChecker(config)
            result = checker.check_all()
            
            # 結果表示
            print("🔍 整合性チェック結果")
            print("=" * 50)
            summary = result['summary']
            print(f"📊 YAML検証: {summary['valid_yaml_files']}/{summary['total_yaml_files']} 成功")
            print(f"📄 DDLファイル: {summary['total_ddl_files']}個存在, {summary['missing_ddl_files']}個不足")
            print(f"📝 Markdownファイル: {summary['total_markdown_files']}個存在, {summary['missing_markdown_files']}個不足")
            print(f"🎯 総合評価: {summary['overall_health']}")
            
            # 詳細エラー表示
            if summary['invalid_yaml_files'] > 0:
                print("\n❌ YAML検証エラー:")
                for file_result in result['yaml_validation']['files']:
                    if not file_result['valid']:
                        print(f"  {file_result['file']}:")
                        for error in file_result['errors']:
                            print(f"    - {error}")
                            
            # 結果ファイル出力
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"\n📁 結果をファイルに出力: {args.output}")
                
        elif args.command == 'validate':
            validator = YAMLValidator(config)
            
            if args.file:
                result = validator.validate_file(Path(args.file))
                if result['valid']:
                    print(f"✅ 検証成功: {args.file}")
                else:
                    print(f"❌ 検証失敗: {args.file}")
                    for error in result['errors']:
                        print(f"  - {error}")
            else:
                yaml_dir = Path(args.yaml_dir) if args.yaml_dir else config.yaml_dir
                result = validator.validate_directory(yaml_dir)
                print(f"📊 検証結果: {result['valid_files']}/{result['total_files']} 成功")
                
        elif args.command == 'generate':
            generator = TableGenerator(config)
            
            if args.table:
                # 特定テーブル生成
                yaml_file = config.yaml_dir / f"テーブル詳細定義YAML_{args.table}.yaml"
                if not yaml_file.exists():
                    print(f"❌ YAMLファイルが見つかりません: {yaml_file}")
                    return 1
                    
                success = True
                if not args.markdown_only:
                    success &= generator.generate_ddl(yaml_file)
                if not args.ddl_only:
                    success &= generator.generate_markdown(yaml_file)
                    
                if success:
                    print(f"✅ {args.table} の生成完了")
                else:
                    print(f"❌ {args.table} の生成失敗")
                    
            elif args.all:
                # 全テーブル生成
                yaml_files = list(config.yaml_dir.glob("*.yaml")) + list(config.yaml_dir.glob("*.yml"))
                success_count = 0
                error_count = 0
                
                for yaml_file in yaml_files:
                    try:
                        ddl_success = True
                        md_success = True
                        
                        if not args.markdown_only:
                            ddl_success = generator.generate_ddl(yaml_file)
                        if not args.ddl_only:
                            md_success = generator.generate_markdown(yaml_file)
                            
                        if ddl_success and md_success:
                            success_count += 1
                            print(f"✅ {yaml_file.name}")
                        else:
                            error_count += 1
                            print(f"❌ {yaml_file.name}")
                            
                    except Exception as e:
                        error_count += 1
                        print(f"❌ {yaml_file.name}: {e}")
                        
                print(f"\n📊 生成結果: 成功 {success_count}件, エラー {error_count}件")
                
        else:
            parser.print_help()
            return 1
            
        return 0
        
    except Exception as e:
        logger.error(f"実行エラー: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
