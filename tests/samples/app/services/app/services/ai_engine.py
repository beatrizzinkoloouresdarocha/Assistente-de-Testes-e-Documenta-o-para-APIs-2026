import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # Carrega as variáveis do arquivo .env

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_initial_test(source_code: str) -> str:
    prompt = f"""
    Dado o seguinte código de uma API FastAPI em Python:
    {source_code}
    
    Escreva uma suite de testes completa usando pytest e TestClient de httpx/fastapi.
    Retorne APENAS o código Python válido, sem explicações em texto.
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text.replace("```python", "").replace("```", "").strip()

def fix_test_code(source_code: str, test_code: str, error_log: str) -> str:
    prompt = f"""
    A API:
    {source_code}
    
    O teste atual:
    {test_code}
    
    O erro gerado pelo Pytest:
    {error_log}
    
    Corrija o código do teste para que passe no Pytest. Retorne APENAS o código Python corrigido.
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text.replace("```python", "").replace("```", "").strip()