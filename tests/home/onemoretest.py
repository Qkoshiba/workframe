import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# from selenium.webdriver.common.devtools.v133.memory import prepare_for_leak_detection


class Framework(unittest.TestCase):
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.maximize_window()
    def setUp(self):
        print('****' * 4)
        print('Start Test000000000999921')
        _baseurl = self.
    def test_login(self):
        baseurl = 'https://eilo.org/'
        website_open = self.driver.get(baseurl)
        login = self.driver.find_element(By.XPATH, '//*[@id="allpage-login-top"]')
        login.click()
        login_input = self.driver.find_element(By.XPATH, '//*[@id="secondary"]/form/fieldset[1]/input') # намирам къде да напиша логин името
        login_input.click()
        time.sleep(2)
        login_input.send_keys('Qkoshiba') # въвеждам потребителско име
        password_input = self.driver.find_element(By.XPATH, '//*[@id="secondary"]/form/fieldset[2]/input') #намирам елемента
        password_input.click()
        password_input.send_keys('Minimalism81') # въвеждам парола
        time.sleep(2)
        click_login_button = self.driver.find_element(By.XPATH, '//*[@id="secondary"]/form/fieldset[3]/input') # намирам копчето
        click_login_button.click()
        assert click_login_button is not None
