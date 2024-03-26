# import os
# import subprocess
# import wget
# import zipfile
# from linkedin_scraper import Person, actions, JobSearch
# from selenium import webdriver
# import pandas as pd
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from scrappy import get_pagination, scrap_applied_jobs, split_applied_jobs
# from date_functionality import extract_date_string, replace_date_string, compare_with_today
# from LinkedIn import set_up, login_LinkedIn

# def get_chrome_version():
#     if os.name == 'nt':  # Windows
#         cmd = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
#         output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
#         version = output.decode('utf-8').strip().split()[-1]
#     else:  # macOS
#         cmd = r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version'
#         output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
#         version = output.decode('utf-8').strip().split()[-1]
#     return version

# def download_chromedriver(chrome_version, max_retries=3):
#     base_url = 'https://chromedriver.storage.googleapis.com'
#     chromedriver_path = os.path.abspath('chromedriver/chromedriver')

#     if os.path.exists(chromedriver_path):
#         # Check if the existing ChromeDriver is compatible with the Chrome version
#         try:
#             output = subprocess.check_output([chromedriver_path, '--version'], stderr=subprocess.STDOUT)
#             current_version = output.decode('utf-8').split()[1].split('.')[0]
#             if current_version == chrome_version.split('.')[0]:
#                 print(f"Compatible ChromeDriver version {current_version} is already installed.")
#                 return chromedriver_path
#         except subprocess.CalledProcessError:
#             pass

#     download_url = f'{base_url}/LATEST_RELEASE_{chrome_version}'
#     try:
#         latest_release = wget.download(download_url, out='chromedriver_version.txt')
#         with open(latest_release, 'r') as file:
#             version = file.read().strip()
#     except Exception as e:
#         print(f"ChromeDriver for Chrome version {chrome_version} not found. Downloading the latest version.")
#         latest_release_url = f'{base_url}/LATEST_RELEASE'
#         latest_release = wget.download(latest_release_url, out='chromedriver_version.txt')
#         with open(latest_release, 'r') as file:
#             version = file.read().strip()

#     download_url = f'{base_url}/{version}/chromedriver_mac64.zip'
#     chromedriver_zip = 'chromedriver.zip'

#     for attempt in range(max_retries):
#         try:
#             wget.download(download_url, out=chromedriver_zip)
#             break
#         except Exception as e:
#             print(f"Error downloading ChromeDriver: {str(e)}")
#             if attempt < max_retries - 1:
#                 print(f"Retrying download (attempt {attempt + 1})...")
#             else:
#                 raise e

#     with zipfile.ZipFile(chromedriver_zip, 'r') as zip_ref:
#         zip_ref.extractall('chromedriver')
#     os.remove(chromedriver_zip)
#     os.remove(latest_release)
#     return chromedriver_path

# chrome_version = get_chrome_version()
# path = download_chromedriver(chrome_version.split('.')[0])

# username = "suseendarannair@gmail.com"
# password = "Azsxdcfvgbhnjmk@123"
# login_url = "https://www.linkedin.com/login"
# feed_url = "https://www.linkedin.com/feed/"
# applied = "https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED"
# next_ = "https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED&start="

# if __name__ == "__main__":
#     try:
#         driver = set_up(DPath=path, Login=login_url)
#         driver = login_LinkedIn(driver, username, password, feed_url, applied)
#         pagination = get_pagination(browser=driver)

#         jobs_df = pd.DataFrame()
#         for pages in range(1, pagination + 1):
#             print(f'-----------------------page{pages}--------------------------')
#             applied_job_list = scrap_applied_jobs(browser=driver)
#             driver.implicitly_wait(2)
#             jobs_dict = split_applied_jobs(jobs=applied_job_list)
#             temp_df = pd.DataFrame(jobs_dict)
#             jobs_df = pd.concat([jobs_df, temp_df])

#             for applied_jobs_details in applied_job_list:
#                 print(applied_jobs_details.text)

#             next_page = f"{next_}{str(pages)}0"
#             WebDriverWait(driver, 10).until(EC.url_changes(next_page))
#             driver.get(next_page)

#         jobs_df.reset_index(drop=True, inplace=True)
#         jobs_df['Periods'] = jobs_df['Status'].apply(extract_date_string)
#         jobs_df['Periods'] = jobs_df['Periods'].apply(replace_date_string)
#         jobs_df['Date'] = jobs_df['Periods'].apply(compare_with_today)
#         jobs_df.to_csv('Tracking list.csv')

#     except Exception as e:
#         print('Error', e)

#     finally:
#         driver.quit()


import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrappy import get_pagination, scrap_applied_jobs, split_applied_jobs
from date_functionality import extract_date_string, replace_date_string, compare_with_today
from LinkedIn import login_LinkedIn

username = "******"
password = "******"
login_url = "https://www.linkedin.com/login"
feed_url = "https://www.linkedin.com/feed/"
applied = "https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED"
next_ = "https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED&start="

if __name__ == "__main__":
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        driver.get(login_url)
        driver.implicitly_wait(10)
        driver = login_LinkedIn(driver, username, password, feed_url, applied)
        pagination = get_pagination(browser=driver)

        jobs_df = pd.DataFrame()
        for pages in range(1, min(pagination, 3) + 1):  # Limit to scraping only the first 3 pages
            print(f'-----------------------page{pages}--------------------------')
            applied_job_list = scrap_applied_jobs(browser=driver)
            jobs_dict = split_applied_jobs(jobs=applied_job_list)
            temp_df = pd.DataFrame(jobs_dict)
            jobs_df = pd.concat([jobs_df, temp_df])

            for applied_jobs_details in applied_job_list:
                print(applied_jobs_details.text)

            if pages < min(pagination, 3):
                next_page = f"{next_}{str(pages)}0"
                WebDriverWait(driver, 10).until(EC.url_changes(next_page))
                driver.get(next_page)

        jobs_df.reset_index(drop=True, inplace=True)
        jobs_df['Periods'] = jobs_df['Status'].apply(extract_date_string)
        jobs_df['Periods'] = jobs_df['Periods'].apply(replace_date_string)
        jobs_df['Date'] = jobs_df['Periods'].apply(compare_with_today)
        jobs_df.to_csv('Tracking list.csv')

    except Exception as e:
        print('Error', e)

    finally:
        driver.quit()