#!/usr/bin/env python3
"""
测试新功能模块的脚本
Test script for new feature modules
"""

import sys
sys.path.insert(0, '/Users/hui/claudeProjects/Yt-tool')

# 示例视频内容（用于测试）
SAMPLE_TRANSCRIPT = """
大家好，欢迎来到今天的Python编程教程。今天我们要学习的是函数和模块。

首先，什么是函数？函数是一段可以重复使用的代码块。我们使用def关键字来定义函数。

比如说：
def greet(name):
    return f"Hello, {name}!"

这个函数接收一个参数name，然后返回一个问候语。

接下来是模块。模块就是一个Python文件，里面包含了函数、类和变量。我们可以用import来导入模块。

例如：
import math
print(math.sqrt(16))  # 输出 4.0

模块的好处是可以让代码更有组织性，而且可以在不同的项目中复用。

总结一下今天学到的：
1. 函数用def定义，可以接收参数和返回值
2. 模块是包含代码的Python文件
3. 用import导入模块

好的，今天的内容就到这里。别忘了点赞订阅，下次见！
"""

SAMPLE_TITLE = "Python入门教程：函数与模块详解"


def test_imports():
    """测试所有新模块是否可以导入"""
    print("=" * 50)
    print("测试模块导入")
    print("=" * 50)

    modules = [
        # AI 增强
        ("video_chat", "VideoChat"),
        ("ai_tutor", "AITutor"),
        ("content_rewrite", "ContentRewriter"),
        ("multimodal_analysis", "MultimodalAnalyzer"),
        # 社交分享
        ("viral_analyzer", "ViralAnalyzer"),
        ("shorts_generator", "ShortsGenerator"),
        ("thread_generator", "ThreadGenerator"),
        ("bilibili_column", "BilibiliColumnGenerator"),
        # 教育学习
        ("exam_prep", "ExamPrep"),
        ("knowledge_test", "KnowledgeTest"),
        ("lecture_notes", "LectureNotes"),
        ("language_learning", "LanguageLearning"),
        # 创作者工具
        ("competitor_analysis", "CompetitorAnalysis"),
        ("thumbnail_idea", "ThumbnailIdea"),
        ("script_template", "ScriptTemplate"),
        ("monetization_advisor", "MonetizationAdvisor"),
        # 实用工具
        ("meeting_notes", "MeetingNotes"),
        ("legal_disclaimer", "LegalDisclaimer"),
        ("plagiarism_check", "PlagiarismCheck"),
        ("auto_bookmark", "AutoBookmark"),
        # 跨平台集成
        ("obsidian_vault", "ObsidianVault"),
        ("logseq_sync", "LogseqSync"),
        ("readwise_export", "ReadwiseExport"),
        ("calendar_integration", "CalendarIntegration"),
        # 创意娱乐
        ("roast_generator", "RoastGenerator"),
        ("poetry_converter", "PoetryConverter"),
        ("game_show", "GameShow"),
        ("story_mode", "StoryMode"),
        # 数据分析
        ("watch_history_analyzer", "WatchHistoryAnalyzer"),
        ("topic_cluster", "TopicCluster"),
        ("trend_detector", "TrendDetector"),
        ("citation_generator", "CitationGenerator"),
    ]

    success = 0
    failed = 0

    for module_name, class_name in modules:
        try:
            module = __import__(f"yt_tool.{module_name}", fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✓ {module_name}.{class_name}")
            success += 1
        except Exception as e:
            print(f"✗ {module_name}.{class_name} - {e}")
            failed += 1

    print(f"\n结果: {success} 成功, {failed} 失败")
    return failed == 0


def test_video_chat():
    """测试视频对话功能（不需要API）"""
    print("\n" + "=" * 50)
    print("测试 VideoChat 类结构")
    print("=" * 50)

    from yt_tool.video_chat import VideoChat

    # 只测试类的方法是否存在，不调用API
    chat = VideoChat.__new__(VideoChat)
    chat.conversation_history = []
    chat.video_context = SAMPLE_TRANSCRIPT
    chat.video_title = SAMPLE_TITLE
    chat.metadata = {}

    methods = ['set_video_context', 'chat', 'ask_about_timestamp',
               'summarize_section', 'explain_concept', 'get_examples',
               'export_conversation', 'clear_history']

    for method in methods:
        if hasattr(chat, method):
            print(f"✓ 方法存在: {method}")
        else:
            print(f"✗ 方法缺失: {method}")

    # 测试导出功能（不需要API）
    chat.conversation_history = [
        {"role": "user", "content": "什么是函数？"},
        {"role": "assistant", "content": "函数是可重复使用的代码块。"}
    ]

    export = chat.export_conversation(format="markdown")
    print(f"\n导出测试: {'✓ 成功' if '函数' in export else '✗ 失败'}")


def test_content_rewrite_styles():
    """测试内容改写样式配置"""
    print("\n" + "=" * 50)
    print("测试 ContentRewriter 样式")
    print("=" * 50)

    from yt_tool.content_rewrite import ContentRewriter, REWRITE_STYLES

    print(f"可用样式数量: {len(REWRITE_STYLES)}")
    print("\n可用样式:")
    for key, value in REWRITE_STYLES.items():
        print(f"  - {key}: {value['name']}")


def test_shorts_generator_platforms():
    """测试短视频平台配置"""
    print("\n" + "=" * 50)
    print("测试 ShortsGenerator 平台")
    print("=" * 50)

    from yt_tool.shorts_generator import PLATFORM_SPECS

    print(f"支持的平台数量: {len(PLATFORM_SPECS)}")
    print("\n平台详情:")
    for key, value in PLATFORM_SPECS.items():
        print(f"  - {key}: {value['name']} (最长 {value['max_duration']}秒)")


def test_exam_prep_types():
    """测试考试题型配置"""
    print("\n" + "=" * 50)
    print("测试 ExamPrep 题型")
    print("=" * 50)

    from yt_tool.exam_prep import EXAM_TYPES

    print("支持的题型:")
    for key, value in EXAM_TYPES.items():
        print(f"  - {key}: {value['name']}")


def test_citation_styles():
    """测试引用格式"""
    print("\n" + "=" * 50)
    print("测试 CitationGenerator 格式")
    print("=" * 50)

    from yt_tool.citation_generator import CITATION_STYLES

    print("支持的引用格式:")
    for key, value in CITATION_STYLES.items():
        print(f"  - {key}: {value['name']}")


def demo_with_api():
    """使用API的演示（需要配置API密钥）"""
    print("\n" + "=" * 50)
    print("API 功能演示")
    print("=" * 50)

    try:
        from yt_tool.config import Config

        # 检查是否配置了API密钥
        provider = Config.get_ai_provider()
        if not provider:
            print("⚠️  未配置AI API密钥")
            print("\n请在 .env 文件中配置以下任一密钥:")
            print("  OPENAI_API_KEY=your-key")
            print("  ANTHROPIC_API_KEY=your-key")
            print("  GOOGLE_API_KEY=your-key")
            return False

        print(f"✓ 检测到 AI 提供商: {provider}")

        # 测试实际功能
        from yt_tool.video_chat import create_video_chat

        chat = create_video_chat(SAMPLE_TRANSCRIPT, SAMPLE_TITLE)
        response = chat.chat("这个视频主要讲了什么？")

        print(f"\n问: 这个视频主要讲了什么？")
        print(f"答: {response[:200]}...")

        return True

    except Exception as e:
        print(f"✗ API测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("\n🧪 YouTube AI Tool - 新功能测试\n")

    # 1. 测试模块导入
    if not test_imports():
        print("\n❌ 模块导入测试失败，请检查依赖")
        return

    # 2. 测试类结构
    test_video_chat()

    # 3. 测试配置
    test_content_rewrite_styles()
    test_shorts_generator_platforms()
    test_exam_prep_types()
    test_citation_styles()

    # 4. API演示（可选）
    print("\n" + "=" * 50)
    print("是否要测试 API 功能？(需要配置API密钥)")
    print("运行: python test_new_features.py --api")
    print("=" * 50)

    if "--api" in sys.argv:
        demo_with_api()

    print("\n✅ 测试完成！")
    print("\n📖 使用示例:")
    print("""
# 1. 视频多轮对话
from yt_tool.video_chat import create_video_chat
chat = create_video_chat(transcript, title)
response = chat.chat("解释一下视频中的概念")

# 2. 生成短视频脚本
from yt_tool.shorts_generator import ShortsGenerator
gen = ShortsGenerator()
script = gen.generate_script(transcript, platform="tiktok")

# 3. 考试备考
from yt_tool.exam_prep import ExamPrep
prep = ExamPrep()
points = prep.generate_exam_points(transcript)

# 4. Obsidian 笔记导出
from yt_tool.obsidian_vault import ObsidianVault
vault = ObsidianVault("/path/to/vault")
note = vault.generate_note(transcript, title)
""")


if __name__ == "__main__":
    main()
