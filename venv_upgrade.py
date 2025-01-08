# Copyright 2025, Mathias Rav <m@git.strova.dk>
# SPDX-License-Identifier: GPL-2+

"""
Recreate a given virtual environment for an older version of Python
with the current version of Python.
"""

import argparse
import glob
import os
import importlib.metadata
import re
import subprocess
import sys


parser = argparse.ArgumentParser(description=__doc__.strip())
parser.add_argument("directory")


def main():
    args = parser.parse_args()
    (sys_path_entry,) = glob.glob(
        os.path.join(args.directory, "lib/python*/site-packages")
    )
    (mo,) = re.finditer("python(\d)\.(\d)", sys_path_entry)
    major, minor = map(int, mo.group(1, 2))
    if (major, minor) == sys.version_info[:2]:
        parser.error(
            "Target venv has same Python version as current: %s.%s" % (major, minor)
        )
    entries = sorted(
        [
            f"{d.name}=={d.version}"
            for d in importlib.metadata.distributions(path=[sys_path_entry])
        ]
    )
    print(" ".join(entries))
    if not entries:
        parser.error("venv contains no installed packages")
    os.rename(args.directory, args.directory + "~")
    subprocess.check_call([sys.executable, "-m", "venv", args.directory])
    subprocess.check_call(
        [os.path.join(args.directory, "bin/pip"), "install"] + entries
    )


if __name__ == "__main__":
    main()
