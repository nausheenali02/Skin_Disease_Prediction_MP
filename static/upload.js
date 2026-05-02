// upload.js

// Show uploaded image preview
function previewImage(event) {
    const preview = document.getElementById("preview");
    const file = event.target.files[0];
    const uploadBox = document.querySelector(".upload-box");

    if (file) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";

        // HIDE upload box after image is uploaded
        uploadBox.style.display = "none";

        // Reset the result box if a new image is selected
        document.getElementById("resultBox").style.display = "none";
        document.getElementById("resultText").innerText = "";
    }
}

// Send the image to the Flask backend
async function analyzePrediction() {
    const resultBox = document.getElementById("resultBox");
    const resultText = document.getElementById("resultText");
    const fileInput = document.getElementById("fileInput");

    if (fileInput.files.length === 0) {
        alert("Please upload an image first.");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
        // Show loading state
        resultBox.style.display = "block";
        resultText.innerHTML = "<em>Analyzing image... please wait.</em>";

        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // Success: Update the UI with prediction
        resultText.innerHTML = `
            <strong>DIAGNOSIS: ${data.prediction.toUpperCase()}</strong> <br>
            <strong>CONFIDENCE: ${data.confidence}%</strong>
        `;
        
        console.log("Full Probabilities:", data.probabilities);

    } catch (error) {
        console.error("Error:", error);
        resultText.innerHTML = "<span style='color: red;'>An error occurred. Make sure your Flask backend is running!</span>";
    }
}