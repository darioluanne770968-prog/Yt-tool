"""
Comic/Storyboard Generator - 漫画/分镜生成器
Convert video content into comic-style visual storyboards
"""

import json
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class ComicGenerator:
    """Generate comic-style storyboards from video content"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def generate_storyboard(self, transcript: str, num_panels: int = 8, style: str = "manga", language: str = "中文") -> Dict[str, Any]:
        """Generate a storyboard breakdown from video content"""
        style_descriptions = {
            "manga": "日式漫画风格，使用分格、速度线、表情符号",
            "comic": "美式漫画风格，鲜明色彩，动作导向",
            "minimal": "极简风格，简洁线条，重点突出",
            "infographic": "信息图风格，数据可视化，图标化",
            "sketch": "手绘草图风格，自由随意"
        }

        prompt = f"""将以下视频内容转换为{num_panels}格漫画/分镜脚本。

风格：{style_descriptions.get(style, style)}

内容：
{transcript[:8000]}

返回JSON格式：
1. title: 漫画标题
2. panels: 面板数组，每个包含：
   - panel_number: 面板编号
   - scene_description: 场景描述（用于AI图像生成）
   - dialogue: 对话/旁白
   - emotion: 情感氛围
   - visual_elements: 视觉元素列表
   - camera_angle: 视角（close-up/medium/wide/bird-eye）
   - action: 动作描述
   - sound_effects: 音效文字（如"砰！"）
   - art_direction: 美术指导说明

3. visual_style_guide:
   - color_palette: 配色建议
   - character_design: 角色设计说明
   - background_style: 背景风格

4. image_prompts: 每个面板的AI绘图提示词（英文）

