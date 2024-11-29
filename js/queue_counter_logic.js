import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

console.log("Queue Counter Logic: Script Loaded");

app.registerExtension({
    name: "Klinter.QueueCounterLogic",
    async setup() {
        console.log("Queue Counter Logic: Setup Started");

        // Ensure UI is loaded
        const checkUI = () => {
            if (!window.queueCounterUI) {
                console.log("Queue Counter Logic: Waiting for UI");
                setTimeout(checkUI, 100);
                return;
            }

            const ui = window.queueCounterUI;
            console.log("Queue Counter Logic: UI Found");

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

                    // Bind event listeners
                    this.ui.actionButton.addEventListener('click', () => {
                        console.log("Queue Counter Logic: Button clicked");
                        if (!this.isRunning) {
                            this.start();
                        } else {
                            this.stop(true);
                        }
                    });

                    // Monitor queue status via WebSocket
                    const originalOnMessage = api.socket.onmessage;
                    api.socket.onmessage = (event) => {
                        // Call original handler
                        if (originalOnMessage) {
                            originalOnMessage(event);
                        }

                        // Handle only text messages, ignore ArrayBuffer
                        if (!(event.data instanceof ArrayBuffer)) {
                            try {
                                const parsedData = JSON.parse(event.data);
                                
                                if (parsedData.type === 'status') {
                                    const queueRemaining = parsedData.data?.status?.exec_info?.queue_remaining;
                                    
                                    console.log('Queue Counter Logic: Queue Status Update', { 
                                        queueRemaining,
                                        lastQueueStatus: this.lastQueueStatus,
                                        currentRun: this.currentRun,
                                        totalRuns: this.totalRuns,
                                        isRunning: this.isRunning
                                    });

                                    if (this.isRunning) {
                                        // Queue transition from having items to empty indicates completion
                                        const runCompleted = this.lastQueueStatus > 0 && queueRemaining === 0;
                                        
                                        if (runCompleted) {
                                            console.log('Queue Counter Logic: Run completed, preparing next run');
                                            this.ui.statusDisplay.textContent = `Run ${this.currentRun} completed`;
                                            
                                            if (this.currentRun < this.totalRuns) {
                                                console.log('Queue Counter Logic: Triggering next run');
                                                // Give a small delay before next run
                                                setTimeout(() => {
                                                    if (this.isRunning) {  // Double check we're still running
                                                        this.triggerNextRun();
                                                    }
                                                }, 500);
                                            } else {
                                                console.log('Queue Counter Logic: All runs completed');
                                                this.stop(false);
                                            }
                                        } else if (queueRemaining > 0) {
                                            this.ui.statusDisplay.textContent = `Run ${this.currentRun} in progress`;
                                        }
                                    }
                                    
                                    this.lastQueueStatus = queueRemaining;
                                }
                            } catch (e) {
                                console.log('Queue Counter Logic: Error parsing message', e);
                            }
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
                        this.stop();
                        return;
                    }

                    if (this.currentRun >= this.totalRuns) {
                        console.log("Queue Counter Logic: All runs completed");
                        this.stop();
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
                    console.log("Queue Counter Logic: Updating UI");
                    if (this.isRunning) {
                        this.ui.actionButton.textContent = `Running (${this.currentRun}/${this.totalRuns})`;
                        this.ui.actionButton.style.backgroundColor = 'yellow';
                        this.ui.actionButton.style.color = 'black';
                        this.ui.statusDisplay.textContent = `Run ${this.currentRun} in progress`;
                    } else {
                        this.ui.actionButton.textContent = 'Auto Run';
                        this.ui.actionButton.style.backgroundColor = this.wasInterrupted ? 'red' : 'white';
                        this.ui.actionButton.style.color = this.wasInterrupted ? 'white' : 'black';
                        this.ui.statusDisplay.textContent = this.wasInterrupted 
                            ? 'Workflow Interrupted' 
                            : `Completed ${this.currentRun} runs`;
                    }
                }
            }

            // Create queue manager instance
            window.queueManager = new QueueManager(ui);
            console.log("Queue Counter Logic: Setup Complete");
        };

        checkUI();
    }
});

console.log("Queue Counter Logic: Script Processed");
