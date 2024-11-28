import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

let remainingIterations = 0;
let isRunning = false;

app.registerExtension({
    name: "Klinter.QueueCounter",
    async setup() {
        // Wait for queue button to be available
        const queueButton = await new Promise((resolve) => {
            const findQueueButton = () => {
                const btn = document.querySelector('#queue-button');
                if (btn) {
                    resolve(btn);
                } else {
                    setTimeout(findQueueButton, 100);
                }
            };
            findQueueButton();
        });

        // Create container with ComfyUI styling
        const container = document.createElement("div");
        container.className = "comfy-queue-counter comfy-menu-btns";
        container.style.cssText = "display: flex; gap: 5px; align-items: center; margin: 6px 0;";

        // Add styles that match ComfyUI
        const style = document.createElement('style');
        style.textContent = `
            .comfy-queue-counter {
                display: flex;
                gap: 5px;
                align-items: center;
                margin: 6px 0;
                padding: 0 10px;
            }
            .comfy-queue-counter input {
                width: 60px;
                color: var(--input-text);
                background-color: var(--comfy-input-bg);
                border: 1px solid var(--border-color);
                border-radius: 4px;
                padding: 2px 4px;
            }
            .comfy-queue-counter button {
                color: var(--input-text);
                background-color: var(--comfy-input-bg);
                border: 1px solid var(--border-color);
                border-radius: 4px;
                padding: 4px 8px;
                cursor: pointer;
                transition: background-color 0.2s;
            }
            .comfy-queue-counter button:hover {
                background-color: var(--comfy-input-bg-hover);
            }
            .comfy-queue-counter button:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
        `;
        document.head.appendChild(style);

        // Create input for iterations
        const input = document.createElement("input");
        input.type = "number";
        input.min = "1";
        input.value = "1";
        input.title = "Number of times to run the queue";

        // Create start button
        const startButton = document.createElement("button");
        startButton.textContent = "Start Auto Run";
        startButton.title = "Start automatic queue processing";

        // Create stop button
        const stopButton = document.createElement("button");
        stopButton.textContent = "Stop";
        stopButton.title = "Stop automatic queue processing";
        stopButton.disabled = true;

        // Add elements to container
        container.appendChild(input);
        container.appendChild(startButton);
        container.appendChild(stopButton);

        // Insert after queue button
        queueButton.parentElement.insertBefore(container, queueButton.nextSibling);

        // Queue monitoring function
        async function checkQueue() {
            if (!isRunning) return;
            
            try {
                const status = await app.api.getQueueStatus();
                if (status.exec_info.queue_remaining === 0) {
                    if (remainingIterations > 0) {
                        remainingIterations--;
                        if (remainingIterations === 0) {
                            stopAutoRun();
                            return;
                        }
                        app.queuePrompt();
                    }
                }
                setTimeout(checkQueue, 1000);
            } catch (error) {
                console.error("Error checking queue:", error);
                stopAutoRun();
            }
        }

        // Start auto run function
        function startAutoRun() {
            const iterations = parseInt(input.value);
            if (iterations < 1) return;

            remainingIterations = iterations - 1; // -1 because first run is immediate
            isRunning = true;
            
            input.disabled = true;
            startButton.disabled = true;
            stopButton.disabled = false;

            // First run uses instant queue
            app.queuePrompt();
            checkQueue();
        }

        // Stop auto run function
        function stopAutoRun() {
            isRunning = false;
            remainingIterations = 0;
            
            input.disabled = false;
            startButton.disabled = false;
            stopButton.disabled = true;
        }

        // Add event listeners
        startButton.addEventListener("click", startAutoRun);
        stopButton.addEventListener("click", stopAutoRun);
    }
});
