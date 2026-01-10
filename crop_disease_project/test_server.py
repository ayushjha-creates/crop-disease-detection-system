#!/usr/bin/env python3
"""
Test script to verify the Crop Disease Detection server is running properly
"""
import requests
import json
import sys
import os
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")

def print_error(msg):
    print(f"{Colors.RED}✗{Colors.END} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.END} {msg}")

def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def test_model_files():
    """Test if model files exist"""
    print_header("Testing Model Files")
    
    model_paths = [
        Path("../model/saved_models/best_model.pth"),
        Path("model/saved_models/best_model.pth"),
        Path("./model/saved_models/best_model.pth"),
    ]
    
    class_paths = [
        Path("../model/saved_models/class_indices.json"),
        Path("model/saved_models/class_indices.json"),
        Path("./model/saved_models/class_indices.json"),
    ]
    
    model_found = False
    class_found = False
    
    for path in model_paths:
        abs_path = path.resolve()
        if abs_path.exists():
            print_success(f"Model file found: {abs_path}")
            print_info(f"  Size: {abs_path.stat().st_size / (1024*1024):.2f} MB")
            model_found = True
            break
    
    if not model_found:
        print_error("Model file (best_model.pth) not found!")
        print_info("Expected locations:")
        for path in model_paths:
            print_info(f"  - {path.resolve()}")
        return False
    
    for path in class_paths:
        abs_path = path.resolve()
        if abs_path.exists():
            print_success(f"Class indices file found: {abs_path}")
            try:
                with open(abs_path, 'r') as f:
                    classes = json.load(f)
                    print_info(f"  Number of classes: {len(classes)}")
            except Exception as e:
                print_warning(f"  Could not read class indices: {e}")
            class_found = True
            break
    
    if not class_found:
        print_error("Class indices file (class_indices.json) not found!")
        return False
    
    return True

