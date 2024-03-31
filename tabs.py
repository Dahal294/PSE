import streamlit as st
import json
import uuid

from graph_functions import (find_density,  # Custom module for graph functions
                             check_path,
                             is_empty,
                             specific_node,
                             is_directed,
                             shortest_path)
from model import metamodel_dict
from ppr_transformer import  ppr_dict_to_graph_dict, graph_dict_to_ppr_dict  # Assuming this module contains some model definitions

# graph_dict = {
#             "nodes": [],
#             "edges": []
#         }
    

def upload_graph():
    # Function to upload an existing graph
    uploaded_graph = st.file_uploader("Upload an existing graph", type="json")
    if uploaded_graph is not None:
        uploaded_graph_dict = json.load(uploaded_graph)
        uploaded_nodes = uploaded_graph_dict["nodes"]
        uploaded_edges = uploaded_graph_dict["edges"]
        if "sourceHandle" in uploaded_graph_dict["edges"][0]:
            uploaded_graph_dict = ppr_dict_to_graph_dict(uploaded_graph_dict)
            uploaded_nodes = uploaded_graph_dict["nodes"]
            uploaded_edges = uploaded_graph_dict["edges"]
    else:
        st.info("Please upload a graph if available")
        uploaded_nodes = []
        uploaded_edges = []
    

    update_graph_button = st.button(
        "Update Graph via the Upload",
        use_container_width=True,
        type="primary"
    )
    if update_graph_button and uploaded_graph is not None:
        st.session_state["node_list"] = uploaded_nodes
        st.session_state["edge_list"] = uploaded_edges
        graph_dict = {
            "nodes": st.session_state["node_list"],
            "edges": st.session_state["edge_list"]
        }
        st.session_state["graph_dict"] = graph_dict

def save_node(label_name, type_name, position = {}, view = {}):
    # Function to save a node
    graph_node = {
            "view": view,
            "id": str(uuid.uuid4()),
            "type": type_name,
            "label": label_name,
            "ui_data": {
                "position": position,
                "width": 150,
                "height": 30,
                "style": {
          "toolbarPosition": "bottom"           
        }
            }
        }
    
    if label_name:
        st.session_state["node_list"].append(graph_node)
        st.info("Data added Successfully")
    else:
        st.error("Enter all Fields")


def delete_node(label1):
    # Function to delete a node
    nodes = st.session_state["node_list"]
    edges = st.session_state["edge_list"]
    label_to_id = {node["label"]: node["id"] for node in nodes}
    if label1 in label_to_id:
        node_id = label_to_id[label1]
        for edge in edges:
            if edge["source"] == node_id or edge["target"] == node_id:
                edges.remove(edge)
        nodes[:] = [node for node in nodes if node["label"] != label1]
        st.info("Data deleted successfully")
    else:
        st.warning("Node not found in the graph.")
    
    


def create_nodes():
    # Function to create nodes
    node_label = st.text_input("Node Label")
    node_type = st.selectbox("Type", options=["product", "process", "resource"])    
    select_view = st.selectbox("Select the view", options = ["", "Automation view", "Basic engineering view", "Sustainability View"])
    view_properties = {}

    if select_view == 'Automation view':
        view_properties["id"] = "view-automation_view"
        view_properties["properties"] = []

        # Allow users to add multiple properties
        num_properties = st.number_input("Number of Properties", min_value=1, value=1)
        for i in range(num_properties):
            property_name = st.text_input(f"Attribute {i+1}")
            target_value = st.number_input(f"Target value {i+1}")
            min_value = st.number_input(f"Min value {i+1}")
            max_value = st.number_input(f"Max value {i+1}")
            unit = st.text_input(f"Unit {i+1}")
            
            property_data = {
                "id": f"property-{i+1}",
                "name": property_name,
                "target_value": target_value,
                "min_value": min_value,
                "max_value": max_value,
                "unit": unit
            }
            view_properties["properties"].append(property_data)

    elif select_view == 'Basic engineering view':
        view_properties["id"] = "view-basic_engineering view"
        view_properties["properties"] = []

        # Allow users to input values for the properties
        num_properties = st.number_input("Number of Properties", min_value=1, value=1)
        for i in range(num_properties):
            property_name = st.text_input(f"Attribute {i+1}")
            target_value = st.number_input(f"Target value {i+1}")
            min_value = st.number_input(f"Min value {i+1}")
            max_value = st.number_input(f"Max value {i+1}")
            unit = st.text_input(f"Unit {i+1}")
            
            property_data = {
                "id": f"property-{i+1}",
                "name": property_name,
                "target_value": target_value,
                "min_value": min_value,
                "max_value": max_value,
                "unit": unit
            }
            view_properties["properties"].append(property_data)
    elif select_view == 'Sustainability View':
        view_properties["id"] = "view-sustainability_view"
        view_properties["properties"] = []
        
        num_properties = st.number_input("Number of Properties", min_value=1, value=1)
        for i in range(num_properties):
            property_name = st.text_input(f"Property Name {i+1}")
            target_value = st.number_input(f"Target Value {i+1}")
            min_value = st.number_input(f"Min Value {i+1}")
            max_value = st.number_input(f"Max Value {i+1}")
            unit = st.text_input(f"Unit {i+1}")
            
            property_data = {
                "id": f"property-{i+1}",
                "name": property_name,
                "target_value": target_value,
                "min_value": min_value,
                "max_value": max_value,
                "unit": unit
            }
            view_properties["properties"].append(property_data)

    save_node_button = st.button("Store Node", use_container_width=True, type="primary")
    if save_node_button:
        save_node(node_label, node_type, view = view_properties)    
   
    



