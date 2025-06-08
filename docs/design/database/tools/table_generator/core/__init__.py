#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツール - 基盤機能

このモジュールには、テーブル生成ツールの基盤機能が含まれています。

モジュール:
- logger: カラー出力対応ログ機能
- models: データクラス・列挙型定義
- config: 設定・定数管理

対応要求仕様ID: PLT.2-TOOL.1
"""

from .logger import EnhancedLogger, Colors, LogLevel
from shared.core.models import GenerationResult, TableDefinition
from shared.core.config import DatabaseToolsConfig as Config
from shared.core.exceptions import (
    DatabaseToolsException, ValidationError, FileOperationError,
    ModelConversionError, ParsingError, GenerationError,
    ConsistencyCheckError, ConfigurationError, SystemError,
    YamlParsingError, BackupError, ConversionError
)

__all__ = [
    'EnhancedLogger', 'Colors', 'LogLevel', 'GenerationResult', 'TableDefinition', 'Config',
    'DatabaseToolsException', 'ValidationError', 'FileOperationError',
    'ModelConversionError', 'ParsingError', 'GenerationError',
    'ConsistencyCheckError', 'ConfigurationError', 'SystemError',
    'YamlParsingError', 'BackupError', 'ConversionError'
]
