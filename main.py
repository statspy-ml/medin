from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from medication_classifier import MedicationClassifier



app = FastAPI()
classifier = MedicationClassifier()  

@app.post("/medicament-recommendation/", response_model=dict)
async def medicament_recommendation(text: str = Form(...)):
   
    classification = classifier.classify_text(text)
    medicament_type = classification.get("topics", {}).get("topics", [])[0]  
    
   
    recommendations = classifier.get_medications_by_type(medicament_type)

    
    return {
        "classification": medicament_type,
        "recommendations": recommendations
    }






