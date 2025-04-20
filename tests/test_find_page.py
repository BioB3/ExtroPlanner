from playwright.sync_api import Playwright, expect


def test_find_page_load(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8501/")
    page.get_by_text("Running...").wait_for(state="detached")
    page.get_by_role("link", name="Find by datetime").click()
    page.get_by_text("Running...").wait_for(state="detached")
    expect(page.get_by_role("heading", name="Find Weather data of a given")).to_be_visible()
    expect(page.locator("#extroplanner")).to_contain_text("Find Weather data of a given time")

    context.close()
    browser.close()

def test_find_closet_data(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8501/find_record")
    page.get_by_text("Running...").wait_for(state="detached")
    page.get_by_text("Kasetsart University").click()
    page.get_by_text("Running...").wait_for(state="detached")
    page.get_by_test_id("stDateInputField").click()
    page.get_by_test_id("stDateInputField").fill("2025/05/05")
    page.get_by_test_id("stTimeInput").locator("div").filter(has_text="HH:mm").nth(2).click()
    page.get_by_role("combobox", name="Select a time, 24-hour format.").fill("10:00")
    page.get_by_role("combobox", name="Select a time, 24-hour format.").press("Enter")
    page.get_by_text("Running...").wait_for(state="detached")
    expect(page.get_by_test_id("stTable").locator("div").filter(has_text="locationwind_speedwind_degreepressuretemperaturehumiditycloud_percentrainfallwea")).to_be_visible()
    expect(page.get_by_role("emphasis")).to_contain_text("The Closest Record to 2025-05-05 10:00:00")
    expect(page.locator("tbody")).to_contain_text("Kasetsart University")

    context.close()
    browser.close()