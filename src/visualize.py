import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import torch


def plot_images(
    train_loader,
    class_names,
    imagenet_mean=[0.485, 0.456, 0.406],
    imagenet_std=[0.229, 0.224, 0.225],
):
    plt.figure(figsize=(10, 6))
    inputs, classes = next(iter(train_loader))
    # print(f"Input Shape: {inputs.shape}")
    # print(f"Classes Shape: {classes.shape}")

    for i in range(8):
        plt.subplot(2, 4, i + 1)
        image = inputs[i].numpy().transpose((1, 2, 0))
        image = np.clip(np.array(imagenet_std) * image + np.array(imagenet_mean), 0, 1)
        title = class_names[classes[i]]
        plt.imshow(image)
        plt.title(title)
        plt.axis("off")

    plt.show()


def plot_data_distribution(dataset):
    plt.figure(figsize=(6, 3))
    hist = sns.histplot(dataset.targets)

    hist.set_xticks(range(len(dataset.classes)))
    hist.set_xticklabels(dataset.classes, rotation=90)
    hist.set_title("Histogram of Classes in EuroSAT")

    plt.show()


def plot_results(
    data_loader,
    best_model,
    class_names,
    device,
    imagenet_mean=[0.485, 0.456, 0.406],
    imagenet_std=[0.229, 0.224, 0.225],
):
    plt.figure(figsize=(12, 6))
    inputs, labels = next(iter(data_loader))
    inputs, labels = inputs.to(device), labels.to(device)

    for i in range(8):
        plt.subplot(2, 4, i + 1)
        image = inputs[i].cpu().numpy().transpose((1, 2, 0))
        image = np.clip(np.array(imagenet_std) * image + np.array(imagenet_mean), 0, 1)

        output = best_model(inputs[i].unsqueeze(0))
        _, pred = torch.max(output, 1)

        true_label = class_names[labels[i].item()]
        pred_label = class_names[pred.item()]
        plt.imshow(image)
        plt.title(
            "Predicted class: {}\nActual Class: {}".format(pred_label, true_label)
        )
        plt.axis("off")

    plt.tight_layout()
    plt.show()
