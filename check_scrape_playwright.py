import asyncio
from playwright.async_api import async_playwright

async def scrape_himolde():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://www.himolde.no/studier/programmer/', wait_until='networkidle')

        # After waiting for network idle, try to find all h3 tags
        program_titles = await page.locator('h3').all_text_contents()

        if not program_titles:
            print('No h3 titles found with Playwright after network idle.')
        else:
            print('Found h3 titles with Playwright:')
            for title in program_titles:
                print(title.strip())

        await browser.close()

if __name__ == '__main__':
    asyncio.run(scrape_himolde())