import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Nastavení Gemini
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Nastavení šablon
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
            return JSONResponse(content={"reply": "Nic jsi nenapsal."}, status_code=400)

        response = model.generate_content(user_message)
        return {"reply": response.text}
    except Exception as e:
        print(f"Chyba: {e}")
        return JSONResponse(content={"reply": "AI má momentálně pauzu, zkus to za vteřinu."}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    # Render potřebuje port z proměnné prostředí
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)