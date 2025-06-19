from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def scrape_scroll(page, scroll_container_selector, item_selector, parse_fn, pause=1.5, max_scrolls=10):
    collected = set()
    for _ in range(max_scrolls):
        page.eval_on_selector(scroll_container_selector, "el => { el.scrollBy(0, el.clientHeight); }")
        page.wait_for_timeout(pause * 1000)
        
        content = page.content()
        soup = BeautifulSoup(content, "html.parser")
        
        container = soup.select_one(scroll_container_selector)
        if not container:
            continue
        
        items = container.select(item_selector)
        for item in items:
            data = parse_fn(item)
            if data:
                collected.add(data)
    return collected

def scrape_building_names():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://experience.arcgis.com/experience/48e2192807e14d7692d76b505f0a9d82/page/Page-1?views=Building-List")
        page.wait_for_selector('div[data-testid="rich-displayer"]', timeout=10000)
        
        building_names = scrape_scroll(page, ".widget-list-list", 'div[data-testid="rich-displayer"] p', parse_building_name, 1.5, 10)

        browser.close()
    return building_names

def parse_building_name(tag):
    return tag.get_text(strip=True)