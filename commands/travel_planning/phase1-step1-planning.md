---
allowed-tools: ["Read", "Write", "Edit", "Bash", "WebSearch", "WebFetch", "mcp__booking-fetcher__fetch_bookingcom_hotels", "TodoWrite"]
description: "旅行コンセプト策定と候補地・候補日時の範囲絞込み"
---# 旅行企画・候補絞込み

プロジェクトID: $ARGUMENTS

## 概要
この手順では、旅行の **なぜ行くのか** という動機と **どんな旅行にしたいか** というコンセプトを明確化し、
**候補地（2-4箇所程度）** と **候補日時の範囲** を絞り込みます。
最終決定はせず、次ステップで具体調査する対象の範囲を設定することが目的です。


## プロジェクト全体構想

この手順は以下の全体的なフェーズ構造の一部です：

### Phase 1: 旅行企画・候補絞込み
旅行コンセプトを策定し、候補地・候補日時を範囲指定
- **🎯 /Users/mikke/Documents/planning_docs/travel_planning/$ARGUMENTS/phase1-step1-planning.md** # 旅行企画・候補絞込み ← **現在のステップ**

### Phase 2: 具体調査・決定
交通・観光・宿泊の具体的調査と行程作成
- /Users/mikke/Documents/planning_docs/travel_planning/$ARGUMENTS/phase2-step1-transport-sightseeing.md # 交通・観光調査
- /Users/mikke/Documents/planning_docs/travel_planning/$ARGUMENTS/phase2-step2-itinerary-draft.md # 行程大枠作成
- /Users/mikke/Documents/planning_docs/travel_planning/$ARGUMENTS/phase2-step3-hotel-search.md # ホテル調査・決定

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


- **依存元**: なし（旅行計画の起点）
- **依存先**: 交通・観光調査
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
- 今回の旅行の主な目的は何ですか？（リラックス、観光、体験、学習など）
- どんな旅行スタイルを希望していますか？（のんびり、アクティブ、文化重視など）
- 旅行で最も重視したいことは何ですか？
- 避けたいこと、苦手なことはありますか？
- 一緒に行く人はいますか？その人の希望も考慮する必要がありますか？
- 希望する宿泊施設のタイプはありますか？（高級ホテル、ビジネスホテル、旅館、民宿、ゲストハウス、リゾートホテル、温泉宿など）
- 宿泊施設で重視したいポイントは何ですか？（立地・アクセス、価格、設備・アメニティ、サービス品質、雰囲気・コンセプト、食事内容など）
- 希望する移動手段はありますか？（飛行機、新幹線・特急、高速バス、自家用車・レンタカー、船・フェリー、現地交通手段など）
- 移動手段で重視したいポイントは何ですか？（価格・コスト、移動時間・速度、快適性、利便性・アクセス、景色・体験、環境負荷など）
- 候補となる地域や国はありますか？（2-4箇所程度に絞り込み）
- 候補となる時期・期間はいつ頃ですか？（範囲で指定）
- 予算の大まかな上限はどの程度ですか？


### 4. 設計案の提示と承認
収集した情報を基に、設計案を提示し、ユーザーの承認を得てください。

### 5. 最終確認とドキュメント作成

承認された内容を @/Users/mikke/Documents/planning_docs/travel_planning/$ARGUMENTS/phase1-step1-planning.md に出力してください

## 重要な対話ポイント
- **旅行の本質的な目的の抽出が最重要**: 「なんとなく行きたい」ではなく、具体的な動機や期待を明確化してください
- **候補地は2-4箇所程度に絞込み**: 多すぎると次ステップでの調査が困難、少なすぎると選択肢が不足
- **候補日時は範囲指定**: 「3月中旬〜4月上旬」「夏休み期間」など、柔軟性を保った設定
- **最終決定はしない**: 次ステップでの具体調査に必要な範囲設定に留める



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

