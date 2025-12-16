"""
Concept Network - 概念关联网络
Generate interactive concept relationship networks
"""

import json
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class ConceptNetwork:
    """Generate concept relationship network visualizations"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def extract_concepts_and_relations(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Extract concepts and their relationships"""
        prompt = f"""从以下内容中提取概念及其关系，用于网络图可视化。

内容：
{transcript[:8000]}

返回JSON格式：
1. concepts: 概念数组，每个包含：
   - id: 唯一标识
   - name: 概念名称
   - category: 类别（core/supporting/example/tool）
   - importance: 重要度（1-10）
   - description: 简短描述

2. relations: 关系数组，每个包含：
   - source: 源概念ID
   - target: 目标概念ID
   - type: 关系类型（is_a/part_of/uses/leads_to/contrasts/depends_on）
   - strength: 关系强度（1-10）
   - label: 关系标签

3. clusters: 概念集群

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

    def export_vis_network(self, network: Dict) -> str:
        """Export for vis.js network visualization"""
        nodes = [
            {
                "id": c["id"],
                "label": c.get("name", ""),
                "title": c.get("description", ""),
                "group": c.get("category", "default"),
                "value": c.get("importance", 5) * 10
            }
            for c in network.get("concepts", [])
        ]

        edges = [
            {
                "from": r["source"],
                "to": r["target"],
                "label": r.get("label", ""),
                "arrows": "to",
                "width": r.get("strength", 1)
            }
            for r in network.get("relations", [])
        ]

        return json.dumps({"nodes": nodes, "edges": edges}, ensure_ascii=False, indent=2)

    def export_cytoscape(self, network: Dict) -> str:
        """Export for Cytoscape.js visualization"""
        elements = []

        for c in network.get("concepts", []):
            elements.append({
                "data": {
                    "id": c["id"],
                    "label": c.get("name", ""),
                    "category": c.get("category", "default")
                }
            })

        for r in network.get("relations", []):
            elements.append({
                "data": {
                    "id": f"{r['source']}_{r['target']}",
                    "source": r["source"],
                    "target": r["target"],
                    "label": r.get("label", "")
                }
            })

        return json.dumps(elements, ensure_ascii=False, indent=2)

    def generate_interactive_html(self, network: Dict, title: str = "概念网络") -> str:
        """Generate interactive HTML visualization"""
        vis_data = self.export_vis_network(network)

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        #network {{ width: 100%; height: 600px; border: 1px solid #ccc; }}
        body {{ font-family: sans-serif; padding: 20px; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div id="network"></div>
    <script>
        var data = {vis_data};
        var container = document.getElementById('network');
        var options = {{
            nodes: {{
                shape: 'dot',
                scaling: {{ min: 10, max: 30 }},
                font: {{ size: 12 }}
            }},
            edges: {{
                font: {{ size: 10, align: 'middle' }},
                smooth: {{ type: 'continuous' }}
            }},
            physics: {{
                stabilization: {{ iterations: 100 }},
                barnesHut: {{ gravitationalConstant: -2000 }}
            }},
            groups: {{
                core: {{ color: '#e74c3c' }},
                supporting: {{ color: '#3498db' }},
                example: {{ color: '#2ecc71' }},
                tool: {{ color: '#9b59b6' }}
            }}
        }};
        var network = new vis.Network(container, data, options);
    </script>
</body>
</html>"""
        return html

    def find_central_concepts(self, network: Dict, top_n: int = 5) -> List[Dict]:
        """Find most central concepts by connection count"""
        connection_count = {}
        for r in network.get("relations", []):
            connection_count[r["source"]] = connection_count.get(r["source"], 0) + 1
            connection_count[r["target"]] = connection_count.get(r["target"], 0) + 1

        concepts = {c["id"]: c for c in network.get("concepts", [])}
        sorted_ids = sorted(connection_count.items(), key=lambda x: x[1], reverse=True)[:top_n]

        return [
            {**concepts.get(cid, {}), "connections": count}
            for cid, count in sorted_ids if cid in concepts
        ]

    def get_concept_neighborhood(self, network: Dict, concept_id: str, depth: int = 1) -> Dict[str, Any]:
        """Get neighboring concepts within specified depth"""
        concepts = {c["id"]: c for c in network.get("concepts", [])}
        relations = network.get("relations", [])

        neighbors = {concept_id}
        for _ in range(depth):
            new_neighbors = set()
            for r in relations:
                if r["source"] in neighbors:
                    new_neighbors.add(r["target"])
                if r["target"] in neighbors:
                    new_neighbors.add(r["source"])
            neighbors.update(new_neighbors)

        return {
            "concepts": [concepts[n] for n in neighbors if n in concepts],
            "relations": [r for r in relations if r["source"] in neighbors and r["target"] in neighbors]
        }

    def merge_networks(self, networks: List[Dict]) -> Dict[str, Any]:
        """Merge multiple concept networks"""
        all_concepts = {}
        all_relations = []

        for network in networks:
            for c in network.get("concepts", []):
                name = c.get("name", "")
                if name not in all_concepts:
                    all_concepts[name] = c
                else:
                    # Merge importance
                    all_concepts[name]["importance"] = max(
                        all_concepts[name].get("importance", 0),
                        c.get("importance", 0)
                    )

            all_relations.extend(network.get("relations", []))

        return {
            "concepts": list(all_concepts.values()),
            "relations": all_relations
        }
