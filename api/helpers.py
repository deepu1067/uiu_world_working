from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pickle

def scrape_paper(url, output_file):
    options = Options()
    options.add_argument("--headless")

    driver = Chrome(options=options)
    driver.get(url)

    # Wait until the specific element is visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="conference-paper"]/div[1]')
        )
    )

    response = driver.find_element(
        By.XPATH, '//*[@id="conference-paper"]'
    ).get_attribute("outerHTML")
    driver.quit()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response, "html.parser")
    with open(f"api/static/{output_file}.pkl", "wb") as file:
        pickle.dump(soup, file)

def get_soup(pkl_file:str):
    with open(f"api/static/{pkl_file}.pkl", "rb") as file:
        soup = pickle.load(file)
    return soup