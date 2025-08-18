'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import {
  HelpCircle,
  Book,
  MessageCircle,
  Mail,
  Phone,
  FileText,
  Search,
  ChevronDown,
  ChevronRight,
  ArrowLeft,
  Home,
  ExternalLink,
  Download,
  PlayCircle,
} from 'lucide-react';

interface FAQItem {
  id: number;
  category: string;
  question: string;
  answer: string;
}

interface GuideItem {
  id: number;
  title: string;
  description: string;
  icon: React.ElementType;
  link: string;
}

export default function HelpPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedFAQ, setExpandedFAQ] = useState<number | null>(null);
  const [selectedCategory, setSelectedCategory] = useState('all');

  // FAQデータ
  const faqItems: FAQItem[] = [
    {
      id: 1,
      category: 'basic',
      question: 'スキル報告書システムとは何ですか？',
      answer: 'スキル報告書システムは、従業員のスキル、作業実績、研修履歴、キャリアプランを一元管理するシステムです。年間スキル報告書の作成や、スキルギャップ分析、キャリア開発支援などの機能を提供しています。',
    },
    {
      id: 2,
      category: 'basic',
      question: 'ログインできない場合はどうすればよいですか？',
      answer: 'ログインできない場合は、以下の点をご確認ください：\n1. ユーザーIDとパスワードが正しく入力されているか\n2. Caps Lockがオンになっていないか\n3. ブラウザのCookieが有効になっているか\nそれでもログインできない場合は、システム管理者にお問い合わせください。',
    },
    {
      id: 3,
      category: 'skills',
      question: 'スキル評価はどのように行いますか？',
      answer: 'スキル評価は以下の手順で行います：\n1. スキル管理画面へアクセス\n2. 評価したいスキルカテゴリを選択\n3. 各スキル項目に対して1-5のレベルを選択\n4. 必要に応じてコメントを追加\n5. 保存ボタンをクリック',
    },
    {
      id: 4,
      category: 'skills',
      question: 'スキルレベルの基準は何ですか？',
      answer: 'スキルレベルは以下の5段階で評価します：\nレベル1: 初心者（基礎知識あり）\nレベル2: 初級（指導の下で実施可能）\nレベル3: 中級（独力で実施可能）\nレベル4: 上級（他者を指導可能）\nレベル5: エキスパート（組織をリード可能）',
    },
    {
      id: 5,
      category: 'work',
      question: '作業実績はどのように登録しますか？',
      answer: '作業実績の登録方法：\n1. 作業実績画面で「新規登録」をクリック\n2. プロジェクト名、期間、役割を入力\n3. 業務内容と成果を記載\n4. 使用技術を選択\n5. 保存して完了',
    },
    {
      id: 6,
      category: 'work',
      question: '過去の作業実績を編集できますか？',
      answer: 'はい、過去の作業実績は編集可能です。作業実績一覧から編集したい項目の「編集」ボタンをクリックしてください。ただし、承認済みの実績は上司の承認取り消しが必要な場合があります。',
    },
    {
      id: 7,
      category: 'training',
      question: '研修履歴はどこで確認できますか？',
      answer: '研修履歴は「研修管理」メニューから確認できます。受講済み、受講中、受講予定の研修が一覧表示され、各研修の詳細情報や修了証明書のダウンロードも可能です。',
    },
    {
      id: 8,
      category: 'report',
      question: '年間スキル報告書の作成方法は？',
      answer: '年間スキル報告書の作成手順：\n1. レポート画面へアクセス\n2. 「新規作成」をクリック\n3. 対象年度を選択\n4. 自動生成されたレポートを確認\n5. 必要に応じて編集\n6. 上司へ提出',
    },
    {
      id: 9,
      category: 'career',
      question: 'キャリアプランの設定方法は？',
      answer: 'キャリアプラン画面で「キャリア目標を設定」をクリックし、短期・中期・長期の目標を入力します。スキルギャップ分析を活用して、必要なスキルや研修を特定し、アクションプランを作成してください。',
    },
    {
      id: 10,
      category: 'other',
      question: 'データのエクスポートは可能ですか？',
      answer: 'はい、各画面でExcelやPDF形式でのエクスポートが可能です。エクスポートボタンをクリックし、必要な形式を選択してダウンロードしてください。',
    },
  ];

  // ユーザーガイド
  const guides: GuideItem[] = [
    {
      id: 1,
      title: 'はじめに',
      description: 'システムの概要と基本的な使い方',
      icon: Book,
      link: '/guides/getting-started',
    },
    {
      id: 2,
      title: 'スキル管理ガイド',
      description: 'スキル評価と管理の詳細手順',
      icon: FileText,
      link: '/guides/skills',
    },
    {
      id: 3,
      title: '作業実績ガイド',
      description: 'プロジェクト実績の登録と管理',
      icon: FileText,
      link: '/guides/work',
    },
    {
      id: 4,
      title: '研修管理ガイド',
      description: '研修の申請から修了まで',
      icon: FileText,
      link: '/guides/training',
    },
    {
      id: 5,
      title: 'レポート作成ガイド',
      description: '年間スキル報告書の作成手順',
      icon: FileText,
      link: '/guides/reports',
    },
    {
      id: 6,
      title: 'ビデオチュートリアル',
      description: '動画で学ぶ基本操作',
      icon: PlayCircle,
      link: '/guides/videos',
    },
  ];

  // カテゴリー
  const categories = [
    { value: 'all', label: 'すべて' },
    { value: 'basic', label: '基本操作' },
    { value: 'skills', label: 'スキル管理' },
    { value: 'work', label: '作業実績' },
    { value: 'training', label: '研修' },
    { value: 'report', label: 'レポート' },
    { value: 'career', label: 'キャリア' },
    { value: 'other', label: 'その他' },
  ];

  // FAQフィルタリング
  const filteredFAQ = faqItems.filter((item) => {
    const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory;
    const matchesSearch = item.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          item.answer.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const toggleFAQ = (id: number) => {
    setExpandedFAQ(expandedFAQ === id ? null : id);
  };

  return (
    <div className="container mx-auto max-w-7xl px-4 py-8">
      {/* ヘッダー */}
      <div className="mb-6">
        <Button
          variant="outline"
          onClick={() => window.location.href = '/dashboard'}
          className="flex items-center mb-4"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          ダッシュボードへ戻る
        </Button>
        
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <HelpCircle className="w-10 h-10 mr-3 text-blue-600" />
            <div>
              <h1 className="text-3xl font-bold text-gray-900">ヘルプセンター</h1>
              <p className="text-gray-600 mt-1">お困りの際はこちらをご確認ください</p>
            </div>
          </div>
          <Button
            variant="ghost"
            onClick={() => window.location.href = '/dashboard'}
            className="flex items-center text-gray-600 hover:text-gray-900"
          >
            <Home className="w-5 h-5 mr-2" />
            ホーム
          </Button>
        </div>
      </div>

      {/* 検索バー */}
      <Card className="mb-8 p-6 bg-blue-50">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-xl font-semibold mb-4 text-center">何かお探しですか？</h2>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <Input
              type="text"
              placeholder="キーワードを入力して検索..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-4 py-3 text-lg"
            />
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* 左側: ユーザーガイド */}
        <div className="lg:col-span-1">
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Book className="w-5 h-5 mr-2" />
              ユーザーガイド
            </h2>
            <div className="space-y-3">
              {guides.map((guide) => {
                const Icon = guide.icon;
                return (
                  <a
                    key={guide.id}
                    href={guide.link}
                    className="block p-3 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-start">
                      <Icon className="w-5 h-5 mt-0.5 mr-3 text-blue-600" />
                      <div className="flex-1">
                        <h3 className="font-medium text-gray-900">{guide.title}</h3>
                        <p className="text-sm text-gray-600 mt-1">{guide.description}</p>
                      </div>
                      <ExternalLink className="w-4 h-4 text-gray-400 mt-0.5" />
                    </div>
                  </a>
                );
              })}
            </div>

            <div className="mt-6 pt-6 border-t">
              <h3 className="font-medium mb-3">ダウンロード</h3>
              <Button
                variant="outline"
                className="w-full flex items-center justify-center"
                onClick={() => window.open('/manual.pdf', '_blank')}
              >
                <Download className="w-4 h-4 mr-2" />
                操作マニュアル (PDF)
              </Button>
            </div>
          </Card>

          {/* お問い合わせ */}
          <Card className="p-6 mt-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <MessageCircle className="w-5 h-5 mr-2" />
              お問い合わせ
            </h2>
            <div className="space-y-4">
              <div className="flex items-center">
                <Mail className="w-5 h-5 mr-3 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-600">メール</p>
                  <a href="mailto:support@example.com" className="text-blue-600 hover:underline">
                    support@example.com
                  </a>
                </div>
              </div>
              <div className="flex items-center">
                <Phone className="w-5 h-5 mr-3 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-600">電話</p>
                  <a href="tel:03-1234-5678" className="text-blue-600 hover:underline">
                    03-1234-5678
                  </a>
                </div>
              </div>
              <div className="pt-4">
                <p className="text-sm text-gray-600 mb-2">営業時間</p>
                <p className="text-sm">平日 9:00-18:00</p>
                <p className="text-sm text-gray-500">（土日祝日を除く）</p>
              </div>
            </div>
          </Card>
        </div>

        {/* 右側: FAQ */}
        <div className="lg:col-span-2">
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">よくある質問</h2>
            
            {/* カテゴリーフィルター */}
            <div className="flex flex-wrap gap-2 mb-6">
              {categories.map((cat) => (
                <button
                  key={cat.value}
                  onClick={() => setSelectedCategory(cat.value)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                    selectedCategory === cat.value
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {cat.label}
                </button>
              ))}
            </div>

            {/* FAQ一覧 */}
            <div className="space-y-3">
              {filteredFAQ.length > 0 ? (
                filteredFAQ.map((item) => (
                  <div
                    key={item.id}
                    className="border rounded-lg overflow-hidden"
                  >
                    <button
                      onClick={() => toggleFAQ(item.id)}
                      className="w-full px-4 py-3 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
                    >
                      <span className="font-medium text-gray-900">{item.question}</span>
                      {expandedFAQ === item.id ? (
                        <ChevronDown className="w-5 h-5 text-gray-400" />
                      ) : (
                        <ChevronRight className="w-5 h-5 text-gray-400" />
                      )}
                    </button>
                    {expandedFAQ === item.id && (
                      <div className="px-4 py-3 bg-gray-50 border-t">
                        <p className="text-gray-700 whitespace-pre-line">{item.answer}</p>
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <HelpCircle className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                  <p>該当する質問が見つかりません</p>
                  <p className="text-sm mt-2">別のキーワードで検索してみてください</p>
                </div>
              )}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}