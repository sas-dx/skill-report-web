# API仕様書：スキルマップ生成API

| 項目                | 内容                                                                                |
|---------------------|------------------------------------------------------------------------------------|
| **API ID**          | API-026                                                                            |
| **API名称**         | スキルマップ生成API                                                                |
| **エンドポイント**  | /api/skills/map                                                                    |
| **HTTPメソッド**    | POST                                                                               |
| **概要・目的**      | 組織・部署・個人のスキルマップデータを生成し、視覚的なスキル分析を提供する          |
| **利用画面**        | SCR-SKILL-MAP                                                                      |
| **優先度**          | 中                                                                                  |
| **認証要件**        | 必須（ユーザー権限以上）                                                            |
| **レート制限**      | 50 req/min                                                                         |

## 1. エンドポイント詳細

### 1.1 スキルマップ生成

#### リクエスト
```http
POST /api/skills/map
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### リクエストボディ
```json
{
  "mapType": "organization",
  "targetId": "org_001",
  "filters": {
    "departments": ["engineering", "design"],
    "skillCategories": ["technical", "business"],
    "experienceLevels": ["beginner", "intermediate", "advanced"],
    "dateRange": {
      "from": "2024-01-01",
      "to": "2025-05-30"
    }
  },
  "visualization": {
    "type": "heatmap",
    "groupBy": "department",
    "aggregation": "average",
    "includeGaps": true,
    "showTrends": true
  },
  "options": {
    "includeSubordinates": true,
    "anonymize": false,
    "exportFormat": "json"
  }
}
```

#### リクエストパラメータ
| パラメータ名 | 型     | 必須 | 説明                                           |
|--------------|--------|------|------------------------------------------------|
| mapType      | String | Yes  | マップ種別（organization/department/team/individual） |
| targetId     | String | Yes  | 対象ID（組織・部署・チーム・個人のID）         |
| filters      | Object | No   | フィルタ条件                                   |
| visualization| Object | No   | 可視化設定                                     |
| options      | Object | No   | 追加オプション                                 |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "skillMap": {
      "id": "map_001",
      "type": "organization",
      "targetId": "org_001",
      "targetName": "エンジニアリング部",
      "generatedAt": "2025-05-30T11:00:00Z",
      "summary": {
        "totalUsers": 45,
        "totalSkills": 120,
        "averageSkillLevel": 3.2,
        "skillCoverage": 0.75,
        "topSkillCategories": [
          {
            "category": "プログラミング",
            "skillCount": 25,
            "averageLevel": 3.8
          },
          {
            "category": "データベース",
            "skillCount": 15,
            "averageLevel": 3.1
          }
        ]
      },
      "skillMatrix": {
        "categories": [
          {
            "id": "programming",
            "name": "プログラミング",
            "skills": [
              {
                "id": "javascript",
                "name": "JavaScript",
                "levels": {
                  "beginner": 5,
                  "intermediate": 15,
                  "advanced": 8,
                  "expert": 2
                },
                "averageLevel": 3.2,
                "trend": "increasing",
                "gapAnalysis": {
                  "currentLevel": 3.2,
                  "targetLevel": 3.5,
                  "gap": 0.3,
                  "priority": "medium"
                }
              },
              {
                "id": "python",
                "name": "Python",
                "levels": {
                  "beginner": 8,
                  "intermediate": 12,
                  "advanced": 5,
                  "expert": 1
                },
                "averageLevel": 2.8,
                "trend": "stable",
                "gapAnalysis": {
                  "currentLevel": 2.8,
                  "targetLevel": 3.2,
                  "gap": 0.4,
                  "priority": "high"
                }
              }
            ]
          }
        ],
        "departments": [
          {
            "id": "frontend",
            "name": "フロントエンド",
            "userCount": 15,
            "skillDistribution": {
              "javascript": {
                "average": 4.1,
                "distribution": [2, 5, 6, 2]
              },
              "react": {
                "average": 3.8,
                "distribution": [1, 4, 8, 2]
              }
            }
          },
          {
            "id": "backend",
            "name": "バックエンド",
            "userCount": 20,
            "skillDistribution": {
              "python": {
                "average": 3.5,
                "distribution": [3, 7, 8, 2]
              },
              "nodejs": {
                "average": 3.2,
                "distribution": [2, 8, 8, 2]
              }
            }
          }
        ]
      },
      "visualization": {
        "type": "heatmap",
        "data": {
          "heatmapData": [
            {
              "skill": "JavaScript",
              "department": "フロントエンド",
              "value": 4.1,
              "color": "#ff6b6b"
            },
            {
              "skill": "Python",
              "department": "バックエンド",
              "value": 3.5,
              "color": "#4ecdc4"
            }
          ],
          "chartConfig": {
            "width": 800,
            "height": 600,
            "colorScale": ["#e8f5e8", "#2d5a2d"],
            "legend": {
              "min": 1,
              "max": 5,
              "labels": ["初級", "中級", "上級", "エキスパート"]
            }
          }
        }
      },
      "recommendations": [
        {
          "type": "skill_gap",
          "priority": "high",
          "title": "Pythonスキル強化",
          "description": "バックエンドチームのPythonスキルレベルを向上させることを推奨",
          "targetSkill": "python",
          "targetDepartment": "backend",
          "currentLevel": 2.8,
          "targetLevel": 3.2,
          "suggestedActions": [
            "Python上級研修の実施",
            "メンタリングプログラムの導入",
            "実践プロジェクトへの参加"
          ]
        },
        {
          "type": "knowledge_sharing",
          "priority": "medium",
          "title": "フロントエンド知識共有",
          "description": "JavaScriptエキスパートによる知識共有セッション",
          "experts": ["user_001", "user_015"],
          "targetAudience": "初級・中級者",
          "suggestedFormat": "週次勉強会"
        }
      ],
      "exportUrls": {
        "pdf": "https://api.example.com/exports/skillmap_001.pdf",
        "excel": "https://api.example.com/exports/skillmap_001.xlsx",
        "png": "https://api.example.com/exports/skillmap_001.png"
      }
    }
  }
}
```

