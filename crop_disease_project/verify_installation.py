#!/usr/bin/env python3
"""
Verification script to check if all dependencies are installed correctly
"""
import sys
import os

def check_dependency(module_name, import_name=None, version_attr='__version__'):
    """Check if a dependency is installed"""
    if import_name is None:
        import_name = module_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, version_attr, 'Installed')
        return True, version
    except ImportError:
        return False, None

def main():
    print("=" * 60)
    print("Crop Disease Project - Dependency Verification")
    print("=" * 60)
    print(f"\nPython version: {sys.version}\n")
    
    # Backend dependencies
    print("Backend Dependencies:")
    print("-" * 60)
    dependencies = [
        ('flask', 'flask'),
        ('flask_cors', 'flask_cors'),
        ('torch', 'torch'),
        ('torchvision', 'torchvision'),
        ('PIL', 'PIL', '__version__'),
        ('numpy', 'numpy'),
        ('pandas', 'pandas'),
        ('tqdm', 'tqdm'),
    ]
    
    all_ok = True
    for display_name, import_name, *rest in dependencies:
        version_attr = rest[0] if rest else '__version__'
        installed, version = check_dependency(display_name, import_name, version_attr)
        if installed:
            print(f"✓ {display_name:20s} {version}")
        else:
            print(f"✗ {display_name:20s} NOT INSTALLED")
            all_ok = False
    
    # Project files
    print("\nProject Files:")
    print("-" * 60)
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Ensure project root is on sys.path so `model` and `backend` packages resolve
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Check model files
    model_dir = os.path.join(project_root, 'model')
    if os.path.exists(model_dir):
        try:
            from model.config import Config
            print("✓ model/config.py")
        except Exception as e:
            print(f"✗ model/config.py - {str(e)[:50]}")
            all_ok = False
        
        try:
            from model.dataset_loader import CropDiseaseDataset
            print("✓ model/dataset_loader.py")
        except Exception as e:
            print(f"✗ model/dataset_loader.py - {str(e)[:50]}")
            all_ok = False
        
        try:
            from model.train_model import ModelTrainer
            print("✓ model/train_model.py")
        except Exception as e:
            print(f"✗ model/train_model.py - {str(e)[:50]}")
            all_ok = False
    
    # Check backend files
    backend_dir = os.path.join(project_root, 'backend')
    if os.path.exists(backend_dir):
        try:
            from backend.model_loader import ModelLoader
            print("✓ backend/model_loader.py")
        except Exception as e:
            print(f"✗ backend/model_loader.py - {str(e)[:50]}")
            all_ok = False
        
        try:
            from backend.recommendation_engine import RecommendationEngine
            print("✓ backend/recommendation_engine.py")
        except Exception as e:
            print(f"✗ backend/recommendation_engine.py - {str(e)[:50]}")
            all_ok = False
        
        try:
            from backend.utils import preprocess_image
            print("✓ backend/utils.py")
        except Exception as e:
            print(f"✗ backend/utils.py - {str(e)[:50]}")
            all_ok = False
        
        try:
            from backend.app import app
            print("✓ backend/app.py")
        except Exception as e:
            print(f"✗ backend/app.py - {str(e)[:50]}")
            all_ok = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_ok:
        print("✓ All dependencies and files are properly installed!")
        return 0
    else:
        print("✗ Some dependencies or files have issues.")
        print("\nTo install missing dependencies, run:")
        print("  cd backend && pip3 install -r requirements.txt")
        return 1

if __name__ == '__main__':
    sys.exit(main())

