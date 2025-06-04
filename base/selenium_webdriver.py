import traceback
from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import utilities.custom_logger as cl
#import utilities.exel_logger as ex
import logging
import time
import os


class SeleniumDriver:
    log_exel = cl.custom_logger(logging.DEBUG)
    #log = ex.excel_logger()

    def __init__(self, driver):
        self.driver = driver

    def screen_shot(self, resultMessage):
        """
        Takes screenshot of the current open web page
        """
        file_name = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshot_directory = "../screenshots/"
        relative_file_name = screenshot_directory + file_name
        current_directory = os.path.dirname(__file__)
        destination_file = os.path.join(current_directory, relative_file_name)
        destination_directory = os.path.join(current_directory, screenshot_directory)

        try:
            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)
            self.driver.save_screenshot(destination_file)
            self.log_exel.info("Screenshot save to directory: " + destination_file)
        except:
            self.log_exel.error("### Exception Occurred when taking screenshot")
            print_stack()

    def get_title(self):
        self.log_exel.info('Getting data for the Title')
        return self.driver.title

    def get_by_type(self, locator_type):
        locator_type = locator_type.lower()
        if locator_type == "id":
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "link":
            return By.LINK_TEXT
        elif locator_type == 'tag':
            return By.TAG_NAME
        else:
            self.log_exel.info("Locator type " + locator_type +
                               " not correct/supported")
        return False

    def get_element(self, locator, locator_type="xpath"):
        element = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_element(by_type, locator)
            self.log_exel.info("Element found with locator: " + locator +
                               " and  locatorType: " + locator_type)
        except:
            self.log_exel.info("Element not found with locator: " + locator +
                               " and locatorType: " + locator_type)
            self.log_exel.error("Exception Caught: {}".format(traceback.format_exc()))
            self.log_exel.error("".join(traceback.format_stack()))
        return element

    def get_element_list(self, locator, locator_type="xpath"):
        """
        Get list of elements
        """
        locator_type = locator_type.lower()
        by_type = self.get_by_type(locator_type)
        elements = self.driver.find_elements(by_type, locator)
        if len(elements) > 0:
            self.log_exel.info("Element list FOUND with locator: " + locator +
                               " and locatorType: " + locator_type)
        else:
            self.log_exel.info("Element list NOT FOUND with locator: " + locator +
                               " and locatorType: " + locator_type)
        return elements

    def element_click(self, locator="", locatorType="xpath", element=None):
        """
        Click on an element -> MODIFIED
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locatorType)
            element.click()
            self.log_exel.info("Clicked on element with locator: " + locator +
                               " locatorType: " + locatorType)
        except:
            self.log_exel.info("Cannot click on the element with locator: " + locator +
                               " locatorType: " + locatorType)
            print_stack()

    def send_keys(self, data, locator="", locatorType="xpath", element=None):
        """
        Send keys to an element -> MODIFIED
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locatorType)
            element.send_keys(data)
            self.log_exel.info("Sent data on element with locator: " + locator +
                               " locatorType: " + locatorType)
        except:
            self.log_exel.info("Cannot send data on the element with locator: " + locator +
                               " locatorType: " + locatorType)
            self.log_exel.error("Exception Caught: {}".format(traceback.format_exc()))
            self.log_exel.error("".join(traceback.format_stack()))

    def send_keys_when_ready(self, data, locator="", locatorType="xpath"):
        """
        Send keys to an element -> MODIFIED
        Either provide element or a combination of locator and locatorType
        """
        try:
            by_type = self.get_by_type(locatorType)
            self.log_exel.info("Waiting for maximum :: " + str(10) +
                               " :: seconds for element to be visible")
            wait = WebDriverWait(self.driver, timeout=10,
                                 poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.visibility_of_element_located((by_type, locator)))
            self.log_exel.info("Element appeared on the web page")
            element.click()
            element.send_keys(data)

            if element.get_attribute("value") != data:
                self.log_exel.debug("Text is not sent by xpath in field so i will try to send string char by char!")
                element.clear()
                for i in range(len(data)):
                    element.send_keys(data[i] + "")
            self.log_exel.info("Sent data on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log_exel.info("Element not appeared on the web page")
            self.log_exel.error("Exception Caught: {}".format(traceback.format_exc()))
            self.log_exel.error("".join(traceback.format_stack()))

    def clear_field(self, locator="", locatorType="id"):
        """
        Clear an element field
        """
        element = self.get_element(locator, locatorType)
        element.clear()
        self.log_exel.info("Clear field with locator: " + locator +
                           " locatorType: " + locatorType)

    def get_text(self, locator="", locatorType="xpath", element=None, info=""):
        """
        NEW METHOD
        Get 'Text' on an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locatorType)
            text = element.text
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log_exel.info("Getting text on element :: " + info)
                self.log_exel.info("The text is :: '" + text + "'")
                text = text.strip()
        except:
            self.log_exel.error("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def is_element_present(self, locator="", locatorType="id", element=None):
        """
        Check if element is present -> MODIFIED
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:  # This means if locator is not empty
                element_list_present = self.get_element_list(locator, locatorType)
            if len(element_list_present) > 0:
                self.log_exel.info("Element present with locator: " + locator +
                                   " locatorType: " + locatorType)
                return True
            else:
                self.log_exel.info("Element not present with locator: " + locator +
                                   " locatorType: " + locatorType)
                return False
        except:
            print("Element not found")
            return False

    def is_element_displayed(self, locator="", locatorType="xpath", element=None):
        """
        NEW METHOD
        Check if element is displayed
        Either provide element or a combination of locator and locatorType
        """
        is_displayed = False
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locatorType)
            if element is not None:
                is_displayed = element.is_displayed()
                self.log_exel.info("Element is displayed")
            else:
                self.log_exel.info("Element not displayed")
            return is_displayed
        except:
            print("Element not found")
            return False

    def element_presence_check(self, locator, byType):
        """
        Check if element is present
        """
        try:
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                self.log_exel.info("Element present with locator: " + locator +
                                   " locatorType: " + str(byType))
                return True
            else:
                self.log_exel.info("Element not present with locator: " + locator +
                                   " locatorType: " + str(byType))
                return False
        except:
            self.log_exel.info("Element not found")
            return False

    def wait_for_element(self, locator, locatorType="id",
                         timeout=10, pollFrequency=0.5):
        element = None
        try:
            by_type = self.get_by_type(locatorType)
            self.log_exel.info("Waiting for maximum :: " + str(timeout) +
                               " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout,
                                 poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((by_type, locator)))
            self.log_exel.info("Element appeared on the web page")
        except:
            self.log_exel.info("Element not appeared on the web page")
            print_stack()
        return element

    def web_scroll(self, direction="up"):
        """
        NEW METHOD
        """
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -800);")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 800);")

    def switch_frame_by_index(self, locator, locatorType="xpath"):

        """
        Get iframe index using element locator inside iframe

        Parameters:
            1. Required:
                locator   - Locator of the element
            2. Optional:
                locatorType - Locator Type to find the element
        Returns:
            Index of iframe
        Exception:
            None
        """
        result = False
        try:
            iframe_list = self.get_element_list("//iframe", locator_type="xpath")
            self.log_exel.info("Length of iframe list: ")
            self.log_exel.info(str(len(iframe_list)))
            for i in range(len(iframe_list)):
                self.switch_to_frame(index=iframe_list[i])
                result = self.is_element_present(locator, locatorType)
                if result:
                    self.log_exel.info("iframe index is:")
                    self.log_exel.info(str(i))
                    break
                self.switch_to_default_content()
            return result
        except:
            print("iFrame index not found")
            return result

    def switch_to_frame(self, id="", name="", index=None):
        """
        Switch to iframe using element locator inside iframe

        Parameters:
            1. Required:
                None
            2. Optional:
                1. id    - id of the iframe
                2. name  - name of the iframe
                3. index - index of the iframe
        Returns:
            None
        Exception:
            None
        """
        if id:
            self.driver.switch_to.frame(id)
        if name:
            self.driver.switch_to.frame(name)
        if index:
            self.log_exel.info("Switch frame with index:")
            self.log_exel.info(str(index))
            self.driver.switch_to.frame(index)

    def switch_to_default_content(self):
        # """
        # Switch to default content
        #
        # Parameters:
        #     None
        # Returns:
        #     None
        # Exception:
        #     None
        # """
        self.driver.switch_to.default_content()

    def get_element_attribute_value(self, attribute, element=None, locator="", locatorType="id"):
        """
        Get value of the attribute of element

        Parameters:
            1. Required:
                1. attribute - attribute whose value to find

            2. Optional:
                1. element   - Element whose attribute need to find
                2. locator   - Locator of the element
                3. locatorType - Locator Type to find the element

        Returns:
            Value of the attribute
        Exception:
            None
        """
        if locator:
            element = self.get_element(locator=locator, locator_type=locatorType)
        value = element.get_attribute(attribute)
        return value

    def is_enabled(self, locator, locatorType="id", info=""):
        """
        Check if element is enabled

        Parameters:
            1. Required:
                1. locator - Locator of the element to check
            2. Optional:
                1. locatorType - Type of the locator(id(default), xpath, css, className, linkText)
                2. info - Information about the element, label/name of the element
        Returns:
            boolean
        Exception:
            None
        """
        element = self.get_element(locator, locator_type=locatorType)
        enabled = False
        try:
            attribute_value = self.get_element_attribute_value(element=element, attribute="disabled")
            if attribute_value is not None:
                enabled = element.is_enabled()
            else:
                value = self.get_element_attribute_value(element=element, attribute="class")
                self.log_exel.info("Attribute value From Application Web UI --> :: " + value)
                enabled = not ("disabled" in value)
            if enabled:
                self.log_exel.info("Element :: '" + info + "' is enabled")
            else:
                self.log_exel.info("Element :: '" + info + "' is not enabled")
        except:
            self.log_exel.error("Element :: '" + info + "' state could not be found")
        return enabled
