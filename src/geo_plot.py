import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import rasterio as rio
from rasterio.plot import show


def plot_district(geodata, district_name):
    fig, ax = plt.subplots(1, figsize=(10, 10))
    geodata[geodata.shapeName == district_name].plot("shapeName", legend=True, ax=ax)


def plot_sat_img(tfile, geobound, roi):
    try:
        image = rio.open(tfile)
        boundary = geobound[geobound.shapeName == roi]

        fig, ax = plt.subplots(figsize=(15, 15))
        boundary.plot(facecolor="none", edgecolor="white", ax=ax, linewidth=1)
        show(image, ax=ax)
        ax.legend()

    except Exception as e:
        print(f"Error plotting the image: {e}")


def plot_tiles(image_path, tiles, region):
    image = rio.open(image_path)
    if tiles.crs != region.crs:
        region = region.to_crs(tiles.crs)

    raster_tiles = gpd.sjoin(tiles, region, predicate="within")

    fig, ax = plt.subplots(figsize=(15, 15))
    raster_tiles.plot(facecolor="none", edgecolor="red", ax=ax, linewidth=0.5)
    show(image, ax=ax)
    ax.set_title("Tiles on Raster", fontsize=12)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()

    return raster_tiles


def plot_crop(image_path, shape, title=None):
    with rio.open(image_path) as src:
        # Mask the image using the provided shape
        out_image, out_transform = rio.mask.mask(src, shape, crop=True)

        # Check for empty output
        if not out_image.any():
            raise ValueError("The selected shape does not intersect the raster.")

        # Extract non-zero values
        _, x_nonzero, y_nonzero = np.nonzero(out_image)
        out_image = out_image[
            :,
            np.min(x_nonzero) : np.max(x_nonzero),
            np.min(y_nonzero) : np.max(y_nonzero),
        ]

        # Show the cropped image
        show(out_image, title=title)
