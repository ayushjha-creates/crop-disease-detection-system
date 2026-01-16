

document.addEventListener("DOMContentLoaded", () => {
  const API_BASE_URL = window.API_BASE_URL || "http://127.0.0.1:8000";
  console.log("API Base URL:", API_BASE_URL);

  // Cache DOM elements
  const elements = {
    // Input elements
    imageInput: document.getElementById("imageInput"),
    predictBtn: document.getElementById("predictBtn"),
    
    // Display elements
    uploadArea: document.getElementById("uploadArea"),
    previewContainer: document.getElementById("previewContainer"),
    imagePreview: document.getElementById("imagePreview"),
    removeImage: document.getElementById("removeImage"),
    
    // Status elements
    connectionStatus: document.getElementById("connectionStatus"),
    statusDot: document.getElementById("statusDot"),
    statusText: document.getElementById("statusText"),
    loadingIndicator: document.getElementById("loadingIndicator"),
    
    // Result elements
    resultSection: document.getElementById("resultSection"),
    cropNameEl: document.getElementById("cropName"),
    diseaseNameEl: document.getElementById("diseaseName"),
    confidenceScoreEl: document.getElementById("confidenceScore"),
    descEl: document.getElementById("desc"),
    symptomsEl: document.getElementById("symptoms"),
    organicEl: document.getElementById("organic"),
    chemicalEl: document.getElementById("chemical"),
    preventiveEl: document.getElementById("preventive"),
    analyzeAnother: document.getElementById("analyzeAnother"),
    
    // Error elements
    errorSection: document.getElementById("errorSection"),
    errorMessage: document.getElementById("errorMessage"),
    retryBtn: document.getElementById("retryBtn")
  };

  
  const requiredElements = ['imageInput', 'predictBtn', 'resultSection'];
  for (const key of requiredElements) {
    if (!elements[key]) {
      console.error(`Error: ${key} element not found!`);
      alert(`Error: ${key} element not found. Please refresh the page.`);
      return;
    }
  }
  console.log("All required elements found");

  let lastPrediction = null;
  let selectedFile = null;

  
  async function testBackendConnection() {
    updateConnectionStatus("checking", "Checking connection...");
    
    try {
      const response = await fetch(`${API_BASE_URL}/`, {
        method: "GET",
        headers: { "Content-Type": "application/json" }
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log("Backend connected:", data);
        updateConnectionStatus("connected", "Connected to backend");
        return true;
      } else {
        console.warn(" Backend responded with status:", response.status);
        updateConnectionStatus("disconnected", "Backend error: " + response.status);
        return false;
      }
    } catch (error) {
      console.error(" Backend connection failed:", error);
      updateConnectionStatus("disconnected", "Cannot connect to backend");
      return false;
    }
  }

  function updateConnectionStatus(status, text) {
    if (elements.statusDot) {
      elements.statusDot.className = status;
    }
    if (elements.statusText) {
      elements.statusText.textContent = text;
    }
  }

  
  testBackendConnection();

  // FILE UPLOAD 
  if (elements.imageInput) {
    // File input change
    elements.imageInput.addEventListener("change", handleFileSelect);
    
    
    if (elements.uploadArea) {
      elements.uploadArea.addEventListener("dragover", (e) => {
        e.preventDefault();
        elements.uploadArea.style.background = "#e8ebff";
      });
      
      elements.uploadArea.addEventListener("dragleave", (e) => {
        e.preventDefault();
        elements.uploadArea.style.background = "#f8f9ff";
      });
      
      elements.uploadArea.addEventListener("drop", (e) => {
        e.preventDefault();
        elements.uploadArea.style.background = "#f8f9ff";
        const files = e.dataTransfer.files;
        if (files.length > 0) {
          elements.imageInput.files = files;
          handleFileSelect();
        }
      });
    }
  }

  function handleFileSelect() {
    const file = elements.imageInput?.files[0];
    
    if (!file) {
      hidePreview();
      return;
    }

    console.log(" File selected:", file.name, "Type:", file.type, "Size:", (file.size / 1024).toFixed(2), "KB");

    
    if (file.size > 10 * 1024 * 1024) {
      showError("File is too large. Please select an image smaller than 10MB.");
      elements.imageInput.value = "";
      hidePreview();
      return;
    }

    
    const validTypes = ["image/jpeg", "image/jpg", "image/png", "image/bmp"];
    if (!validTypes.includes(file.type.toLowerCase())) {
      showError("Please upload a valid image file (JPEG, PNG, or BMP).");
      elements.imageInput.value = "";
      hidePreview();
      return;
    }

    selectedFile = file;
    showPreview(file);
    hideError();
    
    // Enable predict button
    if (elements.predictBtn) {
      elements.predictBtn.disabled = false;
    }
  }

  function showPreview(file) {
    if (!elements.imagePreview || !elements.previewContainer) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      elements.imagePreview.src = e.target.result;
      elements.previewContainer.style.display = "block";
      if (elements.uploadArea) {
        elements.uploadArea.style.display = "none";
      }
    };
    reader.onerror = () => {
      showError("Error reading image file. Please try again.");
      hidePreview();
    };
    reader.readAsDataURL(file);
  }

  function hidePreview() {
    selectedFile = null;
    if (elements.previewContainer) {
      elements.previewContainer.style.display = "none";
    }
    if (elements.uploadArea) {
      elements.uploadArea.style.display = "block";
    }
    if (elements.predictBtn) {
      elements.predictBtn.disabled = true;
    }
  }

  // remove img bttn
  if (elements.removeImage) {
    elements.removeImage.addEventListener("click", () => {
      elements.imageInput.value = "";
      hidePreview();
    });
  }

  
  // PREDICTION HANDLER
  async function handlePredict() {
    console.log(" Starting prediction...");

    if (!selectedFile) {
      showError("Please select an image first.");
      return;
    }

    // Hide previous results/errors
    hideError();
    if (elements.resultSection) {
      elements.resultSection.style.display = "none";
    }

    // Show loading
    showLoading(true);
    if (elements.predictBtn) {
      elements.predictBtn.disabled = true;
      elements.predictBtn.textContent = "Analyzing...";
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      console.log(" Sending request to:", `${API_BASE_URL}/predict`);
      const startTime = Date.now();

      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: "POST",
        body: formData
      });

      const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(2);
      console.log(`Response received in ${elapsedTime}s, Status:`, response.status);

      if (!response.ok) {
        let errorMessage = "Prediction failed";
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorData.message || errorMessage;
          console.error(" Error response:", errorData);
        } catch (e) {
          errorMessage = `Server error: ${response.status} ${response.statusText}`;
          console.error(" Error response text:", await response.text());
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      console.log(" Backend response:", data);

      // Validate response
      if (!data || (data.crop_name === undefined && data.predicted_class === undefined)) {
        throw new Error("Invalid response from server");
      }

      lastPrediction = data;
      displayResults(data);
      
      // Update connection status to connected if it wasn't
      updateConnectionStatus("connected", "Connected");

    } catch (error) {
      console.error(" Prediction error:", error);
      
      let errorMsg = error.message || "Unknown error occurred";
      if (error.name === "TypeError" && error.message?.includes("fetch")) {
        errorMsg = `Cannot connect to backend at ${API_BASE_URL}. Make sure the backend is running.`;
        updateConnectionStatus("disconnected", "Connection failed");
      }
      
      showError(errorMsg);
    } finally {
      showLoading(false);
      if (elements.predictBtn) {
        elements.predictBtn.disabled = false;
        elements.predictBtn.textContent = "🔍 Analyze Disease";
      }
    }
  }


  // DISPLAY RESULTS
  function displayResults(data) {
    if (!elements.resultSection) return;

    // Update prediction fields
    if (elements.cropNameEl) {
      elements.cropNameEl.textContent = data.crop_name || 
        (data.predicted_class?.split("___")[0]) || "Unknown";
    }

    if (elements.diseaseNameEl) {
      const diseaseName = data.disease_name || 
        (data.predicted_class?.includes("___") ? data.predicted_class.split("___")[1] : "Healthy") || 
        "Unknown";
      elements.diseaseNameEl.textContent = diseaseName;
    }

    if (elements.confidenceScoreEl) {
      if (data.confidence !== undefined) {
        elements.confidenceScoreEl.textContent = (data.confidence * 100).toFixed(2) + "%";
      } else if (data.confidence_score !== undefined) {
        elements.confidenceScoreEl.textContent = data.confidence_score + "%";
      }
    }

    // Update recommendations
    if (data.recommendation) {
      if (elements.descEl) {
        elements.descEl.textContent = data.recommendation.disease_description || 
          "No description available. Please consult with an agricultural expert.";
      }
      if (elements.symptomsEl) {
        elements.symptomsEl.textContent = data.recommendation.symptoms || 
          "Please consult with an agricultural expert for specific symptoms.";
      }
      if (elements.organicEl) {
        elements.organicEl.textContent = data.recommendation.treatment_organic || 
          "Please consult with an agricultural expert for organic treatment options.";
      }
      if (elements.chemicalEl) {
        elements.chemicalEl.textContent = data.recommendation.treatment_chemical || 
          "Please consult with an agricultural expert for chemical treatment options.";
      }
      if (elements.preventiveEl) {
        elements.preventiveEl.textContent = data.recommendation.preventive_measures || 
          "Maintain good agricultural practices and monitor the crop regularly.";
      }
    } else {
      // Fallback recommendations
      if (elements.descEl) elements.descEl.textContent = 
        "No recommendation available. Please consult with an agricultural expert.";
      if (elements.symptomsEl) elements.symptomsEl.textContent = 
        "Please consult with an agricultural expert for specific symptoms.";
      if (elements.organicEl) elements.organicEl.textContent = 
        "Please consult with an agricultural expert for organic treatment options.";
      if (elements.chemicalEl) elements.chemicalEl.textContent = 
        "Please consult with an agricultural expert for chemical treatment options.";
      if (elements.preventiveEl) elements.preventiveEl.textContent = 
        "Maintain good agricultural practices and monitor the crop regularly.";
    }

    // Show results 
    elements.resultSection.style.display = "block";
    setTimeout(() => {
      elements.resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 100);

    console.log(" Results displayed successfully");
  }

  
  // UI HELPER FUNCTIONS
  function showLoading(show) {
    if (elements.loadingIndicator) {
      elements.loadingIndicator.style.display = show ? "block" : "none";
    }
  }

  function showError(message) {
    if (elements.errorSection && elements.errorMessage) {
      elements.errorMessage.textContent = message;
      elements.errorSection.style.display = "block";
      setTimeout(() => {
        elements.errorSection.scrollIntoView({ behavior: "smooth", block: "center" });
      }, 100);
    } else {
      alert(message);
    }
  }

  function hideError() {
    if (elements.errorSection) {
      elements.errorSection.style.display = "none";
    }
  }

 
  
  // Predict button
  if (elements.predictBtn) {
    elements.predictBtn.addEventListener("click", async (e) => {
      e.preventDefault();
      e.stopPropagation();
      await handlePredict();
    });
    console.log("Predict button connected");
  }

  // Analyze another button
  if (elements.analyzeAnother) {
    elements.analyzeAnother.addEventListener("click", () => {
      elements.imageInput.value = "";
      hidePreview();
      if (elements.resultSection) {
        elements.resultSection.style.display = "none";
      }
      hideError();
    });
  }

  // Retry button
  if (elements.retryBtn) {
    elements.retryBtn.addEventListener("click", () => {
      hideError();
      if (selectedFile) {
        handlePredict();
      } else {
        testBackendConnection();
      }
    });
  }
  
  console.log(" Frontend initialization complete");
  console.log(" Ready to accept predictions!");
  console.log("Backend URL:", API_BASE_URL);
  console.log(" Connection status will be updated automatically");
});