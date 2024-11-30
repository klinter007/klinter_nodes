import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

console.log("Queue Counter Extension: Script Loaded");

app.registerExtension({
    name: "Klinter.QueueCounter",
    async setup(app) {
        console.log("Queue Counter Extension: Setup Started");

        // Create container for queue counter
        const container = document.createElement('div');
        container.id = 'klinter-queue-counter';
        container.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 10px;
            border-radius: 5px;
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 10px;
            min-width: 300px;
        `;

        // Create input for iterations
        const iterationInput = document.createElement('input');
        iterationInput.type = 'number';
        iterationInput.min = '1';
        iterationInput.max = '100';
        iterationInput.value = '1';
        iterationInput.style.width = '50px';
        iterationInput.style.marginRight = '10px';
        iterationInput.placeholder = 'Runs';

        // Create button
        const actionButton = document.createElement('button');
        actionButton.textContent = 'Auto Run';
        actionButton.style.padding = '5px 10px';
        actionButton.style.backgroundColor = 'white';
        actionButton.style.color = 'black';
        actionButton.style.border = 'none';
        actionButton.style.borderRadius = '3px';

        // Create status display
        const statusDisplay = document.createElement('div');
        statusDisplay.textContent = '';
        statusDisplay.style.marginLeft = '10px';
        statusDisplay.style.flex = '1';

        // Append elements to container
        container.appendChild(iterationInput);
        container.appendChild(actionButton);
        container.appendChild(statusDisplay);

        // Function to add container to body
        const addContainerToBody = () => {
            console.log("Queue Counter: Attempting to add container to body");
            if (document.body) {
                document.body.appendChild(container);
                console.log("Queue Counter: Container added to body");
            } else {
                console.error("Queue Counter: document.body not available");
                // Retry after a short delay
                setTimeout(addContainerToBody, 1000);
            }
        };

        // Try to add container immediately and set up a fallback
        addContainerToBody();

        // Queue management class
        class QueueManager {
            constructor() {
                this.totalRuns = 1;
                this.currentRun = 0;
                this.isRunning = false;
                this.wasInterrupted = false;
            }

            start() {
                if (this.isRunning) return;

                this.totalRuns = Math.max(1, Math.min(parseInt(iterationInput.value, 10), 100));
                this.currentRun = 0;
                this.isRunning = true;
                this.wasInterrupted = false;

                this.updateUI();
                this.triggerNextRun();
            }

            triggerNextRun() {
                if (this.wasInterrupted) {
                    this.stop();
                    return;
                }

                if (this.currentRun >= this.totalRuns) {
                    this.stop();
                    return;
                }

                this.currentRun++;
                app.queuePrompt(0, 1);
                this.updateUI();
            }

            stop(interrupted = false) {
                this.isRunning = false;
                this.wasInterrupted = interrupted;
                this.updateUI();
            }

            updateUI() {
                if (this.isRunning) {
                    actionButton.textContent = `Running (${this.currentRun}/${this.totalRuns})`;
                    actionButton.style.backgroundColor = 'yellow';
                    actionButton.style.color = 'black';
                    statusDisplay.textContent = `Run ${this.currentRun} in progress`;
                } else {
                    actionButton.textContent = 'Auto Run';
                    actionButton.style.backgroundColor = this.wasInterrupted ? 'red' : 'white';
                    actionButton.style.color = this.wasInterrupted ? 'white' : 'black';
                    statusDisplay.textContent = this.wasInterrupted 
                        ? 'Workflow Interrupted' 
                        : `Completed ${this.currentRun} runs`;
                }
            }
        }

        const queueManager = new QueueManager();

        // Hijack API interrupt method
        const originalApiInterrupt = api.interrupt;
        api.interrupt = function() {
            // Call original interrupt method
            originalApiInterrupt.apply(this, arguments);
            
            // If queue manager is running, mark as interrupted
            if (queueManager.isRunning) {
                queueManager.stop(true);
            }
        };

        // Add event listener to button
        actionButton.addEventListener('click', () => {
            console.log("Queue Counter: Button clicked");
            if (!queueManager.isRunning) {
                queueManager.start();
            } else {
                queueManager.stop(true);
            }
        });

        // Listen for queue completion
        const completionEvents = [
            'prompt_queue_complete', 
            'prompt_queue_end', 
            'execution_end'
        ];

        completionEvents.forEach(eventName => {
            app.addEventListener(eventName, () => {
                if (queueManager.isRunning && !queueManager.wasInterrupted) {
                    queueManager.triggerNextRun();
                }
            });
        });

        console.log("Queue Counter Extension: Setup Complete");
    }
});

// Ensure the script is loaded
console.log("Queue Counter Extension: Script Processed");
