# API仕様書：API-013 組織情報取得API

## 1. 基本情報

- **API ID**: API-013
- **API名称**: 組織情報取得API
- **概要**: 組織（部署・役職）の階層構造や詳細情報を取得する
- **エンドポイント**: `/api/organizations`
- **HTTPメソッド**: GET
- **リクエスト形式**: クエリパラメータ
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-ORG](画面設計書_SCR-ORG.md)
- **作成日**: 2025/05/28
- **作成者**: API設計担当
- **改訂履歴**: 2025/05/28 初版作成

---

## 2. リクエスト仕様

### 2.1 リクエストヘッダ

| ヘッダ名 | 必須 | 説明 | 備考 |
|---------|------|------|------|
| Authorization | ○ | 認証トークン | Bearer {JWT} 形式 |
| Accept | - | レスポンス形式 | application/json |

### 2.2 クエリパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| type | string | - | 取得する組織タイプ | "department"（部署）, "position"（役職）<br>指定しない場合は両方取得 |
| department_id | string | - | 部署ID | 指定した部署の詳細情報を取得<br>指定しない場合は全部署情報を取得 |
| include_members | boolean | - | メンバー情報を含めるか | true: メンバー情報を含める, false: 含めない<br>デフォルト: false |
| include_children | boolean | - | 子組織情報を含めるか | true: 子組織情報を含める, false: 含めない<br>デフォルト: true |
| include_positions | boolean | - | 役職情報を含めるか | true: 役職情報を含める, false: 含めない<br>デフォルト: false |

### 2.3 リクエスト例（全組織情報取得）

```
GET /api/organizations HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json
```

### 2.4 リクエスト例（特定部署の詳細情報取得）

