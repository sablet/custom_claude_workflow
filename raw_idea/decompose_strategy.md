# ビジネスプロセス要件定義 - データ構造仕様

## 概要

ビジネスプロセスの要件定義を階層的かつ再帰的なデータ構造として表現します。
この構造により、複雑なビジネスプロセスを明確に定義し、各要素の関係性を厳密に管理できます。

## 1. 基本型定義

### 1.1 列挙型

```python
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field

class ProcessType(str, Enum):
    """プロセスタイプの定義"""
    ROOT = "root"           # トップレベルの要望
    PRIMITIVE = "primitive" # 原子的タスク（分割不可）
    COMPOUND = "compound"   # 複合タスク（子プロセスを持つ）

class FlowType(str, Enum):
    """フロー制御タイプの定義"""
    SEQUENCE = "sequence"   # 順次実行
    BRANCH = "branch"       # 条件分岐
    LOOP = "loop"          # 繰り返し
```

### 1.2 データセット型

```python
class Dataset(BaseModel):
    """インプット/アウトプットデータの定義"""
    name: str = Field(..., description="データセット名")
    description: str = Field(..., description="データセットの説明")
    format: Optional[str] = Field(None, description="データ形式")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "name": "未承認請求書",
                    "description": "承認待ちの請求書データ",
                    "format": "JSON"
                }
            ]
        }
```

## 2. プロセス定義

### 2.1 基本プロセス構造

```python
class ProcessNode(BaseModel):
    """プロセスノードの基本構造（再帰的定義）"""
    process_id: str = Field(..., description="プロセス一意識別子")
    name: str = Field(..., description="プロセス名/目的")
    process_type: ProcessType = Field(..., description="プロセスタイプ")
    
    inputs: List[Dataset] = Field(default_factory=list, description="入力データセット")
    outputs: List[Dataset] = Field(default_factory=list, description="出力データセット")
    constraints: Optional[str] = Field(None, description="制約事項・要件")
    
    # 再帰的構造: 子プロセスフロー
    process_flow: Optional['ProcessFlow'] = Field(None, description="子プロセスフロー")

    class Config:
        schema_extra = {
            "examples": [
                {
                    "process_id": "APPROVE-INVOICE",
                    "name": "請求書承認プロセス",
                    "process_type": "compound",
                    "inputs": [
                        {
                            "name": "未承認請求書",
                            "description": "承認待ちの請求書データ"
                        }
                    ],
                    "outputs": [
                        {
                            "name": "承認済み請求書",
                            "description": "承認処理済みの請求書データ"
                        }
                    ],
                    "constraints": "24時間以内に承認処理を完了すること"
                }
            ]
        }
```

### 2.2 フロー制御構造

```python
class ProcessStep(BaseModel):
    """プロセス実行ステップ"""
    process_ref: str = Field(..., description="参照プロセスID")
    input_mapping: Optional[Dict[str, str]] = Field(None, description="入力データマッピング")
    condition: Optional[str] = Field(None, description="実行条件")

class ProcessFlow(BaseModel):
    """プロセスフロー定義（再帰的構造の核心）"""
    flow_type: FlowType = Field(..., description="フロー制御タイプ")
    steps: List[ProcessStep] = Field(..., description="実行ステップリスト")
    
    # 条件分岐・ループ用の追加設定
    condition: Optional[str] = Field(None, description="フロー実行条件")
    loop_condition: Optional[str] = Field(None, description="ループ継続条件")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "flow_type": "sequence",
                    "steps": [
                        {"process_ref": "VALIDATE-INVOICE"},
                        {"process_ref": "CHECK-APPROVAL-AUTHORITY"},
                        {"process_ref": "EXECUTE-APPROVAL"}
                    ]
                },
                {
                    "flow_type": "branch",
                    "steps": [
                        {
                            "process_ref": "AUTO-APPROVE",
                            "condition": "金額 <= 10000"
                        },
                        {
                            "process_ref": "MANUAL-APPROVE",
                            "condition": "金額 > 10000"
                        }
                    ]
                }
            ]
        }
```

## 3. 完全なデータ構造

### 3.1 統合モデル

```python
# 前方参照の解決
ProcessNode.model_rebuild()

class BusinessProcessDefinition(BaseModel):
    """ビジネスプロセス定義の完全な構造"""
    root_process: ProcessNode = Field(..., description="ルートプロセス")
    all_processes: Dict[str, ProcessNode] = Field(..., description="全プロセス定義辞書")
    
    def validate_references(self) -> bool:
        """プロセス参照の整合性を検証"""
        # 実装: すべてのprocess_refがall_processesに存在することを確認
        pass
    
    def get_process_hierarchy(self) -> Dict:
        """プロセス階層構造を取得"""
        # 実装: 階層構造の可視化データを生成
        pass

    class Config:
        schema_extra = {
            "examples": [
                {
                    "root_process": {
                        "process_id": "INVOICE-PROCESSING",
                        "name": "請求書処理全体プロセス",
                        "process_type": "root",
                        "process_flow": {
                            "flow_type": "sequence",
                            "steps": [
                                {"process_ref": "RECEIVE-INVOICE"},
                                {"process_ref": "APPROVE-INVOICE"},
                                {"process_ref": "REGISTER-PAYMENT"}
                            ]
                        }
                    },
                    "all_processes": {
                        "INVOICE-PROCESSING": "...",
                        "RECEIVE-INVOICE": "...",
                        "APPROVE-INVOICE": "...",
                        "REGISTER-PAYMENT": "..."
                    }
                }
            ]
        }
```

