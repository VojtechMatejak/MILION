import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

app = FastAPI()

# Povolení přístupu (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# NASTAVENÍ TVOJEHO KLÍČE
api_key = "AIzaSyCCN6wiTllhBPtGR8G4E-TS1wql0zKPkuI"
genai.configure(api_key=api_key)
# Tady můžeš botovi nastavit instrukce (osobnost)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="Jsi profesionální zákaznická podpora pro firmu MILION AI. Odpovídej věcně, srozumitelně a česky."
)

# Nastavení šablon - hledá index.html ve složce templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "")
        if not user_message:
            return JSONResponse(content={"reply": "Nic jsi nenapsal..."}, status_code=400)
        
        # Volání Gemini
        response = model.generate_content(user_message)
        return {"reply": response.text}
    except Exception as e:
        print(f"DEBUG CHYBA: {e}")
        return JSONResponse(content={"reply": f"Chyba: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    # Render port
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)