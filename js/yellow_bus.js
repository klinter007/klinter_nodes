import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "YellowBusV2",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "YellowBus") {
            nodeType.prototype.onNodeCreated = function() {
                this.addWidget("button", "Update inputs", null, () => {
                    if (!this.inputs) {
                        this.inputs = [];
                    }
                    const target_number_of_inputs = this.widgets.find(w => w.name === "inputcount")["value"];
                    if(target_number_of_inputs === this.inputs.length) return; // already set, do nothing

                    if(target_number_of_inputs < this.inputs.length) {
                        // Remove excess inputs and outputs
                        for(let i = this.inputs.length-1; i >= target_number_of_inputs; i--) {
                            this.removeInput(i);
                            this.removeOutput(i);
                        }
                    } else {
                        // Add new inputs and outputs
                        for(let i = this.inputs.length; i < target_number_of_inputs; i++) {
                            this.addInput(`value_${i+1}`, "*");  // Wildcard type
                            this.addOutput(`out_${i+1}`, "*");   // Wildcard type
                        }
                    }
                });

                // Call update once on creation
                setTimeout(() => {
                    const widget = this.widgets.find(w => w.name === "Update inputs");
                    if (widget) {
                        widget.callback();
                    }
                }, 100);
            }

            // Handle dynamic type adaptation with proper checks
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                // Only handle input connections
                if (type !== LiteGraph.INPUT) return;
                
                // Handle disconnection
                if (!connected) {
                    if (this.inputs && this.inputs[index]) {
                        this.inputs[index].type = "*";
                    }
                    if (this.outputs && this.outputs[index]) {
                        this.outputs[index].type = "*";
                    }
                    return;
                }
                
                // Handle connection with proper checks
                if (!link_info) return;
                const otherNode = this.graph?._nodes_by_id?.[link_info.origin_id];
                if (!otherNode?.outputs?.[link_info.origin_slot]) return;
                
                const otherType = otherNode.outputs[link_info.origin_slot].type;
                if (!otherType) return;

                // Update both input and corresponding output to match connected type
                if (this.inputs?.[index]) {
                    this.inputs[index].type = otherType;
                }
                if (this.outputs?.[index]) {
                    this.outputs[index].type = otherType;
                }
            }
        }
    }
});
