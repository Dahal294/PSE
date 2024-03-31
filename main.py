import streamlit as st
from streamlit_option_menu import option_menu  # Custom module for option menu

from tabs import (upload_graph,  # Custom module for tab functionalities
                  create_nodes,
                  update_node,
                  store_graph,
                  visualize_graph,
                  analyze_graph,
                  export_graph, create_relations
                  )
from impact_function import check_recheability, check_similar
import networkx as nx


if __name__ == '__main__':
    # Initialize session state variables if not present
    if "node_list" not in st.session_state:
        st.session_state["node_list"] = []
    if "edge_list" not in st.session_state:
        st.session_state["edge_list"] = []
    if "graph_dict" not in st.session_state:
        st.session_state["graph_dict"] = []


    global G1 
    G1 = nx.DiGraph()
    graph_dict = st.session_state["graph_dict"]
    if graph_dict:
        node_list = graph_dict["nodes"]
        edge_list = graph_dict["edges"]
        edge_tuple_list = []

        node_tuple_list = [(node["id"], node) for node in node_list]
        for edge in edge_list:
            edge_tuple = (edge["source"], edge["target"], edge)
            edge_tuple_list.append(edge_tuple)

        G1.add_nodes_from(node_tuple_list)
        G1.add_edges_from(edge_tuple_list)
    # List of tabs for the sidebar
    tab_list = [
        "Import Graph",
        "Store Nodes",
        "Update/View Nodes",
        "Update Relations",
        "Store the Graph",
        "Visualize the Graph",
        "Analyze the Graph",
        "Impact Analysis",
        "Find the Similar Production Structure",
        "Export the Graph" 
        
     ]

    # Set page configuration
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")

    # Sidebar creation
    with st.sidebar:
        # Generate option menu for selecting tabs
        selected_tab = option_menu("Main Menu",
                                   tab_list,
                                   icons = ["cloud-upload",   "save", "pen", "pen" , "save",  "binoculars",    "list-ol"   , "lightbulb", "search", "cloud-download" ],
                                   menu_icon="cast",
                                   default_index=0,
                                   orientation="vertical"
                                   )

    # Main application interface title
    st.title("PyInPSE Tutorial 1")

    # Conditional rendering of tab functionalities based on selected_tab
    if selected_tab == "Import Graph":
        upload_graph()

    if selected_tab == "Store Nodes":
        create_nodes()

    if selected_tab == "Update/View Nodes":
        update_node()

    if selected_tab == "Store the Graph":
        store_graph()

    if selected_tab == "Update Relations":
        create_relations()

    if selected_tab == "Visualize the Graph":
        visualize_graph()

    if selected_tab == "Analyze the Graph":
        analyze_graph()

    if selected_tab == "Export the Graph":
        export_graph()

    if selected_tab == "Impact Analysis":         
        if G1:          
            check_recheability(graph = G1)
        else:
            st.warning("There is no graph to see impact. Please upload one.")

    if selected_tab == "Find the Similar Production Structure":
        if st.session_state["graph_dict"]:
            check_similar(graph = G1)
        else:
            st.warning("There currently  no Graph in session state")






        # for node in graph_dict["nodes"]:
        #     name = node["label"]
        #     store = node["view"]
        #     for key in store.keys():               
        #         key1 = store[key]["properties"]
        #         st.write(name)                
        #         for node1 in key1:
        #             if store[key]["id"] == "view-automation_view":
        #                 result = node1["name"]
        #                 result1 = node1["unit"]
        #                 st.write(f"{result}  {result1}")
        #             if store[key]["id"] == 'view-basic_engineering view':
        #                 result2 = node1["name"]
        #                 result3 = node1["max_value"]
        #                 result4 = node1["unit"]
        #                 st.write(f"the  {result2}  is {result3} {result4} ")


    
