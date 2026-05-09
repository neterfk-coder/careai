"""
Ejecuta este script UNA VEZ para poblar Supabase con centros de salud.
Primero crea la tabla en Supabase con este SQL:

CREATE TABLE health_centers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    address TEXT,
    region TEXT,
    phone TEXT,
    latitude FLOAT,
    longitude FLOAT,
    emergency_24h BOOLEAN DEFAULT FALSE
);
"""

from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

HEALTH_CENTERS = [
    {
        "name": "Hospital Regional Hermilio Valdizán Medrano",
        "type": "Hospital",
        "address": "Jr. Hermilio Valdizán 950, Huánuco",
        "region": "Huánuco",
        "phone": "062-512140",
        "latitude": -9.9306,
        "longitude": -76.2421,
        "emergency_24h": True
    },
    {
        "name": "Hospital de Contingencia Tingo María",
        "type": "Hospital",
        "address": "Av. Ucayali s/n, Tingo María",
        "region": "Huánuco",
        "phone": "062-562100",
        "latitude": -9.2979,
        "longitude": -75.9981,
        "emergency_24h": True
    },
    {
        "name": "Centro de Salud Huánuco",
        "type": "Centro de Salud",
        "address": "Jr. Dámaso Beraún 852, Huánuco",
        "region": "Huánuco",
        "phone": "062-513800",
        "latitude": -9.9263,
        "longitude": -76.2390,
        "emergency_24h": False
    },
    {
        "name": "Puesto de Salud Llicua",
        "type": "Puesto de Salud",
        "address": "Llicua Alta, Huánuco",
        "region": "Huánuco",
        "phone": "062-515200",
        "latitude": -9.9150,
        "longitude": -76.2100,
        "emergency_24h": False
    },
    {
        "name": "Centro de Salud Ambo",
        "type": "Centro de Salud",
        "address": "Av. Principal s/n, Ambo",
        "region": "Huánuco",
        "phone": "062-571080",
        "latitude": -10.1337,
        "longitude": -76.2007,
        "emergency_24h": False
    },
    {
        "name": "Hospital Essalud Huánuco",
        "type": "Hospital",
        "address": "Jr. General Prado 560, Huánuco",
        "region": "Huánuco",
        "phone": "062-512980",
        "latitude": -9.9289,
        "longitude": -76.2438,
        "emergency_24h": True
    },
    {
        "name": "Centro de Salud Pillco Marca",
        "type": "Centro de Salud",
        "address": "Av. Universitaria s/n, Pillco Marca",
        "region": "Huánuco",
        "phone": "062-518900",
        "latitude": -9.9580,
        "longitude": -76.2280,
        "emergency_24h": False
    },
    {
        "name": "Puesto de Salud Andabamba",
        "type": "Puesto de Salud",
        "address": "Plaza principal s/n, Andabamba",
        "region": "Huánuco",
        "phone": None,
        "latitude": -9.9670,
        "longitude": -76.1540,
        "emergency_24h": False
    },
    {
        "name": "Centro de Salud Panao",
        "type": "Centro de Salud",
        "address": "Jr. Lima s/n, Panao",
        "region": "Huánuco",
        "phone": "062-555100",
        "latitude": -9.9090,
        "longitude": -75.9220,
        "emergency_24h": False
    },
    {
        "name": "Hospital de Apoyo Leoncio Prado",
        "type": "Hospital",
        "address": "Jr. Túpac Yupanqui 153, Leoncio Prado",
        "region": "Huánuco",
        "phone": "062-562521",
        "latitude": -9.3024,
        "longitude": -76.0003,
        "emergency_24h": True
    },
]

def seed():
    print("Insertando centros de salud en Supabase...")
    result = supabase.table("health_centers").insert(HEALTH_CENTERS).execute()
    print(f"✅ {len(result.data)} centros insertados correctamente.")

if __name__ == "__main__":
    seed()