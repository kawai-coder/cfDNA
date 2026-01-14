"""CLI for generating fragmentomic and methylation features."""
import typer

from src.features.pipeline import build_features

app = typer.Typer(help="Feature engineering commands")

@app.command()
def make(force: bool = typer.Option(False, help="Overwrite existing feature tables")) -> None:
    """Generate model-ready feature matrices."""
    build_features(force=force)

if __name__ == "__main__":
    app()
