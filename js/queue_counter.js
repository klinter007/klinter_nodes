import { app } from "../../../scripts/app.js";

class QueueCounter {
    constructor() {
        this.iterationsRemaining = 0;
        this.isRunning = false;
        this.createUI();
        this.setupWebSocket();
    }

    createUI() {
        this.container = document.createElement('div');
        this.container.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 10px;
            border-radius: 5px;
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 10px;
        `;

        this.iterationInput = document.createElement('input');
        this.iterationInput.type = 'number';
        this.iterationInput.min = '1';
        this.iterationInput.value = '1';
        this.iterationInput.placeholder = 'Iterations';
        this.iterationInput.style.width = '70px';

        this.counterDisplay = document.createElement('div');
        this.counterDisplay.textContent = '0';

        this.actionButton = document.createElement('button');
        this.actionButton.textContent = 'Test Auto Run';
        this.actionButton.onclick = () => this.toggleAutoRun();

        this.container.appendChild(this.iterationInput);
        this.container.appendChild(this.counterDisplay);
        this.container.appendChild(this.actionButton);

        document.body.appendChild(this.container);
    }

    setupWebSocket() {
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
        };
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
        if (this.isRunning) {
            const pendingQueue = status.queue_pending || [];
            const runningQueue = status.queue_running || [];
            
            if (pendingQueue.length === 0 && runningQueue.length === 0) {
                await this.processNextIteration();
            }
        }
    }

    async checkQueueCompletion() {
        // Additional check for queue completion
        if (this.isRunning) {
            const queueResponse = await fetch('/queue');
            const queueData = await queueResponse.json();
            
            if (queueData.queue_pending.length === 0 && queueData.queue_running.length === 0) {
                await this.processNextIteration();
            }
        }
    }

    async processNextIteration() {
        this.iterationsRemaining--;
        this.updateCounterDisplay();

        if (this.iterationsRemaining > 0) {
            await this.triggerQueueRun();
        } else {
            this.stopAutoRun();
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
            this.stopAutoRun();
        }
    }

    toggleAutoRun() {
        if (!this.isRunning) {
            this.startAutoRun();
        } else {
            this.stopAutoRun();
        }
    }

    startAutoRun() {
        this.iterationsRemaining = parseInt(this.iterationInput.value, 10);
        if (this.iterationsRemaining > 0) {
            this.isRunning = true;
            this.actionButton.textContent = 'Stop Auto Run';
            this.triggerQueueRun();
            this.updateCounterDisplay();
        }
    }

    stopAutoRun() {
        this.isRunning = false;
        this.actionButton.textContent = 'Test Auto Run';
        this.iterationsRemaining = 0;
        this.updateCounterDisplay();
    }

    updateCounterDisplay() {
        this.counterDisplay.textContent = this.iterationsRemaining.toString();
    }
}

// Initialize QueueCounter when ComfyUI loads
if (window.app && window.app.ui) {
    new QueueCounter();
} else {
    document.addEventListener('comfyui:loaded', () => {
        new QueueCounter();
    });
}
