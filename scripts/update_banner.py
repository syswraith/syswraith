from pathlib import Path
import random
import shutil
import subprocess

BOARD = "YOUR_BOARD_URL"
TMP = Path("/tmp/pinterest")
BANNER = Path("banner.jpg")
README = Path("README.md")

shutil.rmtree(TMP, ignore_errors=True)
TMP.mkdir()

subprocess.run(
    ["gallery-dl", "-D", str(TMP), BOARD],
    check=True,
)

images = [
    p for p in TMP.rglob("*")
    if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
]

if not images:
    raise SystemExit("No images found")

source = random.choice(images)

shutil.copyfile(source, BANNER)

print(f"Using: {source}")

# Keep exactly one banner at the top of README.
content = README.read_text()

marker_start = "<!-- BANNER_START -->"
marker_end = "<!-- BANNER_END -->"

banner = f"""{marker_start}
<img src="banner.jpg" width="100%">
{marker_end}"""

if marker_start in content and marker_end in content:
    start = content.index(marker_start)
    end = content.index(marker_end) + len(marker_end)

    content = content[:start] + banner + content[end:]
else:
    content = banner + "\n\n" + content

README.write_text(content)
