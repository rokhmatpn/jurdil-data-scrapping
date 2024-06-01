from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time
import requests
import os
from urllib.parse import urljoin, urlparse


# Directory to save the images
save_dir = 'downloaded_images'

# Function to initialize the WebDriver
def init_driver():
    service = Service('')  # Replace with the path to your chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode for faster performance
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Function to scrape the webpage
def scrape_website(url):
    driver = init_driver()
    driver.get(url)
    
    # Wait for the content to load
    try:
        # Adjust the wait condition according to your needs
        element_present = EC.presence_of_element_located((By.TAG_NAME, 'img'))
        WebDriverWait(driver, 10).until(element_present)
    except Exception as e:
        print(f"Error loading page: {e}")
        driver.quit()
        return
    
    # Get the page source after JavaScript has rendered the content
    page_content = driver.page_source
    
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # articles = []
    # for article in soup.find_all('article'):
    #     title_tag = article.find('h2')
    #     link_tag = article.find('a')
        
    #     if title_tag and link_tag:
    #         title = title_tag.get_text(strip=True)
    #         link = link_tag.get('href')
    #         articles.append({'title': title, 'link': link})
    

    driver.quit()
    
    return page_content

# Function to scrape TPS
def scrape_tps(url):
    driver = init_driver()
    driver.get(url)
    
    # Wait for the content to load
    try:
        # Adjust the wait condition according to your needs
        element_present = EC.presence_of_element_located((By.TAG_NAME, 'a'))
        WebDriverWait(driver, 10).until(element_present)
    except Exception as e:
        print(f"Error loading page: {e}")
        driver.quit()
        return
    
    # Get the page source after JavaScript has rendered the content
    page_content = driver.page_source
    
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')
    link_tags = soup.find_all('a')

    driver.quit()
    
    return link_tags

# Function to scrape the webpage
def scrape_images(url):
    driver = init_driver()
    driver.get(url)
    
    # Wait for the content to load
    try:
        # Adjust the wait condition according to your needs
        element_present = EC.presence_of_element_located((By.TAG_NAME, 'img'))
        WebDriverWait(driver, 10).until(element_present)
    except Exception as e:
        print(f"Error loading page: {e}")
        driver.quit()
        return
    
    # Get the page source after JavaScript has rendered the content
    page_content = driver.page_source
    
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')
    img_tags = soup.find_all('img')
    img_urls = [img['src'] for img in img_tags if img['src'].startswith('https://sirekap-obj-formc.kpu.go.id')]
    
    driver.quit()
    
    # Download the images
    for img_url in img_urls:
        download_image(img_url)

    return img_urls

# Function to download an image
def download_image(img_url):
    try:
        # Get the image content
        img_response = requests.get(img_url)
        img_response.raise_for_status()  # Check if the request was successful

        # Extract the image filename from the URL
        parsed_url = urlparse(img_url)
        img_filename = os.path.basename(parsed_url.path)

        # Define the full path to save the image
        img_path = os.path.join(save_dir, img_filename)

        # Save the image to the specified path
        with open(img_path, 'wb') as img_file:
            img_file.write(img_response.content)
        print(f"Downloaded: {img_url}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {img_url}: {e}")

# Function to click a button and scrape the resulting content
def scrape_after_click(url, button_selector, content_selector):
    driver = init_driver()
    driver.get(url)
    
    try:
        # Wait for the button to be clickable and then click it
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector)))
        button.click()
        
        # Wait for the content to load after clicking the button
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, content_selector)))
        
        # Get the page source after the content has loaded
        page_content = driver.page_source
    except Exception as e:
        print(f"Error during interaction: {e}")
        driver.quit()
        return None

    # # Parse the page content with BeautifulSoup
    # soup = BeautifulSoup(page_content, 'html.parser')
    
    # # Extract the desired content
    # elements = soup.select(content_selector)
    # results = [element.get_text(strip=True) for element in elements]
    results = page_content
    
    driver.quit()
    
    return results

# Function to perform mouse down on the SVG and scrape the resulting content
def scrape_after_mousedown(url, svg_selector, content_selector):
    driver = init_driver()
    driver.get(url)
    
    try:
        # Wait for the SVG element to be present and perform mouse down on it
        svg_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, svg_selector)))
        
        # Perform mouse down using ActionChains
        actions = ActionChains(driver)
        actions.move_to_element(svg_element).click_and_hold().perform()
        
        # Optionally, add a small delay to ensure the event is processed
        WebDriverWait(driver, 2).until(EC.staleness_of(svg_element))  # Wait until the SVG element is stale
        
        # Wait for the content to load after the mouse down event
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, content_selector)))
        
        # Get the page source after the content has loaded
        page_content = driver.page_source
    except Exception as e:
        print(f"Error during interaction: {e}")
        driver.quit()
        return None

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # Extract the desired content
    elements = soup.select(content_selector)
    results = [element.get_text(strip=True) for element in elements]
    
    driver.quit()
    
    return results

# URL of the website to be scraped
url = "https://pemilu2024.kpu.go.id/pilpres/hitung-suara/11/1105/110507/1105072002/1105072002001"
url = "https://pemilu2024.kpu.go.id/pilegdpr/hitung-suara/wilayah"
url = "https://pemilu2024.kpu.go.id/pilegdpr/hitung-suara/wilayah/11/1101/110101/1101012001"

# Create the directory if it doesn't exist
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Perform the scraping
#page_content = scrape_website(url)
#page_content = scrape_images(url)
#page_content = scrape_after_click(url, "#vs124__combobox", "#vs124__listbox .vs__dropdown-menu")
#page_content = scrape_after_mousedown(url, "#vs124__combobox", "#vs124__listbox .vs__dropdown-menu")
page_content = scrape_tps(url)
print("the content is : ")
print(page_content)
# for idx, article in enumerate(articles, start=1):
#     print(f"{idx}. {article['title']}")
#     print(f"   Link: {article['link']}")
