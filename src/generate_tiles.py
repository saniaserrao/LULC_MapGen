from tqdm import tqdm
import rasterio as rio
import geopandas as gpd
import pandas as pd
from shapely.geometry import box


from shapely.geometry import box


def generate_tiles(image_file, output_file, area_str, size=32):
    with rio.open(image_file) as raster:
        transform = raster.transform  # Get affine transform
        raster_bounds = raster.bounds
        width = raster.width
        height = raster.height

    geo_dict = {"id": [], "geometry": []}
    index = 0

    for x in range(0, width, size):
        for y in range(0, height, size):
            # Define the window in pixel coordinates
            window = rio.windows.Window(x, y, size, size)

            # Convert window to bounding box in spatial coordinates
            bbox = rio.windows.bounds(window, transform)
            bbox_geom = box(*bbox)

            geo_dict["id"].append(f"{area_str.lower()}_{index}")
            geo_dict["geometry"].append(bbox_geom)
            index += 1

    # Create GeoDataFrame
    tiles = gpd.GeoDataFrame(pd.DataFrame(geo_dict), crs="EPSG:4326")
    tiles.to_file(output_file, driver="GeoJSON")
    return tiles
