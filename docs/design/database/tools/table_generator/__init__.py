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
from .generators.table_definition import TableDefinitionGenerator
from .data.yaml_data_loader import YamlDataLoader
from .data.data_factory import YamlDrivenDataFactory

__version__ = "1.0.0"
__author__ = "年間スキル報告書WEB化PJT"

__all__ = [
    'EnhancedLogger',
    'Colors', 
    'LogLevel',
    'ProcessingResult',
    'TableDefinitionGenerator',
    'YamlDataLoader',
    'YamlDrivenDataFactory'
]
