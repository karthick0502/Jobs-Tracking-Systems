from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


def set_up(DPath, Login):
    try:
        path = DPath
        # if using chrome
        chrome_options = Options()
        chrome_options.add_experimental_option('detach', True)
        service = Service(executable_path=path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # driver = webdriver.Chrome()
        driver.get(Login)
        driver.implicitly_wait(2)
        return driver
    except Exception as e:
        raise e


def login_LinkedIn(browser, User, Password, Feed, Applied):
    try:
        driver = browser
        # Enter login credentials and submit
        driver.find_element(By.ID, value='username').send_keys(User)
        driver.find_element(By.ID, value='password').send_keys(Password)
        driver.find_element(By.CLASS_NAME, value="login__form_action_container ").click()
        driver.implicitly_wait(2)
        while True:
            try:
                WebDriverWait(driver, 10).until(EC.url_changes(Feed))
            except Exception:
                pass
            if driver.current_url == Feed:
                break
        # driver.implicitly_wait(10)
        driver.get(Applied)
        driver.implicitly_wait(2)
        return driver
    except Exception as e:
        raise e


"""
driver_path = r'K:\\API works\\chromedriver_win32\\chromedriver.exe'
path2 = r"C:\\Users\\mkart\\.cache\\selenium\\chromedriver\\win64\\122.0.6261.128\\chromedriver.exe"
username = "mkarthick502@gmail.com"
password = "7502144781@$K"

# if using chrome
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)
service = Service(executable_path=path2)
driver = webdriver.Chrome(service=service, options=chrome_options)

# driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/login")

initial_url = driver.current_url
feed_url = "https://www.linkedin.com/feed/"

# Enter login credentials and submit
driver.find_element(By.ID, value='username').send_keys(username)
driver.find_element(By.ID, value='password').send_keys(password)
driver.find_element(By.CLASS_NAME, value="login__form_action_container ").click()
driver.implicitly_wait(10)

while True:
    try:
        WebDriverWait(driver, 10).until(EC.url_changes('https://www.linkedin.com/feed/'))
    except BaseException as TimeoutException:
        pass
    if driver.current_url == feed_url:
        break

# driver.implicitly_wait(10)
driver.get("https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED")
next_ = "https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED&start="


def get_pagination(browser):
    applied_pages = browser.find_element(By.CSS_SELECTOR,
                                         value="ul.artdeco-pagination__pages.artdeco-pagination__pages--number")
    pages_length = applied_pages.find_elements(By.TAG_NAME, value='li')
    return len(pages_length)


def scrap_applied_jobs(browser):
    browser.implicitly_wait(3)
    applied_jobs = browser.find_element(By.CSS_SELECTOR, value="ul.reusable-search__entity-result-list.list-style-none")
    applied_jobs = applied_jobs.find_elements(By.CSS_SELECTOR, value="li.reusable-search__result-container")
    return applied_jobs


def split_applied_jobs(jobs):
    p_list = []
    n_list = []
    l_list = []
    s_list = []
    for job in jobs:
        position = job.find_element(By.CSS_SELECTOR, value="div.t-roman.t-sans").text
        name = job.find_element(By.CSS_SELECTOR, value="div.entity-result__primary-subtitle.t-14.t-black.t-normal").text
        location = job.find_element(By.CSS_SELECTOR, value="div.entity-result__secondary-subtitle.t-14.t-normal").text
        status = job.find_element(By.CSS_SELECTOR, value="div.entity-result__insights.t-12").text
        p_list.append(position)
        n_list.append(name)
        l_list.append(location)
        s_list.append(status)
    scrapped_dict = {"Position": p_list, "Name": n_list, "Location": l_list, "Status": s_list}
    return scrapped_dict


def extract_date_string(text):
    found = re.search(r'(\d+\D*)(?:\bago|\bnow)', text)
    if found:
        return found.group(1)
    else:
        return None


def replace_date_string(text):
    replacements = {
        r'(\d+)yr': r'\1 year',
        r'(\d+)mon': r'\1 month',
        r'(\d+)w': r'\1 week',
        r'(\d+)d': r'\1 day',
        r'(\d+)h': r'\1 hour',
        r'(\d+)m': r'\1 minute',
        r'(\d+)s': r'\1 second'
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)
    return text


def compare_with_today(text):
    now = datetime.now().date()
    try:
        date = parse(text, settings={'DATE_ORDER': 'DMY'}).date()
    except ValueError:
        return None

    difference = now - date
    exact_date = now - difference
    return date


pagination = get_pagination(browser=driver)
jobs_df = pd.DataFrame()

for pages in range(1, pagination+1):
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
"""
