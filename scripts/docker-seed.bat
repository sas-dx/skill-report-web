@echo off
REM 要求仕様ID: PLT.1-DOCKER.1 - 開発環境Docker化
REM Docker環境でのseedファイル実行スクリプト（Windows用）

echo 🌱 Docker環境でのseedファイル実行を開始します...

REM PostgreSQLの準備完了を待機
echo 📡 PostgreSQLの準備完了を待機中...
:wait_postgres
docker-compose exec postgres pg_isready -U skill_user -d skill_report_db >nul 2>&1
if errorlevel 1 (
    echo ⏳ PostgreSQLの準備を待機中...
    timeout /t 2 /nobreak >nul
    goto wait_postgres
)

echo ✅ PostgreSQLが準備完了しました

REM Prismaマイグレーションの実行
echo 🔄 Prismaマイグレーションを実行中...
docker-compose exec app npx prisma migrate dev --schema=src/database/prisma/schema.prisma --name init

REM Prismaクライアントの生成
echo 🔧 Prismaクライアントを生成中...
docker-compose exec app npx prisma generate --schema=src/database/prisma/schema.prisma

REM seedファイルの実行
echo 🌱 seedファイルを実行中...
docker-compose exec app npx prisma db seed --schema=src/database/prisma/schema.prisma

echo ✅ Docker環境でのseedファイル実行が完了しました！
pause
