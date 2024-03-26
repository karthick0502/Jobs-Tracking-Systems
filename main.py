from linkedin_scraper import Person, actions, JobSearch
from selenium import webdriver
import pandas as pd

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrappy import get_pagination, scrap_applied_jobs, split_applied_jobs
from date_functionality import extract_date_string, replace_date_string, compare_with_today
from LinkedIn import set_up, login_LinkedIn

path = "*******"
path2 = "*******"
username = "********"
password = "********"

login_url = r"https://www.linkedin.com/login"
feed_url = r"https://www.linkedin.com/feed/"
applied = r"https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED"
next_ = r"https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED&start="

if __name__ == "__main__":
    try:
        driver = set_up(DPath=path2, Login=login_url)
        driver = login_LinkedIn(driver, username, password, feed_url, applied)

        pagination = get_pagination(browser=driver)
        jobs_df = pd.DataFrame()

        for pages in range(1, pagination + 1):
            print(f'-----------------------page{pages}--------------------------')
            applied_job_list = scrap_applied_jobs(browser=driver)
            driver.implicitly_wait(2)
            jobs_dict = split_applied_jobs(jobs=applied_job_list)
            temp_df = pd.DataFrame(jobs_dict)
            jobs_df = pd.concat([jobs_df, temp_df])
            for applied_jobs_details in applied_job_list:
                print(applied_jobs_details.text)
            next_page = f"{next_}{str(pages)}0"
            WebDriverWait(driver, 10).until(EC.url_changes(next_page))
            driver.get(next_page)

        jobs_df.reset_index(drop=True, inplace=True)
        jobs_df['Periods'] = jobs_df['Status'].apply(extract_date_string)
        jobs_df['Periods'] = jobs_df['Periods'].apply(replace_date_string)
        jobs_df['Date'] = jobs_df['Periods'].apply(compare_with_today)
        jobs_df.to_csv('Tracking list.csv')
        driver.quit()
    except Exception as e:
        print('Error', e)

