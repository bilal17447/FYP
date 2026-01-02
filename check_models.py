import google.generativeai as genai

# Aapki API Key (Jo aapne code mein di thi)
genai.configure(api_key="AIzaSyAunlYvgJl3WOdLpAieh-Z5iCafJy1rq1Q")

print("--------------------------------------------------")
print("🔍 Searching for available models...")
print("--------------------------------------------------")

try:
    # Sare models list karein jo 'generateContent' (text generation) support karte hain
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Available: {m.name}")
            
except Exception as e:
    print(f"❌ Error: {e}")

print("--------------------------------------------------")