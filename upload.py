# This source file will contain logic to fill the online form based on the notes 

import os
import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load environment variables 
load_dotenv()

# Opened Sessions 
playwright = None
browser = None
context = None
page = None


def login() -> bool:
    global playwright, browser, context, page
    playwright = sync_playwright().start()

    # launch visible browser
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto(os.getenv("LOGIN_URL"))

    print(">>> Please log in and complete 2FA if needed in opened browser.")
    input("Press Enter once you are logged in...")

    try:
        page.reload()
    except Exception as e:
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] {e}\n")
        return False

    print("URL: " + page.url)

    while True:
        if page.url == os.getenv("DASH_URL") or page.url == os.getenv("FORM_URL"):
            print("✅ Authorization confirmed — user is logged in.")
            return True
        else:
            print("❌ Authorization failed — still on login page or element not found.")
            return False


def end_session():
    global playwright, browser, context, page

    def log_error(e):
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] {repr(e)}\n")

    # Close context
    try:
        if context:
            context.clear_cookies()
            context.close()
    except Exception as e:
        log_error(e)
    finally:
        context = None  

    # Close browser
    try:
        if browser:
            browser.close()
    except Exception as e:
        log_error(e)
    finally:
        browser = None  

    # Stop Playwright
    try:
        if playwright:
            playwright.stop()
    except Exception as e:
        log_error(e)
    finally:
        playwright = None  

    page = None
    print("✅ Session closed and cleaned up.")


if __name__ == "__main__":
    if login():
        print("✅ Session is opened.")

    end_session()