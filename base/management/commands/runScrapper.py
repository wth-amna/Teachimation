# processjobs.py
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin
from django.core.management.base import BaseCommand
from django.conf import settings
# import json
class Command(BaseCommand):
    help = 'processes unprocessed jobs'
    
    def handle(self, *args, **kwargs):
        class Scraper(ABC):
            def __init__(self, driver_path):
                self.driver_path = driver_path
            
                
        class WebScrapper(Scraper):
            def data_source(self):
                return 'https://www.britannica.com/'

            def scrape(self, topic):
                chrome_options = Options()
            
                service = Service(self.driver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)

                try:
                    driver.get(self.data_source())

                    search_bar = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "q"))
                    )

                    search_bar.send_keys(topic)

                    search_bar.submit()

                    time.sleep(2)

                    article_tag = driver.find_element(By.TAG_NAME, 'article')

                    intro_p_tag = article_tag.find_element(By.CSS_SELECTOR, 'p.intro')
                    intro_text = intro_p_tag.text.strip()

                    numdef_p_tags = article_tag.find_elements(By.CSS_SELECTOR, 'p.numdef')
                    numdef_text = '\n'.join(tag.text.strip() for tag in numdef_p_tags) if numdef_p_tags else None
                    combined_text = f"{intro_text}\n{numdef_text}" if numdef_text else intro_text

                    try:
                        tip_div = article_tag.find_element(By.CSS_SELECTOR, 'div.tip.tab[role="note"]')

                        tip_text = tip_div.text.strip()
                    except NoSuchElementException:
                        tip_text = ''

                    all_text = f"{combined_text}\n{tip_text}" if tip_text else combined_text    

                    cleaned_intro_text = self.clean_text(intro_text)
                    cleaned_numdef_text = self.clean_text(numdef_text)
                    cleaned_tip_text = self.clean_text(tip_text)

                    return {
                        'Topic Name': topic,
                        'Text': all_text
                    }
                except (TimeoutException, NoSuchElementException) as e:
                    pass
                finally:
                    driver.quit()

            def clean_text(self, html_text):
                if html_text is None:
                    return ''
                soup = BeautifulSoup(html_text, 'html.parser')

                cleaned_text = soup.get_text(separator='\n', strip=True)
                return cleaned_text


            
    