import os
from openai import OpenAI

# Garanta que a variável OPENAI_API_KEY esteja configurada no seu ambiente
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Você é um especialista em QA e backend Python. Sua tarefa é escrever testes unitários/integração
usando pytest e httpx/TestClient para APIs FastAPI/Flask.
Retorne APENAS o código Python válido, sem explicações em texto e sem formatação markdown (como ```python).
"""

def generate_initial_test(source_code: str) -> str:
    """Gera a primeira versão do arquivo de testes."""
    prompt = f"Gere testes completos com pytest e TestClient para a seguinte API:\n\n{source_code}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def fix_test_code(original_code: str, test_code: str, pytest_error: str) -> str:
    """Refaz/corrige o código de teste com base na saída de erro do pytest."""
    prompt = f"""
O código de teste gerado falhou na execução do pytest.

Código da API:
{original_code}

Código do Teste Atual:
{test_code}

Erro retornado pelo Pytest:
{pytest_error}

Por favor, corrija o código do teste para que todos os cenários passem com sucesso.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()