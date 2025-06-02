# 画面定義書: SCR_AUT_Login - Mermaid図

## 画面レイアウト

```mermaid
flowchart TD
    A[ログイン画面] --> B[ヘッダー部]
    A --> C[認証フォーム部]
    A --> D[アクション部]
    A --> E[メッセージ部]
    A --> F[フッター部]
    
    B --> B1[会社ロゴ]
    B --> B2[年間スキル報告書システム ログイン]
    
    C --> C1[ユーザーID入力欄]
    C --> C2[パスワード入力欄]
    C --> C3[パスワード表示チェックボックス]
    
    D --> D1[ログインボタン]
    D --> D2[SSOでログインボタン]
    D --> D3[パスワードを忘れた方はこちら]
    
    E --> E1[エラーメッセージ表示エリア]
    
    F --> F1[コピーライト表示]
    
    %% スタイリング
    classDef header fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef form fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef action fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef message fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef footer fill:#fafafa,stroke:#424242,stroke-width:2px
    
    class B,B1,B2 header
    class C,C1,C2,C3 form
    class D,D1,D2,D3 action
    class E,E1 message
    class F,F1 footer
```

## 操作フロー

```mermaid
flowchart TD
    START([ログイン画面表示]) --> INPUT[ユーザーID・パスワード入力]
    INPUT --> VALIDATE{入力値バリデーション}
    
    VALIDATE -->|必須項目未入力| ERROR1[エラーメッセージ表示<br/>必須項目が入力されていません]
    VALIDATE -->|形式不正| ERROR2[エラーメッセージ表示<br/>正しい形式で入力してください]
    VALIDATE -->|OK| LOGIN_BTN[ログインボタン押下]
    
    LOGIN_BTN --> API_CALL[API-001: ユーザー認証API呼び出し]
    API_CALL --> AUTH_CHECK{認証結果判定}
    
    AUTH_CHECK -->|認証成功| SESSION[セッション発行]
    AUTH_CHECK -->|認証失敗| FAIL_COUNT{失敗回数チェック}
    AUTH_CHECK -->|システムエラー| ERROR3[システム障害エラー表示]
    
    FAIL_COUNT -->|5回未満| ERROR4[エラーメッセージ表示<br/>ユーザーIDまたはパスワードが違います]
    FAIL_COUNT -->|5回以上| LOCK[アカウントロック<br/>管理者に連絡してください]
    
    SESSION --> TENANT[SCR_TEN_Select<br/>テナント選択画面へ遷移]
    
    %% SSO分岐
    INPUT --> SSO_BTN[SSOでログインボタン押下]
    SSO_BTN --> SSO_API[API-002: SSO認証API呼び出し]
    SSO_API --> IDP[IdPリダイレクト]
    IDP --> SSO_RESULT{SSO認証結果}
    SSO_RESULT -->|成功| SESSION
    SSO_RESULT -->|失敗| ERROR5[SSO認証エラー表示]
    
    %% パスワードリセット分岐
    INPUT --> RESET_LINK[パスワードを忘れた方はこちら]
    RESET_LINK --> RESET_PAGE[SCR_AUT_PasswordReset<br/>パスワードリセット画面へ遷移]
    
    %% エラーからの復帰
    ERROR1 --> INPUT
    ERROR2 --> INPUT
    ERROR4 --> INPUT
    ERROR5 --> INPUT
    
    %% スタイリング
    classDef startEnd fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    classDef process fill:#bbdefb,stroke:#1976d2,stroke-width:2px
    classDef decision fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef error fill:#ffcdd2,stroke:#d32f2f,stroke-width:2px
    classDef success fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    
    class START,TENANT,RESET_PAGE startEnd
    class INPUT,LOGIN_BTN,API_CALL,SESSION,SSO_BTN,SSO_API,IDP,RESET_LINK process
    class VALIDATE,AUTH_CHECK,FAIL_COUNT,SSO_RESULT decision
    class ERROR1,ERROR2,ERROR3,ERROR4,ERROR5,LOCK error
```

