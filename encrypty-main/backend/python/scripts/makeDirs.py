#!/usr/bin/env python3
"""
Script to create test directories for encryption/decryption testing.
"""

import os
import sys

def create_test_directories():
    """Create test directories with sample files."""
    
    # Get project root (parent of backend/python/scripts)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))
    data_dir = os.path.join(project_root, 'data')
    
    # Default test directory name (in data/test)
    test_dir = os.path.join(data_dir, "test")
    
    # Check if custom directory name is provided as argument
    if len(sys.argv) > 1:
        # If absolute path, use it; otherwise, create in data directory
        if os.path.isabs(sys.argv[1]):
            test_dir = sys.argv[1]
        else:
            test_dir = os.path.join(data_dir, sys.argv[1])
    
    # Create the test directory
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        print(f"Created directory: {test_dir}")
    else:
        print(f"Directory already exists: {test_dir}")
    
    # Create sample test files
    test_files = [
        ("test1.txt", "This is a test file for encryption.\nIt contains some sample text."),
        ("test2.txt", "Another test file with different content.\nThis will be encrypted/decrypted."),
    ]
    
    for filename, content in test_files:
        filepath = os.path.join(test_dir, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"Created test file: {filepath}")
        else:
            print(f"File already exists: {filepath}")
    
    print(f"\nTest directory '{test_dir}' is ready for encryption/decryption testing.")
    return test_dir

if __name__ == "__main__":
    create_test_directories()

