# API定義書：API-004 権限設定API

## 1. 基本情報

- **API ID**: API-004
- **API名称**: 権限設定API
- **概要**: ユーザーの権限情報を更新する
- **エンドポイント**: `/api/auth/permissions`
- **HTTPメソッド**: PUT
- **リクエスト形式**: JSON
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
| Content-Type | ○ | コンテンツタイプ | application/json |
| Accept | - | レスポンス形式 | application/json |

### 2.2 リクエストボディ

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| user_id | string | ○ | ユーザーID | 権限を設定するユーザーのID |
| role | string | - | ユーザーロール | "admin", "manager", "user"のいずれか<br>指定しない場合は現在のロールを維持 |
| permissions | array | - | 権限リスト | 付与する権限IDのリスト<br>指定しない場合は現在の権限を維持 |
| permission_groups | array | - | 権限グループリスト | 所属させる権限グループIDのリスト<br>指定しない場合は現在のグループを維持 |
| access_restrictions | object | - | アクセス制限情報 | アクセス制限の設定<br>指定しない場合は現在の制限を維持 |
| operation_type | string | ○ | 操作タイプ | "add"（追加）, "remove"（削除）, "replace"（置換）のいずれか |
| reason | string | ○ | 変更理由 | 権限変更の理由（監査目的） |

#### permissions 配列要素

権限IDの文字列配列

```json
["PERM_VIEW_REPORTS", "PERM_EDIT_PROFILE", "PERM_MANAGE_TEAM"]
```

#### permission_groups 配列要素

権限グループIDの文字列配列

```json
["GROUP_MANAGER", "GROUP_REPORT_VIEWER"]
```

#### access_restrictions オブジェクト

| パラメータ名 | 型 | 必須 | 説明 | 制約・備考 |
|------------|------|------|------|------------|
| ip_restrictions | array | - | IP制限リスト | 許可するIPアドレス/範囲のリスト |
| time_restrictions | array | - | 時間制限リスト | アクセス可能な時間帯のリスト |
| department_restrictions | array | - | 部署制限リスト | アクセス可能な部署のリスト |

### 2.3 リクエスト例（権限追加）

```json
{
  "user_id": "U12345",
  "permissions": ["PERM_VIEW_REPORTS", "PERM_EXPORT_DATA"],
  "operation_type": "add",
  "reason": "データエクスポート機能の利用権限を追加"
}
```

### 2.4 リクエスト例（権限削除）

```json
{
  "user_id": "U12345",
  "permissions": ["PERM_MANAGE_USERS"],
  "operation_type": "remove",
  "reason": "ユーザー管理権限の剥奪（部署異動のため）"
}
```

### 2.5 リクエスト例（権限置換）

