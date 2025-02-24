from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


class MetaScraper:
    SEARCH_URL = "https://www.google.com/search?q={keyword}"

    def __init__(self, keyword):
        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Initialize the WebDriver with headless options
        self.driver = webdriver.Chrome(options=chrome_options)
        # Set the keyword for the Google search
        self.keyword = keyword

    def crawl(self):
        # Open Google search results page
        self.driver.get(MetaScraper.SEARCH_URL.format(keyword=self.keyword))

        # Wait for the page to load
        # time.sleep(3)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "search")))
        # Set to collect unique links
        links = set()

        # Define the number of pages to scrape
        num_pages = 5  # Adjust as needed to control the depth of pagination

        for page in range(num_pages):
            # Parse the current page content with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            # Extract URLs from the current Google search results page
            for a_tag in soup.select('a[href^="http"]'):
                href = a_tag["href"]
                if "google.com" not in href and "webcache" not in href:
                    links.add(href)

            # Attempt to go to the next page of results
            try:
                next_button = self.driver.find_element("xpath", "//a[@id='pnnext']")
                next_button.click()

                # Wait for the next page to load
                # time.sleep(3)
                wait.until(EC.staleness_of(next_button))
                wait.until(EC.presence_of_element_located((By.ID, "search")))
            except NoSuchElementException:
                print("No more pages found.")
                break  # Exit the loop if there is no "Next" button

        # Close the driver
        self.driver.quit()

        # Output the unique links
        print("Unique links from Google search results across pages:")
        for link in links:
            print(link)

        print(len(links))
        return links


if __name__ == "__main__":
    scraper = MetaScraper("book flights")
    scraper.crawl()

