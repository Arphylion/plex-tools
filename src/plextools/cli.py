import mimetypes
import os
from os import getenv, walk
from pathlib import Path

import typer
from plexapi.server import PlexServer

mimetypes.init()

app = typer.Typer()
playlist_app = typer.Typer()
app.add_typer(playlist_app, name="playlist")


def init_plex():
    baseurl = getenv("PLEX_BASE_URL", None)
    token = getenv("PLEX_TOKEN", None)

    if not token:
        typer.secho("PLEX_TOKEN not defined.", fg=typer.colors.RED, bold=True)
        raise typer.Abort()
    if not baseurl:
        typer.secho("PLEX_BASE_URL not defined.", fg=typer.colors.RED, bold=True)
        raise typer.Abort()

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


def is_media_file(filename):
    mimestart = mimetypes.guess_type(filename)[0]

    if mimestart is not None:
        mimestart = mimestart.split("/")[0]
        return mimestart in ["audio", "video", "image"]

    return False


@playlist_app.command("create")
def playlist_create(
    directory: Path = typer.Option(
        Path,
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    )
):
    typer.echo(f"Creating playlist: {directory.absolute()}")
    for dirname, _, filenames in walk(directory.absolute()):
        for filename in filenames:
            if is_media_file(filename):
                print(os.path.join(dirname, filename))


if __name__ == "__main__":
    app()
