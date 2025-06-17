from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/outline", response_class=PlainTextResponse)
async def get_country_outline(country: str = Query(...)):
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code != 200:
        return PlainTextResponse(f"Could not fetch Wikipedia page for {country}", status_code=404)

    soup = BeautifulSoup(response.text, "html.parser")

    # ✅ 1️⃣ Extract true page title FIRST
    page_title = soup.find('h1', id="firstHeading")
    title_text = page_title.get_text().strip() if page_title else country.strip()

    # ✅ 2️⃣ Extract only h2–h6 for sections
    headings = soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6'])

    # ✅ 3️⃣ Build markdown: always starts with # Title
    markdown = f"# {title_text}\n\n"

    for heading in headings:
        text = heading.get_text().strip()
        if text.lower() == "contents":
            continue  # skip TOC heading
        level = int(heading.name[1])
        markdown += f"{'#' * level} {text}\n\n"

    return markdown
