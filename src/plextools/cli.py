from os import getenv

import typer
from plexapi.server import PlexServer

app = typer.Typer()


def init_plex():
    baseurl = getenv("PLEX_BASE_URL", None)
    token = getenv("PLEX_TOKEN", None)

    if not token:
        typer.secho("PLEX_TOKEN not defined.", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)
    if not baseurl:
        typer.secho("PLEX_BASE_URL not defined.", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

    plex = PlexServer(baseurl, token)
    typer.secho(
        f"Connected to {plex.friendlyName} (version: {plex.version})",
        fg=typer.colors.YELLOW,
        bold=True,
    )

    if not plex.isLatest():
        typer.secho(
            "Server out of date, consider updating!",
            fg=typer.colors.RED,
            bold=True,
        )

    return plex


@app.command(name="plextools")
def cli():
    typer.echo("plextools")
    pass


if __name__ == "__main__":
    app()
