from playwright.async_api import async_playwright
import asyncio

async def scrape_links():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://qubed.pk/", timeout=60000)
        await page.wait_for_load_state('networkidle')

        links = await page.eval_on_selector_all(
            "a[href]", "elements => elements.map(el => el.href)"
        )

        await browser.close()
        return sorted(set(links))

async def run_test():
    results = []
    links = await scrape_links()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        for link in links:
            try:
                if "+92" not in link:
                    await page.goto(link, timeout=12000)
                    results.append(f"✅ {link}")
            except Exception as e:
                results.append(f"❌ {link} — {e}")

        await browser.close()

    return results

