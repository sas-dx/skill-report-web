/** @type {import('next').NextConfig} */
const nextConfig = {
  // 要求仕様ID: PLT.1-WEB.1 - Next.js 14 App Router設定
  experimental: {
    serverComponentsExternalPackages: ['@prisma/client', 'bcryptjs'],
  },
  
  // 要求仕様ID: PLT.1-RESP.1 - レスポンシブ対応
  images: {
    domains: ['localhost'],
    formats: ['image/webp', 'image/avif'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },

  // 要求仕様ID: PLT.1-BRS.1 - ブラウザ互換性
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },

  // セキュリティヘッダー設定
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()',
          },
        ],
      },
    ];
  },

  // マルチテナント対応のリライト設定
  async rewrites() {
    return [
      // テナント固有のルーティング
      {
        source: '/tenant/:tenant/api/:path*',
        destination: '/api/:path*?tenant=:tenant',
      },
      {
        source: '/tenant/:tenant/:path*',
        destination: '/:path*?tenant=:tenant',
      },
    ];
  },

  // 環境変数の検証
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },

  // パフォーマンス最適化
  poweredByHeader: false,
  compress: true,
  
  // 開発時の設定
  ...(process.env.NODE_ENV === 'development' && {
    logging: {
      fetches: {
        fullUrl: true,
      },
    },
  }),

  // 本番環境の最適化
  ...(process.env.NODE_ENV === 'production' && {
    output: 'standalone',
    swcMinify: true,
  }),
};

module.exports = nextConfig;
