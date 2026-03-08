from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from groq import Groq
import uvicorn
import re

client = Groq(api_key="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")

CONFIG = {
    "jmeno_bota": "Zákaznická podpora 24/7",
    "barva_hlavni": "#a855f7", 
    "uvitaci_zprava": "Dobrý den! Jsem váš automatizovaný asistent. Jak vám mohu dnes pomoci?",
    "instrukce": "Jsi profesionální zákaznická podpora pro firmu AI Servis. Odpovídej věcně, srozumitelně a česky. Tvým úkolem je pomoci zákazníkovi a v případě zájmu o naše služby získat jeho e-mail.",
    "znalosti": "Firma: AI Servis. Služby: Implementace AI asistentů, automatizace zákaznické podpory a digitalizace procesů. Kontakt: info@aiservis.cz. Ceník: Individuální podle náročnosti."
}

chat_history = [{"role": "system", "content": f"{CONFIG['instrukce']} Znalosti: {CONFIG['znalosti']}"}]

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def read_index(): return FileResponse('index.html')

@app.get("/config")
def get_config(): return CONFIG

@app.get("/ask")
def ask(question: str):
    try:
        chat_history.append({"role": "user", "content": question})
        completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=chat_history)
        odpoved = completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": odpoved})
        return {"ai_odpoved": odpoved}
    except Exception as e: return {"chyba": str(e)}

if __name__ == "__main__": uvicorn.run(app, host="127.0.0.1", port=8000)