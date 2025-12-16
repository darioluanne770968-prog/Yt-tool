"""
Knowledge Graph Builder - 知识图谱构建
Extract entities and relationships from videos to build visual knowledge graphs
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from .ai_client import get_ai_client


class KnowledgeGraphBuilder:
    """Build knowledge graphs from video content"""

    def __init__(self):
        self.ai_client = get_ai_client()
        self.nodes = []
        self.edges = []

    def extract_entities(self, transcript: str, language: str = "中文") -> List[Dict[str, Any]]:
        """Extract entities (concepts, people, tools, etc.) from transcript"""
        prompt = f"""从以下视频内容中提取所有重要实体。

内容：
{transcript[:8000]}

请提取以下类型的实体，返回JSON数组格式：
1. concepts: 概念/理论
2. people: 人物/专家
3. organizations: 组织/公司
4. tools: 工具/软件/技术
5. events: 事件/里程碑
6. locations: 地点
7. terms: 专业术语
8. examples: 具体案例

每个实体包含：
- id: 唯一标识（如 "concept_1"）
- name: 实体名称
- type: 实体类型
- description: 简短描述
- importance: 重要程度（1-10）
- first_mention: 首次提及的上下文

返回JSON数组，语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                entities = json.loads(response[json_start:json_end])
                self.nodes = entities
                return entities
        except json.JSONDecodeError:
            pass

        return []

    def extract_relationships(self, transcript: str, entities: List[Dict] = None, language: str = "中文") -> List[Dict[str, Any]]:
        """Extract relationships between entities"""
        if entities is None:
            entities = self.nodes

        entity_names = [e.get("name", "") for e in entities[:30]]  # Limit for prompt size

        prompt = f"""基于以下实体列表和视频内容，提取实体之间的关系。

实体列表：
{json.dumps(entity_names, ensure_ascii=False)}

视频内容：
{transcript[:6000]}

请识别实体之间的关系，返回JSON数组格式：
每个关系包含：
- source: 源实体名称
- target: 目标实体名称
- relationship: 关系类型（如：包含、依赖、创建、使用、对比、演变为、属于等）
- description: 关系描述
- strength: 关系强度（1-10）
- bidirectional: 是否双向关系

常见关系类型：
- is_a: 是一种
- part_of: 是...的一部分
- uses: 使用
- created_by: 由...创建
- depends_on: 依赖于
- related_to: 相关于
- leads_to: 导致
- contrasts_with: 与...对比
- evolved_from: 从...演变
- example_of: 是...的例子

返回JSON数组，语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                relationships = json.loads(response[json_start:json_end])
                self.edges = relationships
                return relationships
        except json.JSONDecodeError:
            pass

        return []

    def build_graph(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Build complete knowledge graph from transcript"""
        entities = self.extract_entities(transcript, language)
        relationships = self.extract_relationships(transcript, entities, language)

        return {
            "nodes": entities,
            "edges": relationships,
            "metadata": {
                "node_count": len(entities),
                "edge_count": len(relationships),
                "language": language
            }
        }

    def merge_graphs(self, graphs: List[Dict], language: str = "中文") -> Dict[str, Any]:
        """Merge multiple knowledge graphs into one"""
        all_nodes = {}
        all_edges = []

        for graph in graphs:
            for node in graph.get("nodes", []):
                name = node.get("name", "")
                if name not in all_nodes:
                    all_nodes[name] = node
                else:
                    # Merge importance scores
                    existing = all_nodes[name]
                    existing["importance"] = max(
                        existing.get("importance", 0),
                        node.get("importance", 0)
                    )

            all_edges.extend(graph.get("edges", []))

        # Deduplicate edges
        unique_edges = []
        seen = set()
        for edge in all_edges:
            key = (edge.get("source"), edge.get("target"), edge.get("relationship"))
            if key not in seen:
                seen.add(key)
                unique_edges.append(edge)

        return {
            "nodes": list(all_nodes.values()),
            "edges": unique_edges,
            "metadata": {
                "node_count": len(all_nodes),
                "edge_count": len(unique_edges),
                "merged_from": len(graphs)
            }
        }

    def find_central_concepts(self, graph: Dict = None, top_n: int = 10) -> List[Dict]:
        """Find the most central/important concepts in the graph"""
        if graph is None:
            graph = {"nodes": self.nodes, "edges": self.edges}

        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])

        # Calculate degree centrality
        degree_count = {}
        for node in nodes:
            name = node.get("name", "")
            degree_count[name] = 0

        for edge in edges:
            source = edge.get("source", "")
            target = edge.get("target", "")
            if source in degree_count:
                degree_count[source] += 1
            if target in degree_count:
                degree_count[target] += 1

        # Sort by centrality
        sorted_nodes = sorted(
            nodes,
            key=lambda n: (degree_count.get(n.get("name", ""), 0), n.get("importance", 0)),
            reverse=True
        )

        return sorted_nodes[:top_n]

    def get_subgraph(self, center_node: str, depth: int = 2, graph: Dict = None) -> Dict[str, Any]:
        """Get a subgraph centered on a specific node"""
        if graph is None:
            graph = {"nodes": self.nodes, "edges": self.edges}

        edges = graph.get("edges", [])
        nodes = {n.get("name"): n for n in graph.get("nodes", [])}

        # BFS to find connected nodes
        visited = {center_node}
        current_level = {center_node}

        for _ in range(depth):
            next_level = set()
            for edge in edges:
                source = edge.get("source", "")
                target = edge.get("target", "")
                if source in current_level and target not in visited:
                    next_level.add(target)
                    visited.add(target)
                if target in current_level and source not in visited:
                    next_level.add(source)
                    visited.add(source)
            current_level = next_level

        # Filter nodes and edges
        sub_nodes = [nodes[name] for name in visited if name in nodes]
        sub_edges = [
            edge for edge in edges
            if edge.get("source") in visited and edge.get("target") in visited
        ]

        return {
            "nodes": sub_nodes,
            "edges": sub_edges,
            "center": center_node,
            "depth": depth
        }

    def export_mermaid(self, graph: Dict = None) -> str:
        """Export knowledge graph as Mermaid diagram"""
        if graph is None:
            graph = {"nodes": self.nodes, "edges": self.edges}

        mermaid = "graph TD\n"

        # Add nodes
        for node in graph.get("nodes", []):
            node_id = node.get("id", node.get("name", "").replace(" ", "_"))
            name = node.get("name", "")
            node_type = node.get("type", "")
            mermaid += f"    {node_id}[{name}]\n"

        mermaid += "\n"

        # Add edges
        for edge in graph.get("edges", []):
            source = edge.get("source", "").replace(" ", "_")
            target = edge.get("target", "").replace(" ", "_")
            rel = edge.get("relationship", "")
            mermaid += f"    {source} -->|{rel}| {target}\n"

        return mermaid

    def export_d3_json(self, graph: Dict = None) -> str:
        """Export knowledge graph as D3.js compatible JSON"""
        if graph is None:
            graph = {"nodes": self.nodes, "edges": self.edges}

        d3_data = {
            "nodes": [
                {
                    "id": node.get("name", ""),
                    "group": node.get("type", "default"),
                    "importance": node.get("importance", 5)
                }
                for node in graph.get("nodes", [])
            ],
            "links": [
                {
                    "source": edge.get("source", ""),
                    "target": edge.get("target", ""),
                    "value": edge.get("strength", 5),
                    "label": edge.get("relationship", "")
                }
                for edge in graph.get("edges", [])
            ]
        }

        return json.dumps(d3_data, ensure_ascii=False, indent=2)

    def export_cytoscape(self, graph: Dict = None) -> str:
        """Export knowledge graph as Cytoscape.js compatible JSON"""
        if graph is None:
            graph = {"nodes": self.nodes, "edges": self.edges}

        elements = []

        for node in graph.get("nodes", []):
            elements.append({
                "data": {
                    "id": node.get("name", ""),
                    "label": node.get("name", ""),
                    "type": node.get("type", ""),
                    "importance": node.get("importance", 5)
                }
            })

        for i, edge in enumerate(graph.get("edges", [])):
            elements.append({
                "data": {
                    "id": f"edge_{i}",
                    "source": edge.get("source", ""),
                    "target": edge.get("target", ""),
                    "label": edge.get("relationship", "")
                }
            })

        return json.dumps(elements, ensure_ascii=False, indent=2)

    def generate_summary(self, graph: Dict = None, language: str = "中文") -> str:
        """Generate a natural language summary of the knowledge graph"""
        if graph is None:
            graph = {"nodes": self.nodes, "edges": self.edges}

        prompt = f"""基于以下知识图谱数据，生成一段自然语言的总结描述。

节点（概念/实体）：
{json.dumps([n.get('name') for n in graph.get('nodes', [])[:20]], ensure_ascii=False)}

关系：
{json.dumps([(e.get('source'), e.get('relationship'), e.get('target')) for e in graph.get('edges', [])[:20]], ensure_ascii=False)}

请用{language}写一段流畅的总结，描述这些概念之间的关系和整体知识结构。"""

        return self.ai_client.chat(prompt)
