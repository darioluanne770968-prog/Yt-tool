"""
Memory Palace Builder - 思维宫殿/记忆宫殿构建器
Map knowledge to spatial memory using the method of loci
"""

import json
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class MemoryPalaceBuilder:
    """Build memory palaces for spatial memorization"""

    # Predefined palace templates
    PALACE_TEMPLATES = {
        "home": {
            "name": "家",
            "locations": ["门口", "客厅", "沙发", "电视", "厨房", "冰箱", "餐桌", "卧室", "床", "书桌", "浴室", "阳台"]
        },
        "school": {
            "name": "学校",
            "locations": ["校门", "操场", "教学楼", "教室", "黑板", "讲台", "图书馆", "食堂", "实验室", "体育馆", "办公室", "花园"]
        },
        "city": {
            "name": "城市",
            "locations": ["地铁站", "公园", "咖啡店", "书店", "超市", "电影院", "医院", "银行", "餐厅", "健身房", "博物馆", "广场"]
        },
        "journey": {
            "name": "旅程",
            "locations": ["出发点", "车站", "列车", "窗外风景", "隧道", "中转站", "新列车", "山区", "河流", "城市远景", "终点站", "目的地"]
        },
        "body": {
            "name": "身体",
            "locations": ["脚", "膝盖", "腿", "腰", "胃", "胸", "肩膀", "手臂", "手", "脖子", "脸", "头顶"]
        }
    }

    def __init__(self):
        self.ai_client = get_ai_client()

    def build_memory_palace(self, transcript: str, palace_type: str = "home", language: str = "中文") -> Dict[str, Any]:
        """Build a complete memory palace from video content"""
        template = self.PALACE_TEMPLATES.get(palace_type, self.PALACE_TEMPLATES["home"])

        prompt = f"""使用记忆宫殿技术，将以下内容映射到"{template['name']}"的空间记忆中。

记忆宫殿位置（按顺序）：
{', '.join(template['locations'])}

视频内容：
{transcript[:8000]}

要求：
1. 提取核心知识点
2. 为每个位置分配一个知识点
3. 创造生动、夸张、有趣的视觉联想
4. 联想要具体、奇特、有互动性

返回JSON格式：
1. palace_info:
   - name: 宫殿名称
   - theme: 整体主题
   - total_items: 总记忆项数

2. locations: 位置数组，每个包含：
   - place: 位置名称
   - knowledge_point: 知识点
   - visualization: 视觉化描述（生动、夸张、奇特）
   - mnemonic_story: 记忆故事（将知识点与位置联系）
   - sensory_details: 感官细节（视觉、听觉、触觉、嗅觉、味觉）
   - action: 发生的动作
   - emotion: 情感联系

3. journey_narrative: 从头到尾走一遍宫殿的叙述故事
4. review_cues: 复习提示
5. quick_recall_path: 快速回忆路径

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_palace": response}

    def create_custom_palace(self, locations: List[str], name: str = "自定义宫殿") -> Dict[str, Any]:
        """Create a custom memory palace with user-defined locations"""
        return {
            "name": name,
            "locations": locations,
            "total_locations": len(locations)
        }

    def generate_vivid_associations(self, knowledge_points: List[str], locations: List[str], language: str = "中文") -> List[Dict[str, Any]]:
        """Generate vivid, memorable associations for each location"""
        prompt = f"""为以下知识点和位置创建生动的记忆联想。

知识点：
{json.dumps(knowledge_points, ensure_ascii=False)}

位置：
{json.dumps(locations, ensure_ascii=False)}

记忆联想原则：
1. 夸张 - 越夸张越好记
2. 动态 - 有动作和变化
3. 奇特 - 不寻常的组合
4. 感官 - 调动多种感官
5. 情感 - 有情感共鸣
6. 互动 - 知识点与位置互动

