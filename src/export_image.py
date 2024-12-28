import os
import requests
import zipfile
import rasterio
import ee


def export_image(
    image, filename, region, path="C:/Users/Sania Serrao/projects/LULCmapsGen/images"
):
    """Export Image to local disk as a merged RGB GeoTIFF from multiple band files."""
    print(f"Exporting {filename}.zip...")

    roi_dir = os.path.join(path, filename)
    local_zip = os.path.join(roi_dir, f"{filename}.zip")
    local_dir = os.path.join(roi_dir, filename)
    local_rgb_path = os.path.join(roi_dir, f"{filename}_RGB.tif")

    try:
        # Generate the URL for downloading the image (as a ZIP of bands)
        url = image.getDownloadURL(
            {
                "scale": 10,
                "region": region,
                "fileFormat": "GeoTIFF",
                "crs": "EPSG:4326",
                "maxPixels": 1e9,
            }
        )
        print(f"Download URL: {url}")
    except Exception as e:
        print(f"Error generating download URL: {e}")
        return None

    try:
        # Download the ZIP file
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            os.makedirs(roi_dir, exist_ok=True)  # Ensure directory exists
            with open(local_zip, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print(f"ZIP file successfully saved to {local_zip}")
        else:
            print(f"Failed to download image. HTTP status code: {response.status_code}")
            return None

        # Extract the ZIP file
        with zipfile.ZipFile(local_zip, "r") as zip_ref:
            zip_ref.extractall(local_dir)
        # print(f"ZIP file extracted to {local_dir}")

        # Check contents of the ZIP file
        # print(f"Contents of ZIP: {zip_ref.namelist()}")

        # Now merge the extracted bands into a single RGB image
        band_files = [
            os.path.join(local_dir, band)
            for band in zip_ref.namelist()
            if band.endswith(".tif")
        ]

        if len(band_files) != 3:
            print("Error: Expected 3 bands for RGB but found", len(band_files))
            return None

        # Open the bands as separate datasets
        datasets = [rasterio.open(band) for band in band_files]

        # Stack the bands into a single dataset
        meta = datasets[0].meta
        meta.update({"count": len(band_files)})

        with rasterio.open(local_rgb_path, "w", **meta) as dest:
            for idx, dataset in enumerate(datasets, start=1):
                dest.write(dataset.read(1), idx)

        print(f"RGB image saved to {local_rgb_path}")
        return local_rgb_path  # Return the path to the final RGB image

    except Exception as e:
        print(f"Error during export, download, or processing: {e}")
        return None
