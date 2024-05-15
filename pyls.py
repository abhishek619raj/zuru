import argparse
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

def load_directory_structure(file_path: str) -> Optional[Dict[str, Any]]:
    """Load directory structure from a JSON file."""
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'r') as f:
        try:
            directory_data = json.load(f)
            return directory_data
        except json.JSONDecodeError:
            return None

def list_directory_contents(directory_data: Dict[str, Any], show_hidden: bool = False) -> List[str]:
    """List directory contents."""
    contents = directory_data.get('contents', [])
    names = [item['name'] for item in contents if show_hidden or not item['name'].startswith('.')]
    return names

def format_long_output(item: Dict[str, Any], human_readable: bool = False) -> str:
    """Format long output for ls -l."""
    permissions = item['permissions']
    size = human_readable_size(item['size']) if human_readable else item['size']
    modified_time = datetime.fromtimestamp(item['time_modified']).strftime('%b %d %H:%M')
    name = item['name']
    return f"{permissions} {size} {modified_time} {name}"

def filter_by_type(contents: List[Dict[str, Any]], filter_type: str) -> List[Dict[str, Any]]:
    """Filter contents by file or directory type."""
    if filter_type == 'file':
        return [item for item in contents if 'contents' not in item]
    elif filter_type == 'dir':
        return [item for item in contents if 'contents' in item]
    else:
        return []

def navigate_path(directory_data: Dict[str, Any], path: str) -> Optional[Dict[str, Any]]:
    """Navigate to a specific path within the directory structure."""
    if not path:
        return directory_data
    
    components = path.split('/')
    current_data = directory_data
    
    for component in components:
        if not isinstance(current_data, dict):
            return None
        
        found = False
        for item in current_data.get('contents', []):
            if item.get('name') == component:
                current_data = item
                found = True
                break
        
        if not found:
            return None
    
    return current_data

def human_readable_size(size: int) -> str:
    """Convert size to a human-readable format."""
    suffixes = ['B', 'KB', 'MB', 'GB']
    suffix_index = 0
    while size >= 1024 and suffix_index < len(suffixes) - 1:
        size /= 1024.0
        suffix_index += 1
    return f"{size:.1f}{suffixes[suffix_index]}"

def main():
    parser = argparse.ArgumentParser(description='List directory contents like ls command')
    parser.add_argument('file', type=str, default='structure.json', nargs='?', help='Path to JSON file')
    parser.add_argument('--all', '-A', action='store_true', help='List all entries including those starting with .')
    parser.add_argument('--long', '-l', action='store_true', help='Use a long listing format')
    parser.add_argument('--reverse', '-r', action='store_true', help='Reverse the order of listing')
    parser.add_argument('--time-sort', '-t', action='store_true', help='Sort by time modified')
    parser.add_argument('--filter', type=str, choices=['file', 'dir'], help='Filter by file or directory type')
    parser.add_argument('--human', '-H', action='store_true', help='Show human-readable sizes')
    parser.add_argument('path', nargs='?', default='', help='Path to navigate within the structure')
    args = parser.parse_args()

    directory_data = load_directory_structure(args.file)
    if not directory_data:
        print(f"error: cannot access '{args.file}': No such file or directory")
        return

    if args.path:
        directory_data = navigate_path(directory_data, args.path)
        if not directory_data:
            print(f"error: cannot access '{args.path}': No such file or directory")
            return

    contents = directory_data.get('contents', [])
    
    if args.filter:
        contents = filter_by_type(contents, args.filter)

    if args.time_sort:
        contents = sorted(contents, key=lambda x: x['time_modified'], reverse=not args.reverse)

    if args.reverse:
        contents.reverse()  # Reverse the list if `-r` option is specified

    for item in contents:
        if not args.all and item['name'].startswith('.'):
            continue
        
        if args.long:
            print(format_long_output(item, args.human))
        else:
            size = human_readable_size(item['size']) if args.human else item['size']
            print(f"{item['name']} {' ' + size if args.human else ''}")

if __name__ == "__main__":
    main()

