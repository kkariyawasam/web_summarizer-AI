from flask import Flask, request, jsonify
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from openai import OpenAI
from IPython.display import Markdown, display

# Load environment variables (e.g., OpenAI API key)
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI
openai = OpenAI(api_key=openai_api_key)


class WebsiteCrawler:
    def __init__(self, url, wait_time=20, chrome_binary_path=None):
        """
        Initialize the WebsiteCrawler using Selenium to scrape JavaScript-rendered content.
        """
        self.url = url
        self.wait_time = wait_time

        options = uc.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("start-maximized")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        )
        if chrome_binary_path:
            options.binary_location = chrome_binary_path

        self.driver = uc.Chrome(options=options)

        try:
            # Load the URL
            self.driver.get(url)

            # Wait for Cloudflare or similar checks
            time.sleep(10)

            # Ensure the main content is loaded
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.TAG_NAME, "main"))
            )

            # Extract the main content
            main_content = self.driver.find_element(By.CSS_SELECTOR, "main").get_attribute("outerHTML")

            # Parse with BeautifulSoup
            soup = BeautifulSoup(main_content, "html.parser")
            self.title = self.driver.title if self.driver.title else "No title found"
            self.text = soup.get_text(separator="\n", strip=True)

        except Exception as e:
            print(f"Error occurred: {e}")
            self.title = "Error occurred"
            self.text = ""

        finally:
            self.driver.quit()

# Helper functions
system_prompt = (
    "You are an assistant that analyzes the given URL on the web page and provides a short summary, "
    "ignoring text that might be navigation related. Respond in markdown."
)


def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}.\n"
    user_prompt += (
        "The contents of this website are as follows; "
        "please provide a short summary of this website in markdown. "
        "If it includes news or announcements, then summarize these too.\n\n"
    )
    user_prompt += website.text
    return user_prompt


def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)},
    ]


def new_summary(url, chrome_path=None):
    web = WebsiteCrawler(url, 30, chrome_path)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_for(web),
    )
    web_summary = response.choices[0].message.content
   # return Markdown(web_summary)
    return web_summary


# Flask route
@app.route("/endpoint", methods=["POST"])
def handle_input():
    user_input = request.form.get("userInput")  # URL input from user
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        summary = new_summary(user_input)
        html_summary = f"<html><body><h1>Website Summary</h1><pre>{summary}</pre></body></html>"
        return html_summary
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
