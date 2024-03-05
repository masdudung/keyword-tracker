import csv
import time 
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Create a headless Chrome browser
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Initialize ArgumentParser
parser = argparse.ArgumentParser(description='Script description')
# Add keyword argument
parser.add_argument('--keyword', type=str, help='Keyword for the search query')
# Parse the arguments
args = parser.parse_args()
# Access the keyword argument
query = args.keyword

try:
    n_row = 1
    n_pages = 10
    for page in range(0, n_pages):
        url = "http://www.google.com/search?q=" + query + "&start=" + str((page - 1) * 10)
        driver.get(url)
        searchElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'search')))

        # Get the HTML content of the search element
        html_content = searchElement.get_attribute('outerHTML')

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all a elements containing h3 elements
        a_elements = soup.find_all('a')
        data = []
        for a in a_elements:
            # Find the h3 element within each a element
            h3 = a.find('h3')
            if h3:
                # Extract href attribute value from the a element
                href = a.get('href')
                # Concatenate text from the h3 element with a space
                text = " " + h3.get_text()
                # Append href and text to the data list
                data.append([n_row, href, text])
                n_row = n_row + 1

        # Save the extracted data to a CSV file
        filename = "result/" + query.replace(' ', '-') + ".csv"
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if page == 0:
                writer.writerow(['No', 'Href', 'Text'])  # Write header only for the first page
            writer.writerows(data)

        time.sleep(3)

finally:
    # Close the browser
    driver.quit()
