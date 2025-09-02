# InfoSphere – Profile Extractor

A web application that extracts and displays user profile information from public websites such as GitHub, blogs, and team pages. 
⚠️ **Note:** Blocked domains (like LinkedIn) are intentionally excluded.

---

## ✨ Features
- Input one or more URLs and extract public profile details (name, bio, image, social links).
- Displays profiles in a **modern card layout**.
- Export results as JSON.
- Copy individual profile JSON directly.
- Works with GitHub, blogs, or public team pages.

---

## 💻 Tech Stack
- **Backend:** Python, Flask, BeautifulSoup4, Requests
- **Frontend:** HTML, TailwindCSS, Vanilla JS
- **Other:** CORS enabled for frontend-backend communication

---

## 🚀 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Samyuktha-Pari/infosphere-profile-extractor.git](https://github.com/Samyuktha-Pari/infosphere-profile-extractor.git)
    cd infosphere-profile-extractor
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # For macOS/Linux:
    source venv/bin/activate
    # For Windows:
    venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Navigate to the backend directory and run the application:**
    ```bash
    cd backend
    flask run
    ```
    The application will be accessible at `http://127.0.0.1:5000/`.
