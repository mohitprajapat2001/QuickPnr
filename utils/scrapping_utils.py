# Base PNR Scrapping Utilities
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.constants import ElementTypes, PnrConstants, IDs
from pnr.constants import ScrappingConstants
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.image_filtering import CaptchaImageFiltering
from datetime import datetime
from time import sleep
from utils.exceptions import PNRNotFound


class PnrScrapping:
    """Scrapping Class Implemented for PNR Scrapping"""

    def __init__(self, pnr: int):
        self.pnr = pnr
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)
        self.driver.get(PnrConstants.SCRAPPING_URL)
        self.wait = WebDriverWait(self.driver, 10)
        self.pnr_input = self.wait.until(
            EC.presence_of_element_located((By.ID, IDs.PNR_INPUT))
        )
        self.capcha_modal_btn = self.wait.until(
            EC.presence_of_element_located((By.ID, IDs.CAPTCHA_MODAL))
        )

    def fetch_element_by_id(self, ID):
        """Fetch Element with IDs"""
        return self.wait.until(EC.presence_of_element_located((By.ID, ID)))

    def get_tag_name(self, element):
        """Return Element tag name"""
        return element.tag_name

    def get_element_attribute(self, element, attribute):
        """Return Element Attribute"""
        return element.get_attribute(attribute)

    def enter_pnr_and_open_captcha_modal_condition(self):
        """Check Conditions for PNR Scrapping"""
        if self.get_tag_name(
            self.pnr_input
        ) == ElementTypes.INPUT and self.get_element_attribute(
            self.pnr_input, ElementTypes.TYPE
        ) in [
            ElementTypes.TEXT,
            ElementTypes.NUMBER,
        ]:
            if (
                self.get_tag_name(self.capcha_modal_btn) == ElementTypes.INPUT
                and self.get_element_attribute(self.capcha_modal_btn, ElementTypes.TYPE)
                == ElementTypes.BUTTON
            ):
                self.pnr_input.send_keys(self.pnr)
                print(ScrappingConstants.PNR_NUMBER_ENTERED)
                self.capcha_modal_btn.click()
                if self.capcha_modal_btn.is_displayed():
                    print(ScrappingConstants.CAPTCHA_MODEL_OPENED)
        else:
            raise Exception(ScrappingConstants.INVALID_PAGE)

    def handle_captcha_image(self):
        """Handle Captcha Image"""
        image = self.fetch_element_by_id(IDs.CAPTCHA_IMAGE)
        self.driver.save_screenshot(ElementTypes.PAGE_SS)
        captcha = CaptchaImageFiltering(image)
        solved_captcha = captcha.get_solved_capcha_from_image()
        captcha_input = self.fetch_element_by_id(IDs.INPUT_CACHE)
        captcha_input.send_keys(solved_captcha)
        captcha_submit = self.fetch_element_by_id(IDs.CAPTCHA_SUBMIT)
        captcha_submit.click()

    def __call__(self, *args, **kwargs):
        try:
            self.enter_pnr_and_open_captcha_modal_condition()
            # Sleep 4 Seconds Allows Modal to Load Captcha & Open Modal
            sleep(4)
            self.handle_captcha_image()
            # Sleep 4 Seconds Allows Data to Load
            sleep(4)
            data = FormatData(self.driver.find_element(By.ID, "pnrOutputDiv"))()
            data["pnr"] = self.pnr
            return data
        except Exception as err:
            error = self.driver.find_element(By.ID, "errorMessage")
            if error:
                raise PNRNotFound(error.get_attribute("innerHTML"))
            else:
                raise Exception(err)
        finally:
            self.driver.quit()
            print("Driver Closed Successfully")


class FormatData:
    """Retrieve Data from Driver"""

    def __init__(self, output):
        self.output = output
        self.journey_data = self.output.find_element(By.ID, "journeyDetailsTable")

    def get_pnr_details(self):
        """Retreive PNR Details from Driver"""
        # Retreive Journey Details Slicing data to ignore: headers
        journey_details = self.journey_data.find_elements(By.TAG_NAME, "tr")[1:]
        for row in journey_details:
            if row:
                (
                    train_number,
                    train_name,
                    boarding_date,
                    frm,
                    to,
                    reserved_upto,
                    boarding_point,
                    class_,
                ) = row.find_elements(By.TAG_NAME, "td")
                journey_data = {
                    "train_number": train_number.text,
                    "train_name": train_name.text,
                    "boarding_date": datetime.strptime(
                        boarding_date.text, "%d-%m-%Y"
                    ).isoformat(),
                    "reserved_from": frm.text,
                    "reserved_to": to.text,
                    "reserved_upto": reserved_upto.text,
                    "boarding_point": boarding_point.text,
                    "reserved_class": class_.text,
                }
                return journey_data

    def get_other_details(self):
        """Retreive Other Details from Driver"""
        other_details = self.output.find_element(By.ID, "otherDetailsTable")
        other_details_row = other_details.find_elements(By.TAG_NAME, "tr")[1]
        (
            total_fare,
            charting_status,
            remarks,
            train_status,
        ) = other_details_row.find_elements(By.TAG_NAME, "td")
        other_data = {
            "fare": float(total_fare.text),
            "charting_status": charting_status.text,
            "remarks": remarks.text,
            "train_status": train_status.text,
        }
        return other_data

    def get_passenger_details(self):
        """Retreive Passenger Details from Driver"""
        passenger_details = self.output.find_element(By.ID, "psgnDetailsTable")
        passenger_details_rows = passenger_details.find_elements(By.TAG_NAME, "tr")[1:]
        passenger_data = []
        for row in passenger_details_rows:
            (
                passenger_number,
                booking_status,
                current_status,
                coach_position,
            ) = row.find_elements(By.TAG_NAME, "td")
            passenger_data.append(
                {
                    "name": passenger_number.text,
                    "booking_status": booking_status.text,
                    "current_status": current_status.text,
                    "coach_position": coach_position.text,
                }
            )
        return passenger_data

    def __call__(self):
        journey_data = self.get_pnr_details()
        passenger_data = self.get_passenger_details()
        journey_data.update(self.get_other_details())
        return {
            **journey_data,
            "passengers_details": passenger_data,
        }
