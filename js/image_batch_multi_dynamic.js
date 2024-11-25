import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "ImageBatchMultiDynamic",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "ImageBatchMultiDynamic") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                onNodeCreated?.apply(this, arguments);
                this.updateConnections();
            };

            // Update connections when inputcount changes
            nodeType.prototype.onWidgetChange = function(name, value) {
                if (name === "inputcount") {
                    this.updateConnections();
                }
            };

            nodeType.prototype.updateConnections = function() {
                const inputcount = this.widgets.find(w => w.name === "inputcount").value;
                
                // Remove excess inputs
                while (this.inputs.length > inputcount) {
                    this.removeInput(this.inputs.length - 1);
                }
                
                // Add new inputs
                while (this.inputs.length < inputcount) {
                    const index = this.inputs.length + 1;
                    this.addInput(`image_${index}`, "IMAGE");
                }
                
                // Update node size
                this.size = this.computeSize();
                app.graph.setDirtyCanvas(true, true);
            };
        }
    }
});
