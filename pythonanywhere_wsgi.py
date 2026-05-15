import os
import sys


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_ROOT = os.path.join(os.path.expanduser("~"), ".smart-campus-data")

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("SMART_CAMPUS_DATA_ROOT", DATA_ROOT)
os.environ.setdefault("SMART_CAMPUS_MEDIA_ROOT", os.path.join(DATA_ROOT, "media"))
os.environ.setdefault("SMART_CAMPUS_DB", os.path.join(DATA_ROOT, "attendance.db"))

from server import app as application
