"""
Interactive Story Generator - 互动式故事生成器
Convert educational content into choose-your-own-adventure style interactive experiences
"""

import json
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class InteractiveStoryGenerator:
    """Generate interactive learning stories from video content"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def generate_branching_story(self, transcript: str, num_branches: int = 3, language: str = "中文") -> Dict[str, Any]:
        """Generate a branching narrative story from educational content"""
        prompt = f"""将以下教育内容转换为互动分支故事。

原内容：
{transcript[:8000]}

要求：
1. 创建引人入胜的故事框架
2. 将知识点融入故事情节
3. 在关键点设置选择分支（每个决策点{num_branches}个选项）
4. 不同选择导向不同学习路径
5. 所有路径最终覆盖核心知识

返回JSON格式：
1. story_title: 故事标题
2. story_premise: 故事前提/背景设定
3. protagonist: 主角设定
4. learning_objectives: 学习目标
5. nodes: 故事节点数组，每个节点包含：
   - id: 节点ID
   - type: 类型（start/story/choice/learning/ending）
   - content: 内容文本
   - choices: 选择数组（如果是选择节点）
     - text: 选项文本
     - next_node: 跳转节点ID
     - consequence: 后果描述
     - learning_outcome: 学习效果
   - knowledge_point: 涉及的知识点（如适用）
   - next_node: 下一节点ID（非选择节点）
6. endings: 结局数组
   - id: 结局ID
   - type: 类型（best/good/neutral/bad）
   - description: 结局描述
   - knowledge_coverage: 知识覆盖度
7. story_map: 简化的故事流程图描述

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_content": response}

    def generate_scenario_simulation(self, transcript: str, scenario_type: str = "professional", language: str = "中文") -> Dict[str, Any]:
        """Generate scenario-based simulation for practical learning"""
        scenarios = {
            "professional": "职场场景模拟",
            "problem_solving": "问题解决场景",
            "social": "社交场景",
            "technical": "技术实践场景",
            "creative": "创意挑战场景"
        }

        prompt = f"""将以下内容转换为{scenarios.get(scenario_type, scenario_type)}互动模拟。

原内容：
{transcript[:8000]}

模拟要求：
1. 设计真实感的场景
2. 提供多种应对选择
3. 即时反馈每个选择的结果
4. 包含评分机制

返回JSON格式：
1. simulation_title: 模拟标题
2. scenario_setup:
   - context: 场景背景
   - your_role: 你的角色
   - objective: 目标
   - constraints: 限制条件
3. characters: NPC角色列表
4. stages: 阶段数组，每阶段包含：
   - stage_id: 阶段ID
   - situation: 情况描述
   - npc_dialogue: NPC对话
   - options: 选项数组
     - action: 行动描述
     - response: 结果反应
     - score_impact: 分数影响
     - next_stage: 下一阶段
   - hints: 提示（可选显示）
5. scoring:
   - criteria: 评分标准
   - levels: 等级划分
6. debrief: 复盘分析

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_content": response}

    def generate_quest_adventure(self, transcript: str, theme: str = "fantasy", language: str = "中文") -> Dict[str, Any]:
        """Generate RPG-style quest adventure for gamified learning"""
        prompt = f"""将以下教育内容转换为{theme}主题的冒险游戏。

原内容：
{transcript[:8000]}

游戏化要求：
1. 创建角色升级系统
2. 知识点 = 技能/能力
3. 设计任务和挑战
4. 包含收集元素
5. boss战 = 综合测试

返回JSON格式：
1. game_title: 游戏标题
2. world_setting: 世界观设定
3. player_character:
   - base_stats: 基础属性
   - skill_tree: 技能树（对应知识点）
4. main_quest: 主线任务
5. side_quests: 支线任务数组
6. levels: 关卡数组，每关包含：
   - level_id: 关卡ID
   - name: 关卡名
   - story: 剧情
   - challenges: 挑战
     - type: 类型（puzzle/combat/dialogue/collection）
     - description: 描述
     - knowledge_required: 需要的知识
     - rewards: 奖励
   - boss: boss信息（如有）
