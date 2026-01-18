from playwright.sync_api import sync_playwright

AUTH_STATE_PATH = "auth/storage_state.json"

def search_jobs(base_url, keywords):
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            storage_state=AUTH_STATE_PATH
        )

        page = context.new_page()
        page.goto(base_url, wait_until="networkidle")

        # Click on Grade Level
        #grade_level = page.locator(".pds-panels.filter-component input[placeholder='Grade Level']")
        grade_level = page.locator("#jobPanelDetailsTab > div > div > div.pds-panels.filter-component > div:nth-child(4) > div > div > pds-icon")
        grade_level.click()

        # Select Secondary Grade Level
        page.locator('input[name="Secondary"]').wait_for(state="visible")
        page.locator('input[name="Secondary"]').click()

        #externalJobSearchBox-input
        search_box = page.locator("#externalJobSearchBox-input")
        search_box.fill(" ".join(keywords))
        search_box.press("Enter")
        page.wait_for_load_state("networkidle")

        # Get all of the elements in the joblist panel'
        job_cards = page.locator("#jobListPanel > div")
        count = job_cards.count()

        #job_cards = page.locator("#joblist-div > div")
        #count = job_cards.count()

        for i in range(count):
            card = job_cards.nth(i)

            title_el = card.locator(".card-title > div")
            #title = title_el.inner_text().strip()
            if title_el.count() == 0:
                continue
            title = title_el.inner_text()
            if not any(k.lower() in title.lower() for k in keywords):
                continue

            card_info = card.locator(".card-body > p")
            school_name = ""
            location = ""
            date = ""
            if card_info.nth(0):
                school_name = card_info.nth(0).inner_text().strip()
            if card_info.nth(1):
                location = card_info.nth(1).inner_text().strip()
            if card_info.nth(2):
                date = card_info.nth(2).inner_text().strip()
            jobs.append({
                "title": title,
                #"url": title_el.get_attribute("href"),
                "school": school_name,
                #"location": safe_text(card, ".job-location"),
                "location": location,
                #"school": safe_text(card, ".job-school")
                "date": date
            })

        browser.close()

    return jobs

def safe_text(parent, selector):
    try:
        return parent.locator(selector).inner_text().strip()
    except:
        return "N/A"
