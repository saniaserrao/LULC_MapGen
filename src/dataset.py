import os
import zipfile
import numpy as np
from torch.utils import data
from torch.utils.data import Dataset
from torchvision import datasets, models, transforms

#creating dataset for EuroSat by subclassing Dataset->  always implement 3functions: __init__, __len__, and __getitem__.

class EuroSAT(Dataset):
  def __init__(self,dataset,transform=None):
    self.dataset = dataset
    self.transform = transform

  def __getitem__(self, index):
        if self.transform:
            x = self.transform(self.dataset[index][0])
        else:
            x = self.dataset[index][0]
        y = self.dataset[index][1]
        return x, y

  def __len__(self):
        return len(self.dataset)
    

def unzip_data(zip_path, extract_to):
    if not os.path.exists(extract_to):
        print(f"Unzipping {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Extracted to {extract_to}")
    else:
        print(f"Data already unzipped at {extract_to}")
 
       

def split_dataset_and_transform(dataset,input_size=224, imagenet_mean=[0.485, 0.456, 0.406], imagenet_std=[0.229, 0.224, 0.225], train_size=0.7, val_size=0.15):
    
    train_transform=transforms.Compose([
    transforms.ToTensor(),
    transforms.RandomResizedCrop(input_size),
    transforms.RandomVerticalFlip(),
    transforms.RandomHorizontalFlip(),
    transforms.Normalize(imagenet_mean, imagenet_std)
    ])

    test_transform=transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize(input_size),
    transforms.RandomResizedCrop(input_size),
    transforms.Normalize(imagenet_mean, imagenet_std)
    ])

    val_transform=transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize(input_size),
    transforms.RandomResizedCrop(input_size),
    transforms.Normalize(imagenet_mean, imagenet_std)
    ])
    
    train_data = EuroSAT(dataset, train_transform)
    val_data = EuroSAT(dataset, val_transform)
    test_data = EuroSAT(dataset, test_transform)


    indices=list(range(int(len(dataset))))
    train_split = int(train_size * len(dataset))
    val_split = int(val_size * len(dataset))
    np.random.shuffle(indices)

    train_data=data.Subset(train_data,indices=indices[:train_split])
    val_data = data.Subset(val_data, indices=indices[train_split: train_split+val_split])
    test_data = data.Subset(test_data, indices=indices[train_split+val_split:])
    
    return train_data, val_data, test_data




def create_dataloaders(train_data, val_data, test_data, batch_size=8, num_workers=2):

    train_loader = data.DataLoader(train_data, batch_size=batch_size, num_workers=num_workers, shuffle=True)
    val_loader = data.DataLoader(val_data, batch_size=batch_size, num_workers=num_workers, shuffle=False)
    test_loader = data.DataLoader(test_data, batch_size=batch_size, num_workers=num_workers, shuffle=False)
    
    return train_loader, val_loader, test_loader



def get_dataset_info(dataset, data_dir):
    # Print class names and count
    class_names = dataset.classes
    print(f"Class names: {class_names}")
    print(f"Total number of classes: {len(class_names)}\n")
    
    print("Displaying structure of the dataset:")
    for root, dirs, files in os.walk(data_dir):
        level = root.replace(data_dir, '').count(os.sep)
        indent = ' ' * 4 * level 
        if os.path.basename(root):
            print(f"{indent}{os.path.basename(root)}/")
        for file in files[:2]:
            print(f"{indent}    {file}")