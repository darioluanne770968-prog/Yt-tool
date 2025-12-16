"""
Podcast Dialogue Generator - 播客对话生成器
Convert single-narrator content into engaging multi-person podcast dialogues
"""

import json
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class PodcastDialogueGenerator:
    """Generate podcast-style dialogues from video content"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def create_podcast_hosts(self, topic: str, style: str = "casual", num_hosts: int = 2, language: str = "中文") -> List[Dict[str, Any]]:
        """Create podcast host personas"""
        prompt = f"""为一档关于"{topic}"的{style}风格播客创建{num_hosts}位主持人角色。

返回JSON数组，每位主持人包含：
1. name: 名字
2. role: 角色定位（如：专家、好奇的外行、幽默担当）
3. background: 背景简介
4. personality: 性格特点
5. speaking_style: 说话风格
6. catchphrases: 口头禅列表
7. expertise: 擅长领域
8. quirks: 有趣的小习惯
9. voice_description: 声音描述（用于配音参考）

确保角色之间有化学反应和互补性。语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def generate_dialogue(self, transcript: str, hosts: List[Dict] = None, style: str = "casual", language: str = "中文") -> Dict[str, Any]:
        """Generate podcast dialogue from video content"""
        if not hosts:
            hosts = [
                {"name": "主持人A", "role": "专家", "speaking_style": "专业严谨"},
                {"name": "主持人B", "role": "提问者", "speaking_style": "好奇活泼"}
            ]

        host_intro = "\n".join([f"- {h['name']}: {h.get('role', '')}, 风格: {h.get('speaking_style', '')}" for h in hosts])

        prompt = f"""将以下视频内容改编为{style}风格的播客对话。

主持人设定：
{host_intro}

原内容：
{transcript[:8000]}

要求：
1. 自然的对话流程，不是简单的问答
2. 添加主持人之间的互动（打断、补充、开玩笑）
3. 包含开场白和结尾
4. 加入过渡语和连接词
5. 保持原内容的信息量

返回JSON格式：
1. episode_title: 节目标题
2. duration_estimate: 预估时长
3. intro: 开场部分
4. segments: 对话片段数组，每个包含：
   - topic: 讨论话题
   - dialogue: 对话数组，每条包含：
     - speaker: 说话人
     - text: 内容
     - tone: 语气提示
     - action: 动作/表情（可选）
5. outro: 结尾部分
6. show_notes: 节目笔记/时间戳

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_dialogue": response}

    def generate_interview_format(self, transcript: str, guest_profile: str = None, language: str = "中文") -> Dict[str, Any]:
        """Generate interview-style podcast"""
        prompt = f"""将以下内容改编为采访形式的播客。

原内容：
{transcript[:8000]}

{f"嘉宾背景: {guest_profile}" if guest_profile else "请根据内容创建一个合适的专家嘉宾形象"}

采访格式要求：
1. 主持人提出引导性问题
2. 嘉宾深入回答并分享见解
3. 有追问和深入讨论
4. 包含个人经历或案例分享

返回JSON格式：
1. episode_info:
   - title: 标题
   - guest: 嘉宾信息
   - host: 主持人信息
2. pre_interview: 开场介绍嘉宾
3. questions: 问题数组，每个包含：
   - question: 问题
   - answer: 回答
   - follow_up: 追问（可选）
   - highlights: 亮点摘要
