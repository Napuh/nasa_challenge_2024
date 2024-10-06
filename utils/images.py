import base64
from pathlib import Path


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def img_to_html(img_path):
    img_html = f"<img src='data:image/png;base64,{img_to_bytes(img_path)}' class='img-fluid'>"
    return img_html
