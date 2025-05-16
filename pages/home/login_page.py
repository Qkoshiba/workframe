from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging.handlers as handlers
import logging

class LoginPage:

    def __init__(self, driver=None):
        super().__init__()
        if driver is None:
            driver = webdriver.Chrome()
            driver.implicitly_wait(5)
            driver.maximize_window()
        self.driver = driver

        # Стойности по подразбиране за юсър и парола
        self.default_username = "Qkoshiba"
        self.default_password = "Minimalism81"

    # Locators XPATH
    _start_login = '//*[@id="allpage-login-top"]' # Линк за да покаже инпута за логване
    _login_input_username = '//*[@id="secondary"]/form/fieldset[1]/input' # Username field
    _login_input_password = '//*[@id="secondary"]/form/fieldset[2]/input' # Password field
    _login_button = '//*[@id="secondary"]/form/fieldset[3]/input' # Тук натискам копчето за да се логна с вече въведените данни за юсър и парола.

    # Elements
    def start_login(self):
        return self.driver.find_element(By.XPATH, self._start_login)

    def login_input_username(self):
        return self.driver.find_element(By.XPATH, self._login_input_username)

    def login_input_password(self):
        return self.driver.find_element(By.XPATH, self._login_input_password)

    def login_button(self):
        return self.driver.find_element(By.XPATH, self._login_button)

    # Actions
    def start_login_click(self):
        self.start_login().click()
        time.sleep(1)

    def login_input_activate(self):
        self.login_input_username().click()
        time.sleep(1)

    def login_user_send_keys(self, username):
        self.login_input_username().send_keys(username)
        time.sleep(1)

    def login_password_send_keys(self, password):
        self.login_input_password().send_keys(password)
        time.sleep(2)

    def login_button_click(self):
        self.login_button().click()
        time.sleep(1)

    def login(self, username, password):
        self.start_login_click()
        self.login_input_activate()
        self.login_user_send_keys(username)
        self.login_password_send_keys(password)
        self.login_button_click()
        time.sleep(5)

    def logged_user_check(self):
        logged_user = self.driver.find_element(By.XPATH, '//*[@id="allpage-username-top"]/a')
        assert logged_user is not None
        print('✅ Успешен логин — фреймуъркът започва да живее 🚀')
        print('*' * 50)
