from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random
import re
import csv  # Import CSV module

options = Options()
options.add_argument('--disable-gpu')  # Disable GPU acceleration

# Use the Service object to specify the path to the ChromeDriver
service = Service(executable_path="chromedriver.exe")

# Pass the Service object and options to the Chrome driver
driver = webdriver.Chrome(service=service, options=options)

# Open the job portal (e.g., Indeed)
driver.get('https://www.indeed.com/jobs?q=game+developer&l=')

# Wait for the page to load
time.sleep(10)

# # List of programming languages to search for
# languages = ['Python', 'Java', 'C#', 'JavaScript', 'Ruby', 'C++', 'PHP', 'Swift', 'Go', 'Kotlin']

# def extract_languages(job_description):
#     found_languages = []
#     for language in languages:
#         if re.search(fr'\b{language}\b', job_description, re.IGNORECASE):
#             found_languages.append(language)
#     return found_languages



# Scroll slowly through the page, simulating a human reader
def scroll_slowly(driver):
    scroll_pause_time = random.uniform(0.5, 2.0)  # Randomize scroll pauses
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    scroll_position = 0

    while scroll_position < scroll_height:
        scroll_position += random.randint(200, 500)  # Random scroll distance
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(scroll_pause_time)

# Set the limit of job entries
entry_limit = 200
entries_processed = 0  # Counter for how many job entries have been scraped

# Open the CSV file for writing
with open('jobdata3.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['Company Name', 'Job Description'])

    while entries_processed < entry_limit:  # Continue until 1000 entries are processed
        try:
            # Simulate scrolling the page before interacting with job cards
            scroll_slowly(driver)

            # Locate all job cards
            job_cards = driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')

            for index, job_card in enumerate(job_cards):
                if entries_processed >= entry_limit:
                    break  # Exit if we've reached the entry limit

                try:
                    # Refetch the job cards after each interaction to avoid stale element reference
                    job_cards = driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')
                    job_card = job_cards[index]  # Get the job card by index

                    # Introduce a random pause before interacting with each card (simulating user reading time)
                    time.sleep(random.uniform(1.5, 3.5))

                    # Randomly skip some job cards, mimicking how users might not click every card
                    if random.random() > 0.8:  # 20% chance to skip the card
                        print(f"Skipping job card {index + 1}")
                        continue

                    # Click to expand job card details (if needed)
                    job_card.click()
                    time.sleep(random.uniform(2, 5))  # Random wait time for job details to load

                    # Simulate a short pause, as if a human is reading
                    time.sleep(random.uniform(1, 3))

                    # Refetch company name and job description after expanding the job card
                    company_name = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'css-1ioi40n'))
                    ).text

                    job_description = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, 'jobDescriptionText'))
                    ).text

                    # Extract and print required languages
                    # required_languages = extract_languages(job_description)

                    print(f"Company name: {company_name}")
                    # print(f"Required programming languages: {required_languages}")
                    print(f"Job desc: {job_description}")

                    # Write the scraped data to the CSV file
                    writer.writerow([company_name, job_description])

                    # Increment the counter for processed entries
                    entries_processed += 1
                    print(entries_processed)

                except Exception as e:
                    print(f"Error scraping job description: {e}")

            # Try to find and click the "Next" button for pagination
            if entries_processed < entry_limit:  # Only click next if we haven't reached the limit
                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]'))
                    )
                    
                    # Simulate random scrolling before clicking the next button
                    scroll_slowly(driver)

                    # Random pause before clicking "Next", simulating user deciding to move forward
                    time.sleep(random.uniform(2, 5))
                    next_button.click()
                    time.sleep(random.uniform(5, 8))  # Random wait for the next page to load

                except Exception as e:
                    print("No more pages or error clicking 'Next':", e)
                    break  # Exit loop if there's no "Next" button

        except Exception as e:
            print(f"Error processing page: {e}")
            break  # Exit if there's an issue processing the page

# Close the browser
driver.delete_all_cookies()
driver.quit()
