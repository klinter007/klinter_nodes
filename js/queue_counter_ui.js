import { app } from "../../../scripts/app.js";

console.log("Queue Counter UI: Script Loaded");

app.registerExtension({
    name: "Klinter.QueueCounterUI",
    async setup(app) {
        console.log("Queue Counter UI: Setup Started");

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
            padding: 2px 8px;
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
        iterationInput.max = '1000';
        iterationInput.value = '1';
        iterationInput.style.cssText = `
            width: 60px;
            background: #252525;
            border: 1px solid #505050;
            color: white;
            padding: 5px;
            border-radius: 3px;
        `;
        iterationInput.classList.add('queue-counter-iterations');
        container.appendChild(iterationInput);

        // Create status display
        const statusDisplay = document.createElement('div');
        statusDisplay.textContent = 'Ready';
        statusDisplay.style.cssText = `
            flex-grow: 1;
            text-align: center;
            font-size: 14px;
        `;
        statusDisplay.classList.add('queue-counter-status');
        container.appendChild(statusDisplay);

        // Create action button
        const actionButton = document.createElement('button');
        actionButton.textContent = 'Start';
        actionButton.style.cssText = `
            background: #454545;
            border: 1px solid #505050;
            color: white;
            padding: 5px 15px;
            border-radius: 3px;
            cursor: pointer;
        `;
        actionButton.classList.add('queue-counter-action');
        container.appendChild(actionButton);

        // Action button click handler
        actionButton.addEventListener('click', () => {
            // Check if ui object has the necessary methods
            if (ui && ui.actionButton && ui.iterationInput) {
                // Toggle between start and stop
                if (actionButton.textContent === 'Start') {
                    actionButton.textContent = 'Stop';
                    actionButton.style.backgroundColor = '#ff4136';  // Red
                    ui.iterationInput.disabled = true;
                } else {
                    actionButton.textContent = 'Start';
                    actionButton.style.backgroundColor = '#454545';  // Gray
                    ui.iterationInput.disabled = false;
                }
            }
        });

        // Make container draggable
        let isDragging = false;
        let currentX;
        let currentY;
        let initialX;
        let initialY;
        let xOffset = 0;
        let yOffset = 0;

        titleElement.addEventListener('mousedown', dragStart);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', dragEnd);

        function dragStart(e) {
            initialX = e.clientX - xOffset;
            initialY = e.clientY - yOffset;

            if (e.target === titleElement) {
                isDragging = true;
            }
        }

        function drag(e) {
            if (isDragging) {
                e.preventDefault();
                
                currentX = e.clientX - initialX;
                currentY = e.clientY - initialY;

                xOffset = currentX;
                yOffset = currentY;

                setTranslate(currentX, currentY, container);
            }
        }

        function dragEnd(e) {
            initialX = currentX;
            initialY = currentY;

            isDragging = false;
        }

        function setTranslate(xPos, yPos, el) {
            el.style.transform = `translate3d(${xPos}px, ${yPos}px, 0)`;
        }

        // Add container to document
        document.body.appendChild(container);

        // Hide container by default
        container.style.display = 'none';

        // Create UI object to expose
        const ui = {
            container,
            iterationInput,
            statusDisplay,
            actionButton,
            updateRunDisplay(currentRun, totalRuns, chosenRuns) {
                const statusDisplay = container.querySelector('.queue-counter-status');
                const actionButton = container.querySelector('.queue-counter-action');
                const iterationInput = container.querySelector('.queue-counter-iterations');

                // Update status text to show current run progress relative to chosen runs
                statusDisplay.textContent = `Completed ${currentRun}/${chosenRuns} runs`;

                // When all runs are complete, reset button and input
                if (currentRun >= chosenRuns) {
                    actionButton.textContent = 'Start';
                    actionButton.style.backgroundColor = '#2ecc40';  // Green
                    iterationInput.disabled = false;
                }
            }
        };

        // Add configuration settings
        app.ui.settings.addSetting({
            id: "klinter.queueCounter.enabled",
            name: "Instant Queue Limiter Widget",
            type: "boolean",
            defaultValue: true,
            onChange: (value) => {
                container.style.display = value ? 'flex' : 'none';
            }
        });

        // Expose UI globally for logic component
        window.queueCounterUI = ui;

        console.log("Queue Counter UI: Setup Complete", ui);
    }
});

console.log("Queue Counter UI: Script Processed");
