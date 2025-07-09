import os
import re
import moviepy.editor  # Required by instagrapi
from flask import Flask, request, render_template, redirect, flash
from instagrapi import Client
import instaloader
import tempfile

app = Flask(__name__)
app.secret_key = "secret-key"

COOKIES_DIR = "cookies"
os.makedirs(COOKIES_DIR, exist_ok=True)

# Get available account usernames from cookies folder
def get_accounts():
    return [f.split(".")[0] for f in os.listdir(COOKIES_DIR) if f.endswith(".pkl")]

# Download Instagram reel using instaloader and return .mp4 path
def download_reel(url):
    match = re.search(r"instagram\.com/reel/([A-Za-z0-9_-]+)", url)
    if not match:
        raise ValueError("Invalid Instagram Reel URL.")
    shortcode = match.group(1)

    temp_dir = tempfile.mkdtemp()
    loader = instaloader.Instaloader(dirname_pattern=temp_dir, save_metadata=False, download_comments=False)
    post = instaloader.Post.from_shortcode(loader.context, shortcode)
    loader.download_post(post, target=temp_dir)

    for file in os.listdir(temp_dir):
        if file.endswith(".mp4"):
            return os.path.join(temp_dir, file)

    raise FileNotFoundError("Reel video not found.")

# Upload using session cookies
def upload_with_cookies(username, video_path, caption):
    cl = Client()
    cookie_path = os.path.join(COOKIES_DIR, f"{username}.pkl")

    if not os.path.exists(cookie_path):
        raise RuntimeError("Cookie file not found.")

    cl.load_settings(cookie_path)
    sessionid = cl.settings.get("authorization_data", {}).get("sessionid")
    if not sessionid:
        raise RuntimeError("Missing session ID in cookies.")

    cl.login_by_sessionid(sessionid)
    cl.clip_upload(video_path, caption)

@app.route("/", methods=["GET", "POST"])
def index():
    accounts = get_accounts()
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        caption = request.form.get("caption", "").strip()
        username = request.form.get("account", "").strip()

        if not url or not caption or not username:
            flash("All fields are required.")
            return redirect("/")

        try:
            video_path = download_reel(url)
            upload_with_cookies(username, video_path, caption)
            flash(f"✅ Successfully posted from @{username}")
        except Exception as e:
            flash(f"❌ {str(e)}")
        return redirect("/")

    return render_template("index.html", accounts=accounts)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
