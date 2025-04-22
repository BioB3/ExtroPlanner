from playwright.sync_api import Playwright, expect


def test_visualization_page_load(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8501/")
    page.get_by_text("Running...").wait_for(state="detached")
    page.get_by_role("link", name="Visualization").click()
    expect(page.get_by_role("heading", name="Visualization")).to_be_visible()
    expect(page.locator("#extroplanner")).to_contain_text("Visualization")
    expect(page.get_by_test_id("stHorizontalBlock")).to_be_visible()

    context.close()
    browser.close()


def test_change_shown_attribute(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8501/visualization")
    page.get_by_text("Running...").wait_for(state="detached")
    page.get_by_test_id("stHorizontalBlock").get_by_text("Temperature").click()
    page.get_by_text("Running...").wait_for(state="detached")
    expect(page.get_by_test_id("stPlotlyChart")).to_contain_text("Temperature")
    page.get_by_text("Humidity").click()
    page.get_by_text("Running...").wait_for(state="detached")
    expect(page.get_by_test_id("stPlotlyChart")).to_contain_text("Humidity")
    page.get_by_text("Rainfall").click()
    page.get_by_text("Running...").wait_for(state="detached")
    expect(page.get_by_test_id("stPlotlyChart")).to_contain_text("Rainfall")

    context.close()
    browser.close()