def test_backend_import():
    """Test if backend can be imported"""
    print_header("Testing Backend Import")
    
    try:
        # Change to backend directory
        backend_dir = Path(__file__).parent / "backend"
        original_dir = os.getcwd()
        
        if backend_dir.exists():
            os.chdir(backend_dir)
            sys.path.insert(0, str(backend_dir))
        
        try:
            from model_loader import load_model_and_classes
            print_success("Successfully imported model_loader")
            
            # Try loading model (this might take a while)
            print_info("Attempting to load model... (this may take a moment)")
            try:
                model, idx_to_class = load_model_and_classes()
                print_success(f"Model loaded successfully!")
                print_info(f"  Number of classes: {len(idx_to_class)}")
                return True
            except Exception as e:
                print_error(f"Failed to load model: {e}")
                return False
        finally:
            os.chdir(original_dir)
            if backend_dir in sys.path:
                sys.path.remove(str(backend_dir))
    
    except ImportError as e:
        print_error(f"Failed to import backend modules: {e}")
        print_info("Make sure you've installed requirements: pip install -r requirements.txt")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def test_api_endpoint(base_url="http://127.0.0.1:8030", timeout=5):
    """Test if API endpoint is accessible"""
    print_header("Testing API Endpoint")
    
    print_info(f"Testing: {base_url}")
    
    try:
        # Test health check
        response = requests.get(f"{base_url}/", timeout=timeout)
        if response.status_code == 200:
            print_success(f"API is running! Status: {response.status_code}")
            try:
                data = response.json()
                print_info(f"Response: {json.dumps(data, indent=2)}")
            except:
                print_info(f"Response: {response.text}")
            return True
        else:
            print_error(f"API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API server!")
        print_info("Make sure the backend server is running:")
        print_info("  cd crop_disease_project && ./run_backend.sh")
        print_info("  OR")
        print_info("  cd crop_disease_project/backend && uvicorn app:app --host 0.0.0.0 --port 8030")
        return False
    except requests.exceptions.Timeout:
        print_error("API request timed out!")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def test_file_upload(base_url="http://127.0.0.1:8030", timeout=30):
    """Test file upload endpoint (with a dummy test if no image available)"""
    print_header("Testing File Upload Endpoint")
    
    print_info("Note: This test requires a valid image file")
    print_info("Creating a simple test image...")
    
    try:
        from PIL import Image
        import io
        
        # Create a simple test image
        test_image = Image.new('RGB', (224, 224), color='green')
        img_byte_arr = io.BytesIO()
        test_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        print_info(f"Testing upload to: {base_url}/predict")
        
        files = {'file': ('test_image.png', img_byte_arr, 'image/png')}
        response = requests.post(
            f"{base_url}/predict",
            files=files,
            timeout=timeout
        )
        
        if response.status_code == 200:
            print_success("File upload endpoint is working!")
            data = response.json()
            print_info("Response structure:")
            print(json.dumps(data, indent=2))
            
            # Check required fields
            required_fields = ['crop_name', 'disease_name', 'confidence', 'recommendation']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print_warning(f"Missing fields in response: {missing_fields}")
            else:
                print_success("All required fields present in response")
            
            return True
        else:
            print_error(f"Upload failed with status: {response.status_code}")
            try:
                error_data = response.json()
                print_error(f"Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print_error(f"Response: {response.text}")
            return False
    
    except ImportError:
        print_warning("PIL not available, skipping upload test")
        return None
    except Exception as e:
        print_error(f"Upload test failed: {e}")
        return False

def test_frontend_files():
    """Test if frontend files exist"""
    print_header("Testing Frontend Files")
    
    frontend_dir = Path(__file__).parent.parent / "frontend"
    required_files = ['index.html', 'app.js']
    
    if not frontend_dir.exists():
        print_error(f"Frontend directory not found: {frontend_dir}")
        return False
    
    print_success(f"Frontend directory found: {frontend_dir}")
    
    all_exist = True
    for file_name in required_files:
        file_path = frontend_dir / file_name
        if file_path.exists():
            print_success(f"  {file_name} exists")
            if file_name == 'app.js':
                # Check if API URL is configured
                with open(file_path, 'r') as f:
                    content = f.read()
                    if 'API_BASE_URL' in content:
                        print_info(f"  API_BASE_URL configuration found")
        else:
            print_error(f"  {file_name} not found!")
            all_exist = False
    
    return all_exist

def main():
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}  Crop Disease Detection - Server Test Suite{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    results = {}
    
    # Test 1: Model files
    results['model_files'] = test_model_files()
    
    # Test 2: Backend import (optional, can skip if slow)
    print("\n" + Colors.YELLOW + "Skip model loading test? (y/n): " + Colors.END, end="")
    skip_import = input().strip().lower() == 'y'
    
    if not skip_import:
        results['backend_import'] = test_backend_import()
    else:
        print_info("Skipping model loading test")
        results['backend_import'] = None
    
    # Test 3: Frontend files
    results['frontend_files'] = test_frontend_files()
    
    # Test 4: API endpoint (requires server running)
    print("\n" + Colors.YELLOW + "Test API endpoint? (requires server running) (y/n): " + Colors.END, end="")
    test_api = input().strip().lower() == 'y'
    
    if test_api:
        results['api_endpoint'] = test_api_endpoint()
        
        if results['api_endpoint']:
            # Test 5: File upload (requires server running)
            print("\n" + Colors.YELLOW + "Test file upload endpoint? (y/n): " + Colors.END, end="")
            test_upload = input().strip().lower() == 'y'
            
            if test_upload:
                results['file_upload'] = test_file_upload()
    else:
        results['api_endpoint'] = None
        results['file_upload'] = None
    
    # Summary
    print_header("Test Summary")
    
    test_names = {
        'model_files': 'Model Files',
        'backend_import': 'Backend Import & Model Loading',
        'frontend_files': 'Frontend Files',
        'api_endpoint': 'API Endpoint',
        'file_upload': 'File Upload Endpoint'
    }
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test_key, test_name in test_names.items():
        result = results.get(test_key)
        if result is True:
            print_success(f"{test_name}: PASSED")
            passed += 1
        elif result is False:
            print_error(f"{test_name}: FAILED")
            failed += 1
        else:
            print_warning(f"{test_name}: SKIPPED")
            skipped += 1
    
    print(f"\n{Colors.BOLD}Results: {Colors.GREEN}{passed} passed{Colors.END}, {Colors.RED}{failed} failed{Colors.END}, {Colors.YELLOW}{skipped} skipped{Colors.END}\n")
    
    if failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}All tests passed! Your server should be ready to use.{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}Some tests failed. Please check the errors above.{Colors.END}\n")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Test interrupted by user.{Colors.END}\n")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
