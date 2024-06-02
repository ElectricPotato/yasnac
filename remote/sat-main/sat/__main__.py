import sys, traceback
from . import main

rc = 1
try:
    rc = main()
except Exception:
    traceback.print_exc(file=sys.stderr)
sys.exit(rc)
