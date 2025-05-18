import pytest
from selenium import webdriver

def pytest_addoption(parser):
    """Добавяне на аргументи за браузър и ръчно въвеждане."""
    parser.addoption("--browser", choices=["chrome", "firefox"], default="chrome", help="Избор на браузър")
    parser.addoption("--manual", action="store_true", help="Активиране на ръчно въвеждане")

@pytest.fixture(scope="class")
def driver_init(request):
    """Инициализира WebDriver според избора на браузър."""
    browser = request.config.getoption("--browser")

    if browser == "chrome":
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Firefox()

    request.cls.driver = driver
    yield driver
    driver.quit()

@pytest.fixture(scope="class", autouse=True)
def setup(request, driver_init):
    """Настройка на тестовата среда с параметри от терминала."""
    manual_input = request.config.getoption("--manual")
    request.cls.manual_input = manual_input

    driver_init.get("https://eilo.org/")
    driver_init.implicitly_wait(3)
