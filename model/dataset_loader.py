
import os
import logging
from torch.utils.data import Dataset
from PIL import Image

logging.basicConfig(level=logging.INFO)
from PIL import Image


class CropDiseaseDataset(Dataset):
    """Dataset class for crop disease classification images."""

    def __init__(self, data_dir, transform=None):
        """
        Initialize dataset.

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
        """Load images and create class label mappings."""
        if not os.path.exists(self.data_dir):
            raise ValueError(f"Data directory does not exist: {self.data_dir}")

        # Get all class directories
        classes = sorted([
            d for d in os.listdir(self.data_dir)
            if os.path.isdir(os.path.join(self.data_dir, d))
        ])

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

        import logging
        logging.info(f"Loaded {len(self.images)} images from {len(classes)} classes")

    def _is_image_file(self, filename):
        """Check if file is an image."""
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        return any(filename.lower().endswith(ext) for ext in image_extensions)

    def __len__(self):
        """Return dataset size."""
        return len(self.images)

    def __getitem__(self, idx):
        """
        Get item by index.

        Args:
            idx: Index of item

        Returns:
            Tuple of (image, label)
        """
        image_path = self.images[idx]
        label = self.labels[idx]

        # Load image
        try:
            image = Image.open(image_path).convert('RGB')
        except Exception as e:
            logging.error(f"Error loading image {image_path}: {e}")
            # Return a black image as fallback
            image = Image.new('RGB', (224, 224))

        # Apply transforms
        if self.transform:
            image = self.transform(image)

        return image, label
