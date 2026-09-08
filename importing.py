from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def fetch_dynamic_page(url):
    with sync_playwright() as p:
        # Launch a headless browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Loading page and waiting for JavaScript...")
        # wait_until="networkidle" ensures we don't grab the HTML until the JS is done
        page.goto(url, wait_until="networkidle")
        
        # Grab the fully rendered HTML
        html = page.content()
        browser.close()
        return html

# Put your Bhajan Mala URL here
test_url = "https://bhajanmala.com/"

raw_html = fetch_dynamic_page(test_url)
soup = BeautifulSoup(raw_html, 'html.parser')

# Now let's just print the whole text of the page to prove it loaded
print("Page successfully rendered. Here is a snippet of the text:")
print(soup.text[:500])