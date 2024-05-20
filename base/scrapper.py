from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def scraper(url, search_term):
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Initialize Chrome webdriver with options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    # Find the search box element based on the URL
    if "computerhope.com" in url:
        search_box = driver.find_element(By.CLASS_NAME, "sbar")
    elif "geeksforgeeks.org" in url:
        search_box = driver.find_element(By.CLASS_NAME, "ant-input")
    else:
        raise ValueError("Unsupported website URL")

    # Input the search term
    search_box.send_keys(search_term)

    # Simulate pressing the "Enter" key to submit the search
    search_box.send_keys(Keys.ENTER)

    # Wait for search results to load
    time.sleep(5)

    # For geeksforgeeks.org, click on the first search result to navigate to the article page
    if "geeksforgeeks.org" in url:
        # Locate the anchor tag with class "font-primary" inside the parent div
        first_anchor_tag = driver.find_element(By.CSS_SELECTOR, "a.font-primary")
        # Get the href attribute value
        article_url = first_anchor_tag.get_attribute("href")
        # Navigate to the article URL
        driver.get(article_url)

        # Wait for the article page to load
        time.sleep(5)

    # Get the page source
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find and remove unwanted tags
    tags_to_remove = ['header', 'script', 'noscript', 'footer', "button", "input", "style"]
    for sel_tag in tags_to_remove:
        for scr in soup.find_all(sel_tag):
            scr.decompose()

    # Find all <p> tags and extract text
    paragraphs = soup.find_all('p')
    cleaned_paragraphs = [p.get_text() for p in paragraphs]

    driver.quit()

    return cleaned_paragraphs

