import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "KlinterNodes.nodevalue2string",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "nodevalue2string") {
            return;
        }

        const orig_onNodeCreated = nodeType.prototype.onNodeCreated;

        // Add dynamic input handling
        nodeType.prototype.onNodeCreated = function() {
            if (orig_onNodeCreated) {
                orig_onNodeCreated.apply(this, arguments);
            }

            // Add update button
            this.addWidget("button", "Update inputs", null, () => {
                const target_inputs = this.widgets.find(w => w.name === "inputcount")?.value || 2;
                
                // Remove existing value inputs beyond target
                for (let i = this.inputs.length - 1; i >= 0; i--) {
                    const input = this.inputs[i];
                    if (input.name.startsWith("value_") && parseInt(input.name.split("_")[1]) > target_inputs) {
                        this.removeInput(i);
                    }
                }
                
                // Add new inputs up to target
                for (let i = 1; i <= target_inputs; i++) {
                    const inputName = `value_${i}`;
                    if (!this.inputs.find(input => input.name === inputName)) {
                        this.addInput(inputName, ["STRING", "INT", "FLOAT"]);
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

        // Override the connection handling
        const orig_onConnectionsChange = nodeType.prototype.onConnectionsChange;
        nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
            if (orig_onConnectionsChange) {
                orig_onConnectionsChange.apply(this, arguments);
            }

            if (type === LiteGraph.INPUT && connected && link_info) {
                const input = this.inputs[index];
                if (input && input.name.startsWith("value_")) {
                    const sourceNode = app.graph.getNodeById(link_info.origin_id);
                    if (sourceNode) {
                        // Get the node's title or type
                        const nodeName = sourceNode.title || sourceNode.type;
                        
                        // Rename the input to match the connected node
                        input.name = nodeName;
                        
                        // Force a graph change to update the UI
                        app.graph.setDirtyCanvas(true);
                    }
                }
            }
        };
    }
});
