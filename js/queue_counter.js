import { app } from "../../../scripts/app.js";

let remainingIterations = 0;
let isRunning = false;

app.registerExtension({
    name: "Klinter.QueueCounter",
    async setup() {
        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            .comfy-queue-counter {
                background: var(--comfy-input-bg);
                border-radius: 4px;
                padding: 4px 8px;
            }
            .comfy-queue-counter-label {
                color: var(--comfy-input-text);
            }
            .comfy-queue-counter-input {
                background: var(--comfy-input-bg);
                color: var(--comfy-input-text);
                border: 1px solid var(--comfy-input-border);
                border-radius: 4px;
                padding: 2px 4px;
            }
            .comfy-queue-counter-button {
                background: var(--comfy-input-bg);
                color: var(--comfy-input-text);
                border: 1px solid var(--comfy-input-border);
                border-radius: 4px;
                padding: 2px 8px;
                cursor: pointer;
            }
            .comfy-queue-counter-button:hover {
                background: var(--comfy-input-hover);
            }
            .comfy-queue-counter-button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
        `;
        document.head.appendChild(style);

        // Create container
        const container = document.createElement("div");
        container.className = "comfy-queue-counter";
        container.style.display = "flex";
        container.style.alignItems = "center";
        container.style.marginRight = "10px";

        // Add label
        const label = document.createElement("span");
        label.className = "comfy-queue-counter-label";
        label.innerText = "Auto Runs: ";
        label.style.marginRight = "5px";
        container.appendChild(label);

        // Add input
        const input = document.createElement("input");
        input.className = "comfy-queue-counter-input";
        input.type = "number";
        input.min = "0";
        input.value = "0";
        input.style.width = "60px";
        input.addEventListener("change", (e) => {
            remainingIterations = parseInt(e.target.value);
        });
        container.appendChild(input);

        // Add start button
        const startButton = document.createElement("button");
        startButton.className = "comfy-queue-counter-button";
        startButton.innerText = "Start Auto Run";
        startButton.style.marginLeft = "5px";
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
        stopButton.className = "comfy-queue-counter-button";
        stopButton.innerText = "Stop";
        stopButton.style.marginLeft = "5px";
        stopButton.onclick = () => {
            isRunning = false;
            startButton.disabled = false;
            input.disabled = false;
            remainingIterations = parseInt(input.value);
        };
        container.appendChild(stopButton);

        // Add to queue controls
        const queueControls = document.querySelector(".queue-controls");
        if (queueControls) {
            queueControls.insertBefore(container, queueControls.firstChild);
        }

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
