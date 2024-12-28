import os
import numpy as np
import rasterio as rio
from PIL import Image
import torch
from torchvision import transforms


def predict_crop(image, shape, model, show=False):
    imagenet_mean, imagenet_std = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]

    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),  # Combine resize and crop
            transforms.ToTensor(),
            transforms.Normalize(mean=imagenet_mean, std=imagenet_std),
        ]
    )

    classes = [
        "AnnualCrop",
        "Forest",
        "HerbaceousVegetation",
        "Highway",
        "Industrial",
        "Pasture",
        "PermanentCrop",
        "Residential",
        "River",
        "SeaLake",
    ]

    try:
        with rio.open(image) as src:
            out_image, out_transform = rio.mask.mask(src, shape, crop=True)

            if not np.any(out_image):
                return None

            _, x_nonzero, y_nonzero = np.nonzero(out_image)
            if x_nonzero.size == 0 or y_nonzero.size == 0:
                return None

            out_image = out_image[
                :,
                np.min(x_nonzero) : np.max(x_nonzero) + 1,
                np.min(y_nonzero) : np.max(y_nonzero) + 1,
            ]

            out_meta = src.meta.copy()
            out_meta.update(
                {
                    "driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform,
                }
            )

            temp_tif = "temp.tif"
            with rio.open(temp_tif, "w", **out_meta) as dest:
                dest.write(out_image)

        with Image.open(temp_tif) as image:
            input_tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            output = model(input_tensor)
            _, pred = torch.max(output, 1)
            label = str(classes[int(pred[0])])

        if show:
            image.show(title=label)

        if os.path.exists(temp_tif):
            os.remove(temp_tif)

        return label

    except Exception as e:
        print(f"An error occurred: {e}")