```
GET /api/organizations?department_id=D100&include_members=true&include_children=true HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| departments | array | 部署情報リスト | type="department"または未指定の場合 |
| positions | array | 役職情報リスト | type="position"または未指定の場合 |
| last_updated | string | 最終更新日時 | ISO 8601形式 |

#### departments 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| department_id | string | 部署ID | |
| name | string | 部署名 | |
| code | string | 部署コード | |
| description | string | 部署説明 | |
| parent_id | string | 親部署ID | トップレベル部署の場合はnull |
| manager_id | string | 部署管理者ID | |
| level | number | 階層レベル | トップレベル=1 |
| path | string | 部署パス | 上位部署からのパス（例: "/本社/営業本部/営業1部"） |
| members | array | 所属メンバー | include_members=trueの場合のみ |
| children | array | 子部署 | include_children=trueの場合のみ |
| positions | array | 関連役職 | include_positions=trueの場合のみ |
| created_at | string | 作成日時 | ISO 8601形式 |
| updated_at | string | 更新日時 | ISO 8601形式 |

#### members 配列要素（include_members=trueの場合のみ）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| username | string | ユーザー名 | |
| display_name | string | 表示名 | |
| email | string | メールアドレス | |
| position | object | 役職情報 | |
| join_date | string | 部署配属日 | ISO 8601形式（YYYY-MM-DD） |

#### positions 配列要素（type="position"または未指定の場合）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| position_id | string | 役職ID | |
| name | string | 役職名 | |
| code | string | 役職コード | |
| description | string | 役職説明 | |
| level | number | 役職レベル | 数値が大きいほど上位役職 |
| is_manager | boolean | 管理職フラグ | |
| department_type | string | 適用部署タイプ | "all", "head_office", "branch"など |
| created_at | string | 作成日時 | ISO 8601形式 |
| updated_at | string | 更新日時 | ISO 8601形式 |

### 3.2 正常時レスポンス例（全組織情報）

```json
{
  "departments": [
    {
      "department_id": "D001",
      "name": "本社",
      "code": "HQ",
      "description": "本社機能を担う組織",
      "parent_id": null,
      "manager_id": "U00001",
      "level": 1,
      "path": "/本社",
      "created_at": "2020-04-01T00:00:00+09:00",
      "updated_at": "2024-04-01T10:00:00+09:00",
      "children": [
        {
          "department_id": "D100",
          "name": "情報システム部",
          "code": "IS",
          "description": "社内システムの開発・運用を担当",
          "parent_id": "D001",
          "manager_id": "U00010",
          "level": 2,
          "path": "/本社/情報システム部",
          "created_at": "2020-04-01T00:00:00+09:00",
          "updated_at": "2024-04-01T10:00:00+09:00"
        },
        {
          "department_id": "D200",
          "name": "人事部",
          "code": "HR",
          "description": "人事・採用業務を担当",
          "parent_id": "D001",
          "manager_id": "U00020",
          "level": 2,
          "path": "/本社/人事部",
          "created_at": "2020-04-01T00:00:00+09:00",
          "updated_at": "2024-04-01T10:00:00+09:00"
        }
      ]
    }
  ],
  "positions": [
    {
      "position_id": "P001",
      "name": "社長",
      "code": "CEO",
      "description": "最高経営責任者",
      "level": 10,
      "is_manager": true,
      "department_type": "all",
      "created_at": "2020-04-01T00:00:00+09:00",
      "updated_at": "2020-04-01T00:00:00+09:00"
    },
    {
      "position_id": "P100",
      "name": "部長",
      "code": "GM",
      "description": "部門責任者",
      "level": 7,
      "is_manager": true,
      "department_type": "all",
      "created_at": "2020-04-01T00:00:00+09:00",
      "updated_at": "2020-04-01T00:00:00+09:00"
    },
    {
      "position_id": "P200",
      "name": "課長",
      "code": "MGR",
      "description": "課責任者",
      "level": 5,
      "is_manager": true,
      "department_type": "all",
      "created_at": "2020-04-01T00:00:00+09:00",
      "updated_at": "2020-04-01T00:00:00+09:00"
    },
    {
      "position_id": "P300",
      "name": "主任",
      "code": "TL",
      "description": "チームリーダー",
      "level": 3,
      "is_manager": false,
      "department_type": "all",
      "created_at": "2020-04-01T00:00:00+09:00",
      "updated_at": "2020-04-01T00:00:00+09:00"
    },
    {
      "position_id": "P400",
      "name": "一般社員",
      "code": "STF",
      "description": "一般社員",
      "level": 1,
      "is_manager": false,
      "department_type": "all",
      "created_at": "2020-04-01T00:00:00+09:00",
      "updated_at": "2020-04-01T00:00:00+09:00"
    }
  ],
  "last_updated": "2025-05-15T10:30:00+09:00"
}
```

### 3.3 正常時レスポンス例（特定部署の詳細情報）

```json
{
  "departments": [
    {
      "department_id": "D100",
      "name": "情報システム部",
      "code": "IS",
      "description": "社内システムの開発・運用を担当",
      "parent_id": "D001",
      "manager_id": "U00010",
      "level": 2,
      "path": "/本社/情報システム部",
      "members": [
        {
          "user_id": "U00010",
          "username": "yamada.taro",
          "display_name": "山田 太郎",
          "email": "yamada.taro@example.com",
          "position": {
            "position_id": "P100",
            "name": "部長"
          },
          "join_date": "2020-04-01"
        },
        {
          "user_id": "U00011",
          "username": "suzuki.hanako",
          "display_name": "鈴木 花子",
          "email": "suzuki.hanako@example.com",
          "position": {
            "position_id": "P200",
            "name": "課長"
          },
          "join_date": "2021-04-01"
        },
        {
          "user_id": "U12345",
          "username": "tanaka.taro",
          "display_name": "田中 太郎",
          "email": "tanaka.taro@example.com",
          "position": {
            "position_id": "P300",
            "name": "主任"
          },
          "join_date": "2022-04-01"
        }
      ],
      "children": [
        {
          "department_id": "D110",
          "name": "システム開発課",
          "code": "IS-DEV",
          "description": "システム開発を担当",
          "parent_id": "D100",
          "manager_id": "U00011",
          "level": 3,
          "path": "/本社/情報システム部/システム開発課",
          "created_at": "2020-04-01T00:00:00+09:00",
          "updated_at": "2024-04-01T10:00:00+09:00"
        },
        {
          "department_id": "D120",
          "name": "インフラ運用課",
          "code": "IS-INF",
          "description": "インフラ運用を担当",
          "parent_id": "D100",
          "manager_id": "U00012",
          "level": 3,
          "path": "/本社/情報システム部/インフラ運用課",
          "created_at": "2020-04-01T00:00:00+09:00",
          "updated_at": "2024-04-01T10:00:00+09:00"
        }
      ],
      "created_at": "2020-04-01T00:00:00+09:00",
      "updated_at": "2024-04-01T10:00:00+09:00"
    }
  ],
  "last_updated": "2025-05-15T10:30:00+09:00"
}
```

### 3.4 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 組織情報閲覧権限なし |
| 404 Not Found | DEPARTMENT_NOT_FOUND | 部署が見つかりません | 指定された部署IDが存在しない |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.5 エラー時レスポンス例

```json
{
  "error": {
    "code": "DEPARTMENT_NOT_FOUND",
    "message": "部署が見つかりません",
    "details": "指定された部署ID 'D999' は存在しません。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - 組織情報閲覧権限（PERM_VIEW_ORGANIZATIONS）の確認
2. リクエストパラメータの検証
   - typeの値チェック
   - department_idの形式チェック（指定されている場合）
   - 論理パラメータの型チェック
3. 組織情報の取得
   - typeに応じた情報取得
   - department_idが指定されている場合は該当部署の詳細情報取得
   - include_membersがtrueの場合はメンバー情報も取得
   - include_childrenがtrueの場合は子組織情報も取得
   - include_positionsがtrueの場合は役職情報も取得
4. レスポンスの生成
   - 取得した情報を整形
5. レスポンス返却

### 4.2 組織情報取得ルール

- 基本的な組織情報は全ユーザーが閲覧可能
- 詳細な組織情報（メンバー情報など）は権限（PERM_VIEW_ORGANIZATIONS）が必要
- 部署は階層構造で管理され、親子関係を持つ
- 役職は階層構造ではなく、レベル値で上下関係を表現
- 組織情報は人事システムと連携して定期的に更新される
- 組織変更履歴は保持され、過去の組織構造も参照可能（別APIで提供）

### 4.3 パフォーマンス要件

- レスポンスタイム：平均300ms以内
- キャッシュ：組織情報は1時間キャッシュ
- 同時リクエスト：最大30リクエスト/秒

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-011](API仕様書_API-011.md) | プロフィール取得API | ユーザープロフィール情報取得 |
| [API-012](API仕様書_API-012.md) | プロフィール更新API | ユーザープロフィール情報更新 |
| [API-014](API仕様書_API-014.md) | 組織変更履歴取得API | 組織変更履歴情報取得 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| departments | 部署情報 | 参照（R） |
| positions | 役職情報 | 参照（R） |
| users | ユーザー基本情報 | 参照（R） |
| user_departments | ユーザー部署所属情報 | 参照（R） |
| user_positions | ユーザー役職情報 | 参照（R） |
| department_hierarchy | 部署階層関係 | 参照（R） |

### 5.3 注意事項・補足

- 組織情報は人事システムのマスターデータと同期
- 組織変更は四半期ごとに実施されるため、その前後で情報が大きく変わる可能性あり
- 兼務情報は含まれない（別APIで提供）
- 組織情報のキャッシュは1時間ごとに更新
- 大規模な組織階層の取得は処理負荷が高いため、必要な情報のみ取得することを推奨

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Position {
  position_id: string;
  name: string;
  code: string;
  description: string;
  level: number;
  is_manager: boolean;
  department_type: string;
  created_at: string;
  updated_at: string;
}

interface Member {
  user_id: string;
  username: string;
  display_name: string;
  email: string;
  position: {
    position_id: string;
    name: string;
  };
  join_date: string;
}

interface Department {
  department_id: string;
  name: string;
  code: string;
  description: string;
  parent_id: string | null;
  manager_id: string;
  level: number;
  path: string;
  members?: Member[];
  children?: Department[];
  positions?: Position[];
  created_at: string;
  updated_at: string;
}

interface OrganizationResponse {
  departments?: Department[];
  positions?: Position[];
  last_updated: string;
}

const OrganizationComponent: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [organizationData, setOrganizationData] = useState<OrganizationResponse | null>(null);
  const [selectedDepartment, setSelectedDepartment] = useState<string | null>(null);
  const [includeMembers, setIncludeMembers] = useState<boolean>(false);
  const [includePositions, setIncludePositions] = useState<boolean>(false);

  useEffect(() => {
    fetchOrganizationData();
  }, [selectedDepartment, includeMembers, includePositions]);

  const fetchOrganizationData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // APIリクエストURLの構築
      let url = '/api/organizations';
      const params = new URLSearchParams();
      
      if (selectedDepartment) {
        params.append('department_id', selectedDepartment);
      }
      
      if (includeMembers) {
        params.append('include_members', 'true');
      }
      
      if (includePositions) {
        params.append('include_positions', 'true');
      }
      
      // 常に子組織情報を含める
      params.append('include_children', 'true');
      
      if (params.toString()) {
        url += `?${params.toString()}`;
      }
      
      // APIリクエスト
      const response = await axios.get<OrganizationResponse>(url, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Accept': 'application/json'
        }
      });
      
      // データの設定
      setOrganizationData(response.data);
      
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const errorData = err.response.data;
        setError(errorData.error?.message || '組織情報の取得に失敗しました');
      } else {
        setError('組織情報の取得中にエラーが発生しました');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDepartmentSelect = (departmentId: string) => {
    setSelectedDepartment(departmentId);
  };

  const toggleIncludeMembers = () => {
    setIncludeMembers(!includeMembers);
  };

  const toggleIncludePositions = () => {
    setIncludePositions(!includePositions);
  };

  const renderDepartmentTree = (departments: Department[] | undefined) => {
    if (!departments || departments.length === 0) {
      return <div>部署情報がありません</div>;
    }

    return (
      <ul className="department-tree">
        {departments.map(dept => (
          <li key={dept.department_id}>
            <div 
              className={`department-item ${selectedDepartment === dept.department_id ? 'selected' : ''}`}
              onClick={() => handleDepartmentSelect(dept.department_id)}
            >
              <span className="department-name">{dept.name}</span>
              <span className="department-code">({dept.code})</span>
            </div>
            
            {dept.children && dept.children.length > 0 && (
              renderDepartmentTree(dept.children)
            )}
          </li>
        ))}
      </ul>
    );
  };

  const renderDepartmentDetail = (department: Department | undefined) => {
    if (!department) {
      return <div>部署を選択してください</div>;
    }

    return (
      <div className="department-detail">
        <h3>{department.name}</h3>
        <p className="department-path">{department.path}</p>
        
        <div className="department-info">
          <p><strong>部署コード:</strong> {department.code}</p>
          <p><strong>説明:</strong> {department.description}</p>
          <p><strong>レベル:</strong> {department.level}</p>
          <p><strong>作成日:</strong> {new Date(department.created_at).toLocaleDateString()}</p>
          <p><strong>更新日:</strong> {new Date(department.updated_at).toLocaleDateString()}</p>
        </div>
        
        {department.members && department.members.length > 0 && (
          <div className="department-members">
            <h4>所属メンバー</h4>
            <table>
              <thead>
                <tr>
                  <th>名前</th>
                  <th>ユーザー名</th>
                  <th>メールアドレス</th>
                  <th>役職</th>
                  <th>配属日</th>
                </tr>
              </thead>
              <tbody>
                {department.members.map(member => (
                  <tr key={member.user_id}>
                    <td>{member.display_name}</td>
                    <td>{member.username}</td>
                    <td>{member.email}</td>
                    <td>{member.position.name}</td>
                    <td>{new Date(member.join_date).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    );
  };

  const renderPositionList = (positions: Position[] | undefined) => {
    if (!positions || positions.length === 0) {
      return <div>役職情報がありません</div>;
    }

    return (
      <div className="position-list">
        <h3>役職一覧</h3>
        <table>
          <thead>
            <tr>
              <th>役職名</th>
              <th>コード</th>
              <th>説明</th>
              <th>レベル</th>
              <th>管理職</th>
            </tr>
          </thead>
          <tbody>
            {positions.map(position => (
              <tr key={position.position_id}>
                <td>{position.name}</td>
                <td>{position.code}</td>
                <td>{position.description}</td>
                <td>{position.level}</td>
                <td>{position.is_manager ? 'はい' : 'いいえ'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  if (loading) {
    return <div className="loading">組織情報を読み込み中...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!organizationData) {
    return <div className="no-data">組織情報がありません</div>;
  }

  // 選択された部署の詳細情報を取得
  const selectedDepartmentDetail = selectedDepartment 
    ? organizationData.departments?.find(d => d.department_id === selectedDepartment) 
    : organizationData.departments?.[0];

  return (
    <div className="organization-view">
      <div className="organization-header">
        <h2>組織情報</h2>
        <div className="last-updated">
          最終更新: {new Date(organizationData.last_updated).toLocaleString()}
        </div>
        <div className="view-options">
          <label>
            <input 
              type="checkbox" 
              checked={includeMembers} 
              onChange={toggleIncludeMembers} 
            />
            メンバー情報を表示
          </label>
          <label>
            <input 
              type="checkbox" 
              checked={includePositions} 
              onChange={toggleIncludePositions} 
            />
            役職情報を表示
          </label>
        </div>
      </div>
      
      <div className="organization-content">
        <div className="department-tree-container">
          <h3>部署一覧</h3>
          {renderDepartmentTree(organizationData.departments)}
        </div>
        
        <div className="department-detail-container">
          {renderDepartmentDetail(selectedDepartmentDetail)}
        </div>
      </div>
      
      {includePositions && organizationData.positions && (
        <div className="position-container">
          {renderPositionList(organizationData.positions)}
        </div>
      )}
    </div>
  );
};

export default OrganizationComponent;
```

### 6.2 バックエンド実装例（Java/Spring Boot）

```java
package com.example.skillreport.controller;

import com.example.skillreport.dto.DepartmentDto;
import com.example.skillreport.dto.OrganizationResponseDto;
import com.example.skillreport.dto.PositionDto;
import com.example.skillreport.exception.ResourceNotFoundException;
import com.example.skillreport.service.OrganizationService;
import com.example.skillreport.util.SecurityUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/organizations")
public class OrganizationController {

    private final OrganizationService organizationService;
    private final SecurityUtils securityUtils;

    @Autowired
    public OrganizationController(
            OrganizationService organizationService,
            SecurityUtils securityUtils) {
        this.organizationService = organizationService;
        this.securityUtils = securityUtils;
    }

    /**
     * 組織情報を取得するAPI
     *
     * @param type 取得する組織タイプ
     * @param departmentId 部署ID
