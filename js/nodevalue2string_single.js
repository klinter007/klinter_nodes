import { app } from "../../../scripts/app.js";
import { KlinterUtils } from "./klinter_utils.js";

app.registerExtension({
    name: "KlinterNodes.nodevalue2string",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "nodevalue2string") {
            return;
        }

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