4. closing: 结语
5. key_takeaways: 核心要点

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_dialogue": response}

    def generate_debate_format(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Generate debate-style podcast with opposing viewpoints"""
        prompt = f"""将以下内容改编为辩论形式的播客节目。

原内容：
{transcript[:8000]}

要求：
1. 识别内容中可辩论的话题
2. 创建两个持不同观点的角色
3. 设计有来有往的辩论
4. 包含主持人调解

返回JSON格式：
1. debate_topic: 辩论主题
2. participants:
   - moderator: 主持人信息
   - pro_side: 正方信息和立场
   - con_side: 反方信息和立场
3. rounds: 辩论回合数组，每回合包含：
   - round_number: 回合数
   - focus: 焦点话题
   - exchanges: 交锋内容
4. verdict: 总结评判
5. audience_takeaway: 听众收获

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_dialogue": response}

    def generate_storytelling_podcast(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Generate narrative storytelling podcast format"""
        prompt = f"""将以下内容改编为叙事型播客（如Serial、故事FM风格）。

原内容：
{transcript[:8000]}

叙事播客特点：
1. 吸引人的开场钩子
2. 故事化的叙述结构
3. 音效和氛围描述
4. 悬念和节奏控制
5. 情感化的叙述

返回JSON格式：
1. episode_title: 标题
2. hook: 开场钩子（30秒内抓住听众）
3. narrative_structure:
   - setup: 背景设定
   - rising_action: 发展
   - climax: 高潮
   - resolution: 解决
4. narrator_script: 叙述脚本（带情感和音效标记）
5. ambient_sounds: 环境音建议
6. music_cues: 音乐提示
7. chapter_breaks: 章节断点

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_dialogue": response}

    def add_engagement_elements(self, dialogue: Dict, language: str = "中文") -> Dict[str, Any]:
        """Add engagement elements to podcast dialogue"""
        prompt = f"""为以下播客对话添加增强听众参与度的元素。

原对话：
{json.dumps(dialogue, ensure_ascii=False)[:6000]}

请添加：
1. listener_questions: 假设的听众问题
2. call_to_action: 行动号召
3. teasers: 下期预告或悬念
4. interactive_moments: 互动时刻（如"你觉得呢？"）
5. memorable_quotes: 金句标注
6. social_media_clips: 适合剪辑分享的片段
7. timestamps: 时间戳章节

返回增强后的JSON，语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return dialogue

    def export_script(self, dialogue: Dict, format: str = "script") -> str:
        """Export podcast dialogue in various formats"""
        if format == "script":
            script = f"# {dialogue.get('episode_title', '播客脚本')}\n\n"

            if "intro" in dialogue:
                script += "## 开场\n\n"
                script += f"{dialogue['intro']}\n\n"

            if "segments" in dialogue:
                for i, seg in enumerate(dialogue["segments"], 1):
                    script += f"## 第{i}部分: {seg.get('topic', '')}\n\n"
                    for line in seg.get("dialogue", []):
                        speaker = line.get("speaker", "")
                        text = line.get("text", "")
                        tone = line.get("tone", "")
                        script += f"**{speaker}**"
                        if tone:
                            script += f" _{tone}_"
                        script += f": {text}\n\n"

            if "outro" in dialogue:
                script += "## 结尾\n\n"
                script += f"{dialogue['outro']}\n\n"

            return script

        elif format == "transcript":
            # Clean transcript without formatting
            lines = []
            for seg in dialogue.get("segments", []):
                for line in seg.get("dialogue", []):
                    lines.append(f"{line.get('speaker', '')}: {line.get('text', '')}")
            return "\n".join(lines)

        elif format == "json":
            return json.dumps(dialogue, ensure_ascii=False, indent=2)

        return str(dialogue)

    def generate_show_notes(self, dialogue: Dict, language: str = "中文") -> str:
        """Generate podcast show notes"""
        prompt = f"""根据以下播客内容生成专业的节目笔记(show notes)。

内容：
{json.dumps(dialogue, ensure_ascii=False)[:6000]}

节目笔记应包含：
1. 节目简介（2-3句）
2. 时间戳章节
3. 核心要点列表
4. 提到的资源/链接（占位符）
5. 嘉宾信息（如有）
6. 相关推荐
7. 联系方式/社交媒体（占位符）

格式要求：适合发布在播客平台的Markdown格式。
语言使用{language}。"""

        return self.ai_client.chat(prompt)
