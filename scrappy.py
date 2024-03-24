from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def get_pagination(browser):
    try:
        browser.implicitly_wait(10)
        applied_pages = browser.find_element(By.CSS_SELECTOR, "ul.artdeco-pagination__pages.artdeco-pagination__pages--number")
        pages_length = applied_pages.find_elements(By.TAG_NAME, 'li')
        return len(pages_length)
    except Exception as e:
        print(f"Error getting pagination: {str(e)}")
        return 0

def scrap_applied_jobs(browser):
    try:
        browser.implicitly_wait(10)
        applied_jobs = browser.find_element(By.CSS_SELECTOR, "ul.reusable-search__entity-result-list.list-style-none")
        applied_jobs = applied_jobs.find_elements(By.CSS_SELECTOR, "li.reusable-search__result-container")
        return applied_jobs[:10]  # Limit to scraping only the first 10 jobs
    except Exception as e:
        print(f"Error scraping applied jobs: {str(e)}")
        return []

def split_applied_jobs(jobs):
    try:
        p_list = []
        n_list = []
        l_list = []
        s_list = []
        for job in jobs:
            try:
                position = job.find_element(By.CSS_SELECTOR, "div.t-roman.t-sans").text
                name = job.find_element(By.CSS_SELECTOR, "div.entity-result__primary-subtitle.t-14.t-black.t-normal").text
                location = job.find_element(By.CSS_SELECTOR, "div.entity-result__secondary-subtitle.t-14.t-normal").text
                status = job.find_element(By.CSS_SELECTOR, "div.entity-result__insights.t-12").text
                p_list.append(position)
                n_list.append(name)
                l_list.append(location)
                s_list.append(status)
            except Exception as e:
                print(f"Error splitting job details: {str(e)}")
        scrapped_dict = {"Position": p_list, "Name": n_list, "Location": l_list, "Status": s_list}
        return scrapped_dict
    except Exception as e:
        print(f"Error splitting applied jobs: {str(e)}")
        return {}