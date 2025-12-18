"""
Configuration file for model training
"""
import os

class Config:
    def __init__(self):
        # Base directories
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DATA_DIR = os.path.join(self.BASE_DIR, "data")

        # Dataset paths
        self.train_data_path = os.path.join(self.DATA_DIR, "train")
        self.val_data_path   = os.path.join(self.DATA_DIR, "valid")
        self.test_data_path  = os.path.join(self.DATA_DIR, "test")

        # Model / training hyperparameters
        self.NUM_CLASSES   = 38
        self.batch_size    = 32
        self.num_workers   = 2
        self.learning_rate = 1e-3
        self.lr_step_size  = 7
        self.lr_gamma      = 0.1
        self.num_epochs    = 10

        # Model save path
        self.model_save_path = os.path.join(
            self.BASE_DIR,
            "saved_models",
            "best_model.pth",
        )

