"""
Workflow Automation - 工作流自动化
Create automated workflows for video processing and integration with external services
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from .ai_client import get_ai_client


class WorkflowAutomation:
    """Create and manage automated workflows"""

    def __init__(self, storage_path: str = ".workflows.json"):
        self.ai_client = get_ai_client()
        self.storage_path = storage_path
        self.data = self._load_data()
        self.triggers = {}
        self.actions = {}
        self._register_default_actions()

    def _load_data(self) -> Dict:
        """Load workflows from file"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "workflows": {},
                "execution_history": [],
                "webhooks": {}
            }

    def _save_data(self):
        """Save data"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2, default=str)

    def _register_default_actions(self):
        """Register default available actions"""
        self.actions = {
            "extract_transcript": {
                "name": "提取字幕",
                "description": "提取视频字幕文本",
                "params": ["video_url"]
            },
            "generate_summary": {
                "name": "生成摘要",
                "description": "生成视频内容摘要",
                "params": ["transcript", "style", "language"]
            },
            "generate_flashcards": {
                "name": "生成闪卡",
                "description": "从内容生成学习卡片",
                "params": ["transcript", "num_cards", "language"]
            },
            "translate": {
                "name": "翻译",
                "description": "翻译内容到目标语言",
                "params": ["text", "target_language"]
            },
            "export_markdown": {
                "name": "导出Markdown",
                "description": "导出为Markdown文件",
                "params": ["content", "filename"]
            },
            "export_json": {
                "name": "导出JSON",
                "description": "导出为JSON文件",
                "params": ["content", "filename"]
            },
            "send_notification": {
                "name": "发送通知",
                "description": "发送通知（模拟）",
                "params": ["message", "channel"]
            },
            "add_to_notion": {
                "name": "添加到Notion",
                "description": "添加内容到Notion数据库",
                "params": ["content", "database_id"]
            },
            "generate_quiz": {
                "name": "生成测验",
                "description": "从内容生成测验问题",
                "params": ["transcript", "num_questions"]
            },
            "create_study_guide": {
                "name": "创建学习指南",
                "description": "创建学习指南",
                "params": ["transcript", "language"]
            }
        }

    def create_workflow(self, name: str, description: str, trigger: Dict, actions: List[Dict]) -> Dict[str, Any]:
        """Create a new workflow"""
        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        workflow = {
            "id": workflow_id,
            "name": name,
            "description": description,
            "trigger": trigger,
            "actions": actions,
            "enabled": True,
            "created_at": datetime.now().isoformat(),
            "last_run": None,
            "run_count": 0
        }

        self.data["workflows"][workflow_id] = workflow
        self._save_data()
        return workflow

    def create_workflow_from_template(self, template_name: str, params: Dict = None) -> Dict[str, Any]:
        """Create workflow from predefined template"""
        templates = {
            "video_to_notes": {
                "name": "视频转笔记",
                "description": "自动将新视频转换为学习笔记",
                "trigger": {"type": "new_video", "condition": {}},
                "actions": [
                    {"action": "extract_transcript", "params": {}},
                    {"action": "generate_summary", "params": {"style": "detailed", "language": "中文"}},
                    {"action": "generate_flashcards", "params": {"num_cards": 10}},
                    {"action": "export_markdown", "params": {"filename": "notes_{video_id}.md"}}
                ]
            },
            "daily_digest": {
                "name": "每日摘要",
                "description": "每日汇总观看的视频",
                "trigger": {"type": "schedule", "condition": {"time": "21:00"}},
                "actions": [
                    {"action": "collect_daily_videos", "params": {}},
                    {"action": "generate_digest", "params": {}},
                    {"action": "send_notification", "params": {"channel": "email"}}
                ]
            },
            "channel_monitor": {
                "name": "频道监控",
                "description": "监控频道新视频并自动处理",
                "trigger": {"type": "channel_update", "condition": {}},
                "actions": [
                    {"action": "extract_transcript", "params": {}},
                    {"action": "generate_summary", "params": {"style": "brief"}},
                    {"action": "send_notification", "params": {"channel": "telegram"}}
                ]
            },
            "learning_workflow": {
                "name": "学习工作流",
                "description": "完整的学习处理流程",
                "trigger": {"type": "manual", "condition": {}},
                "actions": [
                    {"action": "extract_transcript", "params": {}},
                    {"action": "generate_summary", "params": {}},
                    {"action": "generate_quiz", "params": {"num_questions": 10}},
                    {"action": "create_study_guide", "params": {}},
                    {"action": "add_to_notion", "params": {}}
                ]
            }
        }

        if template_name not in templates:
            return {"error": f"Template '{template_name}' not found"}

        template = templates[template_name]
        if params:
            # Override template params
            for action in template["actions"]:
                if action["action"] in params:
                    action["params"].update(params[action["action"]])

        return self.create_workflow(
            name=template["name"],
            description=template["description"],
            trigger=template["trigger"],
            actions=template["actions"]
        )

    def execute_workflow(self, workflow_id: str, input_data: Dict = None) -> Dict[str, Any]:
        """Execute a workflow"""
        if workflow_id not in self.data["workflows"]:
            return {"error": "Workflow not found"}

        workflow = self.data["workflows"][workflow_id]

        if not workflow["enabled"]:
            return {"error": "Workflow is disabled"}

        execution = {
            "workflow_id": workflow_id,
            "started_at": datetime.now().isoformat(),
            "status": "running",
            "steps": [],
            "input": input_data
        }

        context = input_data or {}

        try:
            for i, action_config in enumerate(workflow["actions"]):
                step_result = {
                    "step": i + 1,
                    "action": action_config["action"],
                    "status": "pending"
                }

                # In a real implementation, this would execute the actual action
                # Here we simulate the execution
                step_result["status"] = "completed"
                step_result["output"] = f"Action {action_config['action']} executed with params: {action_config.get('params', {})}"

                execution["steps"].append(step_result)

            execution["status"] = "completed"
            execution["completed_at"] = datetime.now().isoformat()

        except Exception as e:
            execution["status"] = "failed"
            execution["error"] = str(e)

        # Update workflow stats
        workflow["last_run"] = datetime.now().isoformat()
        workflow["run_count"] += 1

        self.data["execution_history"].append(execution)
        self._save_data()

        return execution

    def generate_webhook_config(self, workflow_id: str, service: str = "generic") -> Dict[str, Any]:
        """Generate webhook configuration for external services"""
        if workflow_id not in self.data["workflows"]:
            return {"error": "Workflow not found"}

        webhook_id = f"wh_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        configs = {
            "generic": {
                "url": f"/api/webhooks/{webhook_id}",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "body_template": {"video_url": "{{video_url}}", "action": "process"}
            },
            "zapier": {
                "webhook_url": f"/api/webhooks/{webhook_id}",
                "trigger": "New Video URL",
                "action": "Process with AI Tool",
                "sample_data": {"video_url": "https://youtube.com/watch?v=example"}
            },
            "ifttt": {
                "service_name": "YouTube AI Tool",
                "trigger": "new_video_webhook",
                "action": "process_video",
                "ingredient": "VideoURL"
            },
            "make": {
                "module": "HTTP",
                "method": "POST",
                "url": f"/api/webhooks/{webhook_id}",
                "body_type": "json"
            }
        }

        webhook_config = {
            "webhook_id": webhook_id,
            "workflow_id": workflow_id,
            "service": service,
            "config": configs.get(service, configs["generic"]),
            "created_at": datetime.now().isoformat()
        }

        self.data["webhooks"][webhook_id] = webhook_config
        self._save_data()

        return webhook_config

    def generate_cron_schedule(self, workflow_id: str, schedule_type: str = "daily", time: str = "09:00") -> Dict[str, Any]:
        """Generate cron schedule for workflow"""
        cron_patterns = {
            "hourly": "0 * * * *",
            "daily": f"0 {time.split(':')[0]} * * *",
            "weekly": f"0 {time.split(':')[0]} * * 0",
            "monthly": f"0 {time.split(':')[0]} 1 * *"
        }

        return {
            "workflow_id": workflow_id,
            "schedule_type": schedule_type,
            "time": time,
            "cron_expression": cron_patterns.get(schedule_type, cron_patterns["daily"]),
            "next_run": "Calculated based on schedule",
            "setup_instructions": {
                "linux": f"crontab -e\n# Add: {cron_patterns.get(schedule_type)} /path/to/yt-tool workflow run {workflow_id}",
                "windows": f"Use Task Scheduler to run 'yt-tool workflow run {workflow_id}' at {time}",
                "docker": f"Use environment variable CRON_SCHEDULE={cron_patterns.get(schedule_type)}"
            }
        }

    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows"""
        return list(self.data["workflows"].values())

    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow details"""
        return self.data["workflows"].get(workflow_id, {"error": "Not found"})

    def toggle_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Enable/disable a workflow"""
        if workflow_id not in self.data["workflows"]:
            return {"error": "Workflow not found"}

        self.data["workflows"][workflow_id]["enabled"] = not self.data["workflows"][workflow_id]["enabled"]
        self._save_data()

        return {"enabled": self.data["workflows"][workflow_id]["enabled"]}

    def delete_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Delete a workflow"""
        if workflow_id not in self.data["workflows"]:
            return {"error": "Workflow not found"}

        del self.data["workflows"][workflow_id]
        self._save_data()

        return {"deleted": True}

    def get_execution_history(self, workflow_id: str = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Get workflow execution history"""
        history = self.data["execution_history"]

        if workflow_id:
            history = [h for h in history if h["workflow_id"] == workflow_id]

        return history[-limit:]

    def export_workflow(self, workflow_id: str, format: str = "json") -> str:
        """Export workflow configuration"""
        if workflow_id not in self.data["workflows"]:
            return "Workflow not found"

        workflow = self.data["workflows"][workflow_id]

        if format == "json":
            return json.dumps(workflow, ensure_ascii=False, indent=2)

        elif format == "yaml":
            # Simplified YAML output
            yaml_str = f"name: {workflow['name']}\n"
            yaml_str += f"description: {workflow['description']}\n"
            yaml_str += f"trigger:\n  type: {workflow['trigger']['type']}\n"
            yaml_str += "actions:\n"
            for action in workflow["actions"]:
                yaml_str += f"  - action: {action['action']}\n"
                if action.get("params"):
                    yaml_str += f"    params: {action['params']}\n"
            return yaml_str

        return str(workflow)

    def get_available_actions(self) -> Dict[str, Any]:
        """Get list of available actions"""
        return self.actions

    def get_available_templates(self) -> List[str]:
        """Get list of available workflow templates"""
        return ["video_to_notes", "daily_digest", "channel_monitor", "learning_workflow"]
