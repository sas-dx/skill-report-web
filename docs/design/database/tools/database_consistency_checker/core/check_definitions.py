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
    ),
    "constraint_consistency": CheckDefinition(
        japanese_name="制約整合性",
        description="DDLとYAMLファイル間での制約定義の詳細整合性確認",
        purpose="CHECK制約、UNIQUE制約、PRIMARY KEY制約、インデックス制約の整合性確認",
        check_content="CHECK制約の条件一致、UNIQUE制約の対象カラム一致、PRIMARY KEY制約の整合性、インデックス制約の詳細比較",
        detected_issues="制約条件不一致、制約対象カラム相違、制約定義漏れ、インデックス設定不整合"
    ),
    "yaml_format_consistency": CheckDefinition(
        japanese_name="YAMLフォーマット整合性",
        description="テーブル定義詳細YAMLファイルの標準テンプレート準拠確認",
        purpose="YAMLファイルが標準テンプレートに準拠しているかの確認",
        check_content="必須セクション存在確認、セクション内構造確認、データ型妥当性確認、テンプレート準拠確認",
        detected_issues="必須セクション不足、構造不整合、データ型不正、テンプレート非準拠"
    ),
    "fix_suggestions": CheckDefinition(
        japanese_name="修正提案",
        description="検出された問題に対する具体的な修正方法の提案",
        purpose="問題の自動修正提案と修正コマンド生成による開発効率向上",
        check_content="テーブル定義修正提案、カラム定義修正提案、制約修正提案、自動修正コマンド生成",
        detected_issues="修正方法不明、手動修正の手間、修正漏れリスク"
    ),
    "multitenant_compliance": CheckDefinition(
        japanese_name="マルチテナント対応",
        description="全テーブルのマルチテナント対応要件準拠確認",
        purpose="tenant_id必須確認、テナント用インデックス・制約確認",
        check_content="tenant_idカラム存在確認、テナント用インデックス確認、テナント制約確認、外部キーテナント整合性確認",
        detected_issues="tenant_id不足、テナントインデックス不足、テナント制約不備、テナント間参照問題"
    ),
    "requirement_traceability": CheckDefinition(
        japanese_name="要求仕様ID追跡",
        description="全テーブル・カラムの要求仕様ID網羅性・妥当性確認",
        purpose="要求仕様IDとテーブル・カラムの対応関係確認によるトレーサビリティ確保",
        check_content="要求仕様ID網羅性確認、要求仕様ID妥当性確認、要求仕様ID形式チェック、未割当項目検出",
        detected_issues="要求仕様ID未割当、要求仕様ID不正、要求仕様ID重複、トレーサビリティ不備"
    ),
    "performance_impact": CheckDefinition(
        japanese_name="パフォーマンス影響分析",
        description="インデックス設計とクエリパフォーマンスの影響分析",
        purpose="インデックスカバレッジ分析、クエリパフォーマンス予測、データ量影響分析",
        check_content="インデックスカバレッジ分析、クエリパフォーマンス予測、データ量影響分析、スロークエリ予測",
        detected_issues="インデックス不足、パフォーマンス劣化予測、データ量超過リスク、クエリ最適化不備"
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
