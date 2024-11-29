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

                    // Safer event handling
                    const setupEventListeners = () => {
                        console.log('Queue Counter Logic: Setting up event listeners');
                        
                        // Use window-based event listening if app.addEventListener fails
                        try {
                            const completionEvents = [
                                'prompt_queue_complete', 
                                'prompt_queue_end', 
                                'execution_end'
                            ];

                            completionEvents.forEach(eventName => {
                                // Try multiple methods of event attachment
                                if (app && typeof app.addEventListener === 'function') {
                                    app.addEventListener(eventName, () => {
                                        console.log(`Queue Counter Logic: Event ${eventName} via app`);
                                        if (this.isRunning && !this.wasInterrupted) {
                                            this.triggerNextRun();
                                        }
                                    });
                                } else {
                                    // Fallback to window event
                                    window.addEventListener(eventName, () => {
                                        console.log(`Queue Counter Logic: Event ${eventName} via window`);
                                        if (this.isRunning && !this.wasInterrupted) {
                                            this.triggerNextRun();
                                        }
                                    });
                                }
                            });
                        } catch (error) {
                            console.error('Queue Counter Logic: Error setting up event listeners', error);
                        }
                    };

                    // Call setup immediately and also defer it
                    setupEventListeners();
                    setTimeout(setupEventListeners, 1000);

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

                    // Monitor queue status via WebSocket
                    const originalOnMessage = api.socket.onmessage;
                    api.socket.onmessage = (event) => {
                        // Call original handler first
                        if (originalOnMessage) {
                            originalOnMessage(event);
                        }

                        // Handle only text messages, ignore ArrayBuffer
                        if (!(event.data instanceof ArrayBuffer)) {
                            try {
                                const parsedData = JSON.parse(event.data);
                                
                                if (parsedData.type === 'status') {
                                    const queueRemaining = parsedData.data?.status?.exec_info?.queue_remaining;
                                    const executionStatus = parsedData.data?.status?.exec_info?.status;
                                    
                                    console.log('Queue Counter Logic: Queue Status Update', { 
                                        queueRemaining,
                                        executionStatus,
                                        currentRun: this.currentRun,
                                        totalRuns: this.totalRuns,
                                        isRunning: this.isRunning
                                    });

                                    if (this.isRunning) {
                                        // Comprehensive completion check
                                        const isComplete = (
                                            queueRemaining === 0 || 
                                            executionStatus === 'complete' || 
                                            executionStatus === 'finished'
                                        );
                                        
                                        if (isComplete) {
                                            console.log('Queue Counter Logic: Run completed, preparing next run');
                                            
                                            if (this.currentRun < this.totalRuns) {
                                                console.log('Queue Counter Logic: Triggering next run');
                                                // Robust next run trigger
                                                setTimeout(() => {
                                                    if (this.isRunning && !this.wasInterrupted) {
                                                        this.triggerNextRun();
                                                    }
                                                }, 250);  // Increased delay for stability
                                            } else {
                                                console.log('Queue Counter Logic: All runs completed');
                                                this.stop(false);
                                            }
                                        }
                                    }
                                }
                            } catch (e) {
                                console.error('Queue Counter Logic: Error parsing WebSocket message', e);
                            }
                        }
                    };

                    this.queueNextPrompt = () => {
                        app.queuePrompt(0, 1);
                    };
                }

                start() {
                    // Reset run counter
                    this.currentRun = 0;
                    this.isRunning = true;
                    this.wasInterrupted = false;

                    // Set total runs from UI input
                    this.totalRuns = Math.max(1, Math.min(
                        parseInt(this.ui.iterationInput.value, 10), 
                        255
                    ));

                    // Update UI initial state to 0
                    if (this.ui && this.ui.updateRunDisplay) {
                        this.ui.updateRunDisplay(0, this.totalRuns, this.totalRuns);
                    }

                    // Initial prompt queue
                    if (this.queueNextPrompt) {
                        this.queueNextPrompt();
                    }

                    // Monitor WebSocket for completion
                    const originalOnMessage = api.socket.onmessage;
                    api.socket.onmessage = (event) => {
                        // Call original handler first
                        if (originalOnMessage) {
                            originalOnMessage(event);
                        }

                        // Handle only text messages
                        if (!(event.data instanceof ArrayBuffer)) {
                            try {
                                const parsedData = JSON.parse(event.data);
                                
                                // Check for workflow completion
                                if (
                                    this.isRunning && 
                                    (parsedData.type === 'execution_success' || 
                                     (parsedData.type === 'status' && 
                                      parsedData.data?.status?.exec_info?.queue_remaining === 0))
                                ) {
                                    console.log('Queue Counter Logic: Workflow Completed', {
                                        currentRun: this.currentRun,
                                        totalRuns: this.totalRuns
                                    });

                                    // Trigger next run if needed
                                    if (this.currentRun < this.totalRuns) {
                                        setTimeout(() => {
                                            this.triggerNextRun();
                                        }, 100);
                                    } else {
                                        this.stop(false);
                                    }
                                }
                            } catch (error) {
                                console.error('Queue Counter Logic: WebSocket Message Error', error);
                            }
                        }
                    };
                }

                triggerNextRun() {
                    console.log('Queue Counter Logic: Triggering Next Run', {
                        currentRun: this.currentRun,
                        totalRuns: this.totalRuns,
                        isRunning: this.isRunning
                    });

                    if (this.isRunning && this.currentRun < this.totalRuns) {
                        // Increment current run
                        this.currentRun++;
                        
                        // Update UI
                        if (this.ui && this.ui.updateRunDisplay) {
                            this.ui.updateRunDisplay(this.currentRun, this.totalRuns, this.totalRuns);
                        }

                        // Queue next prompt
                        if (this.queueNextPrompt) {
                            this.queueNextPrompt();
                        }

                        // If this was the last run, stop
                        if (this.currentRun >= this.totalRuns) {
                            this.stop(false);
                        }
                    }
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