## 4. 使用例

### 4.1 シンプルな例

```python
# 原子的プロセス（primitive）
validate_invoice = ProcessNode(
    process_id="VALIDATE-INVOICE",
    name="請求書フォーマット検証",
    process_type=ProcessType.PRIMITIVE,
    inputs=[Dataset(name="生請求書", description="受信した請求書データ")],
    outputs=[Dataset(name="検証結果", description="フォーマット検証結果")]
)

# 複合プロセス（compound）
invoice_approval = ProcessNode(
    process_id="APPROVE-INVOICE",
    name="請求書承認プロセス",
    process_type=ProcessType.COMPOUND,
    process_flow=ProcessFlow(
        flow_type=FlowType.SEQUENCE,
        steps=[
            ProcessStep(process_ref="VALIDATE-INVOICE"),
            ProcessStep(process_ref="CHECK-AUTHORITY"),
            ProcessStep(process_ref="EXECUTE-APPROVAL")
        ]
    )
)
```

### 4.2 条件分岐の例

```python
approval_branch = ProcessFlow(
    flow_type=FlowType.BRANCH,
    steps=[
        ProcessStep(
            process_ref="AUTO-APPROVE",
            condition="invoice.amount <= 10000"
        ),
        ProcessStep(
            process_ref="MANUAL-APPROVE", 
            condition="invoice.amount > 10000"
        )
    ]
)
```

### 4.3 深い階層構造の例（深さ4レベル）

