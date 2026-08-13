import sys
import subprocess


def run_pytest(test_file_path: str) -> tuple[bool, str]:
    """
    Executa o Pytest no arquivo especificado.
    Retorna (True, stdout) se passou, ou (False, log_de_erro) se falhou.
    """
    # Usa sys.executable para garantir que o pytest rode no mesmo Python/venv ativo
    command = [sys.executable, "-m", "pytest", test_file_path, "-v", "--tb=short"]

    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")

    passed = result.returncode == 0

    if passed:
        output = result.stdout
    else:
        # Combina stdout e stderr para a IA entender exatamente onde o teste falhou
        output = f"{result.stdout}\n{result.stderr}".strip()

    return passed, output
