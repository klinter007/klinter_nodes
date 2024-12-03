import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Klinter.NodeToString",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "NodeToString") {
            // Store the original onNodeCreated
            const onNodeCreated = nodeType.prototype.onNodeCreated;

            // Override onNodeCreated
            nodeType.prototype.onNodeCreated = function () {
                const result = onNodeCreated?.apply(this, arguments);

                // Add dynamic input
                this.addInput("input", "*");

                return result;
            };

            // Override onConnectionsChange to track source node
            nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info) {
                if (type === 1 && connected && link_info) { // Input connection
                    const sourceNode = app.graph.getNodeById(link_info.origin_id);
                    if (sourceNode) {
                        // Store the source node's title or type
                        this.sourceNodeTitle = sourceNode.title || sourceNode.type || "Unknown Node";
                        
                        // Update the input type to match
                        this.inputs[0].type = sourceNode.outputs[link_info.origin_slot].type;
                    }
                }
            };
        }
    }
});
