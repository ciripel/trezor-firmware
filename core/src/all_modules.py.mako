# generated from resources.py.mako
# do not edit manually!
# flake8: noqa
# fmt: off
<%
from pathlib import Path
from itertools import chain

THIS = Path(local.filename).resolve()
SRCDIR = THIS.parent

PATTERNS = (
    "*.py",
    "trezor/**/*.py",
    "apps/**/*.py",
)

pyfiles = chain.from_iterable(sorted(SRCDIR.glob(p)) for p in PATTERNS)
%>\
from trezor.utils import halt

# this module should not be part of the build, its purpose is only to add missed Qstrings
halt("Tried to import excluded module.")

% for pyfile in pyfiles:
<%
pyfile = pyfile.relative_to(SRCDIR)
if pyfile.name == "__init__.py":
    import_name = str(pyfile.parent)
else:
    import_name = str(pyfile.with_suffix(""))
import_name = import_name.replace("/", ".")
%>\
import ${import_name}
% endfor
