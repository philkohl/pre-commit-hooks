from __future__ import annotations

import argparse
import typing


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
        filenames: typing.List[str],
        autofix: bool = False
) -> int:
    # Find all added files that are also in the list of files pre-commit tells
    # us about
    print(filenames)
    retv = 0
    try:
        for filename in filenames:
            if autofix:
                print(f"Sort file: '{filename}'")
                sort_file(filename)
                retv = 1
            else:
                print(f"Do not sort file: '{filename}'")
    except Exception as e:
        print(e)
        retv = 1

    return retv


def main(argv: typing.Optional[typing.List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--autofix",
        action="store_true",
        dest="autofix",
        help="Automatically fixes encountered not-pretty-formatted files",
    )
    parser.add_argument(
        "--enforce-all",
        action="store_true",
        dest="enforce_all",
        help="All files",
    )

    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(argv)

    print(f"Args: '{argv}'")
    print(f"Args: '{args}'")
    print(f"Files: '{args.filenames}'")

    return sort_property_files(
        args.filenames,
        autofix=args.autofix
    )


if __name__ == '__main__':
    raise SystemExit(main())
