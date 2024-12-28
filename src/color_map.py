import matplotlib.colors as cl


def color_map(tiles):
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
    tiles["color"] = tiles["pred"].apply(lambda x: cl.to_hex(colors.get(x, "black")))

    return tiles
