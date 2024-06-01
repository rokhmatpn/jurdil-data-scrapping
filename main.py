import requests
from bs4 import BeautifulSoup

# Function to fetch the content of a webpage
def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

# Function to parse the content and extract article titles and links
def parse_page(content):
    soup = BeautifulSoup(content, 'html.parser')
    articles = []
    
    # Assuming articles are contained in <article> tags
    for article in soup.find_all('article'):
        title_tag = article.find('h2')  # Assuming the title is in an <h2> tag
        link_tag = article.find('a')    # Assuming the link is in an <a> tag
        
        if title_tag and link_tag:
            title = title_tag.get_text(strip=True)
            link = link_tag.get('href')
            articles.append({'title': title, 'link': link})
    
    return articles

# Main function to perform the scraping
def scrape_website(url):
    content = fetch_page(url)
    print(content)
    # if content:
    #     articles = parse_page(content)
    #     for idx, article in enumerate(articles, start=1):
    #         print(f"{idx}. {article['title']}")
    #         print(f"   Link: {article['link']}")

# URL of the website to be scraped
# url = 'https://pemilu2024.kpu.go.id/pilpres/hitung-suara'
# url = 'https://pemilu2024.kpu.go.id/'
url = "https://pemilu2024.kpu.go.id/pilpres/hitung-suara/11/1105/110507/1105072002/1105072002001"

# Perform the scraping
scrape_website(url)
