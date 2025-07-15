from playwright.async_api import async_playwright
import asyncio
import os, shutil


# first delete the previews recorded video 
if os.path.exists("video"):
    shutil.rmtree("video")

# create a folder for new video
os.makedirs("video",exist_ok=True)

# extract all pages link of qubed.pk and then test one by one
async def extract_links():
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=False)

    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://qubed.pk", wait_until="load")
    await page.wait_for_load_state("networkidle")

    # extract all links from page
    links = await page.eval_on_selector_all(
        "a", "elements => elements.map(el => el.href)"
    )
    await browser.close()
    return links


# this one function are checking every page btn,forms,hover, and also with responsive and record video
async def test_qubed_pages():
    # get
    raw_links = await extract_links()
    links = list(set(link.strip() for link in raw_links))  

    # again intialize browser and context with video
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=False)
    context = await browser.new_context(
        record_video_dir = "video/",
        viewport = {
            "width":1280,
            "height":800
        }
    )
    page = await context.new_page()
    
    # checking every page
    try:
        for link in links:
            await page.goto(link, wait_until="load")
            print(f"🔍 Testing : {link}")
            result = {
            "url":link,
            "status":"PASS",
            "errors":[]
            }

            # check whatsapp button
            if await page.locator("a[href*='wa.me']"):
                try:
                    await page.locator("a[href*='wa.me']")
                    await page.eval_on_selector("a[href*='wa.me']",
                    """
                    el => el.scrollIntoView({behave:'smooth', block: 'center'})
                    """)
                    asyncio.sleep(2)
                except Exception as e:
                    result["errors"].append(f"WhatsApp button error\n \n {e}")

            # Hover button
            try:
                buttons = await page.locator("button")
                for i in range(buttons.count()):
                    await page.eval_on_selector(buttons.nth(i),
                    """
                    el => el.scrollIntoView({behave:'smooth', block: 'center'})
                    """)
                    asyncio.sleep(2)
                    buttons.nth(i).hover() 
            except Exception as e:
                result["error"].append(f"Hover error \n \n {e}")

            # fill form
            try:
                inputs = await page.locator("input","textarea")
                for i in range(inputs.count()):
                    await page.eval_on_selector(inputs.nth(i),
                    """
                    el => el.scrollIntoView({behave:'smooth', block: 'center'})
                    """)
                    asyncio.sleep(2)
                    inputs.nth(1).fill("Test Data")
                submit_btns = await page.locator("input[type='submit']", "button[type='submit']")
                for i in range(submit_btns.count()):
                    await page.eval_on_selector(submit_btns.nth(i),
                    """
                    el => el.scrollIntoView({behave:'smooth', block: 'center'})
                    """)
                    asyncio.sleep(2)
                    submit_btns.nth(i).click()
            except Exception as e:
                result["error"].append(f"Form fill/Submit failed\n \n {e}")
            


            # responsive test
            await page.set_viewport_size({"width":375,"height":780})
            await page.goto(link, wait_until="load")
            await page.wait_for_timeout(30000)
            
            
            # check whatsapp button
            if await page.locator("a[href*='wa.me']"):
                try:
                    await page.locator("a[href*='wa.me']")
                    await page.eval_on_selector("a[href*='wa.me']",
                    """
                    el => el.scrollIntoView({behave:'smooth', block: 'center'})
                    """)
                    asyncio.sleep(2)
                except Exception as e:
                    result["errors"].append(f"WhatsApp button error in responsive mode\n \n {e}")

            # Hover button
            try:
                buttons = await page.locator("button")
                for i in range(buttons.count()):
                    await page.eval_on_selector(buttons.nth(i),
                    """
                    el => el.scrollIntoView({behave:'smooth', block: 'center'})
                    """)
                    asyncio.sleep(2)
                    buttons.nth(i).hover   
            except Exception as e:
                result["error"].append(f"Hover error in responsive mode \n \n {e}")

            # fill form
            try:
                inputs = await page.locator("input","textarea")
                for i in range(inputs.count()):
                    await page.eval_on_selector(inputs.nth(i),
                    """
                    el => el.scrollIntoView({behave:'smooth', block: 'center'})
                    """)
                    asyncio.sleep(2)
                    inputs.nth(1).fill("Test Data")
                submit_btns = await page.locator("input[type='submit']", "button[type='submit']")
                for i in range(submit_btns.count()):
                    submit_btns.nth(i).click()
            except Exception as e:
                result["error"].append(f"Form fill/Submit failed in responsive\n \n {e}")

    except Exception as e:
        result["status"].append(f"Fail \n \n {e}")
    
    await browser.close()

asyncio.run(test_qubed_pages())



