"""CLI entrypoint for model training."""
import typer

from src.models.train import train_models

app = typer.Typer(help="Model training commands")

@app.command()
def fit(config: str = typer.Option("conf/modeling.yaml", help="Path to modeling config")) -> None:
    """Train baseline and advanced models defined in configuration."""
    train_models(config_path=config)

if __name__ == "__main__":
    app()
