"""
Generates print-ready QR codes - ONE per machine, labeled with the machine name.
Scanning a code opens product.html?m=<id>, which shows Catalog / Video / Contact
as three cards on one page.

Run again after deploying to Vercel with BASE_URL set to the live domain to produce
the final print versions (same filenames, so nothing else needs to change).
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# ---- CONFIG ----
# Change this to your live Vercel URL after deployment, e.g. "https://your-app.vercel.app"
BASE_URL = "http://localhost:8080"

OUTPUT_DIR = "qr-codes"

MACHINES = [
    {"id": "dy-r9", "name": "DY R9"},
    {"id": "fb450", "name": "FB450"},
    {"id": "pl-puller", "name": "PL PULLER"},
]


def load_font(size):
    for candidate in ("segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_labeled_qr(data, title):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    qr_w, qr_h = qr_img.size
    label_h = 60
    canvas = Image.new("RGB", (qr_w, qr_h + label_h), "white")
    canvas.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(canvas)
    font = load_font(38)
    bbox = draw.textbbox((0, 0), title, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((qr_w - w) / 2, qr_h + 10), title, font=font, fill="black")

    return canvas


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated = []

    for machine in MACHINES:
        url = f"{BASE_URL}/product.html?m={machine['id']}"
        img = make_labeled_qr(url, machine["name"])
        filename = f"{machine['id']}.png"
        path = os.path.join(OUTPUT_DIR, filename)
        img.save(path)
        generated.append((path, url))

    print(f"Generated {len(generated)} QR codes in '{OUTPUT_DIR}/' using BASE_URL={BASE_URL}\n")
    for path, url in generated:
        print(f"  {path}  ->  {url}")


if __name__ == "__main__":
    main()
