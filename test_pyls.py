import json
from pyls import (
    load_directory_structure,
    list_directory_contents,
    filter_by_type,
    navigate_path,
)



# Sample directory structure for testing
sample_directory_data = {
    "contents": [
        {"name": "file1.txt", "permissions": "rw-r--r--", "size": 1024, "time_modified": 1621047520},
        {"name": "file2.txt", "permissions": "rw-r--r--", "size": 2048, "time_modified": 1621047600},
        {"name": "dir1", "permissions": "rwxr-xr-x", "size": 4096, "time_modified": 1621047700, "contents": []},
    ]
}


def test_load_directory_structure(tmp_path):
    # Create a temporary JSON file with sample data
    test_file = tmp_path / "test_structure.json"
    with open(test_file, "w") as f:
        json.dump(sample_directory_data, f)

    # Test loading the directory structure from the temporary file
    loaded_data = load_directory_structure(test_file)
    assert loaded_data == sample_directory_data


def test_list_directory_contents():
    # Test listing directory contents
    names = list_directory_contents(sample_directory_data)
    expected_names = ["file1.txt", "file2.txt", "dir1"]
    assert names == expected_names

    # Test listing directory contents including hidden files
    all_names = list_directory_contents(sample_directory_data, show_hidden=True)
    assert all_names == expected_names


def test_filter_by_type():
    # Test filtering by file type
    filtered_files = filter_by_type(sample_directory_data["contents"], "file")
    assert len(filtered_files) == 2

    # Test filtering by directory type
    filtered_dirs = filter_by_type(sample_directory_data["contents"], "dir")
    assert len(filtered_dirs) == 1


def test_navigate_path():
    # Test navigating to an existing path within the directory structure
    path = "dir1"
    navigated_data = navigate_path(sample_directory_data, path)
    assert navigated_data["name"] == "dir1"

    # Test navigating to a non-existing path
    invalid_path = "dir2"
    navigated_data = navigate_path(sample_directory_data, invalid_path)
    assert navigated_data is None



