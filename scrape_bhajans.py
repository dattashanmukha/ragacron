from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

# Make sure to grab a URL from the site while the English toggle is ACTIVE
target_url = "https://bhajanmala.com/bhajans/"

def fetch_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Loading initial page...")
        page.goto(url, wait_until="networkidle")
        
        # CHANGE THIS to the exact text on the button
        button_text = "Load More" 
        
        # Find a button that contains this exact text (case-insensitive)
        load_btn = page.locator(f"button:has-text('{button_text}')")
        
        click_count = 0
        while True:
            # Check if the button is currently visible on the screen
            if load_btn.is_visible():
                print(f"Clicking '{button_text}' (Click #{click_count + 1})...")
                load_btn.click()
                click_count += 1
                
                # Wait 1.5 seconds for the new cards to render before clicking again
                page.wait_for_timeout(1500) 
            else:
                print("Button disappeared. All bhajans should be loaded.")
                break
                
        # Now that everything is expanded, grab the final HTML
        html = page.content()
        browser.close()
        return html

def parse_cards(html):
    soup = BeautifulSoup(html, 'html.parser')
    buttons = soup.find_all('button')
    
    extracted_data = []
    
    for button in buttons:
        title_tag = button.find('h3')
        if not title_tag:
            continue 
            
        # Start a dictionary for this specific bhajan
        bhajan_data = {
            "Title": title_tag.text.strip()
        }
        
        # Loop through every label (dt) in the card
        for dt in button.find_all('dt'):
            key = dt.text.strip() # This will be 'Ragam', 'Deity', 'ID', etc.
            dd = dt.find_next_sibling('dd')
            
            if dd:
                bhajan_data[key] = dd.text.strip()
        
        # Only add it if we actually pulled some details
        if len(bhajan_data) > 1:
            extracted_data.append(bhajan_data)
            
    return extracted_data

# Execute the pipeline
raw_html = fetch_html(target_url)
bhajan_list = parse_cards(raw_html)

# Save the ripped data
with open('bhajan_database.json', 'w', encoding='utf-8') as f:
    json.dump(bhajan_list, f, indent=4)

print(f"Success. Ripped {len(bhajan_list)} bhajans and saved to bhajan_database.json.")