#! /usr/bin/env python3
"""
This script is used to test the materials.

Every gem5 script should have a docs string that explains what the script does
how to run it.

You should format the "how to run it" with a `$` to indicate a shell command.
After `$`, there should be one of the gem5 binaries available in the
docker container for the codespace (e.g., `gem5`, `gem5-mesi`, `gem5-vega`).

When running this script, it takes one parameter which is the path to the
script it should test. It parses that script for a docstring and the `$ gem5`
command. This script then runs the command and checks for either a 0 exit code
or for the string found after the `$` in the docstring.
"""

import argparse
from pathlib import Path
import re
import subprocess
import sys


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("script", type=str)
    arg_parser.add_argument("--verbose", action="store_true")

    args = arg_parser.parse_args()

    with open(args.script, "r") as f:
        script = f.read()

    if '"""' not in script:
        print("Warning: No docstring found")
        return 2

    docstring = script.split('"""')[1]

    if "$ gem5" not in docstring:
        print("Warning: No gem5 command found in docstring")
        return 2

    if "$ gem5-mesi" in docstring:
        gem5_command = (
            "gem5-mesi "
            + docstring.split("$ gem5-mesi")[1].split("\n")[0].strip()
        )
    elif "$ gem5-vega" in docstring:
        gem5_command = (
            "gem5-vega "
            + docstring.split("$ gem5-vega")[1].split("\n")[0].strip()
        )
    else:
        gem5_command = (
            "gem5 " + docstring.split("$ gem5")[1].split("\n")[0].strip()
        )

    expected_output = docstring.split("$ gem5")[1].split("\n")[1].strip()
    expected_output.replace("...", ".*")

    print(f"Running: {gem5_command}")

    # run the command and get the stdout
    result = subprocess.run(
        gem5_command,
        shell=True,
        capture_output=True,
        text=True,
        cwd=Path(f"{args.script}").parent,
    )

    if result.returncode != 0:
        print(f"Error: {result.returncode}")
        print(result.stderr)
        return 1

    if not re.search(expected_output, result.stdout):
        print("Error: output does not match expected output")
        print(f"Command output: {result.stdout}")
        print(f"Expected output: {expected_output}")
        return 1

    print("Success!")

    if args.verbose:
        print(result.stdout)
        print(result.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
