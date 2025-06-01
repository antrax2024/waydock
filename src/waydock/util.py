import os
import shutil
import subprocess
import importlib.resources
from rich.console import Console
from waydock.constants import SPACES_DEFAULT, APP_NAME


cl = Console(log_time_format="[%Y-%m-%d %H:%M:%S]")
# Força o Rich a não omitir timestamps repetidos
cl._log_render.omit_repeated_times = False


def copyResource(destination) -> bool:
    # Extract only the filename from destination variable
    filename = os.path.basename(destination)
    # if directory does not exist, create it
    os.makedirs(os.path.dirname(destination), exist_ok=True)

    source = importlib.resources.files(anchor=f"{APP_NAME}").joinpath(
        f"assets/{filename}"
    )
    # Convert Traversable to string path and copy the file
    try:
        shutil.copy2(
            src=str(object=source),
            dst=destination,
        )
        return True
    except Exception as e:
        cl.print(f"[bold red]Error copying resource: {e}[/bold red]")
        return False


def printLog(message: str) -> None:
    cl.log(message)


def bytesToGb(bytes_value):
    return int(bytes_value / (1024**3))


def printLine() -> None:
    cl.print("[cyan]=[/cyan]" * 80)


def showStatus(preamble: str, message: str) -> None:
    cl.print(f"[bold yellow]{preamble:<{SPACES_DEFAULT}}[/bold yellow]: {message}")


def showError(message: str) -> None:
    error = "ERROR"
    cl.print(f"[bold red]{error:<{SPACES_DEFAULT}}[/bold red]: {message}")


def fileExists(file: str) -> bool:
    if os.path.isfile(file):
        return True
    else:
        return False


def configDirExists(configDir: str) -> bool:
    if os.path.isdir(configDir):
        return True
    else:
        return False


def executeCommand(command: str) -> tuple[int, str, str]:
    """
    Executes a shell command and returns its exit code, standard output, and standard error.

    Args:
        command (str): The shell command to execute.

    Returns:
        tuple[int, str, str]: A tuple containing the exit code, stdout, and stderr.
    """
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr
