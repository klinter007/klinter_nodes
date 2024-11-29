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
        iterationInput.max = '255';
        iterationInput.value = '1';
        iterationInput.style.cssText = `
            width: 60px;
            background: #252525;
            border: 1px solid #505050;
            color: white;
            padding: 5px;
            border-radius: 3px;
        `;
        container.appendChild(iterationInput);

        // Create status display
        const statusDisplay = document.createElement('div');
        statusDisplay.textContent = 'Ready';
        statusDisplay.style.cssText = `
            flex-grow: 1;
            text-align: center;
            font-size: 14px;
        `;
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
        container.appendChild(actionButton);

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
            updateUI(isRunning, currentRun, totalRuns, wasInterrupted) {
                if (isRunning) {
                    actionButton.textContent = `Running (${currentRun}/${totalRuns})`;
                    actionButton.style.backgroundColor = 'yellow';
                    actionButton.style.color = 'black';
                    statusDisplay.textContent = `Run ${currentRun} in progress`;
                } else {
                    actionButton.textContent = 'Start';
                    actionButton.style.backgroundColor = wasInterrupted ? 'red' : '#454545';
                    actionButton.style.color = wasInterrupted ? 'white' : 'white';
                    statusDisplay.textContent = wasInterrupted 
                        ? 'Workflow Interrupted' 
                        : currentRun > 0 ? `Completed ${currentRun} runs` : 'Ready';
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
