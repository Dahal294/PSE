import streamlit as st
import networkx as nx
import graphviz

# Function to output nodes and edges of a graph
def output_nodes_and_edges(graph: nx.Graph):
    st.write([graph.nodes[node].get("label") for node in graph.nodes])
    edge_labels = [
    (
        next((node.get("label") for node in st.session_state["node_list"] if node.get("id") == a), None),
        next((node.get("label") for node in st.session_state["node_list"] if node.get("id") == b), None)
    )
    for a, b in graph.edges
    ]

    st.write(edge_labels)

# Function to count the number of nodes in a graph
def count_nodes(graph: nx.Graph):
    num_nodes = len(graph.nodes)
    st.info(f"The graph has {num_nodes} nodes")

# Function to calculate the density of a graph
def find_density(graph: nx.Graph):
    density = nx.density(graph)
    st.info(f"The density of graph is {density}")

# Function to check if there exists a path between two nodes in a graph
class NodeInfo:
    def __init__(self, node_id, label):
        self.node_id = node_id
        self.label = label

def check_path(graph: nx.Graph):
    node_info_list = [NodeInfo(node_id, node_data["label"]) for node_id, node_data in graph.nodes(data=True)]
    
    node1_col, node2_col = st.columns(2)
    with node1_col:
        node1_select = st.selectbox("Select first node", options=[node_info.label for node_info in node_info_list], key="node1_select")
    with node2_col:
        node2_select = st.selectbox("Select second node", options=[node_info.label for node_info in node_info_list], key="node2_select")
    
    if node1_select and node2_select:
        # Retrieve the corresponding IDs using the node_info_list
        node1_id = next(node_info.node_id for node_info in node_info_list if node_info.label == node1_select)
        node2_id = next(node_info.node_id for node_info in node_info_list if node_info.label == node2_select)
        
        if nx.has_path(graph, node1_id, node2_id):
            st.success(f"There is a path between node {node1_select} and node {node2_select}.")
        else:
            st.error(f"There is no path between node {node1_select} and node {node2_select}.")


# Function to check if a graph is empty
def is_empty(graph: nx.Graph):
    is_empty = nx.is_empty(graph)
    if is_empty:
        st.info("The graph is empty.")
    else:
        st.info("The graph is not empty.")

# Function to check if a graph is directed
def is_directed(graph: nx.Graph):
    is_directed = nx.is_directed(graph)
    if is_directed:
        st.info("The graph is directed.")
    else:
        st.info("The graph is not directed")

# Function to display information about a specific node in the graph
def specific_node(graph: nx.Graph):
    node_select = st.selectbox("Select node", options=graph.nodes, key="node_select")
    node = graph.nodes[node_select]
    st.info(node)

# Function to find and visualize the shortest path between two nodes in a graph
def shortest_path(graph: nx.Graph):
    source_node_col, sink_node_col = st.columns(2)

    # Extracting labels from node data dictionary for options
    node_labels1 = [graph.nodes[node] for node in graph.nodes]
    node_labels = [i.get("label") for i in node_labels1]

    print(node_labels)
    with source_node_col:
        source_node_label = st.selectbox(
            "Select Process 1",
            options=node_labels
        )
        # Find corresponding node ID for the selected label
        source_node = next(node for node in graph.nodes if graph.nodes[node]["label"] == source_node_label)

    with sink_node_col:
        sink_node_label = st.selectbox(
            "Select Product 2",
            options=node_labels
        )
        # Find corresponding node ID for the selected label
        sink_node = next(node for node in graph.nodes if graph.nodes[node]["label"] == sink_node_label)

    find_path_button = st.button('Find the path', type="primary")

    if find_path_button:
        if source_node == sink_node:
            st.error("Please select different products")
        else:
            try:
                shortest_path_for_graph = nx.shortest_path(graph, source_node, sink_node)

                # Convert node IDs to labels
                shortest_path_labels = [graph.nodes[node]["label"] for node in shortest_path_for_graph]

                # Display the shortest path with labels
                st.info(
                    f"The shortest path between {source_node_label} and {sink_node_label} is {shortest_path_labels}")

                # Create a subgraph containing only nodes in the shortest path
                subgraph = graph.subgraph(shortest_path_for_graph)

                # Create a graphviz graph
                path_graph = graphviz.Digraph()
                for node in subgraph.nodes:
                    path_graph.node(graph.nodes[node]["label"])  # Use node label as node name
                for edge in subgraph.edges:
                    # Use node labels instead of node IDs for edges
                    path_graph.edge(graph.nodes[edge[0]]["label"], graph.nodes[edge[1]]["label"])

                st.graphviz_chart(path_graph)

            except nx.NetworkXNoPath:
                st.error(f"No path exist between {source_node_label} and {sink_node_label}")