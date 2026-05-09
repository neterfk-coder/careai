from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic
from supabase import create_client, Client
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

anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

class TriageRequest(BaseModel):
    symptoms: str
    latitude: float | None = None
    longitude: float | None = None

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return round(R * 2 * math.asin(math.sqrt(a)), 1)

TRIAGE_PROMPT = """Eres SaludIA, un asistente médico de triaje para comunidades rurales del Perú.
Tu objetivo es ayudar a personas que tienen acceso limitado a servicios de salud.
Analiza los síntomas descritos y responde ÚNICAMENTE con un objeto JSON válido (sin texto antes ni después):

{{
  "urgencia": "ALTA" | "MEDIA" | "BAJA",
  "titulo": "nombre breve del posible problema (máx 5 palabras)",
  "descripcion": "explicación clara en 2 oraciones usando lenguaje simple, no técnico",
  "recomendacion": "acción inmediata más importante que debe tomar el paciente",
  "especialidad": "tipo de médico que necesita consultar",
  "primeros_auxilios": [
    "primer paso concreto",
    "segundo paso concreto",
    "tercer paso concreto"
  ],
  "señales_alarma": [
    "señal que indica que debe ir a emergencias inmediatamente"
  ]
}}

Reglas:
- ALTA: riesgo de vida, necesita atención inmediata
- MEDIA: necesita atención en las próximas horas
- BAJA: puede esperar, manejo en casa con seguimiento
- Usa lenguaje simple que cualquier persona pueda entender
- Sé empático y tranquilizador pero honesto sobre la urgencia

Síntomas reportados: {symptoms}"""

@app.post("/api/triage")
async def triage(request: TriageRequest):
    if not request.symptoms or len(request.symptoms.strip()) < 5:
        raise HTTPException(status_code=400, detail="Por favor describe tus síntomas con más detalle.")

    try:
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": TRIAGE_PROMPT.format(symptoms=request.symptoms)
            }]
        )
        triage_result = json.loads(message.content[0].text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error procesando la respuesta de IA.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")

    try:
        response = supabase.table("health_centers").select("*").execute()
        all_centers = response.data or []
    except Exception:
        all_centers = []

    if request.latitude and request.longitude:
        for center in all_centers:
            lat = center.get("latitude")
            lon = center.get("longitude")
            if lat and lon:
                center["distance_km"] = haversine_km(
                    request.latitude, request.longitude, lat, lon
                )
            else:
                center["distance_km"] = None
        all_centers.sort(key=lambda c: c.get("distance_km") or 9999)

    return {
        "triage": triage_result,
        "centers": all_centers[:3]
    }

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "CareAI", "version": "1.0.0"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")