import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "KlinterNodes.nodevalue2string",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "nodevalue2string") {
            return;
        }

        // Override connections change to update input name
        const orig_onConnectionsChange = nodeType.prototype.onConnectionsChange;
        nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
            if (orig_onConnectionsChange) {
                orig_onConnectionsChange.apply(this, arguments);
            }

            // Focus on input connections
            if (type === LiteGraph.INPUT) {
                if (connected && link_info) {
                    const sourceNode = app.graph.getNodeById(link_info.origin_id);
                    
                    if (sourceNode) {
                        // Prefer title, fallback to type
                        const nodeName = sourceNode.title || sourceNode.type || `Node_${sourceNode.id}`;
                        
                        // Update the input's name to show the connected node
                        this.inputs[index].label = nodeName;
                        
                        // Store the node name as a custom property
                        this.inputs[index].connectedNodeName = nodeName;
                    }
                } else {
                    // Reset input label when disconnected
                    this.inputs[index].label = null;
                    this.inputs[index].connectedNodeName = "Not Connected";
                }

                // Force graph to redraw
                if (this.graph) {
                    this.graph.setDirtyCanvas(true);
                }
            }
        };
    }
});
