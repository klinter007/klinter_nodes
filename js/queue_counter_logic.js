import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

console.log("Queue Counter Logic: Script Loaded");

app.registerExtension({
    name: "Klinter.QueueCounterLogic",
    async setup() {
        console.log("Queue Counter Logic: Setup Started");

        // Wait for UI to be ready
        const waitForUI = () => {
            return new Promise((resolve) => {
                const checkUI = () => {
                    if (window.queueCounterUI) {
                        console.log("Queue Counter Logic: UI Found");
                        resolve(window.queueCounterUI);
                    } else {
                        console.log("Queue Counter Logic: Waiting for UI");
                        setTimeout(checkUI, 100);
                    }
                };
                checkUI();
            });
        };

        try {
            const ui = await waitForUI();
            console.log("Queue Counter Logic: Initializing with UI", ui);

            // Queue management class
            class QueueManager {
                constructor(ui) {
                    this.ui = ui;
                    this.totalRuns = 1;
                    this.currentRun = 0;
                    this.isRunning = false;
                    this.wasInterrupted = false;
                    this.lastQueueStatus = 0;

                    console.log("Queue Counter Logic: QueueManager initialized");

                    // Add event listener to button
                    this.ui.actionButton.addEventListener('click', () => {
                        console.log("Queue Counter Logic: Button clicked");
                        if (!this.isRunning) {
                            this.start();
                        } else {
                            this.stop(true);
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
                            console.log(`Queue Counter Logic: Event ${eventName}`);
                            if (this.isRunning && !this.wasInterrupted) {
                                this.triggerNextRun();
                            }
                        });
                    });

                    // Hijack API interrupt method
                    const originalApiInterrupt = api.interrupt;
                    api.interrupt = () => {
                        // Call original interrupt method
                        originalApiInterrupt.apply(api);
                        
                        // If queue manager is running, mark as interrupted
                        if (this.isRunning) {
                            console.log("Queue Counter Logic: Workflow interrupted");
                            this.stop(true);
                        }
                    };
                }

                start() {
                    console.log("Queue Counter Logic: Start method called");
                    if (this.isRunning) {
                        console.log("Queue Counter Logic: Already running, ignoring start");
                        return;
                    }

                    this.totalRuns = Math.max(1, Math.min(
                        parseInt(this.ui.iterationInput.value, 10), 
                        255
                    ));
                    this.currentRun = 0;
                    this.lastQueueStatus = 0;
                    this.isRunning = true;
                    this.wasInterrupted = false;

                    console.log(`Queue Counter Logic: Starting ${this.totalRuns} runs`);
                    this.updateUI();
                    this.triggerNextRun();
                }

                triggerNextRun() {
                    console.log("Queue Counter Logic: triggerNextRun method called", {
                        currentRun: this.currentRun,
                        totalRuns: this.totalRuns,
                        isRunning: this.isRunning,
                        wasInterrupted: this.wasInterrupted
                    });
                    
                    if (this.wasInterrupted) {
                        console.log("Queue Counter Logic: Workflow was interrupted");
                        this.stop(true);
                        return;
                    }

                    if (this.currentRun >= this.totalRuns) {
                        console.log("Queue Counter Logic: All runs completed");
                        this.stop(false);
                        return;
                    }

                    this.currentRun++;
                    console.log(`Queue Counter Logic: Triggering run ${this.currentRun}/${this.totalRuns}`);
                    
                    // Reset queue status before new run
                    this.lastQueueStatus = 0;
                    
                    // Queue the prompt
                    app.queuePrompt(0, 1);
                    this.updateUI();
                }

                stop(interrupted = false) {
                    console.log("Queue Counter Logic: Stop method called");
                    this.isRunning = false;
                    this.wasInterrupted = interrupted;
                    this.updateUI();
                }

                updateUI() {
                    this.ui.updateUI(
                        this.isRunning,
                        this.currentRun,
                        this.totalRuns,
                        this.wasInterrupted
                    );
                }
            }

            // Create queue manager instance
            window.queueManager = new QueueManager(ui);
            console.log("Queue Counter Logic: Setup Complete");
        } catch (e) {
            console.log("Queue Counter Logic: Error during setup", e);
        }
    }
});

console.log("Queue Counter Logic: Script Processed");
