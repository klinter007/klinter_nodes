import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "KlinterNodes.nodevalue2stringmulti",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "nodevalue2stringmulti") {
            return;
        }

        const orig_onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function() {
            if (orig_onNodeCreated) {
                orig_onNodeCreated.apply(this, arguments);
            }

            // Add update button
            this.addWidget("button", "Update inputs", null, () => {
                const target_inputs = this.widgets.find(w => w.name === "inputcount")?.value || 2;
                const current_input_count = this.inputs.length;
                
                // Calculate how many new inputs we need
                const inputs_to_add = target_inputs - current_input_count;
                
                if (inputs_to_add > 0) {
                    // Add new inputs
                    for (let i = 0; i < inputs_to_add; i++) {
                        const inputName = `value_${current_input_count + i + 1}`;
                        this.addInput(inputName, ["STRING", "INT", "FLOAT"], {
                            // Add a custom property to track the connected node name
                            connectedNodeName: "Not Connected"
                        });
                    }
                } else if (inputs_to_add < 0) {
                    // Remove excess inputs from the end
                    for (let i = 0; i < -inputs_to_add; i++) {
                        this.removeInput(this.inputs.length - 1);
                    }
                }
            });

            // Initial setup
            setTimeout(() => {
                const widget = this.widgets.find(w => w.name === "Update inputs");
                if (widget) {
                    widget.callback();
                }
            }, 100);
        };

        // Override connections change to update input names
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
