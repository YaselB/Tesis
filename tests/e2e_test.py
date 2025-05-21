
import pytest
from playwright.sync_api import sync_playwright

URL = "http://localhost:8000/"

@pytest.mark.parametrize("browser_name", ["chromium", "firefox"])
def test_app_loads_in_browser(tmp_path, browser_name):
    with sync_playwright() as p:
        browser = getattr(p, browser_name).launch()
        page = browser.new_page()
        page.goto(URL)
        # Comprueba título o elemento principal
        assert "Hola" in page.content() or page.locator("text=Hola").count() > 0
        browser.close()
