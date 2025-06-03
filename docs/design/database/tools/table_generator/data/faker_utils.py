#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツール - Faker活用ユーティリティ

Fakerライブラリを活用したテストデータ生成機能を提供します。

対応要求仕様ID: PLT.2-DB.1, PLT.2-TOOL.1
"""

import random
from typing import Any, List, Dict, Optional
from faker import Faker
from faker.providers import BaseProvider
from ..core.logger import EnhancedLogger


class JapaneseSkillProvider(BaseProvider):
    """日本のスキル管理システム向けカスタムプロバイダー"""
    
    # 部署名
    departments = [
        '開発部', 'システム部', '業務部', '管理部', '営業部',
        '企画部', '人事部', '総務部', '経理部', '法務部'
    ]
    
    # スキルカテゴリ
    skill_categories = [
        'プログラミング言語', 'フレームワーク', 'データベース', 'インフラ',
        'クラウド', 'ツール', 'マネジメント', 'ビジネス', 'コミュニケーション'
    ]
    
    # プログラミング言語
    programming_languages = [
        'Java', 'Python', 'JavaScript', 'TypeScript', 'C#', 'C++', 'Go',
        'Rust', 'PHP', 'Ruby', 'Kotlin', 'Swift', 'Scala', 'R'
    ]
    
    # フレームワーク
    frameworks = [
        'Spring Boot', 'Django', 'Flask', 'React', 'Vue.js', 'Angular',
        'Express.js', 'Laravel', 'Ruby on Rails', '.NET Core'
    ]
    
    # データベース
    databases = [
        'MySQL', 'PostgreSQL', 'Oracle', 'SQL Server', 'MongoDB',
        'Redis', 'Elasticsearch', 'DynamoDB', 'Cassandra'
    ]
    
    # クラウドサービス
    cloud_services = [
        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform',
        'CloudFormation', 'Ansible', 'Jenkins', 'GitLab CI/CD'
    ]
    
    # プロジェクト名
    project_names = [
        '顧客管理システム', '在庫管理システム', 'ECサイト', '人事システム',
        '会計システム', 'CRMシステム', 'ERPシステム', 'BIシステム',
        'モバイルアプリ', 'Webアプリケーション'
    ]
    
    def department_name(self) -> str:
        """部署名を生成"""
        return self.random_element(self.departments)
    
    def skill_category(self) -> str:
        """スキルカテゴリを生成"""
        return self.random_element(self.skill_categories)
    
    def programming_language(self) -> str:
        """プログラミング言語を生成"""
        return self.random_element(self.programming_languages)
    
    def framework(self) -> str:
        """フレームワークを生成"""
        return self.random_element(self.frameworks)
    
    def database(self) -> str:
        """データベースを生成"""
        return self.random_element(self.databases)
    
    def cloud_service(self) -> str:
        """クラウドサービスを生成"""
        return self.random_element(self.cloud_services)
    
    def project_name(self) -> str:
        """プロジェクト名を生成"""
        return self.random_element(self.project_names)
    
    def skill_name(self) -> str:
        """スキル名を生成（カテゴリに応じて）"""
        category = self.skill_category()
        
        if category == 'プログラミング言語':
            return self.programming_language()
        elif category == 'フレームワーク':
            return self.framework()
        elif category == 'データベース':
            return self.database()
        elif category == 'クラウド':
            return self.cloud_service()
        else:
            return self.random_element([
                'プロジェクト管理', 'チームリーダーシップ', 'アーキテクチャ設計',
                '要件定義', 'テスト設計', 'セキュリティ', 'パフォーマンス最適化'
            ])
    
    def employee_code(self) -> str:
        """従業員コードを生成"""
        return f"EMP{self.random_int(1000, 9999)}"
    
    def skill_code(self) -> str:
        """スキルコードを生成"""
        return f"SKL{self.random_int(100, 999)}"
    
    def project_code(self) -> str:
        """プロジェクトコードを生成"""
        return f"PRJ{self.random_int(1000, 9999)}"


class FakerUtils:
    """Faker活用ユーティリティクラス
    
    Fakerライブラリを使用したテストデータ生成機能を提供します。
    日本語対応とカスタムプロバイダーを含みます。
    """
    
    def __init__(self, locale: str = 'ja_JP', seed: Optional[int] = None, logger: EnhancedLogger = None):
        """初期化
        
        Args:
            locale (str): ロケール設定
            seed (Optional[int]): 乱数シード
            logger (EnhancedLogger, optional): ログ出力インスタンス
        """
        self.logger = logger or EnhancedLogger()
        self.fake = Faker(locale)
        
        # カスタムプロバイダーを追加
        self.fake.add_provider(JapaneseSkillProvider)
        
        # シード設定
        if seed is not None:
            Faker.seed(seed)
            random.seed(seed)
    
    def generate_person_data(self) -> Dict[str, Any]:
        """個人データを生成
        
        Returns:
            Dict[str, Any]: 個人データ辞書
        """
        return {
            'name': self.fake.name(),
            'name_kana': self.fake.kana_name(),
            'email': self.fake.email(),
            'phone': self.fake.phone_number(),
            'address': self.fake.address(),
            'birth_date': self.fake.date_of_birth(minimum_age=22, maximum_age=65),
            'gender': self.fake.random_element(['男性', '女性']),
            'employee_code': self.fake.employee_code()
        }
    
    def generate_company_data(self) -> Dict[str, Any]:
        """会社データを生成
        
        Returns:
            Dict[str, Any]: 会社データ辞書
        """
        return {
            'company_name': self.fake.company(),
            'department': self.fake.department_name(),
            'position': self.fake.job(),
            'hire_date': self.fake.date_between(start_date='-10y', end_date='today'),
            'salary': self.fake.random_int(3000000, 12000000, step=100000)
        }
    
    def generate_skill_data(self) -> Dict[str, Any]:
        """スキルデータを生成
        
        Returns:
            Dict[str, Any]: スキルデータ辞書
        """
        return {
            'skill_name': self.fake.skill_name(),
            'skill_category': self.fake.skill_category(),
            'skill_code': self.fake.skill_code(),
            'skill_level': self.fake.random_element([1, 2, 3, 4]),
            'experience_years': self.fake.random_int(0, 20),
            'certification': self.fake.boolean(chance_of_getting_true=30)
        }
    
    def generate_project_data(self) -> Dict[str, Any]:
        """プロジェクトデータを生成
        
        Returns:
            Dict[str, Any]: プロジェクトデータ辞書
        """
        start_date = self.fake.date_between(start_date='-2y', end_date='today')
        end_date = self.fake.date_between(start_date=start_date, end_date='+1y')
        
        return {
            'project_name': self.fake.project_name(),
            'project_code': self.fake.project_code(),
            'start_date': start_date,
            'end_date': end_date,
            'budget': self.fake.random_int(1000000, 100000000, step=1000000),
            'status': self.fake.random_element(['計画中', '進行中', '完了', '中止']),
            'priority': self.fake.random_element([1, 2, 3, 4, 5]),
            'description': self.fake.text(max_nb_chars=200)
        }
    
    def generate_evaluation_data(self) -> Dict[str, Any]:
        """評価データを生成
        
        Returns:
            Dict[str, Any]: 評価データ辞書
        """
        return {
            'evaluation_date': self.fake.date_between(start_date='-1y', end_date='today'),
            'score': self.fake.random_int(1, 5),
            'comment': self.fake.text(max_nb_chars=500),
            'goals': self.fake.text(max_nb_chars=300),
            'achievements': self.fake.text(max_nb_chars=300)
        }
    
    def generate_by_type(self, data_type: str, **kwargs) -> Any:
        """データタイプに応じてデータを生成
        
        Args:
            data_type (str): データタイプ
            **kwargs: 追加パラメータ
            
        Returns:
            Any: 生成されたデータ
        """
        try:
            # 基本データタイプ
            if data_type == 'name':
                return self.fake.name()
            elif data_type == 'email':
                return self.fake.email()
            elif data_type == 'phone':
                return self.fake.phone_number()
            elif data_type == 'address':
                return self.fake.address()
            elif data_type == 'company':
                return self.fake.company()
            elif data_type == 'text':
                max_chars = kwargs.get('max_nb_chars', 100)
                return self.fake.text(max_nb_chars=max_chars)
            elif data_type == 'word':
                return self.fake.word()
            elif data_type == 'sentence':
                return self.fake.sentence()
            
            # 日付・時刻
            elif data_type == 'date':
                start = kwargs.get('start_date', '-1y')
                end = kwargs.get('end_date', 'today')
                return self.fake.date_between(start_date=start, end_date=end)
            elif data_type == 'datetime':
                start = kwargs.get('start_date', '-1y')
                end = kwargs.get('end_date', 'now')
                return self.fake.date_time_between(start_date=start, end_date=end)
            elif data_type == 'time':
                return self.fake.time()
            
            # 数値
            elif data_type == 'integer':
                min_val = kwargs.get('min_value', 1)
                max_val = kwargs.get('max_value', 100)
                return self.fake.random_int(min_val, max_val)
            elif data_type == 'float':
                min_val = kwargs.get('min_value', 0.0)
                max_val = kwargs.get('max_value', 100.0)
                return round(self.fake.pyfloat(min_value=min_val, max_value=max_val), 2)
            elif data_type == 'decimal':
                min_val = kwargs.get('min_value', 0.0)
                max_val = kwargs.get('max_value', 100.0)
                return round(self.fake.pyfloat(min_value=min_val, max_value=max_val), 2)
            
            # ブール値
            elif data_type == 'boolean':
                chance = kwargs.get('chance_of_getting_true', 50)
                return self.fake.boolean(chance_of_getting_true=chance)
            
            # UUID
            elif data_type == 'uuid':
                return self.fake.uuid4()
            
            # カスタムデータタイプ
            elif data_type == 'department':
                return self.fake.department_name()
            elif data_type == 'skill':
                return self.fake.skill_name()
            elif data_type == 'project':
                return self.fake.project_name()
            elif data_type == 'employee_code':
                return self.fake.employee_code()
            elif data_type == 'skill_code':
                return self.fake.skill_code()
            elif data_type == 'project_code':
                return self.fake.project_code()
            
            else:
                self.logger.warning(f"未対応のデータタイプ: {data_type}")
                return self.fake.word()
                
        except Exception as e:
            self.logger.error(f"データ生成エラー ({data_type}): {e}")
            return None
    
    def generate_choice_data(self, choices: List[Any], weights: Optional[List[float]] = None) -> Any:
        """選択肢からデータを生成
        
        Args:
            choices (List[Any]): 選択肢リスト
            weights (Optional[List[float]]): 重み付けリスト
            
        Returns:
            Any: 選択されたデータ
        """
        try:
            if weights and len(weights) == len(choices):
                return random.choices(choices, weights=weights)[0]
            else:
                return self.fake.random_element(choices)
                
        except Exception as e:
            self.logger.error(f"選択肢データ生成エラー: {e}")
            return choices[0] if choices else None
    
    def generate_pattern_data(self, pattern: str, **kwargs) -> str:
        """パターンに基づいてデータを生成
        
        Args:
            pattern (str): パターン文字列
            **kwargs: 追加パラメータ
            
        Returns:
            str: 生成されたデータ
        """
        try:
            if pattern == 'uuid':
                return str(self.fake.uuid4())
            elif pattern.startswith('EMP'):
                return self.fake.employee_code()
            elif pattern.startswith('SKL'):
                return self.fake.skill_code()
            elif pattern.startswith('PRJ'):
                return self.fake.project_code()
            elif '{' in pattern:
                # フォーマット文字列の場合
                start = kwargs.get('start', 1)
                return pattern.format(self.fake.random_int(start, start + 9999))
            else:
                return pattern
                
        except Exception as e:
            self.logger.error(f"パターンデータ生成エラー ({pattern}): {e}")
            return pattern
    
    def generate_sequence_data(self, start: int = 1, step: int = 1, current_count: int = 0) -> int:
        """連番データを生成
        
        Args:
            start (int): 開始値
            step (int): ステップ値
            current_count (int): 現在のカウント
            
        Returns:
            int: 連番値
        """
        return start + (current_count * step)
    
    def set_seed(self, seed: int):
        """乱数シードを設定
        
        Args:
            seed (int): 乱数シード
        """
        Faker.seed(seed)
        random.seed(seed)
    
    def get_locale_info(self) -> Dict[str, Any]:
        """ロケール情報を取得
        
        Returns:
            Dict[str, Any]: ロケール情報
        """
        return {
            'locale': self.fake.locales,
            'providers': [provider.__name__ for provider in self.fake.providers]
        }
