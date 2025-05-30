# API定義書：API-003 権限情報取得API

## 1. 基本情報

- **API ID**: API-003
- **API名称**: 権限情報取得API
- **概要**: ユーザーの権限情報を取得する
- **エンドポイント**: `/api/auth/permissions`
- **HTTPメソッド**: GET
- **リクエスト形式**: クエリパラメータ
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-ACCESS](画面設計書_SCR-ACCESS.md)
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

### 2.2 リクエストパラメータ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| user_id | string | - | ユーザーID | 指定しない場合は認証済みユーザー自身の権限情報を取得<br>他ユーザーの権限情報取得には管理者権限が必要 |
| include_details | boolean | - | 詳細情報を含めるか | true: 詳細情報を含める, false: 基本情報のみ<br>デフォルト: false |

### 2.3 リクエスト例

```
GET /api/auth/permissions?user_id=U12345&include_details=true HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| username | string | ユーザー名 | |
| role | string | ユーザーロール | "admin", "manager", "user"のいずれか |
| permissions | array | 権限リスト | 付与されている権限のリスト |
| permission_groups | array | 権限グループ | 所属する権限グループのリスト（include_details=trueの場合のみ） |
| access_restrictions | object | アクセス制限情報 | アクセス制限の詳細（include_details=trueの場合のみ） |
| last_updated | string | 最終更新日時 | ISO 8601形式 |

#### permissions 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| permission_id | string | 権限ID | |
| name | string | 権限名 | |
| description | string | 権限の説明 | |
| granted_at | string | 権限付与日時 | ISO 8601形式 |
| granted_by | string | 権限付与者 | 権限を付与したユーザーID |

#### permission_groups 配列要素（include_details=trueの場合のみ）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| group_id | string | グループID | |
| name | string | グループ名 | |
| description | string | グループの説明 | |
| permissions | array | グループに含まれる権限リスト | 権限IDのリスト |

#### access_restrictions オブジェクト（include_details=trueの場合のみ）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| ip_restrictions | array | IP制限リスト | 許可されたIPアドレス/範囲のリスト |
| time_restrictions | array | 時間制限リスト | アクセス可能な時間帯のリスト |
| department_restrictions | array | 部署制限リスト | アクセス可能な部署のリスト |

### 3.2 正常時レスポンス例（基本情報のみ）

```json
{
  "user_id": "U12345",
  "username": "tanaka.taro",
  "role": "manager",
  "permissions": [
    {
      "permission_id": "PERM_VIEW_REPORTS",
      "name": "レポート閲覧",
      "description": "レポートの閲覧権限",
      "granted_at": "2025-01-15T10:30:00+09:00",
      "granted_by": "U00001"
    },
    {
      "permission_id": "PERM_EDIT_PROFILE",
      "name": "プロフィール編集",
      "description": "プロフィール情報の編集権限",
      "granted_at": "2025-01-15T10:30:00+09:00",
      "granted_by": "U00001"
    },
    {
      "permission_id": "PERM_MANAGE_TEAM",
      "name": "チーム管理",
      "description": "チームメンバーの管理権限",
      "granted_at": "2025-03-01T14:15:30+09:00",
      "granted_by": "U00001"
    }
  ],
  "last_updated": "2025-05-01T09:45:22+09:00"
}
```

### 3.3 正常時レスポンス例（詳細情報を含む）

```json
{
  "user_id": "U12345",
  "username": "tanaka.taro",
  "role": "manager",
  "permissions": [
    {
      "permission_id": "PERM_VIEW_REPORTS",
      "name": "レポート閲覧",
      "description": "レポートの閲覧権限",
      "granted_at": "2025-01-15T10:30:00+09:00",
      "granted_by": "U00001"
    },
    {
      "permission_id": "PERM_EDIT_PROFILE",
      "name": "プロフィール編集",
      "description": "プロフィール情報の編集権限",
      "granted_at": "2025-01-15T10:30:00+09:00",
      "granted_by": "U00001"
    },
    {
      "permission_id": "PERM_MANAGE_TEAM",
      "name": "チーム管理",
      "description": "チームメンバーの管理権限",
      "granted_at": "2025-03-01T14:15:30+09:00",
      "granted_by": "U00001"
    }
  ],
  "permission_groups": [
    {
      "group_id": "GROUP_MANAGER",
      "name": "マネージャーグループ",
      "description": "部門管理者向け権限グループ",
      "permissions": [
        "PERM_VIEW_REPORTS",
        "PERM_EDIT_PROFILE",
        "PERM_MANAGE_TEAM"
      ]
    }
  ],
  "access_restrictions": {
    "ip_restrictions": [
      "192.168.1.0/24",
      "10.0.0.5"
    ],
    "time_restrictions": [
      {
        "day_of_week": [1, 2, 3, 4, 5],
        "start_time": "08:00:00",
        "end_time": "20:00:00"
      }
    ],
    "department_restrictions": [
      "情報システム部",
      "人事部"
    ]
  },
  "last_updated": "2025-05-01T09:45:22+09:00"
}
```

### 3.4 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 他ユーザーの権限情報取得権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.5 エラー時レスポンス例

```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "権限がありません",
    "details": "他のユーザーの権限情報を取得するには管理者権限が必要です。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - 他ユーザーの権限情報取得の場合は管理者権限チェック
