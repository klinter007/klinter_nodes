import { app } from "../../../scripts/app.js";
import { KlinterUtils } from "./klinter_utils.js";

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
                
                // Use KlinterUtils to add dynamic inputs
                KlinterUtils.addDynamicInputs(
                    this, 
                    "value_", 
                    current_input_count, 
                    target_inputs, 
                    ["STRING", "INT", "FLOAT"]
                );
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
                KlinterUtils.updateInputLabel(this, index, connected, link_info);
            }
        };
    }
});
