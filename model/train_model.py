
import json
import os
import sys

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# flake8: noqa: E402  # module level import not at top of file (needed for sys.path)
# flake8: noqa: E402  # module level import not at top of file (needed for sys.path)
import torch
from torch import nn, optim
from torch.optim.lr_scheduler import StepLR
from torch.utils.data import DataLoader
from torchvision import models, transforms
from tqdm import tqdm

from config import Config
from dataset_loader import CropDiseaseDataset


class ModelTrainer:
    """Model trainer class for crop disease classification."""

    def __init__(self, config: Config):
        """Initialize model trainer with configuration."""
        self.config = config
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        print(f"Using device: {self.device}")

        # Initialize model
        self.model = self._create_model()

        # Loss function and optimizer
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(
            self.model.parameters(), lr=config.learning_rate
        )
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
        model = models.resnet18(pretrained=False)
        model.fc = torch.nn.Linear(
            model.fc.in_features, self.config.NUM_CLASSES
        )
        return model.to(self.device)

    def setup_data_loaders(self):
        """Create data loaders for training and validation."""
        # Define transforms
        train_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
        ])

        val_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
        ])

        # Create datasets
        train_dataset = CropDiseaseDataset(
            self.config.train_data_path, transform=train_transform
        )
        val_dataset = CropDiseaseDataset(
            self.config.val_data_path, transform=val_transform
        )

        # Create data loaders
        self.train_loader = DataLoader(
            train_dataset,
            batch_size=self.config.batch_size,
            shuffle=True,
            num_workers=self.config.num_workers,
        )

        self.val_loader = DataLoader(
            val_dataset,
            batch_size=self.config.batch_size,
            shuffle=False,
            num_workers=self.config.num_workers,
        )

        print(f"Training samples: {len(train_dataset)}")
        print(f"Validation samples: {len(val_dataset)}")

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

            # Update progress bar
            pbar.set_postfix({
                'loss': running_loss / (pbar.n + 1),
                'acc': 100. * correct / total
            })

        epoch_loss = running_loss / len(self.train_loader)
        epoch_acc = 100. * correct / total
        return epoch_loss, epoch_acc

    def validate_epoch(self):
        """Validate for one epoch."""
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

                # Update progress bar
                pbar.set_postfix({
                    'loss': running_loss / (pbar.n + 1),
                    'acc': 100. * correct / total
                })

        epoch_loss = running_loss / len(self.val_loader)
        epoch_acc = 100. * correct / total
        return epoch_loss, epoch_acc

    def save_model(self, filepath):
        """Save model and class indices."""
        torch.save(self.model.state_dict(), filepath)

        # Save class indices
        if self.train_loader:
            dataset = self.train_loader.dataset
            class_indices = dataset.class_indices
            class_indices_path = os.path.join(
                os.path.dirname(filepath), "class_indices.json"
            )
            with open(class_indices_path, "w", encoding="utf-8") as f:
                json.dump(class_indices, f, indent=2)

        print(f"Model saved to {filepath}")

    def train(self):
        """Main training loop."""
        if self.train_loader is None:
            self.setup_data_loaders()

        best_val_acc = 0.0

        for epoch in range(self.config.num_epochs):
            print(f"\nEpoch {epoch + 1}/{self.config.num_epochs}")

            # Training
            train_loss, train_acc = self.train_epoch()

            # Validation
            val_loss, val_acc = self.validate_epoch()

            # Learning rate scheduler
            self.scheduler.step()

            # Print results
            print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
            print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")

            # Save best model
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                self.save_model(self.config.model_save_path)
                print("New best model saved!")

        print(f"\nTraining completed. Best validation accuracy: {best_val_acc:.2f}%")
        return best_val_acc


def main():
    """Main function to run training."""
    config = Config()
    trainer = ModelTrainer(config)
    trainer.train()


if __name__ == "__main__":
    main()