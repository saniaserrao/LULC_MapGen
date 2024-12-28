import requests
import json
import os


def get_geodata(iso, amd, repo_dir):
    ISO = iso
    ADM = amd

    # Query GeoBoundaries API
    url = f"https://www.geoboundaries.org/api/current/gbOpen/{ISO}/{ADM}"
    response = requests.get(url)

    if response.status_code == 200:
        download_path = response.json()["gjDownloadURL"]
        geojson_data = requests.get(download_path).json()
        filename = "geoboundary" + str(ISO) + "_" + str(ADM) + ".geojson"
        file_path = os.path.join(repo_dir, filename)

        with open(file_path, "w") as file:
            json.dump(geojson_data, file)

        print(f"GeoJSON file saved at: {file_path}")
        return file_path

    else:
        raise Exception(
            f"Failed to fetch GeoJSON data. HTTP Status Code: {response.status_code}"
        )

    return None
