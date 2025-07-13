"""Gemini Flash Task Decomposition Orchestrator System

This module implements a system that decomposes user queries into
flowchart-based tasks using Gemini Flash (dspy) and orchestrates them.
"""

import json
import os
import functools
from collections import deque
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional

import anyio
import dspy
from dotenv import load_dotenv
from dspy.primitives.assertions import assert_transform_module, backtrack_handler

# Gemini Flash 2.5 configuration
DUMMY_DIR = '/tmp/dummy_dir'
os.makedirs(DUMMY_DIR, exist_ok=True)
load_dotenv(os.path.expanduser(".env"))
gemini = dspy.LM(model="gemini/gemini-2.5-flash", temperature=0.0, max_tokens=10000)
dspy.settings.configure(lm=gemini)

# Pydantic data type definitions
PYDANTIC_SCHEMA = """
## Enum Types
class ProcessType(str, Enum):
    ROOT = "root"           # トップレベルの要望
    PRIMITIVE = "primitive" # 原子的タスク（分割不可）
    COMPOUND = "compound"   # 複合タスク（子プロセスを持つ）

class FlowType(str, Enum):
    SEQUENCE = "sequence"   # 順次実行
    BRANCH = "branch"       # 条件分岐
    LOOP = "loop"          # 繰り返し

## Dataset Type
class Dataset(BaseModel):
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

## Process Definition
class ProcessStep(BaseModel):
    process_ref: str = Field(..., description="参照プロセスID")
    input_mapping: Optional[Dict[str, str]] = Field(None, description="入力データマッピング")
    condition: Optional[str] = Field(None, description="実行条件")

class ProcessFlow(BaseModel):
    flow_type: FlowType = Field(..., description="フロー制御タイプ")
    steps: List[ProcessStep] = Field(..., description="実行ステップリスト")
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

class ProcessNode(BaseModel):
    process_id: str = Field(..., description="プロセス一意識別子")
    name: str = Field(..., description="input->outputに変換するプロセス名/目的")
    process_type: ProcessType = Field(..., description="プロセスタイプ")
    inputs: List[Dataset] = Field(default_factory=list, description="入力データセット")
    outputs: List[Dataset] = Field(default_factory=list, description="出力データセット")
    constraints: Optional[str] = Field(None, description="制約事項・要件")
    process_flow: Optional[ProcessFlow] = Field(None, description="子プロセスフロー")

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

class BusinessProcessDefinition(BaseModel):
    root_process: ProcessNode = Field(..., description="ルートプロセス")
    all_processes: Dict[str, ProcessNode] = Field(..., description="全プロセス定義辞書")
    
    def validate_references(self) -> bool:
        # 実装: すべてのprocess_refがall_processesに存在することを確認
        pass
    
    def get_process_hierarchy(self) -> Dict:
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
"""

# Task execution instructions
TASK_INSTRUCTION = """ユーザーからの指示をもとに プロパティを補完したBusinessProcessDefinitionを、mermaid記法としてsyntaxの正しさに注意してフローチャートを記述してください。
* フローチャートのノードは必ずDatasetである
* process_typeがroot,compoundの場合、ProcessNode.process_flowは必ず記述してください
* ユーザーからの指示を忠実に守り、既存のフローチャートに対してユーザーから指示されてない変更はしない
* 初期の段階ではレベル0までを一度に提示してください
    * 2回目以降により詳細化を求められた場合、追加するレベルは 既存レベル+1 までとしてください
* ProcessNode: これに所属するノードとエッジを包含するsubgraphを作成する
    * ただしProcessNode.process_type == root の場合はsubgraphを作成しないでください
* input, output: それぞれをノードとする
* process_id, process_type, constraints は描画しない
* process_flow: input -> (process_flowを展開したもの) -> output の関係性がわかるように記述
* process_flowは未定義のものを含めて良いので、ProcessNode一つだけを返すものとします
* process_id, process_type, constraints は描画しない
* コメントはレンダリング時に失敗しがちなので、コメントは含めない"""

