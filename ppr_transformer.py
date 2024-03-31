import json


def ppr_dict_to_graph_dict(ppr_dict):
    ppr_nodes = ppr_dict["nodes"]
    ppr_edges = ppr_dict["edges"]
    graph_nodes = []
    graph_edges = []
    for node in ppr_nodes:
        graph_node = {
            "id": node["id"],
            "type": node["type"],
            "label": node["data"]["label"],
            "view": node["data"]["props"]["views"],
            "ui_data": {
                "position": node["position"],
                "width": node["width"],
                "height": node["height"],
                "style": node["data"]["style"],
            }
        }
        graph_nodes.append(graph_node)
    for edge in ppr_edges:
        graph_edge = {
            "id": edge["id"],
            "label": edge["label"],
            "source": edge["source"],
            "target": edge["target"],
            "type": edge["label"],
            "ui_data": {
                "sourceHandle": edge["sourceHandle"],
                "targetHandle": edge["targetHandle"],
            }
        }
        graph_edges.append(graph_edge)

    graph_dict = {
        "nodes": graph_nodes,
        "edges": graph_edges
    }
    return graph_dict


# Function to convert a graph dictionary to a PPR dictionary
# Get calls to the dict prevent errors if the keys are not present
def graph_dict_to_ppr_dict(graph_dict):
    ppr_nodes = []
    ppr_edges = []

    for node in graph_dict.get("nodes", []):
        ppr_node = {
            "id": node.get("id", None),
            "type": node.get("type", None),
            "data": {
                "label": node.get("label", None),
                "props": {
                    "views": node.get("view", None),
                },
                "style": node.get("ui_data", {}).get("style", None),
            },
            "position": node.get("ui_data", {}).get("position", None),
            "width": node.get("ui_data", {}).get("width", None),
            "height": node.get("ui_data", {}).get("height", None),
        }
        ppr_nodes.append(ppr_node)

    for edge in graph_dict.get("edges", []):
        ppr_edge = {
            "id": edge.get("id", None),
            "label": edge.get("label", None),
            "source": edge.get("source", None),
            "target": edge.get("target", None),
            "sourceHandle": edge.get("ui_data", {}).get("sourceHandle", None),
            "targetHandle": edge.get("ui_data", {}).get("targetHandle", None),
        }
        ppr_edges.append(ppr_edge)

    ppr_dict = {
        "nodes": ppr_nodes,
        "edges": ppr_edges,
    }
    return ppr_dict