import time

from pages.home.login_page import LoginPage
import unittest
from selenium import webdriver
import winsound

class TestClassNew(unittest.TestCase):
    def get_user_input(self):
        print('Asking if the tester wants to change the default settings of the test!')

        input_user = input("Желаете ли ръчно да въведете ново име и парола или да продължим с теста? !!!ВЪВЕДИ ДА ИЛИ НЕ !!!")
        if input_user.lower() in ['да', 'da']:
            print('Initating user input value transfer ....')


            return True

        else:
            print('Няма нужда да се занимавам се нещо си се тества там :))))')
            return False

    winsound.PlaySound("2.wav", winsound.SND_FILENAME)

    def test_valid_login(self):
        driver = webdriver.Chrome()
        driver.get("https://eilo.org/")
        driver.maximize_window()
        driver.implicitly_wait(3)
        new_test = LoginPage(driver)

        if self.get_user_input():
            username = input('Въведи нов потребител на английски: ')
            pass_word = input('Въведи нова парола на английски: ')
        else:
            username = new_test.default_username
            pass_word = new_test.default_password

        new_test.login(username, pass_word)




        new_test.logged_user_check()
        winsound.PlaySound("3.wav", winsound.SND_FILENAME)
        time.sleep(4)
        driver.quit()




