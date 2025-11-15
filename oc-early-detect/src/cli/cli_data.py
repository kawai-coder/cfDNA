"""Command line interface for data acquisition workflows."""
import typer

from src.io.download import download_dataset

app = typer.Typer(help="Data acquisition commands")

@app.command()
def make(dataset: str = typer.Option("all", help="Dataset key defined in conf/datasets.yaml")) -> None:
    """Download raw data assets configured for the project."""
    download_dataset(dataset)

if __name__ == "__main__":
    app()
