#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル定義書・DDL・サンプルデータ生成ツール群

このパッケージには、テーブル定義書の生成、DDL生成、
YAML駆動サンプルデータ生成機能が含まれています。

主要モジュール:
- core: 基盤機能（ログ、モデル、設定）
- generators: 生成機能（テーブル定義書、DDL、データ）
- data: データ生成機能（YAML駆動、ファクトリ）
- utils: ユーティリティ機能（ファイル操作、YAML読み込み）

対応要求仕様ID: PLT.2-DB.1, PLT.2-TOOL.1
"""

from .core.logger import EnhancedLogger, Colors, LogLevel
from .core.models import ProcessingResult
from .core.config import Config
from .generators.table_definition_generator import TableDefinitionGenerator
from .generators.ddl_generator import DDLGenerator
from .generators.common_columns import CommonColumns
from .data.yaml_data_loader import YamlDataLoader
from .data.faker_utils import BasicDataUtils, FakerUtils
from .utils.yaml_loader import YamlLoader
from .utils.file_utils import FileUtils
from .utils.sql_utils import SqlUtils

__version__ = "1.0.0"
__author__ = "年間スキル報告書WEB化PJT"

__all__ = [
    'EnhancedLogger',
    'Colors', 
    'LogLevel',
    'ProcessingResult',
    'Config',
    'TableDefinitionGenerator',
    'DDLGenerator',
    'CommonColumns',
    'YamlDataLoader',
    'BasicDataUtils',
    'FakerUtils',
    'YamlLoader',
    'FileUtils',
    'SqlUtils'
]
