import os
import fitz  # PyMuPDF
from docx import Document
from crewai import LLM
import json
import re

def get_groq_keys():
    """Returns a list of available Groq API keys."""
    keys = []
    # Check for numbered keys first
    i = 1
    while True:
        key = os.environ.get(f"GROQ_API_KEY_{i}")
        if not key:
            break
        keys.append(key)
        i += 1
    
    # Fallback to standard key if no numbered keys found
    if not keys:
        standard_key = os.environ.get("GROQ_API_KEY")
        if standard_key:
            keys.append(standard_key)
    
    return keys

# Global counter for rotation
_key_index = 0

def get_next_groq_key():
    """Rotates through available Groq API keys."""
    global _key_index
    keys = get_groq_keys()
    if not keys:
        return None
    
    key = keys[_key_index % len(keys)]
    _key_index += 1
    return key

def extract_text_from_file(file_path):
    """Extracts text from PDF, DOCX, or TXT files."""
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    try:
        if ext == ".pdf":
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
        elif ext == ".docx":
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            return f"Unsupported file type: {ext}"
    except Exception as e:
        return f"Error extracting text: {e}"
    
    return text

def parse_resume_with_ai(text, provider_label):
    """Uses LLM to extract structured data from resume text."""
    # Map provider label to model string
    if "Groq" in provider_label:
        model_name = "groq/llama-3.3-70b-versatile"
        api_key = get_next_groq_key()
    elif "OpenAI" in provider_label:
        model_name = "gpt-4o-mini"
        api_key = os.environ.get("OPENAI_API_KEY")
    else:
        # Default fallback to Groq if something goes wrong
        model_name = "groq/llama-3.3-70b-versatile"
        api_key = get_next_groq_key()

    if not api_key:
        return {"error": f"API Key for {provider_label} not found."}

    llm = LLM(model=model_name, api_key=api_key)

    prompt = f"""
    You are an expert HR assistant. Extract the following information from the resume text provided below.
    Provide the output in STRICT JSON format with these exact keys:
    - degree: The highest degree or current major (e.g., "BS Computer Science")
    - university: The name of the university (e.g., "MIT")
    - skills: A comma-separated list of technical skills (e.g., "Python, Java, AWS")
    - experience: A summary of work experience and projects (e.g., "Built a web app using React...")

    If information is missing, use an empty string.

    Resume Text:
    ---
    {text}
    ---
    JSON Output:
    """

    try:
        response = llm.call([{"role": "user", "content": prompt}])
        # Extract JSON from response (sometimes models add markdown backticks)
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return data
        else:
            return {"error": "Could not parse JSON from AI response."}
    except Exception as e:
        return {"error": f"AI Parsing failed: {e}"}
