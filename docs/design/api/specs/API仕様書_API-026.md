# API仕様書：API-026 スキルマップ生成API

## 1. 基本情報

- **API ID**: API-026
- **API名称**: スキルマップ生成API
- **概要**: スキルマップデータを生成する
- **エンドポイント**: `/api/skills/map`
- **HTTPメソッド**: POST
- **リクエスト形式**: JSON
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-SKILL-MAP](画面設計書_SCR-SKILL-MAP.md)
- **作成日**: 2025/05/28
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/28 初版作成

---

## 2. リクエスト仕様

### 2.1 リクエストヘッダ

| ヘッダ名 | 必須 | 説明 | 備考 |
|---------|------|------|------|
| Authorization | ○ | 認証トークン | Bearer {JWT} 形式 |
| Content-Type | ○ | リクエスト形式 | application/json |
| Accept | - | レスポンス形式 | application/json |

### 2.2 リクエストボディ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| map_type | string | ○ | マップタイプ | "radar", "bubble", "heatmap", "network" |
| target_users | array | - | 対象ユーザーID配列 | 指定なしの場合は自身のみ |
| department_id | string | - | 部署ID | 指定された部署に所属するユーザーが対象 |
| skill_categories | array | - | スキルカテゴリ配列 | 指定なしの場合は全カテゴリ |
| skill_ids | array | - | スキルID配列 | 指定なしの場合は全スキル |
| year | number | - | 対象年度 | 指定なしの場合は最新年度 |
| include_average | boolean | - | 平均値を含めるか | デフォルト: false |
| group_by | string | - | グループ化 | "department", "position", "none"<br>デフォルト: "none" |
| visualization_options | object | - | 可視化オプション | マップタイプ別のオプション |

#### visualization_options オブジェクト（マップタイプ別）

##### radar マップの場合

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| max_skills | number | - | 最大スキル数 | デフォルト: 10 |
| sort_by | string | - | ソート条件 | "level", "name", "category"<br>デフォルト: "level" |
| fill_area | boolean | - | 塗りつぶし表示 | デフォルト: true |

##### bubble マップの場合

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| max_skills | number | - | 最大スキル数 | デフォルト: 50 |
| size_by | string | - | サイズ基準 | "level", "experience_years", "popularity"<br>デフォルト: "level" |
| color_by | string | - | 色分け基準 | "category", "level", "experience_years"<br>デフォルト: "category" |

##### heatmap マップの場合

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| max_users | number | - | 最大ユーザー数 | デフォルト: 20 |
| max_skills | number | - | 最大スキル数 | デフォルト: 30 |
| sort_users_by | string | - | ユーザーソート条件 | "name", "department", "position"<br>デフォルト: "department" |
| sort_skills_by | string | - | スキルソート条件 | "name", "category", "popularity"<br>デフォルト: "category" |

##### network マップの場合

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| max_nodes | number | - | 最大ノード数 | デフォルト: 100 |
| node_size_by | string | - | ノードサイズ基準 | "level", "experience_years", "popularity"<br>デフォルト: "level" |
| edge_threshold | number | - | エッジ閾値 | 0.0-1.0の範囲<br>デフォルト: 0.5 |
| layout | string | - | レイアウト | "force", "circular", "hierarchical"<br>デフォルト: "force" |

### 2.3 リクエスト例

