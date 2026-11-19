from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture
def driver():
    driver_path = (
        Path(__file__).resolve().parent.parent
        / "drivers"
        / "msedgedriver.exe"
    )

    service = Service(executable_path=str(driver_path))

    browser = webdriver.Edge(service=service)

    try:
        yield browser
    finally:
        browser.quit()



def test_page_loads_and_elements_are_visible(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    assert driver.title == "Számösszegző"
    assert driver.find_element(By.TAG_NAME, "h1").text == "Számösszegző alkalmazás"

    assert wait.until(EC.visibility_of_element_located((By.ID, "number-input")))
    assert wait.until(EC.visibility_of_element_located((By.ID, "submit-button")))
    assert wait.until(EC.visibility_of_element_located((By.ID, "sum-value")))

    assert driver.find_element(By.ID, "submit-button").text == "Beküldés"


def test_submitting_number_updates_total(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    initial_sum = driver.execute_async_script("""
        const done = arguments[arguments.length - 1];

        fetch('/api/sum')
            .then(response => {
                if (!response.ok)
                    throw new Error('GET /api/sum: ' + response.status);
                return response.json();
            })
            .then(data => done(data.sum))
            .catch(error => done({error: String(error)}));
    """)

    assert type(initial_sum) is int, f"Nem olvasható a kezdőösszeg: {initial_sum}"

    wait.until(
        lambda d: d.find_element(By.ID, "sum-value").text == str(initial_sum)
    )

    driver.find_element(By.ID, "number-input").send_keys("7")
    driver.find_element(By.ID, "submit-button").click()

    wait.until(
        lambda d: d.find_element(By.ID, "sum-value").text == str(initial_sum + 7)
    )

    wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "status-message"),
            "Sikeres beküldés!"
        )
    )

    assert driver.find_element(By.ID, "number-input").get_attribute("value") == ""
