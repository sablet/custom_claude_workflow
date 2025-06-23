# Claude Code 個人設定・メモリファイル

## カスタムスラッシュコマンド設定

### 基本構造
カスタムコマンドは Markdown ファイル（.md）で作成し、YAMLフロントマターでメタデータを設定。

### 個人用コマンド (`~/.claude/commands/`)
`/user:` プレフィックスで呼び出し

#### セキュリティレビューコマンド例
ファイル: `~/.claude/commands/security-review.md`
```markdown
---
allowed-tools: ["Read", "Grep", "Bash"]
description: "コードのセキュリティ脆弱性をレビュー"
---

# セキュリティ脆弱性レビュー

## コンテキスト取得
!git log -n 5
!git status

## レビュー対象
@src/security/$ARGUMENTS

以下の観点でセキュリティレビューを実行:
- SQL インジェクション脆弱性
- XSS 脆弱性チェック
- 認証・認可の実装確認
- 機密情報の適切な取り扱い
- 入力値検証の実装状況
```

使用例: `/user:security-review authentication.js`

### プロジェクト用コマンド (`.claude/commands/`)
`/project:` プレフィックスで呼び出し

#### パフォーマンス最適化コマンド例
ファイル: `.claude/commands/optimize.md`
```markdown
---
allowed-tools: ["Bash", "Read", "Edit"]
description: "コードのパフォーマンス分析と最適化提案"
---

# パフォーマンス分析・最適化

## 現在の変更状況
!git diff HEAD

## 分析対象
@src/performance/$ARGUMENTS

以下の観点で分析:
- アルゴリズム計算量
- メモリ使用量
- ボトルネック特定
- 最適化提案
```

### 名前空間を使用した階層化コマンド

#### フロントエンド専用コマンド
ファイル: `.claude/commands/frontend/component-audit.md`
```markdown
---
description: "React コンポーネントのベストプラクティス監査"
---

# React コンポーネント監査

## 対象コンポーネント
@src/components/$ARGUMENTS

監査項目:
- パフォーマンス最適化（memo, useMemo, useCallback）
- アクセシビリティ準拠
- 状態管理パターン
- Props の型定義
- テストカバレッジ
```

使用例: `/project:frontend:component-audit LoginForm.tsx`

#### バックエンド専用コマンド
ファイル: `.claude/commands/backend/api-review.md`
```markdown
---
allowed-tools: ["Read", "Grep", "Bash"]
description: "API エンドポイントのレビュー"
---

# API エンドポイントレビュー

## API 仕様確認
@src/api/$ARGUMENTS

レビュー項目:
- エラーハンドリング
- レート制限実装
- 認証・認可チェック
- バリデーション実装
- ログ出力適切性
```

## カスタムコマンドの機能

### 利用可能な構文
- `!command`: Bashコマンド実行
- `@path/to/file`: ファイル参照
- `$ARGUMENTS`: 動的引数置換
- 名前空間: `/user:category:subcategory:command`

### YAMLフロントマター設定項目
- `allowed-tools`: 使用可能ツールの制限
- `description`: コマンドの説明

### コマンド作成のベストプラクティス
1. 具体的で実行可能な指示を記載
2. 必要なコンテキスト情報を事前取得
3. 段階的なレビュー・分析手順を明記
4. セキュリティ重視の観点を含める
5. 動的引数を活用して汎用性を高める

## Pythonプロジェクトのデフォルト設定

### パッケージ管理（uv使用）
```bash
# 依存関係のインストール
uv add package_name

# 開発依存関係の追加
uv add --dev package_name

# ツール実行
uv run tool_name

# パッケージのアップグレード
uv add package_name --upgrade-package package_name
```

### コード品質管理
```bash
# フォーマット（Ruff使用）
uv run --frozen ruff format .

# リント・チェック
uv run --frozen ruff check .

# 型チェック（Pyright）
uv run --frozen pyright

# テスト実行（pytest）
uv run --frozen pytest
```

### プロジェクト構造（レイヤード設計）
```
project/
├── src/                    # アプリケーション層
│   ├── api/               # API/インターフェース層
│   ├── service/           # ビジネスロジック層
│   ├── repository/        # データアクセス層
│   └── models/            # ドメインモデル層
├── tests/                 # テストコード
├── config/                # 設定ファイル
├── pyproject.toml         # プロジェクト設定
└── .pre-commit-config.yaml # pre-commitフック設定
```

### コーディング規約
- **型ヒント**: 全ての関数・メソッドに必須
- **docstring**: パブリックAPIに必須（Google/NumPy形式）
- **行長制限**: 88文字
- **データ検証**: Pydantic v2積極活用
- **関数設計**: 小さく・焦点を絞った関数

### pre-commit設定例
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
```

## 個人的な開発方針

### セキュリティファースト
- 防御的セキュリティタスクに特化
- 脆弱性検出・分析ツールの積極活用
- セキュアコーディングガイドラインの遵守

### 効率的なツール使用
- 並行実行を優先: 複数のBashコマンドは同時実行
- 検索順序: Task → Grep → Glob
- ファイル操作: Read → Edit/MultiEdit → Write