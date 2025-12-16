"""
Code extraction from programming tutorials
"""

import re
from typing import List, Dict, Optional
from .ai_client import get_ai_client


class CodeExtractor:
    """Extract code snippets from programming tutorial transcripts"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def extract_code(
        self,
        transcript: str,
        language: str = None,
        output_language: str = "中文",
    ) -> Dict:
        """
        Extract code snippets from tutorial transcript

        Args:
            transcript: Video transcript text
            language: Programming language (auto-detect if None)
            output_language: Language for comments/explanations

        Returns:
            Dictionary with extracted code and metadata
        """
        lang_hint = f"Programming language: {language}" if language else "Auto-detect the programming language"

        system_prompt = f"""You are an expert programmer. Extract code snippets from tutorial transcripts.
Provide explanations in {output_language}. Ensure code is properly formatted and runnable."""

        prompt = f"""Extract all code snippets from this programming tutorial transcript.

{lang_hint}

For each code snippet, provide:
1. The complete code (properly formatted)
2. Brief explanation of what it does
3. Any dependencies or requirements
4. Usage example if applicable

Format:

### Code Snippet 1: [Title/Purpose]

```[language]
[code here]
```

**说明:** [explanation]
**依赖:** [dependencies if any]
**用法示例:**
```[language]
[usage example]
```

---

Transcript:
{transcript[:12000]}
"""

        response = self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

        # Extract code blocks from response
        code_blocks = self._parse_code_blocks(response)

        return {
            "full_response": response,
            "code_blocks": code_blocks,
            "detected_language": language or self._detect_language(response),
        }

    def _parse_code_blocks(self, text: str) -> List[Dict]:
        """Parse code blocks from markdown text"""
        pattern = r"```(\w+)?\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)

        blocks = []
        for lang, code in matches:
            blocks.append({
                "language": lang or "text",
                "code": code.strip(),
            })

        return blocks

    def _detect_language(self, text: str) -> str:
        """Detect programming language from text"""
        indicators = {
            "python": ["def ", "import ", "print(", "class ", "__init__"],
            "javascript": ["const ", "let ", "function ", "=>", "console.log"],
            "typescript": ["interface ", ": string", ": number", "export "],
            "java": ["public class", "public static", "System.out"],
            "go": ["func ", "package ", "fmt.Println"],
            "rust": ["fn ", "let mut", "impl ", "pub fn"],
            "c++": ["#include", "std::", "cout <<", "int main"],
            "sql": ["SELECT ", "FROM ", "WHERE ", "INSERT INTO"],
        }

        text_lower = text.lower()
        for lang, keywords in indicators.items():
            if any(kw.lower() in text_lower for kw in keywords):
                return lang

        return "unknown"

    def extract_commands(
        self,
        transcript: str,
        output_language: str = "中文",
    ) -> str:
        """Extract command-line commands from transcript"""
        system_prompt = f"Extract terminal/command-line commands in {output_language}."

        prompt = f"""Extract all terminal/command-line commands mentioned in this transcript.

Format each command with:
1. The command itself
2. What it does
3. When to use it

Example format:
```bash
npm install express
```
**作用:** 安装 Express.js 框架
**使用场景:** 创建新的 Node.js web 项目时

---

Transcript:
{transcript[:10000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2048)

    def generate_project_structure(
        self,
        transcript: str,
        output_language: str = "中文",
    ) -> str:
        """Generate project structure from tutorial"""
        system_prompt = f"Generate project structures in {output_language}."

        prompt = f"""Based on this tutorial transcript, generate the recommended project structure.

Format:
```
project-name/
├── src/
│   ├── components/
│   │   └── ...
│   ├── utils/
│   │   └── ...
│   └── index.js
├── tests/
│   └── ...
├── package.json
└── README.md
```

Include explanations for each important file/folder.

Transcript:
{transcript[:10000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2048)

    def export_to_file(
        self,
        code_data: Dict,
        output_dir: str = ".",
    ) -> List[str]:
        """Export extracted code to files"""
        import os

        created_files = []

        for i, block in enumerate(code_data.get("code_blocks", []), 1):
            lang = block.get("language", "txt")
            code = block.get("code", "")

            ext_map = {
                "python": "py",
                "javascript": "js",
                "typescript": "ts",
                "java": "java",
                "go": "go",
                "rust": "rs",
                "c++": "cpp",
                "sql": "sql",
                "bash": "sh",
                "shell": "sh",
            }

            ext = ext_map.get(lang, lang)
            filename = os.path.join(output_dir, f"snippet_{i}.{ext}")

            with open(filename, "w", encoding="utf-8") as f:
                f.write(code)

            created_files.append(filename)

        return created_files
