# API仕様書：API-023 スキルマスタ取得API

## 1. 基本情報

- **API ID**: API-023
- **API名称**: スキルマスタ取得API
- **概要**: スキルマスタ情報を取得する
- **エンドポイント**: `/api/skill-masters`
- **HTTPメソッド**: GET
- **リクエスト形式**: クエリパラメータ
- **レスポンス形式**: JSON
- **認証要件**: 必須（JWT認証）
- **利用画面**: [SCR-SKILL-M](画面設計書_SCR-SKILL-M.md)、[SCR-SKILL](画面設計書_SCR-SKILL.md)
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
| category | string | - | スキルカテゴリ | 指定がない場合は全カテゴリ<br>例: "technical", "business", "language" |
| keyword | string | - | 検索キーワード | スキル名・説明の部分一致検索 |
| page | number | - | ページ番号 | デフォルト: 1 |
| size | number | - | 1ページあたりの件数 | デフォルト: 50、最大: 100 |
| sort | string | - | ソート条件 | "name", "category", "popularity"<br>デフォルト: "category,name" |
| order | string | - | ソート順 | "asc"（昇順）, "desc"（降順）<br>デフォルト: "asc" |

### 2.3 リクエスト例

```
GET /api/skill-masters?category=technical&keyword=java&page=1&size=20&sort=popularity&order=desc HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json
```

---

## 3. レスポンス仕様

### 3.1 正常時レスポンス（200 OK）

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| total | number | 総件数 | |
| page | number | 現在のページ番号 | |
| size | number | 1ページあたりの件数 | |
| total_pages | number | 総ページ数 | |
| skills | array | スキルマスタ情報の配列 | |
| categories | array | スキルカテゴリ情報の配列 | |
| last_updated | string | 最終更新日時 | ISO 8601形式 |

#### skills 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | スキルID | |
| category | string | スキルカテゴリ | "technical", "business", "language"など |
| name | string | スキル名 | |
| description | string | 説明 | |
| synonyms | array | 同義語 | |
| related_skills | array | 関連スキル | |
| popularity | number | 人気度 | 1-100（100が最高） |
| created_at | string | 作成日時 | ISO 8601形式 |
| updated_at | string | 更新日時 | ISO 8601形式 |

#### related_skills 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| skill_id | string | 関連スキルID | |
| name | string | 関連スキル名 | |
| relation_type | string | 関連タイプ | "parent", "child", "related" |

#### categories 配列要素

| パラメータ名 | 型 | 説明 | 備考 |
|------------|------|------|------|
| category_id | string | カテゴリID | |
| name | string | カテゴリ名 | |
| description | string | 説明 | |
| display_order | number | 表示順 | |

### 3.2 正常時レスポンス例

