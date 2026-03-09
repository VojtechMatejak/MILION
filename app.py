import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

app = FastAPI()

# Povolení přístupu pro externí weby (důležité pro prodej klientům)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# KONFIGURACE GEMINI
# Tvůj API klíč zůstává stejný
API_KEY = "AIzaSyCCN6wiTllhBPtGR8G4E-TS1wql0zKPkuI"
genai.configure(api_key=API_KEY)

# Tady definujeme model bez "beta" názvů, aby to neházelo 404
model = genai.GenerativeModel('gemini-1.5-flash')

# Nastavení složky pro HTML
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
        
        # Volání Gemini s tvými instrukcemi
        prompt = f"Jsi profesionální asistent firmy MILION AI. Odpovídej stručně a česky. Dotaz: {user_message}"
        response = model.generate_content(prompt)
        
        return {"reply": response.text}
    except Exception as e:
        print(f"DEBUG CHYBA: {e}")
        return JSONResponse(content={"reply": f"Chyba na serveru: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    # Render port - automaticky si vezme správný port od Renderu
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)