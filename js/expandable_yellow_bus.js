import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "YellowBusV2",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "YellowBusV2") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                onNodeCreated?.apply(this, arguments);
                this.connections = 1;
                this.addWidget("button", "Add Connection", null, () => {
                    this.addNewPair();
                });
                this.addWidget("button", "Remove Connection", null, () => {
                    this.removePair();
                });
                this.updateConnections();
            };

            nodeType.prototype.addNewPair = function() {
                if (this.connections < 10) {  // Changed from 5 to 10
                    this.connections++;
                    this.updateConnections();
                }
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
                    const index = this.inputs.length;
                    this.addInput(`in ${index + 1}`, "*");
                    this.addOutput("*", "*");
                }
                this.size = this.computeSize();
                app.graph.setDirtyCanvas(true, true);
            };

            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                if (type === LiteGraph.INPUT) {
                    if (connected) {
                        const otherNode = this.graph._nodes_by_id[link_info.origin_id];
                        if (otherNode && otherNode.outputs && otherNode.outputs[link_info.origin_slot]) {
                            const otherSlot = otherNode.outputs[link_info.origin_slot];
                            this.inputs[index].type = otherSlot.type;
                            this.outputs[index].type = otherSlot.type;
                            this.inputs[index].name = otherSlot.name || otherSlot.type;
                            this.outputs[index].name = otherSlot.name || otherSlot.type;
                        }
                    } else {
                        this.inputs[index].type = "*";
                        this.outputs[index].type = "*";
                        this.inputs[index].name = `in ${index + 1}`;
                        this.outputs[index].name = "*";
                    }
                }
                this.size = this.computeSize();
                app.graph.setDirtyCanvas(true, true);
            };

            nodeType.prototype.onSerialize = function(o) {
                o.connections = this.connections;
            };

            nodeType.prototype.onConfigure = function(o) {
                this.connections = o.connections || 1;
                this.updateConnections();
            };

            const onCloned = nodeType.prototype.onCloned;
            nodeType.prototype.onCloned = function(original) {
                onCloned?.apply(this, arguments);
                this.connections = original.connections;
                this.updateConnections();
            };
        }
    },
});