返回JSON数组，每个联想包含：
- location: 位置
- knowledge: 知识点
- visual_scene: 视觉场景（极度生动）
- characters: 场景中的人物/角色
- action: 发生的动作
- sounds: 声音
- smells: 气味
- textures: 触感
- story_hook: 故事钩子（让人想知道接下来发生什么）
- memory_strength: 预计记忆强度（1-10）

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def generate_palace_story(self, palace: Dict, language: str = "中文") -> str:
        """Generate a narrative story walking through the palace"""
        prompt = f"""将以下记忆宫殿转化为一个引人入胜的故事叙述。

记忆宫殿：
{json.dumps(palace, ensure_ascii=False)[:6000]}

故事要求：
1. 以第一人称讲述
2. 描述走过每个位置时看到的场景
3. 强调奇特和夸张的元素
4. 自然地串联所有知识点
5. 结尾要有总结性的回顾

写一个可以朗读的完整故事，语言使用{language}。"""

        return self.ai_client.chat(prompt)

    def generate_peg_system(self, transcript: str, num_pegs: int = 20, language: str = "中文") -> Dict[str, Any]:
        """Generate a number-peg system for ordered memorization"""
        prompt = f"""使用数字挂钩法（Peg System）帮助记忆以下内容。

内容：
{transcript[:6000]}

数字挂钩法使用押韵或形状联想：
1-棍子，2-鹅，3-耳朵，4-旗子，5-钩子...

提取{num_pegs}个按重要性排序的要点，并创建挂钩联想。

返回JSON格式：
1. peg_system: 使用的挂钩系统定义
2. pegged_items: 挂钩记忆数组，每个包含：
   - number: 数字
   - peg_image: 挂钩形象
   - knowledge: 知识点
   - association: 联想场景
   - recall_cue: 回忆提示

3. review_sequence: 复习顺序建议

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_pegs": response}

    def generate_link_system(self, items: List[str], language: str = "中文") -> Dict[str, Any]:
        """Generate a link/chain memory system"""
        prompt = f"""使用链接法（Link System）将以下项目串联记忆。

项目列表：
{json.dumps(items, ensure_ascii=False)}

链接法原则：
1. 每个项目与下一个项目创建联想
2. 联想要夸张、有动作
3. 形成一个连续的故事链

返回JSON格式：
1. chain: 链接数组，每个包含：
   - item: 当前项目
   - next_item: 下一个项目
   - link_scene: 链接场景（夸张）
   - transition: 过渡描述

2. full_story: 完整的链接故事
3. recall_start: 回忆起点提示

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_links": response}

    def generate_acronym_mnemonics(self, transcript: str, language: str = "中文") -> List[Dict[str, Any]]:
        """Generate acronym-based mnemonics from content"""
        prompt = f"""从以下内容中提取适合用首字母缩略词记忆的内容。

内容：
{transcript[:6000]}

为每组相关概念创建：
1. 原始概念列表
2. 首字母缩略词
3. 记忆句子
4. 扩展故事

返回JSON数组，每个包含：
- concepts: 概念列表
- acronym: 首字母缩略词
- mnemonic_sentence: 记忆句子
- explanation: 解释
- recall_story: 回忆辅助故事

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def generate_rhyme_mnemonics(self, transcript: str, language: str = "中文") -> List[Dict[str, str]]:
        """Generate rhyme-based mnemonics"""
        prompt = f"""为以下内容创建押韵记忆口诀。

内容：
{transcript[:6000]}

要求：
1. 提取核心知识点
2. 创作押韵的记忆口诀
3. 口诀要朗朗上口
4. 内容要准确

返回JSON数组，每个包含：
- topic: 主题
- knowledge: 知识点
- rhyme: 押韵口诀
- rhythm: 节奏提示

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def export_palace(self, palace: Dict, format: str = "markdown") -> str:
        """Export memory palace in various formats"""
        if format == "markdown":
            md = f"# 🏛️ 记忆宫殿: {palace.get('palace_info', {}).get('name', '未命名')}\n\n"

            info = palace.get("palace_info", {})
            md += f"**主题:** {info.get('theme', '')}\n"
            md += f"**记忆项数:** {info.get('total_items', len(palace.get('locations', [])))}\n\n"

            md += "## 🗺️ 宫殿地图\n\n"
            for i, loc in enumerate(palace.get("locations", []), 1):
                md += f"### 📍 站点 {i}: {loc.get('place', '')}\n\n"
                md += f"**知识点:** {loc.get('knowledge_point', '')}\n\n"
                md += f"**场景:** {loc.get('visualization', '')}\n\n"
                md += f"**故事:** {loc.get('mnemonic_story', '')}\n\n"
                if loc.get('sensory_details'):
                    md += f"**感官细节:** {loc.get('sensory_details')}\n\n"
                md += "---\n\n"

            if palace.get("journey_narrative"):
                md += "## 📖 宫殿之旅\n\n"
                md += f"{palace['journey_narrative']}\n\n"

            if palace.get("quick_recall_path"):
                md += "## ⚡ 快速回忆路径\n\n"
                md += f"{palace['quick_recall_path']}\n"

            return md

        elif format == "json":
            return json.dumps(palace, ensure_ascii=False, indent=2)

        return str(palace)

    def get_available_templates(self) -> Dict[str, Dict]:
        """Get all available palace templates"""
        return self.PALACE_TEMPLATES
