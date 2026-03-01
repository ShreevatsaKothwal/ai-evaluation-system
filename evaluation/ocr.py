import pytesseract
from PIL import Image

# Tell Python where Tesseract is installed (Mac path)
# pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()