import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

// Add support for video uploads
app.registerExtension({
	name: "Klinter.VideoUpload",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "LoadVideoForExtendingKlinter") {
			// Add video upload widget
			const onNodeCreated = nodeType.prototype.onNodeCreated;
			nodeType.prototype.onNodeCreated = function () {
				const r = onNodeCreated?.apply(this, arguments);

				// Add a text widget to show the selected file
				const valueWidget = this.addWidget(
					"text",
					"video",
					"",
					(name) => {
						// When the value changes, trigger the node update
						this.setDirtyCanvas(true);
						this.serialize_widgets = true;
					},
					{ serialize: true }
				);

				// Add the upload button
				const uploadWidget = this.addWidget(
					"button",
					"upload_video",
					"Upload Video",
					async () => {
						// Create file input
						const input = document.createElement("input");
						input.type = "file";
						input.accept = "video/mp4,video/mov,video/avi,video/mkv";
						input.style.display = "none";
						document.body.appendChild(input);

						// Handle file selection
						input.onchange = async () => {
							const file = input.files[0];
							if (!file) {
								document.body.removeChild(input);
								return;
							}

							try {
								// Upload the file
								const formData = new FormData();
								formData.append("image", file); // ComfyUI uses "image" for all uploads
								const resp = await api.fetchApi("/upload/image", {
									method: "POST",
									body: formData,
								});

								if (resp.status === 200) {
									const data = await resp.json();
									// Update the value widget with the uploaded file name
									valueWidget.value = data.name;
									// Force widget update
									this.setDirtyCanvas(true);
									app.graph.setDirtyCanvas(true);
								} else {
									alert("Failed to upload video file");
								}
							} catch (error) {
								alert("Error uploading video file: " + error.message);
							}

							// Clean up
							document.body.removeChild(input);
						};

						// Trigger file selection
						input.click();
					}
				);

				return r;
			};
		}
	},
});
