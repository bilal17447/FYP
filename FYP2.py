import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import io
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

# --- PRINT MESSAGE ---
print("--------------------------------------------------")
print("✅ FINAL CODE LOADED: Ready for Summary & Quiz!")
print("--------------------------------------------------")

# 1. .env file se Key uthayen (Secure tareeqa)
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: .env file nahi mili ya usme Key nahi hai!")
else:
    genai.configure(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Model: 'gemini-flash-latest' (Sab se stable aur free)
model = genai.GenerativeModel('gemini-flash-latest')

@app.post("/upload_pdf")
async def process_pdf(file: UploadFile = File(...)):
    try:
        content = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        
        if len(text.strip()) < 10:
            return {"summary": "Error: PDF khali hai ya text read nahi ho raha."}

        # Summary ke liye prompt
        prompt = f"Summarize this text in simple bullet points:\n\n{text[:8000]}"
        
        response = model.generate_content(prompt)
        return {"summary": response.text}
    except Exception as e:
        return {"summary": f"Technical Error: {str(e)}"}

@app.post("/generate_quiz")
async def make_quiz(file: UploadFile = File(...)):
    try:
        # ✅ FIX: Ab ye function pehle PDF read kare ga
        content = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
            
        if len(text.strip()) < 10:
            return {"quiz": "Error: PDF khali hai, quiz nahi ban sakta."}

        # Text ka thora hissa model ko bhejenge
        short_text = text[:8000]

        # ✅ FIX: Prompt mein humne 'short_text' bhej diya hai
        prompt = f"""
        Based on the text provided below, create 3 Multiple Choice Questions (MCQs).
        
        Format exactly like this:
        Q1: [Question]
        a) [Option]
        b) [Option]
        c) [Option]
        d) [Option]
        Answer: [Correct Option]

        Text to use:
        {short_text}
        """
        
        response = model.generate_content(prompt)
        return {"quiz": response.text}
    except Exception as e:
        return {"quiz": f"Error: {str(e)}"}


app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running 🚀"}


app.mount("/static", StaticFiles(directory="static"), name="static")
