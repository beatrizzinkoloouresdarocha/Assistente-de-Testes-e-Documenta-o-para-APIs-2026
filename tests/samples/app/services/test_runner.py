import subprocess
import os

def run_pytest(test_file_path: str) -> tuple[bool, str]:
    """
    Executa o pytest no arquivo especificado.
    Retorna (True, stdout) se passou, ou (False, stderr/stdout) se falhou.
    """
    command = ["pytest", test_file_path, "-v", "--tb=short"]
    
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )
    
    passed = result.returncode == 0
    output = result.stdout if passed else result.stdout + "\n" + result.stderr
    return passed, output