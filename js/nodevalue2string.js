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
                        this.addInput(inputName, ["STRING", "INT"]);
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

        // Function to get node display name
        function getNodeDisplayName(node) {
            // First try to get the title (user-set name)
            if (node.title && node.title !== node.type) {
                return node.title;
            }
            
            // Then try to get the display name from NODE_DISPLAY_NAME_MAPPINGS
            const displayName = app.graph._nodes_by_id[node.id]?.displayName;
            if (displayName) {
                return displayName;
            }
            
            // Finally fallback to node type
            return node.type;
        }

        // Override the original getExtraMenuOptions
        const orig_getExtraMenuOptions = nodeType.prototype.getExtraMenuOptions;
        nodeType.prototype.getExtraMenuOptions = function(_, options) {
            if (orig_getExtraMenuOptions) {
                orig_getExtraMenuOptions.apply(this, arguments);
            }

            // Add a menu option to update the template with connected node names
            options.unshift({
                content: "Update with node names",
                callback: () => {
                    // Get the template widget
                    const templateWidget = this.widgets.find(w => w.name === "template");
                    if (!templateWidget) return;

                    // For each input, get the connected node's name
                    this.inputs.forEach((input, idx) => {
                        if (input.link !== null) {
                            const link = app.graph.links[input.link];
                            if (link) {
                                const sourceNode = app.graph.getNodeById(link.origin_id);
                                if (sourceNode) {
                                    // Replace the placeholder with actual node name
                                    const placeholder = `{node_${idx + 1}}`;
                                    const nodeName = getNodeDisplayName(sourceNode);
                                    templateWidget.value = templateWidget.value.replace(
                                        placeholder,
                                        nodeName
                                    );
                                }
                            }
                        }
                    });
                }
            });
        };
    }
});
