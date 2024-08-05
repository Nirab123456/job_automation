import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def save_html(job_id, html_content):
    output_folder = './html_files/'
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, f"{job_id}.html")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Saved HTML for job ID {job_id} to {file_path}")

def process_job_postings(csv_file):
    jobs_df = pd.read_csv(csv_file)
    
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    
    for index, row in jobs_df.iterrows():
        job_id = row['JobId']
        link = row['Link']

        try:
            driver.get(link)
            
            # Try to find and click the "Show how to apply" button
            try:
                apply_button = wait.until(EC.element_to_be_clickable((By.ID, 'applynowbutton')))
                apply_button.click()
                time.sleep(2)

                print(f"Clicked apply button for job ID {job_id}")
            except Exception as e:
                print(f"No apply button for job ID {job_id}: {e}")
            
            # Save HTML content
            html_content = driver.page_source
            save_html(job_id, html_content)

        except Exception as e:
            print(f"Error processing job ID {job_id}: {e}")
    
    driver.quit()

if __name__ == "__main__":
    csv_file = 'test_data.csv'
    process_job_postings(csv_file)