@dataclass
class TaskResult:
    """Task processing result"""
    task_name: str
    mermaid_flowchart: str
    description: str
    subtasks: List[str]
    timestamp: str


# Validation functions for max_tokens truncation detection
def validate_mermaid_completion(mermaid_flowchart: str) -> bool:
    """Validate that mermaid flowchart is complete and not truncated"""
    if not mermaid_flowchart or len(mermaid_flowchart.strip()) == 0:
        return False
    
    # Check if mermaid code block is properly closed
    if "```mermaid" in mermaid_flowchart and not mermaid_flowchart.rstrip().endswith("```"):
        return False
    
    # Check for common truncation indicators
    truncation_indicators = [
        "...",  # Common truncation marker
        "# Error: Response truncated",
        "Response was truncated",
    ]
    
    for indicator in truncation_indicators:
        if indicator in mermaid_flowchart:
            return False
    
    return True

def validate_json_parseable(next_task_candidates: str) -> bool:
    """Validate that next task candidates can be parsed as JSON"""
    try:
        if not next_task_candidates:
            return True  # Empty is acceptable
        
        parsed = json.loads(next_task_candidates)
        return isinstance(parsed, list)  # Should be a list
    except (json.JSONDecodeError, TypeError):
        return False

def validate_response_completeness(output) -> bool:
    """Comprehensive validation of ProcessNodeDecomposer output"""
    # Basic presence checks
    if not hasattr(output, 'mermaid_flowchart') or not hasattr(output, 'next_task_candidates'):
        return False
    
    # Validate mermaid flowchart completeness
    if not validate_mermaid_completion(output.mermaid_flowchart):
        return False
    
    # Validate JSON parseability
    if not validate_json_parseable(output.next_task_candidates):
        return False
    
    # Check minimum content length (responses that are too short might be truncated)
    if len(output.mermaid_flowchart.strip()) < 20:  # Minimum reasonable mermaid content
        return False
    
    return True


class CompletionChecker(dspy.Signature):
    """タスクの完了判定"""

    conversation_history = dspy.InputField(desc="会話履歴")
    user_feedback = dspy.InputField(desc="ユーザーのフィードバック")
    is_completed = dspy.OutputField(
        desc="ユーザーはレスポンスを問題なく受け入れているか（true/false）", type=bool
    )

class ProcessNodeDecomposer(dspy.Signature):
    """プロセスノードの分解・詳細化。
    
    Pydanticデータタイプとタスク指示を分離して、
    構造化されたプロセス分解を実行します。
    """
    task_instruction: str = dspy.InputField(desc="タスク実行の指示内容")
    data_schema: str = dspy.InputField(desc="ProcessNodeのPydanticデータスキーマ定義")
    query: str = dspy.InputField(desc="ユーザーからのクエリ・要求")
    existing_mermaid_flowchart: str = dspy.InputField(desc="既存のMermaidフローチャート（オプション）", default="")
    context: str = dspy.InputField(desc="コンテキスト情報（オプション）", default="")
    query_history: str = dspy.InputField(desc="過去のクエリ履歴（JSON文字列）", default="[]")

    mermaid_flowchart: str = dspy.OutputField(
        desc="更新された正確なsyntaxのMermaidフローチャート。プロセス間の関係性とサブグラフ構造を含む。"
    )
    flowchart_update_description: str = dspy.OutputField(
        desc="フローチャートの更新内容や変更点の説明テキスト"
    )
    next_task_candidates: str = dspy.OutputField(
        desc="次に分解・分析すべきタスクの候補リスト（JSON配列形式の文字列）。例: [\"フロントエンド設計\", \"データベース設計\", \"API設計\"]"
    )

