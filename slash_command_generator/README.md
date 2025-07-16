# v3コマンド生成ツール

v3プロジェクト企画フェーズのスラッシュコマンドを統一された設定とテンプレートから生成するツールです。

## 使用方法

```bash
uv run --directory v3_command_generator python generator.py
```

## ファイル構成

```
v3_command_generator/
├── config.yaml           # 全設定データ（ステップ定義、質問項目、依存関係等）
├── template.md           # Jinjaテンプレート（共通構造とロジック）
├── generator.py          # 生成スクリプト
├── pyproject.toml        # uv依存関係管理
└── README.md            # このファイル
```

## 出力先

`commands/v3/` ディレクトリに以下のファイルが生成されます：

- `phase1-step1.md` - アイデアと目標の明確化
- `phase1-step2.md` - ユーザー要件定義
- `phase1-step3.md` - ユーザーインタラクション設計
- `phase2-step1.md` - データ構造定義
- `phase2-step2.md` - システム全体データフロー
- `phase2-step3.md` - API設計
- `phase3-step1.md` - テスト計画策定
- `phase3-step2.md` - 実装設計

## 設定の編集

- **ステップ追加・修正**: `config.yaml` の `step_references` と `individual_elements` を編集
- **テンプレート修正**: `template.md` のJinja2テンプレートを編集
- **出力先変更**: `config.yaml` の `common.commands_output_dir` を編集

## 依存関係

- Python 3.12+
- PyYAML 6.0+
- Jinja2 3.1.0+

## 特徴

- **表記統一**: ステップ参照を一元管理し、表記揺れを防止
- **構造化**: step別比較可能な設定構造
- **分離**: 設定データとテンプレートロジックの明確な分離
- **uv管理**: 依存関係の確実な管理