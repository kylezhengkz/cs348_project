from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def scrolling_scrape(page, scroll_container_selector, item_selector, parse_fn, pause=1.5, max_scrolls=10):
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