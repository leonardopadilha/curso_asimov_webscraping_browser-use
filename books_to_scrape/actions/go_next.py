from browser_use import Browser

async def got_next_page(browser: Browser) -> bool:
    page = await browser.get_current_page()

    if not page:
        return False

    elements = await page.get_elements_by_css_selector("li.next a")

    if elements:
        url = await elements[0].evaluate(' () => this.href')
        await browser.navigate_to(url=url)
        return True

    return False