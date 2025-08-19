# chains/network_analysis.py
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import base64
import io
from chains.base import BaseWorkflow

class NetworkAnalysisWorkflow(BaseWorkflow):
    """Workflow for network analysis tasks"""
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Extract files from input
            files = input_data.get("additional_files", {})
            task_description = input_data.get("task_description", "")
            
            # Find edges.csv
            edges_content = None
            for filename, content in files.items():
                if "edges" in filename.lower() and filename.lower().endswith(".csv"):
                    edges_content = content
                    break
            
            if not edges_content:
                return {"error": "edges.csv not found in uploaded files"}
            
            # Parse edges.csv
            edges_df = pd.read_csv(io.StringIO(edges_content))
            
            # Create network graph
            G = nx.Graph()
            for _, row in edges_df.iterrows():
                G.add_edge(row['node1'], row['node2'])
            
            # Calculate metrics
            edge_count = G.number_of_edges()
            degrees = dict(G.degree())
            highest_degree_node = max(degrees, key=degrees.get)
            average_degree = sum(degrees.values()) / len(degrees)
            density = nx.density(G)
            
            # Calculate shortest path
            try:
                shortest_path = nx.shortest_path_length(G, 'Alice', 'Eve')
            except:
                shortest_path = -1  # No path exists
            
            # Generate network graph
            network_graph = self._generate_network_graph(G)
            
            # Generate degree histogram
            degree_histogram = self._generate_degree_histogram(degrees)
            
            return {
                "edge_count": edge_count,
                "highest_degree_node": highest_degree_node,
                "average_degree": average_degree,
                "density": density,
                "shortest_path_alice_eve": shortest_path,
                "network_graph": network_graph,
                "degree_histogram": degree_histogram
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _generate_network_graph(self, G):
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                node_size=2000, font_size=12, font_weight='bold')
        plt.title("Network Graph")
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        return img_base64
    
    def _generate_degree_histogram(self, degrees):
        plt.figure(figsize=(10, 6))
        degree_values = list(degrees.values())
        plt.hist(degree_values, bins=range(min(degree_values), max(degree_values)+2), 
                color='green', alpha=0.7, edgecolor='black')
        plt.xlabel('Degree')
        plt.ylabel('Frequency')
        plt.title('Degree Distribution')
        plt.grid(True, alpha=0.3)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        return img_base64
