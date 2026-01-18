from playwright.sync_api import sync_playwright

AUTH_STATE_PATH = "auth/storage_state.json"

def login_and_save_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # MUST be visible
        context = browser.new_context()

        page = context.new_page()
        page.goto("https://lcps.schoolspring.com/")

        if page.locator("text=Login").count() > 0:
            raise RuntimeError("Session expired")

        print("👉 Please log in manually.")
        print("👉 After login completes, press ENTER here.")

        input()

        context.storage_state(path=AUTH_STATE_PATH)
        browser.close()

        print("✅ Login state saved.")

if __name__ == "__main__":
    login_and_save_state()
