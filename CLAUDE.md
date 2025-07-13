# Claude Code 個人設定・メモリファイル

## カスタムスラッシュコマンド設定

### 基本構造
カスタムコマンドは Markdown ファイル（.md）で作成し、YAMLフロントマターでメタデータを設定。

### 個人用コマンド (`~/.claude/commands/`)
`/user:` プレフィックスで呼び出し

#### セキュリティレビューコマンド例
ファイル: `~/.claude/commands/v1/security-review.md`
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
ファイル: `.claude/commands/v1/optimize.md`
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
ファイル: `.claude/commands/v1/frontend/component-audit.md`
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
ファイル: `.claude/commands/v1/backend/api-review.md`
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

### 重要: uv環境の自動検出と使用
**CRITICAL**: プロジェクトに `uv.lock` ファイルが存在する場合は、必ず `uv` を使用してください。システムのPythonは使用せず、すべてのPythonコマンドを `uv run` 経由で実行してください。

```bash
# uv.lockファイルの確認（最初に必ず実行）
ls uv.lock

# uv.lockが存在する場合の必須パターン
uv run python script.py     # ✅ 正しい
python script.py            # ❌ 間違い（システムPython使用）

uv run pytest               # ✅ 正しい
pytest                      # ❌ 間違い（システムPython使用）

uv run ruff check .         # ✅ 正しい
ruff check .                # ❌ 間違い（システムPython使用）
```

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
├── output/                # 生成物・中間データ格納ディレクトリ
│   ├── docs/              # 生成されたドキュメント
│   ├── reports/           # 分析レポート・HTMLファイル
│   ├── data/              # 中間データ・JSON・CSV等
│   ├── logs/              # ログファイル
│   └── artifacts/         # その他の成果物
├── pyproject.toml         # プロジェクト設定
└── .pre-commit-config.yaml # pre-commitフック設定
```

### 重要: 生成物の出力先管理
**CRITICAL**: コードから生成される全ての中間生成物・データ・レポートは必ず `output/` ディレクトリ配下に配置してください。

#### 出力先の分類と使用例
```bash
# ドキュメント生成
output/docs/仕様書-YYYYMMDD.md
output/docs/設計書-YYYYMMDD.md
output/docs/受け入れテスト基準-YYYYMMDD.md

# レポート生成
output/reports/分析レポート-YYYYMMDD.html
output/reports/セキュリティレポート-YYYYMMDD.html
output/reports/パフォーマンステスト結果-YYYYMMDD.html

# データファイル
output/data/サンプルデータ.json
output/data/テストデータ.csv
output/data/設定データ.yaml

# ログファイル
output/logs/テスト実行ログ-YYYYMMDD.log
output/logs/ビルドログ-YYYYMMDD.log

# その他成果物
output/artifacts/スクリーンショット-YYYYMMDD.png
output/artifacts/データベーススキーマ.sql
```

#### 必須の出力パターン
- **ファイル命名**: `[種類]-[YYYYMMDD-HHMMSS].[拡張子]` 形式
- **ディレクトリ作成**: 出力前に必要なサブディレクトリを作成
- **gitignore**: `output/` ディレクトリを適切に管理（必要に応じて除外）

#### 出力前のディレクトリ確認例
```bash
# outputディレクトリ構造の確認・作成
mkdir -p output/{docs,reports,data,logs,artifacts}

