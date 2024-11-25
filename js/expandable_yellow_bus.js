import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "YellowBusV2",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "YellowBusV2") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                onNodeCreated?.apply(this, arguments);
                this.connections = 1;  // Start with one pair
                
                // Add UI controls
                this.addWidget("button", "Add Connection", null, () => {
                    this.addNewPair();
                });
                this.addWidget("button", "Remove Connection", null, () => {
                    this.removePair();
                });
                
                // Initialize the first pair
                this.updateConnections();
            };

            nodeType.prototype.addNewPair = function() {
                if (this.connections < 10) {  // Maximum 10 pairs
                    this.connections++;
                    this.updateConnections();
                }
            };

            nodeType.prototype.removePair = function() {
                if (this.connections > 1) {  // Always keep at least one pair
                    this.connections--;
                    this.updateConnections();
                }
            };

            nodeType.prototype.updateConnections = function() {
                // Remove excess connections
                while (this.inputs.length > this.connections) {
                    this.removeInput(this.inputs.length - 1);
                    this.removeOutput(this.outputs.length - 1);
                }
                
                // Add new connections
                while (this.inputs.length < this.connections) {
                    const index = this.inputs.length;
                    this.addInput(`in_${index + 1}`, "*");  // Start with wildcard type
                    this.addOutput(`out_${index + 1}`, "*");  // Start with wildcard type
                }
                
                // Update node size
                this.size = this.computeSize();
                app.graph.setDirtyCanvas(true, true);
            };

            // Handle dynamic type adaptation when connections change
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                if (type === LiteGraph.INPUT) {
                    if (connected) {
                        // Get the connected node's output type
                        const otherNode = this.graph._nodes_by_id[link_info.origin_id];
                        if (otherNode && otherNode.outputs && otherNode.outputs[link_info.origin_slot]) {
                            const otherSlot = otherNode.outputs[link_info.origin_slot];
                            
                            // Update input and output types to match
                            this.inputs[index].type = otherSlot.type;
                            this.outputs[index].type = otherSlot.type;
                            
                            // Update names to show the type
                            this.inputs[index].name = `in_${index + 1} (${otherSlot.type})`;
                            this.outputs[index].name = `out_${index + 1} (${otherSlot.type})`;
                        }
                    } else {
                        // Reset to wildcard type when disconnected
                        this.inputs[index].type = "*";
                        this.outputs[index].type = "*";
                        this.inputs[index].name = `in_${index + 1}`;
                        this.outputs[index].name = `out_${index + 1}`;
                    }
                }
                
                // Update node size
                this.size = this.computeSize();
                app.graph.setDirtyCanvas(true, true);
            };

            // Save/load the number of connections
            nodeType.prototype.onSerialize = function(o) {
                o.connections = this.connections;
            };

            nodeType.prototype.onConfigure = function(o) {
                this.connections = o.connections || 1;
                this.updateConnections();
            };

            // Handle cloning
            const onCloned = nodeType.prototype.onCloned;
            nodeType.prototype.onCloned = function(original) {
                onCloned?.apply(this, arguments);
                this.connections = original.connections;
                this.updateConnections();
            };
        }
    }
});