"""
Dataset loader for crop disease classification
"""
import os
from torch.utils.data import Dataset
from PIL import Image
import torch

class CropDiseaseDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        """
        Initialize dataset
        
        Args:
            data_dir: Root directory containing class subdirectories
            transform: Optional transform to be applied on images
        """
        self.data_dir = data_dir
        self.transform = transform
        self.images = []
        self.labels = []
        self.class_indices = {}
        self.idx_to_class = {}
        
        # Load images and create class mappings
        self._load_data()
    
    def _load_data(self):
        """Load images and create class label mappings"""
        if not os.path.exists(self.data_dir):
            raise ValueError(f"Data directory does not exist: {self.data_dir}")
        
        # Get all class directories
        classes = sorted([d for d in os.listdir(self.data_dir) 
                         if os.path.isdir(os.path.join(self.data_dir, d))])
        
        # Create class to index mapping
        for idx, class_name in enumerate(classes):
            self.class_indices[class_name] = idx
            self.idx_to_class[idx] = class_name
        
        # Load all images
        for class_name in classes:
            class_dir = os.path.join(self.data_dir, class_name)
            class_idx = self.class_indices[class_name]
            
            # Get all image files in class directory
            for filename in os.listdir(class_dir):
                if self._is_image_file(filename):
                    image_path = os.path.join(class_dir, filename)
                    self.images.append(image_path)
                    self.labels.append(class_idx)
        
        print(f"Loaded {len(self.images)} images from {len(classes)} classes")
    
    def _is_image_file(self, filename):
        """Check if file is an image"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        return any(filename.lower().endswith(ext) for ext in image_extensions)
    
    def __len__(self):
        """Return dataset size"""
        return len(self.images)
    
    def __getitem__(self, idx):
        """
        Get item by index
        
        Args:
            idx: Index of the item
            
        Returns:
            Tuple of (image, label)
        """
        image_path = self.images[idx]
        label = self.labels[idx]
        
        # Load image
        try:
            image = Image.open(image_path).convert('RGB')
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            # Return a black image as fallback
            image = Image.new('RGB', (224, 224), color='black')
        
        # Apply transforms
        if self.transform:
            image = self.transform(image)
        
        return image, label

# model/dataset_loader.py

'''import os
from typing import Dict, Tuple, List

import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from .config import IMG_SIZE, BATCH_SIZE, NUM_WORKERS, DATA_DIR


def get_data_transforms() -> Dict[str, transforms.Compose]:
    """Return data transforms for train, valid, test."""
    train_transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])

    val_test_transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])

    return {
        "train": train_transform,
        "valid": val_test_transform,
        "test": val_test_transform,
    }


def get_dataloaders() -> Tuple[Dict[str, DataLoader], Dict[str, int], List[str]]:
    """
    Create DataLoaders for train/valid/test using ImageFolder.
    Assumes folder structure:
      DATA_DIR/train/CLASS_NAME/...
      DATA_DIR/valid/CLASS_NAME/...
      DATA_DIR/test/CLASS_NAME/...
    """
    transforms_dict = get_data_transforms()

    image_datasets = {
        split: datasets.ImageFolder(os.path.join(DATA_DIR, split),
                                    transform=transforms_dict[split])
        for split in ["train", "valid", "test"]
    }

    dataloaders = {
        split: DataLoader(image_datasets[split],
                          batch_size=BATCH_SIZE,
                          shuffle=True if split == "train" else False,
                          num_workers=NUM_WORKERS)
        for split in ["train", "valid", "test"]
    }

    dataset_sizes = {split: len(image_datasets[split]) for split in image_datasets}
    class_names = image_datasets["train"].classes

    return dataloaders, dataset_sizes, class_names'''
