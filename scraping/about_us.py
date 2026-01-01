import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://sunbeaminfo.in/about-us"

def about_scrape_to_txt(output_file="text_files/about_us_data.txt"):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        headers = driver.find_elements(
            By.XPATH,
            "//a[@data-toggle='collapse']"
        )

        with open(output_file, "w", encoding="utf-8") as f:

            for header in headers:
                title = header.text.strip()
                if not title:
                    continue

                # Open accordion
                driver.execute_script("arguments[0].click();", header)
                time.sleep(0.5)

                collapse_id = header.get_attribute("href").split("#")[-1]
                content_div = driver.find_element(By.ID, collapse_id)

                f.write("=" * 80 + "\n")
                f.write(f"{title}\n")
                f.write("=" * 80 + "\n\n")

                # List items
                for li in content_div.find_elements(By.XPATH, ".//li"):
                    text = li.text.strip()
                    if text:
                        f.write(f"- {text}\n")

                # Paragraphs
                for p in content_div.find_elements(By.XPATH, ".//p"):
                    text = p.text.strip()
                    if text:
                        f.write(f"{text}\n")

                # Tables
                tables = content_div.find_elements(By.XPATH, ".//table")
                for table in tables:
                    f.write("\n[Table Data]\n")
                    rows = table.find_elements(By.XPATH, ".//tr")
                    for row in rows:
                        cols = [
                            c.text.strip()
                            for c in row.find_elements(By.XPATH, ".//th | .//td")
                        ]
                        if cols:
                            f.write(" | ".join(cols) + "\n")

                f.write("\n\n")

        print(f"✅ Data saved to {output_file}")

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_to_txt()