class ProcessNodeDecomposerWithAssertions(dspy.Module):
    """Enhanced ProcessNodeDecomposer with validation and retry logic"""
    
    def __init__(self):
        super().__init__()
        self.decomposer = dspy.Predict(ProcessNodeDecomposer)
    
    def forward(self, task_instruction: str, data_schema: str, query: str, 
                existing_mermaid_flowchart: str = "", context: str = "", 
                query_history: str = "[]"):
        
        result = self.decomposer(
            task_instruction=task_instruction,
            data_schema=data_schema,
            query=query,
            existing_mermaid_flowchart=existing_mermaid_flowchart,
            context=context,
            query_history=query_history
        )
        
        # Apply validation assertions
        dspy.Assert(
            validate_response_completeness(result),
            "Response appears to be truncated or incomplete. Mermaid flowchart should be properly formatted and JSON should be parseable.",
            target_module=self.decomposer
        )
        
        dspy.Assert(
            validate_mermaid_completion(result.mermaid_flowchart),
            "Mermaid flowchart appears to be truncated or improperly formatted.",
            target_module=self.decomposer
        )
        
        dspy.Assert(
            validate_json_parseable(result.next_task_candidates),
            "Next task candidates should be valid JSON array format.",
            target_module=self.decomposer
        )
        
        return result

class FlowchartUpdater(dspy.Module):
    """Enhanced Flowchart update module with validation and retry"""

    def __init__(self, max_retries: int = 2):
        super().__init__()
        # Create base decomposer with assertions
        base_decomposer = ProcessNodeDecomposerWithAssertions()
        
        # Transform with backtrack handler for retry logic
        self.decomposer = assert_transform_module(
            base_decomposer, 
            functools.partial(backtrack_handler, max_backtracks=max_retries)
        )

    def forward(self, query: str, existing_mermaid: str = "", context: str = "", query_history: list = None):
        if query_history is None:
            query_history = []

        try:
            result = self.decomposer(
                task_instruction=TASK_INSTRUCTION,
                data_schema=PYDANTIC_SCHEMA,
                query=query,
                existing_mermaid_flowchart=existing_mermaid,
                context=context,
                query_history=json.dumps(query_history, ensure_ascii=False)
            )

            return {
                "mermaid_flowchart": result.mermaid_flowchart,
                "flowchart_update_description": result.flowchart_update_description,
                "next_task_candidates": result.next_task_candidates
            }
        
        except Exception as e:
            print(f"⚠️ Flowchart update failed after retries: {str(e)}")
            # Return fallback response
            return {
                "mermaid_flowchart": f"graph TD\n    A[Error: {str(e)}]",
                "flowchart_update_description": f"エラーが発生しました: {str(e)}",
                "next_task_candidates": "[]"
            }


