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

def submitForm(chat : Chat) -> bool:
    if playwright == None or browser == None or context == None or page == None:
        end_session()
        # Perform Logging In
        if login() == False:
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
        page.keyboard.type("Here is my responce for question 1. Merovingian!", delay=50)

        # Fill Question 2
        page.keyboard.press("Tab")
        page.keyboard.type("Here is my responce for question 2. Merovingian!", delay=50)

        # Fill Question 3
        page.keyboard.press("Tab")
        page.keyboard.type("Here is my responce for question 3. Merovingian!", delay=50)

        # Frequency 


        # Resources 


        # Additional Resources 

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
            

    end_session()