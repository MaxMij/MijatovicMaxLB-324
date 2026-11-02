"""Confirm that Azure serves the revision from the current deployment."""

import json
import os
import time
from urllib.error import URLError
from urllib.request import urlopen


def check_deployment(base_url, expected_revision, attempts=12, delay=5):
    url = base_url.rstrip("/") + "/healthz"
    for attempt in range(attempts):
        try:
            with urlopen(url, timeout=10) as response:
                data = json.load(response)
            if data == {"status": "ok", "revision": expected_revision}:
                print(f"Azure liefert den geprüften Commit {expected_revision} aus.")
                return
        except (URLError, TimeoutError, ValueError):
            pass
        if attempt + 1 < attempts:
            time.sleep(delay)
    raise RuntimeError("Azure liefert den erwarteten Commit unter /healthz nicht aus.")


if __name__ == "__main__":
    check_deployment(os.environ["WEBAPP_URL"], os.environ["EXPECTED_REVISION"])
