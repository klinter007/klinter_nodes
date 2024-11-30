import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "KlinterNodes.string_contact_multi",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "string_contact_multi") {
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
                
                // Remove existing string inputs beyond target
                for (let i = this.inputs.length - 1; i >= 0; i--) {
                    const input = this.inputs[i];
                    if (input.name.startsWith("string_") && parseInt(input.name.split("_")[1]) > target_inputs) {
                        this.removeInput(i);
                    }
                }
                
                // Add new inputs up to target
                for (let i = 1; i <= target_inputs; i++) {
                    const inputName = `string_${i}`;
                    if (!this.inputs.find(input => input.name === inputName)) {
                        this.addInput(inputName, "STRING");
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
    }
});
