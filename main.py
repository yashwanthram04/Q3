from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/outline", response_class=PlainTextResponse)
async def get_country_outline(country: str = Query(..., description="Country name")):
    # Wikipedia URL
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code != 200:
        return PlainTextResponse(f"Could not fetch Wikipedia page for {country}", status_code=404)
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Get page title
    page_title = soup.find('h1', id="firstHeading")
    if page_title:
        title_text = page_title.get_text().strip()
    else:
        # Fallback: use the 'country' parameter
        title_text = country.strip()

    # Extract headings (h2 to h6 only — skip h1 since you already have the title)
    headings = soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6'])

    # Start Markdown
    markdown = "## Contents\n\n"
    markdown += f"# {title_text}\n\n"

    for heading in headings:
        level = int(heading.name[1])
        text = heading.get_text().strip()
        markdown += f"{'#' * level} {text}\n\n"

    return markdown
