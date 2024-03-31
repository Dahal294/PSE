metamodel_dict = {
    "nodes": [
        {
            "type": "Product",
            "edges": ["Convey to", "Machine at"]
        },
        {
            "type": "Conveyor",
            "edges": ["Motor", "Sensor", "Machine Structure"]
        },
        {
            "type": "Motor",
            "edges": []
        },
        {
            "type": "Sensor",
            "edges": []
        },
        {
            "type": "Switch",
            "edges": []
        },
        {
            "type": "Lamp",
            "edges": []
        },
        {
            "type": "Machine Structure",
            "edges": []
        }
    ],
    "edges": ["triggered by", "signal for", "conveyed by"]
}
