"""CLI entrypoint for evaluation pipelines."""
import typer

from src.eval.run import evaluate_models

app = typer.Typer(help="Evaluation commands")

@app.command()
def run(config: str = typer.Option("conf/modeling.yaml", help="Path to modeling config")) -> None:
    """Run evaluation suite on trained models."""
    evaluate_models(config_path=config)

if __name__ == "__main__":
    app()
