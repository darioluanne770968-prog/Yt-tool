"""
AI Writer Suite - Generate various written content from video
"""

import json
from typing import List, Dict, Optional
from .ai_client import get_ai_client


class AIWriter:
    """AI-powered writing tools for various content types"""

    def __init__(self):
        self.client = get_ai_client()

    def generate_paper_outline(self, transcript: str, topic: str = "", paper_type: str = "research", language: str = "中文") -> dict:
        """Generate academic paper outline from video content"""
        prompt = f"""基于以下视频内容，生成学术论文大纲：

视频内容：
{transcript[:6000]}

论文主题：{topic or "基于视频内容提取"}
论文类型：{paper_type}

请用{language}生成完整的论文大纲：

# 论文大纲

## 标题建议
提供3个可选标题：
1. [标题1]
2. [标题2]
3. [标题3]

## 摘要框架
- 研究背景（1-2句）
- 研究目的（1句）
- 研究方法（1-2句）
- 主要发现（2-3句）
- 结论意义（1句）

## 正文结构

### 1. 引言
1.1 研究背景
    - 要点1
    - 要点2
1.2 研究意义
    - 理论意义
    - 实践意义
1.3 研究问题
    - 主要问题
    - 子问题
1.4 论文结构

### 2. 文献综述
2.1 [主题1]
    - 已有研究
    - 研究空白
2.2 [主题2]
    - 已有研究
    - 研究空白
2.3 理论框架

### 3. 研究方法
3.1 研究设计
3.2 数据来源
3.3 分析方法
3.4 研究限制

### 4. 结果与分析
4.1 [发现1]
4.2 [发现2]
4.3 [发现3]
4.4 综合讨论

### 5. 结论与建议
5.1 主要结论
5.2 理论贡献
5.3 实践建议
5.4 未来研究方向

## 参考文献建议
- 应查阅的领域/关键词
- 建议的经典文献
- 最新研究动向

## 写作建议
- 预计字数
- 重点章节
- 注意事项

提供可直接使用的论文大纲。"""

        response = self.client.generate(prompt)

        return {
            "topic": topic,
            "paper_type": paper_type,
            "outline": response
        }

    def generate_lesson_plan(self, transcript: str, grade_level: str = "high_school", duration_minutes: int = 45, language: str = "中文") -> dict:
        """Generate a lesson plan for teachers"""
        prompt = f"""基于以下视频内容，为教师生成教学教案：

视频内容：
{transcript[:6000]}

目标学段：{grade_level}
课时时长：{duration_minutes}分钟

请用{language}生成完整教案：

# 教学教案

## 基本信息
- **课程名称**：[名称]
- **适用年级**：{grade_level}
- **课时**：{duration_minutes}分钟
- **教学日期**：____年____月____日

## 教学目标

### 知识目标
1. [目标1]
2. [目标2]
3. [目标3]

### 能力目标
1. [目标1]
2. [目标2]

### 情感态度价值观目标
1. [目标1]
2. [目标2]

## 教学重难点

### 教学重点
- [重点1]
- [重点2]

### 教学难点
- [难点1]
- [难点2]

## 教学准备
- **教师准备**：[列表]
- **学生准备**：[列表]
- **教学资源**：[列表]

## 教学过程

### 一、导入新课（5分钟）
| 时间 | 教师活动 | 学生活动 | 设计意图 |
|------|---------|---------|---------|
| 2分钟 | [活动] | [活动] | [意图] |
| 3分钟 | [活动] | [活动] | [意图] |

### 二、新课讲授（25分钟）
| 时间 | 教师活动 | 学生活动 | 设计意图 |
|------|---------|---------|---------|
| 10分钟 | [活动] | [活动] | [意图] |
| 10分钟 | [活动] | [活动] | [意图] |
| 5分钟 | [活动] | [活动] | [意图] |

### 三、课堂练习（10分钟）
| 时间 | 教师活动 | 学生活动 | 设计意图 |
|------|---------|---------|---------|
| 10分钟 | [活动] | [活动] | [意图] |

### 四、课堂小结（5分钟）
| 时间 | 教师活动 | 学生活动 | 设计意图 |
|------|---------|---------|---------|
| 5分钟 | [活动] | [活动] | [意图] |

## 板书设计
```
[板书布局示意图]
```

## 作业布置
1. 必做题：[题目]
2. 选做题：[题目]
3. 思考题：[题目]

## 教学反思
[留空供教师课后填写]

## 附录
- 课堂练习题
- 拓展材料
- 参考答案

生成完整可用的教学教案。"""

        response = self.client.generate(prompt)

        return {
            "grade_level": grade_level,
            "duration": duration_minutes,
            "lesson_plan": response
        }

    def generate_book_review(self, transcript: str, style: str = "academic", language: str = "中文") -> dict:
        """Generate book/video review"""
        style_desc = {
            "academic": "学术评论风格，注重分析和批评",
            "casual": "轻松的个人观感风格",
            "professional": "专业媒体评论风格",
            "blog": "博客文章风格"
        }

        prompt = f"""基于以下视频内容，撰写评论文章：

内容：
{transcript[:6000]}

风格要求：{style_desc.get(style, style_desc["academic"])}

请用{language}撰写：

# 评论文章

## 标题
[吸引人的标题]

## 副标题
[补充说明]

---

## 开篇引入
[2-3段引人入胜的开场]

## 内容概述
[客观描述主要内容]

## 深度分析
### 优点分析
- [优点1详述]
- [优点2详述]
- [优点3详述]

### 不足之处
- [不足1详述]
- [不足2详述]

### 独特见解
[你的独特观点和分析]

## 与同类作品比较
[与其他相关作品的对比]

## 目标受众分析
[适合什么样的观众/读者]

## 总体评价
### 评分
- 内容深度：⭐⭐⭐⭐☆ (4/5)
- 表达清晰：⭐⭐⭐⭐⭐ (5/5)
- 实用价值：⭐⭐⭐⭐☆ (4/5)
- 总体推荐：⭐⭐⭐⭐☆ (4/5)

### 一句话评价
[精炼的总结评语]

## 结语
[总结性的结尾，可包含推荐语]

---

*作者：AI评论员*
*日期：[日期]*

撰写专业的评论文章。"""

        response = self.client.generate(prompt)

        return {
            "style": style,
            "review": response
        }

    def generate_novel_chapter(self, transcript: str, genre: str = "educational", language: str = "中文") -> dict:
        """Expand video content into a novel chapter"""
        prompt = f"""将以下视频内容扩展为小说章节：

视频内容：
{transcript[:5000]}

小说类型：{genre}

请用{language}创作：

# 小说章节

## 章节标题
第X章：[标题]

---

[以小说的叙事手法重新讲述视频内容]

包含：
1. 场景描写和氛围营造
2. 人物刻画（可以是讲述者、学习者等角色）
3. 对话设计
4. 内心独白
5. 情节发展
6. 知识点的自然融入
7. 引人入胜的结尾

字数：约2000-3000字

风格要求：
- 引人入胜
- 知识与故事完美结合
- 有画面感
- 适合阅读

创作一个精彩的小说章节。"""

        response = self.client.generate(prompt)

        return {
            "genre": genre,
            "chapter": response
        }

    def generate_poetry(self, transcript: str, poetry_type: str = "free_verse", language: str = "中文") -> dict:
        """Generate poetry inspired by video content"""
        prompt = f"""从以下视频内容中提取灵感，创作诗歌：

内容：
{transcript[:4000]}

诗歌类型：{poetry_type}

请用{language}创作：

# 诗歌创作

## 诗歌一：[标题]
类型：[类型]

[诗歌内容]

---

## 诗歌二：[标题]
类型：[类型]

[诗歌内容]

---

## 诗歌三：[标题]
类型：[类型]

[诗歌内容]

---

## 创作说明
- 灵感来源
- 表达的主题
- 使用的意象

创作富有意境的诗歌。"""

        response = self.client.generate(prompt)

        return {
            "poetry_type": poetry_type,
            "poems": response
        }

    def generate_ad_copy(self, transcript: str, product_type: str = "", platform: str = "general", language: str = "中文") -> dict:
        """Generate advertising copy from video content"""
        prompt = f"""基于以下视频内容，生成广告文案：

内容：
{transcript[:4000]}

产品/服务类型：{product_type or "根据内容推断"}
投放平台：{platform}

请用{language}生成多个版本的广告文案：

# 广告文案

## 版本A：情感诉求型
### 标题
[标题]

### 正文
[正文内容]

### 行动号召（CTA）
[CTA]

---

## 版本B：理性诉求型
### 标题
[标题]

### 正文
[正文内容]

### 行动号召（CTA）
[CTA]

---

## 版本C：故事型
### 标题
[标题]

### 正文
[正文内容]

### 行动号召（CTA）
[CTA]

---

## 短视频脚本（15秒）
[脚本内容]

## 社交媒体文案
### 微博版（140字内）
[内容]

### 朋友圈版
[内容]

### 小红书版
[内容]

## 标题选项（A/B测试）
1. [标题1]
2. [标题2]
3. [标题3]
4. [标题4]
5. [标题5]

## 关键词建议
[关键词列表]

生成高转化率的广告文案。"""

        response = self.client.generate(prompt)

        return {
            "product_type": product_type,
            "platform": platform,
            "ad_copy": response
        }

    def generate_seo_article(self, transcript: str, target_keywords: List[str] = None, word_count: int = 2000, language: str = "中文") -> dict:
        """Generate SEO-optimized article"""
        keywords_text = ", ".join(target_keywords) if target_keywords else "根据内容自动提取"

        prompt = f"""基于以下视频内容，撰写SEO优化的长文章：

内容：
{transcript[:6000]}

目标关键词：{keywords_text}
目标字数：{word_count}字

请用{language}撰写：

# SEO优化文章

## SEO元数据
- **Title标签**（50-60字符）：[标题]
- **Meta描述**（150-160字符）：[描述]
- **URL建议**：[url-slug]
- **目标关键词**：[关键词列表]
- **长尾关键词**：[长尾词列表]

---

## 文章正文

### [H1标题 - 包含主关键词]

[引言段落 - 自然包含关键词]

### [H2标题1]
[内容段落...]

#### [H3子标题]
[详细内容...]

### [H2标题2]
[内容段落...]

[继续...]

### 总结
[包含关键词的总结]

### 常见问题（FAQ）
**Q1: [问题]?**
A: [回答]

**Q2: [问题]?**
A: [回答]

**Q3: [问题]?**
A: [回答]

---

## SEO检查清单
- [ ] 标题包含主关键词
- [ ] 关键词密度适中（1-2%）
- [ ] 自然的内部链接机会
- [ ] 图片ALT标签建议
- [ ] 适当的H标签层级
- [ ] 可读性评分：[分数]

## 内容优化建议
[具体的优化建议]

生成高质量的SEO文章。"""

        response = self.client.generate(prompt)

        return {
            "target_keywords": target_keywords,
            "word_count": word_count,
            "article": response
        }

    def generate_script(self, transcript: str, format_type: str = "screenplay", language: str = "中文") -> dict:
        """Generate script in various formats"""
        prompt = f"""将以下内容改编为{format_type}格式的剧本：

原始内容：
{transcript[:5000]}

请用{language}创作：

# {format_type.upper()} 剧本

## 基本信息
- 标题：[标题]
- 类型：[类型]
- 时长：约[X]分钟

## 角色表
| 角色 | 描述 |
|------|------|
| [角色1] | [描述] |
| [角色2] | [描述] |

## 剧本正文

### 场景一
[场景描述]

**角色名**
（动作指示）台词内容。

[继续剧本内容...]

## 制作建议
- 场景需求
- 道具清单
- 特殊效果

创作完整的剧本。"""

        response = self.client.generate(prompt)

        return {
            "format_type": format_type,
            "script": response
        }
