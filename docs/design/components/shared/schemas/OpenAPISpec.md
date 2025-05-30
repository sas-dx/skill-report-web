# OpenAPI仕様書

## 1. 基本情報

- **API名**: Skill Report Web API
- **バージョン**: 1.0.0
- **ベースURL**: `/api/v1`
- **認証方式**: JWT Bearer Token
- **作成日**: 2025/05/30
- **最終更新**: 2025/05/30

---

## 2. OpenAPI仕様

```yaml
openapi: 3.0.3
info:
  title: Skill Report Web API
  description: スキルレポートWebアプリケーションのREST API仕様
  version: 1.0.0
  contact:
    name: 開発チーム
    email: dev-team@company.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: http://localhost:3000/api/v1
    description: 開発環境
  - url: https://staging-api.skillreport.com/api/v1
    description: ステージング環境
  - url: https://api.skillreport.com/api/v1
    description: 本番環境

security:
  - bearerAuth: []

paths:
  # スキル関連API
  /skills:
    get:
      summary: スキル一覧取得
      description: 登録されているスキルの一覧を取得します
      tags:
        - Skills
      parameters:
        - name: page
          in: query
          description: ページ番号
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          description: 1ページあたりの件数
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: category
          in: query
          description: スキルカテゴリでフィルタ
          required: false
          schema:
            $ref: '#/components/schemas/SkillCategory'
        - name: level
          in: query
          description: スキルレベルでフィルタ
          required: false
          schema:
            $ref: '#/components/schemas/SkillLevel'
        - name: search
          in: query
          description: スキル名での検索
          required: false
          schema:
            type: string
            maxLength: 100
      responses:
        '200':
          description: スキル一覧取得成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Skill'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalServerError'

    post:
      summary: スキル新規作成
      description: 新しいスキルを作成します
      tags:
        - Skills
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateSkillRequest'
      responses:
        '201':
          description: スキル作成成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    $ref: '#/components/schemas/Skill'
                  message:
                    type: string
                    example: "スキルが正常に作成されました"
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '409':
          $ref: '#/components/responses/Conflict'
        '500':
          $ref: '#/components/responses/InternalServerError'

  /skills/{skillId}:
    get:
      summary: スキル詳細取得
      description: 指定されたIDのスキル詳細を取得します
      tags:
        - Skills
      parameters:
        - name: skillId
          in: path
          required: true
          description: スキルID
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: スキル詳細取得成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    $ref: '#/components/schemas/Skill'
        '404':
          $ref: '#/components/responses/NotFound'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalServerError'

    put:
      summary: スキル更新
      description: 指定されたIDのスキルを更新します
      tags:
        - Skills
      parameters:
        - name: skillId
          in: path
          required: true
          description: スキルID
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateSkillRequest'
      responses:
        '200':
          description: スキル更新成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    $ref: '#/components/schemas/Skill'
                  message:
                    type: string
                    example: "スキルが正常に更新されました"
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '500':
          $ref: '#/components/responses/InternalServerError'

    delete:
      summary: スキル削除
      description: 指定されたIDのスキルを削除します
      tags:
        - Skills
      parameters:
        - name: skillId
          in: path
          required: true
          description: スキルID
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: スキル削除成功
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '500':
          $ref: '#/components/responses/InternalServerError'

  # ユーザー関連API
  /users:
    get:
      summary: ユーザー一覧取得
      description: 登録されているユーザーの一覧を取得します
      tags:
        - Users
      parameters:
        - name: page
          in: query
          description: ページ番号
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          description: 1ページあたりの件数
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: department
          in: query
          description: 部署でフィルタ
          required: false
          schema:
            type: string
        - name: role
          in: query
          description: 役職でフィルタ
          required: false
          schema:
            $ref: '#/components/schemas/UserRole'
      responses:
        '200':
          description: ユーザー一覧取得成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalServerError'

  /users/{userId}:
    get:
      summary: ユーザー詳細取得
      description: 指定されたIDのユーザー詳細を取得します
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          description: ユーザーID
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: ユーザー詳細取得成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalServerError'

  /users/{userId}/skills:
    get:
      summary: ユーザースキル一覧取得
      description: 指定されたユーザーのスキル一覧を取得します
      tags:
        - Users
        - Skills
      parameters:
        - name: userId
          in: path
          required: true
          description: ユーザーID
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: ユーザースキル一覧取得成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/UserSkill'
        '404':
          $ref: '#/components/responses/NotFound'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalServerError'

    post:
      summary: ユーザースキル追加
      description: 指定されたユーザーにスキルを追加します
      tags:
        - Users
        - Skills
      parameters:
        - name: userId
          in: path
          required: true
          description: ユーザーID
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserSkillRequest'
      responses:
        '201':
          description: ユーザースキル追加成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    $ref: '#/components/schemas/UserSkill'
                  message:
                    type: string
                    example: "スキルが正常に追加されました"
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '409':
          $ref: '#/components/responses/Conflict'
        '500':
          $ref: '#/components/responses/InternalServerError'

  # 認証関連API
  /auth/login:
    post:
      summary: ログイン
      description: ユーザー認証を行い、JWTトークンを取得します
      tags:
        - Authentication
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginRequest'
      responses:
        '200':
          description: ログイン成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: object
                    properties:
                      token:
                        type: string
                        description: JWTアクセストークン
                      refreshToken:
                        type: string
                        description: リフレッシュトークン
                      user:
                        $ref: '#/components/schemas/User'
                  message:
                    type: string
                    example: "ログインに成功しました"
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalServerError'

  /auth/logout:
    post:
      summary: ログアウト
      description: ユーザーをログアウトし、トークンを無効化します
      tags:
        - Authentication
      responses:
        '200':
          description: ログアウト成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "ログアウトしました"
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalServerError'

  /auth/refresh:
    post:
      summary: トークンリフレッシュ
      description: リフレッシュトークンを使用して新しいアクセストークンを取得します
      tags:
        - Authentication
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                refreshToken:
                  type: string
                  description: リフレッシュトークン
              required:
                - refreshToken
      responses:
        '200':
          description: トークンリフレッシュ成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: object
                    properties:
                      token:
                        type: string
                        description: 新しいJWTアクセストークン
                  message:
                    type: string
                    example: "トークンが更新されました"
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalServerError'

  # バッチ関連API
  /batch/jobs:
    get:
      summary: バッチジョブ一覧取得
      description: バッチジョブの一覧を取得します
      tags:
        - Batch
      parameters:
        - name: status
          in: query
          description: ジョブステータスでフィルタ
          required: false
          schema:
            $ref: '#/components/schemas/JobStatus'
        - name: category
          in: query
          description: ジョブカテゴリでフィルタ
          required: false
          schema:
            $ref: '#/components/schemas/JobCategory'
      responses:
        '200':
          description: バッチジョブ一覧取得成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/BatchJob'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalServerError'

    post:
      summary: バッチジョブ実行
      description: 指定されたバッチジョブを実行します
      tags:
        - Batch
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ExecuteBatchJobRequest'
      responses:
        '202':
          description: バッチジョブ実行開始
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: object
                    properties:
                      executionId:
                        type: string
                        description: 実行ID
                  message:
                    type: string
                    example: "バッチジョブの実行を開始しました"
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalServerError'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    # スキル関連スキーマ
    Skill:
      type: object
      properties:
        id:
          type: string
          format: uuid
          description: スキルID
        name:
          type: string
          description: スキル名
          example: "JavaScript"
        description:
          type: string
          description: スキルの説明
          example: "Webフロントエンド開発言語"
        category:
          $ref: '#/components/schemas/SkillCategory'
        tags:
          type: array
          items:
            type: string
          description: スキルタグ
          example: ["プログラミング", "フロントエンド"]
        createdAt:
          type: string
          format: date-time
          description: 作成日時
        updatedAt:
          type: string
          format: date-time
          description: 更新日時
      required:
        - id
        - name
        - category
        - createdAt
        - updatedAt

    SkillCategory:
      type: string
      enum:
        - programming
        - framework
        - database
        - infrastructure
        - design
        - management
        - communication
        - other
      description: スキルカテゴリ

    SkillLevel:
      type: string
      enum:
        - beginner
        - intermediate
        - advanced
        - expert
      description: スキルレベル

    CreateSkillRequest:
      type: object
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
          description: スキル名
        description:
          type: string
          maxLength: 500
          description: スキルの説明
        category:
          $ref: '#/components/schemas/SkillCategory'
        tags:
          type: array
          items:
            type: string
            maxLength: 50
          maxItems: 10
          description: スキルタグ
      required:
        - name
        - category

    UpdateSkillRequest:
      type: object
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
          description: スキル名
        description:
          type: string
          maxLength: 500
          description: スキルの説明
        category:
          $ref: '#/components/schemas/SkillCategory'
        tags:
          type: array
          items:
            type: string
            maxLength: 50
          maxItems: 10
          description: スキルタグ

    # ユーザー関連スキーマ
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
          description: ユーザーID
        email:
          type: string
          format: email
          description: メールアドレス
        name:
          type: string
          description: ユーザー名
        department:
          type: string
          description: 部署
        role:
          $ref: '#/components/schemas/UserRole'
        createdAt:
          type: string
          format: date-time
          description: 作成日時
        updatedAt:
          type: string
          format: date-time
          description: 更新日時
      required:
        - id
        - email
        - name
        - role
        - createdAt
        - updatedAt

    UserRole:
      type: string
      enum:
        - admin
        - manager
        - member
        - viewer
      description: ユーザー役職

    UserSkill:
      type: object
      properties:
        id:
          type: string
          format: uuid
          description: ユーザースキルID
        userId:
          type: string
          format: uuid
          description: ユーザーID
        skillId:
          type: string
          format: uuid
          description: スキルID
        skill:
          $ref: '#/components/schemas/Skill'
        level:
          $ref: '#/components/schemas/SkillLevel'
        experience:
          type: integer
          minimum: 0
          description: 経験年数（月）
        lastUsed:
          type: string
          format: date
          description: 最終使用日
        notes:
          type: string
          description: 備考
        createdAt:
          type: string
          format: date-time
          description: 作成日時
        updatedAt:
          type: string
          format: date-time
          description: 更新日時
      required:
        - id
        - userId
        - skillId
        - skill
        - level
        - createdAt
        - updatedAt

    CreateUserSkillRequest:
      type: object
      properties:
        skillId:
          type: string
          format: uuid
          description: スキルID
        level:
          $ref: '#/components/schemas/SkillLevel'
        experience:
          type: integer
          minimum: 0
          description: 経験年数（月）
        lastUsed:
          type: string
          format: date
          description: 最終使用日
        notes:
          type: string
          maxLength: 500
          description: 備考
      required:
        - skillId
        - level

    # 認証関連スキーマ
    LoginRequest:
      type: object
      properties:
        email:
          type: string
          format: email
          description: メールアドレス
        password:
          type: string
          minLength: 8
          description: パスワード
      required:
        - email
        - password

    # バッチ関連スキーマ
    BatchJob:
      type: object
      properties:
        id:
          type: string
          description: ジョブID
        name:
          type: string
          description: ジョブ名
        category:
          $ref: '#/components/schemas/JobCategory'
        status:
          $ref: '#/components/schemas/JobStatus'
        lastExecuted:
          type: string
          format: date-time
          description: 最終実行日時
        nextExecution:
          type: string
          format: date-time
          description: 次回実行予定日時
        duration:
          type: integer
          description: 実行時間（ミリ秒）
      required:
        - id
        - name
        - category
        - status

    JobCategory:
      type: string
      enum:
        - data-sync
        - statistics
        - cleanup
        - report
        - notification
        - backup
        - maintenance
      description: ジョブカテゴリ

    JobStatus:
      type: string
      enum:
        - pending
        - running
        - completed
        - failed
        - cancelled
      description: ジョブステータス

    ExecuteBatchJobRequest:
      type: object
      properties:
        jobName:
          type: string
          description: 実行するジョブ名
        parameters:
          type: object
          description: ジョブパラメータ
        dryRun:
          type: boolean
          default: false
          description: ドライラン実行フラグ
      required:
        - jobName

    # 共通スキーマ
    Pagination:
      type: object
      properties:
        page:
          type: integer
          minimum: 1
          description: 現在のページ番号
        limit:
          type: integer
          minimum: 1
          description: 1ページあたりの件数
        total:
          type: integer
          minimum: 0
          description: 総件数
        totalPages:
          type: integer
          minimum: 0
          description: 総ページ数
        hasNext:
          type: boolean
          description: 次のページが存在するか
        hasPrev:
          type: boolean
          description: 前のページが存在するか
      required:
        - page
        - limit
        - total
        - totalPages
        - hasNext
        - hasPrev

    Error:
      type: object
      properties:
        code:
          type: string
          description: エラーコード
        message:
          type: string
          description: エラーメッセージ
        details:
          type: object
          description: エラー詳細
        timestamp:
          type: string
          format: date-time
          description: エラー発生日時
      required:
        - code
        - message
        - timestamp

  responses:
    BadRequest:
      description: リクエストが不正です
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "BAD_REQUEST"
            message: "リクエストパラメータが不正です"
            timestamp: "2025-05-30T09:00:00Z"

    Unauthorized:
      description: 認証が必要です
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "UNAUTHORIZED"
            message: "認証が必要です"
            timestamp: "2025-05-30T09:00:00Z"

    Forbidden:
      description: アクセス権限がありません
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "FORBIDDEN"
            message: "この操作を実行する権限がありません"
            timestamp: "2025-05-30T09:00:00Z"

    NotFound:
      description: リソースが見つかりません
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "NOT_FOUND"
            message: "指定されたリソースが見つかりません"
            timestamp: "2025-05-30T09:00:00Z"

    Conflict:
      description: リソースが競合しています
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "CONFLICT"
            message: "リソースが既に存在します"
            timestamp: "2025-05-30T09:00:00Z"

    InternalServerError:
      description: サーバー内部エラー
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "INTERNAL_SERVER_ERROR"
            message: "サーバー内部でエラーが発生しました"
            timestamp: "2025-05-30T09:00:00Z"

tags:
  - name: Skills
    description: スキル管理API
  - name: Users
    description: ユーザー管理API
  - name: Authentication
    description: 認証API
  - name: Batch
    description: バッチ処理API
```

---

## 3. 変更履歴

| 日付 | バージョン | 変更内容 | 担当者 |
|------|-----------|----------|--------|
| 2025/05/30 | 1.0.0 | 初版作成 | 開発チーム |

---

## 4. 関連ドキュメント

- [共通部品定義書](../../共通部品定義書.md)
- [SkillTypes 型定義書](../types/SkillTypes.md)
- [BatchTypes 型定義書](../types/BatchTypes.md)
- [SkillService 定義書](../../backend/services/SkillService.md)

---

このOpenAPI仕様書により、フロントエンドとバックエンド間のAPI契約が明確に定義され、開発効率と品質が向上します。
