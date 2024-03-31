import networkx as nx
import streamlit as st





class NodeInfo:
    def __init__(self, node_id, label, type, view):
        self.node_id = node_id
        self.label = label
        self.type = type
        self.view = view



def check_recheability(graph:nx.Graph):    
    selection = st.selectbox("Choose what you want to do", options = ["check recheability", "check impact"])
    node_info_list = [NodeInfo(node_id, node_data.get("label", ""), node_data.get("type", ""), node_data.get("view", "")) for node_id, node_data in graph.nodes(data=True)]    
    if selection == "check recheability" :
        node1_col, node2_col = st.columns(2)
        with node1_col:
            node1_select = st.selectbox("Select first node", options=[node_info.label for node_info in node_info_list], key="node1_select")
        with node2_col:
            node2_select = st.selectbox("Select second node", options=[node_info.label for node_info in node_info_list], key="node2_select")
        
            # Retrieve the corresponding IDs using the node_info_list
        node1_id = next((node_info.node_id for node_info in node_info_list if node_info.label == node1_select), None)
        node2_id = next((node_info.node_id for node_info in node_info_list if node_info.label == node2_select), None)
        
        if nx.has_path(graph, node1_id, node2_id):
            st.success(f"The {node1_select} is recheable from {node2_select}.")
        else:
            st.error(f"The  {node1_select} is not recheable from {node2_select}.")
    if  selection == "check impact" :
        selection = st.selectbox("Choose the type of impact", options = ["process on product", "product on product", "resource on product"])
        if selection == "process on product":
            node1, node2 = st.columns(2)
            with node1:
                node1_select1 = st.selectbox("Select first node", options=[node_info.label for node_info in node_info_list if node_info.type == "process"], key="node1_select1")
            with node2:
                node2_select2 = st.selectbox("Select second node", options=[node_info.label for node_info in node_info_list if node_info.type == "product" ], key="node2_select2")
            node1_id1 = next((node_info.node_id for node_info in node_info_list if node_info.label == node1_select1), None)
            node2_id2 = next((node_info.node_id for node_info in node_info_list if node_info.label == node2_select2), None)
            node3_id3 = [node_info.node_id for node_info in node_info_list if node_info.type == "resource"]
          
            if nx.has_path(graph, node1_id1, node2_id2):
                if nx.shortest_path_length(graph, source = node1_id1, target = node2_id2) == 1:
                       
                        resource = []
                        for node in node3_id3:
                            if nx.has_path(graph, node1_id1, node ):
                                if nx.shortest_path_length(graph, source = node1_id1, target = node) == 1:
                                    resource.append(node)
                                
                            resource2 = []
                            for res in resource:
                                for node1 in node3_id3:
                                    if nx.has_path(graph, res,  node1 ):
                                        resource2.append(node1)
                        
                        select_view = st.selectbox("Choose the view to see impact", options=["Basic Engineering View", "Sustainability View", "Automation view"])
                        if select_view == "Basic Engineering View":
                            cost = 0
                            for res in resource2:
                                    Basic_Engineering = [node_info.view.get("Basic engineering view") for node_info in node_info_list if res == node_info.node_id]
                                    if Basic_Engineering and isinstance(Basic_Engineering[0], dict):
                                        properties = Basic_Engineering[0]["properties"]
                                    node_info = next((node_info for node_info in node_info_list if res == node_info.node_id), None)
                                    if node_info:
                                        res_name = node_info.label  # Get the name of the NodeInfo instance
                                        # st.write(f"<span style='color: white; font-weight: bold;'>The basic engineering view properties of {res_name}:</span>", unsafe_allow_html=True)
                                        for i in range(len(properties)):
                                            # st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;<span style='color: green;'> {properties[i].get('name', '')} :</span>  {properties[i].get('target_value')} {properties[i].get('unit')}", unsafe_allow_html=True)
                                            if properties[i].get('name', '') == "Cost":
                                                cost += int(properties[i].get('target_value'))                                  
                                    else:
                                        st.write("NodeInfo not found.")
                            st.write(f"The overall cost of resources for process \"{node1_select1} \" on product \"{node2_select2} \"  is {cost} euros. ")
                        if select_view == "Sustainability View":
                            Co2 = 0
                            power_consumption = 0
                            for res in resource2:
                                    Sustainability = [node_info.view.get("Sustainability view") for node_info in node_info_list if res == node_info.node_id]
                                    if Sustainability and isinstance(Sustainability[0], dict):
                                        properties1 = Sustainability[0]["properties"]
                                        print(properties1)    
                                        node_info = next((node_info for node_info in node_info_list if res == node_info.node_id), None)
                                        if node_info:
                                            res_name = node_info.label
                                            for i in range(len(properties1)):
                                                if properties1[i].get('id', '') == "property-power_consumption":
                                                    power_consumption += int(properties1[i].get('target_value'))

                                                if properties1[i].get('id', '') == "property-co2_emission":
                                                    Co2 += int(properties1[i].get('target_value'))
                                    else: 
                                            pass
                            st.write(f"The overall Carbondioxide emission of resources for process \"{node1_select1} \" on product \"{node2_select2} \"  is {Co2} kgs. ")
                            st.write(f"The overall power consumption of resources for process \"{node1_select1} \" on product \"{node2_select2} \"  is {power_consumption} Watt. ")
                                            




                        
            else:
                st.write("There is no path")


        if selection == "resource on product":
             
            node11, node22 = st.columns(2)
            with node11:
                node1_select11 = st.selectbox("Select first node", options=[node_info.label for node_info in node_info_list if node_info.type == "resource"], key="node1_select11")
            with node22:
                node2_select22 = st.selectbox("Select second node", options=[node_info.label for node_info in node_info_list if node_info.type == "product" ], key="node2_select22")
            node1_id11 = next((node_info.node_id for node_info in node_info_list if node_info.label == node1_select11), None)
            node2_id22 = next((node_info.node_id for node_info in node_info_list if node_info.label == node2_select22), None)
            node3_id33 = [node_info.node_id for node_info in node_info_list if node_info.type == "process"]
            for node in node3_id33:
                if nx.has_path(graph, node, node2_id22) and nx.shortest_path_length(graph, source=node, target=node2_id22) == 1:
                    if nx.has_path(graph, node, node1_id11) and not nx.has_path(graph, node2_id22, node):
                            shortest_path = nx.shortest_path(graph, source=node, target=node1_id11)
                            node11 = False
                            for node1 in node3_id33:
                                if node1 != node: 
                                    if node1  in shortest_path:
                                        node11 = True
                            if  not node11:
                                select_resource = st.selectbox("Choose the view to see impact", options=["Basic Engineering View", "Sustainability View", "Automation view"])
                                if select_resource == "Basic Engineering View":
                                    Basic_Engineering1 = [node_info.view.get("Basic engineering view") for node_info in node_info_list if node1_id11 == node_info.node_id]
                                    if Basic_Engineering1 and isinstance(Basic_Engineering1[0], dict):
                                        properties1 = Basic_Engineering1[0]["properties"]                                        
                                        st.write(f"<span style='color: white; font-weight: bold;'>The basic engineering view properties of {node1_select11}:</span>", unsafe_allow_html=True)
                                        for i in range(len(properties1)):
                                            st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;<span style='color: green;'> {properties1[i].get('name', '')} :</span>  {properties1[i].get('target_value')} {properties1[i].get('unit')}", unsafe_allow_html=True)
                                if select_resource == "Sustainability View":
                                    Sustainability_1 = [node_info.view.get("Sustainability view") for node_info in node_info_list if node1_id11 == node_info.node_id]
                                    if Sustainability_1 and isinstance(Sustainability_1[0], dict):
                                        properties2 = Sustainability_1[0]["properties"]                                        
                                        st.write(f"<span style='color: white; font-weight: bold;'>The Sustainability view properties of {node1_select11}:</span>", unsafe_allow_html=True)
                                        for i in range(len(properties2)):
                                            st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;<span style='color: green;'> {properties2[i].get('name', '')} :</span>  {properties2[i].get('target_value')} {properties2[i].get('unit')}", unsafe_allow_html=True)
                                if select_resource == "Automation view":
                                    st.write(f"The  {node1_select11} has an impact on {node2_select22}.")
                                else:
                                    pass
                            
                    else:
                        st.write(f"There is no effect of resource \" {node1_select11} \"  on product  \"{node2_select22} \" ")
                                                 
                else:
                     pass
           
        if selection == "product on product":
            nodea, nodeb = st.columns(2)
            with nodea:
                nodea_selecta = st.selectbox("Select first node", options=[node_info.label for node_info in node_info_list if node_info.type == "product"], key="nodea_selecta")
            with nodeb:
                nodeb_selectb = st.selectbox("Select second node", options=[node_info.label for node_info in node_info_list if node_info.type == "product" ], key="nodeb_selectb")
            nodea_ida = next((node_info.node_id for node_info in node_info_list if node_info.label == nodea_selecta), None)
            nodeb_idb = next((node_info.node_id for node_info in node_info_list if node_info.label == nodeb_selectb), None)  
            if nx.has_path (graph, nodea_ida, nodeb_idb):
                st.info(f"There is impact of product \"{nodea_selecta} \" on  product \"{nodeb_selectb} \"")
            else:
                st.warning(f"There is no impact of product \"{nodea_selecta} \" on  product \"{nodeb_selectb} \"")


