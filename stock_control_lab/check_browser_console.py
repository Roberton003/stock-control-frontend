import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Collect console messages
        messages = []
        page.on("console", lambda msg: messages.append(msg.text))
        
        await page.goto("http://localhost:3000")
        
        # Wait for a bit to make sure all messages are captured
        await asyncio.sleep(3)
        
        await browser.close()
        
        print("--- CONSOLE MESSAGES ---")
        for msg in messages:
            print(msg)

asyncio.run(main())
