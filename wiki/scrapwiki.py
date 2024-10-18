import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

# Path to the ChromeDriver and the directory for downloading CSVs
driver_path = 'FoDS-FinalProject\job_aspect\chromedriver.exe'
download_directory = 'FoDS-FinalProject\wiki'

# Load the list of programming languages from the CSV file
languages_df = pd.read_csv('FoDS-FinalProject/wiki/language_list.csv')  
languages = languages_df['programming language'].tolist()  

# Set the default start date for older pages
start_date = "01/01/2020"  # Adjust as necessary

# Configure Chrome options for automatic downloads
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_directory,  # Change to your download path
    "download.prompt_for_download": False,  # Disable the download prompt
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)
options.add_argument('--disable-gpu')
service = Service(executable_path="FoDS-FinalProject/job_aspect/chromedriver.exe")


# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Function to check if a Wikipedia page exists for a language
def page_exists(language):
    search_url = f"https://id.wikipedia.org/wiki/{language.replace(' ', '_')}"
    response = requests.head(search_url)
    return response.status_code == 200

# Open the Pageviews Analysis Tool website
driver.get('https://pageviews.wmcloud.org/')

n = 1

# Loop through each programming language and download the CSV
for language in languages:
    if page_exists(language):
        try:
            time.sleep(5)

            if(n == 1):
                project_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'project-input'))
                )
                project_field.click()  # Click to focus on the field
                project_field.send_keys(Keys.CONTROL + "a")  # Select all text
                project_field.send_keys(Keys.BACKSPACE) 
                project_field.send_keys('id.wikipedia.org')  # Specify Indonesian Wikipedia
                project_field.send_keys(Keys.ENTER)
                time.sleep(5)

            # Find the input field for the page title
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class="select2-search__field"]'))
            )
            input_field.click()
            input_field.send_keys(Keys.CONTROL + "a")
            input_field.send_keys(Keys.BACKSPACE)
            input_field.send_keys(Keys.CONTROL + "a")
            input_field.send_keys(Keys.BACKSPACE)
            time.sleep(1)
            input_field.send_keys(language)
            time.sleep(3)
            input_field.send_keys(Keys.ENTER)
            input_field.send_keys(Keys.ENTER)
            time.sleep(10)

            # monthly option
            type_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'date-type-select'))
            )
            type_dropdown.click()
            time.sleep(2)  
            month_option = driver.find_element(By.CSS_SELECTOR, "option[value='monthly']")
            month_option.click()
            time.sleep(6)  


            if(n == 1):
                start_date_field = driver.find_element(By.ID, 'month-start')                
                start_date_field.click()

                prev = driver.find_element(By.CSS_SELECTOR, "th[class='datepicker-switch']")
                try:
                    prev.click()
                except Exception:
                    print("invalid pre v click")
                
                span2020 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[text()='2020']"))
                )
                span2020.click()

                first_span = driver.find_element(By.CSS_SELECTOR, "td span:first-of-type")
                try:
                    first_span.click()
                except Exception:
                    print("invalid first click")
                time.sleep(8)

                # end_date_field = driver.find_element(By.CSS_SELECTOR, 'input[name="daterangepicker_end"]')
                # end_date_field.click()
                # end_date_field.send_keys(Keys.CONTROL + "a")
                # end_date_field.send_keys(Keys.BACKSPACE)
                # end_date_field.send_keys(time.strftime("%m/%d/%Y"))  # Current date
                # time.sleep(2)

                # btn = driver.find_element(By.CSS_SELECTOR, 'button[class="applyBtn btn btn-sm btn-success"]')
                # btn.click()

            
            # Find and click the "Download as CSV" button (adjust the element as needed)
            download_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.download-btn-group'))
            )
            download_dropdown.click()
            time.sleep(1)  
            csvopt = driver.find_element(By.CSS_SELECTOR, "a[class='download-csv']")
            csvopt.click()
            time.sleep(6)   
            
            print(f"Downloaded data for {language}. Progress: {n}")
            n += 1
            
        except Exception as e:
            print(f"Failed to download data for {language}: {e}")
    else:
        print(f"No Wikipedia page found for {language}")



# Close the driver after processing all languages
driver.delete_all_cookies()
driver.quit()