def check_similar(graph:nx.graph = None):
    node_info_list = [NodeInfo(node_id, node_data.get("label", ""), node_data.get("type", ""), node_data.get("view", "")) for node_id, node_data in graph.nodes(data=True)]
    similar = st.selectbox("chooose the type of similar production system structures you want to view", options = ["Process", "Product", "Resource"])
    if similar == "Process":
        st.header("Production System Elements of Type \"Process\"")  # Use a header for clarity

        with st.container():
            st.markdown(
                """
                <style>
                .custom-list {
                    list-style-type: disc;
                    padding-left: 20px;
                    margin-top: 10px;
                }
                .total-count {
                    font-family: cursive;
                    margin-top: 40px;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            ordered_list = "<ol class='custom-list'>"
            count = 0
            for node in node_info_list:
                if node.type == "process":
                    ordered_list += f"<li>{node.label}</li>"
                    count += 1
            ordered_list += "</ol>"

            st.markdown(ordered_list, unsafe_allow_html=True)

            st.markdown(f"<p class='total-count'>Total Number of Processes: {count}</p>", unsafe_allow_html=True)
    if similar == "Resource" or similar == "Product":
    # Define header based on type
        st.header(f"Production System Elements of Type \"{similar.capitalize()}\"")

        # Define custom CSS for styling
        with st.container():
            st.markdown(
                """
                <style>
                .custom-list {
                    list-style-type: disc;
                    padding-left: 20px;
                    margin-top: 10px;
                }
                .total-count {
                    font-family: cursive;
                    margin-top: 20px;
                }
                .count-info {
                    font-family: sans-serif;
                    margin-bottom: 20px;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            # Initialize an ordered list and count variables
            ordered_list = "<ol class='custom-list'>"
            ordered_list1 = "<ol class='custom-list'>"
            countr = 0
            count = 0
            count_motor = 0
            count_sensor = 0
            count_lamp = 0
            count_switch = 0
            count_machine = 0

            # Populate the ordered list with recurring elements in the "Resource" type
            for node in node_info_list:
                if node.type.lower() == "resource":
                    if "Motor M" in node.label:
                        ordered_list += f"<li>{node.label}</li>"
                        countr += 1
                        count_motor += 1
                    elif "S_" in node.label:
                        ordered_list += f"<li>{node.label}</li>"
                        countr += 1
                        count_sensor += 1
                    elif "Lamp" in node.label:
                        ordered_list += f"<li>{node.label}</li>"
                        countr += 1
                        count_lamp += 1
                    elif "witch" in node.label:
                        ordered_list += f"<li>{node.label}</li>"
                        countr += 1
                        count_switch += 1
                    elif "achine" in node.label:
                        ordered_list += f"<li>{node.label}</li>"
                        countr += 1
                        count_machine += 1

            if similar.lower() == "resource":
                if count_motor > 0:
                    st.markdown(f"<p class='count-info'> The are total <span style='color: yellow;'> &nbsp; <strong>{count_motor}</strong> &nbsp; </span> Motors in this production system.</p>", unsafe_allow_html=True)
                if count_sensor > 0:
                    st.markdown(f"<p class='count-info'>The are total <span style='color: yellow;'> &nbsp; <strong>{count_sensor}</strong> &nbsp; </span> Sensors in this production system. </p>", unsafe_allow_html=True)
                if count_lamp > 0:
                    st.markdown(f"<p class='count-info'>The are total <span style='color: yellow;'> &nbsp; <strong>{count_lamp}</strong> &nbsp; </span> Lamps in this production system. </p>", unsafe_allow_html=True)
                if count_switch > 0: 
                    st.markdown(f"<p class='count-info'>The are total <span style='color: yellow;'> &nbsp; <strong>{count_switch}</strong> &nbsp; </span> Switches in this production system. </p>", unsafe_allow_html=True)
                if count_machine > 0:
                    st.markdown(f"<p class='count-info'>The are total <span style='color: yellow;'> &nbsp; <strong>{count_machine}</strong> &nbsp; </span> Machine Structures in this production system. </p>", unsafe_allow_html=True)



            # Close the ordered list tag
            ordered_list += "</ol>"

            # Populate the ordered list with the rest of the elements of the specified type
            for node in node_info_list:
                if node.type.lower() == "product" :
                    ordered_list1 += f"<li>{node.label}</li>"
                    count += 1
            ordered_list1 += "</ol>"
            # Display the ordered list
            if similar == "Resource":
                st.markdown(ordered_list, unsafe_allow_html=True)
                st.markdown(f"<p class='total-count'>Total Number of {similar.capitalize()}s: {countr}</p>", unsafe_allow_html=True)
            if similar == "Product":
                st.markdown(ordered_list1, unsafe_allow_html=True)
                st.markdown(f"<p class='total-count'>Total Number of {similar.capitalize()}s: {count}</p>", unsafe_allow_html=True)
            # Display total count of elements of the specified type
            
