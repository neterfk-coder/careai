from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic
import httpx
import os
import json
import math
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="CareAI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

anthropic_client = Anthropic(api_key=os.getenv("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"))
SUPABASE_URL = os.getenv("https://wawqdgavicxbovubwkrl.supabase.co")
SUPABASE_KEY = os.getenv("sb_publishable_iUwmMypW776Ww7kGRbHgsA_M5pps90N")

class TriageRequest(BaseModel):
    symptoms: str
    latitude: float | None = None
    longitude: float | None = None

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return round(R * 2 * math.asin(math.sqrt(a)), 1)

TRIAGE_PROMPT = """Eres CareAI, un asistente médico de triaje para comunidades rurales del Perú.
Analiza los síntomas y responde ÚNICAMENTE con un objeto JSON válido (sin texto antes ni después):

{{
  "urgencia": "ALTA" | "MEDIA" | "BAJA",
  "titulo": "nombre breve del posible problema (máx 5 palabras)",
  "descripcion": "explicación clara en 2 oraciones usando lenguaje simple",
  "recomendacion": "acción inmediata más importante que debe tomar el paciente",
  "especialidad": "tipo de médico que necesita consultar",
  "primeros_auxilios": ["paso 1", "paso 2", "paso 3"],
  "señales_alarma": ["señal de emergencia 1"]
}}

Síntomas: {symptoms}"""

@app.post("/api/triage")
async def triage(request: TriageRequest):
    if not request.symptoms or len(request.symptoms.strip()) < 5:
        raise HTTPException(status_code=400, detail="Please describe your symptoms in more detail.")

    try:
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": TRIAGE_PROMPT.format(symptoms=request.symptoms)}]
        )
        triage_result = json.loads(message.content[0].text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error processing AI response.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/health_centers",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                },
                params={"select": "*", "limit": "20"}
            )
            all_centers = response.json()
    except Exception:
        all_centers = []

    if request.latitude and request.longitude and all_centers:
        for center in all_centers:
            lat = center.get("latitude")
            lon = center.get("longitude")
            if lat and lon:
                center["distance_km"] = haversine_km(request.latitude, request.longitude, lat, lon)
            else:
                center["distance_km"] = None
        all_centers.sort(key=lambda c: c.get("distance_km") or 9999)

    return {"triage": triage_result, "centers": all_centers[:3]}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "CareAI", "version": "1.0.0"}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")