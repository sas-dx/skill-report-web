@echo off
REM 要求仕様ID: PLT.1-DEPLOY.1 - Windowsデプロイスクリプト

echo ================================
echo 年間スキル報告書WEB デプロイスクリプト
echo ================================

REM 環境変数チェック
if not exist .env (
    echo ❌ エラー: .envファイルが見つかりません
    echo 👉 .env.exampleをコピーして.envを作成してください
    exit /b 1
)

REM デプロイ環境選択
echo.
echo デプロイ環境を選択してください:
echo 1) 開発環境 (docker-compose.yml)
echo 2) 本番環境 (docker-compose.prod.yml)
set /p ENV_CHOICE="選択 (1 or 2): "

if "%ENV_CHOICE%"=="1" (
    set COMPOSE_FILE=docker-compose.yml
    set ENV_NAME=開発環境
) else if "%ENV_CHOICE%"=="2" (
    set COMPOSE_FILE=docker-compose.prod.yml
    set ENV_NAME=本番環境
) else (
    echo ❌ 無効な選択です
    exit /b 1
)

echo.
echo 📦 %ENV_NAME% にデプロイします...
echo.

REM 既存のコンテナを停止
echo 🛑 既存のコンテナを停止中...
docker-compose -f %COMPOSE_FILE% down

REM イメージをビルド
echo.
echo 🔨 Dockerイメージをビルド中...
docker-compose -f %COMPOSE_FILE% build --no-cache

REM コンテナを起動
echo.
echo 🚀 コンテナを起動中...
docker-compose -f %COMPOSE_FILE% up -d

REM 起動確認
echo.
echo ⏳ サービスの起動を待機中...
timeout /t 10 /nobreak > nul

REM データベースマイグレーション実行
echo.
echo 🗄️ データベースマイグレーションを実行中...
docker-compose -f %COMPOSE_FILE% exec app npm run db:migrate

REM Prismaクライアント生成
echo.
echo 🔧 Prismaクライアントを生成中...
docker-compose -f %COMPOSE_FILE% exec app npm run db:generate

REM データベースシード実行（開発環境のみ）
if "%ENV_CHOICE%"=="1" (
    set /p SEED_CHOICE="📝 シードデータを投入しますか？ (y/n): "
    if /i "%SEED_CHOICE%"=="y" (
        echo 🌱 シードデータを投入中...
        docker-compose -f %COMPOSE_FILE% exec app npm run db:seed
    )
)

REM ヘルスチェック
echo.
echo 🏥 ヘルスチェック中...
for /L %%i in (1,1,5) do (
    curl -f http://localhost:3000 >nul 2>&1
    if !errorlevel! == 0 (
        echo ✅ アプリケーションが正常に起動しました！
        goto :deploy_complete
    )
    echo ⏳ 待機中... (%%i/5)
    timeout /t 5 /nobreak > nul
)

:deploy_complete
REM デプロイ完了
echo.
echo ================================
echo ✅ デプロイが完了しました！
echo ================================
echo.
echo 📌 アクセスURL:
echo    - アプリケーション: http://localhost:3000
if "%ENV_CHOICE%"=="1" (
    echo    - pgAdmin: http://localhost:8080
    echo      Email: admin@example.com
    echo      Password: admin123
)
echo.
echo 📋 便利なコマンド:
echo    - ログ確認: docker-compose -f %COMPOSE_FILE% logs -f
echo    - 停止: docker-compose -f %COMPOSE_FILE% down
echo    - 再起動: docker-compose -f %COMPOSE_FILE% restart
echo.
pause