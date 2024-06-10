## Overview

This script is designed to compare two JSON files by a specified key and identify the differences between them. It loads the JSON files, splits them by a root entry, and checks for differences based on the specified ID. The results include identifying common IDs, IDs present only in the first file, and IDs present only in the second file. Additionally, the script performs a deep comparison for each matching element in the base file and writes the differences to separate JSON files.

## Key Variables

- `ID = "pmCampaignId"`: The key used to sort and identify the records in the JSON files.
- `IGNORE_DICTIONARY_ITEMS_REMOVED = False`: A flag to determine whether to ignore dictionary items that are removed.
- `IGNORE_PATH = []`: A list of paths to ignore during the comparison.

## Functions

### `loadFile_and_split_by_root_entry`

This function loads a JSON file and splits it by a root entry.

**Parameters:**
- `name` (str): A name to identify the file.
- `file_path` (str): The path to the JSON file.
- `id_key` (str): The key used to identify records.

**Returns:**
- A list of entries split by the root entry.

### `checkDiff`

This function checks for differences between two lists of entries.

**Parameters:**
- `fileListBase` (list): The base list of entries to compare.
- `fileListToCompare` (list): The list of entries to compare against the base list.
- `id_key` (str): The key used to identify records.
- `ignore_removed` (bool): Whether to ignore dictionary items that are removed.
- `ignore_path` (list): A list of paths to ignore during the comparison.

**Returns:**
- Three files:
    - `common_ids.txt`: IDs present in both files.
    - `only_in_first_ids.txt`: IDs present only in the first file.
    - `only_in_second_ids.txt`: IDs present only in the second file.
- JSON files for each matching element with deep differences.

### `deep_compare_and_write`

This function performs a deep comparison for each matching element and writes the differences to a JSON file.

**Parameters:**
- `base_entry` (dict): The base entry to compare.
- `compare_entry` (dict): The entry to compare against the base entry.
- `id_key` (str): The key used to identify records.

**Returns:**
- A JSON file with the differences for each matching element.

## Usage

1. Ensure the necessary JSON files are available at the specified paths.
2. Update the `ID`, `IGNORE_DICTIONARY_ITEMS_REMOVED`, and `IGNORE_PATH` variables as needed.
3. Call the `loadFile_and_split_by_root_entry` function to load and split the JSON files:
    ```python
    fileListBase = loadFile_and_split_by_root_entry("nemo", "/path/to/first/file.json", ID)
    fileListToCompare = loadFile_and_split_by_root_entry("grpc", "/path/to/second/file.json", ID)
    ```
4. Call the `checkDiff` function to compare the lists and generate the result files:
    ```python
    checkDiff(fileListBase, fileListToCompare, ID, IGNORE_DICTIONARY_ITEMS_REMOVED, IGNORE_PATH)
    ```
5. The results will be written to `common_ids.txt`, `only_in_first_ids.txt`, and `only_in_second_ids.txt`.
6. Deep differences for each matching element will be written to separate JSON files.

## Example

```python
# Key to sort and to identify the records
ID = "pmCampaignId"
IGNORE_DICTIONARY_ITEMS_REMOVED = False
IGNORE_PATH = []

fileListBase = loadFile_and_split_by_root_entry("nemo", "/Users/jramirezlondono/Documents/nemo-luis.json", ID)
fileListToCompare = loadFile_and_split_by_root_entry("grpc", "/Users/jramirezlondono/Documents/grpc-luis.json", ID)

checkDiff(fileListBase, fileListToCompare, ID, IGNORE_DICTIONARY_ITEMS_REMOVED, IGNORE_PATH)
```

This will generate the following files:
- `common_ids.txt`
- `only_in_first_ids.txt`
- `only_in_second_ids.txt`
- JSON files for each matching element with detailed differences.

## Requirements

Ensure you have the necessary permissions to read the JSON files and write the output files.

---

## Additional Details

### Deep Comparison using `DeepDiff`

The `checkDiff` function includes a deep comparison using the `DeepDiff` library for each matching element in the base file. This deep comparison identifies any changes in the structure or values of the JSON objects.

**Example Implementation:**

```python
from deepdiff import DeepDiff
import json

def deep_compare_and_write(base_entry, compare_entry, id_key):
    differences = DeepDiff(base_entry, compare_entry, ignore_order=True).to_dict()
    file_name = f"diff_{base_entry[id_key]}.json"
    with open(file_name, 'w') as f:
        json.dump(differences, f, indent=4)
```

This function will generate a JSON file for each ID with the detailed differences between the matching elements.

---