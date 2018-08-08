# Copyright 2018, Mathias Rav <m@git.strova.dk>
# SPDX-License-Identifier: GPL-2+

"""
Recreate a given virtual environment for an older version of Python
with the current version of Python.
"""

import argparse
import glob
import os
import pkg_resources
import re
import subprocess
import sys
import venv


parser = argparse.ArgumentParser(
    description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter()
)
parser.add_argument("directory")


def main():
    args = parser.parse_args()
    sys_path_entry, = glob.glob(
        os.path.join(args.directory, "lib/python*/site-packages")
    )
    mo, = re.finditer("python(\d)\.(\d)", sys_path_entry)
    major, minor = map(int, mo.group(1, 2))
    if (major, minor) == sys.version_info[:2]:
        parser.error(
            "Target venv has same Python version as current: %s.%s" % (major, minor)
        )
    entries = list(pkg_resources.find_on_path(None, sys_path_entry))
    print(entries)
    if not entries:
        parser.error("venv contains no installed packages")
    os.rename(args.directory, args.directory + "~")
    venv.main([args.directory])
    subprocess.check_call(
        [os.path.join(args.directory, "bin/pip"), "install"]
        + ["%s==%s" % (o.project_name, o.version) for o in entries]
    )


if __name__ == "__main__":
    main()
