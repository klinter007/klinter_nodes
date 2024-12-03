// Klinter Nodes Utility Functions

const KlinterUtils = {
    /**
     * Add dynamic inputs to a node
     * @param {Object} node - The node to modify
     * @param {string} inputPrefix - Prefix for input names (e.g., 'value_')
     * @param {number} currentInputCount - Current number of inputs
     * @param {number} targetInputCount - Desired number of inputs
     * @param {Array} inputTypes - Types of inputs to add
     */
    addDynamicInputs: function(node, inputPrefix, currentInputCount, targetInputCount, inputTypes = ["*"]) {
        const inputsToAdd = targetInputCount - currentInputCount;
        
        if (inputsToAdd > 0) {
            // Add new inputs
            for (let i = 0; i < inputsToAdd; i++) {
                const inputName = `${inputPrefix}${currentInputCount + i + 1}`;
                node.addInput(inputName, inputTypes, {
                    connectedNodeName: "Not Connected"
                });
            }
        } else if (inputsToAdd < 0) {
            // Remove excess inputs from the end
            for (let i = 0; i < -inputsToAdd; i++) {
                node.removeInput(node.inputs.length - 1);
            }
        }
    },

    /**
     * Update input labels based on connected nodes
     * @param {Object} node - The node to modify
     * @param {number} index - Index of the input
     * @param {boolean} connected - Whether the input is connected
     * @param {Object} linkInfo - Information about the connection
     */
    updateInputLabel: function(node, index, connected, linkInfo) {
        if (connected && linkInfo) {
            const sourceNode = (typeof app !== 'undefined' && app.graph) ? app.graph.getNodeById(linkInfo.origin_id) : null;
            
            if (sourceNode) {
                // Prefer title, fallback to type
                const nodeName = sourceNode.title || sourceNode.type || `Node_${sourceNode.id}`;
                
                // Update the input's name to show the connected node
                node.inputs[index].label = nodeName;
                
                // Store the node name as a custom property
                node.inputs[index].connectedNodeName = nodeName;
            }
        } else {
            // Reset input label when disconnected
            node.inputs[index].label = null;
            node.inputs[index].connectedNodeName = "Not Connected";
        }

        // Force graph to redraw
        if (node.graph) {
            node.graph.setDirtyCanvas(true);
        }
    }
};

// Make the utility available globally if needed
window.KlinterUtils = KlinterUtils;

export { KlinterUtils };
