from ..web_scrapers.WebScrapingUtils import scrolling_scrape

def scrape_building_names():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://experience.arcgis.com/experience/48e2192807e14d7692d76b505f0a9d82/page/Page-1?views=Building-List")
        page.wait_for_selector('div[data-testid="rich-displayer"]', timeout=10000)
        
        building_names = scrolling_scrape(page, ".widget-list-list", 'div[data-testid="rich-displayer"] p', _parse_building_name, 1.5, 10)

        browser.close()
    return building_names

def _parse_building_name(tag):
    return tag.get_text(strip=True)