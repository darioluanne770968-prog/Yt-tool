"""
3D Knowledge Map - 3D知识地图
Generate 3D visualizable knowledge structure data
"""

import json
import math
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class KnowledgeMap3D:
    """Generate 3D knowledge map visualization data"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def extract_knowledge_structure(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Extract hierarchical knowledge structure from content"""
        prompt = f"""从以下内容中提取层次化的知识结构，用于3D可视化。

内容：
{transcript[:8000]}

返回JSON格式：
1. root: 根节点（核心主题）
2. nodes: 节点数组，每个包含：
   - id: 唯一标识
   - label: 节点名称
   - level: 层级（0=根，1=一级，2=二级...）
   - parent_id: 父节点ID
   - importance: 重要度（1-10）
   - type: 类型（concept/fact/example/tool）
   - color_hint: 颜色提示

3. connections: 跨层级连接数组
   - source: 源节点ID
   - target: 目标节点ID
   - type: 连接类型（related/depends/contrast）

4. clusters: 主题集群

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw": response}

    def generate_3d_coordinates(self, structure: Dict) -> Dict[str, Any]:
        """Generate 3D coordinates for visualization"""
        nodes = structure.get("nodes", [])
        positioned_nodes = []

        # Group by level
        levels = {}
        for node in nodes:
            level = node.get("level", 0)
            if level not in levels:
                levels[level] = []
            levels[level].append(node)

        # Position nodes in 3D space
        for level, level_nodes in levels.items():
            n = len(level_nodes)
            radius = (level + 1) * 100  # Increasing radius for each level
            height = level * 50  # Increasing height

            for i, node in enumerate(level_nodes):
                angle = (2 * math.pi * i) / n if n > 0 else 0
                node["position"] = {
                    "x": round(radius * math.cos(angle), 2),
                    "y": height,
                    "z": round(radius * math.sin(angle), 2)
                }
                node["size"] = 10 + (10 - level) * 2  # Larger nodes at top
                positioned_nodes.append(node)

        structure["nodes"] = positioned_nodes
        return structure

    def export_threejs_format(self, structure: Dict) -> str:
        """Export for Three.js visualization"""
        structure = self.generate_3d_coordinates(structure)

        threejs_data = {
            "nodes": [
                {
                    "id": n["id"],
                    "label": n.get("label", ""),
                    "position": n.get("position", {"x": 0, "y": 0, "z": 0}),
                    "size": n.get("size", 10),
                    "color": self._get_color_for_type(n.get("type", "concept")),
                    "level": n.get("level", 0)
                }
                for n in structure.get("nodes", [])
            ],
            "links": [
                {
                    "source": c.get("source"),
                    "target": c.get("target"),
                    "type": c.get("type", "related")
                }
                for c in structure.get("connections", [])
            ]
        }

        return json.dumps(threejs_data, ensure_ascii=False, indent=2)

    def _get_color_for_type(self, node_type: str) -> str:
        """Get color hex for node type"""
        colors = {
            "concept": "#4CAF50",
            "fact": "#2196F3",
            "example": "#FF9800",
            "tool": "#9C27B0",
            "default": "#607D8B"
        }
        return colors.get(node_type, colors["default"])

    def export_d3_force_3d(self, structure: Dict) -> str:
        """Export for d3-force-3d visualization"""
        structure = self.generate_3d_coordinates(structure)

        d3_data = {
            "nodes": structure.get("nodes", []),
            "links": [
                {"source": c["source"], "target": c["target"], "value": 1}
                for c in structure.get("connections", [])
            ]
        }

        return json.dumps(d3_data, ensure_ascii=False, indent=2)

    def generate_visualization_html(self, structure: Dict, title: str = "知识地图") -> str:
        """Generate a complete HTML page with 3D visualization"""
        data = self.export_threejs_format(structure)

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ margin: 0; overflow: hidden; }}
        #info {{ position: absolute; top: 10px; left: 10px; color: white; font-family: sans-serif; }}
    </style>
    <script src="https://unpkg.com/3d-force-graph"></script>
</head>
<body>
    <div id="3d-graph"></div>
    <div id="info">
        <h2>{title}</h2>
        <p>拖拽旋转 | 滚轮缩放 | 点击节点查看详情</p>
    </div>
    <script>
        const data = {data};

        const Graph = ForceGraph3D()
            (document.getElementById('3d-graph'))
            .graphData(data)
            .nodeLabel('label')
            .nodeColor(node => node.color)
            .nodeVal(node => node.size)
            .linkDirectionalParticles(2)
            .linkDirectionalParticleSpeed(0.005)
            .onNodeClick(node => {{
                alert('节点: ' + node.label);
            }});
    </script>
</body>
</html>"""
        return html

    def merge_structures(self, structures: List[Dict]) -> Dict[str, Any]:
        """Merge multiple knowledge structures"""
        merged = {
            "root": "综合知识图谱",
            "nodes": [],
            "connections": []
        }

        node_offset = 0
        for structure in structures:
            for node in structure.get("nodes", []):
                new_node = node.copy()
                new_node["id"] = f"{node_offset}_{node['id']}"
                if node.get("parent_id"):
                    new_node["parent_id"] = f"{node_offset}_{node['parent_id']}"
                merged["nodes"].append(new_node)

            for conn in structure.get("connections", []):
                new_conn = conn.copy()
                new_conn["source"] = f"{node_offset}_{conn['source']}"
                new_conn["target"] = f"{node_offset}_{conn['target']}"
                merged["connections"].append(new_conn)

            node_offset += len(structure.get("nodes", []))

        return merged
