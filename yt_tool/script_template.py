"""
Script Template - Extract and create video script templates
视频脚本模板提取 - 分析成功视频的脚本结构，提取可复用的模板
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


SCRIPT_TYPES = {
    "tutorial": {"name": "教程类", "structure": "问题-解决方案-步骤-总结"},
    "review": {"name": "评测类", "structure": "开箱-外观-功能-优缺点-总结"},
    "storytelling": {"name": "故事类", "structure": "引入-发展-高潮-结局"},
    "listicle": {"name": "清单类", "structure": "引入-逐条讲解-总结"},
    "vlog": {"name": "Vlog类", "structure": "开场-主线-穿插-结尾"},
    "interview": {"name": "访谈类", "structure": "介绍-问答-总结"},
    "explainer": {"name": "解说类", "structure": "背景-主题-深入-结论"},
}


class ScriptTemplate:
    """Video script template extractor and generator"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def extract_template(self, transcript: str, language: str = "中文") -> str:
        """Extract script template from video"""
        prompt = f"""分析以下视频脚本，提取可复用的模板：

{self._truncate_text(transcript)}

请提取：
## 脚本类型
[识别脚本类型]

## 整体结构
```
1. 开场 (XX秒)
   - 作用：
   - 技巧：
2. 主体
   ...
3. 结尾
   ...
```

## 可复用模板
```
[填空式模板，用___标注可替换部分]
```

## Hook技巧
## 转场技巧
## CTA设计
## 时间节奏

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是资深视频编导。", temperature=0.5)

    def generate_script(self, topic: str, script_type: str = "tutorial", duration: int = 10, language: str = "中文") -> str:
        """Generate script from template"""
        type_info = SCRIPT_TYPES.get(script_type, SCRIPT_TYPES["tutorial"])

        prompt = f"""基于模板生成视频脚本：

**主题**: {topic}
**类型**: {type_info['name']}
**结构**: {type_info['structure']}
**时长**: {duration}分钟

请生成完整脚本：

## 脚本信息
- 主题：{topic}
- 时长：{duration}分钟
- 类型：{type_info['name']}

## 完整脚本

### 开场 (0:00-0:30)
[Hook]

[自我介绍/主题引入]

### 正文
[按时间顺序的完整脚本]

### 结尾
[总结+CTA]

## 拍摄提示
## 画面建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是专业视频脚本作家。", temperature=0.7)

    def compare_structures(self, transcripts: List[str], language: str = "中文") -> str:
        """Compare script structures"""
        videos_text = "\n\n---\n\n".join([
            f"### 视频{i+1}\n{self._truncate_text(t, 5000)}"
            for i, t in enumerate(transcripts[:5])
        ])

        prompt = f"""对比分析以下视频的脚本结构：

{videos_text}

请分析：
## 结构对比表
| 视频 | 开场方式 | 主体结构 | 结尾方式 | 时长分配 |
|------|----------|----------|----------|----------|

## 共同规律
## 差异点
## 最佳实践
## 模板提炼

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是内容结构分析师。", temperature=0.5)

    def improve_script(self, script: str, focus: str = "engagement", language: str = "中文") -> str:
        """Improve existing script"""
        prompt = f"""优化以下视频脚本（重点: {focus}）：

{script}

请提供：
## 问题诊断
## 优化版本
## 修改说明
## 预期提升

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是脚本优化专家。", temperature=0.6)

    def _truncate_text(self, text: str, max_chars: int = 15000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."

    @staticmethod
    def get_script_types() -> Dict:
        return SCRIPT_TYPES
