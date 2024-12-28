import folium


def visualize_lulc(centroid, region, tiles):
    colors = {
        "AnnualCrop": "limegreen",
        "Forest": "darkgreen",
        "HerbaceousVegetation": "olive",
        "Highway": "darkgray",
        "Industrial": "firebrick",
        "Pasture": "goldenrod",
        "PermanentCrop": "green",
        "Residential": "orchid",
        "River": "deepskyblue",
        "SeaLake": "navy",
        "None": "black",
    }

    map = folium.Map(location=[centroid[1], centroid[0]], zoom_start=13)

    folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="Google",
        name="Google Satellite",
        overlay=True,
        control=True,
    ).add_to(map)

    # region boundary plot
    folium.GeoJson(
        region,
        style_function=lambda feature: {
            "fillColor": "none",
            "color": "black",
            "weight": 2,
        },
        name="Region of Interest",
    ).add_to(map)

    legend_txt = '<div style="display: inline-block; width: 12px; height: 12px; background-color: {col};"></div> {txt}'

    for label, color in colors.items():
        name = legend_txt.format(txt=label, col=color)
        feat_group = folium.FeatureGroup(name=name)

        subtiles = tiles[tiles.pred == label]
        if len(subtiles) > 0:
            folium.GeoJson(
                subtiles,
                style_function=lambda feature: {
                    "fillColor": feature["properties"]["color"],
                    "color": "white",
                    "weight": 1,
                    "fillOpacity": 0.5,
                },
                name="LULC Map",
            ).add_to(feat_group)
            map.add_child(feat_group)

    folium.LayerControl().add_to(map)

    return map
