"""
レポート管理ユーティリティ
"""
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Tuple


class ReportManager:
    """レポートファイル管理クラス"""
    
    def __init__(self, base_dir: str = "", report_dir: str = "reports"):
        """
        レポートマネージャー初期化
        
        Args:
            base_dir: ベースディレクトリ
            report_dir: レポートディレクトリ名
        """
        if base_dir:
            self.base_path = Path(base_dir)
        else:
            # ツールのルートディレクトリを自動検出
            self.base_path = Path(__file__).parent.parent
        
        self.report_dir = self.base_path / report_dir
        self.ensure_report_directory()
    
    def ensure_report_directory(self):
        """レポートディレクトリの作成"""
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
        # サブディレクトリも作成
        (self.report_dir / "daily").mkdir(exist_ok=True)
        (self.report_dir / "manual").mkdir(exist_ok=True)
        (self.report_dir / "archive").mkdir(exist_ok=True)
    
    def generate_report_filename(
        self, 
        report_type: str = "consistency_report",
        extension: str = "md",
        custom_prefix: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> str:
        """
        レポートファイル名を生成
        
        Args:
            report_type: レポート種別
            extension: ファイル拡張子
            custom_prefix: カスタムプレフィックス
            timestamp: タイムスタンプ（指定しない場合は現在時刻）
            
        Returns:
            生成されたファイル名
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # タイムスタンプ文字列生成
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        
        # プレフィックス決定
        if custom_prefix:
            prefix = f"{timestamp_str}_{custom_prefix}"
        else:
            prefix = timestamp_str
        
        # ファイル名生成
        filename = f"{prefix}_{report_type}.{extension}"
        
        # ユニーク性保証（同一秒での実行時の連番対応）
        counter = 1
        original_filename = filename
        while (self.report_dir / filename).exists():
            base_name = original_filename.rsplit('.', 1)[0]
            filename = f"{base_name}_{counter:02d}.{extension}"
            counter += 1
        
        return filename
    
    def get_report_path(
        self, 
        report_type: str = "consistency_report",
        extension: str = "md",
        custom_prefix: Optional[str] = None,
        subdirectory: Optional[str] = None
    ) -> Path:
        """
        レポートファイルパスを取得
        
        Args:
            report_type: レポート種別
            extension: ファイル拡張子
            custom_prefix: カスタムプレフィックス
            subdirectory: サブディレクトリ（daily, manual, archive等）
            
        Returns:
            レポートファイルパス
        """
        filename = self.generate_report_filename(
            report_type=report_type,
            extension=extension,
            custom_prefix=custom_prefix
        )
        
        if subdirectory:
            report_path = self.report_dir / subdirectory / filename
            # サブディレクトリが存在しない場合は作成
            report_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            report_path = self.report_dir / filename
        
        return report_path
    
    def create_latest_link(self, report_path: Path, link_name: str = "latest_consistency_report.md"):
        """
        最新レポートへのリンクを作成
        
        Args:
            report_path: レポートファイルパス
            link_name: リンクファイル名
        """
        link_path = self.report_dir / link_name
        
        # 既存のリンクを削除
        if link_path.exists() or link_path.is_symlink():
            link_path.unlink()
        
        try:
            # シンボリックリンクを作成（相対パス）
            relative_path = report_path.relative_to(self.report_dir)
            link_path.symlink_to(relative_path)
        except (OSError, NotImplementedError):
            # シンボリックリンクが作成できない場合はコピー
            shutil.copy2(report_path, link_path)
    
    def cleanup_old_reports(self, keep_days: int = 30, max_reports: int = 100):
        """
        古いレポートファイルのクリーンアップ
        
        Args:
            keep_days: 保持日数
            max_reports: 最大レポート数
        """
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        # レポートファイル一覧を取得（タイムスタンプ順）
        report_files = self._get_report_files_with_timestamp()
        
        # 古いファイルを特定
        old_files = []
        for file_path, timestamp in report_files:
            if timestamp < cutoff_date:
                old_files.append(file_path)
        
        # 最大数を超えた場合の処理
        if len(report_files) > max_reports:
            # 古い順にソート
            sorted_files = sorted(report_files, key=lambda x: x[1])
            excess_count = len(sorted_files) - max_reports
            for file_path, _ in sorted_files[:excess_count]:
                if file_path not in old_files:
                    old_files.append(file_path)
        
        # アーカイブまたは削除
        archive_dir = self.report_dir / "archive"
        for file_path in old_files:
            try:
                if self._should_archive(file_path):
                    # アーカイブに移動
                    archive_path = archive_dir / file_path.name
                    shutil.move(str(file_path), str(archive_path))
                else:
                    # 削除
                    file_path.unlink()
            except Exception as e:
                print(f"⚠️ ファイル処理エラー {file_path}: {e}")
    
    def _get_report_files_with_timestamp(self) -> List[Tuple[Path, datetime]]:
        """タイムスタンプ付きレポートファイル一覧を取得"""
        report_files = []
        
        # メインディレクトリ
        for file_path in self.report_dir.glob("*.md"):
            if file_path.name.startswith("latest_"):
                continue  # 最新リンクファイルはスキップ
            
            timestamp = self._extract_timestamp_from_filename(file_path.name)
            if timestamp:
                report_files.append((file_path, timestamp))
        
        # サブディレクトリ
        for subdir in ["daily", "manual"]:
            subdir_path = self.report_dir / subdir
            if subdir_path.exists():
                for file_path in subdir_path.glob("*.md"):
                    timestamp = self._extract_timestamp_from_filename(file_path.name)
                    if timestamp:
                        report_files.append((file_path, timestamp))
        
        return report_files
    
    def _extract_timestamp_from_filename(self, filename: str) -> Optional[datetime]:
        """ファイル名からタイムスタンプを抽出"""
        try:
            # YYYYMMDD_HHMMSS形式を抽出
            parts = filename.split('_')
            if len(parts) >= 2:
                date_part = parts[0]
                time_part = parts[1]
                
                if len(date_part) == 8 and len(time_part) == 6:
                    timestamp_str = f"{date_part}_{time_part}"
                    return datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
        except (ValueError, IndexError):
            pass
        
        return None
    
    def _should_archive(self, file_path: Path) -> bool:
        """ファイルをアーカイブすべきかどうか判定"""
        # 重要なレポート（エラーを含む）はアーカイブ
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '❌' in content or 'ERROR' in content.upper():
                    return True
        except Exception:
            pass
        
        return False
    
    def get_report_statistics(self) -> dict:
        """レポート統計情報を取得"""
        report_files = self._get_report_files_with_timestamp()
        
        stats = {
            'total_reports': len(report_files),
            'oldest_report': None,
            'newest_report': None,
            'total_size_mb': 0,
            'by_directory': {
                'main': 0,
                'daily': 0,
                'manual': 0,
                'archive': 0
            }
        }
        
        if report_files:
            timestamps = [ts for _, ts in report_files]
            stats['oldest_report'] = min(timestamps).strftime("%Y-%m-%d %H:%M:%S")
            stats['newest_report'] = max(timestamps).strftime("%Y-%m-%d %H:%M:%S")
        
        # ディレクトリ別統計
        for subdir in ['daily', 'manual', 'archive']:
            subdir_path = self.report_dir / subdir
            if subdir_path.exists():
                stats['by_directory'][subdir] = len(list(subdir_path.glob("*.md")))
        
        # メインディレクトリ
        main_files = [f for f in self.report_dir.glob("*.md") if not f.name.startswith("latest_")]
        stats['by_directory']['main'] = len(main_files)
        
        # 総サイズ計算
        total_size = 0
        for file_path, _ in report_files:
            try:
                total_size += file_path.stat().st_size
            except Exception:
                pass
        
        stats['total_size_mb'] = round(total_size / (1024 * 1024), 2)
        
        return stats
    
    def list_recent_reports(self, limit: int = 10) -> List[dict]:
        """最近のレポート一覧を取得"""
        report_files = self._get_report_files_with_timestamp()
        
        # 新しい順にソート
        sorted_files = sorted(report_files, key=lambda x: x[1], reverse=True)
        
        recent_reports = []
        for file_path, timestamp in sorted_files[:limit]:
            report_info = {
                'filename': file_path.name,
                'path': str(file_path),
                'timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                'size_kb': round(file_path.stat().st_size / 1024, 1),
                'directory': file_path.parent.name if file_path.parent != self.report_dir else 'main'
            }
            recent_reports.append(report_info)
        
        return recent_reports
