"""
Logic Analyzer - Analyze logical structure, arguments, and reasoning in videos
"""

import json
from typing import List, Dict
from .ai_client import get_ai_client


class LogicAnalyzer:
    """Analyze logical structure and reasoning in content"""

    def __init__(self):
        self.client = get_ai_client()

    def analyze_argument_structure(self, transcript: str, language: str = "中文") -> dict:
        """Analyze the logical argument structure"""
        prompt = f"""分析以下内容的论证结构：

内容：
{transcript[:8000]}

请用{language}进行详细分析：

## 1. 论证结构图
- 主论点（Thesis）
- 分论点（Sub-claims）
- 支撑证据（Evidence）
- 论证关系（Connections）

## 2. 推理链条
- 前提（Premises）
- 推理过程（Reasoning Steps）
- 结论（Conclusions）

## 3. 论证类型
- 演绎论证（Deductive）
- 归纳论证（Inductive）
- 类比论证（Analogical）
- 因果论证（Causal）

## 4. 论证强度评估
- 逻辑严密性（1-10）
- 证据充分性（1-10）
- 推理有效性（1-10）

## 5. 可视化表示
用文本形式展示论证结构图：
```
主论点
├── 分论点1
│   ├── 证据A
│   └── 证据B
├── 分论点2
│   └── 证据C
└── 结论
```

提供清晰的结构分析。"""

        response = self.client.generate(prompt)

        return {
            "analysis": response,
            "content_length": len(transcript)
        }

    def extract_hidden_assumptions(self, transcript: str, language: str = "中文") -> dict:
        """Extract hidden assumptions and premises"""
        prompt = f"""识别以下内容中的隐含假设：

内容：
{transcript[:6000]}

请用{language}分析：

## 1. 隐含假设列表
列出所有未明说但论证依赖的假设：
- 假设1：[描述]
  - 类型：[价值假设/事实假设/定义假设]
  - 重要性：[关键/次要]

- 假设2：[描述]
  ...

## 2. 前提依赖
- 明确前提
- 隐含前提
- 未证明的前提

## 3. 背景假设
- 文化假设
- 知识假设
- 价值观假设

## 4. 假设验证
对每个关键假设：
- 假设是否合理？
- 有何替代假设？
- 如果假设不成立会怎样？

## 5. 批判性问题
基于假设分析提出的问题：
1. [问题1]
2. [问题2]
...

识别所有关键的隐含假设。"""

        response = self.client.generate(prompt)

        return {
            "hidden_assumptions": response
        }

    def detect_analogies(self, transcript: str, language: str = "中文") -> dict:
        """Detect and analyze analogies and metaphors"""
        prompt = f"""识别以下内容中的类比和比喻：

内容：
{transcript[:6000]}

请用{language}分析：

## 1. 类比列表
| # | 类比/比喻 | 源域 | 目标域 | 效果评估 |
|---|----------|------|--------|---------|
| 1 | [引用] | [来源概念] | [目标概念] | [有效/一般/牵强] |

## 2. 详细分析
对每个类比：
- **类比内容**：[原文引用]
- **映射关系**：源域特征 → 目标域特征
- **相似点**：[列出]
- **差异点**：[列出]
- **类比强度**：[强/中/弱]
- **潜在问题**：[如有]

## 3. 类比质量评估
- 相关性（1-10）
- 准确性（1-10）
- 说服力（1-10）

## 4. 类比的作用
- 帮助理解的方面
- 可能误导的方面

## 5. 建议的改进类比
如果原类比有问题，提供更好的替代。"""

        response = self.client.generate(prompt)

        return {
            "analogies": response
        }

    def build_causal_graph(self, transcript: str, language: str = "中文") -> dict:
        """Build a causal relationship graph"""
        prompt = f"""构建以下内容的因果关系图：

内容：
{transcript[:6000]}

请用{language}分析：

## 1. 因果关系列表
| 原因 | 结果 | 关系强度 | 证据 |
|------|------|---------|------|
| A | B | 强/中/弱 | [引用] |

## 2. 因果链条
描述复杂的因果链：
```
原因A → 中间事件B → 中间事件C → 最终结果D
         ↘ 分支E →/
```

## 3. 因果类型
- 直接因果
- 间接因果
- 充分条件
- 必要条件
- 相关但非因果

## 4. 因果论证评估
- 是否确立了因果关系？
- 有无混淆变量？
- 是否有替代解释？

## 5. Mermaid图表
```mermaid
graph TD
    A[原因1] --> B[结果1]
    A --> C[结果2]
    B --> D[最终结果]
    C --> D
```

## 6. 因果关系的可靠性
对每个因果关系评估其可靠性。"""

        response = self.client.generate(prompt)

        return {
            "causal_graph": response
        }

    def detect_fallacies(self, transcript: str, language: str = "中文") -> dict:
        """Detect logical fallacies"""
        prompt = f"""检测以下内容中的逻辑谬误：

内容：
{transcript[:6000]}

请用{language}分析：

## 1. 发现的谬误
| # | 谬误类型 | 原文引用 | 问题说明 |
|---|---------|---------|---------|
| 1 | [类型] | "[引用]" | [为什么是谬误] |

## 2. 常见谬误检查

### 形式谬误
- [ ] 肯定后件（Affirming the Consequent）
- [ ] 否定前件（Denying the Antecedent）
- [ ] 不当三段论

### 非形式谬误
- [ ] 稻草人谬误（Strawman）
- [ ] 滑坡谬误（Slippery Slope）
- [ ] 诉诸权威（Appeal to Authority）
- [ ] 诉诸情感（Appeal to Emotion）
- [ ] 人身攻击（Ad Hominem）
- [ ] 诉诸无知（Appeal to Ignorance）
- [ ] 假两难（False Dilemma）
- [ ] 循环论证（Circular Reasoning）
- [ ] 以偏概全（Hasty Generalization）
- [ ] 红鲱鱼（Red Herring）
- [ ] 错误因果（Post Hoc）

## 3. 详细分析
对每个发现的谬误：
- 谬误名称
- 原文位置
- 为何是谬误
- 如何修正

## 4. 论证质量总结
- 谬误数量
- 严重程度
- 整体可信度

## 5. 改进建议
如何改进论证以避免这些谬误。"""

        response = self.client.generate(prompt)

        return {
            "fallacies": response
        }

    def analyze_reasoning_chain(self, transcript: str, language: str = "中文") -> dict:
        """Analyze the chain of reasoning"""
        prompt = f"""分析以下内容的推理链条：

内容：
{transcript[:6000]}

请用{language}详细分析：

## 1. 推理步骤分解
步骤1：[起点/前提]
  ↓ [推理类型]
步骤2：[中间结论]
  ↓ [推理类型]
步骤3：[进一步推论]
  ↓ [推理类型]
...
最终结论：[结论]

## 2. 每步推理评估
| 步骤 | 推理类型 | 有效性 | 问题 |
|------|---------|--------|------|
| 1→2 | 演绎/归纳/类比 | ✓/✗ | [如有] |

## 3. 推理强度
- 逻辑连贯性（1-10）
- 步骤完整性（1-10）
- 结论可靠性（1-10）

## 4. 缺失的环节
- 跳跃的推理步骤
- 未充分论证的环节
- 需要补充的信息

## 5. 替代推理路径
是否有其他方式得出同样/不同结论？

## 6. 总结
推理链条的整体质量评估。"""

        response = self.client.generate(prompt)

        return {
            "reasoning_chain": response
        }

    def compare_viewpoints(self, transcript: str, language: str = "中文") -> dict:
        """Compare different viewpoints presented"""
        prompt = f"""分析以下内容中的不同观点：

内容：
{transcript[:6000]}

请用{language}分析：

## 1. 观点识别
| # | 观点 | 持有者 | 核心主张 |
|---|------|--------|---------|
| 1 | [观点名称] | [谁的观点] | [主要内容] |

## 2. 观点对比
| 方面 | 观点A | 观点B | 差异 |
|------|-------|-------|------|
| [维度1] | | | |
| [维度2] | | | |

## 3. 论证比较
每个观点的：
- 论证强度
- 证据质量
- 逻辑严密性

## 4. 共同点与分歧
- 共识领域
- 核心分歧
- 可能的调和点

## 5. 作者立场
- 作者倾向哪个观点？
- 是否公平呈现各方？

## 6. 批判性评价
对各个观点的客观评价。"""

        response = self.client.generate(prompt)

        return {
            "viewpoints_comparison": response
        }

    def generate_logic_report(self, transcript: str, language: str = "中文") -> dict:
        """Generate comprehensive logic analysis report"""
        prompt = f"""生成完整的逻辑分析报告：

内容：
{transcript[:6000]}

请用{language}生成报告：

# 逻辑分析报告

## 执行摘要
[一段话总结]

## 1. 论证结构
[主要论点和结构]

## 2. 推理质量
[推理链条评估]

## 3. 证据评估
[证据的质量和充分性]

## 4. 逻辑问题
[发现的谬误和问题]

## 5. 隐含假设
[关键假设]

## 6. 总体评分
- 逻辑严密性：X/10
- 论证有效性：X/10
- 说服力：X/10
- 总分：X/10

## 7. 建议
[改进建议]

## 8. 结论
[最终评价]"""

        response = self.client.generate(prompt)

        return {
            "report": response
        }
