import typer
import sys
from typing import List, Optional
from io_utils import read_file_list
from assess import process_csv_interactive

app = typer.Typer(help="Data Assessor CLI")

@app.command()
def assess(
    filenames: List[str] = typer.Argument(None, help="CSV files to process"),
    filelist: Optional[str] = typer.Option(None, help="File containing CSV filenames"),
    xcol: str = typer.Option("time", help="Partial match for X column"),
    ycol: str = typer.Option("force", help="Partial match for Y column"),
    json_log: str = typer.Option("assessments_register.json", help="JSON register path")
):
    """Interactive GUI assessment for one or more CSV files"""
    all_files = filenames.copy() if filenames else []

    if filelist:
        all_files += read_file_list(filelist)

    if not all_files and not sys.stdin.isatty():
        all_files += [line.strip() for line in sys.stdin if line.strip()]

    if not all_files:
        typer.echo("❌ No input files provided.", err=True)
        raise typer.Exit(code=1)

    for file in all_files:
        typer.echo(f"\n📂 Processing file: {file}")
        try:
            process_csv_interactive(file, xcol, ycol, json_log)
        except Exception as e:
            typer.echo(f"⚠️ Error processing {file}: {e}", err=True)

if __name__ == "__main__":
    app()
