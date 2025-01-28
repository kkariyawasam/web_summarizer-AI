
# WebSummarizer AI

WebSummarizer AI is a tool that extracts and summarizes content from websites using advanced AI technology. This repository includes the backend setup and provides guidance to integrate with the frontend.

## Features
- Extracts content from JavaScript-rendered websites.
- Summarizes website content using AI.
- Provides an easy-to-use frontend interface.

---

## Frontend Guide
The frontend for this project is hosted on the following link:
[WebSummarizer AI Frontend](https://websummarywithai.blogspot.com/2025/01/blog-post.html)

### How to Use the Frontend
1. Visit the link above to access the interface.
2. Enter the URL of the website you want to summarize in the provided input field.
3. Submit the form to get the summary.

---

## Backend Guide
The backend is built using Flask and Selenium for dynamic website crawling, and OpenAI for AI-driven summarization.

### Prerequisites
- Python 3.8 or higher
- Install the required Python packages:
  ```bash
  pip install flask undetected-chromedriver selenium beautifulsoup4 python-dotenv openai
  ```
- Ensure you have Google Chrome installed for Selenium.

### Setting Up the Backend
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Create a `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key
   ```
3. Run the backend server:
   ```bash
   python app.py
   ```
4. The backend will start on `http://127.0.0.1:5000`.

---

## Integration Guide
1. Ensure the backend server is running.
2. Access the frontend through the link provided.
3. Enter the URL of the website you want to summarize.
4. The frontend will send a request to the backend and display the summary.

---

## Notes
- Some websites may not be supported due to restrictions or technical limitations.
- If a website fails to load, you will see a relevant error message.
- Ensure your environment allows Chrome to run without interruption.

---

## License
This project is licensed under the MIT License. Feel free to contribute or customize as needed.

---

## Support
For any issues or suggestions, please create an issue in this repository or contact the maintainer.
