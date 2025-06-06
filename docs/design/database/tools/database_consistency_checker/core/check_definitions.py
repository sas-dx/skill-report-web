"""
チェック定義とメタデータ
"""
from typing import Dict, NamedTuple


class CheckDefinition(NamedTuple):
    """チェック定義"""
    japanese_name: str
    description: str
    purpose: str
    check_content: str
    detected_issues: str


# チェック名の日本語マッピングと詳細情報
CHECK_DEFINITIONS: Dict[str, CheckDefinition] = {
    "table_existence": CheckDefinition(
        japanese_name="テーブル存在確認",
        description="データベース設計の4つのソース間でテーブル定義の一貫性を確認",
        purpose="設計ドキュメント間でのテーブル定義の一貫性を確認",
        check_content="テーブル一覧.md、entity_relationships.yaml、DDLファイル、詳細YAMLファイルの4つのソース間でテーブルが正しく定義されているかを確認",
        detected_issues="定義漏れ、不整合、命名ミス"
    ),
    "orphaned_files": CheckDefinition(
        japanese_name="孤立ファイル検出",
        description="テーブル一覧に記載されていない不要なファイルを検出",
        purpose="不要なファイルや管理対象外ファイルの検出",
        check_content="テーブル一覧に記載されていないDDLファイルや詳細YAMLファイルを検出",
        detected_issues="削除し忘れたファイル、テーブル一覧への追加漏れ"
    ),
    "column_consistency": CheckDefinition(
        japanese_name="カラム定義整合性",
        description="DDLとYAMLファイル間でのカラム定義の整合性確認",
        purpose="DDLとYAMLファイル間でのカラム定義の整合性確認",
        check_content="データ型、長さ、NULL制約、デフォルト値、ENUM値、インデックス、制約の一致確認",
        detected_issues="型不一致、制約の相違、定義漏れ"
    ),
    "foreign_key_consistency": CheckDefinition(
        japanese_name="外部キー整合性",
        description="エンティティ関連図とDDL間での外部キー定義の整合性確認",
        purpose="エンティティ関連図とDDL間での外部キー定義の整合性確認",
        check_content="外部キー名、参照先テーブル・カラム、ON DELETE/UPDATE設定の一致確認",
        detected_issues="参照先不整合、制約設定の相違、定義漏れ"
    ),
    "data_type_consistency": CheckDefinition(
        japanese_name="データ型整合性",
        description="DDLとYAMLファイル間でのデータ型定義の詳細整合性確認",
        purpose="DDLとYAMLファイル間でのデータ型定義の詳細整合性確認",
        check_content="データ型の詳細比較、長さ・精度・スケールの一致確認、ENUM値の整合性確認",
        detected_issues="データ型不一致、長さ・精度の相違、ENUM値の不整合"
    )
}


def get_japanese_check_name(english_name: str) -> str:
    """英語のチェック名を日本語に変換"""
    definition = CHECK_DEFINITIONS.get(english_name)
    return definition.japanese_name if definition else english_name


def get_check_description(english_name: str) -> str:
    """チェックの説明を取得"""
    definition = CHECK_DEFINITIONS.get(english_name)
    return definition.description if definition else ""


def get_check_definition(english_name: str) -> CheckDefinition:
    """チェック定義を取得"""
    return CHECK_DEFINITIONS.get(english_name, CheckDefinition(
        japanese_name=english_name,
        description="",
        purpose="",
        check_content="",
        detected_issues=""
    ))


def get_all_check_definitions() -> Dict[str, CheckDefinition]:
    """全てのチェック定義を取得"""
    return CHECK_DEFINITIONS.copy()