```json
{
  "total": 120,
  "page": 1,
  "size": 20,
  "total_pages": 6,
  "skills": [
    {
      "skill_id": "S001",
      "category": "technical",
      "name": "Java",
      "description": "オブジェクト指向プログラミング言語。エンタープライズアプリケーション開発に広く使用されている。",
      "synonyms": ["Java SE", "Java EE", "JDK"],
      "related_skills": [
        {
          "skill_id": "S002",
          "name": "Spring Framework",
          "relation_type": "related"
        },
        {
          "skill_id": "S003",
          "name": "JUnit",
          "relation_type": "related"
        }
      ],
      "popularity": 95,
      "created_at": "2020-04-01T00:00:00+09:00",
      "updated_at": "2025-01-15T10:30:00+09:00"
    },
    {
      "skill_id": "S002",
      "category": "technical",
      "name": "Spring Framework",
      "description": "Javaアプリケーション開発のためのオープンソースフレームワーク。",
      "synonyms": ["Spring", "Spring Boot", "Spring MVC"],
      "related_skills": [
        {
          "skill_id": "S001",
          "name": "Java",
          "relation_type": "related"
        },
        {
          "skill_id": "S004",
          "name": "Hibernate",
          "relation_type": "related"
        }
      ],
      "popularity": 90,
      "created_at": "2020-04-01T00:00:00+09:00",
      "updated_at": "2025-01-15T10:30:00+09:00"
    },
    {
      "skill_id": "S005",
      "category": "technical",
      "name": "JavaScript",
      "description": "Webブラウザで動作するスクリプト言語。フロントエンド開発に必須。",
      "synonyms": ["JS", "ECMAScript"],
      "related_skills": [
        {
          "skill_id": "S006",
          "name": "TypeScript",
          "relation_type": "child"
        },
        {
          "skill_id": "S007",
          "name": "React",
          "relation_type": "related"
        }
      ],
      "popularity": 98,
      "created_at": "2020-04-01T00:00:00+09:00",
      "updated_at": "2025-01-15T10:30:00+09:00"
    }
  ],
  "categories": [
    {
      "category_id": "C001",
      "name": "technical",
      "description": "技術スキル",
      "display_order": 1
    },
    {
      "category_id": "C002",
      "name": "business",
      "description": "業務知識",
      "display_order": 2
    },
    {
      "category_id": "C003",
      "name": "language",
      "description": "言語スキル",
      "display_order": 3
    },
    {
      "category_id": "C004",
      "name": "soft",
      "description": "ソフトスキル",
      "display_order": 4
    },
    {
      "category_id": "C005",
      "name": "management",
      "description": "マネジメントスキル",
      "display_order": 5
    }
  ],
  "last_updated": "2025-05-15T10:30:00+09:00"
}
```

### 3.3 エラー時レスポンス

| ステータスコード | エラーコード | エラーメッセージ | 説明 |
|----------------|------------|----------------|------|
| 400 Bad Request | INVALID_PARAMETER | パラメータが不正です | パラメータ形式不正 |
| 400 Bad Request | INVALID_CATEGORY | カテゴリが不正です | 存在しないカテゴリ指定 |
| 400 Bad Request | INVALID_SORT | ソート条件が不正です | 不正なソート条件 |
| 401 Unauthorized | UNAUTHORIZED | 認証が必要です | 認証トークンなし/無効 |
| 403 Forbidden | PERMISSION_DENIED | 権限がありません | スキルマスタ閲覧権限なし |
| 500 Internal Server Error | SYSTEM_ERROR | システムエラーが発生しました | サーバー内部エラー |

### 3.4 エラー時レスポンス例

```json
{
  "error": {
    "code": "INVALID_CATEGORY",
    "message": "カテゴリが不正です",
    "details": "指定されたカテゴリ 'tech' は存在しません。有効なカテゴリ: technical, business, language, soft, management"
  }
}
```

---

## 4. 処理仕様

### 4.1 処理フロー

1. リクエストの認証・認可チェック
   - JWTトークンの検証
   - スキルマスタ閲覧権限（PERM_VIEW_SKILL_MASTERS）の確認
2. リクエストパラメータの検証
   - categoryの値チェック（指定されている場合）
   - page、sizeの範囲チェック
   - sort、orderの値チェック
3. スキルマスタ情報の取得
   - 条件に合致するスキルマスタ情報を取得
   - ページネーション処理
   - ソート処理
4. スキルカテゴリ情報の取得
5. レスポンスの生成
   - 取得したスキルマスタ情報とカテゴリ情報を整形
6. レスポンス返却

### 4.2 スキルマスタ取得ルール

- スキルマスタの閲覧には権限（PERM_VIEW_SKILL_MASTERS）が必要
- 一般ユーザーは参照のみ可能
- 管理者（ROLE_ADMIN）はスキルマスタの更新も可能
- スキルカテゴリは「technical（技術）」「business（業務知識）」「language（言語）」「soft（ソフトスキル）」「management（マネジメント）」の5種類
- 人気度（popularity）は、そのスキルを登録しているユーザー数や検索頻度から算出
- 関連スキルは、親子関係（parent/child）または関連関係（related）で表現
- 同義語（synonyms）は、検索時のマッチング向上のために使用

