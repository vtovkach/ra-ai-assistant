# This source file will contain logic to fill the online form based on the notes 

import os
import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from mytypes import Chat
import time 

# Load environment variables 
load_dotenv()

# Opened Sessions 
playwright = None
browser = None
context = None
page = None

def login() -> bool:

    """Authenticate user and save session if successful.

    Returns:
        bool: True if login succeeded or session reused, False otherwise.
    """

    global playwright, browser, context, page

    playwright = sync_playwright().start()
    browser = playwright.firefox.launch(headless=False)

    # If session file exists, try to reuse it
    if os.path.exists("session.json"):
        print("🔄 Using saved session...")
        context = browser.new_context(storage_state="session.json")
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

    """Perform a manual login and save the authenticated session.

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
        context.storage_state(path="session.json")
        print("💾 Session saved to session.json.")
        return True
    else:
        print("❌ Authorization failed — still on login page or element not found.")
        return False


def close_connection():

    """Gracefully close all Playwright resources and persist the session state.

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
            context.storage_state(path="session.json")
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

    """Forcefully terminate all Playwright resources and clear session data.

    This function performs a complete teardown by closing the browser context,
    browser instance, and Playwright engine. It also clears cookies to ensure
    no session data is preserved between runs.

    Unlike `close_connection()`, this function is meant for crash recovery,
    error cleanup, or full reset scenarios where persistence is not desired.

    All exceptions are logged to `log.txt` instead of being raised to prevent
    shutdown failures from halting the program.
    """

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


def submitForm(chat : Chat) -> bool:
    if not all([playwright, browser, context, page]):
        close_connection()
        # Perform Logging In
        if not login():
            return False
    
    # Go to target webpage 
    page.goto(os.getenv("FORM_URL"))

    time.sleep(2)

    try:
        ## Fill Resident Name Field 
        page.click('input.forms-tag-search-input[placeholder="Tag Residents"]')
        page.keyboard.type('Vadym Tovkach', delay=50)
        time.sleep(1)
        page.wait_for_selector('.forms-subscriptions-search-result-row', state='visible', timeout=10000)
        time.sleep(1)
        page.click('.forms-subscriptions-search-result-row:first-child')
        
        ## Fill Date 
        #page.click('input.elm-datepicker--input[aria-label="Enter date for Date of Interaction"]')
        page.keyboard.press("Tab")
        page.fill('input.elm-datepicker--input[aria-label="Enter date for Date of Interaction"]', '11/03/2025')

        ### It will be loop that will click tab for each question 

        # Fill Question 1
        ##page.click('textarea.forms-textarea.md-textarea[aria-label="Connections and Community"]')
        page.keyboard.press("Tab")
        page.keyboard.type("Here is my responce for question 1. Merovingian!")

        # Fill Question 2
        page.keyboard.press("Tab")
        page.keyboard.type("Here is my responce for question 2. Merovingian!")

        # Fill Question 3
        page.keyboard.press("Tab")
        page.keyboard.type("Here is my responce for question 3. Merovingian!")

        # Frequency
        # Has a list of academic resources and use them as parameter to "arial-label="x"" x is academic resource
        #
        frequencies = ["Frequency: Daily", 
                       "Frequency: Weekly", 
                       "Frequency: Monthly", 
                       "Frequency: Rarely", 
                       "Ghost Resident"
                       ]

        for freq in frequencies:
            page.click(f'[aria-label="{freq}"]')

        # Resources 
        resources = ["Academic Advisor",
                    "Bobcat Bounty",
                    "Career Services",
                    "Counseling Center",
                    "Disability Services",
                    "Referral to LLC Staff",
                    "Residence Director",
                    "Student Health Center",
                    "Student Learning Assistance Center",
                    "No resources were discussed during this chat",
                    "OTHER - please elaborate in next questions"
                    ]
        
        for res in resources:
            page.click(f'[aria-label="{res}"]')
        
        # Additional Resources 
        page.click('[aria-label="Enter text for If you selected OTHER on the Resources question above, please elaborate."]')
        page.keyboard.type("Here is additional resources I talked about!")

    except (Exception) as e:
        print("Exception occured when filling the form! Exception: " + str(e))

    return True


## The following code is used only for testing 

if __name__ == "__main__":
    if login():
        print("✅ Session is opened.")

    while True:
        user_input = input("Test Input: ")
        if(user_input == "exit"):
            break; 
        else:
            submitForm(None)
            

    close_connection()