# Command Line Interface for waydock
# Using click for command line interface
import click
from rich.table import Table
from waydock.util import cl, copyResource, printLog, fileExists
from waydock.constants import APP_NAME, APP_VERSION, CONFIG_FILE, STYLE_FILE


@click.command()
def cli() -> None:
    """
    Command line interface for waydock.
    """
    cl.print(
        f"[bold green]{APP_NAME}[/bold green] [bold blue]{APP_VERSION}[/bold blue]"
    )

    # Criação da tabela
    table = Table(show_header=True, header_style="bold cyan", title="Config Files")
    table.add_column("Item", justify="right")
    table.add_column("Path")
    table.add_column("Status", justify="center")

    if not fileExists(file=CONFIG_FILE):
        printLog(f"{CONFIG_FILE} does not exist. Try to creating...")
        copyResource(CONFIG_FILE)

    if not fileExists(file=STYLE_FILE):
        printLog(f"{STYLE_FILE} does not exist. try to Creating...")
        copyResource(STYLE_FILE)

    table.add_row(
        "Config",
        f"[yellow]{CONFIG_FILE}[/yellow]",
        "[bold green]Passed[/bold green]",
    )
    table.add_row(
        "Style",
        f"[yellow]{STYLE_FILE}[/yellow]",
        "[bold green]Passed[/bold green]",
    )

    cl.print(table)
