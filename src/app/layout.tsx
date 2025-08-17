// 要求仕様ID: PLT.1-WEB.1 - Next.js App Router レイアウト設定
import type { Metadata } from 'next';
import { Inter, Noto_Sans_JP } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });
const notoSansJP = Noto_Sans_JP({ 
  subsets: ['latin'], 
  variable: '--font-noto-sans-jp',
  display: 'swap'
});

export const metadata: Metadata = {
  title: '年間スキル報告書システム',
  description: 'AI駆動開発による年間スキル報告書WEB化システム',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body className={`${inter.className} ${notoSansJP.variable}`}>
        {children}
      </body>
    </html>
  );
}
