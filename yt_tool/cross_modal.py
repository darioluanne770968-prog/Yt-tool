"""
Cross-modal AI - Convert content between different modalities
"""

import json
from typing import List, Dict, Optional
from .ai_client import get_ai_client


class CrossModalConverter:
    """Convert video content to different modalities and formats"""

    def __init__(self):
        self.client = get_ai_client()

    def video_to_podcast_audio(self, transcript: str, title: str = "", language: str = "中文") -> dict:
        """Convert video content to podcast-ready audio script"""
        prompt = f"""将以下视频内容转换为播客音频脚本：

视频标题：{title}
视频内容：
{transcript[:6000]}

请用{language}创建：

# 播客音频脚本

## 元数据
- **播客标题**：[标题]
- **单集标题**：[单集名]
- **时长**：约[X]分钟
- **适合收听场景**：[场景]

## 开场白（30秒）
```
[音乐渐入]

主播：[开场语，问候听众，介绍本期主题]

[音乐渐弱]
```

## 主体内容

### 段落1：[主题]
```
[背景音乐轻声]

主播：[内容]

[音效提示：转场音]
```

### 段落2：[主题]
```
主播：[内容]
```

### 段落3：[主题]
```
主播：[内容]
```

[继续...]

## 总结（1分钟）
```
主播：[总结要点]
```

## 结尾（30秒）
```
主播：[感谢收听，预告下期，引导订阅]

[片尾音乐]
```

## 音频制作建议
- **背景音乐**：[建议]
- **音效使用**：[建议]
- **语速节奏**：[建议]
- **后期处理**：[建议]

## TTS标记版本
[提供带SSML标记的版本，用于TTS合成]

创建可直接使用的播客脚本。"""

        response = self.client.generate(prompt)

        return {
            "title": title,
            "podcast_script": response
        }

    def video_to_ebook(self, transcript: str, chapters: List[str] = None, language: str = "中文") -> dict:
        """Convert video series content to ebook format"""
        prompt = f"""将以下视频内容转换为电子书章节：

视频内容：
{transcript[:8000]}

请用{language}创建：

# 电子书章节

## 书籍信息
- **书名建议**：[书名]
- **副标题**：[副标题]
- **适合读者**：[描述]

---

## 前言

[根据视频内容撰写前言]

---

## 第一章：[章节标题]

### 引言
[章节引言]

### 1.1 [小节标题]
[正文内容，约500-800字]

### 1.2 [小节标题]
[正文内容]

### 1.3 [小节标题]
[正文内容]

### 本章小结
[要点总结]

### 思考题
1. [问题1]
2. [问题2]

---

## 第二章：[章节标题]

[继续...]

---

## 附录
- 术语表
- 延伸阅读
- 参考资源

---

## 排版建议
- 字体：[建议]
- 版式：[建议]
- 插图位置：[建议]

创建完整的电子书章节。"""

        response = self.client.generate(prompt)

        return {
            "ebook_content": response
        }

    def extract_text_from_screenshots(self, visual_descriptions: List[str], language: str = "中文") -> dict:
        """Simulate OCR - extract and organize text/code from described visuals"""
        descriptions_text = "\n".join([f"- {d}" for d in visual_descriptions])

        prompt = f"""基于以下视频画面描述，提取和整理其中的文字/代码内容：

画面描述：
{descriptions_text}

请用{language}整理：

# 视觉内容提取

## 1. 文字内容

### 标题/大字
[提取的标题]

### 要点文字
[提取的要点]

### 详细文字
[提取的详细内容]

## 2. 代码内容

```[语言]
[提取的代码，格式化]
```

### 代码说明
[代码的作用说明]

## 3. 图表数据

| 项目 | 数值 | 说明 |
|------|------|------|
| [项目] | [值] | [说明] |

## 4. 流程/关系图

```
[文字描述流程图结构]
```

## 5. 重要公式

$[数学公式LaTeX格式]$

说明：[公式含义]

## 6. 整理后的笔记

[将所有视觉内容整理成结构化笔记]

提取并整理所有视觉信息。"""

        response = self.client.generate(prompt)

        return {
            "extracted_content": response
        }

    def extract_chart_data(self, chart_description: str, language: str = "中文") -> dict:
        """Extract data from chart descriptions"""
        prompt = f"""基于以下图表描述，提取和重建数据：

图表描述：
{chart_description}

请用{language}提取：

# 图表数据提取

## 1. 图表类型识别
- **类型**：[柱状图/折线图/饼图/散点图等]
- **主题**：[图表主题]
- **数据来源**：[如有说明]

## 2. 提取的数据

### 原始数据表
| X轴/类别 | Y轴/数值 | 备注 |
|---------|---------|------|
| [值] | [值] | [备注] |

### 数据分析
- 最大值：[值]
- 最小值：[值]
- 平均值：[值]
- 趋势：[描述]

## 3. 数据可视化代码

### Python (Matplotlib)
```python
import matplotlib.pyplot as plt
# [绘图代码]
```

### JavaScript (ECharts)
```javascript
option = {{
    // [配置代码]
}}
```

## 4. CSV格式导出
```csv
[CSV格式数据]
```

## 5. 数据解读
[对图表数据的专业解读]

提取完整的图表数据。"""

        response = self.client.generate(prompt)

        return {
            "chart_description": chart_description,
            "extracted_data": response
        }

    def recognize_formulas(self, formula_descriptions: List[str], language: str = "中文") -> dict:
        """Recognize and convert formulas to LaTeX"""
        formulas_text = "\n".join([f"- {f}" for f in formula_descriptions])

        prompt = f"""识别并转换以下数学公式描述：

公式描述：
{formulas_text}

请用{language}提供：

# 公式识别与转换

## 识别的公式

### 公式1
**描述**：[原始描述]
**LaTeX**：$[LaTeX代码]$
**含义**：[公式含义说明]
**应用场景**：[使用场景]

### 公式2
**描述**：[原始描述]
**LaTeX**：$[LaTeX代码]$
**含义**：[公式含义说明]

[继续...]

## 公式集合

### 行内公式
$公式1$, $公式2$, ...

### 独立公式
$$
[完整公式]
$$

## 公式推导
[如果公式之间有推导关系，展示推导过程]

## 代码实现

### Python实现
```python
import numpy as np
# [公式的Python实现]
```

### LaTeX完整文档
```latex
\\documentclass{{article}}
\\usepackage{{amsmath}}
\\begin{{document}}
[公式文档]
\\end{{document}}
```

识别并转换所有数学公式。"""

        response = self.client.generate(prompt)

        return {
            "formula_conversions": response
        }

    def content_to_infographic(self, transcript: str, language: str = "中文") -> dict:
        """Convert content to infographic design spec"""
        prompt = f"""将以下内容转换为信息图设计方案：

内容：
{transcript[:5000]}

请用{language}设计：

# 信息图设计方案

## 1. 设计概述
- **主题**：[主题]
- **尺寸**：[建议尺寸]
- **风格**：[设计风格]
- **色彩方案**：[主色/辅色/强调色HEX]

## 2. 布局结构

```
┌─────────────────────────────────┐
│           标题区域              │
│         [主标题设计]            │
├─────────────────────────────────┤
│  ┌─────┐  ┌─────┐  ┌─────┐    │
│  │ 1   │  │ 2   │  │ 3   │    │
│  │要点 │  │要点 │  │要点 │    │
│  └─────┘  └─────┘  └─────┘    │
├─────────────────────────────────┤
│         [数据可视化区]          │
│              图表               │
├─────────────────────────────────┤
│           [结论/CTA]            │
└─────────────────────────────────┘
```

## 3. 内容模块

### 模块A：标题
- 主标题：[文字]
- 副标题：[文字]
- 图标建议：[描述]

### 模块B：核心要点
| 要点 | 图标 | 颜色 |
|------|------|------|
| [要点1] | [图标] | [颜色] |
| [要点2] | [图标] | [颜色] |

### 模块C：数据展示
- 图表类型：[类型]
- 数据：[数据]
- 视觉效果：[描述]

### 模块D：流程/时间线
[流程图描述]

## 4. 视觉元素

### 图标清单
- [图标1描述]
- [图标2描述]

### 插图需求
- [插图1描述]
- [插图2描述]

## 5. 文字样式

| 元素 | 字体 | 大小 | 颜色 |
|------|------|------|------|
| 主标题 | [字体] | [大小] | [颜色] |
| 正文 | [字体] | [大小] | [颜色] |

## 6. 制作建议

### Canva模板推荐
[模板类型建议]

### AI图像提示词
```
[用于生成插图的AI提示词]
```

创建完整的信息图设计方案。"""

        response = self.client.generate(prompt)

        return {
            "infographic_design": response
        }

    def text_to_video_storyboard(self, transcript: str, duration_minutes: int = 5, language: str = "中文") -> dict:
        """Convert text content to video storyboard"""
        prompt = f"""将以下文字内容转换为视频分镜脚本：

内容：
{transcript[:5000]}

目标时长：{duration_minutes}分钟

请用{language}创建：

# 视频分镜脚本

## 视频信息
- **标题**：[标题]
- **时长**：{duration_minutes}分钟
- **风格**：[风格]
- **分辨率**：1920x1080

## 分镜列表

### 场景1 (0:00-0:30)
| 镜头 | 画面描述 | 文字/旁白 | 音效 | 动效 |
|------|---------|----------|------|------|
| 1-1 | [画面] | [文字] | [音效] | [动效] |
| 1-2 | [画面] | [文字] | [音效] | [动效] |

### 场景2 (0:30-1:30)
| 镜头 | 画面描述 | 文字/旁白 | 音效 | 动效 |
|------|---------|----------|------|------|
| 2-1 | [画面] | [文字] | [音效] | [动效] |

[继续所有场景...]

## 视觉风格指南
- **色调**：[描述]
- **字体**：[推荐]
- **图形风格**：[描述]

## 素材清单

### 需要拍摄
- [场景/镜头]

### 需要设计
- [图形/动画]

### 需要采购
- [素材类型] - [来源建议]

## AI素材提示词
### 背景图
```
[Midjourney/DALL-E提示词]
```

### 人物/场景
```
[提示词]
```

## 后期制作要点
- [剪辑要点]
- [调色建议]
- [音频处理]

创建可执行的视频分镜。"""

        response = self.client.generate(prompt)

        return {
            "duration_minutes": duration_minutes,
            "storyboard": response
        }

    def generate_ar_learning_cards(self, transcript: str, num_cards: int = 5, language: str = "中文") -> dict:
        """Generate AR learning card designs"""
        prompt = f"""基于以下内容设计AR学习卡片：

内容：
{transcript[:4000]}

卡片数量：{num_cards}

请用{language}设计：

# AR学习卡片设计

## 卡片设计规范
- **尺寸**：85mm x 55mm (标准卡片)
- **AR触发**：卡片正面图案
- **内容层次**：基础→进阶→互动

## 卡片设计

### 卡片1：[主题]

**正面设计**
```
┌─────────────────┐
│  [图标/图案]    │
│                 │
│    [主标题]     │
│    [副标题]     │
│                 │
│  [AR触发标记]   │
└─────────────────┘
```
- 图案描述：[描述]
- 色彩：[配色]

**AR内容层**
1. **层1 - 基础信息**
   - 3D文字：[内容]
   - 动画：[描述]

2. **层2 - 详细解释**
   - 3D模型：[描述]
   - 语音：[文本]

3. **层3 - 互动测验**
   - 问题：[问题]
   - 选项：[选项]
   - 反馈：[反馈]

**技术规格**
- 3D模型格式：GLB/GLTF
- 动画时长：[秒]
- 交互方式：[点击/滑动等]

### 卡片2：[主题]
[同样格式...]

[继续更多卡片...]

## 开发建议

### AR平台选择
- **推荐**：[平台名]
- **原因**：[原因]

### 资源需求
- 3D建模：[数量]
- 动画制作：[数量]
- 音频录制：[数量]

### 用户体验流程
1. [步骤1]
2. [步骤2]
3. [步骤3]

设计创新的AR学习卡片。"""

        response = self.client.generate(prompt)

        return {
            "num_cards": num_cards,
            "ar_cards": response
        }

    def convert_to_interactive_presentation(self, transcript: str, language: str = "中文") -> dict:
        """Convert content to interactive presentation format"""
        prompt = f"""将内容转换为交互式演示文稿：

内容：
{transcript[:5000]}

请用{language}创建：

# 交互式演示设计

## 演示信息
- **标题**：[标题]
- **页数**：[预计页数]
- **互动元素**：[类型]
- **平台**：Reveal.js / Mentimeter / Prezi

## 页面设计

### 页面1：封面
```html
<section>
  <h1>[标题]</h1>
  <p>[副标题]</p>
  <button onclick="startPresentation()">开始</button>
</section>
```
**互动**：[点击开始]

### 页面2：目录
**内容**：[目录项]
**互动**：[点击跳转]

### 页面3：[主题]
**内容**：
- [要点1]
- [要点2]

**互动元素**：
- [ ] 投票：[问题]
- [ ] 问答：[问题]
- [ ] 动画：[描述]

[继续更多页面...]

## 互动元素库

### 投票题
1. [问题] - 选项A/B/C/D

### 词云题
1. [开放问题]

### 抢答题
1. [问题] - 答案[X]

## Reveal.js代码
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="reveal.css">
</head>
<body>
  <div class="reveal">
    <div class="slides">
      [slides内容]
    </div>
  </div>
</body>
</html>
```

## 演讲者注释
[每页的演讲者注释]

创建互动性强的演示文稿。"""

        response = self.client.generate(prompt)

        return {
            "interactive_presentation": response
        }