```json
{
  "map_type": "radar",
  "target_users": ["U12345", "U67890"],
  "skill_categories": ["technical", "business"],
  "year": 2025,
  "include_average": true,
  "visualization_options": {
    "max_skills": 8,
    "sort_by": "level",
    "fill_area": true
  }
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| map_type | string | マップタイプ | |
| generated_at | string | 生成日時 | ISO 8601形式 |
| year | number | 対象年度 | |
| data | object | マップデータ | マップタイプ別のデータ構造 |
| metadata | object | メタデータ | |

#### metadata オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_count | number | ユーザー数 | |
| skill_count | number | スキル数 | |
| categories | array | カテゴリ情報 | |
| visualization_options | object | 可視化オプション | リクエストと同じ構造 |

#### data オブジェクト（マップタイプ別）

##### radar マップの場合

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| axes | array | 軸情報の配列 | |
| series | array | データ系列の配列 | |

###### axes 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| name | string | スキル名 | |
| category | string | カテゴリ | |
| max_value | number | 最大値 | 通常は5（最大レベル） |

###### series 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | average の場合は "average" |
| name | string | ユーザー名/グループ名 | |
| color | string | 表示色 | HEX形式（例: "#007bff"） |
| values | array | 値の配列 | axes配列と同じ順序 |
| is_average | boolean | 平均値かどうか | |

##### bubble マップの場合

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| nodes | array | ノード情報の配列 | |
| categories | array | カテゴリ情報の配列 | |

###### nodes 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| id | string | ノードID | スキルID |
| name | string | スキル名 | |
| category | string | カテゴリ | |
| value | number | 値（サイズ） | |
| color_value | number | 色分け値 | |
| user_data | array | ユーザー別データ | |

###### user_data 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| name | string | ユーザー名 | |
| level | number | スキルレベル | |
| experience_years | number | 経験年数 | |

##### heatmap マップの場合

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| x_axis | array | X軸情報（スキル） | |
| y_axis | array | Y軸情報（ユーザー） | |
| values | array | 値の二次元配列 | |

###### x_axis 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| name | string | スキル名 | |
| category | string | カテゴリ | |

###### y_axis 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| name | string | ユーザー名 | |
| department | string | 部署名 | |
| position | string | 役職名 | |

##### network マップの場合

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| nodes | array | ノード情報の配列 | |
| edges | array | エッジ情報の配列 | |

###### nodes 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| id | string | ノードID | スキルIDまたはユーザーID |
| name | string | 名前 | スキル名またはユーザー名 |
| type | string | タイプ | "skill" または "user" |
| category | string | カテゴリ | スキルの場合はスキルカテゴリ<br>ユーザーの場合は部署名 |
| size | number | サイズ | |

###### edges 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| source | string | 始点ノードID | |
| target | string | 終点ノードID | |
| weight | number | 重み | 0.0-1.0の範囲 |
| type | string | タイプ | "user_skill", "skill_relation" |

### 3.2 正常時レスポンス例（radar マップの場合）

```json
{
  "map_type": "radar",
  "generated_at": "2025-05-28T15:30:00+09:00",
  "year": 2025,
  "data": {
    "axes": [
      {
        "skill_id": "S001",
        "name": "Java",
        "category": "technical",
        "max_value": 5
      },
      {
        "skill_id": "S002",
        "name": "Spring Framework",
        "category": "technical",
        "max_value": 5
      },
      {
        "skill_id": "S005",
        "name": "JavaScript",
        "category": "technical",
        "max_value": 5
      },
      {
        "skill_id": "S007",
        "name": "React",
        "category": "technical",
        "max_value": 5
      },
      {
        "skill_id": "S010",
        "name": "SQL",
        "category": "technical",
        "max_value": 5
      },
      {
        "skill_id": "S020",
        "name": "プロジェクト管理",
        "category": "business",
        "max_value": 5
      },
      {
        "skill_id": "S021",
        "name": "要件定義",
        "category": "business",
        "max_value": 5
      },
      {
        "skill_id": "S022",
        "name": "システム設計",
        "category": "business",
        "max_value": 5
      }
    ],
    "series": [
      {
        "user_id": "U12345",
        "name": "山田 太郎",
        "color": "#007bff",
        "values": [4, 3, 3, 2, 4, 3, 3, 4],
        "is_average": false
      },
      {
        "user_id": "U67890",
        "name": "鈴木 花子",
        "color": "#28a745",
        "values": [3, 2, 4, 4, 3, 2, 3, 2],
        "is_average": false
      },
      {
        "user_id": "average",
        "name": "平均",
        "color": "#dc3545",
        "values": [3.5, 2.5, 3.5, 3, 3.5, 2.5, 3, 3],
        "is_average": true
      }
    ]
  },
  "metadata": {
    "user_count": 2,
    "skill_count": 8,
    "categories": [
      {
        "id": "technical",
        "name": "技術スキル",
        "color": "#007bff"
      },
      {
        "id": "business",
        "name": "業務知識",
        "color": "#28a745"
      }
    ],
    "visualization_options": {
      "max_skills": 8,
      "sort_by": "level",
      "fill_area": true
    }
  }
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_MAP_TYPE | マップタイプが不正です | 存在しないマップタイプ |
| 400 Bad Request | INVALID_USER_ID | ユーザーIDが不正です | 存在しないユーザーID |
| 400 Bad Request | INVALID_DEPARTMENT_ID | 部署IDが不正です | 存在しない部署ID |
| 400 Bad Request | INVALID_SKILL_CATEGORY | スキルカテゴリが不正です | 存在しないスキルカテゴリ |
| 400 Bad Request | INVALID_SKILL_ID | スキルIDが不正です | 存在しないスキルID |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | スキルマップ生成権限なし |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_MAP_TYPE",
    "message": "マップタイプが不正です",
    "details": "指定されたマップタイプ 'tree' は存在しません。有効なマップタイプ: radar, bubble, heatmap, network"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - スキルマップ生成権限（PERM_GENERATE_SKILL_MAP）の確認
2. リクエストパラメータの検証
   - マップタイプの検証
   - ユーザーID、部署ID、スキルカテゴリ、スキルIDの存在チェック
   - 可視化オプションの検証
3. 対象ユーザーの決定
   - target_usersが指定されている場合はそのユーザー
   - department_idが指定されている場合はその部署のユーザー
   - どちらも指定がない場合は自身のみ
4. スキルデータの取得
   - 対象ユーザーのスキルデータを取得
   - 指定された年度のデータを取得
   - スキルカテゴリ、スキルIDでフィルタリング
5. マップデータの生成
   - マップタイプに応じたデータ構造の生成
   - 可視化オプションに基づく処理
   - 平均値の計算（include_average=trueの場合）
6. レスポンスの生成
   - 生成したマップデータを整形
7. レスポンス返却

### 4.2 マップタイプ別処理

#### radar マップ

- 各スキルを軸とするレーダーチャート形式
- max_skillsで指定された数のスキルを選択
- sort_byに基づいてスキルをソート
- 各ユーザーのスキルレベルを値として設定
- include_average=trueの場合は平均値も計算

#### bubble マップ

- スキルをノードとするバブルチャート形式
- max_skillsで指定された数のスキルを選択
- size_byに基づいてノードサイズを決定
- color_byに基づいてノード色を決定
- 各ユーザーのスキル情報をノードに紐づけ

#### heatmap マップ

- ユーザー×スキルのマトリクス形式
- max_users, max_skillsで指定された数のユーザー・スキルを選択
- sort_users_by, sort_skills_byに基づいてソート
- スキルレベルを色の濃さで表現

#### network マップ

- スキルとユーザーをノードとするネットワーク形式
- max_nodesで指定された数のノードを選択
- node_size_byに基づいてノードサイズを決定
- edge_thresholdを超える関連のみエッジとして表示
- layoutに基づいてノードの配置を決定

### 4.3 権限チェック

- 自身のスキルマップは常に生成可能
- 他ユーザーのスキルマップ生成には権限（PERM_GENERATE_SKILL_MAP）が必要
- 管理者（ROLE_ADMIN）は全ユーザーのスキルマップを生成可能
- 上長は自部門のメンバーのスキルマップを生成可能

### 4.4 パフォーマンス要件

- 大量のユーザー・スキルデータを処理する場合、処理時間が長くなる可能性がある
- 複雑なマップ（特にnetworkタイプ）の生成は、バックグラウンドジョブとして実行することも検討
- 生成結果はキャッシュされ、同一条件での再生成時に高速化
- 対象ユーザー数が多い場合（100人以上）は、サンプリングや集約処理を適用

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-021](API仕様書_API-021.md) | スキル情報取得API | ユーザースキル情報取得 |
| [API-023](API仕様書_API-023.md) | スキルマスタ取得API | スキルマスタ情報取得 |
| [API-025](API仕様書_API-025.md) | スキル検索API | 条件指定によるスキル検索 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| departments | 部署情報 | 参照（R） |
| positions | 役職情報 | 参照（R） |
| user_skills | ユーザースキル情報 | 参照（R） |
| skill_masters | スキルマスタ | 参照（R） |
| skill_categories | スキルカテゴリ | 参照（R） |
| skill_relations | スキル関連情報 | 参照（R） |

