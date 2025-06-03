#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツール - Faker活用ユーティリティ

Fakerライブラリを活用したテストデータ生成機能を提供します。
※ Fakerが利用できない場合は、基本的なダミーデータを生成します。

対応要求仕様ID: PLT.2-DB.1, PLT.2-TOOL.1
"""

import random
import datetime
from typing import Any, List, Dict, Optional

try:
    from faker import Faker
    from faker.providers import BaseProvider
    FAKER_AVAILABLE = True
except ImportError:
    FAKER_AVAILABLE = False

from ..core.logger import EnhancedLogger


class JapaneseSkillProvider:
    """日本のスキル管理システム向けカスタムプロバイダー（Faker非依存版）"""
    
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
    
    # 日本の姓名
    last_names = ['田中', '佐藤', '鈴木', '高橋', '渡辺', '伊藤', '山本', '中村', '小林', '加藤']
    first_names = ['太郎', '花子', '次郎', '美咲', '健太', '由美', '翔太', '愛子', '大輔', '恵子']
    
    @classmethod
    def random_choice(cls, choices):
        """リストからランダムに選択"""
        return random.choice(choices)
    
    @classmethod
    def department_name(cls) -> str:
        """部署名を生成"""
        return cls.random_choice(cls.departments)
    
    @classmethod
    def skill_category(cls) -> str:
        """スキルカテゴリを生成"""
        return cls.random_choice(cls.skill_categories)
    
    @classmethod
    def programming_language(cls) -> str:
        """プログラミング言語を生成"""
        return cls.random_choice(cls.programming_languages)
    
    @classmethod
    def framework(cls) -> str:
        """フレームワークを生成"""
        return cls.random_choice(cls.frameworks)
    
    @classmethod
    def database(cls) -> str:
        """データベースを生成"""
        return cls.random_choice(cls.databases)
    
    @classmethod
    def japanese_name(cls) -> str:
        """日本人名を生成"""
        return f"{cls.random_choice(cls.last_names)} {cls.random_choice(cls.first_names)}"
    
    @classmethod
    def employee_code(cls) -> str:
        """従業員コードを生成"""
        return f"EMP{random.randint(1000, 9999)}"
    
    @classmethod
    def skill_code(cls) -> str:
        """スキルコードを生成"""
        return f"SKL{random.randint(100, 999)}"


class FakerUtils:
    """Faker活用ユーティリティクラス
    
    Fakerライブラリを使用したテストデータ生成機能を提供します。
    Fakerが利用できない場合は、基本的なダミーデータを生成します。
    """
    
    def __init__(self, locale: str = 'ja_JP', seed: Optional[int] = None, logger: EnhancedLogger = None):
        """初期化
        
        Args:
            locale (str): ロケール設定
            seed (Optional[int]): 乱数シード
            logger (EnhancedLogger, optional): ログ出力インスタンス
        """
        self.logger = logger or EnhancedLogger()
        self.provider = JapaneseSkillProvider()
        
        if FAKER_AVAILABLE:
            self.fake = Faker(locale)
            self.logger.info("Fakerライブラリを使用します")
        else:
            self.fake = None
            self.logger.warning("Fakerライブラリが利用できません。基本的なダミーデータを生成します")
        
        # シード設定
        if seed is not None:
            random.seed(seed)
            if FAKER_AVAILABLE and self.fake:
                Faker.seed(seed)
    
    def generate_by_type(self, data_type: str, **kwargs) -> Any:
        """データタイプに応じてデータを生成
        
        Args:
            data_type (str): データタイプ
            **kwargs: 追加パラメータ
            
        Returns:
            Any: 生成されたデータ
        """
        try:
            if FAKER_AVAILABLE and self.fake:
                return self._generate_with_faker(data_type, **kwargs)
            else:
                return self._generate_without_faker(data_type, **kwargs)
                
        except Exception as e:
            self.logger.error(f"データ生成エラー ({data_type}): {e}")
            return self._fallback_data(data_type)
    
    def _generate_with_faker(self, data_type: str, **kwargs) -> Any:
        """Fakerを使用してデータを生成"""
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
        elif data_type == 'date':
            start = kwargs.get('start_date', '-1y')
            end = kwargs.get('end_date', 'today')
            return self.fake.date_between(start_date=start, end_date=end)
        elif data_type == 'datetime':
            start = kwargs.get('start_date', '-1y')
            end = kwargs.get('end_date', 'now')
            return self.fake.date_time_between(start_date=start, end_date=end)
        elif data_type == 'integer':
            min_val = kwargs.get('min_value', 1)
            max_val = kwargs.get('max_value', 100)
            return self.fake.random_int(min_val, max_val)
        elif data_type == 'boolean':
            chance = kwargs.get('chance_of_getting_true', 50)
            return self.fake.boolean(chance_of_getting_true=chance)
        elif data_type == 'uuid':
            return self.fake.uuid4()
        else:
            return self._generate_custom_data(data_type, **kwargs)
    
    def _generate_without_faker(self, data_type: str, **kwargs) -> Any:
        """Faker非依存でデータを生成"""
        if data_type == 'name':
            return self.provider.japanese_name()
        elif data_type == 'email':
            name = self.provider.japanese_name().replace(' ', '').lower()
            return f"{name}@example.com"
        elif data_type == 'phone':
            return f"090-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        elif data_type == 'address':
            return f"東京都渋谷区{random.randint(1, 99)}-{random.randint(1, 99)}-{random.randint(1, 99)}"
        elif data_type == 'company':
            return f"株式会社{random.choice(['テスト', 'サンプル', 'デモ', 'テック'])}"
        elif data_type == 'text':
            return "サンプルテキストです。"
        elif data_type == 'word':
            return random.choice(['テスト', 'サンプル', 'デモ', 'データ'])
        elif data_type == 'sentence':
            return "これはサンプルの文章です。"
        elif data_type == 'date':
            today = datetime.date.today()
            days_ago = random.randint(0, 365)
            return today - datetime.timedelta(days=days_ago)
        elif data_type == 'datetime':
            now = datetime.datetime.now()
            hours_ago = random.randint(0, 8760)  # 1年分の時間
            return now - datetime.timedelta(hours=hours_ago)
        elif data_type == 'integer':
            min_val = kwargs.get('min_value', 1)
            max_val = kwargs.get('max_value', 100)
            return random.randint(min_val, max_val)
        elif data_type == 'boolean':
            chance = kwargs.get('chance_of_getting_true', 50)
            return random.randint(1, 100) <= chance
        elif data_type == 'uuid':
            import uuid
            return str(uuid.uuid4())
        else:
            return self._generate_custom_data(data_type, **kwargs)
    
    def _generate_custom_data(self, data_type: str, **kwargs) -> Any:
        """カスタムデータタイプの生成"""
        if data_type == 'department':
            return self.provider.department_name()
        elif data_type == 'skill':
            return self.provider.programming_language()
        elif data_type == 'employee_code':
            return self.provider.employee_code()
        elif data_type == 'skill_code':
            return self.provider.skill_code()
        else:
            return self._fallback_data(data_type)
    
    def _fallback_data(self, data_type: str) -> str:
        """フォールバックデータ"""
        return f"sample_{data_type}_{random.randint(1, 999)}"
    
    def set_seed(self, seed: int):
        """乱数シードを設定
        
        Args:
            seed (int): 乱数シード
        """
        random.seed(seed)
        if FAKER_AVAILABLE and self.fake:
            Faker.seed(seed)
    
    def get_locale_info(self) -> Dict[str, Any]:
        """ロケール情報を取得
        
        Returns:
            Dict[str, Any]: ロケール情報
        """
        if FAKER_AVAILABLE and self.fake:
            return {
                'locale': self.fake.locales,
                'providers': [provider.__name__ for provider in self.fake.providers],
                'faker_available': True
            }
        else:
            return {
                'locale': 'ja_JP (fallback)',
                'providers': ['JapaneseSkillProvider'],
                'faker_available': False
            }
