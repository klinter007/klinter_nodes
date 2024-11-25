import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "YellowBusV2",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "YellowBus") {
            // Store original onNodeCreated
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            // Override onNodeCreated to initialize connections
            nodeType.prototype.onNodeCreated = function() {
                onNodeCreated?.apply(this, arguments);
                this.updateConnections();
            };

            // Add button to update connections
            nodeType.prototype.getExtraMenuOptions = function(_, options) {
                options.unshift({
                    content: "Update Connections",
                    callback: () => {
                        this.updateConnections();
                    }
                });
                return options;
            };

            // Update connections when inputcount changes
            nodeType.prototype.onWidgetChange = function(name, value) {
                if (name === "inputcount") {
                    this.updateConnections();
                }
            };

            // Function to update connections based on inputcount
            nodeType.prototype.updateConnections = function() {
                const inputcount = this.widgets.find(w => w.name === "inputcount").value;
                
                // Remove excess connections
                while (this.inputs.length > inputcount) {
                    const index = this.inputs.length - 1;
                    this.removeInput(index);
                    this.removeOutput(index);
                }
                
                // Add new connections
                while (this.inputs.length < inputcount) {
                    const index = this.inputs.length;
                    this.addInput(`value_${index + 1}`, "*");  // Wildcard type
                    this.addOutput(`out_${index + 1}`, "*");   // Wildcard type
                }
                
                // Update node size and canvas
                this.size = this.computeSize();
                app.graph.setDirtyCanvas(true, true);
            };

            // Handle dynamic type adaptation
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                if (type === LiteGraph.INPUT) {
                    if (connected) {
                        // Get connected node's output type
                        const otherNode = this.graph._nodes_by_id[link_info.origin_id];
                        if (otherNode && otherNode.outputs && otherNode.outputs[link_info.origin_slot]) {
                            const otherSlot = otherNode.outputs[link_info.origin_slot];
                            
                            // Update input and output types to match
                            this.inputs[index].type = otherSlot.type;
                            this.outputs[index].type = otherSlot.type;
                            
                            // Update names to show type
                            this.inputs[index].name = `value_${index + 1} (${otherSlot.type})`;
                            this.outputs[index].name = `out_${index + 1} (${otherSlot.type})`;
                        }
                    } else {
                        // Reset to wildcard type when disconnected
                        this.inputs[index].type = "*";
                        this.outputs[index].type = "*";
                        this.inputs[index].name = `value_${index + 1}`;
                        this.outputs[index].name = `out_${index + 1}`;
                    }
                }
                
                // Update node size
                this.size = this.computeSize();
                app.graph.setDirtyCanvas(true, true);
            };

            // Save/load the number of connections
            nodeType.prototype.onSerialize = function(o) {
                o.inputcount = this.widgets.find(w => w.name === "inputcount").value;
            };

            nodeType.prototype.onConfigure = function(o) {
                if (o.inputcount !== undefined) {
                    this.widgets.find(w => w.name === "inputcount").value = o.inputcount;
                }
                this.updateConnections();
            };

            // Handle cloning
            const onCloned = nodeType.prototype.onCloned;
            nodeType.prototype.onCloned = function(original) {
                onCloned?.apply(this, arguments);
                this.widgets.find(w => w.name === "inputcount").value = original.widgets.find(w => w.name === "inputcount").value;
                this.updateConnections();
            };
        }
    }
});
