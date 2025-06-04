import pytest
from selenium import webdriver


def pytest_addoption(parser):
    """Добавяне на аргументи за браузър и ръчно въвеждане."""
    parser.addoption("--browser", choices=["chrome", "firefox", "edge"], default="chrome", help="Избор на браузър")
    parser.addoption("--manual", action="store_true", help="Активиране на ръчно въвеждане")


@pytest.fixture(scope="class")
def driver_init(request):
    """Инициализира WebDriver според избора на браузър."""
    browser = request.config.getoption("--browser")

    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "edge":
        driver = webdriver.Edge()
    else:
        driver = webdriver.Firefox()

    driver.implicitly_wait(5)
    driver.maximize_window()
    _base_url = 'https://www.letskodeit.com/practice'
    driver.get(_base_url)

    request.cls.driver = driver  # Запазваме драйвера в тестовия клас
    yield driver
    driver.quit()


@pytest.fixture(scope="class", autouse=True)
def setup(request, driver_init):
    """Настройка на тестовата среда с параметри от терминала."""
    request.cls.driver = driver_init  # Осигуряваме, че тестовите класове ще имат достъп до driver
    manual_input = request.config.getoption("--manual")
    request.cls.manual_input = manual_input
