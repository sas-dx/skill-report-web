"""
チェック定義 - 日本語名マッピング
"""
from typing import Dict

# チェック名と日本語名のマッピング
CHECK_NAME_MAPPING = {
    'basic_check': '基本チェック',
    'table_existence': 'テーブル存在確認',
    'column_consistency': 'カラム整合性',
    'data_type_consistency': 'データ型整合性',
    'foreign_key_consistency': '外部キー整合性',
    'index_consistency': 'インデックス整合性',
    'naming_convention': '命名規則チェック',
    'required_sections': '必須セクション確認',
    'yaml_format': 'YAMLフォーマット検証',
    'ddl_consistency': 'DDL整合性',
    'table_definition_consistency': 'テーブル定義整合性',
    'sample_data_consistency': 'サンプルデータ整合性'
}


def get_japanese_check_name(check_name: str) -> str:
    """
    チェック名の日本語表記を取得
    
    Args:
        check_name: 英語のチェック名
        
    Returns:
        日本語のチェック名（定義がない場合は英語名をそのまま返す）
    """
    return CHECK_NAME_MAPPING.get(check_name, check_name)


def get_all_check_definitions() -> Dict[str, Dict[str, str]]:
    """
    すべてのチェック定義を取得（簡易版）
    
    Returns:
        チェック定義の辞書
    """
    # 簡易的な定義を返す
    return {
        'table_existence': {
            'japanese_name': 'テーブル存在確認',
            'purpose': 'すべてのテーブルが必要なファイルに定義されているか確認',
            'check_content': 'テーブル一覧、エンティティ関連図、DDL、詳細YAMLの存在確認',
            'detected_issues': '定義漏れ、ファイル不足、不整合'
        },
        'column_consistency': {
            'japanese_name': 'カラム整合性',
            'purpose': 'カラム定義の一貫性を確認',
            'check_content': 'YAML、DDL、定義書間のカラム定義の一致確認',
            'detected_issues': 'カラム名不一致、データ型不一致、制約不一致'
        },
        'foreign_key_consistency': {
            'japanese_name': '外部キー整合性',
            'purpose': '外部キー制約の妥当性を確認',
            'check_content': '参照先テーブル・カラムの存在確認',
            'detected_issues': '参照先不在、循環参照、制約違反'
        },
        'naming_convention': {
            'japanese_name': '命名規則チェック',
            'purpose': '命名規則の準拠を確認',
            'check_content': 'テーブル名、カラム名の命名規則チェック',
            'detected_issues': '命名規則違反、不適切な名前'
        }
    }
