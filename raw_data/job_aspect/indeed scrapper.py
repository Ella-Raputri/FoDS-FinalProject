from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random
import csv  

options = Options()
options.add_argument('--disable-gpu')  

service = Service(executable_path="chromedriver.exe")

driver = webdriver.Chrome(service=service, options=options)

driver.get('https://id.indeed.com/jobs?q=it+developer&l=')

time.sleep(10)



def scroll_slowly(driver):
    scroll_pause_time = random.uniform(0.5, 2.0)  
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    scroll_position = 0

    while scroll_position < scroll_height:
        scroll_position += random.randint(200, 500) 
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(scroll_pause_time)

entry_limit = 500
entries_processed = 0  

with open('jobdata11.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(['Job Title','Company Name','Location','Salary','Job Type','Job Description'])

    while entries_processed < entry_limit:  
        try:
            scroll_slowly(driver)
            job_cards = driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')

            for index, job_card in enumerate(job_cards):
                if entries_processed >= entry_limit:
                    break  

                try:
                    job_cards = driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')
                    job_card = job_cards[index] 

                    time.sleep(random.uniform(1.5, 3.5))
                    if random.random() > 0.9:  
                        print(f"Skipping job card {index + 1}")
                        continue

                    job_card.click()
                    time.sleep(random.uniform(2, 5)) 
                    time.sleep(random.uniform(1, 3))


                    try:
                        company_name = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'css-1ioi40n'))
                        ).text
                    except:
                        company_name="None"

                    try:
                        job_description = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, 'jobDescriptionText'))
                        ).text
                    except:
                        job_description="None"

                    try:
                        job_title = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'jobsearch-JobInfoHeader-title'))
                        ).text
                    except:
                        job_title="None"
                    
                    try:
                        location = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="inlineHeader-companyLocation"]'))
                        ).text
                    except:
                        location="None"

                    try:
                        job_type = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//div[@role='group'][@aria-label='Job type']//div[contains(@class, 'js-match-insights-provider-tvvxwd')]"))
                        ).text
                    except:
                        job_type = "None"
                    
                    try:
                        salary = WebDriverWait(job_card, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'css-19j1a75')]"))
                        ).text
                    except:
                        salary = "None"
                

                    
                    print(f"Company name: {company_name}")
                    print(f"Job desc: {job_description}")
                    print(f'jobtitle: {job_title}')
                    print(f'location: {location}')
                    print(f'job type: {job_type}')
                    print(f'salary: {salary}')


                    writer.writerow([job_title,company_name,location,salary,job_type,job_description])
                    
                    entries_processed += 1
                    print(entries_processed)

                except Exception as e:
                    print(f"Error scraping job description: {e}")


            if entries_processed < entry_limit:  
                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]'))
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



driver.delete_all_cookies()
driver.quit()
