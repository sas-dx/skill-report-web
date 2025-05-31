@echo off
REM 要求仕様ID: PLT.1-DOCKER.1 - 開発環境Docker化
REM Docker開発環境セットアップスクリプト（Windows用）

setlocal enabledelayedexpansion

REM カラー出力用（Windows 10以降）
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM ヘルプ表示
:show_help
echo Docker開発環境管理スクリプト（Windows用）
echo.
echo 使用方法:
echo   %~nx0 [コマンド]
echo.
echo コマンド:
echo   setup     - 初回セットアップ（環境ファイル作成、Docker起動、DB初期化）
echo   start     - Docker環境を起動
echo   stop      - Docker環境を停止
echo   restart   - Docker環境を再起動
echo   logs      - ログを表示
echo   shell     - アプリケーションコンテナにシェル接続
echo   db-shell  - データベースにシェル接続
echo   clean     - Docker環境をクリーンアップ（ボリューム削除）
echo   status    - Docker環境の状態確認
echo   help      - このヘルプを表示
goto :eof

REM ログ出力関数
:log_info
echo %BLUE%[INFO]%NC% %~1
goto :eof

:log_success
echo %GREEN%[SUCCESS]%NC% %~1
goto :eof

:log_warning
echo %YELLOW%[WARNING]%NC% %~1
goto :eof

:log_error
echo %RED%[ERROR]%NC% %~1
goto :eof

REM 環境ファイルの確認・作成
:setup_env
if not exist .env (
    call :log_info ".envファイルが存在しません。.env.exampleからコピーします..."
    copy .env.example .env >nul
    call :log_success ".envファイルを作成しました"
    call :log_warning "必要に応じて.envファイルの設定を変更してください"
) else (
    call :log_info ".envファイルは既に存在します"
)
goto :eof

REM Docker環境のセットアップ
:setup_docker
call :log_info "Docker環境をセットアップしています..."

REM 環境ファイルの確認
call :setup_env

REM Dockerイメージのビルド
call :log_info "Dockerイメージをビルドしています..."
docker-compose build
if errorlevel 1 (
    call :log_error "Dockerイメージのビルドに失敗しました"
    exit /b 1
)

REM Docker環境の起動
call :log_info "Docker環境を起動しています..."
docker-compose up -d
if errorlevel 1 (
    call :log_error "Docker環境の起動に失敗しました"
    exit /b 1
)

REM データベースの準備完了を待機
call :log_info "データベースの準備完了を待機しています..."
timeout /t 10 /nobreak >nul

REM Prismaクライアントの生成
call :log_info "Prismaクライアントを生成しています..."
docker-compose exec app npm run db:generate
if errorlevel 1 (
    call :log_error "Prismaクライアントの生成に失敗しました"
    exit /b 1
)

REM データベースマイグレーション
call :log_info "データベースマイグレーションを実行しています..."
docker-compose exec app npm run db:migrate
if errorlevel 1 (
    call :log_error "データベースマイグレーションに失敗しました"
    exit /b 1
)

REM シードデータの投入
call :log_info "シードデータを投入しています..."
docker-compose exec app npm run db:seed
if errorlevel 1 (
    call :log_error "シードデータの投入に失敗しました"
    exit /b 1
)

call :log_success "Docker環境のセットアップが完了しました！"
call :log_info "アプリケーション: http://localhost:3000"
call :log_info "pgAdmin: http://localhost:8080"
call :log_info "PostgreSQL: localhost:5433"
goto :eof

REM Docker環境の起動
:start_docker
call :log_info "Docker環境を起動しています..."
docker-compose up -d
if errorlevel 1 (
    call :log_error "Docker環境の起動に失敗しました"
    exit /b 1
)
call :log_success "Docker環境が起動しました"
call :show_status
goto :eof

REM Docker環境の停止
:stop_docker
call :log_info "Docker環境を停止しています..."
docker-compose down
if errorlevel 1 (
    call :log_error "Docker環境の停止に失敗しました"
    exit /b 1
)
call :log_success "Docker環境を停止しました"
goto :eof

REM Docker環境の再起動
:restart_docker
call :log_info "Docker環境を再起動しています..."
docker-compose restart
if errorlevel 1 (
    call :log_error "Docker環境の再起動に失敗しました"
    exit /b 1
)
call :log_success "Docker環境を再起動しました"
call :show_status
goto :eof

REM ログの表示
:show_logs
call :log_info "Docker環境のログを表示します（Ctrl+Cで終了）..."
docker-compose logs -f
goto :eof

REM アプリケーションコンテナにシェル接続
:shell_app
call :log_info "アプリケーションコンテナにシェル接続します..."
docker-compose exec app sh
goto :eof

REM データベースにシェル接続
:shell_db
call :log_info "データベースにシェル接続します..."
docker-compose exec postgres psql -U skill_user -d skill_report_db
goto :eof

REM Docker環境のクリーンアップ
:clean_docker
call :log_warning "Docker環境をクリーンアップします（全てのボリュームが削除されます）"
set /p confirm="続行しますか？ (y/N): "
if /i "!confirm!"=="y" (
    call :log_info "Docker環境をクリーンアップしています..."
    docker-compose down -v --remove-orphans
    docker system prune -f
    call :log_success "Docker環境をクリーンアップしました"
) else (
    call :log_info "クリーンアップをキャンセルしました"
)
goto :eof

REM Docker環境の状態確認
:show_status
call :log_info "Docker環境の状態:"
echo.
docker-compose ps
echo.

REM サービスの稼働確認
docker-compose ps | findstr "skill-report-app.*Up" >nul
if not errorlevel 1 (
    call :log_success "アプリケーション: 稼働中 (http://localhost:3000)"
) else (
    call :log_error "アプリケーション: 停止中"
)

docker-compose ps | findstr "skill-report-postgres.*Up" >nul
if not errorlevel 1 (
    call :log_success "PostgreSQL: 稼働中 (localhost:5433)"
) else (
    call :log_error "PostgreSQL: 停止中"
)

docker-compose ps | findstr "skill-report-pgadmin.*Up" >nul
if not errorlevel 1 (
    call :log_success "pgAdmin: 稼働中 (http://localhost:8080)"
) else (
    call :log_error "pgAdmin: 停止中"
)
goto :eof

REM メイン処理
:main
set "command=%~1"
if "%command%"=="" set "command=help"

if "%command%"=="setup" (
    call :setup_docker
) else if "%command%"=="start" (
    call :start_docker
) else if "%command%"=="stop" (
    call :stop_docker
) else if "%command%"=="restart" (
    call :restart_docker
) else if "%command%"=="logs" (
    call :show_logs
) else if "%command%"=="shell" (
    call :shell_app
) else if "%command%"=="db-shell" (
    call :shell_db
) else if "%command%"=="clean" (
    call :clean_docker
) else if "%command%"=="status" (
    call :show_status
) else if "%command%"=="help" (
    call :show_help
) else if "%command%"=="--help" (
    call :show_help
) else if "%command%"=="-h" (
    call :show_help
) else (
    call :log_error "不明なコマンド: %command%"
    echo.
    call :show_help
    exit /b 1
)

goto :eof

REM スクリプト実行
call :main %*
