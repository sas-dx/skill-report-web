// 要求仕様ID: PLT.1-WEB.1 - メインページ（ダッシュボード）
export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            年間スキル報告書システム
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            AI駆動開発による業務効率化・可視化システム
          </p>
          
          <div className="bg-white rounded-lg shadow-md p-6 max-w-2xl mx-auto">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              システム起動確認
            </h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <span className="text-green-800">Next.js 14</span>
                <span className="text-green-600 font-semibold">✓ 動作中</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <span className="text-green-800">TypeScript</span>
                <span className="text-green-600 font-semibold">✓ 設定済み</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <span className="text-green-800">Tailwind CSS</span>
                <span className="text-green-600 font-semibold">✓ 設定済み</span>
              </div>
            </div>
            
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <p className="text-blue-800 text-sm">
                🚀 開発環境が正常に起動しました！<br/>
                次のステップ: 依存関係のインストールとデータベース設定
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
