from playwright.sync_api import Playwright, expect


def test_main_page_load(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8501/")
    page.get_by_text("Running...").wait_for(state="detached")
    expect(
        page.get_by_test_id("stHeadingWithActionElements").get_by_role(
            "heading", name="ExtroPlanner"
        )
    ).to_be_visible()

    context.close()
    browser.close()


def test_viewing_latest_data(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8501/")
    page.get_by_text("Running...").wait_for(state="detached")
    page.get_by_test_id("stRadio").get_by_text("Kasetsart University").click()
    page.get_by_text("Running...").wait_for(state="detached")
    expect(
        page.get_by_test_id("stTable")
        .locator("div")
        .filter(
            has_text="locationwind_speedwind_degreepressuretemperaturehumiditycloud_percentrainfallwea"
        )
    ).to_be_visible()
    expect(page.locator("tbody")).to_contain_text("Kasetsart University")
    page.get_by_text("Nak Niwat").click()
    page.get_by_text("Running...").wait_for(state="detached")
    expect(
        page.get_by_test_id("stTable")
        .locator("div")
        .filter(
            has_text="locationwind_speedwind_degreepressuretemperaturehumiditycloud_percentrainfallwea"
        )
    ).to_be_visible()
    expect(page.locator("tbody")).to_contain_text("Nak Niwat 48")

    context.close()
    browser.close()
