from pathlib import Path
import random
import re
import shutil

README = Path("README.md")
BANNERS = Path("banners")

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

images = [
    p for p in BANNERS.rglob("*")
    if p.suffix.lower() in IMAGE_EXTENSIONS
]

if not images:
    raise SystemExit("No images found")

image = random.choice(images)

target = BANNERS / image.name

if image != target:
    shutil.copy2(image, target)

banner = f"""<!-- BANNER_START -->
<img src="{target}" width="100%" />
<!-- BANNER_END -->"""

readme = README.read_text()

updated = re.sub(
    r"<!-- BANNER_START -->.*?<!-- BANNER_END -->",
    banner,
    readme,
    flags=re.DOTALL,
)

README.write_text(updated)
