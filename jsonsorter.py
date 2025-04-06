#!/usr/bin/env python3
"""
JsonSorter - Intelligent JSON File Organizer

This script searches through JSON files for specific key-value patterns
and organizes them into categorized folders based on their content.
"""
import json
import os
import shutil
import argparse
from pathlib import Path


def search_and_move_json_files(source_dir, dest_dir=None, search_keys=None, search_values=None, 
                               search_multi=None, folder_format=None):
    """
    Search JSON files for specific keys and values, and move them to categorized folders.
    
    Args:
        source_dir (str): Directory containing JSON files to search
        dest_dir (str, optional): Base directory where to move files. If None, creates inside source_dir
        search_keys (list, optional): List of keys to search for in JSON files (categorize by their values)
        search_values (dict, optional): Dictionary mapping keys to values to search for (OR condition)
        search_multi (list, optional): List of dictionaries for AND condition searching
        folder_format (str, optional): Format for folder names when using search_multi. Use {key} placeholders.
    """
    # If no destination directory provided, create one inside source directory
    if dest_dir is None:
        dest_dir = os.path.join(source_dir, "categorized_files")
    
    # Ensure destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Get all JSON files in source directory
    json_files = [f for f in os.listdir(source_dir) if f.endswith('.json')]
    print(f"Found {len(json_files)} JSON files in {source_dir}")
    
    files_moved = 0
    for filename in json_files:
        file_path = os.path.join(source_dir, filename)
        
        # Read JSON file
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print(f"Error: {filename} is not a valid JSON file. Skipping.")
            continue
        except Exception as e:
            print(f"Error reading {filename}: {e}. Skipping.")
            continue
        
        # Case 1: Search for keys only (move to folders named after values)
        if search_keys and not search_values and not search_multi:
            for key in search_keys:
                # Extract value using the key path
                value = get_nested_value(data, key)
                if value is None:
                    continue
                
                # Convert value to string for directory name
                if isinstance(value, (dict, list)):
                    print(f"Warning: Value for key '{key}' in {filename} is complex. Skipping.")
                    continue
                
                value_str = str(value)
                safe_dir_name = create_safe_dirname(value_str)
                target_dir = os.path.join(dest_dir, safe_dir_name)
                
                # Create target directory and copy file
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                
                target_path = os.path.join(target_dir, filename)
                shutil.copy2(file_path, target_path)
                print(f"Copied {filename} to {target_dir} (matched key: {key}, value: {value_str})")
                files_moved += 1
        
        # Case 2: Search for specific key-value pairs (OR condition)
        elif search_values and not search_multi:
            for key, target_value in search_values.items():
                # Extract value using the key path
                value = get_nested_value(data, key)
                if value is None:
                    continue
                
                # Check if the value matches the target value
                value_str = str(value)
                if value_str == target_value:
                    safe_dir_name = create_safe_dirname(target_value)
                    target_dir = os.path.join(dest_dir, safe_dir_name)
                    
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                    
                    target_path = os.path.join(target_dir, filename)
                    shutil.copy2(file_path, target_path)
                    print(f"Copied {filename} to {target_dir} (matched key: {key}, value: {target_value})")
                    files_moved += 1
                    break  # Move to next file after first match
        
        # Case 3: Search for multiple criteria (AND condition)
        elif search_multi:
            for criteria_set in search_multi:
                all_match = True
                match_values = {}
                
                # Check if all criteria in this set match
                for key, target_value in criteria_set.items():
                    value = get_nested_value(data, key)
                    if value is None or str(value) != target_value:
                        all_match = False
                        break
                    match_values[key] = target_value
                
                if all_match:
                    # Determine folder name based on format or default concatenation
                    if folder_format:
                        try:
                            folder_name = folder_format.format(**match_values)
                        except KeyError:
                            # Fallback if format string contains keys not in match_values
                            folder_name = "_".join(f"{k}-{v}" for k, v in match_values.items())
                    else:
                        folder_name = "_".join(f"{k}-{v}" for k, v in match_values.items())
                    
                    safe_dir_name = create_safe_dirname(folder_name)
                    target_dir = os.path.join(dest_dir, safe_dir_name)
                    
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                    
                    target_path = os.path.join(target_dir, filename)
                    shutil.copy2(file_path, target_path)
                    criteria_desc = ", ".join(f"{k}={v}" for k, v in match_values.items())
                    print(f"Copied {filename} to {target_dir} (matched criteria: {criteria_desc})")
                    files_moved += 1
                    break  # Move to next file after first match set
    
    print(f"Operation complete. {files_moved} files were moved.")


def get_nested_value(data, key_path):
    """Extract a value from nested dictionaries using a dot-separated key path."""
    keys = key_path.split('.')
    value = data
    try:
        for k in keys:
            value = value[k]
        return value
    except (KeyError, TypeError):
        return None


def create_safe_dirname(name):
    """Create a safe directory name by replacing invalid characters."""
    return "".join(c if c.isalnum() or c in ['-', '_'] else '_' for c in name)


def main():
    parser = argparse.ArgumentParser(
        description='JsonSorter: Search and organize JSON files into categorized folders based on their content.'
    )
    parser.add_argument('source', help='Source directory containing JSON files')
    parser.add_argument('--destination', '-d', help='Destination base directory (default: creates "categorized_files" in source directory)')
    parser.add_argument('--keys', '-k', nargs='+', help='Keys to search for in JSON files (use dot notation for nested keys)')
    parser.add_argument('--find', '-f', nargs='+', help='Key-value pairs to search for in format key=value (OR condition)')
    parser.add_argument('--and', '-a', dest='and_criteria', nargs='+', action='append',
                      help='Multiple key-value pairs that must all match (AND condition). Use multiple --and arguments for different sets.')
    parser.add_argument('--format', help='Format string for folder names when using --and. Use {key} placeholders, e.g. "{name}_from_{country}"')
    
    args = parser.parse_args()
    
    # Confirm source path exists
    source_path = Path(args.source)
    if not source_path.exists() or not source_path.is_dir():
        print(f"Error: Source directory '{args.source}' does not exist or is not a directory")
        return
    
    # Check if at least one search parameter is provided
    if not args.keys and not args.find and not args.and_criteria:
        print("Error: You must specify at least one of --keys, --find, or --and parameters")
        return
    
    # Parse key-value pairs if provided
    search_values = {}
    if args.find:
        for item in args.find:
            if '=' in item:
                key, value = item.split('=', 1)
                search_values[key] = value
            else:
                print(f"Warning: Ignoring invalid key-value pair format: {item}")
    
    # Parse AND criteria if provided
    search_multi = []
    if args.and_criteria:
        for criteria_group in args.and_criteria:
            criteria_dict = {}
            for item in criteria_group:
                if '=' in item:
                    key, value = item.split('=', 1)
                    criteria_dict[key] = value
                else:
                    print(f"Warning: Ignoring invalid key-value pair format: {item}")
            if criteria_dict:
                search_multi.append(criteria_dict)
    
    # Run the search and move operation
    search_and_move_json_files(
        args.source,
        args.destination,
        args.keys,
        search_values if search_values else None,
        search_multi if search_multi else None,
        args.format
    )


if __name__ == "__main__":
    main()