# Force Vercel to rebuild
import requests
from flask_cors import CORS
from flask import Flask, request, jsonify, send_from_directory
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

# --- Start of Extractor Code (Combined from extractor.py) ---
def extract_profiles(html, source_url):
    soup = BeautifulSoup(html, "html.parser")

    # --- Detect Site Name ---
    domain = urlparse(source_url).netloc
    site_name = domain.replace("www.", "").split(".")[0].capitalize()

    # --- Title / Name Handling ---
    title_text = soup.title.string.strip() if soup.title else ""
    meta_title = soup.find("meta", attrs={"property": "og:title"})
    page_title = meta_title["content"].strip() if meta_title and meta_title.get("content") else title_text

    author_name = None
    author_meta = soup.find("meta", attrs={"name": "author"})
    if author_meta and author_meta.get("content"):
        author_name = author_meta["content"].strip()

    if "github.com" in source_url.lower() and author_name:
        display_name = f"{page_title} ({author_name})"
    else:
        display_name = page_title
        if author_name and ("blog" in source_url.lower() or "about" in source_url.lower()):
            display_name += f" ({author_name})"

    # --- Bio Extraction ---
    bio = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag and desc_tag.get("content"):
        bio = desc_tag["content"].strip()
    else:
        for p in soup.find_all("p"):
            txt = p.get_text(strip=True)
            if len(txt.split()) > 5:
                bio = txt
                break

    # --- Profile Image ---
    img_tag = soup.find("img", attrs={"src": re.compile(r"https?://")})
    profile_image = img_tag["src"] if img_tag else None

    # --- Social Links ---
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http"):
            links.append(href)
    links = list(dict.fromkeys(links))

    if not (display_name or bio or profile_image or links):
        return None

    return {
        "name": display_name,
        "bio": bio,
        "profile_image": profile_image,
        "social_links": links,
        "source_url": source_url,
        "site_name": site_name
    }
# --- End of Extractor Code ---

# The Flask app must be defined before any of the routes
app = Flask(__name__)
CORS(app)

# This new route will serve your index.html file from the public folder
@app.route("/")
def index():
    return send_from_directory("public", "index.html")

@app.route("/api/extract", methods=["POST"])
def extract():
    data = request.json
    urls = data.get("urls", [])
    results = []

    for url in urls:
        try:
            res = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if res.status_code == 200:
                extracted = extract_profiles(res.text, url)
                if extracted:
                    results.append(extracted)
                else:
                    results.append({"error": f"No profile data found", "source_url": url})
            else:
                results.append({"error": f"Failed with status {res.status_code}", "source_url": url})
        except Exception as e:
            results.append({"error": f"Error fetching {url}: {str(e)}", "source_url": url})

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)