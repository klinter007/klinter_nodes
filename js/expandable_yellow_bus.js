import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "YellowBusV2",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "YellowBusV2") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                onNodeCreated?.apply(this, arguments);
                this.addWidget("button", "Add Connection", null, () => {
                    this.addNewPair();
                });
                this.addWidget("button", "Remove Connection", null, () => {
                    this.removePair();
                });
                this.connections = 2;
                this.updateConnections();
            };

            nodeType.prototype.addNewPair = function() {
                this.connections++;
                this.updateConnections();
            };

            nodeType.prototype.removePair = function() {
                if (this.connections > 1) {
                    this.connections--;
                    this.updateConnections();
                }
            };

            nodeType.prototype.updateConnections = function() {
                while (this.inputs.length > this.connections) {
                    this.removeInput(this.inputs.length - 1);
                    this.removeOutput(this.outputs.length - 1);
                }
                while (this.inputs.length < this.connections) {
                    this.addInput("Plug me", "*");
                    this.addOutput("Plug me", "*");
                }
                this.size = this.computeSize();
                app.graph.setDirtyCanvas(true, true);
            };

            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                if (connected && type === LiteGraph.INPUT && link_info) {
                    const otherNode = this.graph._nodes_by_id[link_info.origin_id];
                    if (otherNode && otherNode.outputs && otherNode.outputs[link_info.origin_slot]) {
                        const otherSlot = otherNode.outputs[link_info.origin_slot];
                        this.inputs[index].type = otherSlot.type;
                        this.outputs[index].type = otherSlot.type;
                        this.inputs[index].name = otherSlot.type;
                        this.outputs[index].name = otherSlot.type;
                    }
                } else if (!connected || type === LiteGraph.INPUT) {
                    this.inputs[index].type = "*";
                    this.outputs[index].type = "*";
                    this.inputs[index].name = "Plug me";
                    this.outputs[index].name = "Plug me";
                }
                this.setDirtyCanvas(true, true);
            };
        }
    },
});