## ナビゲーションフロー

```mermaid
flowchart LR
    LOGIN[SCR_AUT_Login<br/>ログイン画面] --> |認証成功| TENANT[SCR_TEN_Select<br/>テナント選択画面]
    LOGIN --> |パスワードリセット| RESET[SCR_AUT_PasswordReset<br/>パスワードリセット画面]
    
    TENANT --> |テナント選択後| HOME[SCR_CMN_Home<br/>ホームダッシュボード画面]
    
    RESET --> |リセット完了| LOGIN
    
    %% 条件表示
    LOGIN -.-> |SSO設定時のみ| SSO_IDP[外部IdP<br/>認証プロバイダー]
    SSO_IDP -.-> |SSO認証成功| TENANT
    
    %% エラー時の遷移
    LOGIN --> |アカウントロック| ADMIN[管理者による<br/>アカウント解除]
    ADMIN -.-> |解除後| LOGIN
    
    %% スタイリング
    classDef primary fill:#e3f2fd,stroke:#1976d2,stroke-width:3px
    classDef secondary fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef external fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef admin fill:#ffebee,stroke:#c62828,stroke-width:2px
    
    class LOGIN,TENANT,HOME primary
    class RESET secondary
    class SSO_IDP external
    class ADMIN admin
```

## 画面項目とイベントの関係図

```mermaid
flowchart TD
    subgraph UI_ELEMENTS[UI要素]
        USER_ID[ユーザーID入力欄]
        PASSWORD[パスワード入力欄]
        SHOW_PASS[パスワード表示チェック]
        LOGIN_BTN[ログインボタン]
        SSO_BTN[SSOログインボタン]
        RESET_LINK[パスワードリセットリンク]
        ERROR_MSG[エラーメッセージ]
    end
    
    subgraph EVENTS[イベント]
        E01[E01: ログインボタン押下]
        E02[E02: SSOログインボタン押下]
        E03[E03: パスワード表示チェック]
        E04[E04: パスワードリセットリンク]
        E05[E05: Enterキー押下]
        E06[E06: 入力エラー]
        E07[E07: ログイン成功]
        E08[E08: ログイン失敗]
        E09[E09: アカウントロック]
    end
    
    subgraph APIS[API呼び出し]
        API001[API-001: ユーザー認証API]
        API002[API-002: SSO認証API]
        API004[API-004: パスワードリセットAPI]
    end
    
    %% UI要素とイベントの関係
    USER_ID --> E06
    PASSWORD --> E06
    LOGIN_BTN --> E01
    LOGIN_BTN --> E05
    SSO_BTN --> E02
    SHOW_PASS --> E03
    RESET_LINK --> E04
    
    %% イベントとAPIの関係
    E01 --> API001
    E02 --> API002
    E04 --> API004
    E05 --> API001
    
    %% APIと結果イベントの関係
    API001 --> E07
    API001 --> E08
    API001 --> E09
    API002 --> E07
    API002 --> E08
    
    %% 結果とUI表示の関係
    E06 --> ERROR_MSG
    E08 --> ERROR_MSG
    E09 --> ERROR_MSG
    
    %% スタイリング
    classDef uiElement fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px
    classDef event fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    classDef api fill:#e0f2f1,stroke:#00695c,stroke-width:2px
    
    class USER_ID,PASSWORD,SHOW_PASS,LOGIN_BTN,SSO_BTN,RESET_LINK,ERROR_MSG uiElement
    class E01,E02,E03,E04,E05,E06,E07,E08,E09 event
    class API001,API002,API004 api
```

## バリデーションフロー