```json
{
  "user_id": "U12345",
  "role": "manager",
  "permissions": ["PERM_VIEW_REPORTS", "PERM_EDIT_PROFILE", "PERM_MANAGE_TEAM"],
  "permission_groups": ["GROUP_MANAGER"],
  "access_restrictions": {
    "ip_restrictions": ["192.168.1.0/24", "10.0.0.5"],
    "time_restrictions": [
      {
        "day_of_week": [1, 2, 3, 4, 5],
        "start_time": "08:00:00",
        "end_time": "20:00:00"
      }
    ],
    "department_restrictions": ["情報システム部", "人事部"]
  },
  "operation_type": "replace",
  "reason": "マネージャー昇格に伴う権限設定"
}
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| user_id | string | ユーザーID | |
| username | string | ユーザー名 | |
| role | string | 更新後のユーザーロール | "admin", "manager", "user"のいずれか |
| permissions | array | 更新後の権限リスト | 付与されている権限のリスト |
| permission_groups | array | 更新後の権限グループ | 所属する権限グループのリスト |
| access_restrictions | object | 更新後のアクセス制限情報 | アクセス制限の詳細 |
| updated_by | string | 更新者 | 更新を行ったユーザーのID |
| updated_at | string | 更新日時 | ISO 8601形式 |
| change_summary | object | 変更内容サマリー | 追加/削除された権限の概要 |

#### permissions 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| permission_id | string | 権限ID | |
| name | string | 権限名 | |
| description | string | 権限の説明 | |

#### permission_groups 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| group_id | string | グループID | |
| name | string | グループ名 | |
| description | string | グループの説明 | |

#### access_restrictions オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| ip_restrictions | array | IP制限リスト | 許可されたIPアドレス/範囲のリスト |
| time_restrictions | array | 時間制限リスト | アクセス可能な時間帯のリスト |
| department_restrictions | array | 部署制限リスト | アクセス可能な部署のリスト |

#### change_summary オブジェクト

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| added | array | 追加された権限 | 権限IDのリスト |
| removed | array | 削除された権限 | 権限IDのリスト |
| role_changed | boolean | ロール変更有無 | ロールが変更された場合true |
| groups_changed | boolean | グループ変更有無 | グループが変更された場合true |
| restrictions_changed | boolean | 制限変更有無 | アクセス制限が変更された場合true |

### 3.2 正常時レスポンス例

```json
{
  "user_id": "U12345",
  "username": "tanaka.taro",
  "role": "manager",
  "permissions": [
    {
      "permission_id": "PERM_VIEW_REPORTS",
      "name": "レポート閲覧",
      "description": "レポートの閲覧権限"
    },
    {
      "permission_id": "PERM_EDIT_PROFILE",
      "name": "プロフィール編集",
      "description": "プロフィール情報の編集権限"
    },
    {
      "permission_id": "PERM_MANAGE_TEAM",
      "name": "チーム管理",
      "description": "チームメンバーの管理権限"
    },
    {
      "permission_id": "PERM_EXPORT_DATA",
      "name": "データエクスポート",
      "description": "データのエクスポート権限"
    }
  ],
  "permission_groups": [
    {
      "group_id": "GROUP_MANAGER",
      "name": "マネージャーグループ",
      "description": "部門管理者向け権限グループ"
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
  "updated_by": "U00001",
  "updated_at": "2025-05-28T15:30:45+09:00",
  "change_summary": {
    "added": ["PERM_EXPORT_DATA"],
    "removed": [],
    "role_changed": false,
    "groups_changed": false,
    "restrictions_changed": false
  }
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_OPERATION | 操作タイプが不正です | 不正なoperation_type |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | 権限設定権限なし |
| 404 Not Found | USER_NOT_FOUND | ユーザーが見つかりません | 指定されたユーザーIDが存在しない |
| 404 Not Found | PERMISSION_NOT_FOUND | 権限が見つかりません | 指定された権限IDが存在しない |
| 404 Not Found | GROUP_NOT_FOUND | 権限グループが見つかりません | 指定されたグループIDが存在しない |
| 409 Conflict | ROLE_PERMISSION_CONFLICT | ロールと権限が矛盾しています | 指定されたロールと権限の組み合わせが不正 |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "PERMISSION_NOT_FOUND",
    "message": "権限が見つかりません",
    "details": "指定された権限ID 'PERM_INVALID_PERMISSION' は存在しません。"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - 権限設定権限（PERM_MANAGE_PERMISSIONS）の確認
2. リクエストパラメータの検証
   - 必須パラメータの存在確認
   - パラメータ形式チェック
   - 操作タイプの検証
3. 対象ユーザーの存在確認
   - 指定されたuser_idのユーザーが存在するか確認
   - 存在しない場合は404エラー
4. 権限・グループの存在確認
   - 指定された権限IDが存在するか確認
   - 指定されたグループIDが存在するか確認
   - 存在しない場合は404エラー
5. 権限の整合性チェック
   - ロールと権限の組み合わせが適切か確認
   - 不適切な場合は409エラー
6. 権限情報の更新
   - 操作タイプに応じた処理実行
     - add: 既存の権限に追加
     - remove: 既存の権限から削除
     - replace: 既存の権限を置換
   - 変更履歴の記録
7. レスポンスの生成
   - 更新後の権限情報を取得・整形
   - 変更サマリーの生成
8. レスポンス返却

### 4.2 権限設定ルール

- 権限設定には管理者権限（PERM_MANAGE_PERMISSIONS）が必要
- 自分自身の権限は変更不可（管理者でも不可）
- 上位権限者の権限は変更不可（管理者は管理者の権限を変更不可）
- ロール変更時は自動的に関連する基本権限が付与/剥奪される
- 権限グループ所属時は自動的にグループ内の全権限が付与される
- 権限の変更はすべて監査ログに記録される

### 4.3 操作タイプ別処理

#### add（追加）
- 既存の権限・グループを維持したまま、新たな権限・グループを追加
- 既に持っている権限・グループは無視（エラーにはならない）
- ロール変更時は既存の権限を維持したまま、新ロールの基本権限を追加

#### remove（削除）
- 指定された権限・グループのみを削除
- 存在しない権限・グループの指定は無視（エラーにはならない）
- ロール変更時は新ロールに必要な基本権限は削除されない

#### replace（置換）
- 既存の権限・グループをすべて削除し、指定された権限・グループに置換
- 指定されていない項目（role, permissions, permission_groups, access_restrictions）は現状維持

### 4.4 パフォーマンス要件

- レスポンスタイム：平均300ms以内
- トランザクション：権限変更は単一トランザクションで処理
- 同時リクエスト：最大20リクエスト/秒

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-001](API仕様書_API-001.md) | ユーザー認証API | ユーザー認証 |
| [API-002](API仕様書_API-002.md) | SSO認証API | SSO認証 |
| [API-003](API仕様書_API-003.md) | 権限情報取得API | ユーザー権限情報取得 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| users | ユーザー情報 | 参照（R） |
| user_roles | ユーザーロール | 参照/更新（R/U） |
| permissions | 権限マスタ | 参照（R） |
| user_permissions | ユーザー権限割当 | 参照/作成/更新/削除（R/C/U/D） |
| permission_groups | 権限グループ | 参照（R） |
| group_permissions | グループ権限割当 | 参照（R） |
| user_group_memberships | ユーザーグループ所属 | 参照/作成/削除（R/C/D） |
| access_restrictions | アクセス制限情報 | 参照/作成/更新/削除（R/C/U/D） |
| permission_change_logs | 権限変更履歴 | 作成（C） |

### 5.3 注意事項・補足

- 権限変更は監査目的で詳細に記録される
- 権限変更後はキャッシュが自動的に更新される
- 権限変更はユーザーのセッションに即時反映される
- 大量の権限変更は非同期バッチ処理で行うことを推奨
- 権限IDの命名規則：PERM_[動作]_[対象]
- 権限グループIDの命名規則：GROUP_[名称]

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState } from 'react';
import axios from 'axios';

interface PermissionUpdateRequest {
  user_id: string;
  role?: string;
  permissions?: string[];
  permission_groups?: string[];
  access_restrictions?: {
    ip_restrictions?: string[];
    time_restrictions?: {
      day_of_week: number[];
      start_time: string;
      end_time: string;
    }[];
    department_restrictions?: string[];
  };
  operation_type: 'add' | 'remove' | 'replace';
  reason: string;
}

interface PermissionUpdateResponse {
  user_id: string;
  username: string;
  role: string;
  permissions: {
    permission_id: string;
    name: string;
    description: string;
  }[];
  permission_groups: {
    group_id: string;
    name: string;
    description: string;
  }[];
  access_restrictions: {
    ip_restrictions: string[];
    time_restrictions: {
      day_of_week: number[];
      start_time: string;
      end_time: string;
    }[];
    department_restrictions: string[];
  };
  updated_by: string;
  updated_at: string;
  change_summary: {
    added: string[];
    removed: string[];
    role_changed: boolean;
    groups_changed: boolean;
    restrictions_changed: boolean;
  };
}

const UserPermissionUpdateForm: React.FC<{ userId: string; onSuccess: (data: PermissionUpdateResponse) => void }> = ({ userId, onSuccess }) => {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedPermissions, setSelectedPermissions] = useState<string[]>([]);
  const [operationType, setOperationType] = useState<'add' | 'remove' | 'replace'>('add');
  const [reason, setReason] = useState<string>('');
  
  // 権限マスタデータ（実際の実装では別途APIから取得）
  const availablePermissions = [
    { id: 'PERM_VIEW_REPORTS', name: 'レポート閲覧' },
    { id: 'PERM_EDIT_PROFILE', name: 'プロフィール編集' },
    { id: 'PERM_MANAGE_TEAM', name: 'チーム管理' },
    { id: 'PERM_EXPORT_DATA', name: 'データエクスポート' },
    { id: 'PERM_MANAGE_USERS', name: 'ユーザー管理' }
  ];

  const handlePermissionChange = (permissionId: string) => {
    if (selectedPermissions.includes(permissionId)) {
      setSelectedPermissions(selectedPermissions.filter(id => id !== permissionId));
    } else {
      setSelectedPermissions([...selectedPermissions, permissionId]);
    }
  };

  const handleOperationTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setOperationType(e.target.value as 'add' | 'remove' | 'replace');
  };

  const handleReasonChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setReason(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (selectedPermissions.length === 0) {
      setError('少なくとも1つの権限を選択してください');
      return;
    }
    
    if (!reason.trim()) {
      setError('変更理由を入力してください');
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      const requestData: PermissionUpdateRequest = {
        user_id: userId,
        permissions: selectedPermissions,
        operation_type: operationType,
        reason: reason
      };
      
      const response = await axios.put<PermissionUpdateResponse>(
        '/api/auth/permissions',
        requestData,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
        }
      );
      
      // 成功時の処理
      onSuccess(response.data);
      
      // フォームリセット
      setSelectedPermissions([]);
      setReason('');
      
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const errorData = err.response.data;
        setError(errorData.error?.message || '権限更新に失敗しました');
      } else {
        setError('権限更新中にエラーが発生しました');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="permission-update-form">
      <h3>ユーザー権限更新</h3>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>操作タイプ:</label>
          <select 
            value={operationType} 
            onChange={handleOperationTypeChange}
            disabled={loading}
          >
            <option value="add">追加</option>
            <option value="remove">削除</option>
            <option value="replace">置換</option>
          </select>
        </div>
        
        <div className="form-group">
          <label>権限:</label>
          <div className="permissions-list">
            {availablePermissions.map(permission => (
              <div key={permission.id} className="permission-item">
                <input
                  type="checkbox"
                  id={`perm-${permission.id}`}
                  checked={selectedPermissions.includes(permission.id)}
                  onChange={() => handlePermissionChange(permission.id)}
                  disabled={loading}
                />
                <label htmlFor={`perm-${permission.id}`}>{permission.name} ({permission.id})</label>
              </div>
            ))}
          </div>
        </div>
        
        <div className="form-group">
          <label>変更理由:</label>
          <textarea
            value={reason}
            onChange={handleReasonChange}
            disabled={loading}
            rows={3}
            placeholder="権限変更の理由を入力してください（監査目的で記録されます）"
            required
          />
        </div>
        
        <div className="form-actions">
          <button type="submit" disabled={loading}>
            {loading ? '処理中...' : '権限を更新'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default UserPermissionUpdateForm;
```

### 6.2 バックエンド実装例（Java/Spring Boot）

```java
package com.example.skillreport.controller;

import com.example.skillreport.dto.PermissionUpdateRequest;
import com.example.skillreport.dto.UserPermissionsDto;
import com.example.skillreport.exception.InvalidOperationException;
import com.example.skillreport.exception.PermissionDeniedException;
import com.example.skillreport.exception.ResourceNotFoundException;
import com.example.skillreport.service.PermissionService;
import com.example.skillreport.service.UserService;
import com.example.skillreport.util.SecurityUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;

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
     * ユーザーの権限情報を更新するAPI
     *
     * @param request 権限更新リクエスト
     * @return 更新後のユーザー権限情報
     */
    @PutMapping("/permissions")
    public ResponseEntity<UserPermissionsDto> updateUserPermissions(
            @Valid @RequestBody PermissionUpdateRequest request) {
        
        // 認証済みユーザーの取得
        String currentUserId = securityUtils.getCurrentUserId();
        
        // 権限設定権限のチェック
        if (!securityUtils.hasPermission("PERM_MANAGE_PERMISSIONS")) {
            throw new PermissionDeniedException("権限設定を行うには管理者権限が必要です。");
        }
        
        // 自分自身の権限変更は禁止
        if (request.getUserId().equals(currentUserId)) {
            throw new InvalidOperationException("自分自身の権限は変更できません。");
        }
        
        // ユーザーの存在確認
        if (!userService.existsById(request.getUserId())) {
            throw new ResourceNotFoundException("指定されたユーザーID: " + request.getUserId() + " が見つかりません。");
        }
        
        // 操作タイプの検証
        String operationType = request.getOperationType();
        if (!operationType.equals("add") && !operationType.equals("remove") && !operationType.equals("replace")) {
            throw new InvalidOperationException("操作タイプは 'add', 'remove', 'replace' のいずれかである必要があります。");
        }
        
        // 権限・グループの存在確認
        if (request.getPermissions() != null) {
            for (String permissionId : request.getPermissions()) {
                if (!permissionService.existsPermission(permissionId)) {
                    throw new ResourceNotFoundException("指定された権限ID: " + permissionId + " が見つかりません。");
                }
            }
        }
        
        if (request.getPermissionGroups() != null) {
            for (String groupId : request.getPermissionGroups()) {
                if (!permissionService.existsPermissionGroup(groupId)) {
                    throw new ResourceNotFoundException("指定された権限グループID: " + groupId + " が見つかりません。");
                }
            }
        }
        
        // 権限の整合性チェック
        if (request.getRole() != null && request.getPermissions() != null) {
            permissionService.validateRolePermissionCombination(request.getRole(), request.getPermissions());
        }
        
        // 権限情報の更新
        UserPermissionsDto updatedPermissions = permissionService.updateUserPermissions(
                request.getUserId(),
                request.getRole(),
                request.getPermissions(),
                request.getPermissionGroups(),
                request.getAccessRestrictions(),
                operationType,
                request.getReason(),
                currentUserId
        );
        
        return ResponseEntity.ok(updatedPermissions);
    }
}
```

### 6.3 権限更新サービス実装例（Java/Spring Boot）

```java
package com.example.skillreport.service.impl;

import com.example.skillreport.dto.AccessRestrictionsDto;
import com.example.skillreport.dto.PermissionChangeLogDto;
import com.example.skillreport.dto.UserPermissionsDto;
import com.example.skillreport.entity.*;
import com.example.skillreport.exception.InvalidOperationException;
import com.example.skillreport.repository.*;
import com.example.skillreport.service.PermissionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
