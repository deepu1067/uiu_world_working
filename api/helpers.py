from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pickle
import requests
import os
import json

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

def get_jobs():
    base_url = "https://jobs.bdjobs.com/"
    jobs = []
    if os.path.exists("api/static/jobs.json"):
        return
    for page in range(1, 81):
        print(f"Processing page {page}")
            
        url = f"https://jobs.bdjobs.com/jobsearch.asp?pg={page}"
        response = requests.get(url)

        if response.status_code != 200:
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        type1 = soup.find_all('div', class_='norm-jobs-wrapper')
        type2 = soup.find_all('div', class_='row featured-wrap')
        type3 = soup.find_all('div', class_='sout-jobs-wrapper')

        for job in type1:
            position = job.find('div', class_= "job-title-text").text.strip()
            job_url = base_url + job.find('div', class_= "job-title-text").find('a').get('href')
            company = job.find('div', class_= "comp-name-text").text.strip()
            location = job.find('div', class_= "locon-text").text.strip()
            try:
                education = job.find('div', class_= "edu-text").text.strip()
            except AttributeError:
                education = ''
            experince = job.find('div', class_= "exp-text").text.strip()
            deadline = job.find('div', class_= "dead-text-d").text.strip()

            data = {
                'position': position,
                'job_url': job_url,
                'company': company,
                'location': location,
                'education': education,
                'experince': experince,
                'deadline': deadline
            }

            jobs.append(data)
        

        for job in type2:
            position = job.find('div', class_= "title").text.strip()
            job_url = base_url + job.find('div', class_= "title").find('a').get('href')
            company = job.find('div', class_= "company").text.strip()
            location = job.find('div', class_= "loccal").text.strip()
            experince = job.select_one(".exp.loccal > p").text.strip()
            education = ''
            deadline = job.select_one(".exp.loccal .dt").text.strip()

            data = {
                'position': position,
                'job_url': job_url,
                'company': company,
                'location': location,
                'experince': experince,
                'education': education,
                'deadline': deadline,
            }

            jobs.append(data)
        

        for job in type3:
            position = job.find('div', class_= "job-title-text").text.strip()
            job_url = base_url + job.find('div', class_= "job-title-text").find('a').get('href')
            company = job.find('div', class_= "comp-name-text").text.strip()
            location = job.find('div', class_= "locon-text").text.strip()
            try:
                education = job.find('div', class_= "edu-text").text.strip()
            except AttributeError:
                education = ''
            experince = job.find('div', class_= "exp-text").text.strip()
            deadline = job.find('div', class_= "dead-text-d").text.strip()

            data = {
                'position': position,
                'job_url': job_url,
                'company': company,
                'location': location,
                'education': education,
                'experince': experince,
                'deadline': deadline
            }

            jobs.append(data)
    
    with open("api/static/jobs.json", "w") as file:
        json.dump(jobs, file, indent=4)
        