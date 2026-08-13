import typer
from pathlib import Path
from app.services.ai_engine import generate_initial_test, fix_test_code
from app.services.test_runner import run_pytest

app = typer.Typer(help="CLI para Geração Automática de Testes de API")


@app.command()
def generate(
    target_file: str = typer.Argument(
        ..., help="Caminho do arquivo da API (ex: tests/samples/sample_api.py)"
    ),
    max_retries: int = typer.Option(
        3, help="Número máximo de tentativas de auto-correção"
    ),
):
    """
    Gera testes unitários para a API e executa o loop de auto-correção via Pytest.
    """
    target_path = Path(target_file)
    if not target_path.exists():
        typer.secho(
            f"Erro: Arquivo '{target_file}' não encontrado.", fg=typer.colors.RED
        )
        raise typer.Exit(code=1)

    source_code = target_path.read_text(encoding="utf-8")
    test_file_path = target_path.parent / f"test_{target_path.name}"

    typer.echo(f"🤖 Gerando testes para: {target_file}...")
    test_code = generate_initial_test(source_code)
    test_file_path.write_text(test_code, encoding="utf-8")

    # Loop de Auto-Correção
    for attempt in range(1, max_retries + 1):
        typer.echo(f"🧪 [Tentativa {attempt}/{max_retries}] Executando Pytest...")
        passed, error_log = run_pytest(str(test_file_path))

        if passed:
            typer.secho(
                f"✅ Sucesso! Todos os testes passaram e foram salvos em: {test_file_path}",
                fg=typer.colors.GREEN,
            )
            return

        typer.secho(
            f"⚠️ Testes falharam! Enviando erro para a IA corrigir...",
            fg=typer.colors.YELLOW,
        )
        test_code = fix_test_code(source_code, test_code, error_log)
        test_file_path.write_text(test_code, encoding="utf-8")

    typer.secho(
        f"❌ Não foi possível corrigir os testes após {max_retries} tentativas.",
        fg=typer.colors.RED,
    )


if __name__ == "__main__":
    app()
