from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random
import csv

# Set up Chrome options and service
options = Options()
options.add_argument('--disable-gpu')
# options.add_argument('--headless')  # Run headlessly (without opening the browser window)
service = Service(executable_path="chromedriver.exe")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the JobStreet portal (adjust the search query as needed)
driver.get('https://www.jobstreet.co.id/en/job-search/it-developer-jobs/')

# Wait for the page to load
time.sleep(10)

# Function to scroll through the page
def scroll_slowly(driver):
    scroll_pause_time = random.uniform(0.5, 2.0)  # Randomize scroll pauses
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    scroll_position = 0

    while scroll_position < scroll_height:
        scroll_position += random.randint(200, 500)  # Random scroll distance
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(scroll_pause_time)

# Set the limit of job entries
entry_limit = 1500
entries_processed = 0

# Open the CSV file for writing
with open('jobstreet2.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Job Title', 'Company Name', 'Location', 'Salary', 'Job Type', 'Job Description', 'Date'])

    while entries_processed < entry_limit:
        try:
            scroll_slowly(driver)
            job_cards = driver.find_elements(By.CSS_SELECTOR, 'a[data-automation="job-list-item-link-overlay"]')  # Adjust selector as needed

            for index, job_card in enumerate(job_cards):
                if entries_processed >= entry_limit:
                    break

                try:
                    job_card.click()
                    time.sleep(random.uniform(2, 5))

                    # Extract job details
                    try:
                        job_title = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[data-automation="job-detail-title"]'))
                        ).text
                    except:
                        job_title = "None"

                    try:
                        company_name = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-automation="advertiser-name"]'))
                        ).text
                    except:
                        company_name = "None"

                    try:
                        location = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-automation="job-detail-location"]'))
                        ).text
                    except:
                        location = "None"

                    try:
                        salary = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-automation="job-detail-salary"]'))
                        ).text
                    except:
                        salary = "None"

                    try:
                        job_type = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-automation="job-detail-work-type"]'))
                        ).text
                    except:
                        job_type = "None"

                    try:
                        job_description = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-automation="jobAdDetails"]'))
                        ).text
                    except:
                        job_description = "None"
                    
                    try:
                        jobdate = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class="papho0 _1j97a3y4y w75d4w0 w75d4w1 w75d4w22 _1708b944 w75d4w7"]'))
                        ).text
                    except:
                        jobdate = "None"

                    
                    print(f"Company name: {company_name}")
                    print(f"Job desc: {job_description}")
                    print(f'jobtitle: {job_title}')
                    print(f'jobdate: {jobdate}')
                    print(f'location: {location}')
                    print(f'job type: {job_type}')
                    print(f'salary: {salary}')

                    # Write to CSV
                    writer.writerow([job_title, company_name, location, salary, job_type, job_description, jobdate])
                    entries_processed += 1
                    print(f"{entries_processed} jobs")

                except Exception as e:
                    print(f"Error scraping job: {e}")

            # Move to the next page if available
            if entries_processed < entry_limit:
                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="Next"]'))
                    )
                    scroll_slowly(driver)
                    time.sleep(random.uniform(2, 5))
                    next_button.click()
                    time.sleep(random.uniform(5, 8))

                except Exception as e:
                    print("No more pages or error clicking 'Next':", e)
                    break

        except Exception as e:
            print(f"Error processing page: {e}")
            break

# Close the browser
driver.delete_all_cookies()

driver.quit()
