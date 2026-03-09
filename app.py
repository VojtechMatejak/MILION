import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from dotenv import load_dotenv

# Načtení klíčů (pro lokální testování z .env, na Renderu z Environment Variables)
load_dotenv()

app = FastAPI()

# Nastavení Gemini motoru
api_key = os.getenv("AIzaSyCCN6wiTllhBPtGR8G4E-TS1wql0zKPkuI")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Nastavení složky pro HTML (předpokládám, že máš složku 'templates')
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Tohle zobrazí tvou hlavní stránku index.html
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "")
        
        if not user_message:
            return JSONResponse(content={"reply": "Nenapsal jsi žádnou zprávu."}, status_code=400)

        # Generování odpovědi od Gemini
        response = model.generate_content(user_message)
        
        return {"reply": response.text}
    except Exception as e:
        return JSONResponse(content={"reply": f"Chyba na straně AI: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)