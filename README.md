# CareAI 🏥

**AI-Powered Medical Triage for Rural Communities**

> Built for the Quantum Sprint Hackathon · For Social Good

---

## What is CareAI?

CareAI is a web application that allows people in rural areas with limited access to healthcare services to describe their symptoms in natural language and instantly receive:

- Urgency classification (High / Medium / Low)
- Clear explanation of the possible condition in simple language
- Step-by-step first aid guidance
- Warning signs that require emergency care
- The 3 nearest health centers with distance and phone number

## Tech Stack

| Layer    | Technology              |
| -------- | ----------------------- |
| Backend  | Python + FastAPI        |
| AI       | Claude API (Anthropic)  |
| Database | Supabase (PostgreSQL)   |
| Frontend | HTML + CSS + JavaScript |
| Deploy   | Railway                 |

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/careai.git
cd careai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment variables

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 4. Create the table in Supabase

Run this SQL in your Supabase project:

```sql
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
```

### 5. Seed the database

```bash
python seed_data.py
```

### 6. Run the server

```bash
uvicorn main:app --reload
```

Open http://localhost:8000

## Deploy on Railway

1. Push your code to GitHub
2. Create a project on [Railway.app](https://railway.app)
3. Connect your repository
4. Add environment variables: `ANTHROPIC_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`
5. Railway deploys automatically — your public URL is ready in minutes

## Social Impact

In Peru, over 30% of the rural population has limited access to healthcare services. CareAI serves as a first-line medical guidance tool that helps people make informed decisions about when and where to seek medical attention — potentially saving lives in underserved communities.

## License

MIT
