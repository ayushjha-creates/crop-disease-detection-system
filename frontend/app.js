// frontend/app.js
document.addEventListener("DOMContentLoaded", () => {

const API_BASE_URL = "http://127.0.0.1:8030";

const imageInput = document.getElementById("imageInput");
const predictBtn = document.getElementById("predictBtn");
const imagePreview = document.getElementById("imagePreview");

const resultSection = document.getElementById("resultSection");
const feedbackSection = document.getElementById("feedbackSection");

const cropNameEl = document.getElementById("cropName");
const diseaseNameEl = document.getElementById("diseaseName");
const confidenceScoreEl = document.getElementById("confidenceScore");

const descEl = document.getElementById("desc");
const symptomsEl = document.getElementById("symptoms");
const organicEl = document.getElementById("organic");
const chemicalEl = document.getElementById("chemical");
const preventiveEl = document.getElementById("preventive");

const feedbackSelect = document.getElementById("feedbackSelect");
const correctLabelInput = document.getElementById("correctLabelInput");
const submitFeedbackBtn = document.getElementById("submitFeedbackBtn");
const feedbackMessage = document.getElementById("feedbackMessage");

let lastPrediction = null;

// Preview selected image
imageInput.addEventListener("change", () => {
  const file = imageInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.src = e.target.result;
    };
    reader.readAsDataURL(file);
  } else {
    imagePreview.src = "";
  }
});

predictBtn.addEventListener("click", async () => {
  const file = imageInput.files[0];
  if (!file) {
    alert("Please select an image first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Prediction failed");
    }

    const data = await response.json();
    console.log("Backend response:", data);


    lastPrediction = data;
  
    cropNameEl.textContent = data.crop_name;
    diseaseNameEl.textContent = data.disease_name;
    confidenceScoreEl.textContent =
      (data.confidence * 100).toFixed(2) + "%";
    
    // ✅ Recommendations
    if (data.recommendation) {
      descEl.textContent = data.recommendation.disease_description || "-";
      symptomsEl.textContent = data.recommendation.symptoms || "-";
      organicEl.textContent = data.recommendation.treatment_organic || "-";
      chemicalEl.textContent = data.recommendation.treatment_chemical || "-";
      preventiveEl.textContent = data.recommendation.preventive_measures || "-";
    }
    
    symptomsEl.textContent =
      data.recommendation.symptoms;
    organicEl.textContent =
      data.recommendation.treatment_organic;
    chemicalEl.textContent =
      data.recommendation.treatment_chemical;
    preventiveEl.textContent =
      data.recommendation.preventive_measures;
    
    resultSection.style.display = "block";
    feedbackSection.style.display = "none";
    



  } catch (error) {
    console.error(error);
    alert("Failed to fetch prediction");
  }
});



});