def update_node():
    # Function to update a node
    node_list = st.session_state["node_list"]
    node_names = [node["label"] for node in node_list]
    select = st.selectbox("Update Nodes", options= ["Update Node", "Delete Node", "View Node"])
    if select ==  "Update Node":
        try:
            node_to_update = st.selectbox("Select node to update",
                                        options=node_names,
                                        index=None,
                                        placeholder="Select the node"
                                        )

            selected_index = node_names.index(node_to_update)

            new_name = st.text_input("Enter new name for the node")
            update_node_button = st.button("Update Node", key="update_node_button", use_container_width=True,
                                        type="primary")
            if update_node_button:
                node_list[selected_index]["label"] = new_name
                st.session_state["node_list"] = node_list
                st.success(f"Node '{node_to_update}' has been updated.")

        except ValueError:
            st.info("Choose the Node you want to Update")
    if select == "Delete Node":
        delete = st.selectbox("Select the node to delete", options=[node.get("label") for node in st.session_state["node_list"]])
        delete_node_button = st.button("Delete Node", use_container_width=True, type="secondary")
        if delete_node_button and delete:
            delete_node(delete)
        elif not delete:
            st.warning("Please select a node to delete.")
    if select == "View Node":
        view = st.selectbox("Select the node to delete", options=[node.get("label") for node in st.session_state["node_list"]])        
        if view :
            select_view = st.selectbox("Choose the view to see impact", options=["Basic Engineering View", "Sustainability View", "Automation View"])
            if select_view == "Basic Engineering View":
                Basic_Engineering1 = [node.get("view").get("Basic engineering view") for node in st.session_state["node_list"] if node.get("label") == view]
                if Basic_Engineering1 and isinstance(Basic_Engineering1[0], dict):
                    properties1 = Basic_Engineering1[0]["properties"]                                        
                    st.write(f"<span style='color: white; font-weight: bold;'>The basic engineering view properties of {view}:</span>", unsafe_allow_html=True)
                    for i in range(len(properties1)):
                        st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;<span style='color: green;'> {properties1[i].get('name', '')} :</span>  {properties1[i].get('target_value')} {properties1[i].get('unit')}", unsafe_allow_html=True)
            elif select_view == "Sustainability View":
                Sustainability1 = [node.get("view").get("Sustainability view") for node in st.session_state["node_list"] if node.get("label") == view]
                if Sustainability1 and isinstance(Sustainability1[0], dict):
                    properties2 = Sustainability1[0]["properties"]                                        
                    st.write(f"<span style='color: white; font-weight: bold;'>The Sustainability view properties of {view}:</span>", unsafe_allow_html=True)
                    for i in range(len(properties2)):
                        st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;<span style='color: green;'> {properties2[i].get('name', '')} :</span>  {properties2[i].get('target_value')} {properties2[i].get('unit')}", unsafe_allow_html=True)
            elif select_view == "Automation View":
                Automation1 = [node.get("view").get("Automation view") for node in st.session_state["node_list"] if node.get("label") == view]
                if Automation1 and isinstance(Automation1[0], dict):
                    properties3 = Automation1[0]["properties"]                                        
                    st.write(f"<span style='color: white; font-weight: bold;'>The Automation view properties of {view}:</span>", unsafe_allow_html=True)
                    for i in range(len(properties3)):
                        st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;<span style='color: green;'> {properties3[i].get('name', '')} :</span>  {properties3[i].get('target_value')} and {properties3[i].get('unit')}", unsafe_allow_html=True)