```python
# レベル4: 最も深い原子的タスク
email_send = ProcessNode(
    process_id="EMAIL-SEND",
    name="承認依頼メール送信",
    process_type=ProcessType.PRIMITIVE,
    inputs=[Dataset(name="承認者情報", description="承認者のメールアドレスと名前")],
    outputs=[Dataset(name="送信結果", description="メール送信成功/失敗の結果")]
)

system_notify = ProcessNode(
    process_id="SYSTEM-NOTIFY",
    name="システム内通知作成",
    process_type=ProcessType.PRIMITIVE,
    inputs=[Dataset(name="通知内容", description="システム通知の詳細情報")],
    outputs=[Dataset(name="通知ID", description="作成された通知の識別子")]
)

# レベル3: 通知処理（複合タスク）
notification_process = ProcessNode(
    process_id="NOTIFICATION-PROCESS",
    name="承認依頼通知処理",
    process_type=ProcessType.COMPOUND,
    inputs=[Dataset(name="承認依頼情報", description="承認が必要な請求書と承認者情報")],
    outputs=[Dataset(name="通知完了確認", description="全通知の完了状況")],
    process_flow=ProcessFlow(
        flow_type=FlowType.SEQUENCE,
        steps=[
            ProcessStep(process_ref="EMAIL-SEND"),
            ProcessStep(process_ref="SYSTEM-NOTIFY")
        ]
    )
)

amount_check = ProcessNode(
    process_id="AMOUNT-CHECK",
    name="金額妥当性チェック",
    process_type=ProcessType.PRIMITIVE,
    inputs=[Dataset(name="請求書データ", description="金額を含む請求書情報")],
    outputs=[Dataset(name="チェック結果", description="金額の妥当性判定結果")]
)

approver_identify = ProcessNode(
    process_id="APPROVER-IDENTIFY",
    name="承認者特定",
    process_type=ProcessType.PRIMITIVE,
    inputs=[Dataset(name="請求書データ", description="部署・金額を含む請求書情報")],
    outputs=[Dataset(name="承認者リスト", description="特定された承認者の一覧")]
)

# レベル2: 承認判定処理（複合タスク）
approval_decision = ProcessNode(
    process_id="APPROVAL-DECISION",
    name="承認可否判定処理",
    process_type=ProcessType.COMPOUND,
    inputs=[Dataset(name="検証済み請求書", description="フォーマット検証済みの請求書データ")],
    outputs=[Dataset(name="承認判定結果", description="承認/却下の判定と理由")],
    process_flow=ProcessFlow(
        flow_type=FlowType.SEQUENCE,
        steps=[
            ProcessStep(process_ref="AMOUNT-CHECK"),
            ProcessStep(process_ref="APPROVER-IDENTIFY"),
            ProcessStep(process_ref="NOTIFICATION-PROCESS")
        ]
    )
)

authority_check = ProcessNode(
    process_id="AUTHORITY-CHECK",
    name="承認権限確認",
    process_type=ProcessType.PRIMITIVE,
    inputs=[Dataset(name="ユーザー情報", description="承認を実行しようとするユーザーの情報")],
    outputs=[Dataset(name="権限結果", description="承認権限の有無")]
)

# レベル1: 承認処理全体（複合タスク）
approval_process = ProcessNode(
    process_id="APPROVAL-PROCESS",
    name="請求書承認処理",
    process_type=ProcessType.COMPOUND,
    inputs=[Dataset(name="受信請求書", description="受信した請求書データ")],
    outputs=[Dataset(name="承認済み請求書", description="承認処理完了後の請求書データ")],
    constraints="承認は受信から48時間以内に完了すること",
    process_flow=ProcessFlow(
        flow_type=FlowType.SEQUENCE,
        steps=[
            ProcessStep(process_ref="AUTHORITY-CHECK"),
            ProcessStep(process_ref="APPROVAL-DECISION")
        ]
    )
)

# レベル0: ルートプロセス
invoice_processing_root = ProcessNode(
    process_id="INVOICE-PROCESSING-ROOT",
    name="請求書処理全体システム",
    process_type=ProcessType.ROOT,
    inputs=[Dataset(name="外部請求書ファイル", description="外部から受信した請求書ファイル")],
    outputs=[Dataset(name="処理完了通知", description="全処理完了の通知")],
    process_flow=ProcessFlow(
        flow_type=FlowType.SEQUENCE,
        steps=[
            ProcessStep(process_ref="FILE-RECEIVE"),
            ProcessStep(process_ref="APPROVAL-PROCESS"),
            ProcessStep(process_ref="PAYMENT-REGISTER")
        ]
    )
)

# 完全なプロセス定義（階層関係を含む）
complete_process_definition = BusinessProcessDefinition(
    root_process=invoice_processing_root,
    all_processes={
        # レベル0（ROOT）
        "INVOICE-PROCESSING-ROOT": invoice_processing_root,
        
        # レベル1（COMPOUND）
        "APPROVAL-PROCESS": approval_process,
        
        # レベル2（COMPOUND/PRIMITIVE）
        "AUTHORITY-CHECK": authority_check,
        "APPROVAL-DECISION": approval_decision,
        
        # レベル3（COMPOUND/PRIMITIVE）
        "AMOUNT-CHECK": amount_check,
        "APPROVER-IDENTIFY": approver_identify,
        "NOTIFICATION-PROCESS": notification_process,
        
        # レベル4（PRIMITIVE）
        "EMAIL-SEND": email_send,
        "SYSTEM-NOTIFY": system_notify,
        
        # その他のプロセス（簡略化）
        "FILE-RECEIVE": ProcessNode(
            process_id="FILE-RECEIVE",
            name="ファイル受信処理",
            process_type=ProcessType.PRIMITIVE
        ),
        "PAYMENT-REGISTER": ProcessNode(
            process_id="PAYMENT-REGISTER", 
            name="支払い登録処理",
            process_type=ProcessType.PRIMITIVE
        )
    }
)
```

### 4.4 階層構造の可視化

上記の例における階層構造：

```
レベル0 (ROOT): INVOICE-PROCESSING-ROOT
├── レベル1 (PRIMITIVE): FILE-RECEIVE
├── レベル1 (COMPOUND): APPROVAL-PROCESS
│   ├── レベル2 (PRIMITIVE): AUTHORITY-CHECK
│   └── レベル2 (COMPOUND): APPROVAL-DECISION
│       ├── レベル3 (PRIMITIVE): AMOUNT-CHECK
│       ├── レベル3 (PRIMITIVE): APPROVER-IDENTIFY
│       └── レベル3 (COMPOUND): NOTIFICATION-PROCESS
│           ├── レベル4 (PRIMITIVE): EMAIL-SEND
│           └── レベル4 (PRIMITIVE): SYSTEM-NOTIFY
└── レベル1 (PRIMITIVE): PAYMENT-REGISTER
```

この例では、**深さ4レベル**の階層構造を実現しており：
- **再帰的参照**: 各`ProcessNode`が`ProcessFlow`を持ち、そこから更に子`ProcessNode`を参照
- **段階的詳細化**: 上位レベルほど抽象的、下位レベルほど具体的なタスク
- **型安全性**: 全ての参照が`all_processes`辞書で解決可能

## 5. 設計原則

1. **明確性**: 各フィールドの型と目的を明確に定義
2. **再帰性**: ProcessNodeが自身のProcessFlowを持つ再帰構造
3. **検証可能性**: 参照整合性の検証機能を内蔵
4. **拡張性**: 新しいフロータイプや制約を容易に追加可能
5. **可視化対応**: 階層構造の可視化データ生成をサポート

この構造により、複雑なビジネスプロセスを厳密かつ体系的に定義できます。

