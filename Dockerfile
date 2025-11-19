# 要求仕様ID: PLT.1-DOCKER.1 - 本番環境Docker設定

# ========================================
# ステージ1: ビルドステージ
# ========================================
FROM node:18-alpine AS builder

# 作業ディレクトリを設定
WORKDIR /app

# package.json と package-lock.json をコピー
COPY package*.json ./

# 全ての依存関係をインストール（開発用も含む）
RUN npm ci

# Prismaスキーマをコピーして生成
COPY src/database/prisma ./src/database/prisma
RUN npx prisma generate --schema=src/database/prisma/schema.prisma

# アプリケーションのソースコードをコピー
COPY . .

# 環境変数を設定（ビルド時に必要）
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Next.jsアプリケーションをビルド（standalone出力を生成）
RUN npm run build

# ========================================
# ステージ2: 実行ステージ
# ========================================
FROM node:18-alpine AS runner

# 作業ディレクトリを設定
WORKDIR /app

# システムの依存関係とロケール設定をインストール
RUN apk add --no-cache \
    libc6-compat \
    openssl \
    tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    echo "Asia/Tokyo" > /etc/timezone

# 非rootユーザーを作成
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# 環境変数を設定
ENV NODE_ENV=production
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV TZ=Asia/Tokyo
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"
ENV NEXT_TELEMETRY_DISABLED=1

# Next.js standalone出力を使用
# standalone出力には必要最小限の依存関係が含まれる
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

# Prismaスキーマとクライアントファイルをコピー
# standaloneビルドにPrismaが含まれない場合に備えて明示的にコピー
COPY --from=builder --chown=nextjs:nodejs /app/node_modules/.prisma ./node_modules/.prisma
COPY --from=builder --chown=nextjs:nodejs /app/node_modules/@prisma ./node_modules/@prisma
COPY --from=builder --chown=nextjs:nodejs /app/src/database/prisma ./src/database/prisma

# 非rootユーザーに切り替え
USER nextjs

# Next.jsのポートを公開
EXPOSE 3000

# ヘルスチェック設定
# 起動に時間がかかる場合があるため、start-periodを60秒に延長
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/api/health', (res) => { process.exit(res.statusCode === 200 ? 0 : 1); })"

# Next.js standalone server.jsを起動
CMD ["node", "server.js"]