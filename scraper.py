"""Scrape SHL Individual Test Solutions catalog."""
import json
import time
import httpx
from bs4 import BeautifulSoup

BASE = "https://www.shl.com/solutions/products/product-catalog/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def scrape_catalog_page(url: str, client: httpx.Client) -> tuple[list[dict], str | None]:
    """Scrape one page of catalog results. Returns (items, next_page_url)."""
    resp = client.get(url, headers=HEADERS, follow_redirects=True, timeout=30)
    soup = BeautifulSoup(resp.text, "lxml")
    
    items = []
    # Find the product table
    table = soup.find("table")
    if not table:
        # Try finding product cards/links instead
        print(f"No table found at {url}")
        return items, None
    
    rows = table.find_all("tr")[1:]  # skip header
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue
        
        link = cols[0].find("a")
        name = link.get_text(strip=True) if link else cols[0].get_text(strip=True)
        href = link["href"] if link and link.get("href") else ""
        if href and not href.startswith("http"):
            href = "https://www.shl.com" + href
        
        # Check for checkmarks (usually images or specific classes)
        def has_check(td):
            return bool(td.find("span", class_=lambda c: c and "catalogue__circle" in c and "--yes" in c)) or \
                   bool(td.find("img")) or "✓" in td.get_text() or "Yes" in td.get_text()
        
        remote = has_check(cols[1]) if len(cols) > 1 else False
        adaptive = has_check(cols[2]) if len(cols) > 2 else False
        test_type = cols[3].get_text(strip=True) if len(cols) > 3 else ""
        languages = cols[4].get_text(strip=True) if len(cols) > 4 else ""
        
        items.append({
            "name": name,
            "url": href,
            "remote_testing": remote,
            "adaptive_irt": adaptive,
            "test_type": test_type,
            "languages": languages
        })
    
    # Find next page link
    next_link = soup.find("a", class_=lambda c: c and "next" in c.lower()) if soup else None
    if not next_link:
        pagination = soup.find("div", class_=lambda c: c and "pagination" in str(c).lower())
        if pagination:
            links = pagination.find_all("a")
            for a in links:
                if "next" in a.get_text(strip=True).lower() or "›" in a.get_text() or ">" == a.get_text(strip=True):
                    next_link = a
                    break
    
    next_url = None
    if next_link and next_link.get("href"):
        next_url = next_link["href"]
        if not next_url.startswith("http"):
            next_url = "https://www.shl.com" + next_url
    
    return items, next_url


def scrape_product_detail(url: str, client: httpx.Client) -> dict:
    """Scrape individual product page for extra detail."""
    try:
        resp = client.get(url, headers=HEADERS, follow_redirects=True, timeout=20)
        soup = BeautifulSoup(resp.text, "lxml")
        desc_el = soup.find("meta", {"name": "description"})
        description = desc_el["content"] if desc_el and desc_el.get("content") else ""
        
        # Look for any additional structured info
        keywords_el = soup.find("meta", {"name": "keywords"})
        keywords = keywords_el["content"] if keywords_el and keywords_el.get("content") else ""
        
        return {"description": description, "keywords": keywords}
    except Exception as e:
        print(f"  Error scraping {url}: {e}")
        return {"description": "", "keywords": ""}


def try_paginated_scrape(client: httpx.Client) -> list[dict]:
    """Try scraping with pagination parameters."""
    all_items = []
    # Type=1 typically means Individual Test Solutions
    for start in range(0, 500, 12):
        url = f"{BASE}?type=1&start={start}&sz=12"
        print(f"Trying {url}...")
        items, _ = scrape_catalog_page(url, client)
        if not items:
            print(f"  No items at start={start}, stopping.")
            break
        all_items.extend(items)
        print(f"  Found {len(items)} items (total: {len(all_items)})")
        time.sleep(0.5)
    return all_items


def main():
    client = httpx.Client()
    
    print("=== Scraping SHL Individual Test Solutions ===")
    
    # Try direct page first
    items, next_url = scrape_catalog_page(BASE + "?type=1", client)
    
    if items:
        all_items = items
        page = 2
        while next_url:
            print(f"Page {page}: {next_url}")
            items, next_url = scrape_catalog_page(next_url, client)
            all_items.extend(items)
            page += 1
            time.sleep(0.5)
    else:
        print("Direct scrape failed, trying paginated approach...")
        all_items = try_paginated_scrape(client)
    
    if not all_items:
        print("Web scraping returned no table data. The site may be JS-rendered.")
        print("Will use pre-built catalog instead.")
        return
    
    # Enrich with product details
    print(f"\nEnriching {len(all_items)} products with details...")
    for i, item in enumerate(all_items):
        if item["url"]:
            print(f"  [{i+1}/{len(all_items)}] {item['name']}")
            detail = scrape_product_detail(item["url"], client)
            item.update(detail)
            time.sleep(0.3)
    
    # Save
    with open("shl_catalog.json", "w", encoding="utf-8") as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)
    
    print(f"\nDone! Saved {len(all_items)} products to shl_catalog.json")
    client.close()


if __name__ == "__main__":
    main()