class TaskDivisionAgent:
    """Task Division Agent (using Gemini Flash)"""

    def __init__(self, cwd: str = None):
        self.conversation_history = []
        self.current_task = None
        self.is_completed = None
        self.cwd = Path(cwd) if cwd else Path(DUMMY_DIR)
        self.last_result = None

    async def process_task(
        self,
        raw_task: str,
        is_continuation: bool = False,
        orchestrator_state: dict = None,
    ) -> dict:
        """Process task with Gemini Flash"""
        print(f"🔍 Task processing started: is_continuation={is_continuation}")
        print(f"🔍 orchestrator_state: {orchestrator_state}")
        if orchestrator_state:
            print(f"🔍 meaningful_state: {self._has_meaningful_state(orchestrator_state)}")

        # Set task mode based on continuation flag
        if is_continuation:
            print("🔄 Continuation session")
            task = f"JSON correction feedback: {raw_task}"
        else:
            print("🆕 New or context-aware session")
            task = raw_task

        self.current_task = task

        print(f"🤖 Gemini Flash processing: {task}")
        result = await self._run_process_decomposition(task, orchestrator_state)

        subtasks = self._extract_subtasks_from_signature(result)

        task_result = {
            "original_task": task,
            "status": "completed",
            "subtasks": subtasks,
            "raw_result": result,
        }
        self.last_result = task_result

        return task_result

    async def _run_process_decomposition(self, task: str, orchestrator_state: dict = None) -> dict:
        """Run process node decomposition using Gemini Flash"""
        # Truncate long tasks for display
        task_preview = task.split('\n')[0] if '\n' in task else task
        if len(task_preview) > 100:
            task_preview = task_preview[:100] + "..."
        print(f"🤖 Process decomposition with Gemini Flash: {task_preview}")
        print("=" * 50)

        if not hasattr(self, 'flowchart_updater'):
            self.flowchart_updater = FlowchartUpdater()

        context_str = ""
        existing_mermaid = ""
        query_history = self.conversation_history

        if orchestrator_state:
            context_str = json.dumps(orchestrator_state, ensure_ascii=False, indent=2)
            if "last_mermaid" in orchestrator_state:
                existing_mermaid = orchestrator_state["last_mermaid"]

        result = self.flowchart_updater(
            query=task,
            existing_mermaid=existing_mermaid,
            context=context_str,
            query_history=query_history
        )

        mermaid_flowchart = self._extract_mermaid_content(result['mermaid_flowchart'])

        print("💬 Gemini response completed")
        print("=" * 50)
        
        return {
            "mermaid_flowchart": mermaid_flowchart,
            "flowchart_update_description": result['flowchart_update_description'],
            "next_task_candidates": result['next_task_candidates'],
        }


    def _extract_mermaid_content(self, mermaid_text: str) -> str:
        """Extract content from mermaid code block"""
        if not mermaid_text:
            return ""
        
        # Extract content if wrapped in ```mermaid blocks
        import re
        pattern = r'```mermaid\s*\n(.*?)\n```'
        match = re.search(pattern, mermaid_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        return mermaid_text.strip()

    def _extract_subtasks_from_signature(self, result: dict) -> list[str]:
        """Extract next task candidates from Signature Output"""
        try:
            next_task_candidates = result.get("next_task_candidates", "[]")
            if isinstance(next_task_candidates, str):
                subtasks = json.loads(next_task_candidates)
            else:
                subtasks = next_task_candidates
            
            print(f"📋 Subtasks extracted from Signature: {subtasks}")
            return subtasks if isinstance(subtasks, list) else []
        except json.JSONDecodeError:
            print("⚠️ Failed to parse JSON format task candidates")
            return []

    def _has_meaningful_state(self, orchestrator_state: dict) -> bool:
        """Check if orchestrator state contains meaningful information"""
        if not orchestrator_state:
            return False

        if orchestrator_state.get("subtasks_to_analyze") and len(orchestrator_state["subtasks_to_analyze"]) > 0:
            return True

        if orchestrator_state.get("analyzed_tasks") and len(orchestrator_state["analyzed_tasks"]) > 0:
            return True

        return False

    def _build_state_context(self, orchestrator_state: dict) -> str:
        """Build context information from orchestrator state"""
        context_parts = []

        if orchestrator_state.get("subtasks_to_analyze"):
            context_parts.append("## Subtasks Waiting for Analysis")
            for i, subtask in enumerate(orchestrator_state["subtasks_to_analyze"], 1):
                context_parts.append(f"{i}. {subtask}")

        if orchestrator_state.get("analyzed_tasks"):
            context_parts.append("\n## Completed Decomposed Tasks")
            for i, task in enumerate(orchestrator_state["analyzed_tasks"], 1):
                context_parts.append(f"{i}. {task}")

        if context_parts:
            return (
                "\n## Orchestrator State Information\n" + "\n".join(context_parts) + "\n"
            )
        return ""

    async def _save_task_result(self, task_name: str, agent_result: dict, should_integrate: bool = False):
        """Save task processing result and optionally integrate"""
        import datetime
        
        if not agent_result or 'raw_result' not in agent_result:
            return
            
        raw_result = agent_result['raw_result']
        
        task_result = TaskResult(
            task_name=task_name,
            mermaid_flowchart=raw_result.get('mermaid_flowchart', ''),
            description=raw_result.get('flowchart_update_description', ''),
            subtasks=agent_result.get('subtasks', []),
            timestamp=datetime.datetime.now().isoformat()
        )
        
        self.analyzed_task_results[task_name] = task_result
        print(f"💾 Saved task result for: {task_name}")
        
        # Only integrate when explicitly requested (is_completed=True)
        if should_integrate:
            integration_result = await self._integrate_new_task_incrementally(task_name, task_result)
            
            if integration_result['was_successful']:
                print(f"✅ Integration completed for: {integration_result['task_name']}")
                print(f"🔧 Changes: {integration_result['integration_changes']}")
            else:
                print(f"⚠️ Integration had issues for: {integration_result['task_name']}")
                print(f"📋 Details: {integration_result['integration_changes']}")


class Orchestrator:
    """Orchestrator: Command center for task division and agent coordination"""

    def __init__(self):
        self.user_session_id = "session_001"
        self.active_agent: TaskDivisionAgent | None = None
        self.task_queue = deque()  # Queue for next analysis candidate tasks
        self.completion_checker = dspy.Predict(CompletionChecker)
        self.global_conversation_history = []
        self.analyzed_tasks = []  # Record completed decomposed tasks

    async def process_user_input(self, user_input: str, is_auto_subtask: bool = False) -> dict:
        """Process user input uniformly"""
        print(f"🎯 User input processing started: {user_input}")

        is_initial_task = len(self.global_conversation_history) == 0

        # Skip completion_checker for automatic subtask processing to avoid infinite loops
        if is_auto_subtask:
            print("🔄 Automatic subtask processing - skipping completion_checker")
            is_completed = False
        elif not is_initial_task:
            # If user says "no problem", mechanically judge as completed
            if user_input == "問題ない":
                is_completed = True
            else:
                completion_result = self.completion_checker(
                    conversation_history="\n".join(self.global_conversation_history),
                    user_feedback=user_input,
                )
                is_completed = completion_result.is_completed.lower() == "true"
            print(f"🔍 Completion judgment result: {is_completed}")

            if is_completed:
                print("✅ Judged as task completed")

                # Perform integration for completed task
                if self.active_agent and hasattr(self.active_agent, 'current_task'):
                    current_task = self.active_agent.current_task
                    if current_task and current_task in self.analyzed_task_results:
                        task_result = self.analyzed_task_results[current_task]
                        integration_result = await self._integrate_new_task_incrementally(current_task, task_result)
                        
                        if integration_result['was_successful']:
                            print(f"✅ Integration completed for: {integration_result['task_name']}")
                            print(f"🔧 Changes: {integration_result['integration_changes']}")
                        else:
                            print(f"⚠️ Integration had issues for: {integration_result['task_name']}")
                            print(f"📋 Details: {integration_result['integration_changes']}")

                # Extract subtasks from last processing result and add to queue
                if self.active_agent and hasattr(self.active_agent, 'last_result'):
                    last_result = self.active_agent.last_result
                    if last_result and "raw_result" in last_result:
                        subtasks = self.active_agent._extract_subtasks_from_signature(last_result["raw_result"])
                        if subtasks:
                            self.add_to_queue(subtasks)
                            print(f"📋 Extracted {len(subtasks)} subtasks for analysis")

                return await self._process_next_task()
        else:
            is_completed = False

        print("🔄 Requesting agent processing")

        # Agent management based on processing context
        if is_auto_subtask:
            print("🆕 Creating new agent for automatic subtask")
            self.active_agent = TaskDivisionAgent()
            is_continuation = False
            orchestrator_state = self._build_orchestrator_state()
        elif self.active_agent is None:
            print("🆕 Creating new agent")
            self.active_agent = TaskDivisionAgent()
            is_continuation = False
            orchestrator_state = self._build_orchestrator_state()
        else:
            print("🔄 Continuing with existing agent")
            is_continuation = True
            orchestrator_state = None

        result = await self.active_agent.process_task(
            user_input,
            is_continuation=is_continuation,
            orchestrator_state=orchestrator_state,
        )

        # Skip conversation history update for automatic subtasks
        if not is_auto_subtask:
            self.global_conversation_history.append(f"User: {user_input}")
            agent_response = result.get('raw_result', {}).get('flowchart_update_description', result['status'])
            self.global_conversation_history.append(f"Agent: {agent_response}")

        return {
            "status": "agent_processing_completed",
            "message": "Agent generated response. Please review.",
            "agent_response": result,
        }

    def _build_orchestrator_state(self) -> dict:
        """Build current state of orchestrator"""
        return {
            "subtasks_to_analyze": list(self.task_queue),
            "analyzed_tasks": self.analyzed_tasks,
        }

    async def _process_next_task(self) -> dict:
        """Process next task"""
        if self.task_queue:
            next_task = self.task_queue.popleft()
            print(f"📋 Processing next task: {next_task}")

            # Record current task as completed before moving to next
            if self.active_agent and self.active_agent.current_task:
                self.analyzed_tasks.append(self.active_agent.current_task)

            # Reset agent for new task context
            self.active_agent = None
            return await self.process_user_input(next_task, is_auto_subtask=True)
        else:
            print("🎉 All tasks completed")

            if self.active_agent and self.active_agent.current_task:
                self.analyzed_tasks.append(self.active_agent.current_task)

            return {"status": "all_completed", "message": "All tasks have been completed"}

    def add_to_queue(self, tasks: list[str]):
        """Add analysis target tasks to queue"""
        for task in tasks:
            self.task_queue.append(task)
        print(f"📝 Added {tasks} to analysis queue")


def _format_response(raw_result: dict) -> str:
    """Format dictionary result for text display"""
    if not raw_result:
        return "Could not retrieve results"
    
    return f"""## Flowchart Update Results

### Update Details
{raw_result.get('flowchart_update_description', 'N/A')}

### Mermaid Flowchart
```mermaid
{raw_result.get('mermaid_flowchart', 'N/A')}
```"""


async def demo_orchestrator2():
    """Orchestrator demonstration"""
    orchestrator = Orchestrator()
    # Want to compare with and without algo_trade repository as context
    task = "Webサイトを作りたい"
    # task = "時系列に対する予測結果の非定常性にペナルティをかける報酬関数を定義したい"
    result = await orchestrator.process_user_input(task)
    agent_response = result.get('agent_response', {})
    raw_result = agent_response.get('raw_result', {})
    response_text = _format_response(raw_result)
    print(f"\n1️⃣ Agent response: {response_text}")
    print(f"\n2️⃣ Analysis queue status: {list(orchestrator.task_queue)}")

    for task in ["問題ない"] * 10:
        result = await orchestrator.process_user_input(task)
        agent_response = result.get('agent_response', {})
        raw_result = agent_response.get('raw_result', {})
        response_text = _format_response(raw_result)
        print(f"\n1️⃣ Agent response: {response_text}")
        print(f"\n2️⃣ Analysis queue status: {list(orchestrator.task_queue)}")
        
    while True:
        task = input("Enter new task: ")
        if task == "exit":
            break
        result = await orchestrator.process_user_input(task)
        agent_response = result.get('agent_response', {})
        raw_result = agent_response.get('raw_result', {})

async def demo_orchestrator3():
    """Orchestrator demonstration"""
    orchestrator = Orchestrator()
    while True:
        task = input("Enter new task: ")
        if task == "exit":
            break
        result = await orchestrator.process_user_input(task)
        agent_response = result.get('agent_response', {})
        raw_result = agent_response.get('raw_result', {})
        response_text = _format_response(raw_result)
        print(f"\n1️⃣ Agent response: {response_text}")
    print(f"\n2️⃣ Analysis queue status: {list(orchestrator.task_queue)}")

async def main():
    await demo_orchestrator2()


if __name__ == "__main__":
    anyio.run(main) 