import { app } from "../../../scripts/app.js";

let remainingIterations = 0;
let isRunning = false;

app.registerExtension({
    name: "Klinter.QueueCounter",
    async setup() {
        // Create container
        const container = document.createElement("div");
        container.className = "comfy-queue-counter";
        container.style.cssText = "display: flex; gap: 5px; align-items: center; margin: 6px 0;";

        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            .comfy-queue-counter {
                display: flex;
                gap: 5px;
                align-items: center;
                margin: 6px 0;
            }
            .comfy-queue-counter input {
                color: var(--input-text);
                background-color: var(--comfy-input-bg);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                width: 60px;
                padding: 2px 4px;
                font-size: inherit;
            }
            .comfy-queue-counter button {
                color: var(--input-text);
                background-color: var(--comfy-input-bg);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 2px 8px;
                cursor: pointer;
                font-size: inherit;
            }
            .comfy-queue-counter button:hover:not(:disabled) {
                filter: brightness(1.2);
            }
            .comfy-queue-counter button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
        `;
        document.head.appendChild(style);

        // Add label
        const label = document.createElement("span");
        label.innerText = "Auto Runs:";
        label.style.color = "var(--descrip-text)";
        container.appendChild(label);

        // Add input
        const input = document.createElement("input");
        input.type = "number";
        input.min = "0";
        input.value = "0";
        input.addEventListener("change", (e) => {
            remainingIterations = parseInt(e.target.value);
        });
        container.appendChild(input);

        // Add start button
        const startButton = document.createElement("button");
        startButton.innerText = "Start Auto Run";
        startButton.onclick = () => {
            if (remainingIterations > 0 && !isRunning) {
                isRunning = true;
                startButton.disabled = true;
                input.disabled = true;
                app.queuePrompt();
                startMonitoring();
            }
        };
        container.appendChild(startButton);

        // Add stop button
        const stopButton = document.createElement("button");
        stopButton.innerText = "Stop";
        stopButton.onclick = () => {
            isRunning = false;
            startButton.disabled = false;
            input.disabled = false;
            remainingIterations = parseInt(input.value);
        };
        container.appendChild(stopButton);

        // Add to queue controls - try different selectors until we find the right spot
        function addToInterface() {
            // Try to find the queue controls
            const queueButtons = document.querySelector(".comfy-menu-btns");
            if (queueButtons) {
                queueButtons.parentElement.insertBefore(container, queueButtons.nextSibling);
                console.log("Added queue counter to interface");
                return true;
            }
            return false;
        }

        // Keep trying to add the interface until we succeed
        function tryAddInterface() {
            if (!addToInterface()) {
                console.log("Queue controls not found, retrying...");
                setTimeout(tryAddInterface, 1000);
            }
        }
        tryAddInterface();

        function startMonitoring() {
            const checkQueueStatus = async () => {
                if (!isRunning) return;

                try {
                    const status = await app.api.getQueueStatus();
                    if (status.exec_info.queue_remaining === 0) {
                        remainingIterations--;
                        input.value = remainingIterations;

                        if (remainingIterations > 0) {
                            // Small delay to ensure clean state
                            setTimeout(() => {
                                if (isRunning) {
                                    app.queuePrompt();
                                    checkQueueStatus();
                                }
                            }, 100);
                        } else {
                            // All done
                            isRunning = false;
                            startButton.disabled = false;
                            input.disabled = false;
                        }
                    } else {
                        // Keep checking while queue is running
                        setTimeout(checkQueueStatus, 500);
                    }
                } catch (error) {
                    console.error("Error checking queue status:", error);
                    // On error, stop the auto-run
                    isRunning = false;
                    startButton.disabled = false;
                    input.disabled = false;
                }
            };

            checkQueueStatus();
        }
    }
});
