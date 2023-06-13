"""Script for merging any number of annotated word pack files into one single,
un-annotated, sorted word pack file. Use as follows:

    python compile-word-packs.py OUTPUT_FILE FILE1 [FILE2 FILE3 ...]
"""

def is_annotation(line: str) -> bool:
    """Return true if a text line is an annotation (ie. begins with #)"""
    if len(line) == 0:
        return False

    return line.strip()[0] == '#'

def remove_annotations(lines: list) -> list:
    """Given a list of text lines, remove all lines that are annotations."""
    return [line for line in lines if not is_annotation(line)]

def remove_blank_lines(lines: list) -> list:
    """Given a list of text lines, remove all whitespace lines or empty lines.
    """
    return [line for line in lines if len(line.strip()) > 0]

def remove_duplicate_lines(lines: list) -> list:
    """Given a list of text lines, remove all extra duplicates of lines."""
    return list(set(lines))

def sort_lines(lines: list) -> list:
    """Given a list of text lines, return a lexicographically-ordered list."""
    return sorted(lines)

import sys
from pathlib import Path

if len(sys.argv) < 3:
    print(f'python {sys.argv[0]} OUTPUT_FILE FILE1 [FILE2 FILE3 ...]')
    print("""
Script for merging any number of annotated word pack files into one single,
un-annotated, sorted word pack file. An "annotation" is defined to be any line
beginning with the # character; these lines are not included in the output file.
The resulting output file is sorted lexicographically and has all blank lines
removed. If any lines are duplicated, the duplicates are also removed.
""")
    sys.exit()

output_path = Path(sys.argv[1])
input_paths = [Path(arg) for arg in sys.argv[2:]]

if output_path.exists():
    confirm_overwrite = input(
        f'WARNING: Output file "{output_path}" already exists - overwrite? (y/n) '
    )

    if confirm_overwrite.lower() != 'y':
        print("Aborting.")
        sys.exit()

input_lines = []

for input_path in input_paths:
    input_wordlist = []
    input_text = input_path.read_text()
    lines = input_text.splitlines()
    lines = [line.strip() for line in lines]
    input_lines.extend(lines)

output_wordlist = input_lines
output_wordlist = remove_annotations(output_wordlist)
output_wordlist = remove_blank_lines(output_wordlist)
output_wordlist = remove_duplicate_lines(output_wordlist)
output_wordlist = sort_lines(output_wordlist)
output_text = '\n'.join(output_wordlist)

output_path.write_text(output_text)
print(f'Saved compiled word pack to "{output_path}".')
print(f'Number of unique items in word pack: {len(output_wordlist)}')
if output_path.suffix != '.txt':
    print(
    f'NOTE: The Codenames file uploader usually expects a filename ending in .txt.'
)
