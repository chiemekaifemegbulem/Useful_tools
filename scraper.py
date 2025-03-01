import requests
from bs4 import BeautifulSoup
import time
import random
import csv
import logging
import threading
from urllib.parse import urljoin
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from stem.control import Controller
from stem import Signal
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import hashlib
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import twocaptcha

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Proxy list (to be replaced with actual proxies)
PROXIES = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080"
]

# Initialize fake user agent
ua = UserAgent()

# CAPTCHA solver using 2Captcha API
CAPTCHA_API_KEY = "your_2captcha_api_key"
captcha_solver = twocaptcha.TwoCaptcha(CAPTCHA_API_KEY)

def solve_captcha(site_key, url):
    try:
        result = captcha_solver.recaptcha(sitekey=site_key, url=url)
        return result["code"]
    except Exception as e:
        logging.error(f"CAPTCHA solving failed: {e}")
        return None

# Tor integration to change IP dynamically
def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='your_tor_password')
        controller.signal(Signal.NEWNYM)
        logging.info("Tor IP address renewed")

# Session with retry strategy
def get_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def get_soup(url):
    headers = {'User-Agent': ua.random}
    proxy = {"http": random.choice(PROXIES), "https": random.choice(PROXIES)}
    session = get_session()
    try:
        response = session.get(url, headers=headers, proxies=proxy, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url} using proxy {proxy}: {e}")
        return None

# Selenium setup for JavaScript-rendered pages
def get_dynamic_soup(url):
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=options)
    
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_source = driver.page_source
        return BeautifulSoup(page_source, 'html.parser')
    finally:
        driver.quit()

def extract_text(tag):
    return tag.text.strip() if tag else "No content available"

def scrape_articles(url):
    soup = get_soup(url) or get_dynamic_soup(url)
    if not soup:
        return []
    
    articles = []
    for article in soup.find_all('article'):
        title_tag = article.find('h2')
        link_tag = article.find('a', href=True)
        summary_tag = article.find('p')
        date_tag = article.find('time')
        author_tag = article.find(class_=re.compile("author|byline", re.I))
        
        if title_tag and link_tag:
            title = extract_text(title_tag)
            link = urljoin(url, link_tag['href'])
            summary = extract_text(summary_tag)
            date = extract_text(date_tag)
            author = extract_text(author_tag)
            article_hash = hashlib.md5((title + link).encode()).hexdigest()
            articles.append({
                "id": article_hash, "title": title, "link": link, 
                "summary": summary, "date": date, "author": author
            })
    
    return articles

def save_to_json(data, filename="scraped_data.json"):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    else:
        existing_data = []
    
    existing_ids = {item['id'] for item in existing_data}
    new_data = [item for item in data if item['id'] not in existing_ids]
    
    if new_data:
        existing_data.extend(new_data)
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
        logging.info(f"Added {len(new_data)} new articles to {filename}")
    else:
        logging.info("No new articles found.")

def scrape_multiple_pages(base_url, pages=5, delay=3):
    all_articles = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(scrape_articles, f"{base_url}?page={page}"): page for page in range(1, pages + 1)}
        
        for future in as_completed(futures):
            page = futures[future]
            try:
                articles = future.result()
                if articles:
                    all_articles.extend(articles)
                logging.info(f"Scraped page {page} successfully")
            except Exception as e:
                logging.error(f"Error scraping page {page}: {e}")
            
            if page % 4 == 0:
                renew_tor_ip()  # Change IP every 3 pages
            
            time.sleep(random.uniform(delay - 1, delay + 1))  # Randomized delay to prevent blocking
    
    save_to_json(all_articles)

def main():
    base_url = "https://example.com/news"  # Replace with actual website
    scrape_multiple_pages(base_url, pages=10, delay=5)

if __name__ == "__main__":
    main()
