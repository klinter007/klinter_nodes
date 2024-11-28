import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Klinter.QueueCounter",
    async setup() {
        // Wait for app.ui to be available
        const waitForUI = () => {
            return new Promise((resolve) => {
                const check = () => {
                    if (app.ui && app.ui.menuContainer) {
                        resolve();
                    } else {
                        setTimeout(check, 100);
                    }
                };
                check();
            });
        };

        await waitForUI();

        // Create our button group
        const queueCounterGroup = document.createElement("div");
        queueCounterGroup.className = "comfy-menu-btns";
        
        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            .queue-counter-input {
                width: 60px;
                color: var(--input-text);
                background-color: var(--comfy-input-bg);
                border: 1px solid var(--border-color);
                border-radius: 4px;
                padding: 2px 4px;
                margin: 0 5px;
            }
        `;
        document.head.appendChild(style);

        // Create input
        const input = document.createElement("input");
        input.type = "number";
        input.min = "1";
        input.value = "1";
        input.className = "queue-counter-input";
        input.title = "Number of times to run the queue";

        // Create buttons using ComfyUI's button style
        const startButton = document.createElement("button");
        startButton.textContent = "Auto Run";
        startButton.className = "comfy-button";
        startButton.title = "Start automatic queue processing";

        const stopButton = document.createElement("button");
        stopButton.textContent = "Stop";
        stopButton.className = "comfy-button";
        stopButton.title = "Stop automatic queue processing";
        stopButton.disabled = true;

        // Add elements to group
        queueCounterGroup.appendChild(input);
        queueCounterGroup.appendChild(startButton);
        queueCounterGroup.appendChild(stopButton);

        // Add group to menu
        const queueButton = app.ui.menuContainer.querySelector('#queue-button');
        if (queueButton && queueButton.parentElement) {
            queueButton.parentElement.insertBefore(queueCounterGroup, queueButton.nextSibling);
        } else {
            // Fallback - add to menu container
            app.ui.menuContainer.appendChild(queueCounterGroup);
        }

        // Tracking variables
        let remainingIterations = 0;
        let isRunning = false;

        // Create a counter display
        const counterDisplay = document.createElement("span");
        counterDisplay.textContent = "Remaining Iterations: 0";
        counterDisplay.style.position = "fixed";
        counterDisplay.style.bottom = "40px";
        counterDisplay.style.right = "10px";
        counterDisplay.style.zIndex = "1000";
        document.body.appendChild(counterDisplay);

        // Queue monitoring function
        async function checkQueue() {
            if (!isRunning) return;
            
            try {
                const status = await app.api.getQueueStatus();
                if (status.exec_info.queue_remaining === 0) {
                    if (remainingIterations > 0) {
                        remainingIterations--;
                        counterDisplay.textContent = `Remaining Iterations: ${remainingIterations}`;
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
            counterDisplay.textContent = `Remaining Iterations: ${remainingIterations + 1}`;
            isRunning = true;
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
            counterDisplay.textContent = "Remaining Iterations: 0";
            startButton.disabled = false;
            stopButton.disabled = true;
        }

        // Add event listeners
        startButton.addEventListener("click", () => startAutoRun());
        stopButton.addEventListener("click", stopAutoRun);

        // Attach to ComfyUI's WebSocket
        const originalWebSocket = window.WebSocket;
        window.WebSocket = class extends originalWebSocket {
            constructor(url, protocols) {
                super(url, protocols);
                this.addEventListener('message', (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        this.handleWebSocketEvent(data);
                    } catch (e) {
                        console.error('WebSocket message parsing error', e);
                    }
                });
            }

            handleWebSocketEvent(data) {
                // Handle different WebSocket events
                if (data.type === 'status') {
                    this.updateQueueStatus(data.status);
                } else if (data.type === 'executing') {
                    this.checkQueueCompletion();
                }
            }

            async updateQueueStatus(status) {
                // Update queue status from WebSocket
                if (isRunning) {
                    const pendingQueue = status.queue_pending || [];
                    const runningQueue = status.queue_running || [];
                    
                    if (pendingQueue.length === 0 && runningQueue.length === 0) {
                        await this.processNextIteration();
                    }
                }
            }

            async checkQueueCompletion() {
                // Additional check for queue completion
                if (isRunning) {
                    const queueResponse = await fetch('/queue');
                    const queueData = await queueResponse.json();
                    
                    if (queueData.queue_pending.length === 0 && queueData.queue_running.length === 0) {
                        await this.processNextIteration();
                    }
                }
            }

            async processNextIteration() {
                remainingIterations--;
                counterDisplay.textContent = `Remaining Iterations: ${remainingIterations}`;

                if (remainingIterations > 0) {
                    await this.triggerQueueRun();
                } else {
                    stopAutoRun();
                }
            }

            async triggerQueueRun() {
                try {
                    const response = await fetch('/prompt', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            prompt: app.graph.serialize(),
                            client_id: app.clientId
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error('Failed to trigger queue run');
                    }
                } catch (error) {
                    console.error('Queue run error:', error);
                    stopAutoRun();
                }
            }
        };

        // Log for debugging
        console.log("Queue Counter extension initialized");
    }
});
