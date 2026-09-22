"""Optional publication/export plots using current Matplotlib APIs."""

from pathlib import Path


def plot_surface(surface, output, *, kind="heatmap"):
    if kind not in ("heatmap", "surface"):
        raise ValueError("Plot kind must be heatmap or surface")
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as error:
        raise ValueError('Install plotting support: python -m pip install ".[plot]"') from error
    grid = surface.grid
    longitude, latitude = np.meshgrid(grid.longitudes, grid.latitudes)
    values = np.asarray(surface.values)
    figure = plt.figure(figsize=(9, 6), layout="constrained")
    try:
        if kind == "surface":
            axis = figure.add_subplot(111, projection="3d")
            plot = axis.plot_surface(longitude, latitude, values, cmap="viridis")
            axis.set_zlabel(surface.unit)
        else:
            axis = figure.add_subplot(111)
            plot = axis.pcolormesh(longitude, latitude, values, cmap="viridis", shading="auto")
        axis.set_xlabel("Longitude")
        axis.set_ylabel("Latitude")
        axis.set_title("Travel cost surface")
        figure.colorbar(plot, ax=axis, label=surface.unit, shrink=0.7)
        figure.text(
            0.01,
            0.01,
            "Interpolated or legacy values are estimates; inspect dataset source metadata.",
            fontsize=7,
        )
        path = Path(output)
        if path.suffix.lower() not in (".png", ".svg", ".pdf"):
            raise ValueError("Plot output must be .png, .svg, or .pdf")
        path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(path, dpi=160)
    finally:
        plt.close(figure)
