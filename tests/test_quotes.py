from playwright.sync_api import Page, expect

def quotes_page_has_title(page: Page):
    page.goto("http://127.0.0.1:5001/quoteshtml")

    title = page.locator("header")
    expect(title).to_have_text("My favourite quotes")