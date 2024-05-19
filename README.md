## README

### Web Scraper for Instagram Search Results

This program is designed to scrape Instagram search results from a specific URL using Selenium and store the extracted data in a CSV file. The program navigates through multiple pages of search results and collects the titles, images, links, and other information from each result.

### Prerequisites

- Python 3.x
- Selenium
- Pandas
- Firefox browser
- Geckodriver (for Firefox)

### Installation

1. **Install Selenium:**

   ```sh
   pip install selenium
   ```

2. **Install Pandas:**

   ```sh
   pip install pandas
   ```

3. **Download Geckodriver:**
   
   Download the appropriate Geckodriver for your system from the [official website](https://github.com/mozilla/geckodriver/releases) and add it to your system's PATH.

### Usage

1. **Update the URL:**

   Modify the `url` variable in the script to the URL you want to scrape.

   ```python
   url = "http://www.uvrx.com/results-instagram/index.html?q=food+blogger+dubai"
   ```

2. **Run the Script:**

   Execute the script to start the web scraping process.

   ```sh
   python scraper.py
   ```

3. **Output:**

   The script will create a `data.csv` file containing the scraped data with the following columns:
   - Titles
   - Image
   - Instagram Links
   - Other Information

### Script Overview

1. **Initialize WebDriver:**

   The script starts by initializing the Firefox WebDriver.

   ```python
   driver = webdriver.Firefox()
   driver.get(url)
   ```

2. **Define Data Containers:**

   Lists are created to store the scraped data.

   ```python
   titles = []
   image_src = []
   links = []
   other_info = []
   ```

3. **Process Data Function:**

   This function processes the data on the current page, extracting titles, images, links, and other information from each search result container.

   ```python
   def process_data(driver):
       # Implementation details
   ```

4. **Pagination and Data Extraction:**

   The script handles pagination by clicking through up to 10 pages of results and calls the `process_data` function for each page.

   ```python
   page_number = 1
   try:
       while page_number <= 10:
           process_data(driver)
           next_page_element = WebDriverWait(driver, 30).until(
               EC.presence_of_element_located((By.XPATH, f"//div[@class='gsc-cursor-page' and @aria-label='Page {page_number + 1}']"))
           )
           next_page_element.click()
           page_number += 1
           WebDriverWait(driver, 30).until(EC.staleness_of(next_page_element))
   except Exception as e:
       print(f"An error occurred: {e}")
   finally:
       driver.quit()
   ```

5. **Save Data to CSV:**

   The scraped data is stored in a Pandas DataFrame and saved to a CSV file.

   ```python
   my_dict = {'Titles': titles, 'Image': image_src, 'Instagram Links': links, 'Other Information': other_info}
   df_headline = pd.DataFrame(my_dict)
   df_headline.to_csv('data.csv')
   ```

### Error Handling

The script includes error handling for various exceptions such as `NoSuchElementException`, `TimeoutException`, and general exceptions during the scraping process.

### Notes

- Adjust the timeouts as necessary to ensure the pages load completely before attempting to scrape data.
- Ensure that the Geckodriver path is correctly set up in your system environment variables.

### License

This project is licensed under the MIT License.

### Acknowledgements

- Selenium WebDriver
- Pandas Library

Feel free to modify and extend this script to suit your needs. Happy scraping!
