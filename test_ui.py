import time
import urllib.request

import pytest
from playwright.sync_api import Page, expect
import main

BASE_URL = "http://localhost:7861"


@pytest.fixture(scope="session", autouse=True)
def gradio_server():
    main.demo.launch(prevent_thread_lock=True, server_port=7861, share=False)
    # for _ in range(30):
    #     try:
    #         urllib.request.urlopen(BASE_URL)
    #         break
    #     except Exception:
    #         time.sleep(0.5)
    yield
    main.demo.close()


# ── Page load 

def test_page_title(page: Page):
    page.goto(BASE_URL)
    expect(page).to_have_title("Dominant Colour Finder")


def test_heading_visible(page: Page):
    page.goto(BASE_URL)
    expect(page.get_by_role("heading", name="Dominant Colour Finder")).to_be_visible()


def test_ui_components_present(page: Page):
    page.goto(BASE_URL)
    expect(page.locator("#image-input")).to_be_visible()
    expect(page.locator("#top-n-slider")).to_be_visible()
    expect(page.locator("#find-colours-btn")).to_be_visible()
    expect(page.locator("#result-output")).to_be_visible()


# ── Core flow 

def test_upload_image_and_get_results(page: Page):
    page.goto(BASE_URL)
    page.locator("#image-input input[type='file']").set_input_files("test.png")
    page.locator("#find-colours-btn").click()
    # Wait for a hex code to appear in the result panel
    expect(page.locator("#result-output")).to_contain_text("#", timeout=10000)


def test_result_contains_rgb_values(page: Page):
    page.goto(BASE_URL)
    page.locator("#image-input input[type='file']").set_input_files("test.png")
    page.locator("#find-colours-btn").click()
    expect(page.locator("#result-output")).to_contain_text("RGB(", timeout=10000)


def test_result_contains_pixel_count(page: Page):
    page.goto(BASE_URL)
    page.locator("#image-input input[type='file']").set_input_files("test.png")
    page.locator("#find-colours-btn").click()
    expect(page.locator("#result-output")).to_contain_text("pixels", timeout=10000)


# ── Slider 

def test_slider_default_value(page: Page):
    page.goto(BASE_URL)
    slider_input = page.locator("#top-n-slider input[type='number']")
    expect(slider_input).to_have_value("3")


def test_result_respects_top_n(page: Page):
    page.goto(BASE_URL)

    # Set slider to 1
    slider_input = page.locator("#top-n-slider input[type='number']")
    slider_input.fill("1")
    slider_input.press("Enter")

    page.locator("#image-input input[type='file']").set_input_files("test.png")
    page.locator("#find-colours-btn").click()
    page.locator("#result-output").wait_for(timeout=10000)

    # With top_n=1 there should be exactly one swatch block
    swatches = page.locator("#result-output div[style*='border-radius:10px']")
    expect(swatches).to_have_count(1, timeout=10000)
