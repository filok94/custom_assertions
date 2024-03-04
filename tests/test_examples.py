from datetime import datetime, timedelta

from playwright.sync_api import Page

from main import custom_expect


def test_example(page: Page):
    # Waiting for the time to become two seconds longer
    page.goto('https://www.utctime.net/', wait_until='domcontentloaded')
    custom_expect(page.locator('#time2')).to_have_time('after', datetime.utcnow() + timedelta(seconds=2))
    # Waiting for integer to be more than five
    page.goto('https://time.is/UTC', wait_until='domcontentloaded')
    custom_expect(page.locator('#bcdigit6')).to_have_int('gt', 5)
