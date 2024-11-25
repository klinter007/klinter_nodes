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
        }
    }
});
