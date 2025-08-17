/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: 上司フィードバック表示コンポーネント
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { RefreshCw, MessageSquare, User, Calendar, Star, ThumbsUp, AlertCircle } from 'lucide-react';

// 型定義
interface ManagerFeedback {
  feedback_id: string;
  manager_name: string;
  manager_position: string;
  feedback_type: 'review' | 'advice' | 'approval' | 'concern';
  feedback_content: string;
  rating?: number;
  created_date: string;
  is_read: boolean;
  priority: 'high' | 'medium' | 'low';
  related_goal?: string;
}

interface ManagerFeedbackSectionProps {
  userId?: string;
  className?: string;
}

/**
 * 上司フィードバック表示コンポーネント
 */
export function ManagerFeedbackSection({ userId, className }: ManagerFeedbackSectionProps) {
  const [feedbacks, setFeedbacks] = useState<ManagerFeedback[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  /**
   * フィードバックデータを取得
   */
  const fetchFeedbacks = async () => {
    try {
      setIsLoading(true);
      setError(null);

      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (userId) {
        headers['x-user-id'] = userId;
      }

      const response = await fetch('/api/career/manager-comment', {
        method: 'GET',
        headers,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success && data.data) {
        // APIレスポンスをコンポーネント用データに変換
        const transformedFeedbacks = data.data.comments?.map((comment: any) => ({
          feedback_id: comment.comment_id,
          manager_name: comment.manager_name,
          manager_position: comment.manager_position,
          feedback_type: mapCommentTypeToFeedbackType(comment.comment_type),
          feedback_content: comment.comment_text,
          rating: undefined, // APIレスポンスに含まれていない場合
          created_date: comment.comment_date,
          is_read: comment.status === 'READ' || comment.status === 'ACKNOWLEDGED',
          priority: mapPriorityLevel(comment.priority),
          related_goal: comment.related_goal_id
        })) || [];
        
        setFeedbacks(transformedFeedbacks);
      } else {
        throw new Error(data.error?.message || 'フィードバックデータの取得に失敗しました');
      }

    } catch (err) {
      console.error('フィードバックデータ取得エラー:', err);
      setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchFeedbacks();
  }, [userId]);

  /**
   * APIのコメントタイプをフィードバックタイプに変換
   */
  const mapCommentTypeToFeedbackType = (commentType: string): ManagerFeedback['feedback_type'] => {
    switch (commentType) {
      case 'CAREER_ADVICE':
        return 'advice';
      case 'SKILL_FEEDBACK':
        return 'review';
      case 'GOAL_REVIEW':
        return 'review';
      case 'GENERAL':
      default:
        return 'advice';
    }
  };

  /**
   * APIの優先度を変換
   */
  const mapPriorityLevel = (priority: string): ManagerFeedback['priority'] => {
    switch (priority) {
      case 'HIGH':
        return 'high';
      case 'LOW':
        return 'low';
      case 'MEDIUM':
      default:
        return 'medium';
    }
  };

  /**
   * フィードバックタイプに応じたアイコンを取得
   */
  const getFeedbackIcon = (type: string) => {
    switch (type) {
      case 'review':
        return <Star className="h-4 w-4 text-yellow-500" />;
      case 'advice':
        return <MessageSquare className="h-4 w-4 text-blue-500" />;
      case 'approval':
        return <ThumbsUp className="h-4 w-4 text-green-500" />;
      case 'concern':
        return <AlertCircle className="h-4 w-4 text-red-500" />;
      default:
        return <MessageSquare className="h-4 w-4 text-gray-500" />;
    }
  };

  /**
   * フィードバックタイプに応じたバッジバリアントを取得
   */
  const getFeedbackVariant = (type: string): "default" | "secondary" | "destructive" | "outline" => {
    switch (type) {
      case 'review':
        return 'default';
      case 'advice':
        return 'secondary';
      case 'approval':
        return 'secondary';
      case 'concern':
        return 'destructive';
      default:
        return 'outline';
    }
  };

  /**
   * フィードバックタイプの日本語表示を取得
   */
  const getFeedbackTypeText = (type: string) => {
    switch (type) {
      case 'review':
        return 'レビュー';
      case 'advice':
        return 'アドバイス';
      case 'approval':
        return '承認';
      case 'concern':
        return '懸念事項';
      default:
        return 'フィードバック';
    }
  };

  /**
   * 優先度に応じたバッジバリアントを取得
   */
  const getPriorityVariant = (priority: string): "default" | "secondary" | "destructive" | "outline" => {
    switch (priority) {
      case 'high':
        return 'destructive';
      case 'medium':
        return 'default';
      case 'low':
        return 'secondary';
      default:
        return 'outline';
    }
  };

  /**
   * 優先度の日本語表示を取得
   */
  const getPriorityText = (priority: string) => {
    switch (priority) {
      case 'high':
        return '高';
      case 'medium':
        return '中';
      case 'low':
        return '低';
      default:
        return '-';
    }
  };

  /**
   * 日付をフォーマット
   */
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  /**
   * 評価星を表示
   */
  const renderRating = (rating?: number) => {
    if (!rating) return null;
    
    return (
      <div className="flex items-center gap-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <Star
            key={star}
            className={`h-4 w-4 ${
              star <= rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
            }`}
          />
        ))}
        <span className="text-sm text-gray-600 ml-1">({rating}/5)</span>
      </div>
    );
  };

  if (isLoading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MessageSquare className="h-5 w-5" />
            上司からのフィードバック
          </CardTitle>
          <CardDescription>
            上司からのコメントやアドバイスを表示
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center h-64">
            <RefreshCw className="h-8 w-8 animate-spin text-gray-400" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-red-500" />
            上司からのフィードバック
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <p className="text-red-600 mb-4">{error}</p>
            <Button onClick={fetchFeedbacks} variant="outline">
              <RefreshCw className="h-4 w-4 mr-2" />
              再試行
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (feedbacks.length === 0) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MessageSquare className="h-5 w-5" />
            上司からのフィードバック
          </CardTitle>
          <CardDescription>
            上司からのコメントやアドバイスを表示
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <p className="text-gray-500">フィードバックがありません</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  // 未読フィードバックを抽出
  const unreadFeedbacks = feedbacks.filter(feedback => !feedback.is_read);

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <MessageSquare className="h-5 w-5" />
              上司からのフィードバック
              {unreadFeedbacks.length > 0 && (
                <Badge variant="destructive" className="ml-2">
                  {unreadFeedbacks.length}件未読
                </Badge>
              )}
            </CardTitle>
            <CardDescription>
              上司からのコメントやアドバイスを表示
            </CardDescription>
          </div>
          <Button onClick={fetchFeedbacks} variant="outline" size="sm">
            <RefreshCw className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {feedbacks.map((feedback) => (
            <div
              key={feedback.feedback_id}
              className={`p-4 border rounded-lg ${
                !feedback.is_read ? 'bg-blue-50 border-blue-200' : 'bg-white'
              }`}
            >
              {/* ヘッダー */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-2">
                    <User className="h-4 w-4 text-gray-500" />
                    <span className="font-medium text-gray-900">
                      {feedback.manager_name}
                    </span>
                    <span className="text-sm text-gray-500">
                      ({feedback.manager_position})
                    </span>
                  </div>
                  {!feedback.is_read && (
                    <Badge variant="destructive" className="text-xs">
                      未読
                    </Badge>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant={getFeedbackVariant(feedback.feedback_type)}>
                    {getFeedbackIcon(feedback.feedback_type)}
                    <span className="ml-1">{getFeedbackTypeText(feedback.feedback_type)}</span>
                  </Badge>
                  <Badge variant={getPriorityVariant(feedback.priority)} className="text-xs">
                    優先度: {getPriorityText(feedback.priority)}
                  </Badge>
                </div>
              </div>

              {/* 関連目標 */}
              {feedback.related_goal && (
                <div className="mb-3">
                  <span className="text-sm text-gray-600">関連目標: </span>
                  <span className="text-sm font-medium">{feedback.related_goal}</span>
                </div>
              )}

              {/* フィードバック内容 */}
              <div className="mb-3">
                <p className="text-gray-800 leading-relaxed">
                  {feedback.feedback_content}
                </p>
              </div>

              {/* 評価 */}
              {feedback.rating && (
                <div className="mb-3">
                  {renderRating(feedback.rating)}
                </div>
              )}

              {/* フッター */}
              <div className="flex items-center justify-between text-sm text-gray-500">
                <div className="flex items-center gap-1">
                  <Calendar className="h-4 w-4" />
                  <span>{formatDate(feedback.created_date)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* 統計情報 */}
        <div className="grid grid-cols-4 gap-4 pt-6 mt-6 border-t">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {feedbacks.length}
            </div>
            <div className="text-xs text-gray-500">総フィードバック数</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-red-600">
              {unreadFeedbacks.length}
            </div>
            <div className="text-xs text-gray-500">未読</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {feedbacks.filter(f => f.feedback_type === 'approval').length}
            </div>
            <div className="text-xs text-gray-500">承認</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-600">
              {feedbacks.filter(f => f.feedback_type === 'review').length}
            </div>
            <div className="text-xs text-gray-500">レビュー</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default ManagerFeedbackSection;