### 1.2 スキルマップ履歴取得

#### リクエスト
```http
GET /api/skills/map/history?targetId=org_001&limit=10
Authorization: Bearer {jwt_token}
```

#### クエリパラメータ
| パラメータ名 | 型      | 必須 | 説明                                           |
|--------------|---------|------|------------------------------------------------|
| targetId     | String  | Yes  | 対象ID                                         |
| limit        | Integer | No   | 取得件数（デフォルト: 10、最大: 50）           |
| dateFrom     | String  | No   | 開始日（YYYY-MM-DD形式）                       |
| dateTo       | String  | No   | 終了日（YYYY-MM-DD形式）                       |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "history": [
      {
        "id": "map_001",
        "generatedAt": "2025-05-30T11:00:00Z",
        "type": "organization",
        "targetName": "エンジニアリング部",
        "summary": {
          "totalUsers": 45,
          "totalSkills": 120,
          "averageSkillLevel": 3.2
        },
        "downloadUrl": "https://api.example.com/skillmaps/map_001"
      },
      {
        "id": "map_002",
        "generatedAt": "2025-05-15T11:00:00Z",
        "type": "organization",
        "targetName": "エンジニアリング部",
        "summary": {
          "totalUsers": 43,
          "totalSkills": 115,
          "averageSkillLevel": 3.1
        },
        "downloadUrl": "https://api.example.com/skillmaps/map_002"
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 3,
      "totalItems": 25,
      "hasNext": true
    }
  }
}
```

### 1.3 スキルマップ詳細取得

#### リクエスト
```http
GET /api/skills/map/{map_id}
Authorization: Bearer {jwt_token}
```

#### パスパラメータ
| パラメータ名 | 型     | 必須 | 説明           |
|--------------|--------|------|----------------|
| map_id       | String | Yes  | スキルマップID |

#### レスポンス（成功時）
```json
{
  "success": true,
  "data": {
    "skillMap": {
      "id": "map_001",
      "type": "organization",
      "targetId": "org_001",
      "targetName": "エンジニアリング部",
      "generatedAt": "2025-05-30T11:00:00Z",
      "parameters": {
        "filters": {
          "departments": ["engineering", "design"],
          "skillCategories": ["technical", "business"]
        },
        "visualization": {
          "type": "heatmap",
          "groupBy": "department"
        }
      },
      "data": "... (1.1と同じ詳細データ)"
    }
  }
}
```

## 2. エラーレスポンス

### 2.1 共通エラーフォーマット
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "エラーメッセージ",
    "details": "詳細情報"
  }
}
```

### 2.2 エラーコード一覧
| エラーコード | HTTPステータス | 説明 |
|-------------|---------------|------|
| INVALID_MAP_TYPE | 400 | 無効なマップ種別 |
| TARGET_NOT_FOUND | 404 | 対象が見つからない |
| INSUFFICIENT_DATA | 400 | データ不足でマップ生成不可 |
| INVALID_VISUALIZATION | 400 | 無効な可視化設定 |
| MAP_NOT_FOUND | 404 | スキルマップが見つからない |
| GENERATION_FAILED | 500 | マップ生成処理失敗 |
| EXPORT_FAILED | 500 | エクスポート処理失敗 |

## 3. 実装仕様

### 3.1 マップ種別
- **organization**: 組織全体のスキルマップ
- **department**: 部署別スキルマップ
- **team**: チーム別スキルマップ
- **individual**: 個人スキルマップ

### 3.2 可視化タイプ
- **heatmap**: ヒートマップ形式
- **radar**: レーダーチャート形式
- **bar**: 棒グラフ形式
- **bubble**: バブルチャート形式

### 3.3 集計方法
- **average**: 平均値
- **median**: 中央値
- **max**: 最大値
- **distribution**: 分布

## 4. パフォーマンス要件

| 項目 | 要件 |
|------|------|
| 生成時間 | 組織レベル: 30秒以内、部署レベル: 10秒以内 |
| 同時生成数 | 10件まで |
| データ保持期間 | 生成から6ヶ月 |
| エクスポートサイズ | PDF: 10MB以内、Excel: 5MB以内 |

## 5. 改訂履歴

| 改訂日     | 改訂者 | 改訂内容                                         |
|------------|--------|--------------------------------------------------|
| 2025/05/30 | 初版   | 初版作成                                         |