语言使用{language}（image_prompts除外）。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_content": response}

    def generate_manga_format(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Generate manga-style layout with Japanese manga conventions"""
        prompt = f"""将以下内容转换为日式漫画分镜格式。

内容：
{transcript[:6000]}

按照漫画规范生成：
1. 使用从右到左的阅读顺序
2. 包含表情符号和效果线
3. 设计对话气泡类型
4. 添加漫画音效

返回JSON格式：
1. pages: 页面数组，每页包含：
   - page_number: 页码
   - layout: 版面布局描述
   - panels: 格子数组

2. characters: 角色设定
   - name: 名字
   - appearance: 外观描述
   - expressions: 常用表情

3. recurring_elements: 重复元素（背景、道具等）

4. sfx_glossary: 音效词汇表

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

    def generate_educational_comic(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Generate educational comic optimized for learning"""
        prompt = f"""将以下教育内容转换为教育漫画形式。

内容：
{transcript[:8000]}

教育漫画要求：
1. 使用角色对话解释概念
2. 用视觉比喻说明抽象内容
3. 设置学习进度点
4. 包含互动元素提示

返回JSON格式：
1. comic_title: 标题
2. learning_objectives: 学习目标
3. characters:
   - teacher_character: 讲解角色设定
   - learner_character: 学习者角色设定
   - supporting_characters: 辅助角色

4. scenes: 场景数组，每个包含：
   - concept: 涉及的概念
   - panels: 面板详情
   - key_visual: 核心视觉元素
   - analogy: 使用的类比

5. review_panel: 复习总结面板
6. quiz_elements: 可选的测验元素

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

    def generate_image_prompts(self, storyboard: Dict, style: str = "digital art") -> List[Dict[str, str]]:
        """Generate detailed prompts for AI image generation"""
        panels = storyboard.get("panels", [])
        prompts = []

        for panel in panels:
            scene = panel.get("scene_description", "")
            emotion = panel.get("emotion", "")
            camera = panel.get("camera_angle", "medium shot")
            elements = panel.get("visual_elements", [])

            base_prompt = f"{style} style, {camera}, {scene}"
            if emotion:
                base_prompt += f", {emotion} mood"
            if elements:
                base_prompt += f", featuring {', '.join(elements[:5])}"

            prompts.append({
                "panel_number": panel.get("panel_number", 0),
                "prompt": base_prompt,
                "negative_prompt": "blurry, low quality, distorted, ugly"
            })

        return prompts

    def generate_webtoon_format(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Generate vertical scrolling webtoon format"""
        prompt = f"""将以下内容转换为竖屏漫画(Webtoon)格式。

内容：
{transcript[:8000]}

Webtoon特点：
1. 垂直滚动布局
2. 每格宽度一致
3. 适合手机阅读
4. 利用滚动制造节奏

返回JSON格式：
1. episode_title: 话标题
2. panels: 面板数组（垂直排列），每个包含：
   - height_ratio: 高度比例（1-3，1为标准）
   - content: 内容描述
   - dialogue: 对话
   - scroll_effect: 滚动效果（fade/reveal/zoom等）

3. cliffhanger: 结尾悬念
4. next_episode_preview: 下话预告

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

    def generate_4koma(self, transcript: str, language: str = "中文") -> List[Dict[str, Any]]:
        """Generate 4-panel comic strips (四格漫画)"""
        prompt = f"""将以下内容转换为多个四格漫画(4コマ/四格漫画)。

内容：
{transcript[:6000]}

四格漫画结构：
1. 起（導入）
2. 承（發展）
3. 転（転折）
4. 結（結局/笑点）

返回JSON数组，每个四格包含：
- title: 小标题
- theme: 涉及的主题/知识点
- panels: 4个面板的数组
  - setup: 场景设置
  - dialogue: 对话
  - punchline: 是否是笑点/高潮

生成5-10个四格漫画，语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def export_storyboard(self, storyboard: Dict, format: str = "markdown") -> str:
        """Export storyboard in various formats"""
        if format == "markdown":
            md = f"# {storyboard.get('title', '分镜脚本')}\n\n"

            if "visual_style_guide" in storyboard:
                vsg = storyboard["visual_style_guide"]
                md += "## 视觉风格指南\n\n"
                md += f"- **配色:** {vsg.get('color_palette', 'N/A')}\n"
                md += f"- **角色设计:** {vsg.get('character_design', 'N/A')}\n\n"

            md += "## 分镜面板\n\n"
            for panel in storyboard.get("panels", []):
                md += f"### 面板 {panel.get('panel_number', '?')}\n\n"
                md += f"**场景:** {panel.get('scene_description', 'N/A')}\n\n"
                md += f"**视角:** {panel.get('camera_angle', 'N/A')}\n\n"
                md += f"**对话:** {panel.get('dialogue', 'N/A')}\n\n"
                md += f"**情感:** {panel.get('emotion', 'N/A')}\n\n"
                if panel.get('sound_effects'):
                    md += f"**音效:** {panel.get('sound_effects')}\n\n"
                md += "---\n\n"

            if "image_prompts" in storyboard:
                md += "## AI绘图提示词\n\n"
                for i, prompt in enumerate(storyboard["image_prompts"], 1):
                    md += f"**Panel {i}:** {prompt}\n\n"

            return md

        elif format == "json":
            return json.dumps(storyboard, ensure_ascii=False, indent=2)

        elif format == "fountain":
            # Screenplay format
            fountain = f"Title: {storyboard.get('title', 'Storyboard')}\n\n"
            for panel in storyboard.get("panels", []):
                fountain += f"INT. PANEL {panel.get('panel_number', '')} - {panel.get('emotion', 'DAY').upper()}\n\n"
                fountain += f"{panel.get('scene_description', '')}\n\n"
                if panel.get('dialogue'):
                    fountain += f"NARRATOR\n{panel.get('dialogue')}\n\n"
            return fountain

        return str(storyboard)

    def generate_visual_summary(self, transcript: str, num_images: int = 5, language: str = "中文") -> List[Dict[str, str]]:
        """Generate visual summary with key moments to illustrate"""
        prompt = f"""从以下视频内容中选择{num_images}个最适合可视化的关键时刻。

内容：
{transcript[:8000]}

为每个时刻提供：
1. moment: 时刻描述
2. importance: 为什么重要
3. visual_concept: 视觉概念
4. image_prompt: AI绘图提示词（英文）
5. caption: 图片说明文字

返回JSON数组，语言使用{language}（image_prompt除外）。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []
