from pages.courses.register_courses_page import CourseTestPage
import pytest
from utilities.teststatus import TestStatus
import unittest


@pytest.mark.usefixtures('setup')
class TestLoginPage(unittest.TestCase):


    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.courses = CourseTestPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.run(order=1)
    def test_invalid_enrol(self):
        login_test = self.courses.login() # Вече успешно се логвам
        search_test = self.courses.search_course()  # Успешно търся курсове Селениум, избирам го, сменям фрейм за да достъпя избор на пакет, поръчвам пакета и скролвам до нов фрейм.
        find_frame_test = self.courses.find_frame() # Най после успях и това да направя
        self.ts.mark(login_test, 'Sucssesful Login')
        self.ts.mark(search_test, 'Searching our course - OK')
        self.ts.mark(find_frame_test, 'Finding frames is hard but I did it !!!!')

    @pytest.mark.run(order=2)
    def test_final_test(self):
        result_final = self.courses.test_final()
        self.ts.mark_final("test_final_test",result_final, "We fail to buy with imaginary bank card")
