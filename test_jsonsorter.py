import os
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from jsonsorter import search_and_move_json_files, get_nested_value, create_safe_dirname

class TestJsonSorter(unittest.TestCase):
    """Test cases for the JsonSorter script functionality."""
    
    def setUp(self):
        """Set up temporary directories and test data."""
        # Create temporary directories
        self.test_dir = tempfile.mkdtemp()
        self.dest_dir = tempfile.mkdtemp()
        
        # Create test JSON files
        self.create_test_files()
    
    def tearDown(self):
        """Clean up temporary directories and files."""
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.dest_dir)
    
    def create_test_files(self):
        """Create test JSON files with various data structures."""
        # Test file 1: Simple structure
        with open(os.path.join(self.test_dir, "user1.json"), "w") as f:
            json.dump({
                "name": "John",
                "country": "Italy",
                "age": 35
            }, f)
        
        # Test file 2: Different values
        with open(os.path.join(self.test_dir, "user2.json"), "w") as f:
            json.dump({
                "name": "Maria",
                "country": "Spain",
                "age": 28
            }, f)
        
        # Test file 3: Nested structure
        with open(os.path.join(self.test_dir, "user3.json"), "w") as f:
            json.dump({
                "profile": {
                    "name": "John",
                    "address": {
                        "country": "Italy",
                        "city": "Rome"
                    }
                },
                "age": 42
            }, f)
    
    def test_get_nested_value(self):
        """Test extracting values from nested structures."""
        data = {
            "a": {
                "b": {
                    "c": "value"
                }
            }
        }
        self.assertEqual(get_nested_value(data, "a.b.c"), "value")
        self.assertIsNone(get_nested_value(data, "a.b.d"))
        self.assertIsNone(get_nested_value(data, "x.y.z"))
    
    def test_create_safe_dirname(self):
        """Test creating safe directory names."""
        self.assertEqual(create_safe_dirname("Simple Name"), "Simple_Name")
        self.assertEqual(create_safe_dirname("name/with\\invalid:chars"), "name_with_invalid_chars")
    
    def test_search_by_key(self):
        """Test searching by key and organizing by values."""
        search_and_move_json_files(self.test_dir, self.dest_dir, search_keys=["name"])
        
        # Check if directories were created
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "John")))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "Maria")))
        
        # Check if files were moved
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "John", "user1.json")))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "Maria", "user2.json")))
    
    def test_search_by_value(self):
        """Test searching for specific key-value pairs."""
        search_and_move_json_files(
            self.test_dir, 
            self.dest_dir, 
            search_values={"country": "Italy"}
        )
        
        # Check if directory was created
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "Italy")))
        
        # Check if the correct file was moved
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "Italy", "user1.json")))
        self.assertFalse(os.path.exists(os.path.join(self.dest_dir, "Italy", "user2.json")))
    
    def test_search_with_and_condition(self):
        """Test searching with multiple criteria (AND condition)."""
        search_and_move_json_files(
            self.test_dir, 
            self.dest_dir, 
            search_multi=[{"name": "John", "country": "Italy"}]
        )
        
        # Check if directory was created with default naming
        default_dir = os.path.join(self.dest_dir, "name-John_country-Italy")
        self.assertTrue(os.path.exists(default_dir))
        
        # Check if the correct file was moved
        self.assertTrue(os.path.exists(os.path.join(default_dir, "user1.json")))
    
    def test_custom_folder_format(self):
        """Test custom folder naming format."""
        search_and_move_json_files(
            self.test_dir, 
            self.dest_dir, 
            search_multi=[{"name": "John", "country": "Italy"}],
            folder_format="{name}_from_{country}"
        )
        
        # Check if directory was created with custom naming
        custom_dir = os.path.join(self.dest_dir, "John_from_Italy")
        self.assertTrue(os.path.exists(custom_dir))
        
        # Check if the correct file was moved
        self.assertTrue(os.path.exists(os.path.join(custom_dir, "user1.json")))
    
    def test_nested_structure_search(self):
        """Test searching in nested structures using dot notation."""
        search_and_move_json_files(
            self.test_dir, 
            self.dest_dir, 
            search_values={"profile.address.country": "Italy"}
        )
        
        # Check if directory was created
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "Italy")))
        
        # Check if the correct file was moved
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "Italy", "user3.json")))


if __name__ == "__main__":
    unittest.main()