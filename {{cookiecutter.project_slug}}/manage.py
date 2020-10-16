import subprocess

import typer
import uvicorn
from sqlalchemy.ext.declarative import DeclarativeMeta

from app import models

cmd = typer.Typer()


@cmd.command(help="run develop server using uvicorn")
def runserver(host: str = "127.0.0.1", port: int = 8000, reload: bool = True):
    uvicorn.run("app.main:app", reload=reload, host=host, port=port)


@cmd.command(help="update all dependencies' versions and apply in requirements folder")
def update_dep():
    files = [
        "requirements/production.in",
        "requirements/test.in",
        "requirements/dev.in",
    ]
    for file in files:
        subprocess.call(
            [
                "pip-compile",
                file,
                "--no-emit-index-url",
                "-U",
                "-i",
                "https://mirrors.aliyun.com/pypi/simple/",
                "-o",
                file.replace(".in", ".txt"),
            ]
        )


@cmd.command(help="test")
def test():
    subprocess.call(["pytest", "--disable-warnings", "-v", "--cov=./", "--cov-report=xml"])
    subprocess.call(["coverage", "html"])


@cmd.command(help="lint")
def lint():
    subprocess.call(["prospector", "app"])


@cmd.command(help="django-like dbshell command use pgcli")
def dbshell():
    from app.core import config

    subprocess.call(["pgcli", config.settings.postgres_dsn])


@cmd.command(help="django-like shell command use ipython")
def shell():
    try:
        import IPython  # pylint: disable=import-outside-toplevel
        from app.core import config  # pylint: disable=import-outside-toplevel
        from traitlets.config import Config  # pylint: disable=import-outside-toplevel

    except ImportError:
        return

    for obj in dir(models):
        obj = getattr(models, obj)
        if isinstance(obj, DeclarativeMeta):
            print(obj)
    preload_scripts = [
        "from app.main import app",
        "from app.core import config",
        "from app.models import *",
        "from app.middlewares import db",
    ]
    typer.secho("\n".join(preload_scripts), fg=typer.colors.GREEN)
    c = Config()
    c.PrefilterManager.multi_line_specials = True
    c.InteractiveShell.editor = "vim"
    c.InteractiveShellApp.exec_lines = preload_scripts
    c.TerminalIPythonApp.display_banner = False
    IPython.start_ipython(argv=[], config=c)


if __name__ == "__main__":
    cmd()