2. リクエストパラメータの検証
   - user_idの形式チェック（指定されている場合）
   - include_detailsの型チェック（指定されている場合）
3. 対象ユーザーの存在確認
   - 指定されたuser_idのユーザーが存在するか確認
   - 存在しない場合は404エラー
4. 権限情報の取得
   - ユーザーの基本情報取得
   - ユーザーに付与された権限リスト取得
   - include_details=trueの場合は詳細情報も取得
5. レスポンスの生成
   - 取得した情報を整形
6. レスポンス返却

### 4.2 権限管理ルール

- 権限は個別に付与または権限グループを通じて付与される
- 権限の継承関係：admin > manager > user
- 上位ロールは下位ロールの全権限を継承する
- 権限の付与・剥奪は監査ログに記録される
- 権限変更履歴は保持される

### 4.3 アクセス制限ルール

- IP制限：指定されたIPアドレス/範囲からのみアクセス可能
- 時間制限：指定された曜日・時間帯のみアクセス可能
- 部署制限：指定された部署のユーザーのみアクセス可能
- 制限は複数条件のAND条件で適用される

### 4.4 パフォーマンス要件

- レスポンスタイム：平均200ms以内
- キャッシュ：権限情報は10分間キャッシュ
- 同時リクエスト：最大50リクエスト/秒

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-001](API仕様書_API-001.md) | ユーザー認証API | ユーザー認証 |
| [API-002](API仕様書_API-002.md) | SSO認証API | SSO認証 |
| [API-004](API仕様書_API-004.md) | 権限設定API | ユーザー権限情報更新 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| user_roles | ユーザーロール | 参照（R） |
| permissions | 権限マスタ | 参照（R） |
| user_permissions | ユーザー権限割当 | 参照（R） |
| permission_groups | 権限グループ | 参照（R） |
| group_permissions | グループ権限割当 | 参照（R） |
| user_group_memberships | ユーザーグループ所属 | 参照（R） |
| access_restrictions | アクセス制限情報 | 参照（R） |

### 5.3 注意事項・補足

- 権限情報は頻繁に変更されないためキャッシュを活用
- 権限チェックは各APIで個別に行われる
- 権限IDの命名規則：PERM_[動作]_[対象]
- 権限グループIDの命名規則：GROUP_[名称]
- 権限情報の変更は監査ログに記録される

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Permission {
  permission_id: string;
  name: string;
  description: string;
  granted_at: string;
  granted_by: string;
}

interface PermissionGroup {
  group_id: string;
  name: string;
  description: string;
  permissions: string[];
}

interface AccessRestrictions {
  ip_restrictions: string[];
  time_restrictions: {
    day_of_week: number[];
    start_time: string;
    end_time: string;
  }[];
  department_restrictions: string[];
}

interface UserPermissions {
  user_id: string;
  username: string;
  role: string;
  permissions: Permission[];
  permission_groups?: PermissionGroup[];
  access_restrictions?: AccessRestrictions;
  last_updated: string;
}

const UserPermissionsComponent: React.FC<{ userId?: string }> = ({ userId }) => {
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [permissionsData, setPermissionsData] = useState<UserPermissions | null>(null);
  const [includeDetails, setIncludeDetails] = useState<boolean>(false);

  useEffect(() => {
    fetchPermissions();
  }, [userId, includeDetails]);

  const fetchPermissions = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // APIリクエストURLの構築
      let url = '/api/auth/permissions';
      const params = new URLSearchParams();
      
      if (userId) {
        params.append('user_id', userId);
      }
      
      params.append('include_details', includeDetails.toString());
      
      if (params.toString()) {
        url += `?${params.toString()}`;
      }
      
      // APIリクエスト
      const response = await axios.get<UserPermissions>(url, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Accept': 'application/json'
        }
      });
      
      // データの設定
      setPermissionsData(response.data);
      
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const errorData = err.response.data;
        setError(errorData.error?.message || '権限情報の取得に失敗しました');
      } else {
        setError('権限情報の取得中にエラーが発生しました');
      }
    } finally {
      setLoading(false);
    }
  };

  const toggleDetails = () => {
    setIncludeDetails(!includeDetails);
  };

  if (loading) {
    return <div className="loading">権限情報を読み込み中...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!permissionsData) {
    return <div className="no-data">権限情報がありません</div>;
  }

  return (
    <div className="user-permissions">
      <div className="header">
        <h2>ユーザー権限情報</h2>
        <button onClick={toggleDetails}>
          {includeDetails ? '基本情報のみ表示' : '詳細情報を表示'}
        </button>
      </div>
      
      <div className="user-info">
        <p><strong>ユーザーID:</strong> {permissionsData.user_id}</p>
        <p><strong>ユーザー名:</strong> {permissionsData.username}</p>
        <p><strong>ロール:</strong> {permissionsData.role}</p>
        <p><strong>最終更新:</strong> {new Date(permissionsData.last_updated).toLocaleString()}</p>
      </div>
      
      <div className="permissions-list">
        <h3>付与されている権限</h3>
        <table>
          <thead>
            <tr>
              <th>権限ID</th>
              <th>権限名</th>
              <th>説明</th>
              <th>付与日時</th>
              <th>付与者</th>
            </tr>
          </thead>
          <tbody>
            {permissionsData.permissions.map(perm => (
              <tr key={perm.permission_id}>
                <td>{perm.permission_id}</td>
                <td>{perm.name}</td>
                <td>{perm.description}</td>
                <td>{new Date(perm.granted_at).toLocaleString()}</td>
                <td>{perm.granted_by}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {includeDetails && permissionsData.permission_groups && (
        <div className="permission-groups">
          <h3>所属する権限グループ</h3>
          <table>
            <thead>
              <tr>
                <th>グループID</th>
                <th>グループ名</th>
                <th>説明</th>
                <th>含まれる権限</th>
              </tr>
            </thead>
            <tbody>
              {permissionsData.permission_groups.map(group => (
                <tr key={group.group_id}>
                  <td>{group.group_id}</td>
                  <td>{group.name}</td>
                  <td>{group.description}</td>
                  <td>{group.permissions.join(', ')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      
      {includeDetails && permissionsData.access_restrictions && (
        <div className="access-restrictions">
          <h3>アクセス制限</h3>
          
          <h4>IP制限</h4>
          <ul>
            {permissionsData.access_restrictions.ip_restrictions.map((ip, index) => (
              <li key={index}>{ip}</li>
            ))}
          </ul>
          
          <h4>時間制限</h4>
          <ul>
            {permissionsData.access_restrictions.time_restrictions.map((time, index) => {
              const days = time.day_of_week.map(day => {
                const dayNames = ['日', '月', '火', '水', '木', '金', '土'];
                return dayNames[day];
              }).join(', ');
              
              return (
                <li key={index}>
                  {days}曜日 {time.start_time} - {time.end_time}
                </li>
              );
            })}
          </ul>
          
          <h4>部署制限</h4>
          <ul>
            {permissionsData.access_restrictions.department_restrictions.map((dept, index) => (
              <li key={index}>{dept}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default UserPermissionsComponent;
```

### 6.2 バックエンド実装例（Java/Spring Boot）

```java
package com.example.skillreport.controller;

import com.example.skillreport.dto.UserPermissionsDto;
import com.example.skillreport.exception.PermissionDeniedException;
import com.example.skillreport.exception.ResourceNotFoundException;
import com.example.skillreport.service.PermissionService;
import com.example.skillreport.service.UserService;
import com.example.skillreport.util.SecurityUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/auth")
public class PermissionController {

    private final PermissionService permissionService;
    private final UserService userService;
    private final SecurityUtils securityUtils;

    @Autowired
    public PermissionController(
            PermissionService permissionService,
            UserService userService,
            SecurityUtils securityUtils) {
        this.permissionService = permissionService;
        this.userService = userService;
        this.securityUtils = securityUtils;
    }

    /**
     * ユーザーの権限情報を取得するAPI
     *
     * @param userId ユーザーID（指定しない場合は認証済みユーザー）
     * @param includeDetails 詳細情報を含めるか
     * @return ユーザーの権限情報
     */
    @GetMapping("/permissions")
    public ResponseEntity<UserPermissionsDto> getUserPermissions(
            @RequestParam(required = false) String userId,
            @RequestParam(required = false, defaultValue = "false") boolean includeDetails) {
        
        // 認証済みユーザーの取得
        String currentUserId = securityUtils.getCurrentUserId();
        
        // ユーザーIDが指定されていない場合は認証済みユーザーのIDを使用
        String targetUserId = (userId != null && !userId.isEmpty()) ? userId : currentUserId;
        
        // 他ユーザーの権限情報取得の場合は権限チェック
        if (!targetUserId.equals(currentUserId)) {
            if (!securityUtils.hasAdminPermission()) {
                throw new PermissionDeniedException("他のユーザーの権限情報を取得するには管理者権限が必要です。");
            }
        }
        
        // ユーザーの存在確認
        if (!userService.existsById(targetUserId)) {
            throw new ResourceNotFoundException("指定されたユーザーID: " + targetUserId + " が見つかりません。");
        }
        
        // 権限情報の取得
        UserPermissionsDto permissions = permissionService.getUserPermissions(targetUserId, includeDetails);
        
        return ResponseEntity.ok(permissions);
    }
}
```

### 6.3 権限チェック実装例（Java/Spring Boot）

```java
package com.example.skillreport.security;

import com.example.skillreport.exception.PermissionDeniedException;
import com.example.skillreport.model.User;
import com.example.skillreport.service.PermissionService;
import com.example.skillreport.util.SecurityUtils;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Set;

/**
 * 権限チェックを行うAspect
 */
@Aspect
@Component
public class PermissionCheckAspect {

    private final PermissionService permissionService;
    private final SecurityUtils securityUtils;

    @Autowired
    public PermissionCheckAspect(
            PermissionService permissionService,
            SecurityUtils securityUtils) {
        this.permissionService = permissionService;
        this.securityUtils = securityUtils;
    }

    /**
     * RequirePermission アノテーションが付与されたメソッドの実行前に権限チェックを行う
     *
     * @param joinPoint JoinPoint
     * @param requirePermission RequirePermission アノテーション
     */
    @Before("@annotation(requirePermission)")
    public void checkPermission(JoinPoint joinPoint, RequirePermission requirePermission) {
        // 必要な権限
        String requiredPermission = requirePermission.value();
        
        // 現在のユーザーID
        String currentUserId = securityUtils.getCurrentUserId();
        
        // ユーザーの権限リスト取得
        Set<String> userPermissions = permissionService.getUserPermissionIds(currentUserId);
        
        // 管理者は全ての権限を持つ
        if (userPermissions.contains("PERM_ADMIN")) {
            return;
        }
        
        // 権限チェック
        if (!userPermissions.contains(requiredPermission)) {
            throw new PermissionDeniedException("この操作を行うには " + requiredPermission + " 権限が必要です。");
        }
        
        // アクセス制限チェック
        checkAccessRestrictions(currentUserId);
    }
    
    /**
     * アクセス制限のチェック
     *
     * @param userId ユーザーID
     */
    private void checkAccessRestrictions(String userId) {
        // IP制限チェック
        if (!permissionService.checkIpRestriction(userId, securityUtils.getCurrentIpAddress())) {
            throw new PermissionDeniedException("現在のIPアドレスからはアクセスできません。");
        }
        
        // 時間制限チェック
        if (!permissionService.checkTimeRestriction(userId)) {
            throw new PermissionDeniedException("現在の時間帯はアクセスできません。");
        }
        
        // 部署制限チェック
        User currentUser = securityUtils.getCurrentUser();
        if (!permissionService.checkDepartmentRestriction(userId, currentUser.getDepartment())) {
            throw new PermissionDeniedException("所属部署からはアクセスできません。");
        }
    }
}
