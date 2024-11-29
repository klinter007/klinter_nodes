import { app } from "../../../scripts/app.js";

console.log("Queue Counter UI: Script Loaded");

app.registerExtension({
    name: "Klinter.QueueCounterUI",
    async setup(app) {
        console.log("Queue Counter UI: Setup Started");

        // Add configuration settings
        app.ui.settings.addSetting({
            id: "klinter.queueCounter.enabled",
            name: "Instant Queue Limiter Widget",
            type: "boolean",
            defaultValue: false,
            onChange: (value) => {
                // Update widget visibility based on settings
                const container = document.getElementById('klinter-queue-counter');
                if (container) {
                    container.style.display = value ? 'flex' : 'none';
                }
            }
        });

        // Create main container for queue counter
        const container = document.createElement('div');
        container.id = 'klinter-queue-counter';
        container.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #353535;
            color: white;
            padding: 10px;
            border-radius: 5px;
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 10px;
            min-width: 300px;
            border: 1px solid #505050;
        `;

        // Create title
        const titleElement = document.createElement('div');
        titleElement.textContent = 'Instant Queue Limiter';
        titleElement.style.cssText = `
            position: absolute;
            top: -20px;
            left: 0;
            background-color: #353535;
            color: white;
            padding: 2px 5px;
            border-radius: 3px 3px 0 0;
            font-size: 12px;
            border: 1px solid #505050;
            border-bottom: none;
            cursor: move;
            user-select: none;
        `;
        container.appendChild(titleElement);

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
        actionButton.textContent = 'Start';
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

        // Draggable functionality
        let isDragging = false;
        let currentX;
        let currentY;
        let initialX;
        let initialY;
        let xOffset = 0;
        let yOffset = 0;

        // Prevent text selection during drag
        titleElement.addEventListener('selectstart', (e) => e.preventDefault());

        // Attach event listeners for dragging
        titleElement.addEventListener('mousedown', (e) => {
            e.preventDefault(); // Prevent default to stop text selection
            initialX = e.clientX - xOffset;
            initialY = e.clientY - yOffset;
            isDragging = true;
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;

            e.preventDefault();
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;

            xOffset = currentX;
            yOffset = currentY;

            container.style.transform = `translate3d(${currentX}px, ${currentY}px, 0)`;
        });

        document.addEventListener('mouseup', () => {
            isDragging = false;
        });

        // Function to add container to body
        const addContainerToBody = () => {
            if (document.body) {
                document.body.appendChild(container);
            } else {
                setTimeout(addContainerToBody, 1000);
            }
        };

        // Try to add container immediately
        addContainerToBody();

        // Multi-run logic
        const logic = new window.QueueCounterLogic();

        actionButton.addEventListener('click', () => {
            // If currently running, stop the process
            if (logic.isRunning) {
                logic.cancelMultiRun();
                actionButton.textContent = 'Start';
                statusDisplay.textContent = 'Runs stopped.';
                iterationInput.disabled = false;
                return;
            }

            // Start multi-run process
            const runCount = parseInt(iterationInput.value, 10);
            
            if (runCount < 1 || runCount > 100) {
                statusDisplay.textContent = 'Invalid run count. Must be between 1-100.';
                return;
            }

            // Disable input during runs
            iterationInput.disabled = true;

            // Change button to Stop
            actionButton.textContent = 'Stop';

            statusDisplay.textContent = `Starting ${runCount} runs...`;

            logic.startMultiRun(
                runCount,
                (currentRun, totalRuns) => {
                    const remainingRuns = totalRuns - currentRun;
                    statusDisplay.textContent = `Completed run ${currentRun}/${totalRuns} (${remainingRuns} left)`;
                },
                () => {
                    // Runs completed
                    statusDisplay.textContent = 'All runs completed!';
                    actionButton.textContent = 'Start';
                    iterationInput.disabled = false;
                },
                () => {
                    // Runs stopped
                    statusDisplay.textContent = 'Runs stopped.';
                    actionButton.textContent = 'Start';
                    iterationInput.disabled = false;
                }
            );
        });

        console.log("Queue Counter UI: Setup Complete");
    }
});

console.log("Queue Counter UI: Script Processed");
