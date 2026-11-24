"""Runs every page of the site headless and reports exceptions. Usage: python tools/smoke_test.py"""
import pathlib
import sys

from streamlit.testing.v1 import AppTest

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["views/home.py", "views/world.py", "views/chronicle.py", "views/media.py",
         "views/devlog.py", "views/download.py", "views/support.py"]

failed = False
for page in PAGES:
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    at.switch_page(page)
    at.run()
    errors = [e.value for e in at.exception]
    print(f"{'FAIL' if errors else 'ok  '} {page}" + (f": {errors[0]}" if errors else ""))
    failed |= bool(errors)
sys.exit(1 if failed else 0)
