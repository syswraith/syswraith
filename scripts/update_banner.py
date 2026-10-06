import os
import random
import subprocess
from pathlib import Path

BOARD = os.environ.get("PINTEREST_BOARD_URL")
if not BOARD:
    raise SystemExit("PINTEREST_BOARD_URL is not set")
COUNT = int(os.environ.get("BANNER_COUNT", "1"))
README = Path("README.md")

MARKER_START = "<!-- BANNER_START -->"
MARKER_END = "<!-- BANNER_END -->"
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

result = subprocess.run(
    ["gallery-dl", "-g", BOARD],
    check=True,
    capture_output=True,
    text=True,
)

urls = [
    line.strip()
    for line in result.stdout.splitlines()
    if line.strip().lower().split("?")[0].endswith(tuple(IMAGE_EXT))
]

if not urls:
    raise SystemExit("No image URLs found on board")

random.shuffle(urls)
picked = urls[: max(1, min(COUNT, len(urls)))]

lines = [MARKER_START]
for url in picked:
    lines.append(f'<img src="{url}" alt="pinterest banner" width="100%">')
lines.append(MARKER_END)
banner = "\n".join(lines)

content = README.read_text()

if MARKER_START in content and MARKER_END in content:
    start = content.index(MARKER_START)
    end = content.index(MARKER_END) + len(MARKER_END)
    content = content[:start] + banner + content[end:]
else:
    content = banner + "\n\n" + content

README.write_text(content)
print(f"Banner set to {len(picked)} image(s) from {BOARD}")
