from playwright.sync_api import sync_playwright
import os
import json
from datetime import datetime

# URLs to test
qubed_urls = [
    "https://qubed.pk/",
    "https://qubed.pk/about",
    "https://qubed.pk/contact-quebed",
    "https://qubed.pk/quebed-reviews",
    "https://suite2.qubed.pk/",
    "https://vt.qubed.pk/"
]

# Prepare folders
os.makedirs("screenshots", exist_ok=True)
os.makedirs("videos", exist_ok=True)
os.makedirs("results", exist_ok=True)

# Store results
test_results = []

def test_qubed_pages():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for url in qubed_urls:
            domain = url.replace("https://", "").replace("/", "_")
            print(f"\n🔍 Testing: {url}")
            result = {
                "url": url,
                "status": "PASS",
                "errors": [],
                "video": ""
            }

            try:
                # Create context with video
                context = browser.new_context(
                    record_video_dir="videos/",
                    viewport={"width": 1280, "height": 800}
                )
                page = context.new_page()
                page.goto(url, timeout=20000)
                page.wait_for_load_state("networkidle")


                # Check WhatsApp button
                try:
                    if page.locator("a[href*='wa.me']").is_visible():
                        page.locator("a[href*='wa.me']").hover()
                except Exception as e:
                    result["errors"].append("WhatsApp button error")

                # Hover buttons
                try:
                    buttons = page.locator("button")
                    for i in range(buttons.count()):
                        buttons.nth(i).hover()
                except Exception as e:
                    result["errors"].append("Hover failed")

                # Fill forms
                try:
                    inputs = page.locator("input, textarea")
                    for i in range(inputs.count()):
                        inputs.nth(i).fill("Test data")
                    submit_btns = page.locator("button[type='submit'], input[type='submit']")
                    for i in range(submit_btns.count()):
                        submit_btns.nth(i).click()
                except Exception as e:
                    result["errors"].append("Form fill/submit failed")

                # Responsive test
                try:
                    mobile_context = browser.new_context(
                        viewport={"width": 390, "height": 844},
                        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
                        record_video_dir="videos/"
                    )
                    mobile_page = mobile_context.new_page()
                    mobile_page.goto(url)
                    mobile_page.wait_for_timeout(2000)
                    mobile_context.close()
                except Exception:
                    result["errors"].append("Responsive/mobile test failed")

                context.close()

            except Exception as e:
                result["status"] = "FAIL"
                result["errors"].append(str(e))
            finally:
                test_results.append(result)

        browser.close()

        # Save results as JSON
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        result_file = f"results/test_results_{timestamp}.json"
        with open(result_file, "w") as f:
            json.dump(test_results, f, indent=2)

        # Summary
        print("\n\n✅ TEST SUMMARY")
        for res in test_results:
            print(f"\n🔗 {res['url']}")
            print(f"   Status: {res['status']}")
            if res["errors"]:
                print(f"   Errors: {res['errors']}")

        print(f"\n📄 Full results saved to: {result_file}")

if __name__ == "__main__":
    test_qubed_pages()
