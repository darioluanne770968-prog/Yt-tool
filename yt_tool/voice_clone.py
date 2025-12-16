"""
Voice Clone Script Generator - AI配音克隆脚本生成
Generate scripts for voice cloning in different languages while preserving style
"""

import json
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class VoiceCloneGenerator:
    """Generate voice clone scripts and dubbing content"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def analyze_voice_style(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Analyze the speaking style characteristics for voice cloning"""
        prompt = f"""分析以下视频内容的说话风格特征，用于AI配音参考。

内容：
{transcript[:6000]}

请分析并返回JSON格式：
1. **voice_characteristics**:
   - pace: 语速（slow/medium/fast）
   - tone: 语调（formal/casual/energetic/calm/authoritative）
   - pitch_variation: 音调变化程度（1-10）
   - emotion_range: 情感范围

2. **speech_patterns**:
   - sentence_structure: 句式特点
   - filler_words: 常用填充词
   - catchphrases: 口头禅
   - transition_phrases: 过渡语

3. **rhythm_markers**:
   - pause_patterns: 停顿模式
   - emphasis_words: 强调词
   - breathing_points: 换气点建议

4. **personality_traits**:
   - speaker_persona: 说话人设
   - engagement_style: 互动风格
   - humor_level: 幽默程度（1-10）

5. **technical_specs**:
   - avg_words_per_minute: 平均每分钟字数
   - sentence_length: 平均句子长度
   - complexity_level: 复杂度

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_analysis": response}

    def generate_dubbed_script(self, transcript: str, target_language: str, source_language: str = "auto", preserve_style: bool = True) -> Dict[str, Any]:
        """Generate dubbed script in target language preserving original style"""
        style_instruction = ""
        if preserve_style:
            style_instruction = """
保持原视频的说话风格：
- 保留语气和情感
- 匹配原始节奏
- 保持停顿位置
- 保留强调语气
"""

        prompt = f"""将以下视频脚本翻译并改编为{target_language}配音脚本。

原脚本：
{transcript[:8000]}

要求：
1. 翻译要自然流畅，符合目标语言习惯
2. 保持与原视频相近的时长（口型同步考虑）
3. 使用配音标记格式
{style_instruction}

返回JSON格式：
1. dubbed_script: 配音脚本（带时间标记）
2. timing_adjustments: 时长调整说明
3. pronunciation_notes: 发音注意事项
4. emotion_cues: 情感提示
5. technical_notes: 技术注意事项

脚本格式示例：
[00:00] (平静) 大家好，欢迎来到...
[00:05] (兴奋) 今天我们要讨论...
[PAUSE 2s]
[00:10] (强调) 这是非常重要的...
"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"dubbed_script": response}

    def generate_multi_voice_script(self, transcript: str, num_voices: int = 2, language: str = "中文") -> Dict[str, Any]:
        """Convert single narrator to multi-voice dialogue"""
        prompt = f"""将以下单人叙述转换为{num_voices}人对话脚本。

原内容：
{transcript[:8000]}

要求：
1. 创建{num_voices}个不同的角色声音
2. 自然分配对话
3. 每个角色有独特的说话风格
4. 保持内容完整性

返回JSON格式：
1. characters: 角色列表，每个包含：
   - name: 角色名
   - voice_type: 声音类型（如：温和男声、活泼女声）
   - personality: 性格特点
   - speaking_style: 说话风格

2. script: 对话脚本，格式：
   [角色名]: (情感) 对话内容

3. direction_notes: 导演说明

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"script": response}

    def create_tts_markup(self, transcript: str, tts_engine: str = "ssml", language: str = "中文") -> str:
        """Create TTS markup (SSML or other formats) for synthesis"""
        prompt = f"""将以下文本转换为{tts_engine.upper()}格式的语音合成标记。

原文本：
{transcript[:6000]}

要求：
1. 添加适当的停顿标记
2. 标注强调词
3. 添加语速和音调变化
4. 标记情感变化点

{"使用SSML格式，包含<speak>, <break>, <emphasis>, <prosody>等标签" if tts_engine == "ssml" else "使用适合TTS引擎的标记格式"}

语言：{language}"""

        return self.ai_client.chat(prompt)

    def generate_audiobook_script(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Convert video content to audiobook-style narration"""
        prompt = f"""将以下视频内容改编为有声书风格的叙述脚本。

原内容：
{transcript[:8000]}

要求：
1. 转换为纯音频叙述风格
2. 移除视觉引用（如"看这里"、"如图所示"）
3. 添加描述性语言补充视觉信息
4. 优化听觉体验

返回JSON格式：
1. audiobook_script: 有声书脚本
2. chapter_markers: 章节标记
3. narrator_directions: 叙述者指导
4. sound_effects_suggestions: 音效建议（可选）
5. background_music_mood: 背景音乐情绪建议

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"audiobook_script": response}

    def localize_script(self, transcript: str, target_region: str, language: str = "中文") -> Dict[str, Any]:
        """Localize script for specific region/culture"""
        prompt = f"""将以下脚本本地化为适合{target_region}地区的版本。

原脚本：
{transcript[:8000]}

本地化要求：
1. 调整文化引用和例子
2. 使用当地习惯表达
3. 替换不适用的俗语/成语
4. 调整幽默风格（如适用）
5. 考虑当地敏感话题

返回JSON格式：
1. localized_script: 本地化脚本
2. changes_made: 修改列表
3. cultural_adaptations: 文化适应说明
4. notes_for_narrator: 叙述者注意事项

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"localized_script": response}

    def generate_voice_direction(self, transcript: str, language: str = "中文") -> str:
        """Generate detailed voice direction for recording"""
        prompt = f"""为以下脚本生成详细的配音指导。

脚本：
{transcript[:6000]}

请为每个段落/句子提供：
1. 情感基调
2. 语速指示
3. 音量变化
4. 停顿位置
5. 强调词标记
6. 表演提示

格式示例：
---
[段落1]
情感：兴奋 → 平静
语速：快速开始，逐渐放慢
"大家好！" - 【高能量，上扬语调】
"今天我们来聊聊..." - 【降低能量，神秘感】
[停顿 1秒]
---

语言使用{language}。"""

        return self.ai_client.chat(prompt)

    def export_script(self, script_data: Dict, format: str = "srt") -> str:
        """Export script in various subtitle/script formats"""
        script = script_data.get("dubbed_script", "") or script_data.get("script", "")

        if format == "srt":
            # Generate SRT format
            lines = script.split('\n')
            srt_output = ""
            counter = 1
            for line in lines:
                if line.strip():
                    srt_output += f"{counter}\n"
                    srt_output += f"00:00:00,000 --> 00:00:05,000\n"  # Placeholder timing
                    srt_output += f"{line.strip()}\n\n"
                    counter += 1
            return srt_output

        elif format == "txt":
            return script

        elif format == "json":
            return json.dumps(script_data, ensure_ascii=False, indent=2)

        return script
