from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/outline", response_class=PlainTextResponse)
async def get_country_outline(country: str = Query(..., description="Country name")):
    # Build Wikipedia URL (English Wikipedia)
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code != 200:
        return PlainTextResponse(f"Could not fetch Wikipedia page for {country}", status_code=404)
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract headings H1 to H6
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    # Build markdown outline
    markdown = "## Contents\n\n"
    for heading in headings:
        level = int(heading.name[1])  # e.g., h2 -> 2
        text = heading.get_text().strip()
        markdown += f"{'#' * level} {text}\n\n"
    
    return markdown