def store_graph():
    # Function to store the graph data
    with st.expander("Show individual lists"):
        st.json(st.session_state["node_list"], expanded=True)
        st.json(st.session_state["edge_list"], expanded=False)

    graph_dict = {
        "nodes": st.session_state["node_list"],
        "edges": st.session_state["edge_list"],
    }
    st.session_state["graph_dict"] = graph_dict

    with st.expander("Show Graph JSON", expanded=False):
        st.json(st.session_state["graph_dict"])


def save_edge(node1, relation, node2):
    edge_dict = {
        "source": node1,
        "target": node2,
        "label": relation,
        "id": str(uuid.uuid4()),
    }
    st.session_state["edge_list"].append(edge_dict)
    st.session_state["graph_dict"]["edges"] = st.session_state["edge_list"]

def delete_edge(node1, node2, relation):
    for i, edge in enumerate(st.session_state["edge_list"]):
        if (edge["source"] == node1 and edge["target"] == node2 and edge["label"] == relation):
            del st.session_state["edge_list"][i]  # Remove the edge using index-based deletion
            # Update the graph_dict's "edges" key with the modified edge_list
            st.session_state["graph_dict"]["edges"] = st.session_state["edge_list"].copy()
            return True  # Edge deleted successfully
        # Edge not found
    return False

def update_edge(node1, node2, relation):
    for i, edge in enumerate(st.session_state["edge_list"]):
        if edge["source"] == node1 and edge["target"] == node2:
            # Modify the existing edge, or perform any other necessary updates
            # For example, you might want to update the 'label' of the edge
            st.session_state["edge_list"][i]["label"] = relation

            # Update the graph_dict with the modified edge_list
            st.session_state["graph_dict"]["edges"] = st.session_state["edge_list"].copy()
            return True
    return False

def create_relations():


        # Model logic
    node_name_list= []
    node_list = st.session_state["node_list"]
    for node in node_list:
        node_name_list.append((node["id"], node))

    class NodeInfo:
        def __init__(self, node_id, label, type):
            self.node_id = node_id
            self.label = label
            self.type = type


    node_info_list = [NodeInfo(node_id, node_data.get("label", ""), node_data.get("type", "")) for node_id, node_data in node_name_list]

    select = st.selectbox("Update Relations", options= ["Store Relation", "Update Relation", "Delete Relation"])
    # UI Rendering
    node1_col, relation_col, node2_col = st.columns(3)
    with node1_col:
        node1_select = st.selectbox("Select first node", options=[node_info.label for node_info in node_info_list], key="node1_select")
    with relation_col:
        # Logic
        relation_list = metamodel_dict["edges"]
        # UI Rendering
        relation_name = st.selectbox(
            "Specify the relation",
            options=relation_list)
    with node2_col:
        node2_select = st.selectbox("Select second node", options=[node_info.label for node_info in node_info_list], key="node2_select")  
        # Retrieve the corresponding IDs using the node_info_list
    node1_id = next((node_info.node_id for node_info in node_info_list if node_info.label == node1_select), None)
    node2_id = next((node_info.node_id for node_info in node_info_list if node_info.label == node2_select), None)

    if select == "Delete Relation":
        delete_edge_button = st.button("Delete Relation", use_container_width=True, type="primary")
        if delete_edge_button:
            delete_edge(node1_id, node2_id, relation_name)


    if select == "Store Relation":
        store_edge_button = st.button("Store Relation",
                                use_container_width=True,
                                type="primary")
        if store_edge_button:
            save_edge(node1_id, relation_name, node2_id)
        
    if select == "Update Relation":
        update_edge_button = st.button("Update Relation", use_container_width=True, type="primary")
        if update_edge_button:
            update_edge(node1_id, node2_id, relation_name)

    st.write(f"{node1_select} is {relation_name} {node2_select}")  



