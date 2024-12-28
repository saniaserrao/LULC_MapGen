import torch
from torchvision import models


def save_model(best_model, model_file):
    torch.save(best_model.state_dict(), model_file)
    print("Model successfully saved to {}.".format(model_file))


def load_model(model_file):
    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    model.fc = torch.nn.Linear(model.fc.in_features, 10)
    model.load_state_dict(torch.load(model_file))
    model.eval()

    print("Model file {} successfully loaded.".format(model_file))
    return model