7. items: 道具系统
8. achievements: 成就列表
9. endings: 多结局

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_content": response}

    def generate_mystery_story(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Generate mystery/detective story where solving requires understanding the content"""
        prompt = f"""将以下内容转换为侦探解谜故事。

原内容：
{transcript[:8000]}

解谜故事要求：
1. 设计一个谜题/案件
2. 线索与知识点关联
3. 破案需要理解内容
4. 多个嫌疑人/可能性

返回JSON格式：
1. mystery_title: 标题
2. case_file:
   - incident: 事件描述
   - victim: 受害者/问题
   - suspects: 嫌疑人列表
   - crime_scene: 现场描述
3. investigation:
   - clues: 线索数组
     - clue_id: 线索ID
     - description: 描述
     - location: 发现位置
     - knowledge_link: 关联的知识点
   - interviews: 问询记录
   - evidence: 证据
4. deduction_stages: 推理阶段
5. solution:
   - reveal: 真相揭露
   - explanation: 解释
   - knowledge_summary: 知识总结
6. interactive_elements: 互动元素

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_content": response}

    def generate_dialogue_tree(self, transcript: str, character: str = "mentor", language: str = "中文") -> Dict[str, Any]:
        """Generate interactive dialogue tree with an AI character"""
        prompt = f"""创建一个与{character}角色的互动对话树，内容基于：

原内容：
{transcript[:6000]}

对话树要求：
1. 角色有独特个性
2. 玩家可选择问题方向
3. 深入对话解锁更多信息
4. 关系系统影响对话选项

返回JSON格式：
1. character_profile:
   - name: 名字
   - personality: 性格
   - background: 背景
   - speech_style: 说话风格
2. relationship_levels: 关系等级定义
3. dialogue_tree: 对话节点数组
   - node_id: 节点ID
   - speaker: 说话者
   - text: 内容
   - player_options: 玩家选项
     - text: 选项文本
     - next_node: 跳转节点
     - relationship_change: 关系变化
     - unlock_condition: 解锁条件（可选）
4. hidden_dialogues: 隐藏对话（高好感度解锁）
5. knowledge_revelations: 知识点揭示映射

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_content": response}

    def export_twine_format(self, story: Dict) -> str:
        """Export story in Twine-compatible format"""
        twine = f":: StoryTitle\n{story.get('story_title', 'Interactive Story')}\n\n"
        twine += ":: StoryData\n{\"ifid\": \"generated\", \"format\": \"Harlowe\", \"format-version\": \"3.3.0\"}\n\n"

        nodes = story.get("nodes", [])
        for node in nodes:
            node_id = node.get("id", "")
            content = node.get("content", "")
            twine += f":: {node_id}\n{content}\n"

            choices = node.get("choices", [])
            if choices:
                for choice in choices:
                    next_node = choice.get("next_node", "")
                    choice_text = choice.get("text", "")
                    twine += f"[[{choice_text}->>{next_node}]]\n"
            elif node.get("next_node"):
                twine += f"[[Continue->{node.get('next_node')}]]\n"

            twine += "\n"

        return twine

    def export_ink_format(self, story: Dict) -> str:
        """Export story in Ink script format (for Inkle)"""
        ink = f"// {story.get('story_title', 'Interactive Story')}\n\n"

        nodes = story.get("nodes", [])
        for node in nodes:
            node_id = node.get("id", "start")
            content = node.get("content", "")
            ink += f"=== {node_id} ===\n{content}\n"

            choices = node.get("choices", [])
            if choices:
                for choice in choices:
                    next_node = choice.get("next_node", "END")
                    choice_text = choice.get("text", "")
                    ink += f"+ [{choice_text}] -> {next_node}\n"
            elif node.get("next_node"):
                ink += f"-> {node.get('next_node')}\n"

            ink += "\n"

        ink += "=== END ===\n-> END\n"
        return ink

    def export_markdown(self, story: Dict) -> str:
        """Export story as Markdown document"""
        md = f"# {story.get('story_title', '互动故事')}\n\n"

        if "story_premise" in story:
            md += f"## 故事背景\n\n{story['story_premise']}\n\n"

        if "protagonist" in story:
            md += f"## 主角设定\n\n{story['protagonist']}\n\n"

        md += "## 故事节点\n\n"
        for node in story.get("nodes", []):
            md += f"### {node.get('id', '')}\n\n"
            md += f"{node.get('content', '')}\n\n"

            choices = node.get("choices", [])
            if choices:
                md += "**选择:**\n"
                for i, choice in enumerate(choices, 1):
                    md += f"{i}. {choice.get('text', '')} → `{choice.get('next_node', '')}`\n"
                md += "\n"

        if "endings" in story:
            md += "## 结局\n\n"
            for ending in story["endings"]:
                md += f"### {ending.get('id', '')} ({ending.get('type', '')})\n"
                md += f"{ending.get('description', '')}\n\n"

        return md
