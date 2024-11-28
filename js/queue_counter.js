import { app } from "../../../scripts/app.js";

let remainingIterations = 0;
let isRunning = false;

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

        // Create a standalone button for testing
        const testButton = document.createElement("button");
        testButton.textContent = "Test Auto Run";
        testButton.style.position = "fixed";
        testButton.style.bottom = "10px";
        testButton.style.right = "10px";
        testButton.style.zIndex = "1000";
        document.body.appendChild(testButton);

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
        function startAutoRun(iterations) {
            if (iterations === undefined) {
                const iterations = parseInt(input.value);
                if (iterations < 1) return;
            }

            remainingIterations = iterations - 1; // -1 because first run is immediate
            isRunning = true;
            
            if (input) {
                input.disabled = true;
                startButton.disabled = true;
                stopButton.disabled = false;
            }

            // First run uses instant queue
            app.queuePrompt();
            checkQueue();
        }

        // Stop auto run function
        function stopAutoRun() {
            isRunning = false;
            remainingIterations = 0;
            
            if (input) {
                input.disabled = false;
                startButton.disabled = false;
                stopButton.disabled = true;
            }
        }

        // Add event listeners
        startButton.addEventListener("click", () => startAutoRun());
        stopButton.addEventListener("click", stopAutoRun);

        // Add event listener to the test button
        testButton.addEventListener("click", () => {
            if (isRunning) {
                stopAutoRun();
                testButton.textContent = "Test Auto Run";
            } else {
                startAutoRun(5); // Example iteration count
                testButton.textContent = "Stop Auto Run";
            }
        });

        // Log for debugging
        console.log("Queue Counter extension initialized");
    }
});
