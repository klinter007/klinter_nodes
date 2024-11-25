import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "YellowBusV1_9",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "YellowBusV1_9") {
            // Handle dynamic type adaptation
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                if (type === LiteGraph.INPUT && connected) {
                    const otherNode = this.graph._nodes_by_id[link_info.origin_id];
                    if (otherNode && otherNode.outputs && otherNode.outputs[link_info.origin_slot]) {
                        const otherType = otherNode.outputs[link_info.origin_slot].type;
                        // Update both input and corresponding output to match connected type
                        this.inputs[index].type = otherType;
                        this.outputs[index].type = otherType;
                    }
                }
            }

            // Initialize inputs and outputs
            nodeType.prototype.onNodeCreated = function() {
                // Add initial 10 inputs and outputs
                for(let i = 0; i < 10; i++) {
                    this.addInput(`value_${i+1}`, "*");
                    this.addOutput(`out_${i+1}`, "*");
                }
            }
        }
    }
});