# 生成前の確認
ls -la output/
```

### コーディング規約

#### 基本規約
- **型ヒント**: 全ての関数・メソッドに必須
- **docstring**: パブリックAPIに必須（Google/NumPy形式）
- **行長制限**: 88文字
- **データ検証**: Pydantic v2積極活用
- **関数設計**: 小さく・焦点を絞った関数

#### 設計原則
- **DRY原則の徹底**: 重複コードを排除し、同一機能を一箇所に集約する。これにより、変更箇所を最小限に抑え、保守性を高める。
- **簡潔性優先**: 同等機能なら最もコンパクトな記述を採用
- **レイヤード設計**: API層 → サービス層 → リポジトリ層 ← モデル層
- **依存性注入**: インターフェース定義による抽象基底クラス活用

#### TDD実装規約
- **Red-Green-Refactorサイクル**: 意図的失敗→最小実装→リファクタリング
- **高抽象・低コスト**: ユーザー視点、高速実行、最小セットアップ
- **簡素なテスト原則**: 核心機能のみ、公開インターフェース重視
- **保守性優先**: 実装変更時にテスト修正が不要な設計
- **テスト実装の厳格な規約**:
    - **ユニットテスト原則不使用**: `unittest` は原則として記述しない。
    - **Mock/Stubの禁止**: 統合テスト、受け入れテストでは `mock`, `stub`, `skip` を使用してはならない。
    - **例外処理の制限**: 統合テスト、受け入れテストでは、異常系のテストを除き `try-except` の使用を禁止する。
- **冗長性の最小化**: 必要性が高い場合を除いて冗長な記述は避ける。これはDRY原則の徹底に直結する。
- **README記述の制限**: ユーザーからの明示的な指示がない限り、`README.md` を記述してはならない。

#### セキュリティ実装
- **入力検証**: SQLインジェクション、XSS、パストラバーサル対策
- **ログセキュリティ**: 機密情報のサニタイズ必須
- **防御的プログラミング**: 外部データエラーの適切な処理

#### 命名規則
- **レイヤード構造**: `[feature]_api.py`, `[feature]_service.py`, `[feature]_repository.py`
- **成果物命名**: `[種類]-YYYYMMDD.[拡張子]` 形式

#### 品質保証・テスト戦略

**CRITICAL**: テスト実行前に、`unittest`以外のテストコード (`tests/integration/`, `tests/acceptance/` 等) に `mock` や `stub` の文字列が残っていないか確認してください。もし残っている場合は、ユーザーに対応方針を確認する必要があります。

```bash
# 段階的テスト実行規約
uv run --frozen ruff check .              # リント
uv run --frozen ruff format .             # フォーマット
uv run --frozen pyright                   # 型チェック
uv run --frozen pytest tests/unit/       # ユニットテスト（原則記述しない）
uv run --frozen pytest tests/acceptance/ # 受け入れテスト
uv run --frozen pytest tests/integration/ # 統合テスト
```

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

### 個人的な開発方針

#### セキュリティファースト
- 防御的セキュリティタスクに特化
- 脆弱性検出・分析ツールの積極活用
- セキュアコーディングガイドラインの遵守
- **冗長性の最小化**: 必要性が高い場合を除いて冗長な記述は避ける
- **README記述の制限**: ユーザーからの明示的な指示がない限り、`README.md` を記述してはならない。

### 効率的なツール使用
- 並行実行を優先: 複数のBashコマンドは同時実行
- 検索順序: Task → Grep → Glob
- ファイル操作: Read → Edit/MultiEdit → Write
- **冗長性の最小化**: 必要性が高い場合を除いて冗長な記述は避ける

### アーキテクチャ変更管理
**CRITICAL**: 編集作業後にアーキテクチャの状態が変更される場合は、必ず `.claude/architecture.md` を更新してください。また、作業開始前にこのファイルを確認してから作業に入ってください。

#### 必須のアーキテクチャ管理フロー
```bash
# 1. 作業開始前: アーキテクチャ状態の確認
!test -f .claude/architecture.md && echo "アーキテクチャファイル存在" || echo "アーキテクチャファイル未作成"
![ -f .claude/architecture.md ] && cat .claude/architecture.md

# 2. 編集作業実施
# [実際の編集作業]

# 3. 作業完了後: アーキテクチャ変更の確認と更新
# 以下のような変更がある場合は .claude/architecture.md を更新:
# - 新しいコンポーネント・モジュールの追加
# - 既存コンポーネント間の依存関係の変更
# - レイヤード設計の構造変更
# - API インターフェースの変更
# - データフローの変更
# - 設計パターンの変更

# アーキテクチャファイルの参照例
@.claude/architecture.md
```

#### アーキテクチャファイルの記載内容
- **システム全体構成**: 主要コンポーネントと役割
- **レイヤード設計**: 各層の責務と依存関係
- **データフロー**: 情報の流れと処理の流れ
- **設計パターン**: 採用している設計パターン
- **外部システム連携**: 外部API・サービスとの連携方法
- **セキュリティ境界**: 認証・認可の仕組み

### Git操作の安全性確保
**CRITICAL**: `git add .` は絶対に使用禁止。必ず個別ファイル指定またはステージング内容を事前確認してください。

#### 必須のGit操作パターン
```bash
# ❌ 危険: 全ファイルを無条件でステージング
git add .

# ✅ 安全: 事前確認してから個別追加
git status                    # 変更ファイルの確認
git diff                      # 変更内容の確認
git add src/specific_file.py  # 個別ファイル指定
git add src/module/           # ディレクトリ指定

# ✅ 安全: インタラクティブステージング
git add -i                    # 対話的に選択
git add -p                    # パッチ単位で選択
```

#### コミット前の必須チェック項目
```bash
# 1. ステージング内容の確認
git status
git diff --cached

# 2. 除外すべきファイルの検出
git status --porcelain | grep -E "\.(log|tmp|cache|pyc|pyo|pyd|__pycache__|\.DS_Store)"
git status --porcelain | grep -E "output/"
git status --porcelain | grep -E "(secret|password|token|key|credential)"

# 3. 一時的なファイルの検出
git status --porcelain | grep -E "(temp|tmp|test_|debug_|scratch)"
```

#### 自動除外すべきファイル/ディレクトリ
- **output/**: 生成物・中間データ（基本的に除外）
- **logs/**: ログファイル
- **temp/**, **tmp/**: 一時ファイル
- **test_**, **debug_**, **scratch**: 一時的なスクリプト
- **secret**, **password**, **token**, **key**: 機密情報
- **\*.log**, **\*.tmp**, **\*.cache**: 一時データ
- **__pycache__/**, **\*.pyc**: Python実行時生成ファイル

#### 推奨gitignore追加項目
```bash
# 生成物・中間データ
output/
logs/
temp/
tmp/

# 一時的なスクリプト
test_*
debug_*
scratch*

# 機密情報ファイル
*secret*
*password*
*token*
*key*
*credential*

# 各種一時ファイル
*.log
*.tmp
*.cache
.DS_Store
```