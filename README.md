Reinstall venv with new Python version
======================================

After upgrading your system Python version,
you may experience that your old venvs (virtual environments) no longer work.
In this case, you need to create a new venv
and install the same packages as in the old venv.
However, you cannot run `pip freeze` in the old venv
(because you uninstalled the version of Python used by that venv).

This script does the equivalent of the following:

* `venv/bin/python3.6 -m pip freeze > /tmp/requirements.txt`
* `mv venv venv~`
* `python3.7 -m venv venv`
* `venv/bin/python3.7 -m pip install -r /tmp/requirements.txt`

(however, without invoking the old `python3.6` and without creating `/tmp/requirements.txt`.)
