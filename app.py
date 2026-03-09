import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import google.generativeai as genai

app = FastAPI()

# TVŮJ KLÍČ NATVRDO (pro jistotu)
api_key = "AIzaSyCCN6wiTllhBPtGR8G4E-TS1wql0zKPkuI"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

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
            return JSONResponse(content={"reply": "Napiš něco..."}, status_code=400)
        
        # Tady voláme Gemini
        response = model.generate_content(user_message)
        return {"reply": response.text}
    except Exception as e:
        # Tohle vypíše chybu do Logu na Renderu, abychom viděli, co se děje
        print(f"DEBUG CHYBA: {e}")
        return JSONResponse(content={"reply": f"Chyba: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)