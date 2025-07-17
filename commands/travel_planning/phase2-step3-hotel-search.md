---
allowed-tools: ["Read", "Write", "Edit", "Bash", "WebSearch", "WebFetch", "mcp__booking-fetcher__fetch_bookingcom_hotels", "TodoWrite"]
description: "ホテル調査・比較分析・決定"
---# ホテル調査・決定

プロジェクトID: $ARGUMENTS

## 概要
MCPツール（mcp__booking-fetcher__fetch_bookingcom_hotels）を使用して、**ホテル調査・比較分析**を実施します。
1万円以内のコスパ重視推奨と、マトリクス分析による価格比較を行います。


## プロジェクト全体構想

この手順は以下の全体的なフェーズ構造の一部です：

### Phase 1: 旅行企画・候補絞込み
旅行コンセプトを策定し、候補地・候補日時を範囲指定
- /Users/mikke/Documents/planning_docs/travel_planning/$ARGUMENTS/phase1-step1-planning.md # 旅行企画・候補絞込み

### Phase 2: 具体調査・決定
交通・観光・宿泊の具体的調査と行程作成
- /Users/mikke/Documents/planning_docs/travel_planning/$ARGUMENTS/phase2-step1-transport-sightseeing.md # 交通・観光調査
- /Users/mikke/Documents/planning_docs/travel_planning/$ARGUMENTS/phase2-step2-itinerary-draft.md # 行程大枠作成
- **🎯 /Users/mikke/Documents/planning_docs/travel_planning/$ARGUMENTS/phase2-step3-hotel-search.md** # ホテル調査・決定 ← **現在のステップ**

### Phase 3: 詳細化・準備
詳細スケジュール作成と最終準備
- /Users/mikke/Documents/planning_docs/travel_planning/$ARGUMENTS/phase3-step1-schedule-detail.md # 詳細スケジュール検討
- /Users/mikke/Documents/planning_docs/travel_planning/$ARGUMENTS/phase3-step2-final-prep.md # 最終準備・持ち物チェック


**複数の質問がある場合の処理原則**：
複数の項目について確認が必要な場合は、必ず一つずつ順番に処理し、各質問の回答を確認してから次の質問に進む。一度に全ての質問を提示することは避け、段階的なアプローチを取る。


## 実行手順

### 1. 前ステップの成果物確認

実際の作成済みファイル一覧
```bash
!mkdir -p /Users/mikke/Documents/planning_docs/travel_planning/$ARGUMENTS
!tree -L 2 /Users/mikke/Documents/planning_docs/travel_planning/$ARGUMENTS | ls -l /Users/mikke/Documents/planning_docs/travel_planning/$ARGUMENTS
```

### 2. 依存関係の確認

依存元のドキュメントを確認してから次に進んでください


- **依存元**: 行程大枠作成
- **依存先**: 詳細スケジュール検討
### 3. 情報収集と質問

**対話原則：**
- ユーザーの入力負荷を軽減するため、選択肢形式での質問を優先
- 複数の質問がある場合は、必ず一つずつ順番に処理し、各質問の回答を確認してから次の質問に進む
- 曖昧な回答には具体例を提示して明確化を図る
- ユーザーの理解レベルや経験に合わせた現実的な提案を行う

**段階的質問テンプレート：**
```
[{purpose}]のため、まず最初の項目について番号で選択してください：

## {item_title}
以下から該当するものを選んでください（複数選択可）：
1. {option1_description}
2. {option2_description}
3. {option3_description}
4. その他（具体的に記入：_______）
---
User: 回答例: 1, 3
（{item_title}の回答を確認後、次の項目について質問）

---

## {next_item_title}
以下から最も近いものを選んでください：
1. {option1_description}
2. {option2_description}
3. {option3_description}
4. その他（具体的に記入：_______）

---
User: 回答例: 2
```


**確認すべき項目：**


### MCPツールでのホテル調査・比較分析

**実行アプローチ**:
- **事前ヒアリング無し**: 前ステップの情報を基に即座にホテル調査を開始
- **マトリクス作成優先**: 詳細確認の前にまず包括的なホテル比較表を作成
- **結果提示後の調整**: マトリクス提示後に必要に応じて条件調整を行う

**実行手順**:
1. 引数解析と検証（エリア名・期間抽出）
2. MCPツールでのデータ取得（mcp__booking-fetcher__fetch_bookingcom_hotels）
3. データ処理とフィルタリング（ドミトリー・カプセル・ホステル除外）
4. マトリクス分析の実行（日程×価格比較表）
5. 価格帯別推奨分析（1万円以内コスパ重視）
6. おすすめホテルランキング生成
7. **結果提示後の確認**: 必要に応じて条件調整やフィルタリングを実施

**除外対象**:
- ドミトリー、カプセルホテル、ホステル、ゲストハウス、民宿
- バックパッカー向け宿泊施設、宿泊単価が著しく高い施設

**出力形式**:
```markdown
## {エリア名}ホテル予約状況マトリクス（{年月}）

| ホテル名 | {日程1} | {日程2} | {日程3} | 評価 |
|----------|---------|---------|---------|------|
| **ホテルA** | ¥XX,XXX | ¥XX,XXX | ¥XX,XXX | X.X★ |

## 🏆 コスパ重視おすすめホテル（1泊1万円以内）

### 1位: {ホテル名} ⭐{評価}点
- **推奨理由**: {推奨理由}
- **平均料金**: ¥{平均価格}/泊
- **利用可能日**: {利用可能日数}/{全日程数}日
```

**マトリクス作成後の確認**:
- 予算調整が必要な場合のフィルタリング
- 特別な設備要求がある場合の絞り込み
- 立地条件の優先順位変更が必要な場合の再分析

### 4. 設計案の提示と承認
収集した情報を基に、設計案を提示し、ユーザーの承認を得てください。

### 5. 最終確認とドキュメント作成

承認された内容を @/Users/mikke/Documents/planning_docs/travel_planning/$ARGUMENTS/phase2-step3-hotel-search.md に出力してください

## 重要な対話ポイント
- **MCPツールの活用**: mcp__booking-fetcher__fetch_bookingcom_hotelsを使用
- **即座にマトリクス分析実行**: 前ステップの情報を基に直ちにホテル調査を開始
- **コスパ重視の分析**: 1万円以内の推奨ホテルを中心に比較
- **マトリクス分析**: 日程×価格の比較表で最適な選択肢を提示
- **行程に適した立地**: Phase2-step2の行程を考慮した立地選択
- **結果提示後の確認**: マトリクス作成後に必要に応じて条件調整



### 6. ステップ完了後の次ステップガイド
### 🚀 次のステップガイド

このステップで収集・整理した情報を基に、次の候補ステップを提案してください：

**ガイド原則**:
- 今回の成果物の内容に基づいて適切な次ステップを提案
- 不要と思われるステップには理由とともにスキップ提案
- 各候補ステップで何をするかを簡潔に説明
- 実行コマンドを明示
- 最終的な選択はユーザーに委ねる

**スキップ判断基準例**:
- 短期間・単純な旅行 → phase3-step1（詳細準備工程）をスキップ
- 慣れた目的地・国内旅行 → phase3-step1を簡略化
- 海外・長期・特殊な旅行 → 全ステップ実行推奨

