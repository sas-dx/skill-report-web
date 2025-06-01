#!/bin/bash
# 要求仕様ID: PLT.1-DOCKER.1 - 開発環境Docker化
# Docker開発環境セットアップスクリプト

set -e

# カラー出力用
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ログ出力関数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# ヘルプ表示
show_help() {
    echo "Docker開発環境管理スクリプト"
    echo ""
    echo "使用方法:"
    echo "  $0 [コマンド]"
    echo ""
    echo "コマンド:"
    echo "  setup     - 初回セットアップ（環境ファイル作成、Docker起動、DB初期化）"
    echo "  start     - Docker環境を起動"
    echo "  stop      - Docker環境を停止"
    echo "  restart   - Docker環境を再起動"
    echo "  logs      - ログを表示"
    echo "  shell     - アプリケーションコンテナにシェル接続"
    echo "  db-shell  - データベースにシェル接続"
    echo "  clean     - Docker環境をクリーンアップ（ボリューム削除）"
    echo "  status    - Docker環境の状態確認"
    echo "  help      - このヘルプを表示"
}

# 環境ファイルの確認・作成
setup_env() {
    if [ ! -f .env ]; then
        log_info ".envファイルが存在しません。.env.exampleからコピーします..."
        cp .env.example .env
        log_success ".envファイルを作成しました"
        log_warning "必要に応じて.envファイルの設定を変更してください"
    else
        log_info ".envファイルは既に存在します"
    fi
}

# Docker環境のセットアップ
setup_docker() {
    log_info "Docker環境をセットアップしています..."
    
    # 環境ファイルの確認
    setup_env
    
    # Dockerイメージのビルド
    log_info "Dockerイメージをビルドしています..."
    docker-compose build
    
    # Docker環境の起動
    log_info "Docker環境を起動しています..."
    docker-compose up -d
    
    # データベースの準備完了を待機
    log_info "データベースの準備完了を待機しています..."
    sleep 10
    
    # Prismaクライアントの生成
    log_info "Prismaクライアントを生成しています..."
    docker-compose exec app npm run db:generate
    
    # データベースマイグレーション
    log_info "データベースマイグレーションを実行しています..."
    docker-compose exec app npm run db:migrate
    
    # シードデータの投入
    log_info "シードデータを投入しています..."
    docker-compose exec app npm run db:seed
    
    log_success "Docker環境のセットアップが完了しました！"
    log_info "アプリケーション: http://localhost:3000"
    log_info "pgAdmin: http://localhost:8080"
    log_info "PostgreSQL: localhost:5433"
}

# Docker環境の起動
start_docker() {
    log_info "Docker環境を起動しています..."
    docker-compose up -d
    log_success "Docker環境が起動しました"
    show_status
}

# Docker環境の停止
stop_docker() {
    log_info "Docker環境を停止しています..."
    docker-compose down
    log_success "Docker環境を停止しました"
}

# Docker環境の再起動
restart_docker() {
    log_info "Docker環境を再起動しています..."
    docker-compose restart
    log_success "Docker環境を再起動しました"
    show_status
}

# ログの表示
show_logs() {
    log_info "Docker環境のログを表示します（Ctrl+Cで終了）..."
    docker-compose logs -f
}

# アプリケーションコンテナにシェル接続
shell_app() {
    log_info "アプリケーションコンテナにシェル接続します..."
    docker-compose exec app sh
}

# データベースにシェル接続
shell_db() {
    log_info "データベースにシェル接続します..."
    docker-compose exec postgres psql -U skill_user -d skill_report_db
}

# Docker環境のクリーンアップ
clean_docker() {
    log_warning "Docker環境をクリーンアップします（全てのボリュームが削除されます）"
    read -p "続行しますか？ (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Docker環境をクリーンアップしています..."
        docker-compose down -v --remove-orphans
        docker system prune -f
        log_success "Docker環境をクリーンアップしました"
    else
        log_info "クリーンアップをキャンセルしました"
    fi
}

# Docker環境の状態確認
show_status() {
    log_info "Docker環境の状態:"
    echo ""
    docker-compose ps
    echo ""
    
    # サービスの稼働確認
    if docker-compose ps | grep -q "skill-report-app.*Up"; then
        log_success "アプリケーション: 稼働中 (http://localhost:3000)"
    else
        log_error "アプリケーション: 停止中"
    fi
    
    if docker-compose ps | grep -q "skill-report-postgres.*Up"; then
        log_success "PostgreSQL: 稼働中 (localhost:5433)"
    else
        log_error "PostgreSQL: 停止中"
    fi
    
    if docker-compose ps | grep -q "skill-report-pgadmin.*Up"; then
        log_success "pgAdmin: 稼働中 (http://localhost:8080)"
    else
        log_error "pgAdmin: 停止中"
    fi
}

# メイン処理
main() {
    case "${1:-help}" in
        setup)
            setup_docker
            ;;
        start)
            start_docker
            ;;
        stop)
            stop_docker
            ;;
        restart)
            restart_docker
            ;;
        logs)
            show_logs
            ;;
        shell)
            shell_app
            ;;
        db-shell)
            shell_db
            ;;
        clean)
            clean_docker
            ;;
        status)
            show_status
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "不明なコマンド: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# スクリプト実行
main "$@"