### 5.3 注意事項・補足

- スキルマップは人材育成・組織分析・プロジェクト編成などに活用
- マップデータは可視化ライブラリ（Chart.js, D3.js, ECharts等）で表示することを想定
- 生成されたマップデータは一時的に保存され、URLで共有可能
- 保存期間は生成から30日間
- エクスポート機能を利用する場合は別APIを使用（API-061 レポート生成API）
- 大規模なマップ生成はシステム負荷が高いため、利用頻度や時間帯に注意

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript + Chart.js）

```typescript
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Chart, RadarController, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js';
import { useParams } from 'react-router-dom';

// Chart.jsコンポーネントの登録
Chart.register(RadarController, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

interface SkillMapParams {
  map_type: 'radar' | 'bubble' | 'heatmap' | 'network';
  target_users?: string[];
  department_id?: string;
  skill_categories?: string[];
  skill_ids?: string[];
  year?: number;
  include_average?: boolean;
  group_by?: 'department' | 'position' | 'none';
  visualization_options?: any;
}

interface RadarMapData {
  axes: {
    skill_id: string;
    name: string;
    category: string;
    max_value: number;
  }[];
  series: {
    user_id: string;
    name: string;
    color: string;
    values: number[];
    is_average: boolean;
  }[];
}

interface SkillMapResponse {
  map_type: string;
  generated_at: string;
  year: number;
  data: RadarMapData | any;
  metadata: {
    user_count: number;
    skill_count: number;
    categories: {
      id: string;
      name: string;
      color: string;
    }[];
    visualization_options: any;
  };
}

const RadarSkillMap: React.FC = () => {
  const { departmentId } = useParams<{ departmentId?: string }>();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [mapData, setMapData] = useState<SkillMapResponse | null>(null);
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<Chart | null>(null);
  
  // マップ生成パラメータ
  const [mapParams, setMapParams] = useState<SkillMapParams>({
    map_type: 'radar',
    skill_categories: ['technical', 'business'],
    include_average: true,
    visualization_options: {
      max_skills: 8,
      sort_by: 'level',
      fill_area: true
    }
  });
  
  // 部署IDが指定されている場合は設定
  useEffect(() => {
    if (departmentId) {
      setMapParams(prev => ({
        ...prev,
        department_id: departmentId
      }));
    }
  }, [departmentId]);
  
  // スキルマップデータの取得
  useEffect(() => {
    const fetchSkillMap = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // APIリクエスト
        const response = await axios.post<SkillMapResponse>('/api/skills/map', mapParams, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
          }
        });
        
        setMapData(response.data);
        
      } catch (err) {
        if (axios.isAxiosError(err) && err.response) {
          const errorData = err.response.data;
          setError(errorData.error?.message || 'スキルマップの生成に失敗しました');
        } else {
          setError('スキルマップの生成中にエラーが発生しました');
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchSkillMap();
  }, [mapParams]);
  
  // Chart.jsでのレーダーチャート描画
  useEffect(() => {
    if (!mapData || mapData.map_type !== 'radar' || !chartRef.current) {
      return;
    }
    
    // 既存のチャートを破棄
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }
    
    const radarData = mapData.data as RadarMapData;
    
    // チャートデータの準備
    const data = {
      labels: radarData.axes.map(axis => axis.name),
      datasets: radarData.series.map(series => ({
        label: series.name,
        data: series.values,
        backgroundColor: series.is_average 
          ? 'rgba(220, 53, 69, 0.2)' // 平均値は赤色半透明
          : `${series.color}33`, // 透明度20%
        borderColor: series.color,
        borderWidth: series.is_average ? 2 : 1,
        pointBackgroundColor: series.color,
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: series.color,
        fill: mapData.metadata.visualization_options.fill_area
      }))
    };
    
    // チャートオプションの準備
    const options = {
      scales: {
        r: {
          angleLines: {
            display: true
          },
          suggestedMin: 0,
          suggestedMax: 5,
          ticks: {
            stepSize: 1
          }
        }
      },
      plugins: {
        legend: {
          position: 'top' as const,
        },
        tooltip: {
          callbacks: {
            title: (items: any) => {
              const index = items[0].dataIndex;
              return radarData.axes[index].name;
            },
            label: (context: any) => {
              const value = context.raw;
              const seriesName = context.dataset.label;
              return `${seriesName}: ${value}`;
            }
          }
        }
      }
    };
    
    // チャートの作成
    chartInstance.current = new Chart(chartRef.current, {
      type: 'radar',
      data,
      options
    });
    
    // クリーンアップ関数
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [mapData]);
  
  // マップパラメータの更新
  const handleParamChange = (field: keyof SkillMapParams, value: any) => {
    setMapParams(prev => ({
      ...prev,
      [field]: value
    }));
  };
  
  // 可視化オプションの更新
  const handleOptionChange = (field: string, value: any) => {
    setMapParams(prev => ({
      ...prev,
      visualization_options: {
        ...prev.visualization_options,
        [field]: value
      }
    }));