def visualize_graph():
    # Function to visualize the graph
    def set_color(node_type):
        color = "Grey"
        if node_type == "resource":
            color = "Blue"
        elif node_type == "product":
            color = "Green"
        elif node_type == "process":
            color = "Violet"
        return color

    import graphviz
    from streamlit_agraph import agraph, Node, Edge, Config

    with st.expander("Graphviz Visualisation"):
        graph = graphviz.Digraph()
        if st.session_state["graph_dict"]:
            graph_dict = st.session_state["graph_dict"]
            node_list = graph_dict["nodes"]
            edge_list = graph_dict["edges"]
            id_to_label = {node["id"]: node["label"] for node in node_list}
            for node in node_list:
                node_name = node["label"]
                graph.node(node_name, color=set_color(node["type"]))
            for edge in edge_list:
                source_id = edge["source"]
                target_id = edge["target"]
                source_label = id_to_label.get(source_id)
                target_label = id_to_label.get(target_id)           
                label = edge["label"]
                
                # Add edge to the graph with node labels instead of IDs
                if source_label is not None and target_label is not None:
                    graph.edge(source_label, target_label, label)

            # Display the graphviz chart
            st.graphviz_chart(graph)
        else:
            st.warning("There is no Graph in Session State. Please upload one")



    with st.expander("Show Graph in AGraph"):
        # Function to visualize the graph using AGraph
        graph_visualisation_nodes = []
        graph_visualisation_edges = []
        for node in st.session_state["node_list"]:
            graph_visualisation_nodes.append(
                Node(
                    id=node["id"],
                    label=node["label"],
                    size=35,  # Increase node size to provide more space for label
                    shape="circularImage",
                    image="https://t4.ftcdn.net/jpg/00/65/77/27/360_F_65772719_A1UV5kLi5nCEWI0BNLLiFaBPEkUbv5Fv.jpg",
                    font={"size": 12}  # Adjust font size for better readability
                )
            )
        for edge in st.session_state["edge_list"]:
            graph_visualisation_edges.append(Edge(
                source=edge["source"],
                label=edge["label"],
                target=edge["target"],
            )
            )
        config = Config(width='100%',
                        height=600,  # Increase height for better visualization
                        directed=True,
                        physics=True,
                        hierarchical=False,  # Disable hierarchical layout to prevent overlapping
                        zoom=0.5,
                        distance=150  # Adjust the distance between nodes as needed
                        )
        agraph(
            nodes=graph_visualisation_nodes,
            edges=graph_visualisation_edges,
            config=config
        )



def analyze_graph():
    # Function to analyze the graph
    import networkx as nx
    from graph_functions import output_nodes_and_edges, count_nodes
    G = nx.DiGraph()
    if st.session_state["graph_dict"]:
        graph_dict = st.session_state["graph_dict"]
        node_list = graph_dict["nodes"]
        edge_list = graph_dict["edges"]
        edge_tuple_list = []

        node_tuple_list = [(node["id"], node) for node in node_list]
        for edge in edge_list:
            edge_tuple = (edge["source"], edge["target"], edge)
            edge_tuple_list.append(edge_tuple)

        G.add_nodes_from(node_tuple_list)
        G.add_edges_from(edge_tuple_list)

        functions = ["Output nodes and edges",
                    "Count Nodes",
                    "Density of Graph",
                    "Check Path",
                    "Check if Graph is Empty",
                    "Shortest Path",
                    ]
        select_function = st.selectbox(label="Select function",
                                    options=functions)
        if select_function == "Output nodes and edges":
            output_nodes_and_edges(graph=G)
        elif select_function == "Count Nodes":
            count_nodes(graph=G)
        elif select_function == "Density of Graph":
            find_density(graph=G)
        elif select_function == "Check Path":
            check_path(graph=G)
        elif select_function == "Check if Graph is Empty":
            is_empty(graph=G)
        elif select_function == "Is Graph Directed":
            is_directed(graph=G)
        elif select_function == "Specific Node":
            specific_node(graph=G)
        elif select_function == "Shortest Path":
            shortest_path(graph=G)
    else:
        st.warning("You need to upload or create  a graph before uploading it ")

def export_graph():
        graph_string = json.dumps(st.session_state["graph_dict"])
        if st.session_state["graph_dict"]:
            ppr_dict = graph_dict_to_ppr_dict(st.session_state["graph_dict"])
            ppr_json = json.dumps(ppr_dict)

            st.download_button(
                "Export Graph to graph_string",
                file_name="graph.json",
                mime="application/json",
                data=graph_string,
                use_container_width=True,
                type="primary"
            )

            st.download_button(
                "Export Graph to ppr_json",
                file_name="graph.json",
                mime="application/json",
                data=ppr_json,
                use_container_width=True,
                type="secondary"
            )
        else:
            st.warning("Please create or upload the graphto export it")