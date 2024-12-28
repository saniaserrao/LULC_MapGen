import torch
from tqdm import tqdm
import timm
from torchsummary import summary
import numpy as np


def initialize_model(model_name, weights, num_classes, device):
    model = timm.create_model(
        model_name, in_chans=weights.meta["in_chans"], num_classes=num_classes
    )
    model.load_state_dict(weights.get_state_dict(progress=True), strict=False)
    model = model.to(device)
    summary(model, (weights.meta["in_chans"], 224, 224))

    return model


def train(model, dataloader, criterion, optimizer, device):
    model.train()

    total_loss = 0.0
    total_correct = 0
    total_samples = len(dataloader.dataset)

    for i, (inputs, labels) in enumerate(
        tqdm(dataloader, desc="Training", leave=False)
    ):
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)  # forward pass
        loss = criterion(outputs, labels)
        loss.backward()  # backward pass
        optimizer.step()

        _, preds = torch.max(
            outputs, dim=1
        )  # prediction will be the class with maximum prob
        total_loss += loss.item() * inputs.size(0)
        total_correct += torch.sum(preds == labels).item()

    epoch_loss = total_loss / total_samples
    epoch_accuracy = (total_correct / total_samples) * 100

    print(f"Train Loss: {epoch_loss:.2f}; Accuracy: {epoch_accuracy:.2f}%")

    return epoch_loss, epoch_accuracy


def evaluate(model, dataloader, criterion, device, phase="val"):
    model.eval()
    total_loss = 0.0
    total_correct = 0
    total_samples = len(dataloader.dataset)

    for i, (inputs, labels) in enumerate(
        tqdm(dataloader, desc="Evaluating", leave=False)
    ):
        inputs, labels = inputs.to(device), labels.to(device)

        with torch.set_grad_enabled(False):
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            _, preds = torch.max(outputs, 1)  # along dim=1 : horizontal

        total_loss += loss.item() * inputs.size(0)
        total_correct += torch.sum(preds == labels)

    epoch_loss = total_loss / total_samples
    epoch_accuracy = (total_correct / total_samples) * 100
    print(f"{phase.title()} Loss: {epoch_loss:.2f}; Accuracy: {epoch_accuracy:.2f}%")

    return epoch_loss, epoch_accuracy


def fit(model, train_loader, val_loader, n_epochs, criterion, optimizer, device):
    best_loss = np.inf
    best_model = None
    accuracy_history = {"train_history": [], "val_history": []}

    for epoch in range(n_epochs):
        print("Epoch {}".format(epoch + 1))
        _, train_acc = train(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)

        accuracy_history["train_history"].append(train_acc)
        accuracy_history["val_history"].append(val_acc)

        if val_loss < best_loss:
            best_loss = val_loss
            best_model = model

    return best_model, accuracy_history
