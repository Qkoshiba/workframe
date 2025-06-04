import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.basepage import BasePage
import utilities.custom_logger as cl


class CourseTestPage(BasePage):
    log = cl.custom_logger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        driver = self.driver

    def login(self, start_login_locator='//*[@id="navbar-inverse-collapse"]/div/div/a', username='', password=''):
        _default_username = 'test@email.com'
        _default_password = 'abcabc'
        _login_start = '//*[@id="navbar-inverse-collapse"]/div/div/a'
        _login_user_field = '//*[@id="email"]'
        _login_pass_field = '//*[@id="login-password"]'
        _login_button = '//*[@id="login"]'
        self.element_click(start_login_locator)
        self.send_keys(_default_username, _login_user_field, 'xpath')
        self.send_keys(_default_password, _login_pass_field, 'xpath')
        self.element_click(_login_button, 'xpath')
        time.sleep(1)
        if _login_button:
            return True
        else:
            return False



    def search_course(self):
        all_courses = '//*[@id="navbar-inverse-collapse"]/ul/li[2]/a'
        search_course_search = '//*[@id="search"]/div/button'
        selenium_course = '//*[@id="course-list"]/div[1]/div/a/div[1]/div[1]/img'
        search_course = '//*[@id="search"]'
        search_course1 = '//*[@name="course"]'

        data = 'Selenium'
        self.element_click(all_courses, 'xpath')
        self.element_click(search_course)
        self.send_keys(data, search_course1, 'xpath')
        self.element_click(search_course_search, 'xpath')
        time.sleep(2)
        self.element_click(selenium_course, 'xpath')
        self.web_scroll(direction='down')
        time.sleep(1)
        self.switch_to_frame(0)
        self.element_click('//*[@id="zen_cs_plans_dynamic_4"]/div/div[2]/a', 'xpath')
        time.sleep(1)
        self.web_scroll(direction='down')
        return True

    def find_frame(self):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By

        card_num = '//*[@id="root"]/form/span[2]/div/div/div[2]/span/input'
        exp_date = '[placeholder="MM / YY"]'  # CSS Selector
        s_code = '[placeholder="Security Code"]'  # CSS Selector


        frames = self.get_element_list('iframe', 'tag')
        found = False  # 🟡 Флаг за успешно намиране

        for i, frame in enumerate(frames):
            self.driver.switch_to.default_content()
            self.switch_to_frame(frame)
            try:
                card_num_locator = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, card_num))
                )
                self.log.info(f"✅ Елементът е намерен в iframe[{i}]")
                self.driver.execute_script("arguments[0].focus();", card_num_locator)
                card_num_locator.send_keys("12309988123123823")
                time.sleep(1)
                found = True  # ✅ Успешно
                break
            except Exception as e:
                self.log.info(f"❌ Няма го в този iframe[{i}]. Продължаваме...")

        if not found:
            self.log.error("❌ Не беше намерен нито един iframe с полето за карта.")
            return  # 🟥 Спри изпълнението тук, няма смисъл да продължаваш

        try:
            self.switch_to_default_content()
            self.switch_frame_by_index(exp_date, 'css')
            self.send_keys("12/25", exp_date, 'css')
            time.sleep(1)
        except Exception as e:
            self.log.error(f"Грешка при въвеждане на дата: {e}")

        try:
            self.switch_to_default_content()
            self.switch_frame_by_index(s_code, 'css')
            self.send_keys('123', s_code, 'css')
            time.sleep(1)
            self.switch_to_default_content()
            button_final = '//*[@id="checkout-form"]/div[2]/div[3]/div/div[1]/div[2]/div/button[1]'
            self.element_click(button_final)
            return True
        except Exception as e:
            self.log.error(f"Грешка при въвеждане на дата: {e}")
            return False


    def test_final(self):
        try:
            self.switch_to_default_content()

            # Изчакване на елемента
            incorect_number = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//*[@id="checkout-form"]/div[2]/div[3]/div/div[1]/div[1]/div/div[1]/ul/li/span'))
            )

            # Фокусиране върху елемента
            self.driver.execute_script("arguments[0].focus();", incorect_number)

            # Проверка дали е видим
            if incorect_number.is_displayed():
                self.log.info("✅ Елементът за грешен номер на карта е намерен!")
                return True
            else:
                self.log.info("❌ Елементът е намерен, но не е видим!")
                return False

        except Exception as e:
            self.log.error(f"❌ Грешка при намирането на съобщението: {e}")
            return False
