"""
Training script for crop disease classification model
"""
import os
import sys
import json
import time

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
from torchvision import models, transforms
from torch.utils.data import DataLoader
from tqdm import tqdm

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from dataset_loader import CropDiseaseDataset
from config import Config


class ModelTrainer:
    def __init__(self, config: Config):
        """Initialize model trainer with configuration."""
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")

        # Initialize model
        self.model = self._create_model()

        # Loss function and optimizer
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=config.learning_rate)
        self.scheduler = StepLR(
            self.optimizer,
            step_size=config.lr_step_size,
            gamma=config.lr_gamma,
        )

        # Data loaders
        self.train_loader = None
        self.val_loader = None

    def _create_model(self):
        """Create ResNet18 model with correct output classes."""
        # NOTE: 'pretrained' is deprecated warning, but still works.
        model = models.resnet18(pretrained=True)

        # Freeze backbone
        for param in model.parameters():
            param.requires_grad = False

        in_features = model.fc.in_features

        # Prefer NUM_CLASSES from config, fallback to class_indices, then 38
        num_classes = getattr(self.config, "NUM_CLASSES", None)

        if num_classes is None:
            class_indices = getattr(self.config, "class_indices", None)
            if class_indices is not None:
                num_classes = len(class_indices)
            else:
                num_classes = 38  # final fallback for this dataset

        print(f"Using num_classes = {num_classes}")
        model.fc = nn.Linear(in_features, num_classes)

        return model.to(self.device)

    def _get_data_loaders(self):
        """Load training and validation datasets."""
        # Data transforms
        train_transform = transforms.Compose(
            [
                transforms.RandomResizedCrop(224),
                transforms.RandomHorizontalFlip(),
                transforms.RandomRotation(15),
                transforms.ColorJitter(
                    brightness=0.2, contrast=0.2, saturation=0.2
                ),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225],
                ),
            ]
        )

        val_transform = transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225],
                ),
            ]
        )

        # Create datasets
        train_dataset = CropDiseaseDataset(
            self.config.train_data_path,
            transform=train_transform,
        )

        val_dataset = CropDiseaseDataset(
            self.config.val_data_path,
            transform=val_transform,
        )

        # Create data loaders
        train_loader = DataLoader(
            train_dataset,
            batch_size=self.config.batch_size,
            shuffle=True,
            num_workers=self.config.num_workers,
            pin_memory=torch.cuda.is_available(),
        )

        val_loader = DataLoader(
            val_dataset,
            batch_size=self.config.batch_size,
            shuffle=False,
            num_workers=self.config.num_workers,
            pin_memory=torch.cuda.is_available(),
        )

        return train_loader, val_loader

    def train_epoch(self):
        """Train for one epoch."""
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        pbar = tqdm(self.train_loader, desc="Training")
        for images, labels in pbar:
            images, labels = images.to(self.device), labels.to(self.device)

            # Zero gradients
            self.optimizer.zero_grad()

            # Forward pass
            outputs = self.model(images)
            loss = self.criterion(outputs, labels)

            # Backward pass
            loss.backward()
            self.optimizer.step()

            # Statistics
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            pbar.set_postfix(
                {
                    "loss": f"{running_loss/(total/labels.size(0)):.4f}",
                    "acc": f"{100*correct/total:.2f}%",
                }
            )

        epoch_loss = running_loss / len(self.train_loader)
        epoch_acc = 100 * correct / total
        return epoch_loss, epoch_acc

    def validate(self):
        """Validate the model."""
        self.model.eval()
        running_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            pbar = tqdm(self.val_loader, desc="Validation")
            for images, labels in pbar:
                images, labels = images.to(self.device), labels.to(self.device)

                outputs = self.model(images)
                loss = self.criterion(outputs, labels)

                running_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

                pbar.set_postfix(
                    {
                        "loss": f"{running_loss/(total/labels.size(0)):.4f}",
                        "acc": f"{100*correct/total:.2f}%",
                    }
                )

        epoch_loss = running_loss / len(self.val_loader)
        epoch_acc = 100 * correct / total
        return epoch_loss, epoch_acc

    def save_model(self, filepath, class_indices):
        """Save model and class indices."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Save model weights
        torch.save(self.model.state_dict(), filepath)

        # Save class indices
        class_indices_path = os.path.join(
            os.path.dirname(filepath), "class_indices.json"
        )
        with open(class_indices_path, "w") as f:
            json.dump(class_indices, f, indent=2)

        print(f"Model saved to {filepath}")
        print(f"Class indices saved to {class_indices_path}")

    def train(self):
        """Run complete training pipeline."""
        print("Loading datasets...")
        self.train_loader, self.val_loader = self._get_data_loaders()

        # Get class indices from dataset
        if hasattr(self.train_loader.dataset, "class_indices"):
            class_indices = self.train_loader.dataset.class_indices
        else:
            class_indices = {}
            classes = sorted(os.listdir(self.config.train_data_path))
            for idx, class_name in enumerate(classes):
                class_indices[class_name] = idx

        best_val_acc = 0.0
        train_losses, train_accs = [], []
        val_losses, val_accs = [], []

        print(f"\nStarting training for {self.config.num_epochs} epochs...")
        print(f"Training samples: {len(self.train_loader.dataset)}")
        print(f"Validation samples: {len(self.val_loader.dataset)}")
        print(f"Number of classes: {len(class_indices)}\n")

        for epoch in range(1, self.config.num_epochs + 1):
            print(f"\nEpoch {epoch}/{self.config.num_epochs}")
            print("-" * 50)

            # Train
            train_loss, train_acc = self.train_epoch()
            train_losses.append(train_loss)
            train_accs.append(train_acc)

            # Validate
            val_loss, val_acc = self.validate()
            val_losses.append(val_loss)
            val_accs.append(val_acc)

            # Scheduler
            self.scheduler.step()

            # Save best model
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                self.save_model(self.config.model_save_path, class_indices)
                print(f"\n✓ New best validation accuracy: {best_val_acc:.2f}%")

            print(f"\nTrain Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
            print(f"Val   Loss: {val_loss:.4f}, Val   Acc: {val_acc:.2f}%")
            print(f"Best Val Acc: {best_val_acc:.2f}%")

        print("\nTraining completed!")
        print(f"Best validation accuracy: {best_val_acc:.2f}%")


def main():
    """Main function to run training."""
    config = Config()
    trainer = ModelTrainer(config)
    trainer.train()


if __name__ == "__main__":
    main()
