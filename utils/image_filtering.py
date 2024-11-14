from PIL import Image
import pytesseract
from utils.constants import ElementTypes
import re


class CaptchaImageFiltering:
    """Filter Pnr Image"""

    def __init__(self, image):
        """Captcha Image Filtering Instances"""
        self.image = image

    def get_image_location(self):
        """Retreive Image Location"""
        return self.image.location

    def get_image_size(self):
        """Retreive Image Size"""
        return self.image.size

    def get_string_from_image(self):
        """Return Text From Image"""
        return pytesseract.image_to_string(ElementTypes.CAPTCHA_IMAGE_TEMPORARY)

    def crop_captcha_from_ss(self):
        """Crop Captcha from Whole SS"""
        location = self.get_image_location()
        size = self.get_image_size()
        ss = Image.open(ElementTypes.PAGE_SS)
        left = location["x"]
        top = location["y"]
        right = location["x"] + size["width"]
        bottom = location["y"] + size["height"]
        im = ss.crop((left, top, right, bottom))
        im.save(ElementTypes.CAPTCHA_IMAGE_TEMPORARY)
        return self.get_string_from_image()

    def get_solved_capcha_from_image(self):
        """Return Solved Capcha from Filtered Image"""
        try:
            counter = 5
            while counter >= 0:
                counter -= 1
                image = self.crop_captcha_from_ss()
                pattern = r"\d+\s*[\+\-\*\/]\s*\d+\s*="
                matches = re.findall(pattern, image)
                if matches:
                    return eval(matches[0][:-1])
                else:
                    continue
        except Exception:
            raise Exception("Captcha Not Solved")
