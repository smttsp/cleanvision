# type: ignore[attr-defined]

import argparse
import glob
import os

import typer
from tqdm import tqdm

from cleanvision.video_sampler import version
from cleanvision.video_sampler.logging import Color, console
from cleanvision.video_sampler.sampler import SamplerConfig, Worker

app = typer.Typer(
    name="video-sampler",
    help="Video sampler allows you to efficiently sample video frames",
    add_completion=False,
)


def version_callback(print_version: bool = True) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]video-sampler[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


# @app.command(name="")
def video_exporter_main(
    video_path: str = typer.Argument(
        ..., help="Path to the video file or a glob pattern."
    ),
    output_path: str = typer.Argument(..., help="Path to the output folder."),
) -> None:
    """Print a greeting with a giving name."""

    min_frame_interval_sec: float = 1.0
    keyframes_only: bool = True # typer.Option(True, help="Only sample keyframes."),
    buffer_size: int = 1 # typer.Option(10, help="Size of the buffer."),
    hash_size: int = 4 # typer.Option(4, help="Size of the hash."),
    queue_wait: float = 0.1 # typer.Option(0.1, help="Time to wait for the queue."),
    debug: bool = False # .Option(False, help="Enable debug mode."),

    output_path = f"{video_path}_images/"
    os.makedirs(output_path, exist_ok=True)

    cfg = SamplerConfig(
        min_frame_interval_sec=min_frame_interval_sec,
        keyframes_only=keyframes_only,
        buffer_size=buffer_size,
        hash_size=hash_size,
        queue_wait=queue_wait,
        debug=debug,
    )
    console.print(cfg, style=f"bold {Color.yellow.value}")

    videos = [video_path]
    msg = "Detected input as a file"
    if not os.path.isfile(video_path):
        videos = glob.glob(video_path)
        msg = f"Detected input as a folder with {len(videos)} files"
    console.print(msg, style=f"bold {Color.cyan.value}")

    worker = Worker(
        cfg=cfg,
    )
    for video in tqdm(videos, desc="Processing videos..."):
        video_subpath = os.path.join(output_path, os.path.basename(video))
        worker.launch(
            video_path=video,
            output_path=video_subpath,
        )


if __name__ == "__main__":
    app()
