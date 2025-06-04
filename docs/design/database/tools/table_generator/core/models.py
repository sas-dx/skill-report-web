#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツール - データモデル

処理結果やデータ構造を定義するデータクラスを提供します。

対応要求仕様ID: PLT.2-TOOL.1
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum


@dataclass
class ProcessingResult:
    """処理結果を格納するデータクラス
    
    テーブル定義書生成やデータ生成の処理結果を格納します。
    
    Attributes:
        table_name (str): テーブル名
        logical_name (str): 論理名
        success (bool): 処理成功フラグ
        has_yaml (bool): YAMLファイル存在フラグ
        error_message (Optional[str]): エラーメッセージ
        warning_message (Optional[str]): 警告メッセージ
        generated_files (List[str]): 生成されたファイルのリスト
        processed_files (List[str]): 処理されたファイルのリスト
        errors (List[str]): エラーリスト
        data_count (Optional[int]): 生成されたデータ件数
    """
    table_name: str
    logical_name: str
    success: bool
    has_yaml: bool
    error_message: Optional[str] = None
    warning_message: Optional[str] = None
    generated_files: List[str] = None
    processed_files: List[str] = None
    errors: List[str] = None
    data_count: Optional[int] = None
    
    def __post_init__(self):
        """初期化後処理"""
        if self.generated_files is None:
            self.generated_files = []
        if self.processed_files is None:
            self.processed_files = []
        if self.errors is None:
            self.errors = []


@dataclass
class ColumnDefinition:
    """カラム定義データクラス
    
    テーブルのカラム定義情報を格納します。
    
    Attributes:
        name (str): カラム名
        logical (str): 論理名
        type (str): データ型
        length (Optional[int]): 長さ
        null (bool): NULL許可フラグ
        default (Optional[Any]): デフォルト値
        description (str): 説明
        primary (bool): プライマリキーフラグ
        unique (bool): ユニークフラグ
        data_generation (Optional[Dict[str, Any]]): データ生成設定
    """
    name: str
    logical: str
    data_type: str
    length: Optional[int] = None
    null: bool = True
    default: Optional[Any] = None
    description: str = ""
    primary: bool = False
    unique: bool = False
    data_generation: Optional[Dict[str, Any]] = None


@dataclass
class IndexDefinition:
    """インデックス定義データクラス
    
    Attributes:
        name (str): インデックス名
        columns (List[str]): 対象カラムリスト
        unique (bool): ユニークインデックスフラグ
        description (str): 説明
    """
    name: str
    columns: List[str]
    unique: bool = False
    description: str = ""


@dataclass
class ForeignKeyDefinition:
    """外部キー定義データクラス
    
    Attributes:
        name (str): 制約名
        column (str): カラム名
        reference_table (str): 参照テーブル名
        reference_column (str): 参照カラム名
        on_update (str): 更新時動作
        on_delete (str): 削除時動作
        description (str): 説明
    """
    name: str
    column: str
    reference_table: str
    reference_column: str
    on_update: str = "CASCADE"
    on_delete: str = "CASCADE"
    description: str = ""


@dataclass
class ConstraintDefinition:
    """制約定義データクラス
    
    Attributes:
        name (str): 制約名
        type (str): 制約種別
        condition (str): 制約条件
        description (str): 説明
    """
    name: str
    type: str
    condition: str = ""
    description: str = ""


@dataclass
class TableDefinition:
    """テーブル定義データクラス
    
    テーブル全体の定義情報を格納します。
    
    Attributes:
        table_name (str): テーブル名
        logical_name (str): 論理名
        category (str): カテゴリ
        overview (str): 概要
        business_columns (List[ColumnDefinition]): 業務カラム定義
        business_indexes (List[IndexDefinition]): 業務インデックス定義
        foreign_keys (List[ForeignKeyDefinition]): 外部キー定義
        business_constraints (List[ConstraintDefinition]): 業務制約定義
        sample_data (List[Dict[str, Any]]): サンプルデータ
        initial_data (List[Dict[str, Any]]): 初期値データ
        notes (List[str]): 特記事項
        business_rules (List[str]): 業務ルール
        revision_history (List[Dict[str, str]]): 改版履歴
        sample_data_config (Optional[Dict[str, Any]]): サンプルデータ設定
        data_generation_rules (Optional[Dict[str, Any]]): データ生成ルール
    """
    table_name: str
    logical_name: str
    category: str = ""
    overview: str = ""
    description: str = ""
    business_columns: List[ColumnDefinition] = None
    business_indexes: List[IndexDefinition] = None
    foreign_keys: List[ForeignKeyDefinition] = None
    business_constraints: List[ConstraintDefinition] = None
    sample_data: List[Dict[str, Any]] = None
    initial_data: List[Dict[str, Any]] = None
    notes: List[str] = None
    business_rules: List[str] = None
    revision_history: List[Dict[str, str]] = None
    sample_data_config: Optional[Dict[str, Any]] = None
    data_generation_rules: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """初期化後処理"""
        if self.business_columns is None:
            self.business_columns = []
        if self.business_indexes is None:
            self.business_indexes = []
        if self.foreign_keys is None:
            self.foreign_keys = []
        if self.business_constraints is None:
            self.business_constraints = []
        if self.sample_data is None:
            self.sample_data = []
        if self.initial_data is None:
            self.initial_data = []
        if self.notes is None:
            self.notes = []
        if self.business_rules is None:
            self.business_rules = []
        if self.revision_history is None:
            self.revision_history = []


class DataGenerationType(Enum):
    """データ生成タイプ列挙型"""
    PATTERN = "pattern"      # パターン生成
    FAKER = "faker"          # Faker使用
    CHOICE = "choice"        # 選択肢から選択
    REFERENCE = "reference"  # 外部キー参照
    RANGE = "range"          # 範囲指定
    FIXED = "fixed"          # 固定値
    SEQUENCE = "sequence"    # 連番


@dataclass
class DataGenerationConfig:
    """データ生成設定データクラス
    
    Attributes:
        type (DataGenerationType): 生成タイプ
        pattern (Optional[str]): パターン文字列
        start (Optional[int]): 開始値
        unique (bool): 一意性フラグ
        method (Optional[str]): Fakerメソッド名
        template (Optional[str]): テンプレート文字列
        choices (Optional[List[Any]]): 選択肢リスト
        weights (Optional[List[float]]): 重み付けリスト
        reference_table (Optional[str]): 参照テーブル名
        reference_column (Optional[str]): 参照カラム名
        filter_condition (Optional[str]): 参照先フィルタ条件
        min_value (Optional[Any]): 最小値
        max_value (Optional[Any]): 最大値
        distribution (Optional[str]): 分布タイプ
        mean (Optional[float]): 平均値
        std (Optional[float]): 標準偏差
        fixed_value (Optional[Any]): 固定値
        step (Optional[int]): ステップ値
    """
    type: DataGenerationType
    pattern: Optional[str] = None
    start: Optional[int] = None
    unique: bool = False
    method: Optional[str] = None
    template: Optional[str] = None
    choices: Optional[List[Any]] = None
    weights: Optional[List[float]] = None
    reference_table: Optional[str] = None
    reference_column: Optional[str] = None
    filter_condition: Optional[str] = None
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    distribution: Optional[str] = None
    mean: Optional[float] = None
    std: Optional[float] = None
    fixed_value: Optional[Any] = None
    step: Optional[int] = None
