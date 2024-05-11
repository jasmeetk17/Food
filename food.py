from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

import pandas as pd

url="http://www.uvrx.com/results-instagram/index.html?q=food+blogger+dubai"

driver=webdriver.Firefox()
driver.get(url)

titles=[]
image_src=[]
links=[]
other_info=[]

def process_data(driver):
# Increase the timeout to 20 seconds
    wait = WebDriverWait(driver, 30) # Adjust the timeout as necessary
    containers = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//div[@class='gsc-webResult gsc-result'])")))

    for container in containers:
        try:
            # Attempt to locate the title, subheading, and link within each container
            title_elements = container.find_elements(By.XPATH, ".//a[@class='gs-title']")
            if title_elements:
                title = title_elements[0].text
                titles.append(title)
            else:
                titles.append('N/A')
            
            image_elements=container.find_elements(By.XPATH, ".//img[@class='gs-image']")
            if image_elements:
                image = image_elements[0].get_attribute('src')
                image_src.append(image)
            else:
                image_src.append('N/A')
            
            link_elements = container.find_elements(By.XPATH, ".//div[@class='gsc-url-top']")
            if link_elements:
                link = link_elements[0].text[20:]
                a = 'www.instagram.com/' + link
                links.append(a)
            else:
                links.append('N/A')

            other_elements = container.find_elements(By.XPATH, ".//div[@class='gs-bidi-start-align gs-snippet']")
            if other_elements:
                other = other_elements[0].text
                other_info.append(other)
            else:
                other_info.append('N/A')
        except Exception as e:
            print(f"Error locating elements: {e}")
            continue
page_number = 1 # Start with the first page
try:
    while page_number <= 10: # Process up to the 10th page
        # Process the current page
        process_data(driver)

        # Attempt to find the next page element by incrementing the page number
        try:
            # Increase the timeout to give the page more time to load
            next_page_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, f"//div[@class='gsc-cursor-page' and @aria-label='Page {page_number + 1}']"))
            )
            # Click the next page element to navigate to the next page
            next_page_element.click()
            page_number += 1 # Increment the page number for the next iteration
            # Wait for the new page to load completely before proceeding
            WebDriverWait(driver, 30).until(EC.staleness_of(next_page_element))
        except NoSuchElementException:
            # If no next page element is found, we're on the last page, so break the loop
            print("No more pages found. Exiting...")
            break
        except TimeoutException:
            # If a timeout occurs, log it, print the current page URL, and break the loop
            print(f"Timeout occurred. Exiting... Current page URL: {driver.current_url}")
            break
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Ensure the driver is closed even if an error occurs
    driver.quit()

my_dict={'Titles':titles, 'Image':image_src,'Instagram Links':links,'Other Information':other_info}

df_headline=pd.DataFrame(my_dict)
df_headline.to_csv('data.csv')

driver.quit()