### 4.3 パフォーマンス要件

- レスポンスタイム：平均300ms以内
- キャッシュ：スキルマスタ情報は1日キャッシュ
- 同時リクエスト：最大30リクエスト/秒

---

## 5. 関連情報

### 5.1 関連API

| API ID | API名称 | 関連内容 |
|--------|--------|----------|
| [API-021](API仕様書_API-021.md) | スキル情報取得API | ユーザースキル情報取得 |
| [API-022](API仕様書_API-022.md) | スキル情報更新API | ユーザースキル情報更新 |
| [API-024](API仕様書_API-024.md) | スキルマスタ更新API | スキルマスタ情報更新 |
| [API-025](API仕様書_API-025.md) | スキル検索API | 条件指定によるスキル検索 |

### 5.2 使用テーブル

| テーブル名 | 用途 | 主な操作 |
|-----------|------|----------|
| skill_masters | スキルマスタ | 参照（R） |
| skill_categories | スキルカテゴリ | 参照（R） |
| skill_synonyms | スキル同義語 | 参照（R） |
| skill_relations | スキル関連情報 | 参照（R） |
| skill_popularity | スキル人気度 | 参照（R） |

### 5.3 注意事項・補足

- スキルマスタは定期的に更新され、新しい技術やスキルが追加される
- スキルマスタの更新権限は管理者のみ持つ
- スキル名は一意であるが、カテゴリが異なれば同名のスキルが存在可能
- 人気度は週次で再計算される
- 関連スキルは最大10件まで表示
- 同義語は最大5件まで登録可能
- キーワード検索はスキル名、説明、同義語に対して行われる
- スキルマスタのデータ量が多いため、常にページネーションを使用する

---

## 6. サンプルコード

### 6.1 フロントエンド実装例（React/TypeScript）

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSearchParams } from 'react-router-dom';

interface RelatedSkill {
  skill_id: string;
  name: string;
  relation_type: string;
}

interface Skill {
  skill_id: string;
  category: string;
  name: string;
  description: string;
  synonyms: string[];
  related_skills: RelatedSkill[];
  popularity: number;
  created_at: string;
  updated_at: string;
}

interface Category {
  category_id: string;
  name: string;
  description: string;
  display_order: number;
}

interface SkillMastersResponse {
  total: number;
  page: number;
  size: number;
  total_pages: number;
  skills: Skill[];
  categories: Category[];
  last_updated: string;
}

