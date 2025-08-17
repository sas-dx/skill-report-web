/**
 * エラーメッセージ表示コンポーネント
 * APIエラーやその他のエラーを統一した形式で表示
 */

'use client';

import React from 'react';

interface ErrorMessageProps {
  title?: string;
  message: string;
  type?: 'error' | 'warning' | 'info';
  onRetry?: () => void;
  onDismiss?: () => void;
  className?: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({
  title = 'エラーが発生しました',
  message,
  type = 'error',
  onRetry,
  onDismiss,
  className = ''
}) => {
  const getIconAndColors = () => {
    switch (type) {
      case 'warning':
        return {
          bgColor: 'bg-yellow-50',
          borderColor: 'border-yellow-200',
          iconColor: 'text-yellow-400',
          textColor: 'text-yellow-800',
          titleColor: 'text-yellow-900',
          icon: (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          )
        };
      case 'info':
        return {
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200',
          iconColor: 'text-blue-400',
          textColor: 'text-blue-800',
          titleColor: 'text-blue-900',
          icon: (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          )
        };
      default: // error
        return {
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200',
          iconColor: 'text-red-400',
          textColor: 'text-red-800',
          titleColor: 'text-red-900',
          icon: (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          )
        };
    }
  };

  const { bgColor, borderColor, iconColor, textColor, titleColor, icon } = getIconAndColors();

  return (
    <div className={`${bgColor} border ${borderColor} rounded-md p-4 ${className}`}>
      <div className="flex">
        <div className="flex-shrink-0">
          <svg className={`h-5 w-5 ${iconColor}`} viewBox="0 0 20 20" fill="currentColor">
            {icon}
          </svg>
        </div>
        <div className="ml-3 flex-1">
          <h3 className={`text-sm font-medium ${titleColor}`}>
            {title}
          </h3>
          <div className={`mt-2 text-sm ${textColor}`}>
            <p>{message}</p>
          </div>
          {(onRetry || onDismiss) && (
            <div className="mt-4 flex space-x-3">
              {onRetry && (
                <button
                  type="button"
                  onClick={onRetry}
                  className={`text-sm font-medium ${
                    type === 'error' 
                      ? 'text-red-800 hover:text-red-700' 
                      : type === 'warning'
                      ? 'text-yellow-800 hover:text-yellow-700'
                      : 'text-blue-800 hover:text-blue-700'
                  } underline`}
                >
                  再試行
                </button>
              )}
              {onDismiss && (
                <button
                  type="button"
                  onClick={onDismiss}
                  className={`text-sm font-medium ${
                    type === 'error' 
                      ? 'text-red-800 hover:text-red-700' 
                      : type === 'warning'
                      ? 'text-yellow-800 hover:text-yellow-700'
                      : 'text-blue-800 hover:text-blue-700'
                  } underline`}
                >
                  閉じる
                </button>
              )}
            </div>
          )}
        </div>
        {onDismiss && (
          <div className="ml-auto pl-3">
            <button
              type="button"
              onClick={onDismiss}
              className={`inline-flex rounded-md p-1.5 ${
                type === 'error' 
                  ? 'text-red-500 hover:bg-red-100 focus:ring-red-600' 
                  : type === 'warning'
                  ? 'text-yellow-500 hover:bg-yellow-100 focus:ring-yellow-600'
                  : 'text-blue-500 hover:bg-blue-100 focus:ring-blue-600'
              } focus:outline-none focus:ring-2 focus:ring-offset-2`}
            >
              <span className="sr-only">閉じる</span>
              <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ErrorMessage;