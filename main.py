import streamlit as st
from streamlit_option_menu import option_menu
from tabs import upload_graph, create_Node, create_relation, store_graph, visualize_graph, analyze_graph, export_graph

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if 'Node_list' not in st.session_state:
        st.session_state['Node_list'] = []
    if "edge_list" not in st.session_state:
        st.session_state['edge_list'] = []
    if "graph_dict" not in st.session_state:
        st.session_state['graph_dict'] = {}

    st.title('Python in production systems engineering')

    with st.sidebar:
        selected_option = option_menu("Select an option", [
            "Import Graph",
            "Create Nodes(nodes)",
            "Create Relations Between Nodes",
            "Store The Graph",
            "Visualize the Graph",
            "Analyze the Graph ",
            "Export The Graph"
        ])

    if selected_option == "Import Graph":
        upload_graph()
    elif selected_option == "Create Nodes(nodes)":
        create_Node()
    elif selected_option == "Create Relations Between Nodes":
        create_relation()
    elif selected_option == "Store The Graph":
        store_graph()
    elif selected_option == "Visualize the Graph":
        visualize_graph()
    elif selected_option == "Analyze the Graph ":
        analyze_graph()
    elif selected_option == "Export The Graph":
        export_graph()
