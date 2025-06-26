---
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep"]
description: "要求分析結果をサンプルデータで検証しHTMLレポートを生成"
---

# 分析レポート作成: $ARGUMENTS

## 要求分析結果の読み込み
@$ARGUMENTS

## サンプルデータ検証

### 1. 関連テストデータの収集
!find . -name "*test*" -type f -name "*.json" -o -name "*.yaml" -o -name "*.csv" | head -10

### 2. 既存データスキーマの確認
!find . -name "*schema*" -o -name "*model*" -type f -name "*.py" -o -name "*.ts" -o -name "*.js" | head -5

## HTMLレポート生成

### レポート構成
- **要求概要**: 分析した要求の要約
- **ユーザーストーリー検証**: 各ストーリーの実現可能性
- **サンプルデータ分析**: 実際のデータを使った検証結果
- **技術的実装課題**: 特定された技術的な問題点
- **推奨アプローチ**: 最適な実装方針
- **リスク評価**: 潜在的なリスクと対策

### HTMLテンプレート
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>要求分析レポート</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        h3 { color: #7f8c8d; }
        .summary { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .story { background: #f8f9fa; border-left: 4px solid #3498db; padding: 15px; margin: 10px 0; }
        .verification { background: #d5f4e6; border-left: 4px solid #27ae60; padding: 15px; margin: 10px 0; }
        .issue { background: #ffeaa7; border-left: 4px solid #fdcb6e; padding: 15px; margin: 10px 0; }
        .risk { background: #fab1a0; border-left: 4px solid #e17055; padding: 15px; margin: 10px 0; }
        .data-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        .data-table th, .data-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .data-table th { background-color: #3498db; color: white; }
        .code { background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 5px; overflow-x: auto; font-family: 'Courier New', monospace; }
        .timestamp { color: #7f8c8d; font-size: 0.9em; text-align: right; margin-top: 20px; }
        .status-pass { color: #27ae60; font-weight: bold; }
        .status-fail { color: #e74c3c; font-weight: bold; }
        .status-warning { color: #f39c12; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>要求分析レポート</h1>
        
        <div class="summary">
            <h2>📋 要求概要</h2>
            <!-- 要求分析結果の要約をここに挿入 -->
        </div>

        <h2>📖 ユーザーストーリー検証</h2>
        <!-- 各ストーリーの検証結果をここに挿入 -->

        <h2>🔍 サンプルデータ分析</h2>
        <!-- データ分析結果をここに挿入 -->

        <h2>⚠️ 技術的実装課題</h2>
        <!-- 技術的な問題点をここに挿入 -->

        <h2>💡 推奨アプローチ</h2>
        <!-- 実装方針をここに挿入 -->

        <h2>🚨 リスク評価</h2>
        <!-- リスクと対策をここに挿入 -->

        <div class="timestamp">
            レポート生成日時: {TIMESTAMP}
        </div>
    </div>
</body>
</html>
```

### データ検証スクリプト
```python
import json
import csv
import yaml
from pathlib import Path
from datetime import datetime

def validate_sample_data():
    """サンプルデータの検証を実行"""
    results = {
        'data_sources': [],
        'validation_results': [],
        'schema_compliance': [],
        'performance_metrics': {}
    }
    
    # データソースの検出と分析
    for data_file in Path('.').rglob('*.json'):
        try:
            with open(data_file) as f:
                data = json.load(f)
                results['data_sources'].append({
                    'file': str(data_file),
                    'type': 'json',
                    'size': len(str(data)),
                    'keys': list(data.keys()) if isinstance(data, dict) else 'array'
                })
        except Exception as e:
            results['validation_results'].append({
                'file': str(data_file),
                'status': 'error',
                'message': str(e)
            })
    
    return results

if __name__ == "__main__":
    validation_results = validate_sample_data()
    print(json.dumps(validation_results, indent=2, ensure_ascii=False))
```

## レポート出力ファイル名
`analysis-report-{YYYYMMDD-HHMMSS}.html`

## 実行手順
1. 要求分析結果ファイルを解析
2. プロジェクト内のサンプルデータを収集・検証
3. ユーザーストーリーの実現可能性を評価
4. 技術的課題とリスクを特定
5. HTMLレポートを生成・出力

## 成果物
- 包括的な分析レポート（HTML形式）
- データ検証結果の詳細
- 実装推奨事項とリスク評価