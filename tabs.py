import streamlit as st
import json
import uuid
from model import metamodel_dict
import graphviz
from streamlit_agraph import agraph, Node, Edge, Config
import networkx as nx


# def add_color(node):
#     color = ""
#     if

def upload_graph():
    uploaded_graph = st.file_uploader("Upload an existing Graph", type="json")
    if uploaded_graph is not None:
        uploaded_graph_dict = json.load(uploaded_graph)

        uploaded_node = uploaded_graph_dict["nodes"]
        uploaded_edge = uploaded_graph_dict["edges"]

    else:
        st.info("Please upload a graph if available")

    update = st.button("Upload", use_container_width=True, type="primary")

    if update and uploaded_graph is not None:
        st.session_state["Node_list"] = uploaded_node
        st.session_state["edge_list"] = uploaded_edge



def save_edge(Node1, relation, Node2):
    edge_dict = {
        "Source": Node1,
        "Target": Node2,
        "type": relation,
        "id": str(uuid.uuid1())
    }
    st.session_state["edge_list"].append(edge_dict)


def print_hi(name, age):
    # Use a breakpoint in the code line below to debug your script.
    st.info(f'Hi,My name is  {name} and I am {age} ')


def save_Node(name, age):
    Node_dict = {
        "id": str(uuid.uuid1()),
        'name': name,
        'age': age,
        "type": "Node"
    }
    st.session_state["Node_list"].append(Node_dict)


def create_Node():
    name_Node = st.text_input('What is your name?')
    age_Node = st.number_input('Input the age of the Node', value=0)
    print_hi(name_Node, age_Node)
    save_Node_button = st.button("Store Node ", use_container_width=True)
    if save_Node_button:
        save_Node(name_Node, age_Node)
    st.write(st.session_state["Node_list"])


def create_relation():
    Node1_col, relation_col, Node2_col = st.columns(3)
    Node_list = st.session_state["Node_list"]
    Node_name_list = []
    for Node in Node_list:
        Node_name_list.append(Node['name'])
    with Node1_col:
        Node_list = st.session_state["Node_list"]
        Node1_select = st.selectbox('Select the first Node',
                                      options=Node_name_list,
                                      key='Node1_select'
                                      )
    with relation_col:
        # Logic
        relation_list = metamodel_dict["edges"]
        relation_name = st.selectbox('Specify the relation',
                                     options=["Friends With", "Parent of", "Child of", "Sibling of", "Colleague of"]
                                     )
    with Node2_col:
        Node2_select = st.selectbox('Select the second Node',
                                      options=["David", "Ranjit", "Paula"],
                                      )

    store_edge_button = st.button("Store Relation", use_container_width=True, type="primary")
    if store_edge_button:
        save_edge(Node1_select, relation_name, Node2_select)
    st.write(f"{Node1_select} is {relation_name}  with {Node2_select}")
    st.write(st.session_state["edge_list"])


def visualize_graph():
    global graph_dict
    graph_dict = {
        "nodes": st.session_state["Node_list"],
        "edges": st.session_state["edge_list"],

    }
    st.session_state["graph_dict"] = graph_dict
    with st.expander("Visualize the graph"):
        graph = graphviz.Digraph()
        graph_dict = st.session_state["graph_dict"]
        node_list = graph_dict["nodes"]
        edge_list = graph_dict["edges"]

        for node in node_list:
            node_name = node["name"]
            graph.node(node_name)
        for edge in edge_list:
            source = edge["Source"]
            target = edge["Target"]
            label = edge["type"]
            graph.edge(source, target, label)
        st.graphviz_chart(graph)


def store_graph():
    with st.expander("Show individual lists"):
        st.json(st.session_state["Node_list"], expanded=False)
        st.json(st.session_state["edge_list"], expanded=False)

    with st.expander("Show Graph JSON"):
        st.json(graph_dict)

    # nodes = []
    # edges = []
    # nodes.append(Node(id="Spiderman",
    #                   label="Peter Parker",
    #                   size=25,
    #                   shape="circularImage",
    #                   image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png")
    #              )  # includes **kwargs
    # nodes.append(Node(id="Captain_Marvel",
    #                   size=25,
    #                   shape="circularImage",
    #                   image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png")
    #              )
    # edges.append(Edge(source="Captain_Marvel",
    #                   label="friend_of",
    #                   target="Spiderman",
    #                   # **kwargs
    #                   )
    #              )
    #
    # config = Config(width=750,
    #                 height=950,
    #                 directed=True,
    #                 physics=True,
    #                 hierarchical=False,
    #                 # **kwargs
    #                 )


def analyze_graph():
    G = nx.Graph()
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge_list = graph_dict["edges"]
    node_tuple_list = []
    edge_tuple_list = []
    # for node in node_list:
    #     G.add_node(node["name"])
    #     st.write(G)
    for node in node_list:
        node_tuple = (node["name"])
        node_tuple_list.append(node_tuple)

    for edge in edge_list:
        edge_tuple = (edge["Source"], edge["Target"], edge)
        edge_tuple_list.append(edge_tuple)

    G.add_edges_from(node_tuple_list)
    G.add_nodes_from(node_tuple_list)
    st.write(G.nodes)
    st.write(G.edges)


def export_graph():
    graph_string = json.dumps(st.session_state['graph_dict'])
    st.write(graph_string)

    st.download_button(label="Export to JSON",
                       file_name="graph.json",
                       mime='application/json',
                       data=graph_string,
                       use_container_width=True,
                       type="primary")
