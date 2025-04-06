# JsonSorter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)

**JsonSorter** is an intelligent file organizer that searches through JSON files for specific patterns and organizes them into categorized folders based on their content.

## Features

- **Smart Content Searching**: Find JSON files based on their content, not just filenames
- **Nested Field Support**: Easily search for values in nested JSON structures using dot notation
- **Flexible Search Options**:
  - Simple categorization by field values
  - Search for specific key-value pairs (OR condition)
  - Search for multiple criteria that must all match (AND condition)
- **Custom Folder Naming**: Format destination folder names using placeholders

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/jsonsorter.git

# Navigate to the project directory
cd jsonsorter

# Make the script executable (Linux/Mac)
chmod +x jsonsorter.py
```

## Usage

### Basic Usage

```bash
python jsonsorter.py /path/to/json/files --keys name
```

This will search through all JSON files in the specified directory and organize them into folders based on the value of the "name" field.

### Search Options

#### Search by Key (Categorize by Value)

Organize files into folders named after the values found for specific keys:

```bash
python jsonsorter.py /path/to/json/files --keys name category
```

For nested fields, use dot notation:

```bash
python jsonsorter.py /path/to/json/files --keys user.profile.name metadata.category
```

#### Search for Specific Values

Find files that match specific key-value pairs (OR condition):

```bash
python jsonsorter.py /path/to/json/files --find name=John
```

#### Search with Multiple Criteria (AND Condition)

Find files that match all specified criteria:

```bash
python jsonsorter.py /path/to/json/files --and name=John country=Italy
```

#### Multiple Sets of Criteria

Find files matching either of multiple criteria sets:

```bash
python jsonsorter.py /path/to/json/files --and name=John country=Italy --and name=Maria country=Spain
```

### Custom Destination Directory

By default, files are moved to a "categorized_files" folder in the source directory. You can specify a different destination:

```bash
python jsonsorter.py /path/to/json/files --destination /path/to/output --keys name
```

### Custom Folder Naming Format

For AND-condition searches, you can customize the folder naming format:

```bash
python jsonsorter.py /path/to/json/files --and name=John country=Italy --format "{name}_from_{country}"
```

This would create folders like "John_from_Italy" instead of the default "name-John_country-Italy".

## Examples

### Example 1: Organize User Data by Country

If you have user data in JSON files and want to organize them by country:

```bash
python jsonsorter.py users_data/ --keys address.country
```

### Example 2: Find Data for Specific Demographics

Find data for males over 30 years old:

```bash
python jsonsorter.py users_data/ --and gender=male age=30+ --format "{gender}_age_{age}"
```

### Example 3: Organize Products by Category and Brand

```bash
python jsonsorter.py products/ --keys category brand
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.