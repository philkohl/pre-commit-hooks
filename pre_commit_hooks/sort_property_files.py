from __future__ import annotations

import argparse
from typing import Sequence

from pre_commit_hooks.util import added_files

class PropertyEntry:
    def __init__(self, input: str):
        splitted = input.split("=")

        if len(splitted) < 2:
            raise Exception(f"'{input}' not well formatted!")

        self.key = splitted[0]
        self.value = "=".join(splitted[1:])

    def __lt__(self, other):
        return self.key < other.key


def sort_file(filename):
    entries = []
    with open(filename, encoding="UTF-8") as f:
        lines = [line for line in f]

    for l in lines:
        entries.append(PropertyEntry(l))

    sorted_entries = sorted(entries)

    with open(filename, "w", encoding="UTF-8") as f:
        f.writelines([f"{e.key}={e.value}" for e in sorted_entries])


def sort_property_files(
        filenames: Sequence[str],
        *,
        enforce_all: bool = False,
) -> int:
    # Find all added files that are also in the list of files pre-commit tells
    # us about
    retv = 0
    filenames_filtered = set(filenames)

    if not enforce_all:
        filenames_filtered &= added_files()

    print("Sort files", filenames_filtered)
    try:
        for filename in filenames_filtered:
            print(f"Sort file: '{filename}'")
            sort_file(filename)
            retv = 1
    except Exception as e:
        print(e)
        retv = 1

    return retv


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
    )
    parser.add_argument(
        '--enforce-all', action='store_true',
        help='Enforce all files are checked, not just staged files.',
    )
    args = parser.parse_args(argv)

    print(f"Args: '{argv}'")
    return sort_property_files(
        args.filenames,
        enforce_all=args.enforce_all,
    )


if __name__ == '__main__':
    raise SystemExit(main())