```mermaid
flowchart TD
    INPUT_START[入力開始] --> USER_ID_CHECK{ユーザーID検証}
    
    USER_ID_CHECK -->|未入力| USER_ID_ERROR[必須エラー:<br/>ユーザーIDは必須です]
    USER_ID_CHECK -->|50文字超過| USER_ID_LENGTH_ERROR[文字数エラー:<br/>50文字以内で入力してください]
    USER_ID_CHECK -->|形式不正| USER_ID_FORMAT_ERROR[形式エラー:<br/>英数字・記号で入力してください]
    USER_ID_CHECK -->|OK| PASSWORD_CHECK{パスワード検証}
    
    PASSWORD_CHECK -->|未入力| PASSWORD_ERROR[必須エラー:<br/>パスワードは必須です]
    PASSWORD_CHECK -->|8文字未満| PASSWORD_LENGTH_ERROR[文字数エラー:<br/>8文字以上で入力してください]
    PASSWORD_CHECK -->|組み合わせ不正| PASSWORD_FORMAT_ERROR[形式エラー:<br/>英数字・記号の組み合わせで入力してください]
    PASSWORD_CHECK -->|OK| BUSINESS_RULE_CHECK{ビジネスルール検証}
    
    BUSINESS_RULE_CHECK -->|アカウントロック| ACCOUNT_LOCK_ERROR[アカウントロックエラー:<br/>管理者に連絡してください]
    BUSINESS_RULE_CHECK -->|パスワード期限切れ| PASSWORD_EXPIRED_ERROR[パスワード期限エラー:<br/>パスワードを更新してください]
    BUSINESS_RULE_CHECK -->|OK| VALIDATION_SUCCESS[バリデーション成功]
    
    %% エラーからの復帰
    USER_ID_ERROR --> INPUT_START
    USER_ID_LENGTH_ERROR --> INPUT_START
    USER_ID_FORMAT_ERROR --> INPUT_START
    PASSWORD_ERROR --> INPUT_START
    PASSWORD_LENGTH_ERROR --> INPUT_START
    PASSWORD_FORMAT_ERROR --> INPUT_START
    
    %% 成功時の処理
    VALIDATION_SUCCESS --> API_CALL[API認証呼び出し]
    
    %% スタイリング
    classDef start fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    classDef decision fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef error fill:#ffcdd2,stroke:#d32f2f,stroke-width:2px
    classDef success fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    
    class INPUT_START start
    class USER_ID_CHECK,PASSWORD_CHECK,BUSINESS_RULE_CHECK decision
    class USER_ID_ERROR,USER_ID_LENGTH_ERROR,USER_ID_FORMAT_ERROR,PASSWORD_ERROR,PASSWORD_LENGTH_ERROR,PASSWORD_FORMAT_ERROR,ACCOUNT_LOCK_ERROR,PASSWORD_EXPIRED_ERROR error
    class VALIDATION_SUCCESS,API_CALL success
```

---

## 図の説明

### 1. 画面レイアウト図
- ログイン画面の構成要素を階層構造で表現
- 各セクション（ヘッダー、フォーム、アクション、メッセージ、フッター）とその内容を視覚化
- 色分けにより各セクションの役割を明確化

### 2. 操作フロー図
- ユーザーの操作から画面遷移までの完全なフローを表現
- 通常ログイン、SSO、パスワードリセットの3つの主要パスを含む
- エラーハンドリングと復帰フローも詳細に記載

### 3. ナビゲーションフロー図
- 画面間の遷移関係を表現
- 条件付き遷移（SSO設定時、アカウントロック時）も含む
- システム全体での画面の位置づけを明確化

### 4. 画面項目とイベントの関係図
- UI要素、イベント、API呼び出しの関係を表現
- 画面定義書のイベント・アクション定義との対応を視覚化

### 5. バリデーションフロー図
- 入力値検証の詳細なフローを表現
- フィールドレベル、ビジネスルールレベルの検証を段階的に表示
- エラーメッセージとの対応も明確化

これらのMermaid図により、画面定義書の内容をより視覚的に理解しやすくなります。
