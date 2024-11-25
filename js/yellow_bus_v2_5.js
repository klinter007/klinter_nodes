import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "YellowBusV2_5",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "YellowBusV2_5") {
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
                            this.addInput(`input_${i+1}`, "empty");
                            this.addOutput(`out_${i+1}`, "*");
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

            // Handle dynamic type adaptation
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                // Only handle input connections
                if (type !== LiteGraph.INPUT) return;
                
                // Handle disconnection
                if (!connected || !link_info) {
                    if (this.inputs?.[index]) {
                        this.inputs[index].type = "empty";
                    }
                    return;
                }
                
                // Handle connection with proper checks
                const otherNode = this.graph?._nodes_by_id?.[link_info.origin_id];
                const otherOutput = otherNode?.outputs?.[link_info.origin_slot];
                if (!otherOutput?.type) return;
                
                // Update input to match connected type
                if (this.inputs?.[index]) {
                    this.inputs[index].type = otherOutput.type;
                }
            }
        }
    }
});
