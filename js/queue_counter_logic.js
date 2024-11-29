import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

console.log("Queue Counter Logic: Script Loaded");

app.registerExtension({
    name: "Klinter.QueueCounterLogic",
    init() {
        console.log("Queue Counter Logic: Initialization Started");
        
        // Try to catch ComfyUI API events
        try {
            if (window.comfyAPI && window.comfyAPI.api) {
                console.log("Queue Counter Logic: Attempting to add ComfyUI API event listeners");
                
                window.comfyAPI.api.addEventListener('execution_success', (event) => {
                    console.log("ComfyUI API: Execution Success Event", event);
                });
                
                window.comfyAPI.api.addEventListener('execution_start', (event) => {
                    console.log("ComfyUI API: Execution Start Event", event);
                });
                
                window.comfyAPI.api.addEventListener('execution_error', (event) => {
                    console.error("ComfyUI API: Execution Error Event", event);
                });
            } else {
                console.warn("Queue Counter Logic: comfyAPI not found during initialization");
            }
        } catch (error) {
            console.error("Queue Counter Logic: Error setting up ComfyUI API listeners", error);
        }
    },
    setup() {
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
                    this.queuedPrompts = 0;
                    this.completedPrompts = 0;
                    this.activePromptIds = new Set();

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

                    // Additional event listeners for comprehensive tracking
                    this.setupAdditionalEventListeners();
                }

                setupAdditionalEventListeners() {
                    // Try to add listeners to multiple event systems
                    const events = [
                        'prompt_queue_complete', 
                        'prompt_queue_end', 
                        'execution_end',
                        'execution_success'
                    ];

                    // ComfyUI app events
                    events.forEach(eventName => {
                        app.on(eventName, (event) => {
                            console.log(`Queue Counter Logic: ComfyUI App Event - ${eventName}`, event);
                            this.handleQueueProgress(eventName, event);
                        });
                    });

                    // ComfyUI API events
                    if (window.comfyAPI && window.comfyAPI.api) {
                        ['execution_success', 'execution_start', 'execution_error'].forEach(eventName => {
                            window.comfyAPI.api.addEventListener(eventName, (event) => {
                                console.log(`Queue Counter Logic: ComfyUI API Event - ${eventName}`, event);
                                this.handleQueueProgress(eventName, event);
                            });
                        });
                    }
                }

                handleQueueProgress(eventName, event) {
                    console.log(`Queue Counter Logic: Handling Queue Progress for ${eventName}`);
                    
                    // Track completed prompts
                    if (eventName === 'execution_success') {
                        // Extract prompt ID from the event
                        const promptId = event?.detail?.prompt_id;
                        
                        if (promptId && this.activePromptIds.has(promptId)) {
                            this.completedPrompts++;
                            this.activePromptIds.delete(promptId);
                            
                            console.log(`Queue Counter Logic: Completed Prompts: ${this.completedPrompts}/${this.queuedPrompts}`);
                        }
                    }

                    // Trigger next run if all conditions are met
                    if (this.isRunning && 
                        !this.wasInterrupted && 
                        this.completedPrompts >= this.currentRun) {
                        console.log(`Queue Counter Logic: Triggering next run after ${eventName}`);
                        this.triggerNextRun();
                    }
                }

                start() {
                    console.log("Queue Counter Logic: Start method called");
                    if (this.isRunning) {
                        console.log("Queue Counter Logic: Already running, ignoring start");
                        return;
                    }

                    this.totalRuns = Math.max(1, Math.min(
                        parseInt(this.ui.iterationInput.value, 10), 
                        100
                    ));
                    this.currentRun = 0;
                    this.isRunning = true;
                    this.wasInterrupted = false;
                    this.queuedPrompts = 0;
                    this.completedPrompts = 0;
                    this.activePromptIds.clear();

                    console.log(`Queue Counter Logic: Starting ${this.totalRuns} runs`);

                    this.updateUI();
                    this.triggerNextRun();
                }

                triggerNextRun() {
                    console.log("Queue Counter Logic: triggerNextRun method called");
                    
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
                    this.queuedPrompts++;
                    
                    console.log(`Queue Counter Logic: Triggering run ${this.currentRun}/${this.totalRuns}`);

                    // Ensure prompt is queued with a slight delay
                    setTimeout(() => {
                        try {
                            console.log("Queue Counter Logic: Calling app.queuePrompt(0, 1)");
                            const promptPromise = app.queuePrompt(0, 1);
                            
                            // Handle the Promise returned by queuePrompt
                            promptPromise.then((result) => {
                                console.log("Queue Counter Logic: Prompt Queued Result", result);
                                
                                // If result contains a prompt_id, track it
                                if (result?.prompt_id) {
                                    this.activePromptIds.add(result.prompt_id);
                                    console.log(`Queue Counter Logic: Added Active Prompt ID: ${result.prompt_id}`);
                                }
                            }).catch((error) => {
                                console.error("Queue Counter Logic: Prompt Queuing Error", error);
                                this.stop(true);
                            });
                        } catch (error) {
                            console.error("Queue Counter Logic: Queue Prompt Error", error);
                            this.stop(true);
                        }
                    }, 100);  // Small delay to prevent race conditions

                    this.updateUI();
                }

                stop(interrupted = false) {
                    console.log(`Queue Counter Logic: Stop method called (Interrupted: ${interrupted})`);
                    this.isRunning = false;
                    this.wasInterrupted = interrupted;
                    this.updateUI();

                    // Reset counters
                    this.queuedPrompts = 0;
                    this.completedPrompts = 0;
                    this.activePromptIds.clear();
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

            class QueueCounterLogic {
                constructor() {
                    this.totalRuns = 0;
                    this.currentRun = 0;
                    this.isRunning = false;
                    this.stopRequested = false;
                }

                log(message) {
                    // Use ComfyUI's WebSocket API to send a log message
                    if (window.comfyAPI && window.comfyAPI.api && window.comfyAPI.api.socket) {
                        window.comfyAPI.api.socket.send(JSON.stringify({
                            type: 'instant_queue_limiter_log',
                            data: {
                                message: `Instant Queue Limiter: ${message}`
                            }
                        }));
                    }
                }

                startMultiRun(runs, progressCallback, completionCallback, stopCallback) {
                    // Reset state
                    this.totalRuns = runs;
                    this.currentRun = 0;
                    this.isRunning = true;
                    this.stopRequested = false;

                    this.log(`Starting ${runs} runs`);

                    // Start the multi-run process
                    this.runWorkflow(progressCallback, completionCallback, stopCallback);
                }

                runWorkflow(progressCallback, completionCallback, stopCallback) {
                    // Check if we should stop
                    if (this.stopRequested) {
                        this.log('Job stopped');
                        this.isRunning = false;
                        stopCallback && stopCallback();
                        return;
                    }

                    // Check if we've completed all runs
                    if (this.currentRun >= this.totalRuns) {
                        this.log('All done');
                        this.isRunning = false;
                        completionCallback && completionCallback();
                        return;
                    }

                    // Increment current run
                    this.currentRun++;

                    // Trigger queue
                    const queueButton = document.querySelector('.comfy-queue-btn');
                    if (queueButton) {
                        queueButton.click();
                    }

                    // Update progress
                    progressCallback && progressCallback(this.currentRun, this.totalRuns);

                    // Wait and check for next run
                    this.waitForWorkflowCompletion(() => {
                        const remainingRuns = this.totalRuns - this.currentRun;
                        this.log(`Only ${remainingRuns} times left`);

                        // Schedule next run if not stopped
                        if (!this.stopRequested) {
                            this.runWorkflow(progressCallback, completionCallback, stopCallback);
                        } else {
                            this.log('Job stopped');
                            this.isRunning = false;
                            stopCallback && stopCallback();
                        }
                    });
                }

                waitForWorkflowCompletion(callback) {
                    const checkCompletion = () => {
                        const queueRemainingElement = document.querySelector('.queue-remaining');
                        
                        if (queueRemainingElement && queueRemainingElement.textContent === '0') {
                            callback();
                        } else if (this.stopRequested) {
                            // Interrupt if stop is requested
                            const interruptButton = document.querySelector('.comfy-interrupt-btn');
                            if (interruptButton && !interruptButton.disabled) {
                                interruptButton.click();
                            }
                            callback();
                        } else {
                            // Check again in a moment
                            setTimeout(checkCompletion, 500);
                        }
                    };

                    checkCompletion();
                }

                cancelMultiRun() {
                    // Request stop
                    this.stopRequested = true;

                    this.log('Job stopped');

                    // Interrupt current queue if possible
                    const interruptButton = document.querySelector('.comfy-interrupt-btn');
                    if (interruptButton && !interruptButton.disabled) {
                        interruptButton.click();
                    }
                }
            }

            // Export to global window object
            window.QueueCounterLogic = QueueCounterLogic;

            // Hijack API interrupt method
            const originalApiInterrupt = api.interrupt;
            api.interrupt = function() {
                console.log("Queue Counter Logic: API Interrupt called");
                // Call original interrupt method
                originalApiInterrupt.apply(this, arguments);
                
                // If queue manager is running, mark as interrupted
                if (window.queueManager && window.queueManager.isRunning) {
                    console.log("Queue Counter Logic: Stopping due to interrupt");
                    window.queueManager.stop(true);
                }
            };

            // Create queue manager and attach to window for global access
            window.queueManager = new QueueManager(ui);

            console.log("Queue Counter Logic: Setup Complete");
        };

        // Start checking for UI
        checkUI();
    }
});

console.log("Queue Counter Logic: Script Processed");
