import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "YellowBus",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "YellowBus") {
            // Initialize node with update button
            nodeType.prototype.onNodeCreated = function() {
                this.addWidget("button", "Update Pairs", null, () => {
                    if (!this.inputs) {
                        this.inputs = [];
                    }
                    const target_pairs = this.widgets.find(w => w.name === "pairs")["value"];
                    if(target_pairs === this.inputs.length) return; // already set, do nothing

                    if(target_pairs < this.inputs.length) {
                        // Remove excess inputs and outputs
                        for(let i = this.inputs.length-1; i >= target_pairs; i--) {
                            this.removeInput(i);
                            this.removeOutput(i);
                        }
                    } else {
                        // Add new inputs and outputs
                        for(let i = this.inputs.length; i < target_pairs; i++) {
                            this.addInput(`input_${i+1}`, "*");  // Use wildcard type
                            this.addOutput(`out_${i+1}`, "*");   // Use wildcard type
                        }
                    }
                });

                // Call update once on creation
                setTimeout(() => {
                    const widget = this.widgets.find(w => w.name === "Update Pairs");
                    if (widget) {
                        widget.callback();
                    }
                }, 100);
            }

            // Force a node refresh with proper type updates
            function refreshNode(node) {
                // Trigger multiple refresh methods
                if (node.graph) {
                    node.graph.change();  // Notify graph of changes
                }
                node.setDirtyCanvas(true, true);  // Mark canvas as dirty
                
                // Force size recalculation
                if (typeof node.computeSize === "function") {
                    const size = node.computeSize();
                    node.size = size;
                    node.onResize?.(size);
                }

                // Schedule another refresh
                setTimeout(() => {
                    node.setDirtyCanvas(true, true);
                }, 10);
            }

            // Handle dynamic type adaptation and refresh display
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                // Only handle input connections
                if (type !== LiteGraph.INPUT) return;
                
                // Handle disconnection
                if (!connected || !link_info) {
                    if (this.inputs?.[index]) {
                        this.inputs[index].type = "*";  // Reset to wildcard type
                        this.inputs[index].name = `input_${index + 1}`;  // Reset name
                        if (this.outputs?.[index]) {
                            this.outputs[index].name = `out_${index + 1}`;  // Reset output name
                        }
                    }
                    refreshNode(this);
                    return;
                }
                
                // Handle connection with proper checks
                const otherNode = this.graph?._nodes_by_id?.[link_info.origin_id];
                const otherOutput = otherNode?.outputs?.[link_info.origin_slot];
                if (!otherOutput?.type) return;
                
                // Update input type and display
                if (this.inputs?.[index]) {
                    const type = otherOutput.type;
                    this.inputs[index].type = type;
                    this.inputs[index].name = `input_${index + 1} (${type})`;
                    
                    // Update corresponding output
                    if (this.outputs?.[index]) {
                        this.outputs[index].type = type;  // Match input type
                        this.outputs[index].name = `out_${index + 1} (${type})`;
                    }
                }

                // Force refresh display
                refreshNode(this);
            }
        }
    }
});
