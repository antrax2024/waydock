# Command Line Interface for waydock
# Using click for command line interface
import sys
import click
from rich.table import Table
from waydock.util import cl, showError, fileExists
from waydock.constants import APP_NAME, APP_VERSION, CONFIG_FILE, STYLE_FILE


@click.command()
def cli() -> None:
    """
    Command line interface for waydock.
    """
    cl.print(
        f"[bold green]{APP_NAME}[/bold green] [bold blue]{APP_VERSION}[/bold blue]"
    )

    cl.print("Config files...")
    # Criação da tabela
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Item", justify="right")
    table.add_column("Path")
    table.add_column("Status", justify="center")

    configFileOk = fileExists(file=CONFIG_FILE)
    styleFileOk = fileExists(file=STYLE_FILE)
    table.add_row(
        "Config",
        f"[yellow]{CONFIG_FILE}[/yellow]",
        f"{'[bold green]Passed[/bold green]' if configFileOk else '[bold red]Fail[/bold red]'}",
    )
    table.add_row(
        "Style",
        f"[yellow]{STYLE_FILE}[/yellow]",
        f"{'[bold green]Passed[/bold green]' if styleFileOk else '[bold red]Fail[/bold red]'}",
    )

    cl.print(table)

    if not configFileOk:
        showError(f"{CONFIG_FILE} does not exist. Exiting...")
        sys.exit(1)

    if not styleFileOk:
        showError("Style file does not exists... Exiting...")
        sys.exit(1)
