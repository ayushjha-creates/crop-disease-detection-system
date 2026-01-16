"""Rule-based crop disease recommendation helper."""
from typing import Dict


# Disease treatment database with organic and chemical options
RECOMMENDATIONS: Dict[str, Dict[str, str]] = {
    "Apple___Apple_scab": {
        "disease_description": "Fungal disease causing olive-brown spots on apple leaves and fruits.",
        "symptoms": "Velvety dark spots on leaves, distorted fruits, premature leaf fall.",
        "treatment_organic": (
            "Prune infected twigs and branches. Remove fallen leaves. Use sulfur-based "
            "fungicidal sprays and neem oil as per local guidelines."
        ),
        "treatment_chemical": (
            "Apply recommended systemic fungicides following local agricultural "
            "department guidelines and pre-harvest intervals."
        ),
        "preventive_measures": (
            "Plant resistant varieties where possible, maintain proper spacing for "
            "air circulation, and avoid overhead irrigation late in the day."
        ),
    },
    "Potato___Early_blight": {
        "disease_description": "Fungal disease causing concentric ring spots and defoliation in potato.",
        "symptoms": "Dark brown concentric spots on older leaves, yellowing, premature defoliation.",
        "treatment_organic": (
            "Remove affected leaves. Improve soil health with compost. Use copper-based "
            "or biological fungicides, and ensure crop rotation."
        ),
        "treatment_chemical": (
            "Apply recommended protectant fungicides (e.g., mancozeb-type compounds) "
            "as per local extension recommendations."
        ),
        "preventive_measures": (
            "Use certified seed, avoid overhead irrigation, maintain proper spacing "
            "and rotate with non-host crops."
        ),
    },
    "Potato___Late_blight": {
        "disease_description": "Serious disease of potato causing leaf blight and tuber rot.",
        "symptoms": "Water-soaked lesions on leaves, white fungal growth on undersides, tuber rot.",
        "treatment_organic": (
            "Remove and destroy severely infected plants. Use biofungicides and "
            "ensure good field drainage."
        ),
        "treatment_chemical": (
            "Use recommended systemic fungicides at early signs of infection, "
            "following label instructions and local regulations."
        ),
        "preventive_measures": (
            "Plant tolerant varieties, avoid late planting in disease-prone areas, "
            "ensure proper hilling and field drainage."
        ),
    },
    "Tomato___Late_blight": {
        "disease_description": "Highly destructive fungal disease of tomato foliage and fruit.",
        "symptoms": "Dark water-soaked lesions on leaves and stems, white fungal growth in humid conditions.",
        "treatment_organic": (
            "Remove infected plant parts, avoid overhead irrigation, and apply approved biofungicides."
        ),
        "treatment_chemical": (
            "Use recommended fungicides in rotation to avoid resistance, always "
            "respect safety intervals and dosage."
        ),
        "preventive_measures": (
            "Plant resistant varieties, maintain field hygiene, ensure good air circulation."
        ),
    },
    "Tomato___Leaf_Mold": {
        "disease_description": "Fungal disease causing yellow spots and mold growth on leaves.",
        "symptoms": "Yellow spots on upper leaf surfaces and olive-green mold below; leaves may curl and drop.",
        "treatment_organic": (
            "Improve ventilation in greenhouses, prune lower leaves, and use sulfur or "
            "biofungicides approved for tomato."
        ),
        "treatment_chemical": (
            "Use recommended fungicides according to local guidelines and rotate active ingredients."
        ),
        "preventive_measures": (
            "Avoid high humidity, provide good air movement, and avoid overhead irrigation."
        ),
    },
    "Corn_(maize)___Common_rust_": {
        "disease_description": "Rust disease of maize causing reddish-brown pustules on leaves.",
        "symptoms": "Small elongated pustules on both leaf surfaces that later turn dark.",
        "treatment_organic": (
            "Use resistant varieties where available, and remove severely infected plants when feasible."
        ),
        "treatment_chemical": (
            "Apply recommended fungicides if disease pressure is high, depending on local guidelines."
        ),
        "preventive_measures": (
            "Rotate crops, avoid dense planting, and monitor fields regularly."
        ),
    },
}


def get_recommendation(crop_name: str, disease_name: str) -> Dict[str, str]:
    """Return treatment advice based on crop and disease."""
    
    crop_name = crop_name.strip() if crop_name else ""
    disease_name = disease_name.strip() if disease_name else ""
    
# Handle healthy plants
    if not disease_name or disease_name.lower() == "healthy" or disease_name == " ":
        return {
            "disease_description": (
                f"The {crop_name} crop appears to be healthy with no signs of disease detected."
            ),
            "symptoms": "No symptoms detected. The crop appears healthy.",
            "treatment_organic": (
                "No treatment needed. Continue with regular healthy crop management practices."
            ),
            "treatment_chemical": (
                "No chemical treatment needed. Maintain good agricultural practices to "
                "prevent future disease outbreaks."
            ),
        }
    
    # Try exact match first
    key = f"{crop_name}___{disease_name}"
    rec = RECOMMENDATIONS.get(key)
    
    if rec:
        return rec
    
    # Try normalized key (fallback for format differences)
    normalized_key = key.replace(" ", "_").replace("__", "_")
    rec = RECOMMENDATIONS.get(normalized_key)
    
    if rec:
        return rec
    
    # Search for partial matches by crop name
    for rec_key in RECOMMENDATIONS.keys():
        if crop_name.lower() in rec_key.lower() and disease_name.lower() in rec_key.lower():
            return RECOMMENDATIONS[rec_key]

    # Return generic advice for unknown diseases
    return {
        "disease_description": (
            f"The system detected a potential issue with {crop_name} crop. "
            f"Detected condition: {disease_name}. Detailed information "
            "for this specific disease is not available in the rule base."
        ),
        "symptoms": (
            "Check for spots, discoloration, wilting, or unusual growth on leaves and stems. "
            "Consult with an agricultural expert for specific symptoms of this condition."
        ),
        "treatment_organic": (
            "Remove and safely dispose of heavily infected plant parts. Maintain field "
            "hygiene and improve soil health with compost or organic amendments. "
            "Consider consulting with a local agricultural extension officer for organic treatment options."
        ),
        "treatment_chemical": (
            "Consult a local agricultural extension officer or certified agronomist for "
            "appropriate and safe chemical treatment based on local recommendations. "
            "Always follow label instructions and safety guidelines."
        ),
        "preventive_measures": (
            "Use disease-free seed and seedlings, practice crop rotation, maintain "
            "proper spacing and irrigation, and monitor the field regularly. "
            "Implement good agricultural practices to prevent disease spread."
        ),
    }