const SkillMastersView: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<SkillMastersResponse | null>(null);
  
  // 現在のクエリパラメータを取得
  const category = searchParams.get('category') || '';
  const keyword = searchParams.get('keyword') || '';
  const page = parseInt(searchParams.get('page') || '1', 10);
  const size = parseInt(searchParams.get('size') || '20', 10);
  const sort = searchParams.get('sort') || 'category,name';
  const order = searchParams.get('order') || 'asc';
  
  useEffect(() => {
    const fetchSkillMasters = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // APIリクエストURLの構築
        let url = '/api/skill-masters?';
        const params = new URLSearchParams();
        
        if (category) {
          params.append('category', category);
        }
        
        if (keyword) {
          params.append('keyword', keyword);
        }
        
        params.append('page', page.toString());
        params.append('size', size.toString());
        params.append('sort', sort);
        params.append('order', order);
        
        url += params.toString();
        
        // APIリクエスト
        const response = await axios.get<SkillMastersResponse>(url, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Accept': 'application/json'
          }
        });
        
        // データの設定
        setData(response.data);
        
      } catch (err) {
        if (axios.isAxiosError(err) && err.response) {
          const errorData = err.response.data;
          setError(errorData.error?.message || 'スキルマスタの取得に失敗しました');
        } else {
          setError('スキルマスタの取得中にエラーが発生しました');
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchSkillMasters();
  }, [category, keyword, page, size, sort, order]);
  
  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newParams = new URLSearchParams(searchParams);
    newParams.set('category', e.target.value);
    newParams.set('page', '1'); // カテゴリ変更時はページを1に戻す
    setSearchParams(newParams);
  };
  
  const handleKeywordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newParams = new URLSearchParams(searchParams);
    newParams.set('keyword', e.target.value);
    setSearchParams(newParams);
  };
  
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // 検索ボタンクリック時の処理
    // すでにuseEffectでパラメータ変更時に検索が実行されるため、
    // ここでは特に何もしない
  };
  
  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newParams = new URLSearchParams(searchParams);
    newParams.set('sort', e.target.value);
    setSearchParams(newParams);
  };
  
  const handleOrderChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newParams = new URLSearchParams(searchParams);
    newParams.set('order', e.target.value);
    setSearchParams(newParams);
  };
  
  const handlePageChange = (newPage: number) => {
    if (newPage < 1 || (data && newPage > data.total_pages)) {
      return;
    }
    
    const newParams = new URLSearchParams(searchParams);
    newParams.set('page', newPage.toString());
    setSearchParams(newParams);
  };
  
  const renderPagination = () => {
    if (!data) return null;
    
    const { page, total_pages } = data;
    
    return (
      <div className="pagination">
        <button 
          onClick={() => handlePageChange(1)} 
          disabled={page === 1}
        >
          最初へ
        </button>
        <button 
          onClick={() => handlePageChange(page - 1)} 
          disabled={page === 1}
        >
          前へ
        </button>
        <span className="page-info">
          {page} / {total_pages} ページ
        </span>
        <button 
          onClick={() => handlePageChange(page + 1)} 
          disabled={page === total_pages}
        >
          次へ
        </button>
        <button 
          onClick={() => handlePageChange(total_pages)} 
          disabled={page === total_pages}
        >
          最後へ
        </button>
      </div>
    );
  };
  
  const renderPopularityBar = (popularity: number) => {
    return (
      <div className="popularity-bar">
        <div 
          className="popularity-fill" 
          style={{ width: `${popularity}%` }}
        />
        <span className="popularity-text">{popularity}</span>
      </div>
    );
  };
  
  const getCategoryLabel = (categoryName: string): string => {
    if (!data) return categoryName;
    
    const category = data.categories.find(c => c.name === categoryName);
    return category ? category.description : categoryName;
  };
  
  const getRelationTypeLabel = (relationType: string): string => {
    const types: Record<string, string> = {
      'parent': '親スキル',
      'child': '子スキル',
      'related': '関連スキル'
    };
    return types[relationType] || relationType;
  };
  
  if (loading) {
    return <div className="loading">スキルマスタを読み込み中...</div>;
  }
  
  if (error) {
    return <div className="error">{error}</div>;
  }
  
  if (!data) {
    return <div className="no-data">スキルマスタ情報がありません</div>;
  }
  
  return (
    <div className="skill-masters-view">
      <div className="skill-masters-header">
        <h2>スキルマスタ</h2>
        <div className="last-updated">
          最終更新: {new Date(data.last_updated).toLocaleString()}
        </div>
      </div>
      
      <div className="search-filters">
        <form onSubmit={handleSearch}>
          <div className="filter-row">
            <div className="filter-group">
              <label htmlFor="category">カテゴリ:</label>
              <select 
                id="category"
                value={category}
                onChange={handleCategoryChange}
              >
                <option value="">全カテゴリ</option>
                {data.categories.map(cat => (
                  <option key={cat.category_id} value={cat.name}>
                    {cat.description}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="filter-group">
              <label htmlFor="keyword">キーワード:</label>
              <input 
                id="keyword"
                type="text"
                value={keyword}
                onChange={handleKeywordChange}
                placeholder="スキル名や説明で検索"
              />
              <button type="submit">検索</button>
            </div>
          </div>
          
          <div className="filter-row">
            <div className="filter-group">
              <label htmlFor="sort">並び順:</label>
              <select 
                id="sort"
                value={sort}
                onChange={handleSortChange}
              >
                <option value="category,name">カテゴリ・名前順</option>
                <option value="name">名前順</option>
                <option value="popularity">人気度順</option>
              </select>
            </div>
            
            <div className="filter-group">
              <label htmlFor="order">順序:</label>
              <select 
                id="order"
                value={order}
                onChange={handleOrderChange}
              >
                <option value="asc">昇順</option>
                <option value="desc">降順</option>
              </select>
            </div>
          </div>
        </form>
      </div>
      
      <div className="results-summary">
        検索結果: {data.total}件中 {(page - 1) * size + 1}-{Math.min(page * size, data.total)}件を表示
      </div>
      
      {renderPagination()}
      
      <div className="skills-list">
        {data.skills.map(skill => (
          <div key={skill.skill_id} className="skill-card">
            <div className="skill-header">
              <h3 className="skill-name">{skill.name}</h3>
              <span className="skill-category">{getCategoryLabel(skill.category)}</span>
            </div>
            
            <div className="skill-popularity">
              <span>人気度:</span>
              {renderPopularityBar(skill.popularity)}
            </div>
            
            <div className="skill-description">
              <p>{skill.description}</p>
            </div>
            
            {skill.synonyms.length > 0 && (
              <div className="skill-synonyms">
                <h4>同義語:</h4>
                <div className="synonyms-list">
                  {skill.synonyms.map((synonym, index) => (
                    <span key={index} className="synonym-tag">{synonym}</span>
                  ))}
                </div>
              </div>
            )}
            
            {skill.related_skills.length > 0 && (
              <div className="related-skills">
                <h4>関連スキル:</h4>
                <ul>
                  {skill.related_skills.map(related => (
                    <li key={related.skill_id}>
                      <span className="relation-type">{getRelationTypeLabel(related.relation_type)}:</span>
                      <span className="related-skill-name">{related.name}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            <div className="skill-meta">
              <span className="skill-id">ID: {skill.skill_id}</span>
              <span className="skill-updated">更新: {new Date(skill.updated_at).toLocaleDateString()}</span>
            </div>
          </div>
        ))}
      </div>
      
      {renderPagination()}
    </div>
  );
};

export default SkillMastersView;
```

### 6.2 バックエンド実装例（Java/Spring Boot）

```java
package com.example.skillreport.controller;

import com.example.skillreport.dto.SkillMastersResponseDto;
import com.example.skillreport.service.SkillMasterService;
import com.example.skillreport.util.SecurityUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/skill-masters")
public class SkillMasterController {

    private final SkillMasterService skillMasterService;
    private final SecurityUtils securityUtils;

    @Autowired
    public SkillMasterController(
            SkillMasterService skillMasterService,
            SecurityUtils securityUtils) {
        this.skillMasterService = skillMasterService;
        this.securityUtils = securityUtils;
    }

    /**
     * スキルマスタ情報を取得するAPI
     *
     * @param category スキルカテゴリ
     * @param keyword 検索キーワード
     * @param page ページ番号
     * @param size 1ページあたりの件数
     * @param sort ソート条件
     * @param order ソート順
     * @return スキルマスタ情報
     */
    @GetMapping
    public ResponseEntity<SkillMastersResponseDto> getSkillMasters(
            @RequestParam(required = false) String category,
            @RequestParam(required = false) String keyword,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "50") int size,
            @RequestParam(defaultValue = "category,name") String sort,
            @RequestParam(defaultValue = "asc") String order) {
        
        // 権限チェック
        securityUtils.checkPermission("PERM_VIEW_SKILL_MASTERS");
        
        // パラメータの検証
        if (size > 100) {
            size = 100; // 最大サイズを制限
        }
        
        // スキルマスタ情報を取得
        SkillMastersResponseDto response = skillMasterService.getSkillMasters(
                category, keyword, page, size, sort, order);
        
        return ResponseEntity.ok(response);
    }
}
