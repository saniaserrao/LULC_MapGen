import ee


# generating image of ROI by aggregating multiple images across time to filter out cloud cover
def generate_image(
    region,
    min_date,
    max_date,
    product="COPERNICUS/S2",
    range_min=300,
    range_max=4500,
    cloud_pct=10,
):
    """Generates cloud-filtered, median-aggregated
    Sentinel-2 image from Google Earth Engine using the
    Pythin Earth Engine API.

    Args:
      region (ee.Geometry): The geometry of the area of interest to filter to.
      product (str): Earth Engine asset ID
      min_date (str): Minimum date to acquire collection of satellite images
      max_date (str): Maximum date to acquire collection of satellite images
      range_min (int): Minimum value for visalization range
      range_max (int): Maximum value for visualization range
      cloud_pct (float): The cloud cover percent to filter by (default 10)

    Returns:
      ee.image.Image: Generated Sentinel-2 image clipped to the region of interest
    """

    image = (
        ee.ImageCollection(product)
        .filterBounds(region)
        .filterDate(str(min_date), str(max_date))
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cloud_pct))
        .median()
    )

    image = image.visualize(bands=["B4", "B3", "B2"], min=range_min, max=range_max)

    return image.clip(region)
