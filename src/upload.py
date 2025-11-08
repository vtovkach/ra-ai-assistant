# This source file will contain logic to fill the online form based on the notes 

import os
import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import time 
from mytypes import *
from exceptions.FormExceptions import *

# Load environment variables 
load_dotenv()

# Opened Sessions 
playwright = None
browser = None
context = None
page = None

def log_error(e):
    with open("logs/log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {repr(e)}\n")

def login() -> bool:

    """
    Authenticate user and save session if successful.

    Returns:
        bool: True if login succeeded or session reused, False otherwise.
    """

    global playwright, browser, context, page

    playwright = sync_playwright().start()
    browser = playwright.firefox.launch(headless=False)

    # If session file exists, try to reuse it
    if os.path.exists("session/session.json"):
        print("🔄 Using saved session...")
        context = browser.new_context(storage_state="session/session.json")
        page = context.new_page()
        page.goto(os.getenv("DASH_URL"))

        # Check if still logged in
        if page.url.startswith(os.getenv("LOGIN_URL")):
            print("⚠️ Saved session expired — re-authenticating.")
            return fresh_login()
        else:
            print("✅ Session still valid — user is logged in.")
            return True
    else:
        return fresh_login()

def fresh_login() -> bool:

    """
    Perform a manual login and save the authenticated session.

    Opens a new browser context at the login page, pauses for the user
    to complete authentication (including possible 2FA), then verifies
    whether login succeeded. If successful, saves cookies and localStorage
    to `session.json` for reuse in future runs.

    Args:
        browser: The active Playwright browser instance.

    Returns:
        bool: True if login succeeded and session was saved; False otherwise.
    """

    global context, page, browser

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

    if page.url in (os.getenv("DASH_URL"), os.getenv("FORM_URL")):
        print("✅ Authorization confirmed — user is logged in.")
        # Save the session state here
        context.storage_state(path="session/session.json")
        print("💾 Session saved to session.json.")
        return True
    else:
        print("❌ Authorization failed — still on login page or element not found.")
        return False


def close_connection():

    """
    Gracefully close all Playwright resources and persist the session state.

    Saves the current browser context (cookies and localStorage) to `session.json`
    so that future runs can restore the logged-in session. Closes the context,
    browser, and Playwright engine in order, ensuring a clean shutdown even if
    an exception occurs.

    This function should be called at normal program exit or when an operation
    completes successfully — not for crash recovery or forced teardown.

    Exceptions:
        Any errors during shutdown are caught and printed in order to 
        prevent program termination.
    """

    global playwright, browser, context, page
    try:
        if context:
            context.storage_state(path="session/session.json")
            print("💾 Session saved before exit.")
            context.close()
        if browser:
            browser.close()
        if playwright:
            playwright.stop()
        print("👋 Connection closed cleanly.")
    except Exception as e:
        print(f"Error closing connection: {e}")
    finally:
        playwright = browser = context = page = None


def end_session():

    """ 
    Forcefully terminate all Playwright resources and clear session data.

    This function performs a complete teardown by closing the browser context,
    browser instance, and Playwright engine. It also clears cookies to ensure
    no session data is preserved between runs.

    Unlike `close_connection()`, this function is meant for crash recovery,
    error cleanup, or full reset scenarios where persistence is not desired.

    All exceptions are logged to `log.txt` instead of being raised to prevent
    shutdown failures from halting the program.
    
    """

    global playwright, browser, context, page

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


def submitForm(chat: Chat) -> bool:

    """
    Fill and submit the resident interaction form using Playwright automation.

    Ensures an active Playwright session, navigates to the target form,
    and programmatically fills each field based on the provided Chat object.
    Handles login automatically if the session is missing or expired.

    Args:
        chat (Chat): Contains resident name, date, answers, frequency, and resources.

    Returns:
        bool: True if the form submission completes successfully, False otherwise.
    """

    if not all([playwright, browser, context, page]):
        close_connection()
        if not login():
            end_session()
            raise FormFail("Failed to login.")

    # Navigate to the form
    page.goto(os.getenv("FORM_URL"))
    time.sleep(2)

    if page.url != os.getenv("FORM_URL"):
        log_error(f"Failed to open form page.")
        raise FormFail("Failed to open form page.")

    # Resident name
    try:
        page.click('input.forms-tag-search-input[placeholder="Tag Residents"]')
        page.keyboard.type(chat.name)
        page.wait_for_selector('.forms-subscriptions-search-result-row', state='visible', timeout=5000)
        time.sleep(2.5)
        page.click('.forms-subscriptions-search-result-row:first-child')
    except Exception as e:
        log_error(f"Error selecting resident's name: {e}")
        raise FormFail("Failed to select resident from the list.")

    # Date
    try:
        page.keyboard.press("Tab")
        page.fill('input.elm-datepicker--input[aria-label="Enter date for Date of Interaction"]', chat.date)
    except Exception as e:
        log_error(f"Error selecting date: {e}")
        raise FormFail("Failed to input the date.")
    
    # Answers
    try:
        for ans in chat.answers:
            page.keyboard.press("Tab")
            page.keyboard.type(ans)
    except Exception as e:
        log_error(f"Error filling answers: {e}")
        raise FormFail("Failed to input answers.")

    # Frequency
    try:
        page.click(f'[aria-label="{chat.frequency}"]')
    except Exception as e:
        log_error(f"Error selecting frequency: {e}")
        FormFail("Failed to select frequency.")

    # Resources
    try:
        for res in chat.resources:
            if res == "N/A":
                page.click('[aria-label="No resources were discussed during this chat"]')
            else:
                page.click(f'[aria-label="{res}"]')
    except Exception as e:
        log_error(f"Error selecting resources: {e}")
        raise FormFail("Failed to select resources.")
        
    # Additional resources
    try:
        page.click('[aria-label="Enter text for If you selected OTHER on the Resources question above, please elaborate."]')
        page.keyboard.type(chat.additionalResources)
        page.keyboard.press("Tab")
    except Exception as e:
        log_error(f"Error filling additional resources: {e}")
        raise FormFail("Failed to input additional resources.") 

    
    '''''
    # Submit
    try:
        page.click('button[title="Click to submit form"]')
    except Exception as e:
        log_error(f"Error clicking submit button: {e}")
        raise FormFail("Failed to submit form.")
    
    # Wait and check if new submission page is loaded, if not raise an exception 
    time.sleep(2)
    if page.url == os.getenv("FORM_URL"):
        raise FormFail("Failed to submit form. Not all inputs fields were answered.")
    '''''

    return True


## The following code is used only for testing 

if __name__ == "__main__":
    loginStatus = login()
    
    if loginStatus:
        print("✅ Session is opened.")
    
    while loginStatus:
        user_input = input("Test Input: ")
        if(user_input == "exit"):
            break; 
        else:
            submitForm(None)
    
    if loginStatus:
        close_connection()