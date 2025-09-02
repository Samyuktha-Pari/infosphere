from flask import Flask, request, jsonify, send_from_directory
import requests
from extractor import extract_profiles
from flask_cors import CORS

# Initialize Flask app without static folder
app = Flask(__name__)
CORS(app)

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